# Rule Update Proposals

ルール改善候補レポートは、reason_code分析、評価結果、週次レビュー、月次較正をもとに、将来見直すべきルール候補を整理するためのものです。

このレポートは売買ロジックを変更しません。`weights.json` も更新せず、`generate_signal.py` も自動で書き換えません。出力は人間レビュー用の提案に限定します。

## reason_code分析から見ること

reason_codeごとの勝率、平均R、取り逃し、評価件数を見て、強める候補と弱める候補を分けます。

- 勝率と平均Rが良いreason_code: `strengthen_reason_code`
- 平均Rが悪いreason_code: `weaken_reason_code`
- 件数不足: `data_insufficient`

## なぜ自動反映しないのか

短期間の成績は相場環境に大きく左右されます。少数のclosed評価だけでスコアやrank条件を自動変更すると、たまたま良かった/悪かった条件に過剰適応する可能性があります。

## closed評価30〜50件未満では提案止まりにする理由

reason_codeやasset、side、rankごとの評価件数が少ないと、平均Rや勝率が大きくぶれます。最低でも30〜50件程度のclosed評価が蓄積するまでは、提案を出して監視する段階に留めます。

## proposal_typeの見方

- `strengthen_reason_code`: 有効なreason_codeを少し優遇する候補
- `weaken_reason_code`: 低期待値のreason_codeを抑制する候補
- `relax_no_trade_filter`: 見送りすぎによる取り逃しを減らす候補
- `strengthen_no_trade_filter`: 有効な見送り条件を維持/強化する候補
- `increase_asset_weight` / `reduce_asset_weight`: asset単位の優遇/抑制候補
- `increase_side_bias` / `reduce_side_bias`: side単位の優遇/抑制候補
- `review_rank_threshold`: rank判定条件の見直し候補
- `data_insufficient`: 判断保留

## proposal_strengthとpriority

`proposal_strength` は HIGH / MEDIUM / LOW / DATA_INSUFFICIENT で表示します。`priority` は小さいほど優先度が高く、HIGH=1、MEDIUM=2、LOW=3、DATA_INSUFFICIENT=4です。

## 人間レビューの手順

1. HIGH / MEDIUM の提案から確認します。
2. 対象reason_codeが特定assetやsideに偏っていないか確認します。
3. no_trade_reason緩和候補は、低品質シグナル増加のリスクを確認します。
4. 週次・月次で同じ提案が繰り返し出るか確認します。
5. 十分な件数が溜まってから、必要なら手動でルール変更を実装します。

この処理は分析と提案生成だけを行います。実売買、発注、XM操作、Google Sheetsへの書き込み、GitHub Actionsからのgit pushは行いません。
