"""Codex review gate（.github/workflows/pr_review_gate.yml）を、実物の手順を走らせて確かめる。

2026-11-24: ゲートは「指摘なし」のレビューを「レビュー未着」と取り違えていた。Codex は指摘が無いとき
レビューを作らず、要約コメントを completed・指摘なしに書き換えるだけなので、reviews API しか見ない
ゲートは20分待って「未着のまま通過(fail-open)」と書いた。9/6〜11/24 にマージされた73本のうち68本に黄色が付き、
要約の状態が残っている範囲では 33本が実際はレビュー済み・指摘なしだった。
逆に、修正を push したあとの head は誰にも読まれないまま通っていた（push では Codex は動かない）ので、
ゲートが自分で `@codex review` と書くようにした（頼む手順）。

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


def _workflow() -> dict:
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def _job() -> dict:
    return _workflow()["jobs"]["wait-for-codex-review"]


def _filter() -> str:
    return _job()["env"]["SUMMARY_FILTER"]


def _step() -> dict:
    """待つ手順。"""
    steps = [st for st in _job()["steps"] if st["name"].startswith("Wait for Codex review")]
    assert len(steps) == 1
    return steps[0]


def _ask_step() -> dict:
    """頼む手順。"""
    steps = [st for st in _job()["steps"] if st.get("id") == "ask"]
    assert len(steps) == 1
    return steps[0]


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
    out = subprocess.run(["jq", "-rs", "--arg", "head", head, _filter()],
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
  *"/issues/"*"/comments -f body="*)
    # レビューの依頼（POST）。失敗させる場面では何も記録しない。
    if [ -f "$GATE_FIXTURES/ask_fails.txt" ]; then echo "HTTP 403" >&2; exit 1; fi
    printf '%s\n' "$args" >> "$GATE_FIXTURES/asked.txt"; exit 0 ;;
  *"/pulls/"*"--jq .head.sha"*)
    # PR のいまの head。呼ぶたびに live_head.txt の次の行を返す（最後の行は繰り返す）。
    calls=$(( $(cat "$GATE_FIXTURES/head_calls.txt" 2>/dev/null || echo 0) + 1 ))
    echo "$calls" > "$GATE_FIXTURES/head_calls.txt"
    total=$(wc -l < "$GATE_FIXTURES/live_head.txt")
    [ "$calls" -gt "$total" ] && calls=$total
    sed -n "${calls}p" "$GATE_FIXTURES/live_head.txt"; exit 0 ;;
  "api graphql"*) cat "$GATE_FIXTURES/unresolved.txt" 2>/dev/null || exit 1; exit 0 ;;
  *"/pulls/"*"/reviews"*)
    calls=$(( $(cat "$GATE_FIXTURES/review_calls.txt" 2>/dev/null || echo 0) + 1 ))
    echo "$calls" > "$GATE_FIXTURES/review_calls.txt"
    # N 回目以降は reviews の取得が失敗する場面（本物の gh は何も出さずに終わる。手順側の awk が 0 にする）
    if [ -f "$GATE_FIXTURES/reviews_fail_from.txt" ] && [ "$calls" -ge "$(cat "$GATE_FIXTURES/reviews_fail_from.txt")" ]; then exit 1; fi
    cat "$GATE_FIXTURES/reviews_count.txt"; exit 0 ;;
  *"/issues/"*"/comments"*)
    if [[ "$args" == *"--jq"* ]]; then cat "$GATE_FIXTURES/quota_count.txt"; exit 0; fi
    # 要約を読む呼び出し。何回目かを数え、場面によって途中から失敗させたり、中身を差し替えたりする。
    calls=$(( $(cat "$GATE_FIXTURES/comment_calls.txt" 2>/dev/null || echo 0) + 1 ))
    echo "$calls" > "$GATE_FIXTURES/comment_calls.txt"
    if [ -f "$GATE_FIXTURES/fail_from.txt" ] && [ "$calls" -ge "$(cat "$GATE_FIXTURES/fail_from.txt")" ]; then exit 1; fi
    if [ -f "$GATE_FIXTURES/late_from.txt" ] && [ "$calls" -ge "$(cat "$GATE_FIXTURES/late_from.txt")" ]; then
      cat "$GATE_FIXTURES/comments_late.json"; exit 0
    fi
    cat "$GATE_FIXTURES/comments.json"
    exit 0 ;;
esac
echo "unexpected gh call: $args" >&2
exit 9
"""


