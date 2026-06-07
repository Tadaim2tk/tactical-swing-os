# Tactical Swing OS AI Feedback Loop

AI Feedback Loop は、日次シグナルと評価結果に、市場ナラティブのproxy評価を重ねて確認するための研究用レイヤーです。

## 目的

価格データとテクニカル指標だけでは、「なぜそのシグナルが市場文脈に合っていたのか」「なぜ逆風だったのか」を説明しきれない場合があります。AI Feedback Loop は、既存の `MARKET_SNAPSHOT`、`SIGNALS`、`EVALUATIONS`、Reason Code分析、Rule Update Proposalを読み、翌日の判断で注意すべき仮説を文章化します。

## ナラティブ評価とは

ナラティブ評価は、市場の大きな文脈を数値化する試みです。たとえば、株価指数が強く、VIXが低下し、DXYが弱い場合はリスクオン寄りとみなします。GOLDが上昇し、VIXが上昇し、株価指数が弱い場合はリスクオフ寄りとみなします。

今回の実装では、ニュース本文やLLM APIは使いません。まずは既存市場データから次のproxy scoreを作ります。

- `risk_on_score`
- `risk_off_score`
- `dollar_strength_score`
- `rate_pressure_score`
- `gold_safe_haven_score`
- `oil_supply_risk_proxy_score`
- `crypto_liquidity_score`
- `equity_momentum_score`
- `volatility_stress_score`
- `narrative_confidence`

## narrative_alignment の見方

各シグナルについて、市場ナラティブとの整合性を次の4分類で出します。

- `aligned`: 市場文脈がシグナル方向を支えている
- `conflicted`: 市場文脈がシグナル方向と衝突している
- `neutral`: 文脈上は中立
- `insufficient_data`: データ不足で判定できない

`narrative_alignment_score` は `-100` から `+100` です。正の値が大きいほど文脈整合、負の値が大きいほど文脈逆風です。

## improvement_hypotheses の見方

`improvement_hypotheses` は、明日の判断で監視するための仮説です。たとえば、GOLD LONGがドル高・金利上昇と衝突している場合、GOLDのLONG条件を慎重化する候補として表示します。

この仮説は自動適用しません。`weights.json` や `generate_signal.py` は変更せず、人間レビューの材料として扱います。

## なぜ自動売買や自動更新に使わないのか

ナラティブ評価はproxyであり、ニュース本文や地政学イベント、政策発言などを直接読んでいません。誤判定や過剰反応を避けるため、実売買、発注、XM操作、自動パラメータ更新には使いません。

## 将来拡張

今回の構造は、将来ニュースAPI、経済指標カレンダー、LLM評価、地政学リスク分類を追加できるように分離しています。`score_narratives.py` は現在rule-basedですが、後からLLMベースのスコアリングへ置き換えられます。
