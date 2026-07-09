# 2026-06-30 daily TSO output (prose, recovered 2026-07-09)
# source: 毎朝7時タスク確認 https://chatgpt.com/c/6a419a9e-84c8-83e8-9f82-af43b8e33db9
# format: prose (TSO_LOG-style csv block appears in-chat but was never saved as a .csv file that day)
# note: the report header in-chat reads「TSO Daily Signal Log」without a date; the date 2026-06-30 is fixed by the embedded Obsidian draft title and the TSO_LOG csv rows

TSO Daily Signal Log
TSO Daily Signal Log
1. 本日の結論
新規エントリー

A級候補なし

B級監視

GOLD（戻り売り監視）

USDJPY（押し目買い監視）

WTI（押し目買い監視）

見送り

BTC

ETH

SPX

NASDAQ

理由：
BTCはETF/CMEフロー確認不足のためルール上NO_TRADE優先。ETHも同様。株式指数は反発しているが、今週は米雇用統計を控えておりイベントリスクが大きい。
Reuters

2. 前回判断の簡易検証
BTC見送り

継続見送り

ETF/CME確認不足

ルール適合

評価：
見送り妥当

USDJPY

円安継続

160～162円帯推移

方向性は上昇継続
Reuters
+1

評価：
ロング優勢維持

GOLD

金価格は下落継続

原油上昇→インフレ懸念→利上げ観測→金売りの流れ
Reuters
+1

評価：
強気判断は不適切だった可能性

3. 市場全体の前提
現在のレジーム

ややリスクオン

理由

S&P500上昇

NASDAQ上昇

VIXは極端な警戒状態ではない

AI関連株への買い戻し発生

ただし中東リスク継続
Reuters

評価

リスクオン 60
中立 25
リスクオフ 15
4. 資産別判断
GOLD
何が起きているか

金価格急落

ドル高

利上げ観測上昇

なぜ重要か

金は金利を生まない資産のため高金利環境に弱い。

売買判断

短期：弱気

方向：売り優勢
評価：B級
BTC
何が起きているか

株式市場は反発しているが暗号資産の確証データ不足。

売買判断
NO_TRADE
理由：MES不足
ETF/CME未確認
ETH

BTC同様

NO_TRADE
WTI
何が起きているか

中東情勢不安で原油反発。WTI約70ドル台。
Reuters

売買判断
中期強気
短期押し目待ち
USDJPY
何が起きているか

161円台

1980年代以来の円安圏

日米金利差が依然大きい
Reuters
+1

売買判断
方向：買い
評価：B級
SPX
何が起きているか

S&P500 +1.17%反発。
Reuters

売買判断
強気
ただし雇用統計前
新規追撃は見送り
NASDAQ
何が起きているか

NASDAQ +2.07%。AI関連買い戻し。
Reuters

売買判断
強気
押し目待ち
DXY

ドル指数は100～101付近。高止まり。
Reuters
+1

評価

強気
US10Y

米10年債利回り

約4.38%。
Trading Economics

評価

中立〜強気
VIX

確認できた急騰なし。

中立
5. A級候補

本日該当なし

A級候補なし
6. B級監視候補
USDJPY

A級昇格条件

161.0近辺への押し
ドル指数維持
米10年債維持
WTI

A級昇格条件

69〜70ドル押し目
中東リスク継続
GOLD

A級昇格条件

戻り失敗
ドル高継続
7. 触らない資産
BTC

ETF確認不足

CME確認不足

ETH

BTC依存

SPX/NASDAQ

雇用統計前

8. 後日検証ポイント

米雇用統計結果

SOXXの反発継続有無

USDJPYが162突破するか

WTIが70ドル維持するか

GOLDが4000ドル割れを試すか

9. Obsidian保存用 Observation Draft
Markdown
# 2026-06-30 Daily Market Observation

Type: 一般市場Observation

## Summary
市場はややリスクオン。
株式反発。
ドル高継続。
金は弱い。

## Observation
- S&P500上昇
- NASDAQ上昇
- USDJPYは161円台
- 原油反発
- GOLD下落

## Evaluation
A級候補なし。
USDJPY・WTI・GOLDをB級監視。

## Interpretation
市場は中東リスクよりも景気堅調とAIテーマを重視。
ドル高と高金利が継続。

## Later Review
- 雇用統計
- USDJPY 162
- WTI 70維持
- GOLD 4000防衛

## Tags
#TSO #Observation #USDJPY #WTI #GOLD
10. TSO_LOG
CSV
csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-06-30,TSO-20260630-001,USDJPY,BUY,B,MONITOR,,,,,,,,,0.25,RISK_ON,60,,,,70,,USDJPY<159.5,162突破確認,partial
2026-06-30,TSO-20260630-002,WTI,BUY,B,MONITOR,,,,,,,,,0.25,RISK_ON,60,,,,68,,WTI<68,70維持確認,partial
2026-06-30,TSO-20260630-003,BTC,NONE,NO_TRADE,NONE,,,,,,,,,0.00,NEUTRAL,,,,,,ETF/CME不足,ETF/CME確認,unverified
JSON
JSON
[
{
"signal_id":"TSO-20260630-001",
"asset":"USDJPY",
"side":"BUY",
"rank":"B",
"risk_pct":0.25,
"regime":"RISK_ON"
},
{
"signal_id":"TSO-20260630-002",
"asset":"WTI",
"side":"BUY",
"rank":"B",
"risk_pct":0.25,
"regime":"RISK_ON"
},
{
"signal_id":"TSO-20260630-003",
"asset":"BTC",
"side":"NONE",
"rank":"NO_TRADE",
"risk_pct":0.0,
"verified_status":"unverified"
}
]
情報源
