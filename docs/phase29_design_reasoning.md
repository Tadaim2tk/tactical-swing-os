# Phase 29 設計推論の引き継ぎ（2026-07-04）

このドキュメントは「**難しい推論は済んでいる。以後は実行と検証だけでよい**」状態を作るためのもの。
以後のセッション（実装担当モデル）は、ここに書かれた設計を**再設計せずに実装**すること。
設計の変更が必要になった場合は、その理由を明記して人間の判断を仰ぐ。

---

## 0. 実行モードの原則（以後のセッションへ）

1. **再設計しない。実行する。** 本書と docs/governance_reform_2026-07.md が設計の正。
2. 迷ったら `insufficient_data` / `blocked` に倒す（false green の禁止は不可侵）。
3. **ゲートを弱める変更は書かない**（閾値の緩和・条件の削除・n の引き下げ）。強める/追加も原則しない（アンチ停滞: ガード追加はループ前進ではない）。
4. 新しい統計手法を発明しない。`stat_guards.py` にあるもの（t検定 / PSR / DSR / decay）だけを使う。
5. 各マイルストーンでは §3 のチェックリストを**そのまま**実行する。
6. 変更はすべて小さいPRで。テスト削除・書き換えによる green 化は禁止（不可侵 #6）。

---

## 1. Outcome 連結の設計（昇格ゲート `no_outcome_linkage` の解除）

### 1.1 目的と量

昇格ゲートが要求する系列は **d_i = R(weighted の意思決定_i) − R(base の意思決定_i)**。
測りたい量は「**ポリシー全体の価値差** E[d]」であり、「変わった行だけの条件付き差」ではない。

### 1.2 ペアの定義（重要な統計判断・変更禁止）

- ペア = 同一 (date, asset, signal_id)。shadow 側と評価側を signal_id で join する。
- **side は weights で変わらない**（shadow は rank/strength のみ変える）。よって取引そのもの
  （entry/SL/TP）は同一で、差が出るのは「actionable ⇔ NO_TRADE の入れ替わり」だけ。
- ペアの4分類:

| base | weighted | diff の定義 |
|---|---|---|
| actionable | actionable | **0**（同一トレード） |
| actionable | NO_TRADE | **− R_base**（weighted は見送った） |
| NO_TRADE | actionable | **+ R_hypothetical**（下記 1.4） |
| NO_TRADE | NO_TRADE | **0** |

- **diff=0 のペアも系列に含める（ゼロ埋めが正しい）。** 理由: ゼロを除外すると
  「E[d | 決定が変わった]」という別の量になり、影響を過大評価する選択バイアスが入る。
  ゼロ込みなら identity weights → 全ゼロ → ゲートの `zero_difference` で blocked、と現行実装と整合。
  ゼロが多いほど有意になりにくいのは**正しい保守性**（決定をほとんど変えない候補は、変えた分で
  大きな差を出さない限り昇格材料にならない）。
- ただし **divergent_pairs（diff≠0 になり得たペア数）を必ず併記**する。gate の n とは別に、
  「実際に何件の決定が変わったか」を人間が見られるようにする（n=300 でも divergent=2 なら
  その有意性は2件が駆動している、と分かる状態にする）。

### 1.3 R の取得（base 側）

- 確定した評価（`results/evaluations.csv` / `latest_evaluations.csv` の realized R）を使う。
  **評価が閉じたペアだけを系列に入れる**（awaiting は入れない。捏造しない）。
- R の定義は評価側の既存定義（SLキャップ込みのトレードR）をそのまま使う。
  PROTO-0001 の終値Rとは別物（あちらは判断の質、こちらはポリシー価値）。混ぜない。

### 1.4 反実仮想 R（base=NO_TRADE, weighted=actionable の行）

このケースだけ「起きなかったトレード」の R が要る。設計:

- NO_TRADE 行にも entry_low/entry_high/sl/tp1 はシナリオ値として存在する。
  **同じ評価ロジック**（evaluate_signal 系の充足判定）を OHLC に対して仮想適用して R を得る。
