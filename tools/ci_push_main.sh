#!/usr/bin/env bash
# 定期実行が作ったデータ追記のコミットを、専用鍵で main へ push する。弾かれたら取り込み直してやり直す。
#
# 2026-11-25: daily cycle と news narratives が同じ秒に push した。後になった daily cycle は
#   ! [remote rejected] HEAD -> main (cannot lock ref 'refs/heads/main': is at 4ef82bc… but expected b6f3769…)
# で弾かれ、その日の夜間の台帳（採点・執行シミュレーション・市場コンテキストの写し・売買頻度の記録）は
# main に入らないままジョブが赤で終わった。push は1回きりで、弾かれたあと取り込み直す手順が無かった。
# 2本は cron では5分ずれているが、GitHub が遅らせて同じ分にまとめて始めることがあり、どちらも約40秒で終わる。
#
# 使い方（workflow の、コミットを作った直後から呼ぶ）:
#   TSO_BOT_DEPLOY_KEY=... GITHUB_REPOSITORY=owner/repo bash tools/ci_push_main.sh [branch]
#
# 守っていること:
# - **鍵は push の直前に書き、直後に消す。** 取り込みや待ちのあいだは置かない（#121 Codex P1）。
# - 取り込み（git pull --rebase）が失敗したら、やり直さずに落とす。同じファイルを別の実行が書き換えた
#   ということなので、機械が勝手に片方を選ばない。
# - 最後まで弾かれたら赤で終わり、**この実行のデータは main に入っていない**と書く。黙って捨てない。
# 試験: src/test_ci_push_main.py（このスクリプトを、手元の bare リポジトリを相手にそのまま走らせる）。
set -euo pipefail

branch="${1:-main}"
attempts="${TSO_PUSH_ATTEMPTS:-5}"
: "${TSO_BOT_DEPLOY_KEY:?TSO_BOT_DEPLOY_KEY is not set}"
: "${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is not set}"
case "$attempts" in ''|*[!0-9]*|0) echo "::error::TSO_PUSH_ATTEMPTS must be a positive integer (got '$attempts')"; exit 2 ;; esac

key_file=""
cleanup() {
  if [ -n "$key_file" ]; then
    rm -f "$key_file"
  fi
}
trap cleanup EXIT

push_once() {
  local rc=0
  # 置き場所を明示する（macOS の mktemp は、型を渡さないと TMPDIR を見ない。試験が鍵の置き場所を見張れるように
  # どの環境でも同じ決め方にする）。mktemp が作るファイルは持ち主だけが読める。
  key_file=$(mktemp "${TMPDIR:-/tmp}/tso-push-key.XXXXXX")
  printf '%s\n' "$TSO_BOT_DEPLOY_KEY" > "$key_file"
  GIT_SSH_COMMAND="ssh -i $key_file -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new" \
    git push "git@github.com:$GITHUB_REPOSITORY.git" "HEAD:$branch" || rc=$?
  rm -f "$key_file"
  key_file=""
  return "$rc"
}

attempt=1
while :; do
  # ほかの実行が先に入れたコミットを取り込む。手を付けていない追跡ファイルの変更が残っていても止まらないように
  # --autostash を付ける（コミット済みの追記だけが push の対象）。
  git pull --rebase --autostash origin "$branch"
  if push_once; then
    echo "pushed to $branch (attempt $attempt/$attempts)"
    exit 0
  fi
  if [ "$attempt" -ge "$attempts" ]; then
    break
  fi
  echo "::warning::push to $branch was rejected (attempt $attempt/$attempts). Another run probably pushed first; pulling again and retrying."
  sleep $((attempt * 5))
  attempt=$((attempt + 1))
done
echo "::error::could not push to $branch after $attempts attempts. This run's data is NOT on $branch. Re-run this workflow once the cause is clear (docs/operations_runbook.md §1h)."
exit 1