def _run_gate(tmp_path: Path, *, reviews: int = 0, comments=(), unresolved="0", quota: int = 0, head: str = HEAD,
              fail_comments_from: int = 0, late_comments=None, late_from: int = 0, fail_reviews_from: int = 0,
              step=None, live_heads=(HEAD,), ask_fails: bool = False, ask_outcome: str = "skipped"):
    """ゲートの手順を走らせる（既定は待つ手順。step=_ask_step() で頼む手順）。unresolved=None は GraphQL の失敗。

    fail_comments_from=N: 要約を読む N 回目以降の呼び出しを失敗させる。
    late_comments, late_from=N: N 回目以降は late_comments を返す（Codex が読み直した場面）。
    fail_reviews_from=N: レビューを数える N 回目以降の呼び出しを失敗させる。
    live_heads: PR のいまの head を聞かれるたびに順に返す値。ask_fails: 依頼の POST を失敗させる。
    ask_outcome: 待つ手順へ渡す、頼む手順の結果（success / failure / skipped）。
    戻り値の posted は、待つ手順なら PR に書いた通知、頼む手順なら依頼の POST。"""
    asking = step is not None and step.get("id") == "ask"
    step = step or _step()
    fixtures = tmp_path / "fixtures"
    fixtures.mkdir()
    (fixtures / "reviews_count.txt").write_text("%d\n" % reviews, encoding="utf-8")
    (fixtures / "quota_count.txt").write_text("%d\n" % quota, encoding="utf-8")
    (fixtures / "comments.json").write_text(json.dumps(list(comments)), encoding="utf-8")
    if unresolved is not None:
        (fixtures / "unresolved.txt").write_text("%s\n" % unresolved, encoding="utf-8")
    if fail_comments_from:
        (fixtures / "fail_from.txt").write_text("%d\n" % fail_comments_from, encoding="utf-8")
    if fail_reviews_from:
        (fixtures / "reviews_fail_from.txt").write_text("%d\n" % fail_reviews_from, encoding="utf-8")
    (fixtures / "live_head.txt").write_text("".join("%s\n" % h for h in live_heads), encoding="utf-8")
    if ask_fails:
        (fixtures / "ask_fails.txt").write_text("1\n", encoding="utf-8")
    if late_from:
        (fixtures / "late_from.txt").write_text("%d\n" % late_from, encoding="utf-8")
        (fixtures / "comments_late.json").write_text(json.dumps(list(late_comments or [])), encoding="utf-8")
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
               SUMMARY_FILTER=_filter(), GATE_FIXTURES=str(fixtures), ASK_OUTCOME=ask_outcome,
               GITHUB_STEP_SUMMARY=str(summary))
    # GitHub は run の手順を `bash -e` で走らせる
    out = subprocess.run(["bash", "-e", str(script)], env=env, capture_output=True, text=True, timeout=120)
    record = fixtures / ("asked.txt" if asking else "posted.txt")
    posted = record.read_text(encoding="utf-8") if record.exists() else ""
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


def test_findings_seen_once_are_not_forgotten_when_a_later_poll_cannot_read_the_summary(tmp_path):
    """39回は「指摘あり」と読め、最後の1回だけ取得に失敗する。指摘を見たあとで fail-open にしない（#229 Codex P2）。"""
    out, posted, _ = _run_gate(tmp_path, reviews=0, comments=[_summary(HEAD, "completed", True)], fail_comments_from=40)
    assert out.returncode == 1, out.stdout + out.stderr
    assert posted == ""                                             # 「未着のまま通過」を書かない
    assert "指摘があると報告" in out.stdout
    assert "cannot be read now" in out.stdout                       # 最後の周は読めなかった


def test_findings_seen_once_do_not_open_the_quota_door_either(tmp_path):
    """指摘を見たあとで要約が読めなくなり、枠切れの通知だけが残っている場面。枠切れの文面で通さない。"""
    out, posted, _ = _run_gate(tmp_path, reviews=0, comments=[_summary(HEAD, "completed", True)],
                               fail_comments_from=2, quota=1)
    assert out.returncode == 1 and posted == ""


def test_a_review_seen_once_keeps_the_quota_door_shut_when_later_polls_fail(tmp_path):
    """1周目にレビュー（未解決2件）を見た。2周目からレビューの取得が失敗し、枠切れの通知だけが読める場面。

    修正前は、レビューが数えられない周に枠切れの道へ入り、未解決の指摘を残したまま緑で通った。"""
    out, posted, _ = _run_gate(tmp_path, reviews=1, unresolved="2", quota=1, fail_reviews_from=2)
    assert out.returncode == 1, out.stdout + out.stderr
    assert posted == ""                                             # 枠切れの文面でも、未着の文面でも通さない
    assert "still unresolved after 20 min" in out.stdout
    assert "cannot be read now" in out.stdout


