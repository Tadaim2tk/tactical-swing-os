#!/usr/bin/env bash
# GATE-ACK を書いた人のうち、**いま書き込み権限がある login だけ**を返す。
#
# **標準出力は login のカンマ区切りだけ。** 診断は標準エラーへ出す。
# 初版はワークフローの中に関数として書いていて、権限が無いときの説明文を
# 標準出力へ出していた。呼ぶ側は `[ -n "$(resolve_ack)" ]` で承認の有無を見るので、
# **「権限が無いので無視する」という説明そのものが承認として通っていた。**
# 出力に意味を持たせる関数は、診断を混ぜた時点で壊れる。
#
# `author_association` は使わない。書き込み権限ではないので、MEMBER を名乗る Bot でも
# 通ってしまう。投稿者が User であることを jq 側で確かめ、権限は API に聞く。
# **聞けなければ承認しない。**
#
# usage: resolve_gate_ack.sh <comments.json> <owner/repo> <head sha>
set -u
comments="${1:?comments.json が要る}"
repo="${2:?owner/repo が要る}"
head_sha="${3:?head sha が要る}"

ack=""
repo_owner=$(gh api "repos/$repo" --jq '.owner.login' 2>/dev/null || echo "")

for login in $(jq -r --arg s "GATE-ACK: $head_sha" \
      '[.[] | select((.user.type // "") == "User")
            | select((.body // "") | contains($s))
            | .user.login] | unique | .[]' "$comments" 2>/dev/null); do
  if [ -n "$repo_owner" ] && [ "$login" = "$repo_owner" ]; then
    ack="$ack,$login"
    continue
  fi
  perm=$(gh api "repos/$repo/collaborators/$login/permission" \
           --jq '.permission' 2>/dev/null || echo "")
  case "$perm" in
    admin|maintain|write)
      ack="$ack,$login"
      ;;
    *)
      echo "GATE-ACK を無視: $login の書き込み権限を確認できない (${perm:-照会できず})" >&2
      ;;
  esac
done

printf '%s' "${ack#,}"