- 充足判定（entry ゾーンに価格が入ったか）が**判定不能／未充足**の場合は、そのペアを
  `uncomputable_counterfactual` として**系列から除外し、除外数を必ず表示**する（正直表示）。
  勝手に 0 と置かない（0 は「差がない」という主張であり、不明とは違う）。
- 実装は独立モジュール `src/link_shadow_outcomes.py`（新設）とし、evaluate_signal の関数を
  import して使う。generate_signal / evaluate_signal 本体は変更しない。

### 1.5 データ配管

- 出力: `data/shadow_outcome_diffs.csv`（git追跡・データ追記コミット対象に追加してよい）
  列: `date, asset, signal_id, weights_version, pair_type, base_r, weighted_r, diff, evaluation_closed_at`
- **weights_version はその日の shadow 実行時の版**を使う（`results/shadow_weighted_signals.csv`
  に版が載っている。無ければ ledger の date→version で引く）。版が違う行を混ぜて集計しない。
- ゲートへの接続: `shadow_weights.build_summary` が本CSVから「現行 approved 版と同版」の diff 系列を
  読み、`evaluate_promotion_gate(diffs, comparisons)` に渡す。**identity 版では全ゼロ → blocked のまま**
  が正しい（テスト済みの不変条件）。
- 実行タイミング: daily_cycle の evaluate 後に1ステップ追加（soft-fail・data追記コミットに同乗）。

### 1.6 やってはいけないこと（このセクションの罠）

- ✗ 評価が閉じる前のペアを入れる（awaiting を 0 やモメンタム推定で埋める）
- ✗ ゼロペアを除外して n を divergent だけにする（過大評価バイアス）
- ✗ 版をまたいで diff を合算する
- ✗ SLキャップ前の終値Rと評価Rを混ぜる

---

## 2. Weights 語彙のギャップ分析（初の非identity候補に向けて）

### 2.1 構造的事実

OBS-20260608-WTI の教訓仮説は「**regime=oil_supply_shock × 過熱(ffs高) のとき momentum 由来の
A昇格を減点**」。しかし現在の approved_weights 語彙は
`global{trend/momentum/volatility/risk_penalty/rank} × asset × rank × side` の**無条件スカラー倍**のみで、
**条件付き（regime依存）の項を表現できない**。つまり「昇格経路は存在するが、最初の実仮説が
その語彙で書けない」— これが現在の設計ギャップである。

### 2.2 選択肢と判断材料（人間が選ぶ。実装モデルは先走らない）

**案A: 語彙拡張 `regime_weights`（schema_version 2）**
```json
"regime_weights": {"oil_supply_shock": {"risk_penalty_weight": 1.5, "momentum_weight": 0.8}}
```
- 意味: その regime の日だけ global 係数に乗算。shadow 再構成は「regime を読んで係数を合成」の1行追加。
- 長所: shadow 比較フレームがそのまま使える。差分が weights ファイルだけで表現され、監査が簡単。
- 短所: 「ffs>閾値のとき」のような**条件は書けない**（regime 単位まで）。粒度が粗い。
- 適用範囲: 仮説の「regime で一律減点」近似としては十分。まずここから。

**案B: ルール変更（generate_signal の risk_penalty に regime×overextension 項を追加）**
- 意味: `calc_risk_penalty` に「regime がショック系 かつ ffs>80 なら +N」を加える通常のPR開発。
- 長所: 仮説を正確に表現できる。ガバナンス改革で generate_signal のPR開発は合法。
- 短所: **shadow 比較フレームの外**に出る（weights 差分でなくコード差分になる）。効果検証は
  ablation 的な before/after 再構成が必要で、比較の自動蓄積が使えない。
- 適用範囲: 案Aで方向性が確認できた後の精密化として。

**推奨順序: A →（Aの shadow 比較が materials_ready を出したら）→ B を検討。**
どちらも実施は「候補を書く人間承認PR」から。単発観測しか根拠がない現時点では**まだ書かない**
（ゲートがどうせ blocked にする。まず outcome 連結 §1 を先に）。

### 2.3 実装順序（依存関係）

```
§1 outcome 連結（これが無いと何を昇格させる根拠も生まれない）
 → 案A の語彙拡張 SPEC（schema_version 2 の JSON スキーマと再構成式だけ先に固定）
 → 適格データが揃った時点で候補 weights PR（人間）
```

