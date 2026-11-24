"""Codex review gate（.github/workflows/pr_review_gate.yml）を、実物の手順を走らせて確かめる。

2026-11-24: ゲートは「指摘なし」のレビューを「レビュー未着」と取り違えていた。Codex は指摘が無いとき
レビューを作らず、要約コメントを completed・指摘なしに書き換えるだけなので、reviews API しか見ない
ゲートは20分待って「未着のまま通過(fail-open)」と書いた。9/6〜11/24 にマージされた73本のうち68本に黄色が付き、
要約の状態が残っている範囲では 33本が実際はレビュー済み・指摘なしだった。
逆に、修正を push したあとの head は誰にも読まれないまま通っていた（push では Codex は動かない）。
ゲートが自分で依頼を書く方式は PR #230 で実際に試して働かないと分かった（Codex は github-actions[bot] の依頼を
読まない）ので入れていない。時間切れで通すときの通知を「誰も頼んでいない」「読み始めたが終わらなかった」
「動くはずなのに来なかった」の3つに分けた。

2026-11-25: 同じ head に前の回のレビュー（指摘は解決済み）が残っていると、Codex が読み直している最中でも
「レビュー到着・未解決ゼロ」でその場で通っていた。読み直しの結果はマージの後に届く。読んでいる最中は通さず、
未解決は数えて覚えておくようにした（末尾の「同じ head の読み直し」）。

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
PUSHED_AT = "2026-11-24T13:15:34Z"
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
    # ゲートは PR に依頼のコメントを書かない（Codex は github-actions[bot] の依頼を読まない）。書こうとしたら落とす。
    echo "the gate must not post review requests: $args" >&2; exit 9 ;;
  "api graphql"*)
    # 未解決スレッドを数える呼び出し。何回目かを数え、場面によって途中から数を差し替える（新しい指摘が届いた場面）。
    calls=$(( $(cat "$GATE_FIXTURES/thread_calls.txt" 2>/dev/null || echo 0) + 1 ))
    echo "$calls" > "$GATE_FIXTURES/thread_calls.txt"
    if [ -f "$GATE_FIXTURES/unresolved_late_from.txt" ] && [ "$calls" -ge "$(cat "$GATE_FIXTURES/unresolved_late_from.txt")" ]; then
      cat "$GATE_FIXTURES/unresolved_late.txt"; exit 0
    fi
    cat "$GATE_FIXTURES/unresolved.txt" 2>/dev/null || exit 1; exit 0 ;;
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
              event_action: str = "opened", pushed_at: str = PUSHED_AT,
              late_unresolved=None, unresolved_late_from: int = 0):
    """ゲートの手順を走らせる。unresolved=None は GraphQL の失敗。

    fail_comments_from=N: 要約を読む N 回目以降の呼び出しを失敗させる。
    late_comments, late_from=N: N 回目以降は late_comments を返す（Codex が読み直した場面）。
    fail_reviews_from=N: レビューを数える N 回目以降の呼び出しを失敗させる。
    event_action: この実行を起こした出来事（opened / synchronize など）。pushed_at: push の時刻。
    late_unresolved, unresolved_late_from=N: 未解決スレッドを数える N 回目以降は late_unresolved を返す
    （新しい指摘スレッドが届いた場面）。"""
    step = _step()
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
    if unresolved_late_from:
        (fixtures / "unresolved_late_from.txt").write_text("%d\n" % unresolved_late_from, encoding="utf-8")
        (fixtures / "unresolved_late.txt").write_text("%s\n" % late_unresolved, encoding="utf-8")
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
               SUMMARY_FILTER=_filter(), GATE_FIXTURES=str(fixtures), EVENT_ACTION=event_action, PUSHED_AT=pushed_at,
               GITHUB_STEP_SUMMARY=str(summary))
    # GitHub は run の手順を `bash -e` で走らせる
    out = subprocess.run(["bash", "-e", str(script)], env=env, capture_output=True, text=True, timeout=120)
    record = fixtures / "posted.txt"
    posted = record.read_text(encoding="utf-8") if record.exists() else ""
    return out, posted, (summary.read_text(encoding="utf-8") if summary.exists() else "")


def test_a_review_with_no_findings_passes_at_once_and_is_not_called_unreviewed(tmp_path):
    """誤表示だった 33本の形: レビューは無いが、要約がいまの head を completed・指摘なしと言っている。"""
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


# --------------------------------------------------------------------------- push されたあとの head
def _request(created_at: str, user_type: str = "User", login: str = "Tadaim2tk", body: str = "@codex review") -> dict:
    return {"user": {"login": login, "type": user_type}, "body": body, "created_at": created_at}


def test_old_runs_of_the_same_pull_request_are_folded_and_the_gate_writes_no_requests():
    concurrency = _workflow()["concurrency"]
    assert concurrency["cancel-in-progress"] is True
    assert concurrency["group"] == "codex-review-gate-${{ github.event.pull_request.number }}"
    # ゲートが自分で依頼を書く手順は置かない。PR #230 で試したところ、Codex は github-actions[bot] の依頼に
    # 「Codex のアカウントを作って接続してください」と返すだけで、読まなかった。
    steps = _job()["steps"]
    assert len(steps) == 1 and "-f body=" not in steps[0]["run"]


def test_a_pushed_head_that_nobody_asked_about_passes_with_a_notice_that_says_so(tmp_path):
    """push では Codex は動かない。誰も頼んでいない head を「Codex が来なかった」と書かない。"""
    out, posted, summary = _run_gate(tmp_path, reviews=0, comments=[], event_action="synchronize")
    assert out.returncode == 0, out.stdout + out.stderr
    assert "🟠" in posted and "誰もレビューに出していません" in posted and HEAD[:7] in posted
    assert "push (%s) より後に人が書いた依頼は 0 件" % PUSHED_AT in posted   # いつの push を基準にしたかを書く
    assert "レビュー未着のまま通過しました" not in posted
    assert "event=synchronize head=%s pushed_at=%s" % (HEAD, PUSHED_AT) in out.stdout
    assert "@codex" not in posted                                   # 通知の文面が Codex を呼び出さない
    assert "誰にもレビューに出されないまま通過" in summary


def test_a_pushed_head_that_someone_asked_about_keeps_the_no_show_notice(tmp_path):
    """人が頼んだのに来なかった。こちらは Codex 側の問題なので、従来の文面で通す。"""
    asked = [_request("2026-11-24T13:15:40Z")]
    out, posted, _ = _run_gate(tmp_path, reviews=0, comments=asked, event_action="synchronize")
    assert out.returncode == 0, out.stdout + out.stderr
    assert "レビュー未着のまま通過しました(fail-open)" in posted and "🟠" not in posted
    assert "@codex" not in posted


def test_requests_from_before_the_push_or_from_a_bot_do_not_count(tmp_path):
    cases = {
        "earlier": [_request("2026-11-24T13:10:00Z")],                                   # 前の head への依頼
        "bot": [_request("2026-11-24T13:16:00Z", user_type="Bot", login="github-actions[bot]")],
        "mention": [_request("2026-11-24T13:16:00Z", body="説明の中で @codex review に触れただけ")],
    }
    for name, comments in cases.items():
        (tmp_path / name).mkdir()
        out, posted, _ = _run_gate(tmp_path / name, reviews=0, comments=comments, event_action="synchronize")
        assert out.returncode == 0 and "🟠" in posted, name


def test_when_the_requests_cannot_be_read_the_gate_does_not_claim_that_nobody_asked(tmp_path):
    """依頼の有無を読めなかった（41回目＝時間切れのあとの取得が失敗）。「0 件」と言い切らず、従来の文面で通す。"""
    out, posted, _ = _run_gate(tmp_path, reviews=0, comments=[], event_action="synchronize", fail_comments_from=41)
    assert out.returncode == 0, out.stdout + out.stderr
    assert "レビュー未着のまま通過しました(fail-open)" in posted and "🟠" not in posted
    assert "review requests by people since the push: unknown" in out.stdout


def test_a_review_that_started_but_never_finished_is_not_called_unrequested(tmp_path):
    """#190・#191 の形。Codex はいまの head を読み始めている。push された head でも「誰も頼んでいない」とは書かない。"""
    reading = [_summary(HEAD, "running", None)]
    for name, action in (("pushed", "synchronize"), ("opened", "opened")):
        (tmp_path / name).mkdir()
        out, posted, summary = _run_gate(tmp_path / name, reviews=0, comments=reading, event_action=action)
        assert out.returncode == 0, name + out.stdout + out.stderr
        assert "レビュー未着のまま通過しました(fail-open)" in posted and "読み始めましたが" in posted, name
        assert "🟠" not in posted and "@codex" not in posted, name
        assert "読み始めたが20分で終わらなかった" in summary, name


