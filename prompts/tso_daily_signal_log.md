# TSO Daily Signal Log — 出力契約プロンプト v3（全経路共通）

このファイルは (a) ChatGPT スケジュールタスク「TSO Daily Signal Log v2」（毎日7:00、
同名会話）のタスク本文の正本ミラー、かつ (b) `scripts/tso_daily_gpt.sh` が codex exec へ
**そのまま標準入力で渡す実行プロンプト**である（#102、web検索有効）。

v3 は 2026-07-27、v2タスク移設後の連続失敗（7/24「貼り付けプロンプト」拒否・7/25-26
実行なし）を受けた**ユーザー主導の改定**（ChatGPT との対話でタスク本文を全面書き換え）。
核心は「出力停止を最重大失敗とし、検証を一次情報限定から複数ソース・モデル推測許容へ緩和」。
経緯・差分・リスクは docs/gpt_prompt_changelog.md (8)。v2全文は git 履歴を参照。
ChatGPTタスク本文との差分は末尾の**ターミナル経路向け追加のみ**。

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
- Entry、SL、TP、RR、MAE想定、イベントリスクを確認する（ロット制約は人間が発注時に見る。changelog(20)）。
- BTCはMES<50またはETF/CME根拠不足ならNO_TRADE優先。ただしETF/CME欠損だけで分析自体を停止しない。
- A級条件は原則CBS>=75、EMS>=65、expected_r>=0.45、MAE想定<=0.25R。
- 最大日次リスクは通常0.50%。
- 避けるのは、WTIの供給ショック直後のmomentum追随と、参照系列の取り違え。NASDAQ / BTC / USDJPY の
  成行参加（判断日の終値までに帯へ来なければその終値で入る。2026-09-09 人間承認）は規則であって追随ではない。
  方向の確信が強い日に「追随になる」だけを理由に全資産を見送らない（9/16 は4資産を強いと書いて0件だった。changelog(20)）。
- SL幅は **1×ATR10 以上**を下限とする（ATR10 = 判断日の前日までの10本の日足の真の値幅の平均。
  2026-11-03 人間決定、changelog(20)）。狭いSLは日中の揺れで当たるだけで方向の誤りを教えない
  （9/16以降SL幅は0.5ATRに縮み、約定7件中6件がSL。幅を1×ATR10にした併走観測は全期間+8.4R）。
  TP1とrrは広げたSLから再計算する。広げた結果rrが1.2を割る判断はB級の監視行として記帳し、A級にはしない。
  7/17の「2倍拡張」（固定倍率、9/1に廃止）とは別物で、値幅に合わせた下限である。
- 決済は5営業日の時間決済を基本とし、TP1/TP2は参考目標として記帳する。
- 本文は素の Markdown だけで書く（見出し・箇条書き・表・```csv フェンス）。UI部品のタグ、サンドボックスの添付ファイル、
  ZIP は使わない。CSV は本文中の ```csv フェンスにそのまま書く（取込は会話の本文テキストからこのフェンスを読む。
  changelog(21)(22)）。
- rr は entry中点・SL・TP1 から自分で再計算し、一致を確認してから記帳する（8/27に算術ずれ3件の実績）。
- regime列は RISK_ON / RISK_OFF / NEUTRAL / MIXED / EVENT / UNKNOWN の6語のみ。ニュアンスは本文に書く。
- 本文の冒頭付近に、実行に使用しているモデル名を1行で明記する。
- GOLDは基準にする限月を毎回明記し、日をまたいで同じ限月の価格で比較する（現在は12月限を基準）。
- 本文に「本日の市場の主役」と判断する資産を1語で明記する（検証用の観察項目。LOG28列は不変）。
- expected_r は主観評価でよい。ただし **NASDAQ / BTC / USDJPY の3資産に限り、「Entry未到達で不参加」を
  下げ幅の理由に使わないこと**。この3資産には、判断日の終値までに帯へ来なければ
  その終値で成行で入る規則を置いた（2026-09-09、人間の承認）。不参加の確率を
  二重に引くと expected_r が過小になり、A級条件 0.45 の手前で落ちる（changelog(16)）。
  時間決済・イベント前の早期撤退を織り込むのは従来どおりでよい。
- 本文に、invalidation が発動したかを1行で記す（書式: `invalidation_check: <signal_id>=fired|not_fired|unknown, ...`）。
  対象は**資産ごとに、前日までに出した方向あり判断のうち最新の1件だけ**（最大10件）。同じ資産の古い判断は最新のものに
  引き継がれたとみなし、書かない。その最新の判断を出してから5営業日と、5本目の翌朝まで毎日書く（途中で見送りに変えた資産も、
  窓が閉じるまで書く）。`historical_pending_signals=unknown` のようにまとめて書かない。判定は価格で行う: invalidation に
  書いた水準を、判断日以降の高値・安値が越えていれば fired、越えていなければ not_fired。価格を確認できないときだけ unknown。
  推測で fired と書かない（changelog(15)(18)(22)）。

