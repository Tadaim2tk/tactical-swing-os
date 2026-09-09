#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Codexレビューが「どの状態か」を1か所で決める。

**きっかけ(#162)**: Codexは 2026-09-08T23:26Z に P2指摘を出したのに、ゲートは
15分後の 23:41Z に「レビュー未着(fail-open)」と書いて緑にし、その1分後にマージされた。
原因は、ゲートが `pulls/{pr}/reviews` しか見ていなかったこと。**Codexは指摘を
issue comment で出すので、reviews API には現れない。** ワークフロー側は
「issue comment として来る」と註までしていたが、探していたのは枠切れの文言だけだった。

ここでは判定だけを行う。ネットワークに触らない。だから架空の入力で試験できる。

判定は6つ。**同じ緑が2つの意味を持たないようにする。**
  findings      いまのheadに対する指摘が残っている            → 赤
  clean         いまのheadをレビュー済みで、指摘が無い        → 緑
  acked         **人が指摘を承知のうえで通した**              → 緑(clean とは別に記録)
  quota         Codexが利用上限。待っても来ない                → 緑(明示のfail-open)
  pending       まだ来ていない/実行中                          → 待つ。時間切れで緑(明示のfail-open)
  undecidable   来たが結論を読み取れない                       → 赤

**判定できないものを緑にしない。** 読み取れないときは undecidable であって pending ではない。

古い結果で誤らないための条件
  - レビュー要約は、いまの head SHA を指しているものだけを見る
  - 指摘は、本文が **いまの head SHA の blob URL** を含むものだけを数える
    （過去コミットへの指摘や、解決済みの古い指摘で赤にしない／緑にしない）
  - 投稿者は `chatgpt-codex-connector[bot]` かつ Bot に限る（なりすまし避け）

行き詰まったときの逃げ道は、**明示して記録に残す**形だけを認める。
書き込み権のある人が `GATE-ACK: <head SHAの40桁>` とコメントすると通る。
ただし **clean とは別の `acked` を返す。** 人が飲み込んだことと、レビューが
問題なしと言ったことは別の事実で、同じ緑にすると後から区別できない。
SHAを含めるので、コミットが変われば承認は自動的に切れる。
"""
import argparse
import json
import re
import sys

BOT_LOGIN = "chatgpt-codex-connector[bot]"
SUMMARY_MARKER = "codex-pull-request-review-summary"
QUOTA_MARK = "usage limits for code reviews"
ACK_PREFIX = "GATE-ACK:"
WRITE_ROLES = {"OWNER", "MEMBER", "COLLABORATOR"}

# 要約コメントの表: | 📝 **Code Review** | ✅ **Completed** ... | `fed98b0` | PR opened |
ROW_SHA = re.compile(r"`([0-9a-f]{7,40})`")
DONE = ("completed", "complete", "finished")
RUNNING = ("running", "in progress", "in_progress", "queued", "pending", "started")
BROKEN = ("failed", "failure", "error", "cancelled", "canceled", "timed out")


def _bot(c):
    u = c.get("user") or {}
    return u.get("login") == BOT_LOGIN and u.get("type") == "Bot"


def _summary_rows(body):
    """要約コメントの表から (状態の文字列, コミット) を拾う。"""
    out = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        for i, cell in enumerate(cells):
            m = ROW_SHA.search(cell)
            if m and i > 0:
                out.append((cells[i - 1].lower(), m.group(1)))
                break
    return out


def _status_kind(text):
    if any(w in text for w in DONE):
        return "done"
    if any(w in text for w in RUNNING):
        return "running"
    if any(w in text for w in BROKEN):
        return "broken"
    return "unknown"


def classify(head_sha, comments, reviews_for_head=0, unresolved_threads=0):
    """(state, reason) を返す。**ネットワークに触らない。**

    unresolved_threads に None を渡すと「数えられなかった」の意味になり、
    レビューが来ている場合は undecidable に倒す。
    """
    head_sha = (head_sha or "").strip().lower()
    if not re.fullmatch(r"[0-9a-f]{40}", head_sha):
        return "undecidable", "head SHA が40桁の16進ではない: %r" % head_sha

    # 人による明示の承認。SHA付きなので、コミットが変われば効かなくなる。
    for c in comments:
        if (c.get("author_association") or "").upper() not in WRITE_ROLES:
            continue
        if _bot(c):
            continue
        if ("%s %s" % (ACK_PREFIX, head_sha)) in (c.get("body") or "").replace("\r", ""):
            return "acked", "書き込み権のある人が GATE-ACK でこのコミットを承認した。**レビューが問題なしと言ったのではない**"

    bots = [c for c in comments if _bot(c)]
    if any(QUOTA_MARK in (c.get("body") or "") for c in bots):
        return "quota", "Codexが利用上限に達している。待っても来ない"

    # いまの head を指す指摘。blob URL の40桁で照合する。
    blob = "/blob/%s/" % head_sha
    findings = [c for c in bots
                if SUMMARY_MARKER not in (c.get("body") or "")
                and blob in (c.get("body") or "")]

    # いまの head に対する要約（最後のものを見る。要約は編集で更新される）
    summary_kind = None
    for c in bots:
        body = c.get("body") or ""
        if SUMMARY_MARKER not in body:
            continue
        for status, sha in _summary_rows(body):
            if head_sha.startswith(sha):
                summary_kind = _status_kind(status)

    if unresolved_threads is None:
        if summary_kind or reviews_for_head or findings:
            return "undecidable", "未解決スレッド数を数えられなかった。レビューは来ている"
        return "pending", "未解決スレッド数を数えられなかったが、レビューもまだ無い"

    if findings:
        return "findings", "このコミットへの指摘が %d件 残っている" % len(findings)
    if unresolved_threads > 0:
        return "findings", "未解決のCodex指摘スレッドが %d件 残っている" % unresolved_threads

    if summary_kind == "done":
        return "clean", "このコミットのレビューが完了し、指摘が無い"
    if summary_kind == "running":
        return "pending", "このコミットのレビューが実行中"
    if summary_kind == "broken":
        return "undecidable", "レビューが異常終了した。結論が無い"
    if summary_kind == "unknown":
        return "undecidable", "要約の状態欄を読み取れなかった"

    if reviews_for_head > 0:
        return "clean", "このコミットへのレビューが %d件 あり、未解決スレッドが無い" % reviews_for_head
    return "pending", "このコミットへのレビューがまだ無い"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--head", required=True)
    ap.add_argument("--comments", required=True, help="issue comments の JSON 配列ファイル")
    ap.add_argument("--reviews", default="0")
    ap.add_argument("--unresolved", default="0", help="数えられなかったときは unknown")
    a = ap.parse_args()
    try:
        comments = json.load(open(a.comments, encoding="utf-8"))
    except Exception as e:                                       # noqa: BLE001
        print("undecidable"); print("コメントを読めなかった: %s" % str(e)[:120]); return 0
    if not isinstance(comments, list):
        print("undecidable"); print("コメントが配列ではない"); return 0
    try:
        reviews = int(a.reviews)
    except ValueError:
        reviews = 0
    unresolved = None if a.unresolved.strip() in ("", "unknown") else int(a.unresolved)
    state, why = classify(a.head, comments, reviews, unresolved)
    print(state); print(why)
    return 0


if __name__ == "__main__":
    sys.exit(main())