def test_a_review_that_was_running_and_then_became_unreadable_is_still_not_called_unrequested(tmp_path):
    """読み始めた跡を一度見たら、その後コメントが読めなくなっても覚えている。"""
    out, posted, _ = _run_gate(tmp_path, reviews=0, comments=[_summary(HEAD, "running", None)],
                               event_action="synchronize", fail_comments_from=3)
    assert out.returncode == 0, out.stdout + out.stderr
    assert "読み始めましたが" in posted and "🟠" not in posted


def test_an_opened_pull_request_that_codex_never_reviewed_keeps_the_no_show_notice(tmp_path):
    """PR を開いたときは Codex が自分で動く場面。来なければ「未着」。"""
    out, posted, _ = _run_gate(tmp_path, reviews=0, comments=[], event_action="opened")
    assert out.returncode == 0 and "レビュー未着のまま通過しました(fail-open)" in posted and "🟠" not in posted


def test_a_pushed_head_with_a_clean_review_passes_without_any_notice(tmp_path):
    out, posted, summary = _run_gate(tmp_path, reviews=0, comments=[_summary(HEAD, "completed", False)],
                                     event_action="synchronize")
    assert out.returncode == 0 and posted == "" and "レビュー済み・指摘なし" in summary


# --------------------------------------------------------------------------- 同じ head の読み直し
REREADING = "reviewing this head again"


