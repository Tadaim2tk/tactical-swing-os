"""Dashboardモジュール分割の後方互換テスト (SPEC: 機能変更なし)。

build_dashboard.py を io / summaries / render の3モジュールへ分割した後も、
公開API・サマリーキー・空データ耐性が維持されることを検証する。
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))

import build_dashboard as bd
import dashboard_io
import dashboard_render
import dashboard_summaries


# === モジュールが正しい責務を持つ ===

def test_io_module_owns_loaders():
    for name in ["load_data", "read_csv", "read_json", "read_text", "load_sheet_data"]:
        assert hasattr(dashboard_io, name), f"dashboard_io missing {name}"


def test_render_module_owns_renderers():
    for name in ["render_html", "stat_card", "table_html", "display_value", "DISPLAY_LABELS"]:
        assert hasattr(dashboard_render, name), f"dashboard_render missing {name}"


def test_summaries_module_owns_summary_functions():
    for name in [
        "signal_summary", "evaluation_summary", "asset_performance",
        "prediction_calibration_summary", "narrative_reliability_summary",
        "transaction_cost_summary", "audit_report_summary",
    ]:
        assert hasattr(dashboard_summaries, name), f"dashboard_summaries missing {name}"


# === build_dashboard が後方互換のため全公開名を再エクスポートする ===

def test_build_dashboard_reexports_public_api():
    for name in [
        "load_data", "render_html", "build_dashboard", "main",
        "signal_summary", "evaluation_summary", "asset_performance",
        "prediction_calibration_summary", "narrative_reliability_summary",
        "transaction_cost_summary", "audit_report_summary",
        "stat_card", "table_html",
    ]:
        assert hasattr(bd, name), f"build_dashboard no longer exposes {name}"


def test_build_dashboard_is_thin():
    # オーケストレーションのみ。肥大化が再発していないこと(目安: 500行未満)。
    lines = (Path(__file__).parent / "build_dashboard.py").read_text(encoding="utf-8").count("\n")
    assert lines < 500, f"build_dashboard.py is {lines} lines; expected thin orchestration"


# === 空データでもサマリー関数が落ちない ===

def test_summaries_handle_empty_data():
    empty = pd.DataFrame()
    assert isinstance(dashboard_summaries.signal_summary(empty), dict)
    assert isinstance(dashboard_summaries.evaluation_summary(empty), dict)
    assert isinstance(dashboard_summaries.prediction_calibration_summary(None, empty), dict)
    assert isinstance(dashboard_summaries.narrative_reliability_summary(None, empty), dict)
    assert isinstance(dashboard_summaries.transaction_cost_summary(empty, None), dict)
    assert isinstance(dashboard_summaries.audit_report_summary(""), dict)


# === 統合レイヤーのキーが維持されている (機能変更なしの担保) ===

def test_integration_layer_keys_preserved():
    pc = dashboard_summaries.prediction_calibration_summary(
        {"calibration_status": "tracking", "scored_n": 5}, pd.DataFrame()
    )
    assert pc["available"] is True and pc["calibration_status"] == "tracking"
    tc = dashboard_summaries.transaction_cost_summary(pd.DataFrame(), {"_meta": {"status": "unconfigured"}})
    assert tc["cost_model_status"] == "unconfigured"
