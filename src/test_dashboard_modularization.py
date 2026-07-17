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


def test_build_dashboard_has_main_entrypoint():
    # 回帰防止: 分割時に __main__ ガードが脱落すると `python build_dashboard.py` が
    # 何も生成せず exit 0 になり、Pages artifact の tar が失敗する。
    source = (Path(__file__).parent / "build_dashboard.py").read_text(encoding="utf-8")
    assert 'if __name__ == "__main__":' in source
    assert "raise SystemExit(main())" in source


def test_main_actually_generates_outputs(tmp_path, monkeypatch):
    # main() を実行して実際に index.html / dashboard_summary.json が生成されることを保証する
    # (出力先を一時ディレクトリへ差し替え、リポジトリの成果物を汚さない)。
    import dashboard_io
    out_dir = tmp_path / "dashboard"
    monkeypatch.setattr(bd, "REPORTS_DIR", out_dir, raising=False)
    monkeypatch.setattr(dashboard_io, "REPORTS_DIR", out_dir, raising=False)
    rc = bd.main()
    assert rc == 0
    assert (out_dir / "index.html").exists()
    assert (out_dir / "dashboard_summary.json").exists()
    html_text = (out_dir / "index.html").read_text(encoding="utf-8")
    # 2026-07-17 再設計: サービスの一次面は「台帳の今日の判断 → 答え合わせ → 成績」。
    # 全セクションは温存されるが、内部データは details.group に折りたたむ。
    for section in [
        "予測ノートの成績",
        "監査レポート",
        "準備中の分析(データが貯まると自動で動き出します)",
        "確信度と的中率のズレ(キャリブレーション)",
        "ニュース解釈の信頼性",
        "取引コストモデル",
        "前営業日の答え合わせ",
        "見送り(NO_TRADE)",
    ]:
        assert f"<h2>{section}</h2>" in html_text, section
    # 一次面の契約: 状態ピル・今日の判断・成績(チャート)は折りたたみの外にある
    assert 'class="pills"' in html_text
    assert 'id="today"' in html_text and 'id="perf"' in html_text
    assert 'class="chart"' in html_text  # 累積R/地平線勝率のSVG
    first_group = html_text.index('<details class="group"')
    assert html_text.index('id="today"') < first_group
    assert html_text.index('id="perf"') < first_group
    assert html_text.index('id="exec"') < first_group  # 執行ビューも一次面
    # 台帳が読めた場合の判断カード(この統合テストは実データで走る)
    assert 'class="jgrid"' in html_text or "方向つき判断はありません" in html_text or "台帳(data/signal_log.csv)が読めません" in html_text


# === 空データでもサマリー関数が落ちない ===

def test_summaries_handle_empty_data():
    empty = pd.DataFrame()
    assert isinstance(dashboard_summaries.signal_summary(empty), dict)
    assert isinstance(dashboard_summaries.evaluation_summary(empty), dict)
    assert isinstance(dashboard_summaries.prediction_calibration_summary(None, empty), dict)
    assert isinstance(dashboard_summaries.narrative_reliability_summary(None, empty), dict)
    assert isinstance(dashboard_summaries.transaction_cost_summary(empty, None), dict)
    assert isinstance(dashboard_summaries.audit_report_summary(""), dict)
    assert isinstance(dashboard_summaries.todays_judgements_summary(empty, empty), dict)
    assert isinstance(dashboard_summaries.performance_series_summary(empty, empty), dict)
    assert isinstance(dashboard_summaries.execution_view_summary(empty, empty), dict)
    assert isinstance(dashboard_summaries.execution_sim_summary(empty), dict)


# === 統合レイヤーのキーが維持されている (機能変更なしの担保) ===

def test_integration_layer_keys_preserved():
    pc = dashboard_summaries.prediction_calibration_summary(
        {"calibration_status": "tracking", "scored_n": 5}, pd.DataFrame()
    )
    assert pc["available"] is True and pc["calibration_status"] == "tracking"
    tc = dashboard_summaries.transaction_cost_summary(pd.DataFrame(), {"_meta": {"status": "unconfigured"}})
    assert tc["cost_model_status"] == "unconfigured"
