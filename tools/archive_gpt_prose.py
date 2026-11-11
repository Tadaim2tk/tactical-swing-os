"""GPT日次出力の散文を追記型アーカイブへ保存する（runbook §1c の対策候補2）。

問題: 台帳CSVは構造化された行を保つが、**判断の理由・因果モデル・主役申告の根拠は
文章側にしかない**。その散文は 2026-07-05 を最後に誰も保存していなかった
（data/prediction_log_archive/ が同日で止まっている）。inbox/*.md にもヘッダ注記と
CSVブロック（約2.7KB）しか無く、推論の本体（1日あたり約13KB）は毎日消えていた。

取得経路: ChatGPTの会話ページで各assistant turnの innerText を連結し、Blob経由で
ダウンロードさせる。DOM抽出をツール結果に通すと引用URLのクエリ文字列で
コンテンツフィルタに掛かるため、ファイル経由にして全文を無修正で運ぶ。

    // ブラウザ側（会話ページで実行）
    const turns=[...document.querySelectorAll('[data-message-author-role="assistant"]')];
    const payload = turns.map(t => {
      const m = t.innerText.match(/— (\d{4}-\d{2}-\d{2})/);
      return '===== TSO_DAILY ' + (m?m[1]:'unknown') + ' (' + t.innerText.length + ' chars) =====\n' + t.innerText;
    }).join('\n\n');
    const a=document.createElement('a');
    a.href=URL.createObjectURL(new Blob([payload],{type:'text/plain;charset=utf-8'}));
    a.download='tso_daily_prose_export.txt'; document.body.appendChild(a); a.click(); a.remove();

規約:
- **append-only**。既にある日は上書きしない（推測で埋めない・後から書き換えない）。
- 区切り行が宣言する文字数と実際の長さが合わない日は**書かずに警告する**
  （転記事故を黙って通さない）。

usage: python tools/archive_gpt_prose.py ~/Downloads/tso_daily_prose_export.txt [--apply]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ARCHIVE = Path("data/prediction_log_archive")
HEADER = re.compile(r"^===== TSO_DAILY (\d{4}-\d{2}-\d{2}|unknown) \((\d+) chars\) =====$", re.M)
JP_DATE = re.compile(r"(\d{4})年(\d{1,2})月(\d{1,2})日")
ISO_DATE = re.compile(r"— (\d{4}-\d{2}-\d{2})")
# レポート自身が名乗る実行日。前置きの後に来ることがある(7/27)
RUN_DATE = re.compile(r"実行日[：:]\s*\**\s*(\d{4})年(\d{1,2})月(\d{1,2})日")
# 見出し行「# TSO Daily Signal Log v2 — <日付>」が先頭以外にある場合
TITLE_LINE = re.compile(
    r"^#*\s*\**\s*TSO Daily Signal Log v2[^\n]{0,20}?"
    r"(?:(?P<iso>\d{4}-\d{2}-\d{2})|(?P<y>\d{4})年(?P<mo>\d{1,2})月(?P<d>\d{1,2})日)", re.M)


def detect_day(text: str):
    """本文先頭から日付を拾う。2026-09-01形式と2026年8月26日形式の両方に対応。

    8月以前の出力は和暦表記で、ISO形式だけを見ていると丸ごと取りこぼす
    (2026-09-05に実際に取りこぼした)。
    """
    m = ISO_DATE.search(text[:300])
    if m:
        return m.group(1)
    m = JP_DATE.search(text[:300])
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    # 先頭300字に無い場合(#171 Codex P2): 7/27 は「タスクのプロンプトを修正しました…」
    # という前置きの後に「**実行日：2026年7月27日**」が来ていて、台帳には10行入って
    # いるのにアーカイブから落ちた。窓を広げるだけだと本文中の「7月28日の終値」の
    # ような日付を拾うので、**レポート自身の見出し語彙に限って**全文を探す。
    m = RUN_DATE.search(text)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    m = TITLE_LINE.search(text)
    if m:
        if m.group("iso"):
            return m.group("iso")
        return f"{m.group('y')}-{int(m.group('mo')):02d}-{int(m.group('d')):02d}"
    return None


def split_export(text: str):
    """区切り行で分割し (date, declared_len, body) を返す。"""
    marks = list(HEADER.finditer(text))
    out = []
    for i, m in enumerate(marks):
        start = m.end() + 1  # 区切り行直後の改行を落とす
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out.append((m.group(1), int(m.group(2)), text[start:end].rstrip("\n")))
    return out


def from_chatgpt_export(path: Path, title_match: str):
    """ChatGPT公式エクスポート(conversations.json)から日次出力を取り出す。

    Blob経由のDOM抽出は仮想スクロールのせいで直近しか取れない(2026-09-05に
    5日分で頭打ちになった)。過去分の一括回収は公式エクスポートを使う:
    ChatGPT → 設定 → データコントロール → データをエクスポート → メールのzip →
    展開して conversations.json をこのモードへ渡す。
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("conversations", [])
    out = []
    for conv in data:
        title = str(conv.get("title", ""))
        if title_match and title_match.lower() not in title.lower():
            continue
        for node in (conv.get("mapping") or {}).values():
            msg = (node or {}).get("message") or {}
            if ((msg.get("author") or {}).get("role")) != "assistant":
                continue
            parts = ((msg.get("content") or {}).get("parts")) or []
            text = "\n".join(p for p in parts if isinstance(p, str)).strip()
            if not text:
                continue
            day = detect_day(text)
            if day:
                out.append((day, len(text), text))
    # 同じ日が複数あれば最長のものを採る(再生成分より完全な方)
    best = {}
    for day, n, text in out:
        if day not in best or n > best[day][0]:
            best[day] = (n, text)
    return [(d, n, t) for d, (n, t) in sorted(best.items())]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("export_file")
    ap.add_argument("--apply", action="store_true", help="実際に書き出す（既定はdry-run）")
    ap.add_argument("--from-chatgpt-export", action="store_true",
                    help="ChatGPT公式エクスポートの conversations.json を読む")
    ap.add_argument("--title", default="TSO", help="会話タイトルの部分一致（既定: TSO）")
    ap.add_argument("--transport", default=None,
                    help="ヘッダに残す取得経路。省略時はモードから決める。"
                         "本文の出所が既定と違うとき(例: 会話APIの raw markdown を Blob 形式に"
                         "整えて渡した)は必ず明示する。出所の記録が嘘になると後から検算できない")
    args = ap.parse_args()
    # 経路をモードで決め打ちしていたため、会話APIから取った本文にも
    # 「DOM innerText -> Blob download」と書いていた(#170 Codex P2)。
    # DOMの innerText と raw markdown では ```csv フェンスや ** の有無が違い、
    # 同じ「本文」でも抽出の意味が変わる。ヘッダは実際の経路を言う。
    if args.transport is None:
        args.transport = ("ChatGPT conversation JSON (公式エクスポート conversations.json または "
                          "/backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export"
                          if args.from_chatgpt_export else
                          "DOM innerText -> Blob download -> tools/archive_gpt_prose.py")

    src = Path(args.export_file).expanduser()
    if not src.exists():
        print(f"error: {src} が無い")
        return 1
    if args.from_chatgpt_export:
        entries = from_chatgpt_export(src, args.title)
        if not entries:
            print(f"error: タイトルに '{args.title}' を含む会話から日次出力を1件も取り出せなかった")
            return 1
        print(f"conversations.json から {len(entries)}日分を検出（{entries[0][0]}..{entries[-1][0]}）")
    else:
        entries = split_export(src.read_text(encoding="utf-8"))
        if not entries:
            print("error: 区切り行 '===== TSO_DAILY <date> (<n> chars) =====' が1つも無い")
            return 1

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    written = skipped = mismatched = 0
    for day, declared, body in entries:
        if day == "unknown":
            print(f" ! 日付を判別できない塊 ({len(body)}字) — 書かない")
            mismatched += 1
            continue
        # 実長は区切り行の宣言と一致するはず(±改行1つ)。公式エクスポート経路は
        # 区切り行が無く declared==len(body) を自分で入れているので常に通る。
        if abs(len(body) - declared) > 1:
            print(f" ! {day}: 宣言 {declared}字 vs 実際 {len(body)}字 — 転記事故の疑いがあるため書かない")
            mismatched += 1
            continue
        dest = ARCHIVE / f"{day}_tso-daily-signal-log.md"
        if dest.exists():
            print(f" = {day}: 既にある（append-only台帳のため上書きしない）")
            skipped += 1
            continue
        print(f" + {day}: {len(body)}字 -> {dest}")
        if args.apply:
            ARCHIVE.mkdir(parents=True, exist_ok=True)
            dest.write_text(
                f"<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 {day} 07:00 JST -->\n"
                f"<!-- transport: {args.transport} -->\n"
                f"<!-- archived_at: {now} / chars: {len(body)} / 値は無修正 -->\n\n" + body + "\n",
                encoding="utf-8")
        written += 1

    verb = "wrote" if args.apply else "[dry-run] would write"
    print(f"{verb}={written} skipped_existing={skipped} mismatched={mismatched}")
    if not args.apply and written:
        print("実行するには --apply を付ける")
    return 1 if mismatched else 0


if __name__ == "__main__":
    sys.exit(main())
