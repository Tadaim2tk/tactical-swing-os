# TSO Daily Signal Log — 出力契約プロンプト v3（全経路共通）

このファイルは (a) ChatGPT スケジュールタスク「TSO Daily Signal Log v2」（毎日7:00、
同名会話）のタスク本文の正本ミラー、かつ (b) `scripts/tso_daily_gpt.sh` が codex exec へ
**そのまま標準入力で渡す実行プロンプト**である（#102、web検索有効）。

v3 は 2026-07-27、v2タスク移設後の連続失敗（7/24「貼り付けプロンプト」拒否・7/25-26
実行なし）を受けた**ユーザー主導の改定**（ChatGPT との対話でタスク本文を全面書き換え）。
核心は「出力停止を最重大失敗とし、検証を一次情報限定から複数ソース・モデル推測許容へ緩和」。
経緯・差分・リスクは docs/gpt_prompt_changelog.md (8)。v2全文は git 履歴を参照。
ChatGPTタスク本文との差分は末尾の**ターミナル経路向け追加2項のみ**。

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
- SL幅は通常想定のまま広げない（2026-09-01改定: 7/17導入の「2倍拡張」はn=51の再判定で
  効果を実証できず、効いた形跡のある時間決済のみ残す人間決定。changelog(13)）。
- 決済は5営業日の時間決済を基本とし、TP1/TP2は参考目標として記帳する。
- rr は entry中点・SL・TP1 から自分で再計算し、一致を確認してから記帳する（8/27に算術ずれ3件の実績）。
- regime列は RISK_ON / RISK_OFF / NEUTRAL / MIXED / EVENT / UNKNOWN の6語のみ。ニュアンスは本文に書く。
- 本文の冒頭付近に、実行に使用しているモデル名を1行で明記する。
- GOLDは基準にする限月を毎回明記し、日をまたいで同じ限月の価格で比較する（現在は12月限を基準）。
- 本文に「本日の市場の主役」と判断する資産を1語で明記する（検証用の観察項目。LOG28列は不変）。
- 本文に、その日BTC/ETHの判断に**実際に使えた根拠の有無**を1行で記す
  （書式: `crypto_grounds: etf=有/無, cme=有/無`）。これは**根拠を探しに行けという指示ではなく、
  無いことは減点でも失格でもない**。見送りの理由を後から追えるようにするためだけの記録欄である
  （crypto専用の週次タスクを廃止した代わりの観察列。LOG28列は不変。changelog(14)）。

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

## 月次較正2026-08の採用ルール（2026-08-15適用・GPT月次提案の全採用は人間決定）

- 運用モードは通常寄り防御: 1取引0.25%、A級のみ0.50%、日次合計0.50%、攻撃モード停止。
- A級の追加条件: RR最低1.2（原則1.5以上を優先）、SL距離はTP1距離の2.0倍以下、
  XM最小ロットでの想定実損が許容額（約3,000円）以内。満たさない場合はシグナル成立でも
  「実取引NO_TRADE」と本文に明記する。
- B級のうち CBS70以上・EMS60以上・RR1.5以上・較正後win_prob0.50以上・想定実損3,000円以内
  を満たすものは「B+観察候補」として本文に明記する（A級への自動昇格はしない）。
- 許容実損は2026-08-27に約1,500円→約3,000円へ引き上げ（人間指示。3,000円程度の想定実損で
  実取引NO_TRADEへ格下げしない。理論risk_pctの上限とは別枠で、最小ロット制約時の実損上限として扱う）。
- 本文の判断説明では申告win_probに較正後参考値を併記してよい（上方補正は+0.05まで）。
  ただしTSO_LOGのwin_prob列には従来どおり生の主観確率のみを書く（28列の構成・単位は不変）。

## ターミナル経路向け追加（ChatGPTタスク本文には未反映・実質は共通ルール）

- NO_TRADE行の `type` の直後から `expected_r` までの空欄は**8列ちょうど**。その次の列が
  `tq_score`。余分な空欄を1つ入れると取込時に `date` と `signal_id` がずれて全行rejectになる。
  例: `...,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,42,38,78,,RISK_OFF,...`（2026-07-24の取込失敗対策、#102）
- 実売買・発注の指示はしない（これは予測記録であり売買指示ではない）。
