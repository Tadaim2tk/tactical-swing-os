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

借りるのは **TSO の観測結果（特徴量）** であって、TSO の判断そのものではない。
TSO が「BTC を買い」と判断したことを日本株に持ち込むのではなく、その判断の材料になった
市場環境の数値だけを、日本株側の銘柄固有分析と**掛け合わせる**。

```
日本株側（銘柄固有）              TSO 側（市場レベル）
企業業績 / 決算 / 材料             リスク選好 / 円ドル環境
銘柄固有ナラティブ        ×        ボラティリティ / 金利
需給 / バリュエーション            米株環境 / マクロ市場ナラティブ
                        ↓
                 日本株の最終評価
```

### 役割分担（層を混同しないための整理）

**TSO 本体は「銘柄ごとのナラティブ」を持っていない。** `data/narrative_memory.csv` の
`asset_tags` に実在する値は BTC / SPX / NASDAQ / US10Y / DXY / WTI のみで、日本の個別銘柄も
セクターも一切含まれない。

これは**本設計を否定する材料ではない**。銘柄固有の層は日本株側が既に持っているので、
TSO からは市場レベルの層だけを借りればよい、という役割分担の確認である。

| 層 | 担当 | 既存の置き場所 |
|---|---|---|
| 銘柄固有のナラティブ | **JP 側が既に保持** | `jp_swing_signals.csv` の `narrative` / `catalyst_type` / `market_misread` / `narrative_edge` |
| 市場レベルの文脈 | **TSO 本体から借用**（本仕様） | `data/market_context_daily.csv`（新設） |

この2つを混同すると「TSO のナラティブ分析が日本株の**銘柄選定**に効いている」という誤った
説明になる。効きうるのは市場レベルの層である。

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

## 4. 出力: `data/market_context_daily.csv`（point-in-time feature store）

`results/` 配下は `.gitignore` 対象で永続しないため、後続研究が参照する台帳は **`data/` に置き
git 管理下とする**。**append-only、1 run 1 行**。同一 run の再実行は冪等（`generated_at_utc` が
一致すれば何もしない）。同じ日に複数 run があれば複数行が並ぶ — 消費側は §6 の結合規則で
「判断時刻より前の最新行」を選ぶため、行が増えても曖昧さは生じない。

### 保存する変数と、検証に投入する変数は別である

これが本仕様の中心的な設計判断。

| | 方針 | 理由 |
|---|---|---|
| **保存** | その日に得られた観測を**多めに**残す（10 スコア + 主要9資産の生の変化率・終値 = 全42列） | 後から「実は US10Y の方が効いていた」と分かっても、当時の値を保存していなければ**取り返せない** |
| **検証投入** | **少なめに**絞る（初期は3変数、§6） | 日本株の想定サンプル数に対して変数が多すぎるとノイズを拾う（過学習） |

point-in-time で保存する情報は多め、モデルに入れる変数は少なめ。この2つは矛盾しない。
**保存 ≠ 採用**であり、保存されていること自体は「その変数を使ってよい」根拠にはならない。

### 列（全42列）

| 列 | 型 | 説明 |
|---|---|---|
| `snapshot_id` | str | `MCTX-YYYYMMDDTHHMMSSZ`（生成時刻ベース） |
| `context_date` | date | スナップショットが記述している営業日（元バーの日付） |
| `generated_at_utc` / `generated_at_jst` | datetime | 実際に生成された時刻 |
| `usable_from_utc` | datetime | **この行を判断に使ってよい最早時刻**。lookahead 防止の要 |
| `source_run_id` | str | GitHub Actions の run id（ローカル実行は `local`） |
| `risk_on_score` 〜 `narrative_confidence` | float | §2 の 10 スコア |
| `chg_pct_<ASSET>` | float | 主要9資産それぞれの当日変化率（生値） |
| `close_<ASSET>` | float | 主要9資産それぞれの終値（生値） |
| `input_assets_available` / `input_assets_expected` | int | 取得できた資産数 / 期待数（9） |
| `staleness_days` | int | **最新**バー基準の鮮度（この行が「いつの市場」を描いているか） |
| `oldest_asset_date` | date | 主要資産のうち**最も古い**バーの日付 |
| `max_asset_staleness_days` | int | **最古**バー基準の鮮度。**status の判定はこちらを使う** |
| `asset_date_spread_days` | int | 最新バーと最古バーの日数差 |
| `status` | enum | `ok` / `stale` / `insufficient_data` |
| `status_reason` | str | `ok` 以外のときの理由（空欄は理由なし） |

