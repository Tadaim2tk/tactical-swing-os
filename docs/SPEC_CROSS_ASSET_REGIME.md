# 仕様（先行起草・未活性）: Cross Asset Regime Engine

- status: **draft — deferred / inactive（本体未実装）**
- spec_id: SPEC-CAR-001
- drafted_at: 2026-06-16 (JST)
- phase: 28.0（SPEC-only。コード・workflow・Dashboard セクションは追加しない）
- 前提仕様: [SPEC-RD-001](SPEC_REGIME_DECAY.md)（レジーム較正と忘却）, SPEC-SG-001（統計ガード）
- 関連: [evaluation_cohort_maturity.md](evaluation_cohort_maturity.md), [dashboard_health.md](dashboard_health.md)

> **この文書は設計の凍結ではなく、本体実装を始める前に「発火条件・安全境界・入力定義・
> 非活性条件」を先に固定するための先行仕様である。** 現時点で clean evaluations が十分に
> 蓄積していないため、エンジン本体を実装すると「データが無いのにそれっぽい判断器」を作る
> false-green / overfitting のリスクがある。よって Phase 28.0 は **SPEC-only** とし、コードは
> 一切追加しない。

## 1. 目的

Cross Asset Regime Engine は、**単一資産シグナルではなく、資産横断の市場環境（レジーム）を
分類するための将来レイヤー**である。

- 当面は **分析・監査・説明のための補助レイヤー**であり、自動売買や自動重み変更には使わない。
- 「いま市場全体がどのレジームか」を人間の監査者が読めるようにし、個別シグナルの解釈に
  文脈を与える。例: あるロング判断が `risk_off` レジーム下で出ていたか、`risk_on` 下だったか。
- レジーム分類そのものは**提案・説明・監査**にとどめ、`generate_signal.py` や `weights.json`
  へ自動適用しない（適用は人間承認事項。§6）。

## 2. 入力候補

既存の研究OSが生成済みの成果物・監査ログを入力源とする（新規データ取得は前提としない）。

| 入力 | 役割 |
|---|---|
| `MARKET_SNAPSHOT`（data/raw, fetch_market.py 由来） | 価格・ボラ等の素データ |
| `SIGNALS` / `results/signals.csv` | 当日の資産横断シグナル状況 |
| `EVALUATIONS` / `LATEST_EVALUATIONS` | 決着済み成績（レジーム別の有効性検証用） |
| `NEWS_NARRATIVE` | ニュース由来のナラティブ分類 |
| `AI_FEEDBACK` | 直近判断の振り返り |
| `PORTFOLIO_LAYER` | 資産横断のエクスポージャ／相関の文脈 |
| `TRANSACTION_COST_SUMMARY` | net-R 判定に使う場合のコスト前提（未設定なら使わない。§4） |
| `DATA_HEALTH` | 入力の鮮度・欠損ガード（critical なら非活性。§4） |
| `ADVERSARIAL` / `LOOKAHEAD` / `DATETIME` 監査 | 未来情報混入・時刻整合の健全性（blocked なら非活性。§4） |

対象資産・指標の例（クロスアセット関係の解釈に用いる）:

`SPX` / `NASDAQ` / `VIX` / `DXY` / `USDJPY` / `GOLD` / `WTI` / `BTC` / `ETH` / `US10Y`

> 入力の実在カラム・スキーマは実装フェーズ（§7）で確定する。本SPECは入力の**意図**を固定する。

## 3. レジーム分類候補

排他的・網羅的な最終分類ではなく、起草時点の候補集合。実装プロトタイプ（Phase 28.2）で
ラベル定義・判定根拠・false positive/negative 例を確定する。

- `risk_on` / `risk_off`
- `inflation_pressure` / `disinflation`
- `dollar_strength` / `dollar_weakness`
- `rate_pressure`
- `safe_haven_demand`
- `commodity_shock`
- `crypto_liquidity`
- `mixed`（複合・優勢レジーム無し）
- `insufficient_data`（**データ不足を正直に表す既定値**。§4 のゲート未達時はこれを出す）

## 4. 非活性ゲート（発火条件）

以下を **すべて** 満たすまで `engine_status` は `inactive` / `insufficient_data` とし、レジーム
ラベルを断定しない。false-green（不足データを正常分類と誤読）を避けるための中核条件。

