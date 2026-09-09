"""SL/TP執行シミュレーション(保守的)の単体テスト。

固定する原則:
1. 曖昧さは常に不利側 — worst-in-zone約定 / 約定足のSL成立 / TP1は翌足以降 / SL優先
2. 判定不能は捏造しない — バー不足は open、未到達は no_fill
3. 採点系と同じ±10%水準ガードで系列取り違えを隔離
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import simulate_execution as se


def _ohlcv(bars):
    """bars: list of (date, open, high, low, close)"""
    df = pd.DataFrame(bars, columns=["date", "open", "high", "low", "close"])
    df["date"] = pd.to_datetime(df["date"])
    return df


def _row(**over):
    base = dict(date="2026-07-01", signal_id="X", asset="WTI", side="BUY", rank="B",
                risk_pct="0.25", entry_low="72.0", entry_high="73.0", sl="70.0", tp1="76.0")
    base.update(over)
    return pd.Series(base)


def test_long_fill_then_tp1_next_bar():
    bars = _ohlcv([
        ("2026-07-01", 74, 74.5, 72.5, 74.0),   # 約定(low<=73) SLなし TP同足でも翌足まで持ち越し
        ("2026-07-02", 74, 76.5, 73.5, 76.0),   # TP1 76 到達
    ])
    r = se.simulate_row(_row(), bars, "t")
    assert r["status"] == "filled_tp1"
    assert r["fill_price"] == 73.0            # worst-in-zone (BUY=entry_high)
    assert abs(r["r_result"] - 1.0) < 1e-9    # (76-73)/(73-70)=1.0R


def test_same_bar_sl_is_conservative_loss():
    bars = _ohlcv([("2026-07-01", 74, 74.5, 69.5, 74.0)])  # 約定もSL(70)も同足 → 不利側
    r = se.simulate_row(_row(), bars, "t")
    assert r["status"] == "filled_sl"
    assert r["r_result"] == -1.0


def test_sl_priority_when_same_later_bar():
    bars = _ohlcv([
        ("2026-07-01", 74, 74.5, 72.9, 74.0),            # 約定のみ
        ("2026-07-02", 74, 77.0, 69.5, 75.0),            # SLもTP1も同足 → SL優先
    ])
    r = se.simulate_row(_row(), bars, "t")
    assert r["status"] == "filled_sl" and r["r_result"] == -1.0


def test_tp1_not_credited_on_fill_bar_then_time_exit():
    bars = _ohlcv([
        ("2026-07-01", 74, 76.5, 72.9, 74.0),  # 約定足でTP1タッチ → 持ち越し(不利側)
        ("2026-07-02", 74, 75.0, 73.5, 74.5),
        ("2026-07-03", 74, 75.0, 73.5, 74.5),
        ("2026-07-06", 74, 75.0, 73.5, 74.5),
        ("2026-07-07", 74, 75.0, 73.5, 74.5),
        ("2026-07-08", 74, 75.0, 73.5, 74.2),  # 期限バー(判断日+5) 終値決済
    ])
    r = se.simulate_row(_row(), bars, "t")
    assert r["status"] == "filled_time_exit"
    assert abs(r["r_result"] - (74.2 - 73.0) / 3.0) < 1e-3


def test_no_fill_and_open():
    far = [("2026-07-0%d" % d, 80, 81, 78, 80) for d in range(1, 6)]
    r = se.simulate_row(_row(), _ohlcv(far), "t")
    assert r["status"] == "no_fill"
    r2 = se.simulate_row(_row(), _ohlcv(far[:2]), "t")   # 約定待ち窓が未完
    assert r2["status"] == "open"


def test_short_direction_mirrors():
    row = _row(side="SELL", entry_low="76.0", entry_high="77.0", sl="79.0", tp1="72.0")
    bars = _ohlcv([
        ("2026-07-01", 75, 76.5, 74.5, 75.0),  # SELL約定(worst=entry_low=76) SL(79)未達
        ("2026-07-02", 75, 75.5, 71.5, 72.5),  # TP1 72 到達
    ])
    r = se.simulate_row(row, bars, "t")
    assert r["status"] == "filled_tp1"
    assert r["fill_price"] == 76.0
    assert abs(r["r_result"] - (76 - 72) / 3.0) < 1e-3  # r_resultは4桁丸め


def test_scale_mismatch_excluded():
    # 監査F3以降、水準検査は「判断時に既知の終値」で行う。判断前のバーが要る。
    bars = _ohlcv([("2026-06-30", 74, 75, 73, 74), ("2026-07-01", 74, 75, 73, 74)])
    r = se.simulate_row(_row(entry_low="720", entry_high="730", sl="700", tp1="760"), bars, "t")
    assert r["status"] == "excluded_scale"
    assert r["scale_check"] == "excluded"


def test_scale_check_not_checked_does_not_exclude():
    """判断前のバーが無く検査できないとき、検査不能を除外に変えない(母集団を静かに縮めない)。"""
    r = se.simulate_row(_row(entry_low="720", entry_high="730", sl="700", tp1="760"),
                        _ohlcv([("2026-07-01", 74, 75, 73, 74)]), "t")
    assert r["scale_check"] == "not_checked"
    assert r["status"] != "excluded_scale"


def test_signal_before_price_window_gets_typed_status_not_fake_fill():
    # 2026-08-31監査P1-4a: rawは直近240日で上書きされるため、信号日が窓外に落ちた行を
    # 窓先頭のバーへ静かにアンカーすると「6月の判断が8月のバーで約定」する(符号反転の
    # 実例を確認済み)。typed status で正直に返し、偽の約定を作らない。
    bars = _ohlcv([("2026-08-0%d" % d, 74, 76.5, 72.5, 74.0) for d in range(3, 8)])
    r = se.simulate_row(_row(date="2026-07-01"), bars, "t")  # 窓は8/3開始、信号は7/1
    assert r["status"] == "data_window_expired"
    assert r["fill_date"] == "" and pd.isna(r["r_result"])


def test_ledger_filter_only_priced_orders(tmp_path):
    led = pd.DataFrame([
        _row().to_dict(),
        _row(signal_id="W", risk_pct="0.00").to_dict(),          # 監視のみ → 対象外
        _row(signal_id="N", side="NONE", rank="NO_TRADE").to_dict(),
        _row(signal_id="A0", rank="C").to_dict(),                 # 未知rank → 対象外
    ])
    raw = tmp_path
    _ohlcv([("2026-07-01", 74, 74.5, 72.5, 74.0), ("2026-07-02", 74, 76.5, 73.5, 76.0)]).assign(
        date=lambda d: d["date"].dt.strftime("%Y-%m-%d")
    ).to_csv(raw / "WTI.csv", index=False)
    sim = se.simulate_ledger(led, raw_dir=raw)
    assert len(sim) == 1 and sim.iloc[0]["signal_id"] == "X"


def test_summarize_counts_and_cost_sensitivity():
    sim = pd.DataFrame([
        {"status": "filled_tp1", "r_result": 1.0, "capital_pct": 0.25, "rank": "B"},
        {"status": "filled_sl", "r_result": -1.0, "capital_pct": -0.25, "rank": "B"},
        {"status": "no_fill", "r_result": float("nan"), "capital_pct": float("nan"), "rank": "B"},
    ], columns=se.COLUMNS[:0].tolist() + ["status", "r_result", "capital_pct", "rank"]) if False else pd.DataFrame([
        {"status": "filled_tp1", "r_result": 1.0, "capital_pct": 0.25},
        {"status": "filled_sl", "r_result": -1.0, "capital_pct": -0.25},
        {"status": "no_fill", "r_result": float("nan"), "capital_pct": float("nan")},
    ])
    s = se.summarize(sim)
    assert s["fills_resolved"] == 2 and s["no_fill"] == 1
    assert s["gross_total_r"] == 0.0
    assert abs(s["cost_sensitivity_r"]["0.05R"] - (0.0 - 0.1)) < 1e-9


# === 監査F3 (2026-09-06): 判断後の終値で標本を選ばない =========================

def test_decision_day_close_does_not_change_inclusion():
    """監査の中心的所見の再現。

    同じ事前情報(前日終値100・entry 99-101・SL 95)、同じ当日レンジ(high 101 / low 79)で、
    **当日の終値だけ**を 80 と 100 に変えても、母集団に含むかどうかが変わってはいけない。
    旧実装は当日終値80なら excluded_scale(損益なし)、100なら filled_sl(-1R)だった。
    """
    row = _row(entry_low="99", entry_high="101", sl="95", tp1="110")
    results = {}
    for close in (80.0, 100.0):
        bars = _ohlcv([("2026-06-30", 100, 100, 100, 100),
                       ("2026-07-01", 100, 101, 79, close),
                       ("2026-07-02", 100, 101, 99, 100)])
        results[close] = se.simulate_row(row, bars, "t")
    assert results[80.0]["status"] == results[100.0]["status"], \
        "判断後に確定する終値で母集団が変わってはいけない"
    assert results[80.0]["scale_check"] == results[100.0]["scale_check"] == "passed"
    assert results[80.0]["status"] == "filled_sl"


def test_reference_deviation_is_recorded_even_when_passing():
    bars = _ohlcv([("2026-06-30", 100, 100, 100, 100), ("2026-07-01", 100, 101, 99, 100)])
    r = se.simulate_row(_row(entry_low="99", entry_high="101", sl="95", tp1="110"), bars, "t")
    assert r["scale_check"] == "passed"
    assert r["reference_deviation"] == 0.0, "隔離の可否を後から検算できるよう常に残す"


def test_execution_anchor_matches_scoring_anchor_rule():
    """採点側と執行側で同じ規約を使う(写しを持って片方だけ直る事故を防ぐ)。"""
    import pandas as pd
    from score_prediction_log import decision_time_anchor
    weekday_only = pd.DataFrame({"date": pd.to_datetime(
        ["2026-06-29", "2026-06-30", "2026-07-01", "2026-07-02", "2026-07-03"])})  # 月-金
    k, a = decision_time_anchor(weekday_only, "2026-07-01")
    assert (k, a) == (2, 1), "週5日資産は k-1"
    seven_day = pd.DataFrame({"date": pd.date_range("2026-06-29", periods=7, freq="D")})  # 週末を含む
    k, a = decision_time_anchor(seven_day, "2026-07-01")
    assert (k, a) == (2, 0), "週7日資産は k-2"


# === 監査F5 (2026-09-06): 「5日」が2つある件の名前分け ========================

def test_time_exit_records_its_bar_offset():
    """時間決済したバーの位置を列に残す。「5日」という名前だけでは量が特定できない。"""
    bars = _ohlcv([("2026-06-30", 100, 100, 100, 100)]
                  + [("2026-07-%02d" % d, 100, 101, 99, 100 + d) for d in range(1, 9)])
    r = se.simulate_row(_row(entry_low="99", entry_high="101", sl="80", tp1="999"), bars, "t")
    assert r["status"] == "filled_time_exit"
    assert r["exit_bar_offset"] == se.EXIT_DEADLINE_BARS


def test_time_exit_is_one_bar_later_than_scoring_horizon():
    """執行の時間決済(6本目)と採点の r_close_5d(5本目)が別の量であることを固定する。

    2026-09-07 の人間の言明で、どちらも実際の手仕舞いではないことが確定した
    （実際は日数固定ではなくシナリオ崩壊で降りる）。現実に合わせる問題ではなく、
    同じ「5日」で呼ばないという名前の問題である。
    """
    from score_prediction_log import HORIZONS
    assert 5 in HORIZONS
    scoring_offset_from_k = 5 - 1          # j = k - 1 + h  → k+4 が5本目
    execution_offset_from_idx0 = se.EXIT_DEADLINE_BARS   # idx0 + 5 が6本目
    assert execution_offset_from_idx0 == scoring_offset_from_k + 1, \
        "1バー差であることが前提。変えるなら両方の名前と文書を同時に直すこと"


def test_no_fill_records_what_the_direction_would_have_earned():
    """Entry帯へ戻らなかった判断が、方向として何Rぶん動いたかを残す。

    2026-09-09 の観測: 約定した110件が -6.53R、約定しなかった32件が +24.53R。
    Entry規則が「当たった判断ほど落とす」側に働いている可能性があり、
    それを執行側の表だけで検算できるようにするための列。
    """
    # BUY entry 72-73、価格は一度も73へ戻らず上昇し続ける
    bars = _ohlcv([(f"2026-07-0{i}", 74 + i, 75 + i, 73.5 + i, 74.5 + i) for i in range(1, 7)])
    r = se.simulate_row(_row(), bars, "t")
    assert r["status"] == "no_fill"
    # 建値は約定した場合と同じ worst-in-zone (73.0)、risk = 73-70 = 3.0
    # 5本目(FILL_WINDOW_BARS=5)の終値 = 74.5+5 = 79.5 → (79.5-73)/3 = 2.1667
    assert abs(r["forgone_r"] - 2.1667) < 1e-3
    assert pd.isna(r["r_result"]), "参加していないので執行Rは名乗らない"


def test_short_no_fill_forgone_uses_short_direction():
    """SELL は下落が利益。方向を取り違えると逆選択の符号が反転する。"""
    bars = _ohlcv([(f"2026-07-0{i}", 70 - i, 70.5 - i, 69 - i, 69.5 - i) for i in range(1, 7)])
    r = se.simulate_row(_row(side="SELL", entry_low="72.0", entry_high="73.0",
                             sl="75.0", tp1="66.0"), bars, "t")
    assert r["status"] == "no_fill"
    # SELL の worst-in-zone は entry_low=72.0、risk = 75-72 = 3.0
    # 5本目の終値 = 69.5-5 = 64.5 → (72-64.5)/3 = 2.5
    assert abs(r["forgone_r"] - 2.5) < 1e-3


def test_open_window_does_not_claim_forgone_r():
    """窓が閉じていないうちは逃した分を名乗らない(判定不能は捏造しない)。"""
    bars = _ohlcv([("2026-07-01", 75, 76, 74, 75.5), ("2026-07-02", 76, 77, 75, 76.5)])
    r = se.simulate_row(_row(), bars, "t")
    assert r["status"] == "open"
    assert pd.isna(r["forgone_r"])


def test_summary_reports_forgone_separately_from_realized():
    """逃した分を実現Rに混ぜない。混ぜると建ててもいない玉の損益が成績になる。"""
    sim = pd.DataFrame([
        {"status": "filled_tp1", "r_result": 1.0, "capital_pct": 0.25, "forgone_r": float("nan")},
        {"status": "no_fill", "r_result": float("nan"), "capital_pct": float("nan"), "forgone_r": 2.0},
        {"status": "no_fill", "r_result": float("nan"), "capital_pct": float("nan"), "forgone_r": 1.0},
    ])
    out = se.summarize(sim)
    assert out["gross_total_r"] == 1.0, "実現Rには no_fill を入れない"
    assert out["no_fill_forgone_r"] == 3.0
    assert out["no_fill_forgone_avg_r"] == 1.5


def test_forming_last_bar_does_not_claim_forgone_r(monkeypatch):
    """5本目が当日ラベルのままなら逃した分を名乗らない(#165 Codex P2)。

    window_complete は行数だけで決まるので、24時間動く資産では当日の
    未確定バーが5本目に数えられ、日中値が終値扱いで入る。#137 と同型。
    """
    bars = _ohlcv([(f"2026-07-0{i}", 74 + i, 75 + i, 73.5 + i, 74.5 + i) for i in range(1, 6)])
    monkeypatch.setattr(se, "_current_utc_date", lambda: pd.Timestamp("2026-07-05"))
    r = se.simulate_row(_row(), bars, "t")
    assert r["status"] == "no_fill"
    assert pd.isna(r["forgone_r"]), "5本目(7/5)が当日なので確定値を名乗らない"
    monkeypatch.setattr(se, "_current_utc_date", lambda: pd.Timestamp("2026-07-06"))
    r2 = se.simulate_row(_row(), bars, "t")
    assert not pd.isna(r2["forgone_r"]), "閉じたら記録する"


# --- 押し目を待たずに追る規則の併走観測(人間の承認 2026-09-09) ---

def test_chase_enters_at_the_close_when_the_band_never_comes():
    """帯へ来なければ判断日ラベルの終値で入る。建値はその終値。"""
    bars = _ohlcv([("2026-07-01", 74, 75, 73.5, 74.5),    # 帯72-73へ来ない
                   ("2026-07-02", 75, 77, 74.5, 76.5),
                   ("2026-07-03", 77, 78, 76, 77.5)])
    st, r = se.chase_row(_row(), bars, wait_bars=1)
    # 建値74.5 / SL70 -> risk=4.5、TP1=76.0 は7/2の高値77で到達 -> (76-74.5)/4.5
    assert st == "chase_tp1"
    assert abs(r - 0.3333) < 1e-3


def test_chase_does_not_judge_sl_on_the_bar_it_entered_at_the_close():
    """終値で入った足の安値は既に過ぎている。そこで損切りにすると過去を覗く。

    帯72-73へは届かず(高値71.5)、しかし安値64がSL65を割った足。
    その足の終値71.0で入るので、64を付けたのは建てる前の出来事である。
    """
    row = _row(sl="65.0", tp1="90.0")   # TP1は窓内で当たらない位置に置く
    bars = _ohlcv([("2026-07-01", 71.0, 71.5, 64.0, 71.0),
                   ("2026-07-02", 71, 72.5, 70.0, 72.0),
                   ("2026-07-03", 72, 73.5, 71.0, 73.0),
                   ("2026-07-04", 73, 74.5, 72.0, 74.0),
                   ("2026-07-05", 74, 75.5, 73.0, 75.0),
                   ("2026-07-06", 75, 76.5, 74.0, 76.0)])
    st, r = se.chase_row(row, bars, wait_bars=1)
    assert st == "chase_time_exit", "入った足のSLで即死させない"
    assert abs(r - (76.0 - 71.0) / (71.0 - 65.0)) < 1e-3


def test_chase_refuses_when_price_already_passed_the_target():
    """目標を過ぎてから追わない。伸びしろが無い建値を掴むだけ。"""
    bars = _ohlcv([("2026-07-01", 76, 78, 75.5, 77.0)])   # TP1=76 を既に超えた終値
    st, r = se.chase_row(_row(), bars, wait_bars=1)
    assert st == "beyond_tp1"
    assert pd.isna(r)


def test_chase_refuses_when_price_already_broke_the_stop():
    """損切り水準の向こうでは追わない。"""
    bars = _ohlcv([("2026-07-01", 71, 71.5, 68, 69.0)])   # SL=70 の下で引けた
    st, r = se.chase_row(_row(), bars, wait_bars=1)
    assert st == "beyond_sl"
    assert pd.isna(r)


def test_chase_uses_the_band_price_when_the_band_did_come():
    """帯へ来た日は追わない。従来どおりゾーン内の最悪価格で建てる。"""
    bars = _ohlcv([("2026-07-01", 74, 74.5, 72.5, 74.0),
                   ("2026-07-02", 74, 76.5, 73.5, 76.0)])
    st, r = se.chase_row(_row(), bars, wait_bars=1)
    assert st == "band_tp1"
    assert abs(r - 1.0) < 1e-9, "worst-in-zone 73.0 建て -> (76-73)/3"


def test_chase_does_not_build_a_price_from_a_forming_bar(monkeypatch):
    """当日ラベルの未確定バーの終値で建値を作らない(#137/#165 と同型)。"""
    bars = _ohlcv([("2026-07-01", 74, 75, 73.5, 74.5)])
    monkeypatch.setattr(se, "_current_utc_date", lambda: pd.Timestamp("2026-07-01"))
    st, r = se.chase_row(_row(), bars, wait_bars=1)
    assert st == "open" and pd.isna(r)


def test_chase_summary_is_separate_from_realized_r():
    """追った場合を実現Rに混ぜない。既定の執行規約は押し目待ちのまま。"""
    sim = pd.DataFrame([
        {"asset": "NASDAQ", "status": "no_fill", "r_result": float("nan"),
         "capital_pct": float("nan"), "forgone_r": 2.0, "chase_status": "chase_tp1", "chase_r": 1.0},
        {"asset": "NASDAQ", "status": "filled_sl", "r_result": -1.0,
         "capital_pct": -0.25, "forgone_r": float("nan"), "chase_status": "band_sl", "chase_r": -1.0},
    ])
    out = se.summarize(sim)
    assert out["gross_total_r"] == -1.0, "実現Rに chase を入れない"
    assert out["chase"]["total_r"] == 0.0
    assert out["chase"]["chased"] == 1
    assert out["chase"]["baseline_total_r"] == -1.0


# --- TP1で半分降りて残りを時間決済まで持つ規則(人間の承認 2026-09-09) ---

def _six(rest):
    """判断日から決済期限まで6本。rest は1本目以降の (h, l, c)。"""
    bars = [("2026-07-01", 74, 74.5, 72.5, 74.0)]        # 帯72-73に触れて約定・SLなし
    for i, (h, l, c) in enumerate(rest, start=2):
        bars.append((f"2026-07-0{i}", c, h, l, c))
    return _ohlcv(bars)


def test_half_exit_books_tp1_and_rides_the_rest_to_the_deadline():
    """TP1で半分、残りは6本目の終値。建値73/risk3/TP1=76 -> 0.5*1.0 + 0.5*(79-73)/3。"""
    bars = _six([(76.5, 74.0, 76.2), (77, 75, 76.8), (78, 76, 77.5),
                 (78.5, 76.5, 78.0), (79.5, 77, 79.0)])
    st, r, r_be = se.half_exit_row(_row(), bars)
    assert st == "half_tp1_then_time"
    assert abs(r - (0.5 * 1.0 + 0.5 * 2.0)) < 1e-3
    assert abs(r_be - r) < 1e-9, "一度も建値へ戻っていないので同じ"


def test_half_exit_gives_back_the_rest_when_price_reverses():
    """TP1後に反転したら残りは返上する。**これがTP1全決済より悪くなる日**。

    元のSLのままなら残り -1.0R、建値へ上げていれば 0R。両方測って比べられるようにする。
    """
    bars = _six([(76.5, 74.0, 76.2),     # TP1到達
                 (76.5, 73.5, 74.0),     # 建値73は割らない
                 (74.0, 69.0, 70.5),     # SL70も建値73も割る
                 (72, 70.5, 71), (72, 70.5, 71)])
    st, r, r_be = se.half_exit_row(_row(), bars)
    assert st == "half_tp1_then_stopped"
    assert abs(r - (0.5 * 1.0 + 0.5 * -1.0)) < 1e-3, "元のSLなら残りは-1R"
    assert abs(r_be - (0.5 * 1.0 + 0.5 * 0.0)) < 1e-3, "建値なら残りは0R"
    assert r_be > r


def test_half_exit_is_identical_when_the_stop_comes_first():
    """SLが先なら分ける対象が無い。r_result と同じ値でなければ比較が壊れる。"""
    bars = _six([(74, 69.0, 70.0), (72, 70, 71), (72, 70, 71), (72, 70, 71), (72, 70, 71)])
    st, r, r_be = se.half_exit_row(_row(), bars)
    assert st == "half_sl_before_tp1"
    assert r == r_be == -1.0
    assert abs(se.simulate_row(_row(), bars, "t")["r_result"] - r) < 1e-9


def test_half_exit_is_identical_when_tp1_is_never_reached():
    """TP1に届かなければ全部を時間決済。分けても同じ。"""
    bars = _six([(75, 73.5, 74.5), (75, 73.5, 74.5), (75, 73.5, 74.5),
                 (75, 73.5, 74.5), (75, 73.5, 74.8)])
    st, r, r_be = se.half_exit_row(_row(), bars)
    assert st == "half_no_tp1_time_exit"
    assert r == r_be
    assert abs(se.simulate_row(_row(), bars, "t")["r_result"] - r) < 1e-9


def test_half_exit_needs_a_fill_first():
    """建っていない判断は分ける対象ではない。空欄で返す。"""
    bars = _ohlcv([(f"2026-07-0{i}", 76, 78, 75, 77) for i in range(1, 7)])
    st, r, r_be = se.half_exit_row(_row(), bars)
    assert st == "" and pd.isna(r) and pd.isna(r_be)


def test_half_exit_does_not_close_on_a_forming_bar(monkeypatch):
    """期限バーが形成途中なら確定値を名乗らない(#137/#165/#166 と同型)。"""
    bars = _six([(76.5, 74.0, 76.2), (77, 75, 76.8), (78, 76, 77.5),
                 (78.5, 76.5, 78.0), (79.5, 77, 79.0)])
    monkeypatch.setattr(se, "_current_utc_date", lambda: pd.Timestamp("2026-07-06"))
    st, r, r_be = se.half_exit_row(_row(), bars)
    assert st == "open" and pd.isna(r) and pd.isna(r_be)


def test_half_exit_summary_keeps_the_baseline_beside_it():
    """同じ母集団の実現Rを並べないと、差が読めない。"""
    sim = pd.DataFrame([
        {"asset": "WTI", "status": "filled_tp1", "r_result": 1.0, "capital_pct": 0.25,
         "forgone_r": float("nan"), "chase_status": "", "chase_r": float("nan"),
         "half_exit_status": "half_tp1_then_time", "half_exit_r": 1.5, "half_exit_be_r": 1.5},
        {"asset": "WTI", "status": "filled_sl", "r_result": -1.0, "capital_pct": -0.25,
         "forgone_r": float("nan"), "chase_status": "", "chase_r": float("nan"),
         "half_exit_status": "half_sl_before_tp1", "half_exit_r": -1.0, "half_exit_be_r": -1.0},
    ])
    out = se.summarize(sim)
    assert out["half_exit"]["total_r"] == 0.5
    assert out["half_exit"]["baseline_total_r"] == 0.0
    assert out["half_exit"]["tp1_split"] == 1
    assert out["gross_total_r"] == 0.0, "実現Rに half_exit を混ぜない"


def test_half_exit_breakeven_stop_is_judged_on_the_tp1_bar_itself():
    """TP1を踏んだ足が建値まで戻っていたら、建値版はその足で止まる(#168 Codex P2)。

    TP1が先か戻りが先かは分からない。同じ足の順序不明は不利側に倒す規約。
    元のSL版はその足でSL未到達が確認済みなので、翌足以降を見るのと同じ結果になる。
    """
    bars = _six([(76.5, 72.8, 75.0),     # TP1=76到達、かつ安値72.8で建値73を割る
                 (77, 75, 76.8), (78, 76, 77.5), (78.5, 76.5, 78.0), (79.5, 77, 79.0)])
    st, r, r_be = se.half_exit_row(_row(), bars)
    assert st == "half_tp1_then_time"
    assert abs(r - (0.5 * 1.0 + 0.5 * 2.0)) < 1e-3, "元のSLは割っていないので伸ばせる"
    assert abs(r_be - (0.5 * 1.0 + 0.5 * 0.0)) < 1e-3, "建値版はその足で止まったと扱う"


def test_half_exit_breakeven_cannot_record_a_loss_when_tp1_lands_on_the_deadline_bar():
    """TP1が期限足に当たり終値が建値割れでも、建値版は残りを負にしない(#168 Codex P2)。

    翌足から見る実装だと runner の走査が空になり、時間決済の終値で残りの損を
    記録していた。「返上しない」という建値版の定義に反する。
    """
    bars = _six([(75, 73.5, 74.5), (75, 73.5, 74.5), (75, 73.5, 74.5), (75, 73.5, 74.5),
                 (76.5, 72.0, 72.5)])  # 期限足でTP1到達、安値72で建値割れ、終値72.5
    st, r, r_be = se.half_exit_row(_row(), bars)
    assert st == "half_tp1_then_time"
    assert abs(r - (0.5 * 1.0 + 0.5 * (72.5 - 73.0) / 3.0)) < 1e-3, "元のSL版は終値で返上"
    assert abs(r_be - 0.5) < 1e-3, "建値版は建値で止まる。残りは0"
    assert r_be > r
