# -*- coding: utf-8 -*-
"""GATE-ACK の権限確認。**シェル経路そのものを試す。**

判定器(python)の試験だけでは、ワークフローが承認の有無を読み取る接続部分を
検査できない。実際、初版は権限が無いときの説明文を標準出力へ出していたため、
**「権限が無いので無視する」という説明が承認として通っていた。**

ここでは偽の `gh` を PATH の先頭に置いて、API応答を差し替えて確かめる。
架空の login と架空のリポジトリしか使わない。
"""
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "tools" / "resolve_gate_ack.sh"
HEAD = "a" * 40
OWNER_REPO = "example-owner/example-repo"

FAKE_GH = r"""#!/usr/bin/env bash
# 引数だけを見て応答する偽の gh。PERMS と OWNER を環境変数から読む。
set -u
path="${2:-}"
case "$path" in
  repos/*/*/collaborators/*/permission)
    login=$(printf '%s' "$path" | awk -F/ '{print $5}')
    val=$(printf '%s' "$PERMS" | tr ',' '\n' | awk -F= -v l="$login" '$1==l{print $2}')
    if [ -z "$val" ] || [ "$val" = "ERROR" ]; then exit 1; fi
    printf '%s\n' "$val"
    ;;
  repos/*/*)
    if [ -z "${OWNER:-}" ]; then exit 1; fi
    printf '%s\n' "$OWNER"
    ;;
  *) exit 1 ;;
esac
"""


def _comment(login, body, kind="User"):
    return {"user": {"login": login, "type": kind},
            "author_association": "MEMBER", "body": body}


def _run(tmp_path, comments, perms="", owner="example-owner"):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    gh = bin_dir / "gh"
    gh.write_text(FAKE_GH, encoding="utf-8")
    gh.chmod(gh.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    cj = tmp_path / "comments.json"
    cj.write_text(json.dumps(comments, ensure_ascii=False), encoding="utf-8")
    env = dict(os.environ)
    env["PATH"] = "%s:%s" % (bin_dir, env["PATH"])
    env["PERMS"], env["OWNER"] = perms, owner
    return subprocess.run(["bash", str(SCRIPT), str(cj), OWNER_REPO, HEAD],
                          capture_output=True, text=True, env=env)


ACK = "GATE-ACK: %s 確認しました" % HEAD


def test_read_only_user_does_not_pass(tmp_path):
    """**これが通っていた。** 説明文が標準出力に混ざり、承認ありと読まれた。"""
    r = _run(tmp_path, [_comment("example-reader", ACK)], perms="example-reader=read")
    assert r.stdout == "", "標準出力に診断が混ざっている: %r" % r.stdout
    assert "example-reader" in r.stderr        # 無視した理由は残る


def test_permission_lookup_failure_does_not_pass(tmp_path):
    r = _run(tmp_path, [_comment("example-unknown", ACK)], perms="example-unknown=ERROR")
    assert r.stdout == ""


def test_write_user_passes(tmp_path):
    r = _run(tmp_path, [_comment("example-writer", ACK)], perms="example-writer=write")
    assert r.stdout == "example-writer"


@pytest.mark.parametrize("perm", ["admin", "maintain", "write"])
def test_each_write_level_passes(tmp_path, perm):
    r = _run(tmp_path, [_comment("example-writer", ACK)],
             perms="example-writer=%s" % perm)
    assert r.stdout == "example-writer"


def test_repo_owner_passes_without_permission_lookup(tmp_path):
    r = _run(tmp_path, [_comment("example-owner", ACK)], perms="")
    assert r.stdout == "example-owner"


def test_bot_is_not_considered(tmp_path):
    r = _run(tmp_path, [_comment("example-bot", ACK, kind="Bot")],
             perms="example-bot=admin")
    assert r.stdout == ""


def test_ack_for_another_commit_is_not_considered(tmp_path):
    r = _run(tmp_path, [_comment("example-writer", "GATE-ACK: %s" % ("b" * 40))],
             perms="example-writer=write")
    assert r.stdout == ""


def test_only_authorised_logins_are_printed(tmp_path):
    r = _run(tmp_path,
             [_comment("example-reader", ACK), _comment("example-writer", ACK)],
             perms="example-reader=read,example-writer=write")
    assert r.stdout == "example-writer"


def test_no_ack_comment_prints_nothing(tmp_path):
    r = _run(tmp_path, [_comment("example-writer", "ふつうのコメント")],
             perms="example-writer=write")
    assert r.stdout == ""


def test_owner_lookup_failure_still_checks_permission(tmp_path):
    """owner を引けなくても、権限のある人は通り、無い人は通らない。"""
    assert _run(tmp_path, [_comment("example-writer", ACK)],
                perms="example-writer=write", owner="").stdout == "example-writer"
    assert _run(tmp_path, [_comment("example-reader", ACK)],
                perms="example-reader=read", owner="").stdout == ""