def test_findings_are_superseded_only_by_a_verified_clean_result(tmp_path):
    """Codex が同じ head を読み直して指摘なしになった場面。確かめられたら通る。"""
    out, posted, summary = _run_gate(tmp_path, reviews=0, comments=[_summary(HEAD, "completed", True)],
                                     late_comments=[_summary(HEAD, "completed", False)], late_from=3)
    assert out.returncode == 0, out.stdout + out.stderr
    assert posted == "" and "レビュー済み・指摘なし" in summary
    # 読み直しの途中（running）のまま時間切れなら、赤のまま
    out2, posted2, _ = _run_gate(tmp_path / "ok", reviews=0, comments=[_summary(HEAD, "completed", True)],
                                 late_comments=[_summary(HEAD, "running", None)], late_from=3)
    assert out2.returncode == 1 and posted2 == ""


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


# --------------------------------------------------------------------------- 頼む手順（push のあとの head）
def test_the_gate_asks_only_on_a_push_to_a_ready_pull_request_and_old_runs_are_folded():
    ask = _ask_step()
    condition = " ".join(ask["if"].split())
    assert condition == "github.event.action == 'synchronize' && github.event.pull_request.draft == false"
    assert ask["continue-on-error"] is True                      # 頼めなくても待つ側は動かす
    job = _job()
    assert [st.get("id") for st in job["steps"]][0] == "ask"      # 頼んでから待つ
    assert _step()["env"]["ASK_OUTCOME"] == "${{ steps.ask.outcome }}"
    concurrency = _workflow()["concurrency"]
    assert concurrency["cancel-in-progress"] is True
    assert concurrency["group"] == "codex-review-gate-${{ github.event.pull_request.number }}"


def test_a_pushed_head_nobody_has_read_gets_exactly_one_request(tmp_path):
    out, asked, _ = _run_gate(tmp_path, step=_ask_step(), reviews=0, comments=[_summary(OTHER, "completed", False)])
    assert out.returncode == 0, out.stdout + out.stderr
    assert asked.count("-f body=@codex review") == 1 and "issues/228/comments" in asked
    assert "asked Codex to review" in out.stdout


def test_no_request_when_this_head_is_already_reviewed_or_being_reviewed(tmp_path):
    cases = {
        "review": dict(reviews=1, comments=[]),
        "clean": dict(reviews=0, comments=[_summary(HEAD, "completed", False)]),
        "findings": dict(reviews=0, comments=[_summary(HEAD, "completed", True)]),
        "running": dict(reviews=0, comments=[_summary(HEAD, "running", None)]),
    }
    for name, kwargs in cases.items():
        (tmp_path / name).mkdir()
        out, asked, _ = _run_gate(tmp_path / name, step=_ask_step(), **kwargs)
        assert out.returncode == 0 and asked == "", name       # 同じ head を二度読ませない
        assert "not asking again" in out.stdout, name


def test_an_outdated_run_does_not_ask_for_the_newer_head(tmp_path):
    """依頼のコメントはコミットを名指さない。古い実行が頼むと、最新の head が読まれてしまう。"""
    (tmp_path / "first").mkdir()
    out, asked, _ = _run_gate(tmp_path / "first", step=_ask_step(), live_heads=(OTHER,))
    assert out.returncode == 0 and asked == "" and "the newer run owns the request" in out.stdout
    # 最初の確認のあと、頼む直前までに head が動いた場合も頼まない
    (tmp_path / "second").mkdir()
    out2, asked2, _ = _run_gate(tmp_path / "second", step=_ask_step(), live_heads=(HEAD, OTHER))
    assert out2.returncode == 0 and asked2 == "" and "while checking" in out2.stdout


def test_a_request_that_cannot_be_posted_fails_the_ask_step_and_then_the_gate(tmp_path):
    """頼めなかった回は「レビューが来なかった」ではなく「レビューを求めていない」。fail-open にしない。"""
    (tmp_path / "ask").mkdir()
    out, asked, _ = _run_gate(tmp_path / "ask", step=_ask_step(), ask_fails=True)
    assert out.returncode != 0 and asked == ""                  # outcome=failure として待つ手順へ渡る
    (tmp_path / "wait").mkdir()
    waited, posted, _ = _run_gate(tmp_path / "wait", reviews=0, comments=[], ask_outcome="failure")
    assert waited.returncode == 1 and posted == ""              # 黄色い通知で通さない
    assert "レビューを頼めなかった" in waited.stdout
    # 頼めなくても、レビューが届いていれば（誰かが手で頼んだ）通る
    (tmp_path / "manual").mkdir()
    ok, posted_ok, _ = _run_gate(tmp_path / "manual", reviews=0, comments=[_summary(HEAD, "completed", False)],
                                 ask_outcome="failure")
    assert ok.returncode == 0 and posted_ok == ""


def test_after_a_successful_request_an_unanswered_wait_still_fails_open_with_the_notice(tmp_path):
    """頼んだのに Codex が来なかった（Codex 側が止まっている）。これは従来どおり黄色で通す。"""
    out, posted, _ = _run_gate(tmp_path, reviews=0, comments=[], ask_outcome="success")
    assert out.returncode == 0 and "レビュー未着のまま通過しました(fail-open)" in posted

