# -*- coding: utf-8 -*-
"""レビューゲートの判定。**架空のコメントだけで試す。** 通信もリポジトリも要らない。

#162 で実際に起きたことを再現する回帰試験を含む。Codexが指摘を issue comment で
出したのに、ゲートは reviews API しか見ずに「未着」と判定して緑にした。
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
from codex_review_state import classify                          # noqa: E402

HEAD = "a" * 40
OLD = "b" * 40
BOT = {"login": "codex-bot-placeholder", "type": "Bot"}


def _bot(body):
    return {"user": {"login": "chatgpt-codex-connector[bot]", "type": "Bot"},
            "author_association": "NONE", "body": body}


def _human(body, role="OWNER"):
    return {"user": {"login": "example-maintainer", "type": "User"},
            "author_association": role, "body": body}


def _summary(sha, status="✅ **Completed**"):
    return _bot("<!-- codex-pull-request-review-summary -->\n\n"
                "| Review | Status | Commit | Review trigger |\n"
                "| --- | --- | --- | --- |\n"
                "| 📝 **Code Review** | %s | `%s` | PR opened |\n" % (status, sha[:7]))


def _finding(sha, title="Example finding"):
    return _bot("\n### 💡 Codex Review\n\n"
                "https://github.com/example/example/blob/%s/data/example.csv#L1\n"
                "**![P2 Badge]  %s**\n\nExample body.\n" % (sha, title))


def test_issue_comment_finding_blocks():
    """#162 の再現。指摘は issue comment で来る。reviews API は空。**緑にしない。**"""
    state, _ = classify(HEAD, [_summary(HEAD), _finding(HEAD)],
                        reviews_for_head=0, unresolved_threads=0)
    assert state == "findings"


def test_completed_summary_without_findings_is_clean():
    state, _ = classify(HEAD, [_summary(HEAD)], reviews_for_head=0, unresolved_threads=0)
    assert state == "clean"


def test_old_clean_summary_does_not_pass_new_commit():
    """前のコミットの「問題なし」で、いまの変更を緑にしない。"""
    state, _ = classify(HEAD, [_summary(OLD)], reviews_for_head=0, unresolved_threads=0)
    assert state == "pending"


def test_finding_on_old_commit_does_not_block():
    """直したあとの新しいコミットを、古い指摘で赤にしない。"""
    state, _ = classify(HEAD, [_summary(HEAD), _finding(OLD)],
                        reviews_for_head=0, unresolved_threads=0)
    assert state == "clean"


def test_quota_is_its_own_state():
    state, _ = classify(HEAD, [_bot("Codex has hit usage limits for code reviews.")],
                        reviews_for_head=0, unresolved_threads=0)
    assert state == "quota"


def test_nothing_yet_is_pending():
    state, _ = classify(HEAD, [], reviews_for_head=0, unresolved_threads=0)
    assert state == "pending"


def test_running_summary_is_pending_not_clean():
    state, _ = classify(HEAD, [_summary(HEAD, "⏳ **Running**")],
                        reviews_for_head=0, unresolved_threads=0)
    assert state == "pending"


def test_failed_review_is_undecidable_not_clean():
    """異常終了は「未着」ではない。結論が無いので緑にしない。"""
    state, _ = classify(HEAD, [_summary(HEAD, "❌ **Failed**")],
                        reviews_for_head=0, unresolved_threads=0)
    assert state == "undecidable"


def test_unreadable_status_is_undecidable():
    state, _ = classify(HEAD, [_summary(HEAD, "🟪 **Something new**")],
                        reviews_for_head=0, unresolved_threads=0)
    assert state == "undecidable"


def test_unresolved_thread_count_unknown_blocks_when_review_exists():
    state, _ = classify(HEAD, [_summary(HEAD)], reviews_for_head=1, unresolved_threads=None)
    assert state == "undecidable"


def test_impostor_comment_is_ignored():
    """似た名前の投稿者を、正規のレビューとして数えない。"""
    fake = {"user": {"login": "chatgpt-codex-connector", "type": "User"},
            "author_association": "NONE",
            "body": "<!-- codex-pull-request-review-summary -->\n"
                    "| Review | Status | Commit | Review trigger |\n"
                    "| 📝 **Code Review** | ✅ **Completed** | `%s` | PR opened |\n" % HEAD[:7]}
    state, _ = classify(HEAD, [fake], reviews_for_head=0, unresolved_threads=0)
    assert state == "pending"


def test_review_thread_findings_still_block():
    state, _ = classify(HEAD, [_summary(HEAD)], reviews_for_head=1, unresolved_threads=2)
    assert state == "findings"


def test_ack_is_recorded_apart_from_clean():
    """人が飲み込んだことを「レビュー問題なし」と同じ緑にしない。"""
    assert classify(HEAD, [_summary(HEAD), _finding(HEAD),
                           _human("GATE-ACK: %s 確認済み" % HEAD)],
                    0, 0)[0] == "acked"
    assert classify(HEAD, [_summary(HEAD)], 0, 0)[0] == "clean"


def test_ack_needs_write_role_and_matching_sha():
    assert classify(HEAD, [_summary(HEAD), _finding(HEAD),
                           _human("GATE-ACK: %s" % OLD)], 0, 0)[0] == "findings"
    assert classify(HEAD, [_summary(HEAD), _finding(HEAD),
                           _human("GATE-ACK: %s" % HEAD, role="NONE")], 0, 0)[0] == "findings"


def test_bad_head_sha_is_undecidable():
    assert classify("not-a-sha", [_summary(HEAD)], 0, 0)[0] == "undecidable"
