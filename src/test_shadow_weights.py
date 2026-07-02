"""Shadow weights layer (Phase 29.1) の単体テスト。

検証の柱:
1. 承認済み weights のみ読み込む（missing/invalid/not_approved は正直なステータス）
2. identity weights なら weighted == base（厳密ゼロ差分）
3. 非identity weights で rank/strength が期待通り変化する
4. base side=NONE 行は weighted でも復活しない
5. shadow 成果物は安全フィールド(shadow_mode=true / affects_live_recommendation=false)を必ず携行
6. 比較台帳の追記・重複排除・昇格判断材料(累積>=30)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import shadow_weights as sw


def _signal_row(**over) -> dict:
    base = dict(
        date="2026-07-02", signal_id="20260702_WTI_LONG_TREND", asset="WTI", side="LONG",
        rank="A", recommended_action="TRADE",
        trend_score=80.0, momentum_score=70.0, volatility_score=80.0,
        risk_penalty_score=10.0, entry_quality_score=70.0, direction_confidence=70.0,
        rr=1.5, signal_strength=73.25,
    )
    base.update(over)
    return base


def _weights(**global_over) -> dict:
    glob = {k: 1.0 for k in sw._GLOBAL_KEYS}
    glob.update(global_over)
    return {
        "global": glob,
        "asset_weights": {"WTI": 1.0, "BTC": 1.0},
        "rank_weights": {"A": 1.0, "B": 1.0, "NO_TRADE": 1.0},
        "side_weights": {"LONG": 1.0, "SHORT": 1.0, "NONE": 1.0},
    }


def _approved_payload(**over) -> dict:
    payload = {
        "schema_version": 1, "status": "approved", "weights_version": "vT",
        "approved_by": "human (PR merge)", "approved_at": "2026-07-02",
        "source_pr": 0, "sample_count": 0, "guard_report_id": None,
    }
    payload.update(_weights())
    payload.update(over)
    return payload


# === 1. 読込: 承認済みのみ / 正直なステータス ===

def test_load_missing(tmp_path):
    r = sw.load_approved_weights(tmp_path / "nope.json")
    assert r["status"] == "missing" and r["weights"] is None


def test_load_not_approved(tmp_path):
    p = tmp_path / "w.json"
    p.write_text(json.dumps(_approved_payload(status="draft")), encoding="utf-8")
    r = sw.load_approved_weights(p)
    assert r["status"] == "not_approved" and r["weights"] is None


def test_load_corrupt_json(tmp_path):
    p = tmp_path / "w.json"
    p.write_text("{not json", encoding="utf-8")
    assert sw.load_approved_weights(p)["status"] == "invalid"


def test_load_non_numeric_weight_is_invalid(tmp_path):
    payload = _approved_payload()
    payload["global"]["trend_weight"] = "abc"
    p = tmp_path / "w.json"
    p.write_text(json.dumps(payload), encoding="utf-8")
    assert sw.load_approved_weights(p)["status"] == "invalid"


def test_shipped_repo_file_is_approved_identity():
    # 出荷seed: identity baseline が approved で読めること
    r = sw.load_approved_weights(Path(__file__).parent.parent / "models" / "approved_weights.json")
    assert r["status"] == "approved"
    assert r["weights_version"] == "v0-identity"
    assert sw.is_identity_weights(r["weights"]) is True


# === 2. identity なら厳密ゼロ差分 ===

def test_identity_zero_diff_long_and_short():
    signals = pd.DataFrame([
        _signal_row(),
        _signal_row(signal_id="s2", side="SHORT", trend_score=20.0, momentum_score=30.0),
    ])
    out = sw.compute_shadow(signals, _weights(), "vT")
    assert not out["rank_changed"].any()
    assert not out["action_changed"].any()
    assert (out["strength_delta"] == 0).all()
    assert (out["weighted_rank"] == out["recon_base_rank"]).all()
    # 再構成が保存rankと一致(mismatchなし)
    assert not out["reconstruction_mismatch"].any()


# === 3. 非identity で期待通り変化 ===

def test_downweight_trend_downgrades_rank():
    # trend_weight=0.5 -> setup 76.5 -> 62.5 で A -> B に降格
    signals = pd.DataFrame([_signal_row()])
    out = sw.compute_shadow(signals, _weights(trend_weight=0.5), "vT")
    r = out.iloc[0]
    assert r["recon_base_rank"] == "A"
    assert r["weighted_rank"] == "B"
    assert r["rank_changed"] and r["action_changed"]
    assert r["weighted_recommended_action"] == "WATCH"
    assert r["strength_delta"] < 0


def test_risk_penalty_weight_increase_can_downgrade():
    # risk_penalty_weight=10 -> setup 76.5 - 0.2*10*10 +2(元のペナルティ分) => 大幅低下 -> NO_TRADE
    signals = pd.DataFrame([_signal_row()])
    out = sw.compute_shadow(signals, _weights(risk_penalty_weight=40.0), "vT")
    assert out.iloc[0]["weighted_rank"] == "NO_TRADE"
    assert out.iloc[0]["weighted_signal_strength"] == 0.0


# === 4. NONE 行は復活しない ===

def test_none_rows_never_resurrected():
    signals = pd.DataFrame([
        _signal_row(signal_id="n1", side="NONE", rank="NO_TRADE", recommended_action="NO_TRADE",
                    rr=0.0, signal_strength=0.0),
    ])
    out = sw.compute_shadow(signals, _weights(trend_weight=3.0, momentum_weight=3.0), "vT")
    assert out.iloc[0]["weighted_rank"] == "NO_TRADE"
    assert out.iloc[0]["weighted_signal_strength"] == 0.0


# === 5. run(): 出力・安全フィールド・台帳 ===

def _setup_dirs(tmp_path, monkeypatch):
    monkeypatch.setattr(sw, "RESULTS_DIR", tmp_path / "results")
    monkeypatch.setattr(sw, "REPORTS_DIR", tmp_path / "reports")
    monkeypatch.setattr(sw, "LEDGER_PATH", tmp_path / "data" / "ledger.csv")


def test_run_writes_outputs_and_ledger(tmp_path, monkeypatch):
    _setup_dirs(tmp_path, monkeypatch)
    p = tmp_path / "approved.json"
    p.write_text(json.dumps(_approved_payload()), encoding="utf-8")
    signals = pd.DataFrame([_signal_row(), _signal_row(signal_id="s2", side="NONE", rank="NO_TRADE", rr=0.0)])

    summary = sw.run(signals, models_path=p)

    assert (tmp_path / "results" / "shadow_weighted_signals.csv").exists()
    assert (tmp_path / "results" / "shadow_weight_impact_summary.json").exists()
    assert (tmp_path / "reports" / "shadow_weight_impact.md").exists()
    assert summary["weights_status"] == "approved"
    assert summary["n_signals"] == 2 and summary["n_actionable"] == 1
    # 安全フィールド固定
    assert summary["shadow_mode"] is True
    assert summary["affects_live_recommendation"] is False
    assert summary["weights_json_updated"] is False
    assert summary["patch_applied"] is False
    assert summary["apply_automatically"] is False
    assert summary["requires_human_approval"] is True

    ledger = pd.read_csv(tmp_path / "data" / "ledger.csv")
    assert len(ledger) == 1 and int(ledger.iloc[0]["n_actionable"]) == 1

    # 同日再実行 -> 重複しない(上書き)
    sw.run(signals, models_path=p)
    ledger = pd.read_csv(tmp_path / "data" / "ledger.csv")
    assert len(ledger) == 1


def test_run_not_approved_is_honest(tmp_path, monkeypatch):
    _setup_dirs(tmp_path, monkeypatch)
    p = tmp_path / "approved.json"
    p.write_text(json.dumps(_approved_payload(status="draft")), encoding="utf-8")
    summary = sw.run(pd.DataFrame([_signal_row()]), models_path=p)
    assert summary["weights_status"] == "not_approved"
    assert summary["n_signals"] == 0  # 比較は実行しない(捏造しない)
    report = (tmp_path / "reports" / "shadow_weight_impact.md").read_text(encoding="utf-8")
    assert "weights未適用" in report


def test_run_without_signals_is_honest(tmp_path, monkeypatch):
    _setup_dirs(tmp_path, monkeypatch)
    p = tmp_path / "approved.json"
    p.write_text(json.dumps(_approved_payload()), encoding="utf-8")
    summary = sw.run(pd.DataFrame(), models_path=p)
    assert summary["weights_status"] == "no_signals"
    assert summary["n_signals"] == 0


# === 6. 昇格判断材料 ===

def test_promotion_readiness_threshold():
    empty = pd.DataFrame(columns=sw.SHADOW_COLUMNS)
    loaded = {"status": "approved", "weights_version": "vT", "weights": _weights(), "meta": {}}
    from time_utils import now_utc
    not_ready = sw.build_summary(empty, loaded, 29, now_utc())
    ready = sw.build_summary(empty, loaded, 30, now_utc())
    assert not_ready["promotion_sample_ready"] is False
    assert ready["promotion_sample_ready"] is True
    assert ready["min_comparisons_for_promotion"] == 30


def test_comparisons_accumulated_filters_by_version():
    ledger = pd.DataFrame([
        {"date": "2026-07-01", "weights_version": "vA", "n_actionable": 10},
        {"date": "2026-07-02", "weights_version": "vA", "n_actionable": 5},
        {"date": "2026-07-02", "weights_version": "vB", "n_actionable": 99},
    ])
    assert sw._comparisons_accumulated(ledger, "vA") == 15
    assert sw._comparisons_accumulated(ledger, "vB") == 99
    assert sw._comparisons_accumulated(ledger, "vC") == 0


# === 昇格ゲート (司令 B-1 指示: identity のうちにブロック条件をテストで固定) ===
# 「小標本1件の後知恵(例: OBS-20260608-WTI の単発 failure)で weights を動かさない」を
# 機械的に保証する。ゲート通過=材料提示のみで、承認は常に人間PR(不可侵 #4)。

def test_gate_blocked_without_outcome_linkage_even_with_many_comparisons():
    # 比較数が閾値を大きく超えても、結果(R差分)系列が未接続なら必ず blocked
    gate = sw.evaluate_promotion_gate(None, comparisons_accumulated=1000)
    assert gate["decision"] == "blocked"
    assert any(r.startswith("no_outcome_linkage") for r in gate["blocked_reasons"])
    assert gate["requires_human_approval"] is True
    assert gate["apply_automatically"] is False


def test_gate_blocked_on_single_observation_hindsight():
    # 単発の観測(n=1)では絶対に materials_ready にならない
    gate = sw.evaluate_promotion_gate([2.5], comparisons_accumulated=1)
    assert gate["decision"] == "blocked"
    joined = " ".join(gate["blocked_reasons"])
    assert "insufficient_comparisons" in joined
    assert "insufficient_outcome_samples" in joined


def test_gate_blocked_at_29_samples():
    diffs = [0.5] * 29
    gate = sw.evaluate_promotion_gate(diffs, comparisons_accumulated=29)
    assert gate["decision"] == "blocked"
    assert any("insufficient" in r for r in gate["blocked_reasons"])


def test_gate_blocked_on_zero_difference_identity():
    # identity weights の帰結: 差分ゼロ30件 -> 変更を正当化できない
    gate = sw.evaluate_promotion_gate([0.0] * 30, comparisons_accumulated=30)
    assert gate["decision"] == "blocked"
    assert any(r.startswith("zero_difference") for r in gate["blocked_reasons"])


def test_gate_blocked_when_mean_negative():
    gate = sw.evaluate_promotion_gate([-0.3] * 30, comparisons_accumulated=30)
    assert gate["decision"] == "blocked"
    assert any(r.startswith("mean_diff_not_positive") for r in gate["blocked_reasons"])


def test_gate_blocked_when_noisy_not_significant():
    # 平均は僅かに正だがノイズが大きい -> t検定で弾く
    diffs = [0.02, -1.0, 1.0, -0.9, 0.95] * 6  # n=30, mean~0.014
    gate = sw.evaluate_promotion_gate(diffs, comparisons_accumulated=30)
    assert gate["decision"] == "blocked"
    assert any(r.startswith("not_significant") or r.startswith("dsr_below") for r in gate["blocked_reasons"])


def test_gate_blocked_by_dsr_under_multiple_testing():
    # 単独なら有意に見える系列でも、多数候補の同時検定(n_trials=20, 候補間分散大)では
    # 期待最大Sharpeに届かず DSR が弾く
    diffs = [0.1, 0.12, 0.08, 0.11, 0.09, 0.1] * 5  # n=30, 安定した正
    single = sw.evaluate_promotion_gate(diffs, comparisons_accumulated=30, n_trials=1)
    multi = sw.evaluate_promotion_gate(diffs, comparisons_accumulated=30, n_trials=20, sharpe_variance=25.0)
    assert single["decision"] == "materials_ready"  # 単独検定なら通る
    assert multi["decision"] == "blocked"
    assert any(r.startswith("dsr_below_threshold") for r in multi["blocked_reasons"])


def test_gate_materials_ready_never_auto_applies():
    # 全条件クリアでも「材料提示」止まり(人間承認とセット)
    diffs = [0.5, 0.6, 0.45, 0.55, 0.5, 0.58] * 5  # n=30, 強く安定した正
    gate = sw.evaluate_promotion_gate(diffs, comparisons_accumulated=60)
    assert gate["decision"] == "materials_ready"
    assert gate["blocked_reasons"] == []
    assert gate["requires_human_approval"] is True
    assert gate["apply_automatically"] is False


def test_summary_carries_gate_and_v0_is_blocked():
    # v0(identity, outcome未接続)の run では summary の gate が必ず blocked
    from time_utils import now_utc
    loaded = sw.load_approved_weights(Path("models/approved_weights.json"))  # repo同梱の v0-identity
    summary = sw.build_summary(pd.DataFrame(columns=sw.SHADOW_COLUMNS), loaded, 1000, now_utc())
    assert summary["promotion_gate"]["decision"] == "blocked"
    assert summary["promotion_sample_ready"] is True  # 蓄積進捗とゲートは別物として両立
