"""全 GitHub Actions workflow が有効な YAML であることの回帰テスト。

背景 (2026-07-09): daily_cycle.yml に単一行 `run:` の plain scalar 内コロン
(`|| echo "warning: ..."`) が混入して YAML parse 不能になり、7/4〜7/8 の
日次サイクル(シグナル生成・Sheets同期・shadow台帳)が5日間停止した。
壊れた workflow は push のたびに jobs ゼロの failed run を作り、cron は黙って
止まる(false quiet)。このテストが同クラスの事故を CI 前に捕まえる。
"""

from __future__ import annotations

from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml", reason="PyYAML が無い環境ではスキップ(CIには存在)")

WORKFLOW_DIR = Path(__file__).resolve().parent.parent / ".github" / "workflows"


def test_all_workflows_parse_as_yaml():
    files = sorted(WORKFLOW_DIR.glob("*.yml")) + sorted(WORKFLOW_DIR.glob("*.yaml"))
    assert files, "workflow ファイルが見つからない"
    broken = []
    for f in files:
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            broken.append(f"{f.name}: {str(e).splitlines()[0]}")
            continue
        if not isinstance(data, dict) or ("jobs" not in data):
            broken.append(f"{f.name}: jobs キーが無い")
    assert not broken, "壊れた workflow:\n" + "\n".join(broken)


def test_no_unquoted_colon_in_single_line_run():
    # `run: ... echo "...: ..."` の単一行 plain scalar は YAML を壊す(今回の事故パターン)
    import re
    pattern = re.compile(r'^\s+run: (?!\|)(?!>)[^\n]*: ', re.MULTILINE)
    offenders = []
    for f in sorted(WORKFLOW_DIR.glob("*.yml")):
        text = f.read_text(encoding="utf-8")
        for m in pattern.finditer(text):
            line_no = text[: m.start()].count("\n") + 1
            offenders.append(f"{f.name}:{line_no}")
    assert not offenders, f"単一行 run にコロン入りscalar(要 block scalar 化): {offenders}"
