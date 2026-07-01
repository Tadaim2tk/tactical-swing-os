# Minimal Observation Loop（Phase 29.4）— 観測ループを実際に回す

- 実装: `src/run_observation_loop.py`（手動CLI。日次workflowには入れない — 観測記録は研究行為であり人間のリズムで回す）
- 恒久記録（git追跡）: `data/observation_log.csv` + `data/observations/OBS-*.md`
- テスト: `src/test_observation_loop.py`
- プロトコル: Obsidian vault の **PROTO-0001 TSO A Rank Expected R** に準拠

## 使い方

```bash
python src/run_observation_loop.py                 # 適格イベント > 直近A-rank を自動選定
python src/run_observation_loop.py --signal-id 20260608_WTI_LONG_A-MOMENTUM
```

1周 = **観測**（判断時の記録値）→ **事前ナラティブ**（判断時に存在した情報のみ + as-of memory 状態）
→ **評価**（+5/+10営業日、当時の reference price / risk unit で R）→ **類似局面検索**（as-of）
→ **教訓の記録**（自動検出した運用上の穴 + 分析者の教訓を OBS md に）。

## PROTO-0001 準拠の要点

- 適格イベント = A-rank かつ **CBS >= 80 かつ EMS >= 70**。適格が無い間は直近 A-rank を
  `non_qualifying_dry_run` として回す（プロトコル台帳には記録しない）。
- **反後知恵**: reference price / risk unit は判断時の記録値のみ。元記録が不足なら
  `invalid_data`（推定で埋めない）。結果窓が未確定なら `pending`（再実行で確定に更新・重複しない）。
- 判定: `success`（R>0）/ `failure`（R<=0）— PROTO の終値ベース定義のまま。
  SLキャップ後のトレードP&Lとは測るものが違う（教訓として両方書く。定義は変えない）。

## 初回実走（2026-07-02）

`OBS-20260608-WTI`: 6/8 の WTI LONG A-Momentum（CBS76/EMS84 = 非適格 dry-run）→
+5営業日 **R=-3.65 failure**（供給ショック剥落で崩落）。教訓は OBS md 参照
（スパイク追随リスク / regime×overextension 減点仮説 → shadow weights 候補 / 指標ギャップ）。

## 安全条件

研究記録のみ。実売買・発注なし。signal score 未接続。weights.json / generate_signal.py 変更なし。
