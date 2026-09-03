# TSO 週次レビュー（ChatGPTタスク「レビューする短期スイングモデル」の正本）

status: 2026-09-03 新設。**タスクは以前から稼働していたが正本が無く、本文の変更履歴が
残らない状態だった**（2026-09-03 のタスク棚卸しで判明。runbook §1b）。
以下は同日に実査した本文の写しである。**本文を変えるときは必ずこのファイルも同時に直す。**

実行: **毎週土曜 12:00 JST**（GitHub Actions の weekly_review 12:10 の10分前）
タスクID: `6a2102e95d2c8191924c2f6f9fbd340c`
出力先の会話: 「週次レビュー設定」

---

## 本文（2026-09-03 時点の写し）

```
日本語でTactical Swing OS v3の週次レビューを行う。対象はXM等のレバレッジ付き短期〜中期売買で、
長期ポートフォリオではない。対象期間は実行日を含む過去7日間。出力停止を最重大の失敗として扱い、
必ずレビューとREVIEW_LOGを出す。

【入力（毎週、過去の取得可否に関わらず新規に取得を試みる）】
1. 台帳CSV: https://raw.githubusercontent.com/Tadaim2tk/tactical-swing-os/main/data/signal_log.csv
2. 採点CSV: https://raw.githubusercontent.com/Tadaim2tk/tactical-swing-os/main/data/prediction_log_scores.csv
3. 保守的執行シミュレーション: https://raw.githubusercontent.com/Tadaim2tk/tactical-swing-os/main/data/execution_simulation.csv
4. ダッシュボード(照合用): https://tadaim2tk.github.io/tactical-swing-os/
旧Google Sheets「Tactical Swing OS Log」は参照しない(2026-07に上記台帳へ移行済み)。取得できない
ソースは「取得不能」と明記し、取得できた範囲で定量レビューする。数値を推測で埋めない
(価格系列からMFE/MAEを近似した場合は「暫定値」と明記)。

【必須評価】
1. 週次サマリー：総合成績、A級/B級/NO_TRADE/DATA_UNAVAILABLE別の件数と妥当性。
2. 仮想売買検証：signal_id単位で集計し、**5日方向勝敗(directional)と保守的執行結果
   (sl_first/tp1_first/time_exit)を必ず分けて集計する。混同しない**。
3. 誤差分解：方向性ミス、タイミングミス、SL設計ミス、利確ミス、レジーム認識ミス、
   イベント読み違い、相関崩れ、取り逃しを件数と影響Rで集計。
4. 取り逃し監査：監視していたが入らなかった資産、押し目待ちで未約定だった資産を抽出し、潜在Rを推定。
5. 資産別評価：GOLD、BTC、ETH、WTI、USDJPY、SPX/NASDAQのどれが機能し、どれがノイズだったか。
6. モジュール別評価：EMS、FFS、CDS、IAS、CBS、MESのどれが当たり、どれが誤差を増やしたか。
7. 較正チェック：当週B級の事前win_prob平均と決着分の実現勝率。決着nが5未満の項目は「判定不能」と書く。
8. 重み調整案：提案のみ。1週間の変更幅は最大15pt。weights.jsonへの適用は人間承認前と明記。
9. 来週の運用ルール修正案：すべて提案として書く。
   A級条件(CBS>=75/EMS>=65/expected_r>=0.45/MAE<=0.25R)は据え置き前提。
10. 最終結論：来週は攻撃・通常・防御のどれかと最大リスク量の推奨。

【必須の表】
signal_id別成績表、資産別成績表、エラー分類別の件数と損益R表、モジュール別の機能度表、
来週の暫定ウェイト表

【REVIEW_LOG：最後に必ず出力】
次の列順でCSVを1つ出す。続けて同内容をJSONでも出す。数値不明はnull。
week_start,week_end,total_signals,a_signals,b_signals,no_trade_days,win_rate,profit_factor,
total_r,max_drawdown_r,missed_r,best_asset,worst_asset,best_module,worst_module,
next_week_mode,max_daily_risk_pct,rule_change_1,rule_change_2,rule_change_3

【制約】
- 実売買・発注の指示はしない。
- 過去週の「取得できない」という結論を今週の前提として引き継がない。
```

---

## 既知の課題（写した時点で気づいたもの。本文はまだ直していない）

1. **「決着nが5未満は判定不能」は行数の閾値であり、独立性を見ていない**（項目7）。
   連続日の判断は4/5の窓を共有するため、5行あっても独立な観測は1件のことがある。
   本来は**資産×バースト（間隔7日超で分割）のクラスタ数**で見るべき。
   台帳138行が独立クラスタ16件だった実例がある（research_leader_lens_2026-09-03）。
   → 「決着クラスタが3未満の項目は判定不能」へ変える案。月次でまとめて判断する。
2. **A級条件の具体数値が本文に書かれている**（項目9）。生成側ではなくレビュー側なので
   B+印のときのような直接の内生化ではないが、閾値がプロンプトに常駐する構図は同じ。
   閾値を取り込み側へ移す案（changelog(13)の宿題）と一緒に扱う。
3. REVIEW_LOG の出力先が会話のみで、**台帳に着地していない**。
   `best_module` / `next_week_mode` などは他に記録が無い。取込先の新設は要検討。

## 着地先

現状: 会話のみ（`docs/weekly_review.md` は GitHub Actions 側の週次レビューの説明であり別物）。
GitHub Actions の `weekly_review`（土 12:10）とは**独立**に走る。両者は入力は同じだが
出力先が違い、突き合わせは人間が行っている。
