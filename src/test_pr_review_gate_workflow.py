"""Codex review gate（.github/workflows/pr_review_gate.yml）を、実物の手順を走らせて確かめる。

2026-11-24: ゲートは「指摘なし」のレビューを「レビュー未着」と取り違えていた。Codex は指摘が無いとき
レビューを作らず、要約コメントを completed・指摘なしに書き換えるだけなので、reviews API しか見ない
ゲートは20分待って「未着のまま通過(fail-open)」と書いた。11/15〜11/23 にマージされた12本がこの形だった。

ここでは YAML から手順（run）と jq の式（SUMMARY_FILTER）を取り出し、`gh` と `sleep` だけを偽物に差し替えて
そのまま bash で走らせる。文字列を眺める試験ではなく、終了コードと PR に書く文面を見る。
"""
from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "pr_review_gate.yml"
HEAD = "7a69789738397e2bd6f6fb7383c47319c4fe4dc3"
OTHER = "f" * 40
BOT = {"login": "chatgpt-codex-connector[bot]", "type": "Bot"}

pytestmark = pytest.mark.skipif(shutil.which("jq") is None or shutil.which("bash") is None,
                                reason="jq と bash が要る")


def _step() -> dict:
    parsed = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    return parsed["jobs"]["wait-for-codex-review"]["steps"][0]


def _summary(sha: str, status, findings, user: dict = BOT) -> dict:
    """Codex の要約コメント（2026-11 の実物と同じ形）。"""
    state = {"code_review": {"commit_sha": sha, "has_any_findings": findings,
                             "has_unresolved_findings": findings, "status": status},
             "security_review": {"commit_sha": None, "has_any_findings": None,
                                 "has_unresolved_findings": None, "status": None}}
    body = ("<!-- codex-pull-request-review-summary -->\n"
            "<!-- codex-review-state:v1 %s -->\n\n<details>\n"
            "<summary><strong>Codex Review Summary</strong>: ✅ Completed</summary>\n\n"
            "| 📝 **Code Review** | ✅ **Completed** | `%s` | PR opened |\n</details>\n"
            % (json.dumps(state, separators=(",", ":")), sha[:7]))
    return {"user": user, "body": body}


