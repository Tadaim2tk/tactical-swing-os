"""jp_swing_ledger.py + jp_adversarial_checklist.py のユニットテスト。"""

from __future__ import annotations

import io
import tempfile
from pathlib import Path

import pandas as pd
import pytest

import jp_swing_ledger as ledger
import jp_adversarial_checklist as adv


# ── validate_signal_row ──────────────────────────────────────────

def _minimal_signal() -> dict:
    return {
        "hypothesis_id": "JP-20260616-001",
        "decision_date": "2026-06-16",
        "intended_order_date": "2026-06-17",
        "assumed_execution_date": "2026-06-18",
        "ticker": "7203.T",
        "company_name": "トヨタ自動車",
        "sector": "輸送用機器",
        "narrative": "テスト仮説",
        "falsifier": "来期ガイダンスが市場予想を下回る",
        "horizon_days": 20,
        "confidence_pct": 65,
        "status": "pending",
    }


def test_validate_signal_valid_row_passes():
    row = _minimal_signal()
    errors = ledger.validate_signal_row(row)
    assert errors == []


def test_validate_signal_missing_hypothesis_id():
    row = _minimal_signal()
    row["hypothesis_id"] = ""
    errors = ledger.validate_signal_row(row)
    assert any("hypothesis_id" in e for e in errors)


def test_validate_signal_missing_narrative():
    row = _minimal_signal()
    row["narrative"] = ""
    errors = ledger.validate_signal_row(row)
    assert any("narrative" in e for e in errors)


def test_validate_signal_empty_falsifier_rejected():
    row = _minimal_signal()
    row["falsifier"] = "未定"
    errors = ledger.validate_signal_row(row)
    assert any("falsifier" in e for e in errors)


def test_validate_signal_tbd_falsifier_rejected():
    row = _minimal_signal()
    row["falsifier"] = "tbd"
    errors = ledger.validate_signal_row(row)
    assert any("falsifier" in e for e in errors)


def test_validate_signal_invalid_horizon():
    row = _minimal_signal()
    row["horizon_days"] = 15  # not in {10,20,30}
    errors = ledger.validate_signal_row(row)
    assert any("horizon_days" in e for e in errors)


def test_validate_signal_invalid_confidence_over_100():
    row = _minimal_signal()
    row["confidence_pct"] = 110
    errors = ledger.validate_signal_row(row)
    assert any("confidence_pct" in e for e in errors)


def test_validate_signal_invalid_confidence_negative():
    row = _minimal_signal()
    row["confidence_pct"] = -5
    errors = ledger.validate_signal_row(row)
    assert any("confidence_pct" in e for e in errors)


def test_validate_signal_invalid_catalyst_type():
    row = _minimal_signal()
    row["catalyst_type"] = "unknown_type"
    errors = ledger.validate_signal_row(row)
    assert any("catalyst_type" in e for e in errors)


def test_validate_signal_valid_catalyst_types():
    for ct in ledger.VALID_CATALYST_TYPES:
        row = _minimal_signal()
        row["catalyst_type"] = ct
        errors = ledger.validate_signal_row(row)
        assert not any("catalyst_type" in e for e in errors), f"Failed for {ct}"


def test_validate_signal_date_order_violation_intended_before_decision():
    row = _minimal_signal()
    row["intended_order_date"] = "2026-06-15"  # decision_date(6/16)より前
    errors = ledger.validate_signal_row(row)
    assert any("intended_order_date" in e for e in errors)


def test_validate_signal_date_order_violation_assumed_before_intended():
    row = _minimal_signal()
    row["assumed_execution_date"] = "2026-06-16"  # intended(6/17)より前
    errors = ledger.validate_signal_row(row)
    assert any("assumed_execution_date" in e for e in errors)


def test_validate_signal_valid_falsifier_type():
    for ft in ledger.VALID_FALSIFIER_TYPES:
        row = _minimal_signal()
        row["falsifier_type"] = ft
        errors = ledger.validate_signal_row(row)
        assert not any("falsifier_type" in e for e in errors), f"Failed for {ft}"


def test_validate_signal_invalid_falsifier_type():
    row = _minimal_signal()
    row["falsifier_type"] = "unknown_type"
    errors = ledger.validate_signal_row(row)
    assert any("falsifier_type" in e for e in errors)