| ゲート | 初期案の閾値 | 理由 |
|---|---|---|
| clean closed evaluations | `minimum_closed_evaluations: 30` | 統計的に意味のある分類に最低限必要（SPEC-SG-001 の n>=30 と整合） |
| 評価が複数資産に分散 | `minimum_assets_with_closed_evaluations: 4` | 単一資産偏重での「クロスアセット」分類を防ぐ |
| 観測期間 | `minimum_days_observed: 20` | レジームは時間軸の概念。短すぎる窓での断定を防ぐ |
| Data Health（全体） | `critical` でも `degraded` でもない | `degraded`（stale/empty を含む）でも分類を出すと劣化データを正常分類と誤読する |
| regime 必須入力レイヤーの鮮度 | どの必須入力レイヤーも `stale` / `missing` / `unavailable` / `unknown_age` / `future_timestamp` でない（`fresh` のみ通過） | 監視対象（MARKET_SNAPSHOT / SIGNALS / EVALUATIONS / LATEST_EVALUATIONS 等）が1つでも劣化していたら分類しない |
| lookahead / adversarial audit | 監査 artifact が**存在**し、`audit_status` が `passed`（または明示的に許容する `warning`）のときのみ通過 | 「何も見ていないのに passed にしない」（Phase 23/24 の思想）。`unavailable`（未生成/未取得）・`high_risk`・`blocked` はすべて非活性 |
| transaction cost | `unconfigured` のとき net-R 依存の判定を**使わない** | 証拠の無いコストで net 成績を語らない（SPEC-TC-001 / 証拠主義） |

- どれか1つでも未達なら `engine_status=inactive`、レジームは `insufficient_data`。
- ゲート未達の理由（どの条件で止まったか）を機械可読に併記する（honest state）。
- 閾値（N 等）の変更は新 spec_id ではなく本ドキュメント更新履歴への追記で可とするが、
  **緩める方向の変更は人間承認を必須**とする。

## 5. 出力候補（今回は生成しない）

将来の実装フェーズで生成する出力を**定義のみ**する。Phase 28.0 ではファイルを作らない。

- `results/cross_asset_regime.csv`
- `results/cross_asset_regime.json`
- `results/cross_asset_regime_summary.json`（`engine_status` / アクティブ判定 / ゲート未達理由を含む）
- `reports/regime/YYYY-MM-DD_cross_asset_regime.md`

> 出力スキーマ（列名・enum）は Phase 28.1〜28.2 で確定。`*_summary.json` は他レイヤー同様
> `requires_human_approval=true` / `weights_json_updated=false` / `generate_signal_updated=false`
> を含める方針とする。

## 6. 安全条件

- レジーム分類は **提案・説明・監査用**。判断の自動化ではない。
- `weights.json` を更新しない。
- `generate_signal.py` を自動変更しない。
- 実売買・発注・XM/証券会社操作を行わない。
- Google Sheets への新規書き込みを追加しない。
- 人間承認なしに下流ロジック（シグナル生成・重み・提案採択）へ適用しない。
- false-green を避け、不足データは断定せず `insufficient_data` と表示する（honest red over false green の原則）。
- LLM・有料 API を新規に使わない（将来 LLM を併用する場合は別 SPEC と lookahead 監査の前段が必須）。

## 7. 将来の実装フェーズ案

段階を分け、各段で安全条件とゲートを満たすことを確認してから次へ進む。

| Phase | 内容 | 出すもの |
|---|---|---|
| 28.1 | input loader + **非活性サマリのみ** | `engine_status=inactive` とゲート未達理由だけを返す。分類はまだしない |
| 28.2 | regime classification prototype | §3 のラベル定義・判定根拠・FP/FN 例を確定し、分類を試作 |
| 28.3 | dashboard integration | 既存 Data Health と同じ思想で「鮮度≠成熟度≠レジーム確度」を正直表示 |
| 28.4 | backtest / impact analysis | レジーム別に既存評価の有効性を後ろ向き検証（重みは変えない） |
| 28.5 | human-reviewed use in proposals | 人間レビューを通した上で、提案レイヤーの**文脈**として使用（自動適用はしない） |

## 8. テスト方針（将来実装時）

本体実装フェーズで満たすべきテスト条件を先に文書化する。いずれも「不足/異常を正常と
誤読しない」ことの検証が主目的。

- **空データ**: 入力が空 → `engine_status=inactive` / `insufficient_data`、例外で落ちない。
- **評価不足**: closed evaluations < N → `insufficient_data`、ゲート未達理由を併記。
- **監査 blocked / unavailable / high_risk**: lookahead / adversarial が `passed`（許容 `warning`）以外 → 分類を出さない。**監査未生成・未取得の `unavailable` も非活性**（何も見ていないのに passed にしない）。
- **mixed regime**: 優勢レジームが無いとき `mixed` を返し、無理に1つへ断定しない。
- **stale / degraded data**: Data Health が `critical` または `degraded`、もしくは必須入力レイヤーが `stale` / `missing` / `unavailable` / `unknown_age` → 非活性。
- **future timestamp**: 必須入力の時刻が未来（クロックスキュー超）→ 非活性（既存 Data Health と整合）。
- **asset concentration**: 評価が単一資産に偏る → `minimum_assets_with_closed_evaluations` 未達で非活性。
- **no transaction cost evidence**: cost `unconfigured` → net-R 依存判定を使わない経路を検証。

## 9. 変更手続き

- 入力定義・ゲート閾値・分類ラベルの変更は本ドキュメントの更新履歴への追記を必須とする。
- ゲートを**緩める**変更、および本 SPEC を `draft` から `active` へ昇格させる判断は、人間承認を必須とする。
- 本体実装（Python コード追加）は Phase 28.1 以降の別 PR で行い、本 SPEC ではコードを追加しない。
