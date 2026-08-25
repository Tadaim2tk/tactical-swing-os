# 仕様（起草・未活性）: JP Market Context Bridge (SPEC-JMCB-001)

Phase 27.3。TSO 本体の日次実行結果（市場コンテキストのスコア群）を**変数として日次で保存**し、
日本株スイング判断がそれを**参照できる形にする**ためのブリッジ。

本フェーズは「保存」と「記録」までを扱う。**判断への反映は非活性ゲート（§5）が開くまで行わない。**

---

## 1. 目的と、目的でないもの

### 目的

日本株の個別銘柄も市場全体のレジーム（リスクオン/オフ、円ドル、金利、ボラティリティ）の影響を
受ける。TSO 本体はその市場レジームを既に毎日数値化しているので、日本株側が同じものを
再発明せず**借りられる**状態にする。

### 目的でないもの（重要）

**TSO 本体は「銘柄ごとのナラティブ」を持っていない。** `data/narrative_memory.csv` の
`asset_tags` に実在する値は BTC / SPX / NASDAQ / US10Y / DXY / WTI のみで、日本の個別銘柄も
セクターも一切含まれない。

したがって借りられるのは**市場レベルの文脈**であって、銘柄固有のナラティブではない。構造は次の通り。

| 層 | 担当 | 既存の置き場所 |
|---|---|---|
| 銘柄固有のナラティブ | **JP 側が既に保持** | `jp_swing_signals.csv` の `narrative` / `catalyst_type` / `market_misread` / `narrative_edge` |
| 市場レジーム | **TSO 本体から借用**（本仕様） | `data/market_context_daily.csv`（新設） |

この2つを混同すると「TSO のナラティブ分析が日本株の銘柄選定に効いている」という誤った説明に
なる。効きうるのは市場レジームの層だけである。

---

## 2. 借用元の実体

`src/score_market_context.py` が算出する 10 個のスコア。

```
risk_on_score / risk_off_score / dollar_strength_score / rate_pressure_score /
gold_safe_haven_score / oil_supply_risk_proxy_score / crypto_liquidity_score /
equity_momentum_score / volatility_stress_score / narrative_confidence
```

入力資産は `KEY_ASSETS = BTC, GOLD, WTI, USDJPY, SPX, NASDAQ, DXY, VIX, US10Y`。
このうち **USDJPY・VIX・US10Y・NASDAQ** は日本株に効く理屈が立つ。

---

## 3. タイミング（成立するが余裕は2時間）

| 時刻 (UTC) | 時刻 (JST) | 出来事 |
|---|---|---|
| 21:55 | 06:55 (翌日) | `daily_cycle` が起動しスコアを算出 |
| 22:00頃 | 07:00頃 | スナップショット確定・コミット |
| 00:00 | **09:00** | **東証寄り付き** |

寄りの約2時間前にスナップショットが揃うため、当日の寄り前判断に使える。

**ただしこの2時間の余裕は CI の成否に依存する。** 2026-08-22〜24 には daily cycle が3日連続で
失敗した実績があり（PR #112 インシデント）、その間スコアは更新されなかった。よって
「前日の値をそのまま使う」フォールバックは**禁止**とし、§4 の `status` 列で明示的に劣化を表す。

---

## 4. 出力: `data/market_context_daily.csv`

`results/` 配下は `.gitignore` 対象で永続しないため、JP 側が後から参照する台帳は **`data/` に置き
git 管理下とする**。1日1行の append-only。同一 `context_date` の再実行は冪等（上書きせず同値確認）。

| 列 | 型 | 説明 |
|---|---|---|
| `snapshot_id` | str | `MCTX-YYYY-MM-DD` |
| `context_date` | date | 対象営業日 |
| `generated_at_utc` | datetime | 実際に生成された時刻 |
| `usable_from_utc` | datetime | **この行を判断に使ってよい最早時刻**。lookahead 防止の要 |
| `source_run_id` | str | GitHub Actions の run id（追跡用） |
| `risk_on_score` 〜 `narrative_confidence` | float | §2 の 10 スコア |
| `input_assets_available` | int | `KEY_ASSETS` 9件のうち実際に取得できた数 |
| `staleness_days` | int | 元になった価格バーの鮮度（PR #107 の鮮度ガードを流用） |
| `status` | enum | `ok` / `stale` / `insufficient_data` |

### status の判定

- `ok`: `input_assets_available >= 7` かつ `staleness_days <= 1`
- `stale`: 取得はできたが鮮度が落ちている（`staleness_days >= 2`）
- `insufficient_data`: 上記を満たさない。**値を推測で埋めない**

---

## 5. 非活性ゲート

SPEC-CAR-001（Cross Asset Regime Engine）と同じ方式を踏襲する。以下を**すべて**満たすまで、
本ブリッジは `bridge_status = inactive` とし、**JP の採否判断を一切変更しない**（記録のみ）。

