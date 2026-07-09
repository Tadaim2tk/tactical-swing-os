# 2026-07-03 daily TSO output (prose, recovered 2026-07-09)
# source: 毎朝7時タスク確認 https://chatgpt.com/c/6a419a9e-84c8-83e8-9f82-af43b8e33db9
# format: prose (TSO_LOG-style csv block appears in-chat but was never saved as a .csv file that day)

TSO Daily Signal Log
TSO Daily Signal Log（2026-07-03）
1. 本日の結論
新規エントリー

A級候補なし

B級監視候補

USDJPY（押し目買い）

GOLD（戻り売り）

WTI（押し目買い再評価）

NO_TRADE

BTC

ETH

SPX

NASDAQ

理由：
雇用統計系データが弱くドル安方向へ振れた一方、半導体・AI関連には需給悪化懸念が出ているため、指数は方向感がやや不安定。BTCはETF/CME確認不足のためルール通りNO_TRADE継続。
Reuters
+1

2. 前回判断の簡易検証
USDJPY

前回：

BUY監視

結果：

ドル指数下落

円はやや反発

介入なし確認

評価：
ロング優勢は維持だが強さはやや低下。
Reuters
+1

GOLD

前回：

SELL監視

結果：

ドル安で金反発

評価：
即売りではなく戻り待ち継続が正解。
Reuters
+1

WTI

前回：

押し目買い監視

結果：

70ドル割れ近辺

ホルムズ海峡リスク後退

評価：
買い急がず正解。
Reuters
+1

3. 市場全体の前提
レジーム判定

中立

理由

雇用データ悪化

ドル下落

金上昇

半導体株急落

ダウは堅調

強いリスクオンでも強いリスクオフでもなく、市場内部でセクターローテーションが発生している。
Reuters
+1

リスクオン 40
中立 45
リスクオフ 15
4. 資産別判断
GOLD
確認済み

ドル安で上昇

雇用悪化で利上げ期待後退

なぜ重要か

金利低下期待は金に追い風。

売買判断
方向：中立〜やや強気
評価：B級

Reuters

BTC
確認済み

リスク資産環境は悪化していない

未確認（unverified）

ETFフロー

CME建玉

Funding

Basis

MES

売買判断
NO_TRADE
ETH

BTC同様

NO_TRADE
WTI
確認済み

WTIは70ドル近辺

イラン停戦後の供給正常化観測

売買判断
中立

Reuters
+1

USDJPY
確認済み

円は依然40年安値圏

介入警戒継続

売買判断
方向：買い優勢
評価：B級

Reuters
+1

SPX
確認済み

S&P500は横ばい

AIセクター失速

売買判断
中立

Reuters
+1

NASDAQ
確認済み

半導体指数急落

AI需要への懸念

売買判断
弱気寄り

Reuters
+1

DXY
確認済み

ドル指数下落。

弱気

Reuters

US10Y
確認済み

雇用悪化で金利上昇圧力低下。

中立

Reuters

VIX
確認済み

パニック状態なし。

中立
5. A級候補

なし

理由

expected_r不足
イベント優位性不足
BTC確認不足
6. B級監視候補
USDJPY

A級昇格条件

161〜162円への押し
DXY反発
米金利反発
GOLD

A級昇格条件

ドル安継続
4200突破
WTI

A級昇格条件

70ドル回復維持
供給障害再発
7. 触らない資産
BTC
MES不明
ETF未確認
CME未確認
ETH
BTC依存
確認不足
SPX
方向感不足
RR不足
NASDAQ
半導体調整中
押し目形成待ち
8. 後日検証ポイント

半導体指数（SOX）の続落有無

SOXX採点対象の推移

USDJPY介入

GOLDの4200突破有無

WTIの70ドル回復

9. Obsidian保存用 Observation Draft
Markdown
# 2026-07-03 Daily Market Observation

Type: 一般市場Observation

## Summary
市場は中立。
ドル安。
金反発。
半導体株調整。

## Observation
- 雇用データ弱い
- ドル指数下落
- 金上昇
- 半導体株急落
- 円は依然安い

## Evaluation
A級候補なし。
USDJPY、GOLD、WTIをB級監視。

## Interpretation
AI相場の過熱修正が始まっている可能性がある。
ただし市場全体はまだ崩れていない。

## Later Review
- SOX指数
- SOXX
- USDJPY
- GOLD
- WTI

## Tags
#TSO #Observation #SOXX #USDJPY #GOLD #WTI
10. TSO_LOG
CSV
csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-07-03,TSO-20260703-001,USDJPY,BUY,B,MONITOR,161.0,162.0,159.8,164.0,165.0,2.0,57,0.33,,,,0.25,NEUTRAL,58,,,,69,,USDJPY<159.8,DXY反発,verified
2026-07-03,TSO-20260703-002,GOLD,BUY,B,MONITOR,4140,4180,4080,4250,4320,1.9,56,0.31,,,,0.25,NEUTRAL,57,,,,68,,GOLD<4080,4200突破,verified
2026-07-03,TSO-20260703-003,WTI,BUY,B,MONITOR,69.0,70.0,67.0,73.0,75.0,2.0,55,0.29,,,,0.25,NEUTRAL,56,,,,67,,WTI<67.0,70回復,verified
2026-07-03,TSO-20260703-004,BTC,NONE,NO_TRADE,NONE,,,,,,,,,,100,0.00,NEUTRAL,,,,,,ETF/CME不足,ETF確認,unverified
JSON
JSON
[
{
"signal_id":"TSO-20260703-001",
"asset":"USDJPY",
"side":"BUY",
"rank":"B",
"expected_r":0.33,
"risk_pct":0.25
},
{
"signal_id":"TSO-20260703-002",
"asset":"GOLD",
"side":"BUY",
"rank":"B",
"expected_r":0.31,
"risk_pct":0.25
},
{
"signal_id":"TSO-20260703-003",
"asset":"WTI",
"side":"BUY",
"rank":"B",
"expected_r":0.29,
"risk_pct":0.25
},
{
"signal_id":"TSO-20260703-004",
"asset":"BTC",
"side":"NONE",
"rank":"NO_TRADE",
"verified_status":"unverified"
}
]
情報源
