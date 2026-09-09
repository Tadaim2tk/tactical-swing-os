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


def _human(body, login="example-maintainer"):
    return {"user": {"login": login, "type": "User"},
            "author_association": "NONE", "body": body}


def _other_bot(body, login="example-other-bot"):
    return {"user": {"login": login, "type": "Bot"},
            "author_association": "MEMBER", "body": body}


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


ACK = ["example-maintainer"]


def test_ack_is_recorded_apart_from_clean():
    """人が飲み込んだことを「レビュー問題なし」と同じ緑にしない。"""
    assert classify(HEAD, [_summary(HEAD), _finding(HEAD),
                           _human("GATE-ACK: %s 確認済み" % HEAD)],
                    0, 0, ACK)[0] == "acked"
    assert classify(HEAD, [_summary(HEAD)], 0, 0, ACK)[0] == "clean"


def test_ack_needs_verified_login_and_matching_sha():
    # 別のコミット向けの承認は効かない
    assert classify(HEAD, [_summary(HEAD), _finding(HEAD),
                           _human("GATE-ACK: %s" % OLD)], 0, 0, ACK)[0] == "findings"
    # 権限を確認していない login の承認は効かない
    assert classify(HEAD, [_summary(HEAD), _finding(HEAD),
                           _human("GATE-ACK: %s" % HEAD, login="example-stranger")],
                    0, 0, ACK)[0] == "findings"
    # ack_logins を渡さなければ、承認そのものが成立しない
    assert classify(HEAD, [_summary(HEAD), _finding(HEAD),
                           _human("GATE-ACK: %s" % HEAD)], 0, 0, None)[0] == "findings"


def test_bot_cannot_ack_even_with_member_association():
    """`author_association` は書き込み権限ではない。Botに承認させない。"""
    for c in (_other_bot("GATE-ACK: %s" % HEAD),
              _other_bot("GATE-ACK: %s" % HEAD, login="example-maintainer")):
        assert classify(HEAD, [_summary(HEAD), _finding(HEAD), c],
                        0, 0, ACK)[0] == "findings"


def test_quota_does_not_override_current_findings():
    """枠切れ通知は head を持たない。**いまの指摘を古い通知で上書きしない。**"""
    cs = [_bot("Codex has hit usage limits for code reviews."),
          _summary(HEAD), _finding(HEAD)]
    assert classify(HEAD, cs, 0, 2, ACK)[0] == "findings"
    assert classify(HEAD, cs, 0, 0, ACK)[0] == "findings"
    # 未解決スレッドだけでも、枠切れより優先する
    assert classify(HEAD, [_bot("Codex has hit usage limits for code reviews.")],
                    1, 3, ACK)[0] == "findings"
    # いまの head について何も無いときだけ、枠切れが効く
    assert classify(HEAD, [_bot("Codex has hit usage limits for code reviews.")],
                    0, 0, ACK)[0] == "quota"


def test_quota_does_not_override_undecidable():
    cs = [_bot("Codex has hit usage limits for code reviews."),
          _summary(HEAD, "❌ **Failed**")]
    assert classify(HEAD, cs, 0, 0, ACK)[0] == "undecidable"


def test_stale_unreadable_summary_does_not_poison_the_current_head():
    """**古い要約が読めないというだけで、いまのコミットの結論を捨てない(#163 Codex P2)。**

    捨てると、修正を push しても永久に undecidable のままで復帰できない。
    """
    stale = _bot("<!-- codex-pull-request-review-summary -->\n\n"
                 "Code Review completed for %s (old layout, no table)\n" % OLD)
    assert classify(HEAD, [stale, _summary(HEAD)], 0, 0, ACK)[0] == "clean"
    # 指摘が来ていれば、もちろん findings が勝つ
    assert classify(HEAD, [stale, _summary(HEAD), _finding(HEAD)], 0, 0, ACK)[0] == "findings"


def _vague(extra=""):
    return _bot("<!-- codex-pull-request-review-summary -->\n\n"
                "Review status unavailable.\n" + extra)


def test_unknown_commit_summary_only_poisons_when_head_has_no_result():
    """どのコミットか分からない要約は、いまの結果が無いときだけ効かせる。"""
    assert classify(HEAD, [_vague()], 0, 0, ACK)[0] == "undecidable"
    assert classify(HEAD, [_vague(), _summary(HEAD)], 0, 0, ACK)[0] == "clean"


def test_numbers_in_the_body_are_not_commit_identifiers():
    """**実行番号や日付をコミットと読まない(#167 レビュー指摘)。**

    どちらも [0-9a-f]{7,40} に当たるので、16進に見えるかどうかでは判別できない。
    番号を添えただけで「別コミットの要約」になり、停止理由が消えていた。
    """
    for extra in ("Run ID: 34312276826\n",          # 実行番号（数字だけ）
                  "Recorded: 20260909\n",           # 日付（数字だけ）
                  "Attempt 1234567 of 2\n",
                  "`34312276826`\n"):               # 番号を引用符で囲っただけ
        assert classify(HEAD, [_vague(extra)], 0, 0, ACK)[0] == "undecidable", extra
        # いまの head の結果があれば、当然そちらが勝つ
        assert classify(HEAD, [_vague(extra), _summary(HEAD)], 0, 0, ACK)[0] == "clean", extra


def test_a_real_commit_reference_still_excludes_the_summary():
    """別コミットだと**分かる**書き方なら、これまでどおり持ち込まない。"""
    for extra in ("https://github.com/example/example/commit/%s\n" % OLD,
                  "https://github.com/example/example/blob/%s/x.py#L1\n" % OLD,
                  "Reviewed commit: `%s`\n" % OLD[:7],
                  "SHA: %s\n" % OLD):
        assert classify(HEAD, [_vague(extra)], 0, 0, ACK)[0] == "pending", extra


def test_unreadable_summary_is_undecidable_not_pending():
    """要約はあるのに表を読めない → 未到着ではない。時間切れで緑にしない。"""
    broken = _bot("<!-- codex-pull-request-review-summary -->\n\n"
                  "Code Review completed for %s (new layout, no table)\n" % HEAD)
    assert classify(HEAD, [broken], 0, 0, ACK)[0] == "undecidable"
    # 表は読めたが head の行が無く、本文が head を名指している場合も読めていない
    mixed = _bot("<!-- codex-pull-request-review-summary -->\n\n"
                 "| Review | Status | Commit | Review trigger |\n| --- | --- | --- | --- |\n"
                 "| 📝 **Code Review** | ✅ **Completed** | `%s` | PR opened |\n"
                 "latest run targeted %s\n" % (OLD[:7], HEAD))
    assert classify(HEAD, [mixed], 0, 0, ACK)[0] == "undecidable"
    empty_table = _bot("<!-- codex-pull-request-review-summary -->\n\n"
                       "| Review | Status |\n| --- | --- |\n")
    assert classify(HEAD, [empty_table], 0, 0, ACK)[0] == "undecidable"


def test_bad_head_sha_is_undecidable():
    assert classify("not-a-sha", [_summary(HEAD)], 0, 0)[0] == "undecidable"