def test_validate_signal_invalid_outcome_type():
    row = _minimal_signal()
    row["outcome_type"] = "Z"
    errors = ledger.validate_signal_row(row)
    assert any("outcome_type" in e for e in errors)


def test_validate_signal_valid_outcome_types():
    for ot in ledger.OUTCOME_TYPES:
        row = _minimal_signal()
        row["outcome_type"] = ot
        errors = ledger.validate_signal_row(row)
        assert not any("outcome_type" in e for e in errors), f"Failed for {ot}"


# ── validate_pass_row ────────────────────────────────────────────

def _minimal_pass() -> dict:
    return {
        "pass_id": "PASS-20260616-001",
        "assessment_date": "2026-06-16",
        "ticker": "6758.T",
        "company_name": "ソニーグループ",
        "pass_reason": "too_chased",
        "pass_detail": "直近3日で+8%急騰後のためラグで不利",
    }


def test_validate_pass_valid_row_passes():
    row = _minimal_pass()
    errors = ledger.validate_pass_row(row)
    assert errors == []


def test_validate_pass_missing_pass_id():
    row = _minimal_pass()
    row["pass_id"] = ""
    errors = ledger.validate_pass_row(row)
    assert any("pass_id" in e for e in errors)


def test_validate_pass_missing_pass_detail():
    row = _minimal_pass()
    row["pass_detail"] = ""
    errors = ledger.validate_pass_row(row)
    assert any("pass_detail" in e for e in errors)


def test_validate_pass_invalid_reason():
    row = _minimal_pass()
    row["pass_reason"] = "bad_reason"
    errors = ledger.validate_pass_row(row)
    assert any("pass_reason" in e for e in errors)


def test_validate_pass_all_valid_reasons():
    for reason in ledger.VALID_PASS_REASONS:
        row = _minimal_pass()
        row["pass_reason"] = reason
        errors = ledger.validate_pass_row(row)
        assert not any("pass_reason" in e for e in errors), f"Failed for {reason}"


# ── load/save ─────────────────────────────────────────────────────

def test_load_signals_nonexistent_returns_empty_df():
    df = ledger.load_signals(Path("/tmp/nonexistent_jp_signals.csv"))
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ledger.JP_SIGNAL_COLUMNS
    assert len(df) == 0


def test_load_pass_log_nonexistent_returns_empty_df():
    df = ledger.load_pass_log(Path("/tmp/nonexistent_jp_pass.csv"))
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ledger.JP_PASS_LOG_COLUMNS
    assert len(df) == 0


def test_save_and_load_roundtrip():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "test_signals.csv"
        row = {col: "" for col in ledger.JP_SIGNAL_COLUMNS}
        row.update(_minimal_signal())
        df = pd.DataFrame([row])
        ledger.save_signals(df, path)
        loaded = ledger.load_signals(path)
        assert len(loaded) == 1
        assert loaded.iloc[0]["ticker"] == "7203.T"


# ── validate_signals_df ──────────────────────────────────────────

def test_validate_signals_df_all_valid():
    row = {col: "" for col in ledger.JP_SIGNAL_COLUMNS}
    row.update(_minimal_signal())
    df = pd.DataFrame([row])
    issues = ledger.validate_signals_df(df)
    assert issues == []


def test_validate_signals_df_flags_bad_rows():
    row = {col: "" for col in ledger.JP_SIGNAL_COLUMNS}
    row.update(_minimal_signal())
    row["falsifier"] = ""  # 不正
    df = pd.DataFrame([row])
    issues = ledger.validate_signals_df(df)
    assert len(issues) == 1
    assert issues[0]["row_index"] == 0


# ── OUTCOME_TYPES completeness ───────────────────────────────────

def test_outcome_types_has_all_six():
    assert set(ledger.OUTCOME_TYPES.keys()) == {"A", "B", "C", "D", "E", "F"}


# ── adversarial checklist ─────────────────────────────────────────

def _all_pass_answers() -> dict:
    return {item.id: "pass" for item in adv.ALL_CHECKS}


def _all_fail_answers() -> dict:
    return {item.id: "fail" for item in adv.ALL_CHECKS}


def test_adoption_decision_all_pass():
    result = adv.adoption_decision(_all_pass_answers())
    assert result["decision"] == "adopt_eligible"
    assert result["critical_fails"] == 0