- JP 側の closed 評価が **30 件以上**
- スナップショットの `status = ok` が **20 営業日以上**連続で存在
- Ablation（§6）で改善が確認され、**人間が承認**している

どれか1つでも未達なら `inactive`。この間も §4 の保存と §6 の記録は行う。

---

## 6. JP 側の記録（Phase 27.3-b）

`jp_swing_signals.csv` に**参照の記録**用の列を追加する。判断には効かせない。

| 追加列 | 説明 |
|---|---|
| `mctx_snapshot_id` | 実際に参照したスナップショットの id |
| `mctx_status` | 参照時点の `status`。参照できなければ `insufficient_data` |

### 結合規則（lookahead 安全性）

JP の判断時刻（`decision_date` の寄り前）より **`usable_from_utc` が厳密に前**である最新の
スナップショット1行のみを採用する。条件を満たす行が無ければ `insufficient_data` を記録し、
**直近の行で代用しない**。

この規則は `narrative_memory.csv` の `signal_cutoff_utc` / `allowed_for_signal` /
`cutoff_violation` と同じ思想であり、既存の `src/audit_narrative_lookahead.py` の監査対象に
本ファイルを追加して機械的に検査する。

### 取り込む変数は最初から全部入れない

10 スコアすべてを説明変数にすると、日本株の想定サンプル数（1銘柄スイングで年間数十件規模）に
対して変数が多すぎ、ノイズを拾う。**事前に理由で 3 個に絞る**（後から成績を見て選ぶと後知恵）。

初期採用候補と、その理由:

1. `dollar_strength_score` — 円ドルは日本株の輸出セクターに直結する
2. `volatility_stress_score` — 変動が上がると個別材料が市場全体に飲まれる
3. `risk_on_score` — 小型・材料株はリスク選好局面で伸びやすい

**この3個の選定自体が検証対象であり、正しいと決まったわけではない。**

---

## 7. 検証（Phase 27.3-c）

Phase 29.3 の Ablation 評価フレームを流用し、次の2系統を比較する。

- `jp_technical_only`: 現行の JP 判断のみ
- `jp_plus_market_context`: §6 の3変数を加えたもの

改善が出るまで §5 のゲートは開かない。**改善しなければ、この設計は捨てる。**

---

## 8. 安全条件

- 本ブリッジは**値を保存し記録するだけ**であり、重み更新・自動発注・自動採否には一切関与しない。
- データが揃わない場合は `insufficient_data` を出す。推測で埋めない（honest red over false green）。
- CI 失敗時に前日値で代用しない。劣化は `status` で正直に表す。
- 判断への反映は §5 のゲート通過 + 人間承認の**両方**が必要。

---

## 9. 実装順序

| 段階 | 内容 | 前提 |
|---|---|---|
| 27.3-a | `src/export_market_context_snapshot.py` + `data/market_context_daily.csv` + daily_cycle への組み込み | なし（**今すぐ着手可能**） |
| 27.3-b | JP 側の参照列追加と結合規則、lookahead 監査への登録 | 27.3-a |
| 27.3-c | Ablation による検証 | JP closed 評価 30 件 |

### 27.3-a を先に、かつ早く着手すべき理由

**点在時点（point-in-time）の市場コンテキストは、後から作れない。**

今日の値を明日以降に再構成しようとすると、その時点で確定していなかった情報が混入する
（lookahead 汚染）。日本株の判断が1件も無い現在でも、**スナップショットの蓄積だけは今日から
始める価値がある**。逆に、蓄積を後回しにすると、JP のデータが貯まった時点で「比較対象の
市場コンテキストが存在しない」という理由で 27.3-c の検証自体が実行できなくなる。

これは「実装はデータを待たない」（SPEC_CROSS_ASSET_REGIME.md §7）と同じ判断。

---

## 10. 現時点の既知の制約

- **`data/jp_swing_signals.csv` は 0 行**（2026-08-25 時点）。JP 側の判断実績がまだ存在しないため、
  「市場コンテキストを足すと精度が上がる」という仮説は**現時点では検証不能**。
  27.3-a の価値は蓄積開始であって、精度改善の実証ではない。
- 借用できるのは市場レベルの文脈のみ（§1）。銘柄固有ナラティブの自動化は本仕様の範囲外。
- コスト値は `config/jp_cost_model.json` が unconfigured のままであり、net-R 基準の評価は
  依然として使えない（Phase 26.2 と同じ制約）。

---

## 11. 変更手続き

本仕様の変更は PR で行い、人間の承認を得る。ゲート条件（§5）の緩和は特に、
false-green を生む方向の変更であるため、緩和理由を PR 本文に明記すること。
