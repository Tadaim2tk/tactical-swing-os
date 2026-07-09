# 2026-07-02 daily TSO output (prose, recovered 2026-07-09)
# source: 毎朝7時タスク確認 https://chatgpt.com/c/6a419a9e-84c8-83e8-9f82-af43b8e33db9
# format: prose (TSO_LOG-style csv block appears in-chat but was never saved as a .csv file that day)

TSO Daily Signal Log
TSO Daily Signal Log（2026-07-02）
1. 本日の結論
新規エントリー

A級候補なし

B級監視候補

USDJPY（押し目買い）

GOLD（戻り売り）

WTI（押し目待ち）

NO_TRADE

BTC

ETH

SPX

NASDAQ

理由：
BTC・ETHはETFフロー、CME建玉、Funding等の確認が不足しておりルール上NO_TRADE。SPX/NASDAQは上昇トレンド継続だが高値圏でRR（リスクリワード）が悪化。
Reuters
+1

2. 前回判断の簡易検証
USDJPY

前回：B級買い監視

結果：

162円台後半維持

日米金利差継続

円安トレンド継続
Reuters
+1

評価：
監視継続で妥当

WTI

前回：押し目買い監視

結果：

WTIは68～70ドル帯

イラン関連供給懸念後退で軟調
Reuters

評価：
買い急がず正解

GOLD

前回：戻り売り監視

結果：

金は反発（+1.4%）
Reuters

評価：
戻り売り候補維持
まだ明確な下落再開は未確認

3. 市場全体の前提
レジーム判定

中立～ややリスクオン

理由

S&P500は堅調

Dowは高値圏

Nasdaqはやや失速

VIXは16付近で落ち着いている
Trading Economics
+1

原油下落はインフレ圧力低下要因

雇用統計待ちで様子見も増加

判定

リスクオン 55
中立 35
リスクオフ 10
4. 資産別判断
GOLD
確認済み

前日+1.4%反発
Reuters

なぜ重要か

前四半期の急落後の自律反発か、本格反転かの分岐点。

売買判断
方向：弱気寄り
評価：B級
BTC
確認済み

リスクオン環境継続

未確認（unverified）

ETFフロー

CME OI

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

WTI 68.23ドル付近

Brent 71.34ドル付近

イラン関連供給懸念緩和
Reuters

売買判断
中立
押し目待ち
USDJPY
確認済み

162.6円近辺

40年ぶり円安圏

介入警戒継続
Reuters
+1

売買判断
方向：買い優勢
評価：B級
SPX
確認済み

7500近辺

高値圏維持
Trading Economics

売買判断
強気維持
追撃は見送り
NASDAQ
確認済み

一部大型テックが重石

AIテーマ継続
Google
+1

売買判断
強気維持
押し待ち
DXY
確認済み

Fedの利上げ観測が下支え。
Reuters

評価

やや強気
US10Y
確認済み

10年債利回り 約4.40%。
WSLS

評価

中立〜強気
VIX
確認済み

16.18付近。
Trading Economics
+1

評価

中立
5. A級候補

本日該当なし

理由

expected_r不足
イベント優位性不足
BTC確認不足
6. B級監視候補
USDJPY

A級昇格条件

161〜162への押し
米10年債4.4%以上維持
DXY上昇継続
GOLD

A級昇格条件

反発失速
ドル高継続
4100近辺で上値停止
WTI

A級昇格条件

68ドル維持
供給懸念再燃
7. 触らない資産
BTC
MES不明
ETF未確認
CME未確認
ETH
BTC依存
検証不足
SPX
高値圏
RR不足
NASDAQ
押し待ち優先
8. 後日検証ポイント

米雇用統計

USDJPY介入有無

WTIが68ドルを維持するか

GOLD反発継続か失速か

SOXXの7/6採点対象推移

9. Obsidian保存用 Observation Draft
Markdown
# 2026-07-02 Daily Market Observation

Type: 一般市場Observation

## Summary
市場は中立からややリスクオン。
株式は高値圏維持。
円安継続。
原油は軟調。
金は反発。

## Observation
- USDJPYは162円台後半
- WTIは68ドル台
- S&P500は7500近辺
- VIXは16付近
- GOLDは反発

## Evaluation
A級候補なし。
USDJPY、GOLD、WTIをB級監視。

## Interpretation
市場は雇用統計待ち。
方向感よりもイベント待機モード。

## Later Review
- 雇用統計
- USDJPY介入
- GOLD反発継続性
- WTI需給

## Tags
#TSO #Observation #USDJPY #GOLD #WTI
10. TSO_LOG
CSV
csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-07-02,TSO-20260702-001,USDJPY,BUY,B,MONITOR,161.0,162.0,159.8,164.0,165.5,2.0,58,0.34,,,,0.25,NEUTRAL,60,,,,70,,USDJPY<159.8,162維持,verified
2026-07-02,TSO-20260702-002,GOLD,SELL,B,MONITOR,4080,4120,4160,4010,3950,1.8,55,0.30,,,,0.25,NEUTRAL,56,,,,68,,GOLD>4160,反発失速確認,verified
2026-07-02,TSO-20260702-003,WTI,BUY,B,MONITOR,68.0,69.0,66.5,72.0,74.0,2.1,56,0.31,,,,0.25,NEUTRAL,57,,,,67,,WTI<66.5,68維持,verified
2026-07-02,TSO-20260702-004,BTC,NONE,NO_TRADE,NONE,,,,,,,,,,100,0.00,NEUTRAL,,,,,,ETF/CME不足,ETF確認,unverified
JSON
JSON
[
{
"signal_id":"TSO-20260702-001",
"asset":"USDJPY",
"side":"BUY",
"rank":"B",
"expected_r":0.34,
"risk_pct":0.25
},
{
"signal_id":"TSO-20260702-002",
"asset":"GOLD",
"side":"SELL",
"rank":"B",
"expected_r":0.30,
"risk_pct":0.25
},
{
"signal_id":"TSO-20260702-003",
"asset":"WTI",
"side":"BUY",
"rank":"B",
"expected_r":0.31,
"risk_pct":0.25
},
{
"signal_id":"TSO-20260702-004",
"asset":"BTC",
"side":"NONE",
"rank":"NO_TRADE",
"verified_status":"unverified"
}
]
情報源