def test_a_reread_in_progress_is_not_overtaken_by_the_earlier_review_of_the_same_head(tmp_path):
    """同じ head に前の回のレビュー（指摘は解決済み）があり、Codex が読み直している最中。前のレビューで先に通さない。

    直す前は1周目で「レビュー到着・未解決ゼロ」として通った。--auto の予約があればそこでマージされ、
    読み直しの結果はマージの後に届く。"""
    out, posted, summary = _run_gate(tmp_path, reviews=1, unresolved="0", comments=[_summary(HEAD, "running", None)],
                                     late_comments=[_summary(HEAD, "completed", False)], late_from=3)
    assert out.returncode == 0, out.stdout + out.stderr
    assert out.stdout.count(REREADING) == 2                         # 1・2周目は待った
    assert posted == "" and "未解決指摘なし (1 review(s))" in summary  # 読み直しが指摘なしで終わってから通る


def test_a_reread_that_never_finishes_passes_as_unfinished_not_as_reviewed(tmp_path):
    """読み直しが20分で終わらない。未解決はゼロなので赤にはしないが、「レビュー済み」とも書かない。"""
    out, posted, summary = _run_gate(tmp_path, reviews=1, unresolved="0", comments=[_summary(HEAD, "running", None)])
    assert out.returncode == 0, out.stdout + out.stderr
    assert out.stdout.count(REREADING) == 40
    assert "読み始めましたが" in posted and "🟠" not in posted
    assert "still unresolved" not in out.stdout                     # 未解決は無い。赤の文面を出さない
    assert "未解決指摘なし" not in summary and "読み始めたが20分で終わらなかった" in summary


def test_unresolved_threads_stay_red_while_a_reread_is_in_progress(tmp_path):
    """前の回の指摘が未解決のまま読み直しを頼み、読み直しが終わらない。fail-open で通さない。"""
    out, posted, _ = _run_gate(tmp_path, reviews=1, unresolved="2", comments=[_summary(HEAD, "running", None)])
    assert out.returncode == 1, out.stdout + out.stderr
    assert posted == "" and "still unresolved after 20 min" in out.stdout
    # 数えられなかった場合（GraphQL の失敗）も同じ
    out2, posted2, _ = _run_gate(tmp_path / "bad", reviews=1, unresolved=None, comments=[_summary(HEAD, "running", None)])
    assert out2.returncode == 1 and posted2 == ""


def test_threads_resolved_during_a_reread_that_never_finishes_are_not_called_unresolved(tmp_path):
    """読み直しの最中に、残っていた指摘を resolve した（3周目から未解決ゼロ）。読み直しは終わらない。

    最後に数えた結果は未解決ゼロなので、「未解決が残っている」の赤にはしない。読み終えていないので緑の文面にもしない。"""
    out, posted, _ = _run_gate(tmp_path, reviews=1, unresolved="2", comments=[_summary(HEAD, "running", None)],
                               late_unresolved="0", unresolved_late_from=3)
    assert out.returncode == 0, out.stdout + out.stderr
    assert "still unresolved" not in out.stdout and "読み始めましたが" in posted
    assert out.stdout.count("unresolved finding threads: 2") == 2 and out.stdout.count(REREADING) == 38


