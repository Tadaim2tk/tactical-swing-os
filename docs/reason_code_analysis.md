# Reason Code Analysis

reason_codes分析は、Tactical Swing OS が「なぜそのシグナルを出したか」を、仮想評価結果と結び付けて検証するための仕組みです。

シグナルの勝ち負けだけを見ると、たまたま相場が良かったのか、判断理由そのものが有効だったのかが分かりにくくなります。`reason_codes` を分解して集計すると、`trend_up` や `momentum_positive` のような判断理由ごとに、勝率、平均R、取り逃し、未約定を確認できます。

## 勝っている理由コードの見方

`reliability_label` が `strong_positive` または `positive` の reason_code は、現時点では有効に働いている可能性があります。ただし、評価件数が少ない間は偶然の影響が大きいため、すぐにルールやweightsへ反映しません。

## 負けている理由コードの見方

`strong_negative` または `negative` の reason_code は、Entry条件、SL距離、Rank判定、または相場環境との相性を見直す候補です。単独で悪いと決めつけず、asset、side、rankと合わせて確認します。

## no_trade_reasonの見方

`no_trade_reason` は、見送り判断がうまく機能したかを確認するために使います。

- `effective_filter`: 見送りが有効だった可能性
- `over_filtering_risk`: 見送りすぎで機会損失が出ている可能性
- `insufficient_data`: データ不足

`no_trade_missed` や `missed_opportunity` が多い理由は、翌月以降の改善候補です。

## データ不足時の注意

reason_codeごとの評価件数が5件未満の場合は `insufficient_data` とします。少数サンプルでは勝率や平均Rが大きくぶれるため、結論を急がない方針です。

## weights自動更新について

このフェーズでは `weights.json` は自動更新しません。reason_code単位の分析結果は、週次レビューと月次較正のメモとして使い、十分な件数が蓄積してから重み調整を検討します。

この処理は分析と仮想評価の集計だけを行います。実売買、発注、XM操作、Google Sheetsへの書き込み、GitHub Actionsからのgit pushは行いません。