---

## 3. マイルストーン実行手順書（チェックリスト）

### 3.1 類似局面検索の初稼働（目安 7/8。memory 過去局面 5 日到達時）

1. `results/similar_narrative_summary.json` の `status` が `insufficient_data`→`ok` に変わったことを確認
2. `results/similar_narrative_cases.csv` の全行で `similar_date < query_date` を機械確認（1行でも違えば即報告・使用停止）
3. Dashboard の類似局面検索セクションに表が出て、「signal score 未接続」の注記が残っていることを確認
4. 類似度の値域チェック: 全行 0 <= similarity <= 1（TF-IDF+cosine の性質。負や>1が出たら実装バグ）
5. **罠**: 初期は corpus が小さく、類似度が高く出やすい（母集団が狭いだけ）。「高い類似度=強い根拠」と
   読まない。レポートの注意書きが正しく機能しているかだけ見る。

### 3.2 shadow 30 比較到達（目安 7/15）

1. `promotion_sample_ready: true` になる（蓄積の進捗表示）
2. **`promotion_gate.decision` は `blocked` のままが正しい**（理由: `no_outcome_linkage`、
   §1 実装後は `zero_difference`）。materials_ready になっていたら**逆に異常**（identityで差が出るはずがない）
3. この時点でやることは「§1 outcome 連結の実装PR」（未着手なら）

### 3.3 ablation の verdict 初出（n_pairs>=30 到達時）

1. `results/ablation_arm_comparison.csv` の verdict を確認
2. **`no_significant_difference` は失敗ではない**。「テキスト層は現時点で価値を証明していない」という
   正しい知見であり、そのまま記録する。improves が出るまで signal 接続はしない
3. `degrades` が出た場合も貴重な知見（テキスト層の使い方が悪い可能性）。閾値をいじって
   improves を探しに行くのは**後知恵の典型**なので絶対にしない（閾値変更は人間PRのみ）
4. cohort の対称性を確認: `ablation_cohort.csv` で (date,asset,horizon) ごとに3行あるか

### 3.4 C-1: TF-IDF vs embedding 比較（APIキー登録後・1回だけ）

目的: **embedding が retrieval の結論を変えるか**を数字で見る。効くかどうかの判断はその後。

手順（スクリプト新設不要・使い捨てで良い）:
1. `TSO_EMBEDDING_PROVIDER=openai OPENAI_API_KEY=... python src/retrieve_similar_narratives.py` を実行し
   `results/similar_narrative_cases.csv` を `_openai.csv` として退避
2. 環境変数なしで再実行（TF-IDF）→ `_tfidf.csv`
3. 比較指標: (a) 各 query_date の top-5 類似日集合の Jaccard 重なり、(b) similarity 順位の Spearman 相関
4. 判断基準: Jaccard >= 0.6 なら「結論はほぼ同じ → TF-IDF のまま運用（コスト0）」。
   Jaccard < 0.6 なら「retrieval が実質的に変わる → evaluate_narrative_similarity の方向一致率を
   両 provider で比較し、良い方を採用する Issue を立てる（採用は人間判断）」
5. **罠**: 「embedding の方が意味を分かっているはず」という事前信念で決めない。数字だけで決める。

#### C-1 結果（2026-07-09 実施済み・CI run 29004885624 / 装置は PR #87）

- mean Jaccard(top-5) = **1.0**（query 3日: 7/7, 7/8, 7/9 すべてで top-5 集合が完全一致）。順位の Spearman は 0.7 / 0.9 / 0.3
- 判定: **equivalent**（top-5 は両 provider で同一）。凍結基準の既定は「TF-IDF のまま運用（コスト0）」だが、**人間判断（2026-07-09）で `TSO_EMBEDDING_PROVIDER=openai` を維持**: 検索結論が同一である以上どちらでも成立し、少額の API コストを許容して embedding を本番使用（API 失敗時は TF-IDF へ自動フォールバック）。`OPENAI_API_KEY` secret も残置
- 正直な注記: 候補コーパスが 5〜7 日と小さく、7/7 は候補5日ちょうどで一致が強制、7/8 も最小 Jaccard 0.67 と閾値超えが構造的に確定していた。実質の判別力があった query は 7/9 のみ（最小 0.43、Spearman 0.3）。判定は凍結基準どおり有効だが、コーパスが数倍に育ち narrative retrieval が意思決定に効き始めたら `embedding_comparison.yml` の workflow_dispatch 一発で再確認する価値がある
- 生データ: `data/embedding_comparison_c1_2026-07-09.json`（Actions artifact は90日で失効するため commit で恒久化）

