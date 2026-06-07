# Tactical Swing OS News Narrative Layer

ニュースナラティブレイヤーは、短期スイング判断に影響しやすい公開ニュース見出しを取得し、リスクオン/リスクオフ、ドル高、金利圧力、地政学リスク、原油供給リスク、暗号資産流動性などの文脈を補助的に数値化するための研究用レイヤーです。

## 仕組み

`src/fetch_news.py` は `config/news_sources.json` に定義したRSS/公開フィードから見出しを取得し、`results/news_headlines.csv` と `results/news_headlines.json` に保存します。RSSソースの一部が失敗しても、workflow全体は止めず、取得できた範囲または空の成果物を生成します。

`src/classify_news_narratives.py` は取得した見出しを英語キーワードで分類し、`results/news_narrative_scores.csv` と `results/news_narrative_scores.json` を作ります。分類は見出しベースで、本文読解、感情分析、LLM判定、有料ニュースAPIはまだ使いません。

## Market Proxy Scoreとの違い

既存のAI Feedbackは、BTC、GOLD、WTI、DXY、VIX、US10Yなどの価格・市場データからナラティブを推定するmarket proxy scoreを使っています。ニュースナラティブレイヤーは、価格にまだ十分反映されていない可能性のある見出し情報を補助入力として扱います。

初期実装ではニュース分類を粗い補助情報として扱い、market proxy scoreより重くしすぎません。AI Feedbackではおおむね30%程度の補助ウェイトで使い、`narrative_source_mix` に `market_proxy_only`、`market_proxy_plus_news`、`news_only`、`insufficient_data` を記録します。

## AI Feedbackでの使われ方

ニューススコアが存在する場合、AI Feedbackは以下のような補正を行います。

- GOLD LONG: 地政学リスクや安全資産需要が高い場合、整合性を補強
- BTC LONG: リスクオフやドル高が強い場合、衝突方向を補強
- WTI LONG: 原油供給リスクが高い場合、整合性を補強
- USDJPY LONG: ドル高や金利圧力が高い場合、整合性を補強
- SPX/NASDAQ: リスクオン、株式モメンタム、金利圧力、ボラティリティを補助的に評価

## 限界

この分類はRSS見出しとキーワードに依存します。同じ単語でも文脈によって意味が変わるため、誤分類や過小評価が起こります。ニュースの重要度、本文内容、発言者、時系列の鮮度、既に市場が織り込んだかどうかは厳密には判定していません。

## 安全条件

このレイヤーは分析・研究用です。実売買、発注、XM操作、自動売買、Google Sheetsへの書き込み、`weights.json` の自動更新、`generate_signal.py` の自動変更は行いません。

将来的には、LLMによる本文要約、要人発言解析、経済指標カレンダー、地政学リスク分類、有料ニュースAPIへの差し替えができるよう、取得・分類・AI Feedback統合を分離しています。
