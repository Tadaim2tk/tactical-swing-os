# SPEC-RNC-001: 遡及市場コーパス（過去データのナラティブ事後生成）

status: v0 実装（2026-08-31 人間発案「ERSと同じ感じで過去データのナラティブを作る」）

## 目的

ニュース基盤の作り替え（監査後の人間判断#3、2026-08-31）の土台として、過去約5年の
日次市場データ（10資産・VIX・金利・ドル・先行遅行関係）から、ルール計算の特徴量と
ローカルLLMによる日次ナラティブを**事後生成**する。類似局面検索・レジーム較正・
将来のナラティブ評価軸の教師データに使う。

## 不可侵の区別: これは「再構成データ」である

- 本コーパスは **retrospective_derived**（現在の確定値から事後計算）。
  point-in-time feature store（market_context_daily.csv = as-seen）とは**別物**であり、
  併合しない。「当時モデルが何を見ていたか」の代用に使うことを禁ずる。
- 全ファイルに provenance 列/フィールド（source, fetched_at, generated_at, instrument）を持つ。

## 監査（audit_blindspots_2026-08-31）の教訓の織り込み

1. リターンは**資産固有カレンダー上の close-to-close**・`pct_change(fill_method=None)`。
   資産間で日付をunionしたwide表での一括pct_changeは禁止（ERS#1）。
2. USDJPY を含む FX は open を使わない（P1-1: Yahoo FXのopenは寄値でない）。
3. 市場跨ぎの先行遅行は「暦の1日前」でなく**相手市場の直近の閉じたバー**
   （merge_asof backward, allow_exact_matches=False。休み跨ぎは累積。ERS#2）。
4. 閉じた語彙（レジーム等のラベル）は**ルールで計算**し、LLMには自由記述
   （何が主導したか・どの乖離が異常か）だけをさせる（ERS#9）。
5. 測定器の版を固定し digest で記録する（ERS METHOD_TRANSFER#2）:
   モデルcommit / mlx-lm版 / プロンプト全文sha / 温度 / 生成長 / 前処理規則。
   実行時に宣言と実環境の一致を検査し、違えば生成しない。
6. ルール閾値（レジーム等）は**当てはめで選ばず事前に宣言**し「層別用・未検証」と
   明記する（ERS#8: 探索して選んだ閾値を発見と呼ばない）。

## 構成

```
tools/retro_build_market.py      価格層: yfinance 5y 一括取得(一度きり) → 資産別リターン
                                  → 日次結合(資産別bar_date明示) → ルール・ラベル
tools/retro_fetch_gdelt.py       ニュース層: GDELT DOC 2.0 API から日次見出し(一度きり・
                                  レート控えめ・再開可能)。取得は広く、選別は読む側
tools/retro_generate_narratives.py  ナラティブ層: ローカルLLM(版固定)で日次ナラティブ生成
data/retro/prices_long.csv       資産別 close-to-close リターン(long形式)
data/retro/market_daily.csv      日次結合+ルール特徴量(bar_date_ASSET列つき)
data/retro/news_gdelt.csv        日次見出し(date, title, source, url, tone)
data/retro/narratives.jsonl      LLM生成ナラティブ(1行=1営業日)
data/retro/instrument.json       測定器の版manifest+digest
```

## ラベル語彙（閉・ルール計算・v1閾値は事前宣言）

- risk_state: risk_on / risk_off / mixed / neutral（SPXリターンとVIX変化の符号・大きさ）
- vol_state: calm(VIX<16) / elevated(16-24) / stressed(>24)
- yield_move / usd_move / crypto_move: up / down / flat（|変化|の事前宣言閾値）
- 閾値はコード内 THRESHOLDS_V1 に集約し「層別用・未検証・変更は版を上げる」と注記。

## LLM の役割（自由記述のみ）

入力: その日のルール特徴量表＋（あれば）見出し上位。温度0・思考モード無効。
出力: 日本語2〜4文のナラティブ、主導資産、特異な乖離の指摘。
JSONの閉じたフィールドはルール層からコピーし、LLM出力からは採らない。

## 更新規約

- 取得は一度きり。再実行は差分日付のみ（resumable）。
- narratives.jsonl は append-only。instrument が変わったら別versionとして併存させ、
  旧行を書き換えない。

## 主役アセットのレンズ（2026-08-31 人間発案で追加）

「その時市場の主役だったアセットを切り替えながら見る」ため、価格層に機械判定の主役列を持つ:

- `leader_asset` / `leader_score` / `leader_margin`(2位との差=明確さ)
- 判定式 LEADER_V1(事前宣言・層別用・未検証): 直近20営業日の
  他資産との|相関|平均 × 自身の活発度(平常120日比)。相関は両資産にバーがある日のみで計算。
- 歴史照合(実装時のサニティ): 2021-11=US10Y(利上げ転換) / 2022-03=GOLD(ウクライナ) /
  2022-09・2023-03=VIX(弱気相場・SVB危機) / 2023-11=ETH(ETF期待) / 2026-08=ETH(ETFフロー) —
  既知の相場史と整合。
- ナラティブ生成は主役を軸に「この日の値動きが主役の構図を追認したか崩したか」を記述し、
  主役交代の兆しを anomaly に書く。閉じた値(主役そのもの)はルール層からコピーする。

## ERSコーパスからの借用（2026-09-03）

ERS側（`~/.ers-corpus/regime_history/regime_2021_2026.parquet`）が2021-2026のマクロ20系列を
既に取得済みのため、**再取得せず参照する**（一度きり取得の原則）。

- 借用ツール: `tools/bridge_ers_macro.py` → `data/retro/macro_ext.csv`
- 借りる系列（TSO本体10資産に無いもののみ）: 銀(SI=F)・銅(HG=F)・半導体(^SOX)・日経(^N225)・
  5年金利(^FVX)・30年金利(^TYX)・SOL・XRP・TOPIX ETF・J-REIT ETF、計10系列15,381行
- provenance 列に `ers_corpus_reference` と取得元ファイルパスを刻む。
  **TSOが自分で取得した系列と混ぜない**（出所を追えなくしない）。
- 更新: ERS側が伸びたら再実行するだけ。TSOからネットワークは叩かない。