def _state(pages, head: str = HEAD) -> str:
    """SUMMARY_FILTER を実物の文字列のまま jq に渡す。pages はページごとのコメント配列。"""
    stdin = "\n".join(json.dumps(page) for page in pages)
    out = subprocess.run(["jq", "-rs", "--arg", "head", head, _step()["env"]["SUMMARY_FILTER"]],
                         input=stdin, capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    return out.stdout.strip()


# --------------------------------------------------------------------------- 要約コメントの読み方
def test_summary_for_the_current_head_is_read_as_clean_findings_or_running():
    assert _state([[_summary(HEAD, "completed", False)]]) == "clean"
    assert _state([[_summary(HEAD, "completed", True)]]) == "findings"
    assert _state([[_summary(HEAD, "running", None)]]) == "running"
    assert _state([[_summary(HEAD, "queued", None)]]) == "running"
    # 結論が無いものを clean にしない
    assert _state([[_summary(HEAD, "completed", None)]]) == "running"
    assert _state([[_summary(HEAD, "failed", False)]]) == "running"


def test_summary_that_does_not_speak_for_this_head_or_this_bot_is_none():
    assert _state([[]]) == "none"
    assert _state([]) == "none"                                              # コメントが1ページも無い
    assert _state([[_summary(OTHER, "completed", False)]]) == "none"         # 別のコミットのレビュー
    assert _state([[_summary(HEAD[:7], "completed", False)]]) == "none"      # 短い SHA は一致とみなさない
    human = {"login": "chatgpt-codex-connector[bot]", "type": "User"}
    assert _state([[_summary(HEAD, "completed", False, user=human)]]) == "none"
    other_bot = {"login": "github-actions[bot]", "type": "Bot"}
    assert _state([[_summary(HEAD, "completed", False, user=other_bot)]]) == "none"
    # 目印の無いコメント、JSON が壊れた要約、JSON の形が違う要約
    quoted = {"user": BOT, "body": 'codex-review-state:v1 {"code_review":{"commit_sha":"%s","has_any_findings":false,"status":"completed"}} -->' % HEAD}
    assert _state([[quoted]]) == "none"
    broken = {"user": BOT, "body": "<!-- codex-pull-request-review-summary -->\n<!-- codex-review-state:v1 {\"code_review\": -->"}
    assert _state([[broken]]) == "none"
    odd = {"user": BOT, "body": "<!-- codex-pull-request-review-summary -->\n<!-- codex-review-state:v1 {\"code_review\":\"completed\"} -->"}
    assert _state([[odd]]) == "none"
    assert _state([[{"user": None, "body": None}]]) == "none"


def test_summary_is_found_on_a_later_page_and_findings_win_over_clean():
    filler = [{"user": {"login": "someone", "type": "User"}, "body": "x"}] * 3
    assert _state([filler, [_summary(HEAD, "completed", False)]]) == "clean"
    assert _state([[_summary(HEAD, "completed", False)], [_summary(HEAD, "completed", True)]]) == "findings"


# --------------------------------------------------------------------------- 手順をそのまま走らせる
GH_STUB = r"""#!/usr/bin/env bash
# 偽の gh。場面ごとの答えを $GATE_FIXTURES のファイルから返す。
args="$*"
case "$args" in
  "pr comment"*) printf '%s\n' "$args" >> "$GATE_FIXTURES/posted.txt"; exit 0 ;;
  "api graphql"*) cat "$GATE_FIXTURES/unresolved.txt" 2>/dev/null || exit 1; exit 0 ;;
  *"/pulls/"*"/reviews"*) cat "$GATE_FIXTURES/reviews_count.txt"; exit 0 ;;
  *"/issues/"*"/comments"*)
    if [[ "$args" == *"--jq"* ]]; then cat "$GATE_FIXTURES/quota_count.txt"; else cat "$GATE_FIXTURES/comments.json"; fi
    exit 0 ;;
esac
echo "unexpected gh call: $args" >&2
exit 9
"""


def _run_gate(tmp_path: Path, *, reviews: int = 0, comments=(), unresolved="0", quota: int = 0, head: str = HEAD):
    """ゲートの手順を走らせる。unresolved=None は GraphQL の失敗。"""
    step = _step()
    fixtures = tmp_path / "fixtures"
    fixtures.mkdir()
    (fixtures / "reviews_count.txt").write_text("%d\n" % reviews, encoding="utf-8")
    (fixtures / "quota_count.txt").write_text("%d\n" % quota, encoding="utf-8")
    (fixtures / "comments.json").write_text(json.dumps(list(comments)), encoding="utf-8")
    if unresolved is not None:
        (fixtures / "unresolved.txt").write_text("%s\n" % unresolved, encoding="utf-8")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name, body in (("gh", GH_STUB), ("sleep", "#!/usr/bin/env bash\nexit 0\n")):
        path = bin_dir / name
        path.write_text(body, encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    script = tmp_path / "step.sh"
    script.write_text(step["run"], encoding="utf-8")
    summary = tmp_path / "step_summary.md"
    env = dict(os.environ, PATH="%s%s%s" % (bin_dir, os.pathsep, os.environ["PATH"]),
               GH_TOKEN="x", PR="228", REPO="owner/repo", HEAD_SHA=head,
               SUMMARY_FILTER=step["env"]["SUMMARY_FILTER"], GATE_FIXTURES=str(fixtures),
               GITHUB_STEP_SUMMARY=str(summary))
    # GitHub は run の手順を `bash -e` で走らせる
    out = subprocess.run(["bash", "-e", str(script)], env=env, capture_output=True, text=True, timeout=120)
    posted = (fixtures / "posted.txt").read_text(encoding="utf-8") if (fixtures / "posted.txt").exists() else ""
    return out, posted, (summary.read_text(encoding="utf-8") if summary.exists() else "")


def test_a_review_with_no_findings_passes_at_once_and_is_not_called_unreviewed(tmp_path):
    """11/15〜11/23 の12本の形: レビューは無いが、要約がいまの head を completed・指摘なしと言っている。"""
    out, posted, summary = _run_gate(tmp_path, reviews=0, comments=[_summary(HEAD, "completed", False)])
    assert out.returncode == 0, out.stdout + out.stderr
    assert posted == ""                                             # 「未着のまま通過」を書かない
    assert "レビュー済み・指摘なし" in summary and "未着" not in summary
    assert "waiting for Codex review" not in out.stdout             # 20分待たない（1周目で通る）


def test_no_review_and_no_summary_still_fails_open_with_the_yellow_notice(tmp_path):
    out, posted, summary = _run_gate(tmp_path, reviews=0, comments=[])
    assert out.returncode == 0, out.stdout + out.stderr
    assert "レビュー未着のまま通過しました(fail-open)" in posted
    assert "未着のまま通過" in summary
    assert out.stdout.count("waiting for Codex review") == 40       # 最後まで待った


def test_a_clean_summary_for_another_commit_is_not_taken_as_a_review_of_this_head(tmp_path):
    out, posted, _ = _run_gate(tmp_path, reviews=0, comments=[_summary(OTHER, "completed", False)])
    assert out.returncode == 0
    assert "レビュー未着のまま通過しました(fail-open)" in posted       # いまの head は誰も読んでいない


def test_a_summary_reporting_findings_without_a_visible_review_fails_closed(tmp_path):
    """指摘があると分かっている PR を fail-open で通さない（#162 で起きた形）。"""
    out, posted, _ = _run_gate(tmp_path, reviews=0, comments=[_summary(HEAD, "completed", True)])
    assert out.returncode == 1, out.stdout + out.stderr
    assert posted == ""
    assert "指摘があると報告" in out.stdout


def test_a_review_object_keeps_the_existing_rule_of_zero_unresolved_threads(tmp_path):
    ok, posted_ok, summary_ok = _run_gate(tmp_path / "ok", reviews=1, unresolved="0")
    assert ok.returncode == 0 and posted_ok == "" and "未解決指摘なし (1 review(s))" in summary_ok
    bad, posted_bad, _ = _run_gate(tmp_path / "bad", reviews=1, unresolved="2")
    assert bad.returncode == 1 and posted_bad == ""
    assert "still unresolved after 20 min" in bad.stdout


def test_a_clean_summary_does_not_hide_unresolved_threads_from_earlier_commits(tmp_path):
    out, posted, _ = _run_gate(tmp_path, reviews=0, comments=[_summary(HEAD, "completed", False)], unresolved="1")
    assert out.returncode == 1 and posted == ""
    assert "still unresolved after 20 min" in out.stdout


def test_a_clean_summary_does_not_pass_when_the_threads_cannot_be_counted(tmp_path):
    out, posted, _ = _run_gate(tmp_path, reviews=0, comments=[_summary(HEAD, "completed", False)], unresolved=None)
    assert out.returncode == 1 and posted == ""                     # GraphQL が落ちたら緑にしない


def test_quota_notice_still_passes_at_once_with_its_own_wording(tmp_path):
    out, posted, summary = _run_gate(tmp_path, reviews=0, comments=[], quota=1)
    assert out.returncode == 0
    assert "レビュー枠切れのまま通過しました(fail-open)" in posted and "未着" not in posted
    assert "枠切れ" in summary


@pytest.fixture(autouse=True)
def _each_case_gets_its_own_directory(tmp_path):
    for name in ("ok", "bad"):
        (tmp_path / name).mkdir()