- B級の記帳の扱い（2026-11-03。changelog(19)(20)）:
  1. B級監視候補に挙げた資産は、rank=B の行として記帳する。監視用のEntry帯・SL・TP1は暫定値でよい。
     「正式なB級」と「監視水準」を分けない。本文に監視水準を書いたのに TSO_LOG では NO_TRADE、
     という形は禁止（2026-10 はこの形が31日中16日あり、台帳が空の間は検証も執行シミュレーションも止まる）。
  2. A級条件（CBS≥75・EMS≥65・expected_r≥0.45・MAE≤0.25R・RR≥1.2・SL距離≤TP1距離の2倍）は
     A級の条件であって、B級の記帳条件ではない。B級は「方向の見立てがあり、監視用の帯とSLを書けること」で成立する。
  3. 「実取引NO_TRADE」という注記は書かない。ロット数と1回の損失額の上限は人間が発注時に決めるもので、
     GPTの判断条件ではない（changelog(20)）。
  4. 見立てが続く日は、その日の帯とSLで毎日B行を出す（台帳は毎日の判断の記録であり、1本の見立てを
     1回だけ書く場所ではない。8月はこの形だった）。前日までの signal_id の invalidation_check は別に続ける。
  5. FOMC・CPI・日銀などのイベント前でもB行は出す。イベントは invalidation と本文に書く。
     イベント前に見送ってよいのは A級の新規だけ。
  6. 直前の判断が SL や fired になったことは、同じ資産の新しい見立てを止める理由にしない。
     止めるなら価格構造の理由を本文に書く。

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
- NO_TRADE行は `side=NONE, rank=NO_TRADE, type=NO_TRADE`、signal_id は `YYYYMMDD_ASSET_NONE_NO_TRADE`。type の直後から
  expected_r までの8列（entry_low, entry_high, sl, tp1, tp2, rr, win_prob, expected_r）と risk_pct は空欄にし、tq_score、
  opp_score、no_trade_score、regime、ems、ffs、cds、ias、cbs、mes は実評価値を入れる。
  例: `2026-11-12,20261112_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,38,29,82,,EVENT,42,40,35,30,39,32,VIX_close_missing,VIX_index,partially_verified`
- どの行も28列（カンマ27個）。出力前に数える（2026-11-11 は見送り4行が27列で、スコアが1列ずれていた。changelog(22)）。
- win_probは0〜1。数値は半角、桁区切り・通貨記号なし。
- signal_idはYYYYMMDD_ASSET_SIDE_TYPE形式。
- ObsidianやGitHubへ保存できなくても、チャット上の記録を必ず残す。

## 月次較正2026-08の採用ルール（2026-08-15適用・GPT月次提案の全採用は人間決定。2026-11-03 改定）

- 運用モードは通常寄り防御: 1取引0.25%、A級のみ0.50%、日次合計0.50%、攻撃モード停止。
- A級の追加条件: RR最低1.2（原則1.5以上を優先）、SL距離はTP1距離の2.0倍以下。
- B級のうち CBS70以上・EMS60以上・RR1.5以上・較正後win_prob0.50以上を満たすものは
  「B+観察候補」として本文に明記する（A級への自動昇格はしない）。
- ロット数と1回の損失額の上限（例: 3,000円）は、人間が発注時に決める。GPTはこれを判断の条件にしない。
  最小ロットで収まるか、実損がいくらになるかを理由に、NO_TRADEにもSLの縮小にもしない
  （2026-11-03 人間の言明: ロットと損失上限は売買判断とは別の話。8/15〜11/2の間この条件が判断に入り、
  SLを0.5ATRへ縮め、見送りを増やしていた。changelog(20)）。
- 本文の判断説明では申告win_probに較正後参考値を併記してよい（上方補正は+0.05まで）。
  ただしTSO_LOGのwin_prob列には従来どおり生の主観確率のみを書く（28列の構成・単位は不変）。

## ターミナル経路向け追加（ChatGPTタスク本文には未反映・実質は共通ルール）

- 実売買・発注の指示はしない（これは予測記録であり売買指示ではない）。
- （NO_TRADE 行の空欄8列と語彙の約束は、2026-11-11 に共通の「TSO_LOG固定28列」節へ移した。changelog(22)）