def test_a_poll_that_cannot_read_the_summary_does_not_end_the_reread(tmp_path):
    """1周目は「読んでいる最中」と読め、2周目から要約の取得が失敗する。読めなかったことを「読み終えた」と読まない。"""
    out, posted, _ = _run_gate(tmp_path, reviews=1, unresolved="0", comments=[_summary(HEAD, "running", None)],
                               fail_comments_from=2)
    assert out.returncode == 0, out.stdout + out.stderr
    assert "no unresolved finding threads remain" not in out.stdout  # 前のレビューでは通していない
    assert out.stdout.count(REREADING) == 40 and "読み始めましたが" in posted


def test_a_reread_that_ends_with_new_findings_is_red_until_they_are_resolved(tmp_path):
    """読み直しが新しい指摘を出した。指摘スレッドが見え、要約が「指摘あり」に変わる。"""
    out, posted, _ = _run_gate(tmp_path, reviews=1, unresolved="0", comments=[_summary(HEAD, "running", None)],
                               late_comments=[_summary(HEAD, "completed", True)], late_from=3,
                               late_unresolved="1", unresolved_late_from=3)
    assert out.returncode == 1, out.stdout + out.stderr
    assert posted == "" and "still unresolved after 20 min" in out.stdout
    assert out.stdout.count(REREADING) == 2
    # その指摘を resolve して再実行すれば通る（要約は「指摘あり」のまま。前からの手順）
    ok, posted_ok, summary_ok = _run_gate(tmp_path / "ok", reviews=2, unresolved="0",
                                          comments=[_summary(HEAD, "completed", True)])
    assert ok.returncode == 0 and posted_ok == "" and "未解決指摘なし (2 review(s))" in summary_ok
    assert REREADING not in ok.stdout                               # 読み直しの最中ではないので、待たない


def test_findings_from_a_reread_that_are_resolved_pass_within_the_same_run(tmp_path):
    """読み直しが「指摘あり」で終わり（3周目）、その指摘が同じ周回までに resolve されていた。再実行を待たせずに通る。

    結論が「指摘あり」に変わっても「読んでいる最中」のままにしていると、未解決ゼロでも待ち続け、時間切れで赤になる。"""
    out, posted, summary = _run_gate(tmp_path, reviews=1, unresolved="1", comments=[_summary(HEAD, "running", None)],
                                     late_comments=[_summary(HEAD, "completed", True)], late_from=3,
                                     late_unresolved="0", unresolved_late_from=3)
    assert out.returncode == 0, out.stdout + out.stderr
    assert out.stdout.count("unresolved finding threads: 1") == 2   # 1・2周目は未解決が残っていた
    assert posted == "" and "未解決指摘なし (1 review(s))" in summary and REREADING not in out.stdout


def test_new_threads_that_show_before_the_summary_changes_are_not_missed(tmp_path):
    """実際に見た順番: Codex は結果（レビュー）を先に置き、2〜3秒あとで要約を書き換える。

    3周目に新しい指摘スレッドが見え、要約は4周目に「指摘あり」へ変わる。その隙間の周回でも通さない。"""
    out, posted, _ = _run_gate(tmp_path, reviews=1, unresolved="0", comments=[_summary(HEAD, "running", None)],
                               late_comments=[_summary(HEAD, "completed", True)], late_from=4,
                               late_unresolved="1", unresolved_late_from=3)
    assert out.returncode == 1, out.stdout + out.stderr
    assert posted == "" and "still unresolved after 20 min" in out.stdout


def test_a_first_review_in_progress_still_waits_and_then_passes_when_it_ends_clean(tmp_path):
    """読み直しではなく最初のレビュー（前の回のレビューは無い）。動きは変わらない: 待って、指摘なしで終われば通る。"""
    out, posted, summary = _run_gate(tmp_path, reviews=0, comments=[_summary(HEAD, "running", None)],
                                     late_comments=[_summary(HEAD, "completed", False)], late_from=3)
    assert out.returncode == 0, out.stdout + out.stderr
    assert posted == "" and "レビュー済み・指摘なし" in summary
    assert REREADING not in out.stdout and out.stdout.count("waiting for Codex review") == 2