def test_adoption_decision_critical_fail_blocks():
    answers = _all_pass_answers()
    # fail a critical check
    critical = [i for i in adv.ALL_CHECKS if i.severity == "critical"]
    assert critical, "No critical checks defined"
    answers[critical[0].id] = "fail"
    result = adv.adoption_decision(answers)
    assert result["decision"] == "blocked"


def test_adoption_decision_two_high_fails_recommends_pass():
    answers = _all_pass_answers()
    high_items = [i for i in adv.ALL_CHECKS if i.severity == "high"]
    assert len(high_items) >= 2
    for item in high_items[:2]:
        answers[item.id] = "fail"
    result = adv.adoption_decision(answers)
    assert result["decision"] in {"pass_recommended", "blocked"}


def test_adoption_decision_missing_answers_flags_insufficient():
    result = adv.adoption_decision({})
    assert result["decision"] in {"insufficient_data", "blocked"}


def test_checklist_text_contains_all_ids():
    text = adv.checklist_text()
    for item in adv.ALL_CHECKS:
        assert item.id in text


def test_all_checks_have_unique_ids():
    ids = [item.id for item in adv.ALL_CHECKS]
    assert len(ids) == len(set(ids))


def test_run_checklist_separates_severity():
    answers = _all_pass_answers()
    critical = [i for i in adv.ALL_CHECKS if i.severity == "critical"]
    answers[critical[0].id] = "fail"
    r = adv.run_checklist(answers)
    assert len(r["critical_fails"]) == 1
    assert all(i["id"] != critical[0].id for i in r["high_fails"])


# ── 検証CLI (Phase 27.1): 読み取り専用・ネットワーク無し ─────────

def test_cli_clean_data_exits_zero(tmp_path, capsys):
    """有効な仮説1件 + 空のpass_log → 検証OK・exit 0。"""
    sig = tmp_path / "sig.csv"
    pl = tmp_path / "pl.csv"
    row = _minimal_signal()
    pd.DataFrame([row], columns=ledger.JP_SIGNAL_COLUMNS).to_csv(sig, index=False)
    pd.DataFrame(columns=ledger.JP_PASS_LOG_COLUMNS).to_csv(pl, index=False)
    rc = ledger.main(["--signals", str(sig), "--pass-log", str(pl)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "OK" in out
    assert "読み取り専用" in out  # 安全注意が出る


def test_cli_invalid_data_exits_one(tmp_path, capsys):
    """falsifier 未記入 → 検出されて exit 1。"""
    sig = tmp_path / "sig.csv"
    pl = tmp_path / "pl.csv"
    row = _minimal_signal()
    row["falsifier"] = ""  # 必須が空
    pd.DataFrame([row], columns=ledger.JP_SIGNAL_COLUMNS).to_csv(sig, index=False)
    pd.DataFrame(columns=ledger.JP_PASS_LOG_COLUMNS).to_csv(pl, index=False)
    rc = ledger.main(["--signals", str(sig), "--pass-log", str(pl)])
    assert rc == 1
    out = capsys.readouterr().out
    assert "falsifier" in out


def test_cli_does_not_modify_input_files(tmp_path):
    """CLIは読み取り専用 — 入力CSVのバイト列が前後で一致すること。"""
    sig = tmp_path / "sig.csv"
    pl = tmp_path / "pl.csv"
    pd.DataFrame([_minimal_signal()], columns=ledger.JP_SIGNAL_COLUMNS).to_csv(sig, index=False)
    pd.DataFrame(columns=ledger.JP_PASS_LOG_COLUMNS).to_csv(pl, index=False)
    before_sig = sig.read_bytes(); before_pl = pl.read_bytes()
    ledger.main(["--signals", str(sig), "--pass-log", str(pl)])
    assert sig.read_bytes() == before_sig
    assert pl.read_bytes() == before_pl


def test_cli_empty_files_exit_zero(tmp_path):
    """ヘッダーのみ(出荷seedと同じ状態) → exit 0。"""
    sig = tmp_path / "sig.csv"
    pl = tmp_path / "pl.csv"
    pd.DataFrame(columns=ledger.JP_SIGNAL_COLUMNS).to_csv(sig, index=False)
    pd.DataFrame(columns=ledger.JP_PASS_LOG_COLUMNS).to_csv(pl, index=False)
    assert ledger.main(["--signals", str(sig), "--pass-log", str(pl)]) == 0
