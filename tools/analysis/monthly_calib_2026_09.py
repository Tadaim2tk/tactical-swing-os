# 9/1月次較正の実測パート: 台帳×遡及コーパスの as-of 結合と層別分析
# 規約: 判断日Dには「D-1までで確定した」コーパス行を当てる(merge_asof backward, allow_exact=False)
import json
import numpy as np
import pandas as pd

led = pd.read_csv('data/signal_log.csv', parse_dates=['date'])
sc = pd.read_csv('data/prediction_log_scores.csv', parse_dates=['date'])
sim = pd.read_csv('data/execution_simulation.csv', parse_dates=['date'])
mk = pd.read_csv('data/retro/market_daily.csv', parse_dates=['date'])

ctx = mk[['date', 'leader_asset', 'leader_margin', 'risk_state', 'vol_state']].sort_values('date')
def asof_join(df):
    out = pd.merge_asof(df.sort_values('date'), ctx, on='date',
                        direction='backward', allow_exact_matches=False)
    return out

sc2 = asof_join(sc)
sim2 = asof_join(sim)

R = {}

# 1) 較正(修正済み物差し): 申告wp vs 実現(5d close), 期間(a)(b)(c)
act = sc2[(sc2['actionable'] == True) & sc2['result_5d'].isin(['success', 'failure'])].copy()  # noqa: E712
wp = pd.to_numeric(led.set_index('signal_id')['win_prob'], errors='coerce')
act['wp'] = act['signal_id'].map(wp)
act = act[act['wp'].notna()]
def calib(sub):
    n = len(sub)
    if n == 0: return {'n': 0}
    real = (sub['result_5d'] == 'success').mean()
    return {'n': int(n), 'wp_mean': round(float(sub['wp'].mean()), 3),
            'realized': round(float(real), 3), 'err': round(float(real - sub['wp'].mean()), 3)}
b_a = act[act['date'] <= '2026-07-15']
b_b = act[(act['date'] >= '2026-07-16') & (act['date'] <= '2026-07-26')]
b_c = act[act['date'] >= '2026-07-27']
R['calibration'] = {'all': calib(act), 'a_to_0715': calib(b_a), 'b_0716_26': calib(b_b), 'c_0727_': calib(b_c)}

# 2) レジーム分割(初実行): (c)期間を risk_state / leader で割る
R['c_by_risk_state'] = {k: calib(g) for k, g in b_c.groupby('risk_state') if len(g) >= 3}
R['c_by_leader'] = {k: calib(g) for k, g in b_c.groupby('leader_asset') if len(g) >= 3}
R['all_by_leader'] = {k: calib(g) for k, g in act.groupby('leader_asset') if len(g) >= 5}

# 3) 主役レンズの本題: 「主役と同じ資産への判断」vs「脇役への判断」
act['is_leader_trade'] = act['asset'] == act['leader_asset']
R['leader_vs_other'] = {'leader_asset_trades': calib(act[act['is_leader_trade']]),
                        'other_asset_trades': calib(act[~act['is_leader_trade']])}
# Rでも
r5 = pd.to_numeric(act['r_close_5d'], errors='coerce')
R['leader_vs_other_r'] = {
    'leader_mean_r5': round(float(r5[act['is_leader_trade']].mean()), 3) if act['is_leader_trade'].any() else None,
    'other_mean_r5': round(float(r5[~act['is_leader_trade']].mean()), 3)}

# 4) B+観察枠の再照合(修正済みスコアで)
led_i = led.set_index('signal_id')
def num(col, sid): return pd.to_numeric(led_i[col].get(sid), errors='coerce')
act['cbs'] = act['signal_id'].map(lambda s: num('cbs', s))
act['ems'] = act['signal_id'].map(lambda s: num('ems', s))
act['rr'] = act['signal_id'].map(lambda s: num('rr', s))
bp = act[(act['cbs'] >= 70) & (act['ems'] >= 60) & (act['rr'] >= 1.5) & (act['wp'] >= 0.50)]
nbp = act[~act.index.isin(bp.index)]
R['bplus_frame'] = {'match': {'n': len(bp), 'mean_r5': round(float(pd.to_numeric(bp['r_close_5d'], errors='coerce').mean()), 3) if len(bp) else None,
                              'win': round(float((bp['result_5d'] == 'success').mean()), 3) if len(bp) else None},
                    'others': {'n': len(nbp), 'mean_r5': round(float(pd.to_numeric(nbp['r_close_5d'], errors='coerce').mean()), 3),
                               'win': round(float((nbp['result_5d'] == 'success').mean()), 3)}}

# 5) ジオメトリ再判定(事前登録テスト): 7/18以降の決着 vs 介入前プラセボ窓
sim_dec = sim2[sim2['r_result'].notna()].sort_values('date')
pre = sim_dec[sim_dec['date'] < '2026-07-18']['r_result'].values
post = sim_dec[sim_dec['date'] >= '2026-07-18']['r_result'].values
R['geometry'] = {'pre_n': len(pre), 'pre_mean': round(float(np.mean(pre)), 3) if len(pre) else None,
                 'post_n': len(post), 'post_mean': round(float(np.mean(post)), 3) if len(post) else None,
                 'post_gross': round(float(np.sum(post)), 3) if len(post) else None}
if len(pre) >= 15 and len(post) >= 15:
    rng = np.random.default_rng(20260901)
    allr = np.concatenate([pre, post]); nb = len(post); obs = np.mean(post) - np.mean(pre)
    perm = [np.mean(s[:nb]) - np.mean(s[nb:]) for s in (rng.permutation(allr) for _ in range(5000))]
    R['geometry']['perm_p_onesided'] = round(float(np.mean([p >= obs for p in perm])), 3)
    # プラセボ窓: 介入前からpost_nサイズの連続窓
    if len(pre) > nb:
        placebo = [np.sum(pre[i:i+nb]) for i in range(len(pre) - nb + 1)]
        R['geometry']['placebo_windows_ge_post_gross'] = round(float(np.mean([p >= np.sum(post) for p in placebo])), 3)

# 6) 月別基準値(期間効果の物差し)
sim_dec['ym'] = sim_dec['date'].dt.to_period('M').astype(str)
R['monthly_mean_r'] = {k: {'n': int(len(g)), 'mean': round(float(g['r_result'].mean()), 3), 'gross': round(float(g['r_result'].sum()), 2)}
                       for k, g in sim_dec.groupby('ym')}

# 7) 3,000円ルール(8/28適用)の前後: nの正直な確認
post3k = led[led['date'] >= '2026-08-28']
R['rule_3000yen'] = {'days': int(post3k['date'].nunique()), 'rows': len(post3k),
                     'note': 'n極小につき判定不能(次回月次で)'}

print(json.dumps(R, ensure_ascii=False, indent=1))
EOF_MARKER = True
