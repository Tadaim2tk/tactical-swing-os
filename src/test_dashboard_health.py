"""Data Health / Freshness (Phase 24) の単体テスト。

古い/空/欠損/unavailable なデータを正常と誤読しないことを検証する。
表示専用であり weights.json 等は変更しないことも確認する。
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import dashboard_summaries as ds

NOW = pd.Timestamp("2026-06-16 00:00:00")


# === parse_generated_at ===

def test_parse_utc_and_jst_and_dateonly():
    assert ds.parse_generated_at("2026-06-15 23:00:00 UTC") == pd.Timestamp("2026-06-15 23:00:00")
    # JST 08:00 == UTC 23:00 前日
    assert ds.parse_generated_at("2026-06-16 08:00:00 JST") == pd.Timestamp("2026-06-15 23:00:00")
    assert ds.parse_generated_at("2026-06-15") == pd.Timestamp("2026-06-15 00:00:00")


def test_parse_bad_values():
    assert ds.parse_generated_at(None) is None
    assert ds.parse_generated_at("") is None
    assert ds.parse_generated_at("not a date") is None
    assert ds.parse_generated_at(float("nan")) is None


# === assess_layer ステータス ===

def test_fresh_when_recent_with_rows():
    r = ds.assess_layer("x", "2026-06-15 20:00:00 UTC", 5, NOW, threshold_hours=36)
    assert r["status"] == "fresh"
    assert r["row_count"] == 5
    assert r["age_hours"] == 4.0


def test_stale_when_older_than_threshold():
    r = ds.assess_layer("x", "2026-06-10 00:00:00 UTC", 5, NOW, threshold_hours=36)
    assert r["status"] == "stale"
    assert r["age_hours"] > 36


def test_missing_when_no_ts_no_rows():
    assert ds.assess_layer("x", None, 0, NOW, 36)["status"] == "missing"
    assert ds.assess_layer("x", "", 0, NOW, 36)["status"] == "missing"


def test_empty_when_rows_zero_but_ts_present():
    assert ds.assess_layer("x", "2026-06-15 20:00:00 UTC", 0, NOW, 36)["status"] == "empty"


def test_allow_empty_layer_is_fresh_with_zero_rows():
    # 監査系(0件=異常なし)は row=0でも生成時刻が新しければ fresh
    r = ds.assess_layer("adv", "2026-06-15 20:00:00 UTC", 0, NOW, 36, allow_empty=True)
    assert r["status"] == "fresh"


def test_unavailable_overrides():
    r = ds.assess_layer("x", "2026-06-15 20:00:00 UTC", 5, NOW, 36, unavailable=True)
    assert r["status"] == "unavailable"


def test_unknown_age_when_rows_but_no_ts():
    r = ds.assess_layer("x", None, 5, NOW, 36)
    assert r["status"] == "unknown_age"


# === data_health_summary 集計 ===

def _extras_with(adv_status="passed", narr_status="passed"):
    return {
        "latest_evaluations_summary_json": {"generated_at_utc": "2026-06-15 20:00:00 UTC"},
        "prediction_calibration_json": {"generated_at_utc": "2026-06-15 20:00:00 UTC", "calibration_status": "tracking"},
        "narrative_reliability_json": {"generated_at_utc": "2026-06-15 20:00:00 UTC", "narrative_reliability_status": narr_status},
        "narrative_lookahead_audit_summary_json": {"generated_at_utc": "2026-06-15 20:00:00 UTC", "audit_status": "passed"},
        "adversarial_review_summary_json": {"generated_at_utc": "2026-06-15 20:00:00 UTC", "review_status": adv_status},
        "news_narrative_scores_json": {"generated_at_utc": "2026-06-15 20:00:00 UTC"},
        "ai_feedback_json": [{"generated_at_utc": "2026-06-15 20:00:00 UTC"}],
        "portfolio_layer_summary_json": {"generated_at_utc": "2026-06-15 20:00:00 UTC"},
        "datetime_audit_summary_json": {"generated_at_utc": "2026-06-15 20:00:00 UTC"},
        "model_state_update_summary_json": {"generated_at_jst": "2026-06-16 05:00:00 JST"},
    }


def _row_counts_all(n=3):
    return {k: n for k in [
        "signals", "evaluations", "latest_evaluations", "weekly_review", "monthly_calibration",
        "prediction_calibration", "narrative_reliability", "narrative_lookahead_audit", "adversarial_review",
        "news_narrative_scores", "ai_feedback", "portfolio_layer", "datetime_audit", "model_state_update_proposals",
    ]}


def _latest_dates_fresh():
    return {
        "latest_signal_date": "2026-06-15", "latest_evaluation_date": "2026-06-15",
        "latest_weekly_review_date": "2026-06-15", "latest_monthly_calibration_date": "2026-06-15",
    }


def test_health_summary_healthy_when_all_fresh():
    h = ds.data_health_summary(_extras_with(), _row_counts_all(3), _latest_dates_fresh(), NOW)
    assert h["available"] is True
    assert h["health_status"] == "healthy"
    assert h["stale_count"] == 0 and h["missing_count"] == 0 and h["empty_count"] == 0
    assert h["attention_layers"] == []


def test_health_summary_critical_when_core_missing():
    # signals/evaluations が欠損 -> critical
    rc = _row_counts_all(3)
    rc["signals"] = 0
    rc["evaluations"] = 0
    ld = _latest_dates_fresh()
    ld["latest_signal_date"] = ""
    ld["latest_evaluation_date"] = ""
    h = ds.data_health_summary(_extras_with(), rc, ld, NOW)
    assert h["health_status"] == "critical"
    assert "signals" in h["attention_layers"] and "evaluations" in h["attention_layers"]


def test_health_summary_degraded_when_stale():
    extras = _extras_with()
    extras["portfolio_layer_summary_json"] = {"generated_at_utc": "2026-05-01 00:00:00 UTC"}  # 古い
    h = ds.data_health_summary(extras, _row_counts_all(3), _latest_dates_fresh(), NOW)
    assert h["health_status"] in ("degraded", "critical")
    assert "portfolio_layer" in h["attention_layers"]


def test_health_summary_unavailable_layer_flagged():
    h = ds.data_health_summary(_extras_with(narr_status="unavailable"), _row_counts_all(3), _latest_dates_fresh(), NOW)
    assert h["unavailable_count"] >= 1
    assert "narrative_reliability" in h["attention_layers"]


def test_adversarial_review_zero_rows_not_empty():
    rc = _row_counts_all(3)
    rc["adversarial_review"] = 0  # 0件=正常
    h = ds.data_health_summary(_extras_with(), rc, _latest_dates_fresh(), NOW)
    adv = [l for l in h["layers"] if l["layer"] == "adversarial_review"][0]
    assert adv["status"] == "fresh"


# === safety flags 固定 ===

def test_safety_flags_fixed():
    h = ds.data_health_summary(_extras_with(), _row_counts_all(3), _latest_dates_fresh(), NOW)
    assert h["requires_human_approval"] is True
    assert h["weights_json_updated"] is False
    assert h["generate_signal_updated"] is False


# === 空入力で落ちない ===

def test_empty_inputs_do_not_crash():
    h = ds.data_health_summary({}, {}, {}, NOW)
    assert h["available"] is True
    assert h["total_layers"] == len(ds.LAYER_HEALTH_REGISTRY)
    # 全レイヤー missing 相当 -> critical
    assert h["health_status"] == "critical"


# === セルフ監査で指摘されたギャップの追補 ===

def test_stale_boundary_minutes_past_is_stale_not_fresh():
    # 丸めバグ回帰防止: しきい値を数分超えたら fresh ではなく stale
    # ts = now - 36h - 90s -> raw_age 36.025h > 36 -> stale (旧実装は round で 36.0 になり fresh だった)
    ts = (NOW - pd.Timedelta(hours=36, seconds=90)).strftime("%Y-%m-%d %H:%M:%S") + " UTC"
    assert ds.assess_layer("x", ts, 5, NOW, threshold_hours=36)["status"] == "stale"


def test_stale_boundary_exactly_threshold_is_fresh():
    # ちょうど閾値(age==36)は strict '>' なので fresh
    ts = (NOW - pd.Timedelta(hours=36)).strftime("%Y-%m-%d %H:%M:%S") + " UTC"
    assert ds.assess_layer("x", ts, 5, NOW, threshold_hours=36)["status"] == "fresh"


def test_future_timestamp_flagged_as_anomaly():
    # 明確に未来(>1h)の生成時刻は時計異常として future_timestamp
    ts = (NOW + pd.Timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S") + " UTC"
    r = ds.assess_layer("x", ts, 5, NOW, threshold_hours=36)
    assert r["status"] == "future_timestamp"
    assert r["age_hours"] < 0


def test_small_future_skew_tolerated_as_fresh():
    # 軽微なクロックスキュー(<1h)は許容して fresh
    ts = (NOW + pd.Timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S") + " UTC"
    assert ds.assess_layer("x", ts, 5, NOW, threshold_hours=36)["status"] == "fresh"


def test_health_summary_watch_on_future_timestamp():
    extras = _extras_with()
    extras["portfolio_layer_summary_json"] = {"generated_at_utc": (NOW + pd.Timedelta(hours=10)).strftime("%Y-%m-%d %H:%M:%S") + " UTC"}
    h = ds.data_health_summary(extras, _row_counts_all(3), _latest_dates_fresh(), NOW)
    assert h["future_timestamp_count"] >= 1
    assert h["health_status"] == "watch"
    assert "portfolio_layer" in h["attention_layers"]


def test_health_summary_watch_when_only_unknown_age():
    # 行はあるが全レイヤーの生成時刻が取れない -> watch
    rc = _row_counts_all(3)
    ld = {k: "" for k in ["latest_signal_date", "latest_evaluation_date", "latest_weekly_review_date", "latest_monthly_calibration_date"]}
    h = ds.data_health_summary({}, rc, ld, NOW)
    assert h["health_status"] == "watch"
    assert h["unknown_age_count"] > 0
    assert h["missing_count"] == 0 and h["stale_count"] == 0


def test_rollup_precedence_unavailable_beats_stale_and_worst_layer():
    extras = _extras_with(narr_status="unavailable")
    extras["portfolio_layer_summary_json"] = {"generated_at_utc": "2026-05-01 00:00:00 UTC"}  # stale
    h = ds.data_health_summary(extras, _row_counts_all(3), _latest_dates_fresh(), NOW)
    assert h["health_status"] == "critical"          # unavailable が stale より優先
    assert h["worst_status"] == "unavailable"        # _HEALTH_RANK 最大
    assert h["worst_layer"] == "narrative_reliability"


def test_resolve_ts_jst_fallback_for_utc_spec():
    # _utc キーが無く generated_at_jst だけのレイヤー(model_state)が fresh になる
    extras = _extras_with()
    extras["model_state_update_summary_json"] = {"generated_at_jst": "2026-06-16 05:00:00 JST"}
    h = ds.data_health_summary(extras, _row_counts_all(3), _latest_dates_fresh(), NOW)
    ms = [l for l in h["layers"] if l["layer"] == "model_state_proposals"][0]
    assert ms["status"] == "fresh"
    assert ms["last_generated"]


def test_parse_jst_dateonly_and_tz_offset():
    # JST日付のみは -9h、tz-aware offset も正規化される
    assert ds.parse_generated_at("2026-06-16 JST") == pd.Timestamp("2026-06-15 15:00:00")
    assert ds.parse_generated_at("2026-06-16 08:00:00+09:00") == pd.Timestamp("2026-06-15 23:00:00")


def test_allow_empty_does_not_mask_missing_or_stale():
    # allow_empty でも、生成時刻が無ければ missing / 古ければ stale
    assert ds.assess_layer("x", None, 0, NOW, 36, allow_empty=True)["status"] == "missing"
    assert ds.assess_layer("x", "2026-05-01 00:00:00 UTC", 0, NOW, 36, allow_empty=True)["status"] == "stale"


def test_resolve_ts_list_payload_unwrap():
    # ai_feedback はリスト形式。先頭レコードの generated_at を使う
    extras = _extras_with()
    extras["ai_feedback_json"] = [{"generated_at_utc": "2026-06-15 20:00:00 UTC"}]
    h = ds.data_health_summary(extras, _row_counts_all(3), _latest_dates_fresh(), NOW)
    ai = [l for l in h["layers"] if l["layer"] == "ai_feedback"][0]
    assert ai["status"] == "fresh"
    # 空リストかつ行0 -> missing
    extras["ai_feedback_json"] = []
    rc = _row_counts_all(3); rc["ai_feedback"] = 0
    h2 = ds.data_health_summary(extras, rc, _latest_dates_fresh(), NOW)
    ai2 = [l for l in h2["layers"] if l["layer"] == "ai_feedback"][0]
    assert ai2["status"] == "missing"


# === evaluation_summary 評価成熟度: 「評価0件/未決着だけ」を false healthy にしない (Phase 27.2) ===

def test_evaluation_maturity_no_signals_when_empty():
    s = ds.evaluation_summary(pd.DataFrame())
    assert s["evaluation_maturity"] == "no_signals"
    assert s["closed"] == 0
    assert s["awaiting_horizon"] == 0
    assert s["data_missing"] == 0


def test_evaluation_maturity_accumulating_when_no_finalized():
    # 全件 pending / awaiting_horizon -> 決着0 -> accumulating(active にしない)
    df = pd.DataFrame(
        [
            {"evaluation_status": "pending", "outcome": "open_unresolved", "error_type": "awaiting_horizon", "r_multiple": None},
            {"evaluation_status": "pending", "outcome": "open_unresolved", "error_type": "data_missing", "r_multiple": None},
        ]
    )
    s = ds.evaluation_summary(df)
    assert s["evaluation_maturity"] == "accumulating"
    assert s["closed"] == 0
    assert s["awaiting_horizon"] == 1
    assert s["data_missing"] == 1


def test_evaluation_maturity_active_only_when_finalized_exists():
    df = pd.DataFrame(
        [
            {"evaluation_status": "closed", "outcome": "win_tp1", "error_type": "target_reached", "r_multiple": 2.0},
            {"evaluation_status": "pending", "outcome": "open_unresolved", "error_type": "awaiting_horizon", "r_multiple": None},
        ]
    )
    s = ds.evaluation_summary(df)
    assert s["evaluation_maturity"] == "active"
    assert s["closed"] == 1
    assert s["awaiting_horizon"] == 1


def test_evaluation_maturity_accumulating_when_only_no_trade_unassessed():
    # no_trade だが正否未確定(awaiting_horizon)のみ -> finalized=0 -> accumulating
    df = pd.DataFrame(
        [
            {"evaluation_status": "skipped", "outcome": "no_trade", "error_type": "awaiting_horizon", "r_multiple": 0.0},
        ]
    )
    s = ds.evaluation_summary(df)
    assert s["evaluation_maturity"] == "accumulating"


def test_evaluation_maturity_invalid_dates_not_active():
    # 入力不正(invalid_signal_date)だけでは active 化しない。件数として可視化される (Codex P2)
    df = pd.DataFrame(
        [
            {"evaluation_status": "skipped", "outcome": "invalid", "error_type": "invalid_signal_date", "r_multiple": None},
            {"evaluation_status": "skipped", "outcome": "invalid", "error_type": "invalid_signal_date", "r_multiple": None},
        ]
    )
    s = ds.evaluation_summary(df)
    assert s["evaluation_maturity"] != "active"
    assert s["evaluation_maturity"] == "accumulating"
    assert s["invalid_signal_date"] == 2


# === evaluation_summary 29日窓の determinism (UTC as_of / local datetime.now() 非依存) ===

def _two_closed_around_cutoff():
    # as_of=2026-06-16 のとき cutoff=2026-05-18。境界(=29日前)は含み、その前日は除外。
    return pd.DataFrame(
        [
            {"evaluation_status": "closed", "outcome": "win_tp1", "r_multiple": 1.0, "evaluation_date": "2026-05-18"},
            {"evaluation_status": "closed", "outcome": "loss_sl", "r_multiple": -1.0, "evaluation_date": "2026-05-17"},
        ]
    )


def test_evaluation_summary_29day_window_uses_injected_as_of():
    s = ds.evaluation_summary(_two_closed_around_cutoff(), as_of="2026-06-16")
    # 2026-05-18(=cutoff)のみ残り、2026-05-17 は除外される
    assert s["closed"] == 1
    assert s["total_evaluated"] == 1


def test_evaluation_summary_window_is_tz_stable(monkeypatch):
    # ローカル時計を動かしても、注入した as_of に対して結果は一定 (datetime.now() 非依存)
    df = _two_closed_around_cutoff()
    a = ds.evaluation_summary(df, as_of="2026-06-16")
    b = ds.evaluation_summary(df, as_of="2026-06-16")
    assert a["closed"] == b["closed"] == 1
    # as_of を1日進めると窓も1日進み、2026-05-18 が脱落して closed=0
    s_next = ds.evaluation_summary(df, as_of="2026-06-17")
    assert s_next["closed"] == 0


def test_evaluation_summary_default_as_of_uses_utc_now(monkeypatch):
    # as_of 未指定なら ds.now_utc()(UTC) を基準にする。local datetime.now() を使わない
    fixed = pd.Timestamp("2026-06-16 00:00:00", tz="UTC")
    monkeypatch.setattr(ds, "now_utc", lambda: fixed)
    s = ds.evaluation_summary(_two_closed_around_cutoff())
    assert s["closed"] == 1


def test_evaluation_summary_malformed_as_of_falls_back_to_utc_now(monkeypatch):
    # 不正な as_of は窓を壊さず UTC today へフォールバック(例外で落ちない / 非決定にならない)
    fixed = pd.Timestamp("2026-06-16 00:00:00", tz="UTC")
    monkeypatch.setattr(ds, "now_utc", lambda: fixed)
    s = ds.evaluation_summary(_two_closed_around_cutoff(), as_of="not-a-date")
    assert s["closed"] == 1  # fixed=2026-06-16 基準と一致
    # NaT 系も同様にフォールバック
    assert ds.evaluation_summary(_two_closed_around_cutoff(), as_of=float("nan"))["closed"] == 1


def test_asset_performance_uses_same_injected_as_of_window():
    # 資産別成績も dashboard 全体の as_of と同じ29日窓を使う。
    # ここが default now_utc() 任せだと、日境界をまたぐ実行で上部summaryとズレ得る。
    evaluations = _two_closed_around_cutoff()
    evaluations["asset"] = "BTC"
    signals = pd.DataFrame([{"asset": "BTC"}])

    current = ds.asset_performance(signals, evaluations, as_of="2026-06-16")
    next_day = ds.asset_performance(signals, evaluations, as_of="2026-06-17")

    assert current.loc[0, "total_r"] == 1.0
    assert current.loc[0, "win_rate"] == 1.0
    assert next_day.loc[0, "total_r"] == 0.0
    assert next_day.loc[0, "win_rate"] == 0.0
