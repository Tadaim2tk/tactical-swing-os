#!/bin/bash
# TSO Daily Signal Log をターミナル GPT (codex exec) で生成し、検証付きプレビューまで行う。
# 人間がプレビューを確認してから --apply で台帳に入れる（human-in-the-loop を維持）。
#
# 使い方:  ./scripts/tso_daily_gpt.sh
# 前提:    codex CLI がログイン済み (ChatGPTアカウント認証)
set -euo pipefail
cd "$(dirname "$0")/.."

DATE=$(date +%F)
OUT="inbox/${DATE}_daily_log_gpt.md"
mkdir -p inbox

echo "== codex exec で日次ログを生成 (web検索有効・read-onlyサンドボックス) =="
codex --search exec \
  --ignore-user-config \
  --sandbox read-only \
  --skip-git-repo-check \
  - < prompts/tso_daily_signal_log.md > "$OUT"

echo ""
echo "== 生成物: $OUT =="
echo ""
echo "== 取込プレビュー (dry-run・検証つき) =="
python src/ingest_daily_log.py --file "$OUT" --origin gpt_terminal

echo ""
echo "内容を確認して問題なければ:"
echo "  python src/ingest_daily_log.py --file $OUT --origin gpt_terminal --apply"
