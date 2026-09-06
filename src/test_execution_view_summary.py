"""監査F7/F8 (2026-09-06) の再現テスト。

F7: 最大DDが同日内の銘柄名の文字順で変わっていた（+10R/-4R/-4R を並べ替えると 8R→4R）。
F8: 「営業日窓」の日軸が絞り込み後の日付だったため、全件見送りの日が消えていた。
"""
import pandas as pd
import pytest

import dashboard_summaries as ds


def _scores(rows):
    return pd.DataFrame([{
        "date": r["date"], "signal_id": r["sid"], "asset": r["asset"],
        "rank": r.get("rank", "B"), "actionable": r.get("actionable", "true"),
        "data_quality": "ok", "entry_touched_5d": r.get("touched", "true"),
        "r_close_5d": r.get("r5", 0.0),
    } for r in rows])


def _ledger(rows, rp=0.25):
    return pd.DataFrame([{"signal_id": r["sid"], "risk_pct": rp} for r in rows])


# --- F7 -----------------------------------------------------------------

def _same_day_rows(assets):
    """同日に +10R / -4R / -4R。合計 +2R は固定で、資産ラベルだけ入れ替える。"""
    rs = [10.0, -4.0, -4.0]
    return [{"date": "2026-07-01", "sid": f"s{i}", "asset": a, "r5": r}
            for i, (a, r) in enumerate(zip(assets, rs))]


@pytest.mark.parametrize("assets", [
    ["AAA", "BBB", "CCC"],   # +10 が先頭 → 旧実装の最大DD 8R
    ["ZZZ", "AAA", "BBB"],   # +10 が最後 → 旧実装の最大DD 4R
    ["MMM", "ZZZ", "AAA"],
])
def test_max_dd_is_independent_of_asset_name_order(assets):
    rows = _same_day_rows(assets)
    out = ds.execution_view_summary(_scores(rows), _ledger(rows))
    assert out["cum_r"] == 2.0
    assert out["max_dd_r"] == 0.0, "同日内の並べ替えで最大DDが動いてはいけない"
    assert out["max_dd_basis"] == "daily_net_r"


def test_max_dd_still_measures_real_day_over_day_drawdown():
    rows = [{"date": "2026-07-01", "sid": "a", "asset": "AAA", "r5": 5.0},
            {"date": "2026-07-02", "sid": "b", "asset": "BBB", "r5": -3.0},
            {"date": "2026-07-03", "sid": "c", "asset": "CCC", "r5": -1.0}]
    out = ds.execution_view_summary(_scores(rows), _ledger(rows))
    assert out["cum_r"] == 1.0
    assert out["max_dd_r"] == 4.0, "日をまたぐ本物のDDは測れていること"


# --- F8 -----------------------------------------------------------------

def test_window_axis_includes_no_trade_days():
    """全件見送りの日（actionable=false）も窓の日軸に入る。"""
    fills = [{"date": f"2026-07-0{d}", "sid": f"f{d}", "asset": "GOLD", "r5": 1.0} for d in (1, 2, 3)]
    no_trade = [{"date": f"2026-07-0{d}", "sid": f"n{d}", "asset": "GOLD",
                 "rank": "NO_TRADE", "actionable": "false", "r5": 0.0} for d in (4, 5, 6, 7)]
    out = ds.execution_view_summary(_scores(fills + no_trade), _ledger(fills + no_trade))
    assert out["ledger_days"] == 7, "見送り日が日軸から消えてはいけない"
    assert out["fill_days"] == 3
    assert out["window_basis"] == "ledger_days"
    w5 = next(w for w in out["windows"] if w["w"] == 5)
    assert w5["n_windows"] == 3, "7日 - 5 + 1 = 3窓（絞り込み後の3日なら窓は作れない）"


def test_window_counts_shrink_when_only_fill_days_are_used():
    """旧挙動との差を明示的に固定する（絞り込み後の日付だと窓が減る）。"""
    fills = [{"date": f"2026-07-{d:02d}", "sid": f"f{d}", "asset": "GOLD", "r5": 1.0} for d in range(1, 6)]
    no_trade = [{"date": f"2026-07-{d:02d}", "sid": f"n{d}", "asset": "GOLD",
                 "rank": "NO_TRADE", "actionable": "false", "r5": 0.0} for d in range(6, 13)]
    out = ds.execution_view_summary(_scores(fills + no_trade), _ledger(fills + no_trade))
    assert out["ledger_days"] == 12
    w10 = next(w for w in out["windows"] if w["w"] == 10)
    assert w10["n_windows"] == 3, "全記帳日12日なら10日窓は3本（約定日5日だけなら0本）"
    # 見送り日(0R)が入るぶん、窓の合計は後ろへ行くほど小さくなる
    assert w10["best"] == 5.0 and w10["worst"] == 3.0