### status の判定

- `insufficient_data`: `input_assets_available < 7`、またはバー日付が判定できない。**値を推測で埋めない**
- `stale`: `max_asset_staleness_days >= 4`
- `ok`: 上記以外

**鮮度は最新バーではなく最古バーで判定する。** 資産ごとに配信の進みが違うため（FX は米株より
1 日先、指数系は 1 日遅れることがある）、最新日だけを見ると「一部の資産だけ古い」状態が
`staleness_days = 0` に隠れる。実データで確認済みの事象:

| 日付 | 実際に起きたこと |
|---|---|
| 2026-08-25 | US10Y だけ 1 日古い（他は当日）。旧実装では `staleness_days = 0` |
| 2026-06-10 | DXY が 1 日古く、USDJPY は 1 日先。バー日付の幅が 2 日 |

`asset_date_spread_days` を併記することで、消費側は「全体が古い」のか
「一部だけ配信が遅れている」のかを区別できる。

**閾値 4 日の根拠**: 通常の週末は金→日で 2 日、3 連休で 3 日空くのが正常。ここを 2 日にすると
毎週月曜が `stale` になり警告が意味を失う。4 日以上空いていれば取得が止まっている可能性が高い。
`staleness_days` の生値も保存されるので、消費側が独自にもっと厳しく判定することもできる。

なお `status` が `ok` でなくてもスコアは算出できる分だけ記録する。資産が欠けると
`narrative_confidence` が自動的に下がるため、消費側は `status` と `narrative_confidence` を
併せて見る。

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

### 検証に投入する変数は最初から全部入れない

§4 のとおり**保存は 42 列すべて**行う。そのうえで、モデルに投入する変数は絞る。
保存された全変数を説明変数にすると、日本株の想定サンプル数（1銘柄スイングで年間数十件規模）に
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

| 段階 | 内容 | 前提 | 状態 |
|---|---|---|---|
| 27.3-a | `src/export_market_context_snapshot.py` + `data/market_context_daily.csv` + daily_cycle への組み込み | なし | ✅ 実装済 |
| 27.3-b1 | 新規 JP swing signal と snapshot の結合（参照列 + 結合規則 + lookahead 監査登録） | 27.3-a + JP の dry-run 開始 | ⏳ |
| 27.3-b2 | 旧 `earnings-research-os` 254 件と、**当時保存された** TSO 記録の historical join | 27.3-a | ✅ 実装済 |
| 27.3-c | Ablation による検証 → ゲート判断。新規 JP データに加え、可能なら旧決算研究データも研究用サンプルとして使う | 27.3-b1 / b2 | ⏳ |

### 27.3-b2 の成果物（2026-08-25 実装済み）

| ファイル | 内容 |
|---|---|
| `data/market_context_historical.csv` | 過去アーティファクト88件から復元した市場コンテキスト（27.3-a と同スキーマ + provenance 4列） |
| `data/ers_legacy_context_link.csv` | 旧ERS 254件 ↔ snapshot の対応表（provenance 付き） |

生成: `python src/build_historical_market_context.py --artifacts-dir <dir> --artifact-index <tsv> --records <ERSのrecords.csv>`

**実装時に固定した4条件**:

1. **provenance を全件に残す** — `source_artifact_id` / `source_artifact_name` /
   `artifact_created_at_utc` / `source_market_run_ts_utc` を全行に記録。254件すべてで空欄ゼロ。
2. **「寄り前の最新」を機械的に保証** — `usable_from_utc < 判断時刻（09:00 JST）` を満たす最新1行のみ。
   検証: 違反0件、より新しい使用可能行の取りこぼし0件。
3. **週末の空きは除外しない** — 数日空いても「当時利用可能だった最新記録」として採用する。
   `lag_hours` を記録するので、消費側が必要なら自分で絞れる。実績: 中央値 1.3 時間、
   24時間超が20件、最大 73.9 時間（3.1日 = 週末）。
4. **native と historical を区別** — `provenance` 列で `native_point_in_time` /
   `historical_artifact_join` を機械的に分離。ファイルも分けている。

**`usable_from_utc` は保守側に倒す**: 値が算出されたのは `run_ts` だが、確実に手元にあったと
言えるのはアーティファクト確定時刻なので、後者を「使ってよい最早時刻」とする。