### 3.5 適格 A-rank イベント発生時（CBS>=80 & EMS>=70）

1. `python src/run_observation_loop.py` を実行（run_type=qualifying になる）
2. vault の PROTO-0001 Observation Log の**表に**正式記録（dry-run とは違い、表に入れる）
3. +5営業日後に同コマンド再実行で pending→確定

---

## 4. 既知の非バグ挙動（誤修正の防止）

以後のセッションが「バグに見えるが仕様」を壊さないためのリスト:

- **cron 遅延で memory_date が翌日になる**: news は 21:50 UTC 予定が実際 22:4x に走るため、
  cutoff(21:55) を過ぎ、memory_date は翌日になる。これは「その夜のニュースは翌日のシグナルの材料」
  という**正しい as-of** であり、修正禁止。
- **shadow の rank_changes=0 / 全 diff 0**: identity weights の帰結。正常。
- **`promotion_sample_ready: true` かつ `promotion_gate: blocked` の併存**: 前者は蓄積進捗、
  後者は統計的成立。別物として両方表示する設計（false green 防止）。
- **similar narratives の `no_query_document`**: 当日の allowed ニュースがまだ無い時間帯に出る。障害ではない。
- **ablation で NONE 行の r が NaN**: non-actionable は結果を持たない設計。0 で埋めない。
- **Pages デプロイの一過性失敗**: 2026-07-03/04 に「Deployment failed, try again later」が2回発生、
  成果物は正常でリトライで成功した前例あり。まず1回リトライ→ githubstatus 確認→ それでもダメなら報告。

---

## 5. 今後の優先順位（人間と合意済みの順）

1. **§1 outcome 連結**（`link_shadow_outcomes.py` + ゲート接続 + テスト）— 最優先。
   これが無いと 7/15 に 30 比較が揃っても何も判断できない
2. §2 案A の SPEC 固定（JSON スキーマと再構成式のみ。候補値はまだ書かない）
3. C-1 — **済（2026-07-09）**: equivalent、TF-IDF 続行（結果は §3.4 に記録）
4. Phase 26.2 コスト値（人間の出典付き入力待ち・変わらず）

各項目とも: 小さいPR・テスト付き・正直表示・ゲートを弱めない。


---

## 6. 全判断採点の原則（2026-07-09 人間指示による追加）

**「全ての判断を記録し、後日採点する」— 見送り・B級・NO_TRADE も学習サンプルである。**

false green（データ不足を健全と偽る）と対を成す失敗モードとして、
**サンプル廃棄**（保守側デフォルトで判断を採点対象から外す）を禁止する:

- 手動予測台帳 data/signal_log.csv は `score_prediction_log.py` が**全行**を遡及採点する
  （+1/3/5/10営業日 close-R・PROTO同様の反後知恵・awaiting の冪等更新・
  データ品質不一致は補正せず suspect_data で除外+可視化）。
- 新しい判断ログ（ChatGPT日次）は台帳に追記すれば翌日から自動採点される。
  スキーマ差異（BUY/SELL表記・verified_status 列・TSO-YYYYMMDD-NNN形式）は正規化で吸収。
- 集計は件数と勝敗を常に表示し、n<30 は statistical_basis=insufficient_data を併記
  （「表示しない」のではなく「判断材料未満と明示して表示する」）。
- **禁止**: ランクによる採点対象の選別 / 「配線しない」を「採点しない」と拡大解釈すること /
  実売買サイズの提案（B+級 0.25% のような資金配分は本リポジトリの責務外・不可侵 #1）。
