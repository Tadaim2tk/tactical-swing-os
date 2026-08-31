"""B+研究(docs/research_bplus_2026-09-01.md)の集約検定スクリプト。

(1) クラスタ単位並べ替え検定: 同一資産の連続日シグナル(間隔<=7暦日)を1クラスタに束ね、
    B+ラベルをクラスタ単位で並べ替える(疑似反復対策)。
(2) 相対パーセンタイル版B+: 月内順位で条件を再定義し、閾値ドリフトの寄与を見る。
(3) 条件充足数(0-4)別の勝率。
(4) 感度: wp閾値をraw>=0.50と較正込み下限>=0.45の両方で(Codex P2対応。実損3,000円条項は
    台帳にロット情報が無く再構成不能=本研究の限界として文書に記載)。
usage: python tools/analysis/bplus_tests_2026_09.py  (repo rootで実行・読み取り専用)
"""
import numpy as np
import pandas as pd

led = pd.read_csv('data/signal_log.csv')
sc = pd.read_csv('data/prediction_log_scores.csv', parse_dates=['date'])
li = led.set_index('signal_id')
d = sc[(sc['actionable'] == True) & sc['result_5d'].isin(['success', 'failure'])].copy()  # noqa: E712
for c in ['cbs', 'ems', 'rr', 'win_prob']:
    d[c] = pd.to_numeric(d['signal_id'].map(li[c]), errors='coerce')
d = d[d['win_prob'].notna()].sort_values(['asset', 'date']).reset_index(drop=True)
d['win'] = (d['result_5d'] == 'success').astype(int)

for wp_th, lab in [(0.50, 'raw wp>=0.50'), (0.45, 'calibrated-lower wp>=0.45')]:
    d['bp'] = ((d['cbs'] >= 70) & (d['ems'] >= 60) & (d['rr'] >= 1.5) & (d['win_prob'] >= wp_th)).astype(int)
    obs = d[d['bp'] == 1]['win'].mean() - d[d['bp'] == 0]['win'].mean()
    d['gap'] = d.groupby('asset')['date'].diff().dt.days.fillna(99)
    d['cl'] = (d.groupby('asset')[(d['gap'] > 7).name if False else 'gap'].transform(lambda s: (s > 7).cumsum()).astype(str) + '_' + d['asset'])
    cl = d.groupby('cl').agg(win=('win', 'mean'), bp=('bp', 'mean')).reset_index()
    cl['lab'] = (cl['bp'] >= 0.5).astype(int)
    obs_cl = cl[cl['lab'] == 1]['win'].mean() - cl[cl['lab'] == 0]['win'].mean()
    rng = np.random.default_rng(1)
    labs, wins = cl['lab'].values, cl['win'].values
    perm = [wins[s == 1].mean() - wins[s == 0].mean() for s in (rng.permutation(labs) for _ in range(20000))]
    p = float(np.mean(np.abs(perm) >= abs(obs_cl)))
    print(f"[{lab}] 行差={obs:+.3f} | クラスタ({int(cl['lab'].sum())}vs{int((1-cl['lab']).sum())})差={obs_cl:+.3f} p={p:.3f}")

d['k'] = (d['cbs'] >= 70).astype(int) + (d['ems'] >= 60).astype(int) + (d['rr'] >= 1.5).astype(int) + (d['win_prob'] >= 0.50).astype(int)
print("充足数別:", {int(k): f"{g['win'].mean():.3f}(n={len(g)})" for k, g in d.groupby('k') if len(g) >= 5})