**結果**: 254/254 件が結合可能、全件 `snapshot_status = ok`。

復元した88行のうち **4行が `stale`**（最古資産基準で 7〜9 日）、1行は 8/9 資産のみ。
これは 27.3-a の監査修正（最古資産基準の鮮度判定）が過去分にも効いていることを示す。
旧実装の最新日基準なら、この4行は新鮮に見えていた。

### 27.3-b2 の前提調査（2026-08-25 実施済み）

`Tadaim2tk/earnings-research-os` の remote main に **254 件**の日本株決算研究データが存在する
（`data/records.csv`、2026-06-10 〜 2026-08-25、6月50件 / 7月123件 / 8月81件）。
決算日・rank・narrative・judge・buy/exit 条件・翌日/5日/20日リターン・reaction を含む。

TSO 側の point-in-time 原本の残存状況を調査した結果:

- GitHub Actions のアーティファクトが **899 件すべて未期限切れ**、最古 2026-06-06。
  daily cycle 本体の成果物は **74 日分**存在する。
- 各アーティファクトに `results/market_snapshot.csv`（`run_ts` 付き）と `data/raw/*.csv` が含まれる。
  これは**再構成ではなく当時の記録そのもの**であり、`run_ts` が「いつ確定していたか」を証明する。
- 254 件それぞれについて「その日の東証寄り（09:00 JST）より前の最新アーティファクト」を探すと、
  **254/254 件が結合可能**（4日以内）。判断時刻との時間差は中央値 1.3 時間、最大 3.1 日（週末）。

**重要な制約**: 結合に使ってよいのは**当時保存された記録だけ**。当時の記録が無い日について、
現在の価格データから市場コンテキストを後付け生成してはならない（`unavailable` とする）。
今回は全期間で記録が残っていたが、この原則は将来も維持する。

なお 27.3-b2 で復元した行は、`source_run_id` と provenance を明示して
27.3-a の日次行とは区別できるようにすること（両者を混ぜて「全部 point-in-time」と扱わない）。

### 27.3-a を先に、かつ早く着手すべき理由

**点在時点（point-in-time）の市場コンテキストは、後から作れない。**

今日の値を明日以降に再構成しようとすると、その時点で確定していなかった情報が混入する
（lookahead 汚染）。日本株の判断が1件も無い現在でも、**スナップショットの蓄積だけは今日から
始める価値がある**。逆に、蓄積を後回しにすると、JP のデータが貯まった時点で「比較対象の
市場コンテキストが存在しない」という理由で 27.3-c の検証自体が実行できなくなる。

これは「実装はデータを待たない」（SPEC_CROSS_ASSET_REGIME.md §7）と同じ判断。

### 他プロジェクトへの適用（将来）

同じ「市場環境を point-in-time で保存し、後から個別要因と分離して検証する」構造は、
決算研究（ERS / earnings-research-system）にもそのまま使える。
「決算は良かったのに地合いで売られた」を、銘柄要因と市場要因に分けて研究できるようになる。
本仕様は日本株スイングを最初の消費者として書いているが、`data/market_context_daily.csv` 自体は
特定の消費者に依存しない汎用の feature store として設計してある。

---

## 10. 現時点の既知の制約

- **`data/jp_swing_signals.csv` は 0 行**（2026-08-25 時点）。TSO 内の JP 専用台帳に限れば
  判断実績はまだ無い。ただし**研究所全体では違う**: 別リポジトリ `earnings-research-os` に
  254 件の日本株決算研究データがあり（§9 の 27.3-b2）、こちらは検証サンプルになりうる。
  したがって「JP dry-run が 1 件入るまで完全待機」ではなく、b2 の交差調査を先に進める。
- 27.3-a の初回行は**ローカル実行**で記録されている（`source_run_id=local`）。
  2 行目以降は daily cycle（21:55 UTC）が記録する。
- 借用できるのは市場レベルの文脈のみ（§1）。銘柄固有ナラティブの自動化は本仕様の範囲外。
- コスト値は `config/jp_cost_model.json` が unconfigured のままであり、net-R 基準の評価は
  依然として使えない（Phase 26.2 と同じ制約）。

---

## 11. 変更手続き

本仕様の変更は PR で行い、人間の承認を得る。ゲート条件（§5）の緩和は特に、
false-green を生む方向の変更であるため、緩和理由を PR 本文に明記すること。
