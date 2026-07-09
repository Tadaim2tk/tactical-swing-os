# 2026-07-01 daily TSO output (prose, recovered 2026-07-09)
# source: 毎朝7時タスク確認 https://chatgpt.com/c/6a419a9e-84c8-83e8-9f82-af43b8e33db9
# format: prose (TSO_LOG-style csv block appears in-chat but was never saved as a .csv file that day)

TSO Daily Signal Log
TSO Daily Signal Log（2026-07-01）
1. 本日の結論
新規エントリー

A級候補なし

B級監視候補

USDJPY（押し目買い）

WTI（押し目買い）

GOLD（戻り売り）

見送り（NO_TRADE）

BTC

ETH

SPX

NASDAQ

理由：
BTC・ETHはETFフロー、CME建玉（Open Interest）等の確認が不足しており、TSOルール上はNO_TRADE優先。SPX/NASDAQは強いが、すでに大幅上昇後で追撃エントリーの期待値が低い。
Reuters
+1

2. 前回判断の簡易検証
USDJPY

前回：

B級監視

押し目買い候補

結果：

円安継続

Reuters確認値で162円台後半まで進行
Reuters

評価：
見立て継続有効

WTI

前回：

押し目買い監視

結果：

70ドル台維持

ただし中東停戦により原油上値は重い
Reuters

評価：
押し目待ち継続

BTC

前回：

NO_TRADE

結果：

検証データ不足

評価：
見送り維持

3. 市場全体の前提
レジーム判定

ややリスクオン

理由

S&P500は四半期で+14.9%

NASDAQは四半期で+21.4%

AI関連が再び市場を主導

原油急落

VIX急騰確認なし

景気後退懸念より成長期待が優勢
Reuters
+2
Reuters
+2

判定

リスクオン 65
中立 25
リスクオフ 10
4. 資産別判断
GOLD
確認済み

金は四半期で約14%下落

2013年以来の大幅安
Reuters

なぜ重要か

ドル高と高金利は金に逆風。

売買判断
方向：弱気
評価：B級
BTC
確認済み

リスクオン環境

未確認（unverified）

ETFフロー

CME建玉

Funding

Basis

売買判断
NO_TRADE
ETH

BTC同様

NO_TRADE
WTI
確認済み

ホルムズ海峡輸送改善

停戦維持

Brent 72ドル近辺

WTI 70ドル近辺
Reuters

なぜ重要か

供給懸念後退で原油上昇圧力低下。

売買判断
中期強気
短期中立
USDJPY
確認済み

円は40年安値圏

約162.5円付近

介入警戒継続
Reuters

売買判断
方向：買い優勢
介入リスクあり
評価：B級
SPX
確認済み

S&P500終値 7499.36

四半期+14.9%
Reuters
+1

売買判断
強気
新規追撃は見送り
NASDAQ
確認済み

終値 26213

四半期+21.4%

AI関連主導
Reuters
+1

売買判断
強気
押し目待ち
DXY
確認済み

ドルは4四半期連続上昇
Reuters

評価

強気
US10Y
確認済み

利上げ観測継続

債券利回り上昇圧力継続
Reuters

評価

中立～強気
VIX
確認済み

パニック状態確認なし。

中立
5. A級候補

該当なし

理由

expected_r不足
イベント優位性不足
BTC確認不足
6. B級監視候補
USDJPY

A級昇格条件

160.5〜161.5押し
米金利維持
DXY高止まり
WTI

A級昇格条件

69〜70押し
供給懸念再燃
GOLD

A級昇格条件

4050〜4100戻り
ドル高継続
7. 触らない資産
BTC

理由

MES不明
ETF未確認
CME未確認
ETH

理由

BTC依存
根拠不足
SPX

理由

高値圏
RR不足
NASDAQ

理由

AI主導相場
押し待ち優先
8. 後日検証ポイント

雇用統計前の市場変化

USDJPY介入有無

WTI 70ドル維持

SOXX継続上昇有無

GOLD戻り売り機会

9. Obsidian保存用 Observation Draft
Markdown
# 2026-07-01 Daily Market Observation

Type: 一般市場Observation

## Summary
市場はリスクオン継続。
AI主導で株式が強い。
ドル高と円安が続く。
金は弱い。

## Observation
- S&P500高値圏
- NASDAQ高値圏
- USDJPYは162円台
- 原油70ドル前後
- 金は下落トレンド

## Evaluation
A級候補なし。
USDJPY、WTI、GOLDをB級監視。

## Interpretation
現在の市場は景気悪化より成長継続を重視している。
AI投資テーマが再び市場中心。

## Later Review
- 雇用統計
- USDJPY介入
- WTI需給
- SOXX推移

## Tags
#TSO #Observation #USDJPY #WTI #GOLD #SOXX
10. TSO_LOG
CSV
csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-07-01,TSO-20260701-001,USDJPY,BUY,B,MONITOR,160.5,161.5,159.4,163.5,165.0,2.2,58,0.35,,,,0.25,RISK_ON,60,,,,70,,USDJPY<159.4,162維持,verified
2026-07-01,TSO-20260701-002,WTI,BUY,B,MONITOR,69.0,70.0,67.5,73.0,75.0,2.0,55,0.30,,,,0.25,RISK_ON,58,,,,68,,WTI<67.5,70維持,verified
2026-07-01,TSO-20260701-003,GOLD,SELL,B,MONITOR,4050,4100,4140,3980,3920,1.8,56,0.28,,,,0.25,RISK_ON,55,,,,67,,GOLD>4140,戻り失敗,verified
2026-07-01,TSO-20260701-004,BTC,NONE,NO_TRADE,NONE,,,,,,,,,,100,0.00,NEUTRAL,,,,,,ETF/CME不足,ETF確認,unverified
JSON
JSON
[
{
"signal_id":"TSO-20260701-001",
"asset":"USDJPY",
"side":"BUY",
"rank":"B",
"expected_r":0.35,
"risk_pct":0.25
},
{
"signal_id":"TSO-20260701-002",
"asset":"WTI",
"side":"BUY",
"rank":"B",
"expected_r":0.30,
"risk_pct":0.25
},
{
"signal_id":"TSO-20260701-003",
"asset":"GOLD",
"side":"SELL",
"rank":"B",
"expected_r":0.28,
"risk_pct":0.25
},
{
"signal_id":"TSO-20260701-004",
"asset":"BTC",
"side":"NONE",
"rank":"NO_TRADE",
"verified_status":"unverified"
}
]
情報源
