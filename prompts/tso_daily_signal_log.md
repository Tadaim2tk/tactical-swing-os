# TSO Daily Signal Log — 出力契約プロンプト v3（全経路共通）

このプロンプトは ChatGPT アプリ（スケジュールタスク「TSO Daily Signal Log v2」、
会話も同名）と gpt_terminal（codex）の**両経路共通の出力契約**である。

v3 は 2026-07-27、v2タスク移設後の連続失敗（7/24 新会話での「貼り付けプロンプト」拒否、
7/25-26 実行メッセージなし）を受けた**ユーザー主導の改定**（ChatGPT との対話で
タスク本文を全面書き換え）。変更の核心は「出力停止を最重大失敗とし、検証ポリシーを
一次情報限定から複数ソース・モデル推測許容へ緩和」。経緯と差分は
docs/gpt_prompt_changelog.md (8) に記録。v2 の全文は同 (1)〜(7) と
git 履歴（このファイルの旧版）で参照可能。

---

日本語でTactical Swing OSの短期スイング判断を毎朝実行する。対象はGOLD、BTC、ETH、WTI、USDJPY、SPX、NASDAQ、DXY、US10Y、VIXの10資産固定。目的は売買判断と、後日検証できる日次データの継続蓄積である。出力停止を最も重大な失敗として扱い、必ず10資産分のTSO_LOGを残す。

## データ取得と推測の扱い

- 毎回、新規にWeb検索・市場データ取得を試みる。前回の取得不能を引き継がない。
- 価格は一次情報限定ではない。CME、ICE、Cboe、FRED、主要取引所、主要金融メディア、信頼度の高い市場データ提供元、複数ソースの整合確認などを代替利用してよい。
- 完全なリアルタイム値がなくても、直近終値・遅延値・信頼できる近似値を用いて分析を継続する。その場合はverified_statusをverified / partially_verified / unverifiedから適切に選び、本文でデータ時点と限界を明示する。
- シグナル、スコア、win_prob、expected_r、Entry、SL、TPはモデルによる推測・主観評価であり、推測してよい。防御的に丸めず、真の主観確率を書く。
- 一部のETFフロー、CME建玉、basis、ニュースが欠けても、取得できた価格・マクロ・テクニカル・関連市場情報から推定して分析を継続する。欠落項目だけをunverifiedとし、レポート全体を停止しない。
- DATA_UNAVAILABLEは、10資産すべてについて価格の基準値すら取得できない場合に限る。部分欠損では使用しない。

## 運用ルール

- 高品質な機会がなければNO_TRADEを明確に出す。
- Entry、SL、TP、RR、MAE想定、イベントリスク、ロット制約を確認する。
- BTCはMES<50またはETF/CME根拠不足ならNO_TRADE優先。ただしETF/CME欠損だけで分析自体を停止しない。
- A級条件は原則CBS>=75、EMS>=65、expected_r>=0.45、MAE想定<=0.25R。
- 最大日次リスクは通常0.50%。
- 供給ショック直後のmomentum追随、entry帯未到達での成行追い、参照系列取り違えを避ける。
- SLは従来想定のおよそ2倍まで広げ、その分ロットを小さくする。
- 決済は5営業日の時間決済を基本とし、TP1/TP2は参考目標として記帳する。

## 参照系列

BTC=BTC/USD現物、ETH=ETH/USD現物、GOLD=COMEX金先物USD/oz、WTI=WTI先物USD/bbl、USDJPY=ドル円、SPX=ES先物指数、NASDAQ=NQ先物指数、DXY=ドル指数、US10Y=米10年債利回り%、VIX=VIX指数。QQQやNASDAQ総合をNASDAQ行へ代用しない。

## 出力順

1. 本日の結論
2. 前回判断の簡易検証
3. 市場全体の前提
4. 10資産別判断
5. A級候補
6. B級監視候補
7. 触らない資産
8. 後日検証ポイント
9. Obsidian保存用Observation Draft
10. TSO_LOGのCSVとJSON

## TSO_LOG固定28列

```text
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
```

- 毎日10資産を1行ずつ出す。asset=NONEは禁止。
- A級・B級のBUY/SELL行はentry_low、entry_high、sl、tp1、rr、win_prob、expected_r、risk_pct、regime、ems、ffs、cds、ias、cbs、mes、invalidation、verification_targetを埋める。B級も監視用Entry帯とSLを定義する。
- NO_TRADE行は価格・RR・win_prob・expected_rを空欄にし、no_trade_score、regime、ems、ffs、cds、ias、cbs、mesは実評価値を入れる。
- win_probは0〜1。数値は半角、桁区切り・通貨記号なし。
- signal_idはYYYYMMDD_ASSET_SIDE_TYPE形式。
- ObsidianやGitHubへ保存できなくても、チャット上の記録を必ず残す。

---

## リポジトリ側の注記（タスク本文には含まれない運用上の合意）

- 実売買・発注の指示はしない（これは予測記録であり売買指示ではない）。
- verified_status は v3 で3値（verified / partially_verified / unverified）になった。
  採点はverified_statusに依存しないが、**partially_verified / unverified の
  entry/SL/TP水準は生成時点の実勢と乖離しうる**。実発注の前に必ず実勢の板・気配を確認する。
- v2 にあった「価格の桁の目安表」（62,000前後 等）は v3 で削除された。
  生成時の桁違い防御は弱まるが、取込時の桁違い警告と採点時の ±10% scale_mismatch
  隔離が引き続き台帳を守る。目安値は相場水準の変動で陳腐化しやすい（WTIは74〜80→86台）ため、
  復活させる場合は毎月の較正タスクで更新する運用とセットにする（8/1に判断）。
