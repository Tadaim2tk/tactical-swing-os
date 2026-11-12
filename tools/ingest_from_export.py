#!/usr/bin/env python3
"""ChatGPT の会話エクスポート(JSON)から、未取込の日次レポートを台帳へ入れる（毎朝の取込を1コマンドに）。

なぜ必要か（2026-11-11）
------------------------
Codex の自動化は 2026-10-28 のレポートから ChatGPT の本文を読めなくなった（read_thread が
content reference しか返さない。GPT-6 の出力が新しい描画方式 model_dil_v2 になった日から）。
10/30〜11/2 は添付ファイルをブラウザの保存ダイアログで落として凌いだが、11/9 から
chatgpt.com では Computer Use が使えない。残っている確実な経路は、ログイン済みブラウザから
会話 API (/backend-api/conversation/<id>) の JSON を取る方法だけで、その JSON を渡せば
このスクリプトが残りを全部やる。手作業で毎回やっていた手順（アーカイブ → 検証 → 取込 →
主役・invalidation・週次 crypto の記録 → 採点 → 執行シミュレーション）を固定する。

2026-11-12 追記: 11/12 の出力は read_thread が本文そのものを返し、Codex が取り込んだ（#212）。11/10・11/11 は
本文に出典の部品 <Cite> が残っていて参照しか返らず、11/12 は部品タグが 0 だった（model_dil_v2 は3日とも付いている。
原因は確定させていない。docs/gpt_prompt_changelog.md (22) の追記）。毎朝の取込は Codex が主で、この経路は予備。

    python tools/ingest_from_export.py ~/Downloads/tso_daily_conversation_YYYYMMDD.json           # dry-run
    python tools/ingest_from_export.py ~/Downloads/tso_daily_conversation_YYYYMMDD.json --apply

エクスポートは会話オブジェクトの配列（1件でも配列）。日次会話（題名に「TSO Daily Signal Log」）と、
あれば週次 crypto 会話（題名に「Crypto market update」）を同じ配列に入れてよい。

規約
----
* 1日は10資産10行そろったときだけ取り込む（部分取込はしない）。そろわない日は理由を出して飛ばす。
* 値は直さない。見送り行の語彙と空欄の数だけ ingest_daily_log が補正し、data/ingest_normalizations.csv に残す。
* 主役・invalidation・crypto_grounds・expected_r_basis は本文に明示された値だけを既存の記録ツールへ渡す。
  台帳に無い signal_id や集約した書き方（historical_pending_signals=unknown など）は記録しない。
  crypto_grounds と expected_r_basis は、同じ本文の中で値が食い違っていたら記録しない（どちらが正しいか決めない）。
  2026-11-12 まで、この2つはこの経路で記録していなかった（Codex の経路だけが記録していた）ので、
  この経路で入れた 11/3〜11/11 の9日ぶんが両方の台帳から抜けていた。
* 終了コード: 0=正常（追加0でも）、2=取り込めなかった日がある、3=取込の後段（アーカイブ・主役・invalidation・
  週次 crypto・価格取得・採点・執行シミュレーション）のどれかが失敗した、1=致命的（日次会話が見つからない等）。
* 後段だけをやり直す: `--sidecars-for 2026-11-10,2026-11-11`（その日の主役・invalidation・crypto_grounds・
  expected_r_basis を本文から記録し直す。記録ツールは追記型なので、既にある値は上書きされない）、
  `--force-score`（追加0でも価格取得・採点・執行simを回す）。
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))
import archive_gpt_prose as agp  # noqa: E402
import ingest_daily_log as idl  # noqa: E402
import record_crypto_grounds as rcg  # noqa: E402  語彙だけ借りる（有/無）
import record_signal_extras as rse  # noqa: E402  語彙だけ借りる（subjective/two_point）

ASSETS = ["GOLD", "BTC", "ETH", "WTI", "USDJPY", "SPX", "NASDAQ", "DXY", "US10Y", "VIX"]
LEDGER = Path("data/signal_log.csv")
CTX_PATH = Path("data/crypto_context_weekly.csv")
PRED_PATH = Path("data/crypto_predictions_weekly.csv")
SUMMARY_PATH = Path("results/ingest_from_export_summary.json")
SID_RE = re.compile(r"^\d{8}_[A-Z0-9]+_[A-Z0-9_\-]+$")
LEADER_RES = [re.compile(r"本日の市場の主役[：:]\s*[*`]*\s*([A-Z0-9]+)"),
              re.compile(r"^market_leader:\s*([A-Z0-9]+)", re.M)]
INVAL_LINE_RE = re.compile(r"(?<![\"\w])invalidation_check:\s*([^\n]+)")
# 本文の1行申告（changelog (14)(15)）。JSON のキー（"crypto_grounds": {...}）は拾わない（直前が " の形を除く）。
GROUNDS_LINE_RE = re.compile(r"(?<![\"\w])crypto_grounds:\s*([^\n]+)")
BASIS_LINE_RE = re.compile(r"(?<![\"\w])expected_r_basis:\s*([^\n]+)")
GROUNDS_TOKEN = r"\s*[=＝:：]\s*([^\s,、，;；/()（）。]+)"
# 行頭とは限らない: 2026-11-08 の出力は <text preserveWhitespace>{`CRYPTO_CTX,...`}</text> で包まれていた。
# 欄は英数字・_・-・. だけなので、その文字が続く範囲を1行として拾う。
CRYPTO_LINE_RE = re.compile(r"(CRYPTO_(?:CTX|PRED),[A-Za-z0-9_.,\-]+)")


def _run(args: list[str]) -> tuple[int, str]:
    r = subprocess.run([sys.executable, *args], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def _ledger_rows() -> list[dict]:
    with LEDGER.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_conversations(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("conversations", [data] if "mapping" in data else [])
    return [c for c in data if isinstance(c, dict)]


def validate_day(day: str, text: str) -> tuple[bool, str]:
    """10資産10行・日付一致・拒否なし、を満たすか。"""
    rows, fmt = idl.extract_rows(text)
    if rows.empty:
        return False, "本文に CSV ブロックが無い（または読めない）"
    if len(rows) != len(ASSETS):
        return False, f"行数が {len(rows)}（10資産10行が必要）"
    assets = sorted(rows["asset"].astype(str).str.strip().str.upper())
    if assets != sorted(ASSETS):
        return False, f"資産が10種そろっていない: {assets}"
    dates = set(rows["date"].astype(str).str.strip())
    if dates != {day}:
        return False, f"行の日付 {sorted(dates)} が本文の日付 {day} と違う"
    if idl.REJECT_COL in rows.columns:
        bad = rows[rows[idl.REJECT_COL].astype(str).str.strip() != ""]
        if len(bad):
            return False, "列数が合わない行がある: " + "; ".join(
                f"{r['signal_id']}({r[idl.REJECT_COL]})" for _, r in bad.iterrows())
    return True, fmt


def _unescape_md(text: str) -> str:
    """Markdown のエスケープ `\\_` を `_` に戻す（`_` そのものは消さない）。

    会話 API の本文（content.parts）にはエスケープは無い。同じメッセージの model_dil_v2.fallbackMarkdown は
    コードフェンスの外の `_` を `\\_` と書く（`invalidation\\_check: 20261111\\_GOLD\\_SELL\\_PULLBACK=not\\_fired`）。
    Codex の read_thread が返すのは後者で、Codex が保存した 2026-11-12 以降のアーカイブもこの形。
    どちらの形を渡されても同じ結果になるよう、1行申告を読む前に必ず通す。"""
    return text.replace("\\_", "_")


def find_leader(text: str) -> str | None:
    text = _unescape_md(text)
    for rx in LEADER_RES:
        m = rx.search(text)
        if m and m.group(1).upper() in ASSETS:
            return m.group(1).upper()
    return None


def _declared_lines(rx: re.Pattern, text: str) -> list[str]:
    """本文の1行申告を、Markdown の飾り（太字・コード・\\_ のエスケープ）と UI 部品の閉じを外して返す。"""
    out = []
    for m in rx.finditer(_unescape_md(text)):
        line = re.sub(r"[*`]", "", m.group(1))
        out.append(re.split(r"[<}]", line)[0].strip())
    return out


def _grounds_word(token: str) -> str | None:
    t = token.strip().rstrip("。.").lower()
    if t in {x.lower() for x in rcg.TRUE}:
        return "present"
    if t in {x.lower() for x in rcg.FALSE}:
        return "absent"
    return None


def find_crypto_grounds(text: str) -> tuple[tuple[str, str] | None, str]:
    """本文の `crypto_grounds: etf=有, cme=無` から ((etf, cme), 理由) を返す。値は present / absent。

    本文には同じ申告が何度か出る（冒頭・観察メモ・ログの前）。全部が閉じた語彙（有/無 など。
    tools/record_crypto_grounds.py と同じ）で読めて、全部が同じ値のときだけ記録する。1つでも読めない
    申告や食い違う申告があれば記録しない（どれが正しいかをここで決めない）。"""
    lines = _declared_lines(GROUNDS_LINE_RE, text)
    if not lines:
        return None, "本文に crypto_grounds の1行が無い"
    seen: list[tuple[str, str]] = []
    for line in lines:
        e = re.search("etf" + GROUNDS_TOKEN, line, re.I)
        c = re.search("cme" + GROUNDS_TOKEN, line, re.I)
        pair = (_grounds_word(e.group(1)) if e else None, _grounds_word(c.group(1)) if c else None)
        if not (pair[0] and pair[1]):
            return None, f"crypto_grounds を閉じた語彙（有/無）で読めない申告がある: {line[:60]}"
        if pair not in seen:
            seen.append(pair)
    if len(seen) > 1:
        return None, "同じ本文に食い違う crypto_grounds がある: " + " / ".join(f"etf={e},cme={c}" for e, c in seen)
    return seen[0], ""


def find_expected_r_basis(text: str) -> tuple[str | None, str]:
    """本文の `expected_r_basis: subjective` から (値, 理由) を返す。語彙は tools/record_signal_extras.py と同じ。

    crypto_grounds と同じく、全部の申告が読めて同じ値のときだけ記録する。値の後ろの補足（括弧書き）は読まない。"""
    lines = _declared_lines(BASIS_LINE_RE, text)
    if not lines:
        return None, "本文に expected_r_basis の1行が無い"
    seen: list[str] = []
    for line in lines:
        m = re.match(r"[A-Za-z_]+", line)
        word = m.group(0).lower() if m else ""
        if word not in rse.BASIS_VOCAB:
            return None, (f"expected_r_basis を閉じた語彙（{' / '.join(sorted(rse.BASIS_VOCAB))}）で読めない申告がある: "
                          f"{line[:60]}")
        if word not in seen:
            seen.append(word)
    if len(seen) > 1:
        return None, "同じ本文に食い違う expected_r_basis がある: " + " / ".join(seen)
    return seen[0], ""


def parse_invalidation(text: str, ledger_dates: dict[str, str], day: str) -> tuple[list[str], list[str]]:
    """本文の invalidation_check 行から (記録できる項目, 記録しない項目と理由) を返す。"""
    keep: dict[str, str] = {}
    skipped: list[str] = []
    conflicted: set[str] = set()   # 一度矛盾した ID は、後から何度出ても記録しない(#210 Codex P2)
    for m in INVAL_LINE_RE.finditer(_unescape_md(text)):
        line = re.sub(r"[*`]", "", m.group(1))
        line = re.split(r"[<}]", line)[0]
        for part in line.split(","):
            part = part.strip().rstrip("。.")
            if "=" not in part:
                continue
            sid, verdict = (x.strip() for x in part.split("=", 1))
            vm = re.match(r"[A-Za-z_\-]+", verdict)
            verdict = vm.group(0) if vm else ""
            if not SID_RE.match(sid) or not verdict:
                skipped.append(f"{part[:60]}（signal_id の形でない）")
                continue
            if sid not in ledger_dates:
                skipped.append(f"{sid}（台帳に無い）")
                continue
            if ledger_dates[sid] > day:
                skipped.append(f"{sid}（判断日 {ledger_dates[sid]} が確認日 {day} より後）")
                continue
            if sid in conflicted:
                continue
            if sid in keep and keep[sid] != verdict:
                skipped.append(f"{sid}（同じ本文に矛盾する値 {keep[sid]} / {verdict}）")
                keep.pop(sid)
                conflicted.add(sid)
                continue
            keep.setdefault(sid, verdict)
    return [f"{k}={v}" for k, v in keep.items()], skipped


def crypto_lines(convs: list[dict], title: str) -> list[str]:
    out: list[str] = []
    for conv in convs:
        if title.lower() not in str(conv.get("title", "")).lower():
            continue
        msgs = []
        for node in (conv.get("mapping") or {}).values():
            msg = (node or {}).get("message") or {}
            if ((msg.get("author") or {}).get("role")) != "assistant":
                continue
            parts = ((msg.get("content") or {}).get("parts")) or []
            text = "\n".join(p for p in parts if isinstance(p, str))
            msgs.append((msg.get("create_time") or 0, text))
        for _, text in sorted(msgs, key=lambda x: x[0]):
            for m in CRYPTO_LINE_RE.finditer(_unescape_md(text)):
                line = m.group(1).strip().rstrip(",.")
                if line not in out:
                    out.append(line)
    return out


def _existing_weeks() -> tuple[set[str], set[tuple[str, str]]]:
    ctx, pred = set(), set()
    if CTX_PATH.exists():
        with CTX_PATH.open(encoding="utf-8", newline="") as f:
            ctx = {r["week_start"] for r in csv.DictReader(f)}
    if PRED_PATH.exists():
        with PRED_PATH.open(encoding="utf-8", newline="") as f:
            pred = {(r["week_start"], r["asset"]) for r in csv.DictReader(f)}
    return ctx, pred


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export_file", type=Path)
    ap.add_argument("--apply", action="store_true", help="実際に書く（既定は dry-run）")
    ap.add_argument("--origin", default="chatgpt_app")
    ap.add_argument("--title", default="TSO Daily Signal Log", help="日次会話の題名の部分一致")
    ap.add_argument("--crypto-title", default="Crypto market update", help="週次 crypto 会話の題名の部分一致")
    ap.add_argument("--since", help="この日付以降の未取込日だけ扱う（既定: 台帳の最終日の14日前）")
    ap.add_argument("--no-score", action="store_true", help="価格取得・採点・執行シミュレーションを飛ばす")
    ap.add_argument("--no-fetch", action="store_true", help="価格取得(src/fetch_market.py)だけ飛ばす")
    ap.add_argument("--force-score", action="store_true", help="追加0でも価格取得・採点・執行シミュレーションを回す（後段の再試行）")
    ap.add_argument("--sidecars-for", default="", help="取込済みの日の主役・invalidation・crypto_grounds・expected_r_basis を本文から記録し直す（カンマ区切りの日付）")
    args = ap.parse_args(argv)
    failures: list[str] = []      # 後段の失敗。1つでもあれば終了コード 3 (#210 Codex P2)

    src = args.export_file.expanduser()
    if not src.exists():
        print(f"error: {src} が無い")
        return 1
    convs = load_conversations(src)
    entries = agp.from_chatgpt_export(src, args.title)
    if not entries:
        print(f"error: 題名に '{args.title}' を含む会話から日次レポートを1件も取り出せなかった")
        return 1

    ledger = _ledger_rows()
    counts: dict[str, int] = {}
    for r in ledger:
        counts[r["date"]] = counts.get(r["date"], 0) + 1
    last = max(counts) if counts else "0000-00-00"
    since = args.since or (date.fromisoformat(last) - timedelta(days=14)).isoformat()
    summary: dict = {"export": str(src), "applied": bool(args.apply), "ledger_last_before": last, "since": since,
                     "days": [], "skipped_days": [], "leaders": [], "invalidation": [],
                     "crypto_grounds": [], "expected_r_basis": [], "crypto": [],
                     "partial_days_in_ledger": sorted(d for d, n in counts.items() if d >= since and n != len(ASSETS))}

    # 1) 本文アーカイブ（無い日だけ。既存は上書きしない）
    rc, out = _run([str(ROOT / "tools" / "archive_gpt_prose.py"), str(src), "--from-chatgpt-export",
                    "--title", args.title] + (["--apply"] if args.apply else []))
    summary["archive"] = out.splitlines()[-1] if out else ""
    print("[archive]", summary["archive"])
    if rc != 0:
        failures.append(f"archive rc={rc}: {summary['archive'][:120]}")

    # 2) 未取込の日を古い順に
    targets = [(d, t) for d, _n, t in entries if d not in counts and d >= since]
    ingested: list[tuple[str, str]] = []
    for day, text in targets:
        ok, why = validate_day(day, text)
        if not ok:
            summary["skipped_days"].append({"day": day, "reason": why})
            print(f"[skip] {day}: {why}")
            continue
        dry = idl.ingest(text, origin=args.origin, apply=False, run_score=False)
        would = dry.get("would_append", 0)
        if dry["rejected"] or would + dry["skipped_duplicate"] != len(ASSETS) or would == 0:
            why = f"検証で弾かれた行がある（追加 {would}・重複 {dry['skipped_duplicate']}・拒否 {dry['rejected']}）"
            summary["skipped_days"].append({"day": day, "reason": why})
            print(f"[skip] {day}: {why}")
            continue
        res = idl.ingest(text, origin=args.origin, apply=args.apply, run_score=False) if args.apply else dry
        warns = [f"{d['signal_id']}: {'; '.join(d['warnings'])}" for d in res["details"] if d["warnings"]]
        rows, _ = idl.extract_rows(text)
        ab = int(rows["rank"].astype(str).str.upper().isin(["A", "B"]).sum())
        summary["days"].append({"day": day, "rows": len(rows), "ab_rows": ab,
                                "appended": res.get("appended", 0) if args.apply else would, "warnings": warns})
        print(f"[ingest] {day}: 10行（A/B {ab}）" + ("" if args.apply else " [dry-run]") + (f" 警告 {len(warns)}" if warns else ""))
        ingested.append((day, text))

    # 3) 主役・invalidation・crypto_grounds・expected_r_basis
    #    （取り込んだ日と、--sidecars-for で指定した取込済みの日。dry-run では読むだけ）
    ledger_dates = {r["signal_id"]: r["date"] for r in (_ledger_rows() if args.apply else ledger)}
    redo = [d.strip() for d in args.sidecars_for.split(",") if d.strip()]
    by_day = {d: t for d, _n, t in entries}
    for d in redo:
        if d not in by_day:
            failures.append(f"--sidecars-for {d}: エクスポートにその日の本文が無い")
        elif d not in counts:
            failures.append(f"--sidecars-for {d}: 台帳にその日の行が無い（先に取込が必要）")
        elif d not in [x for x, _ in ingested]:
            ingested.append((d, by_day[d]))
    for day, text in ingested:
        leader = find_leader(text)
        if leader and args.apply:
            rc, out = _run([str(ROOT / "tools" / "record_leader.py"), day, leader, args.origin])
            last_line = out.splitlines()[-1] if out else ""
            summary["leaders"].append({"day": day, "leader": leader, "result": last_line})
            if rc != 0 and "already recorded" not in out:      # 記録済み(rc=1)は失敗ではない
                failures.append(f"record_leader {day} rc={rc}: {last_line[:120]}")
        else:
            summary["leaders"].append({"day": day, "leader": leader, "result": "dry-run" if leader else "本文に主役の1語が無い"})
        items, skipped = parse_invalidation(text, ledger_dates, day)
        entry = {"day": day, "items": len(items), "skipped": skipped, "result": ""}
        if items and args.apply:
            rc, out = _run([str(ROOT / "tools" / "record_signal_extras.py"), "invalidation", day, ",".join(items), args.origin])
            recorded = sum(1 for ln in out.splitlines() if ln.startswith("recorded invalidation"))
            notes = [ln.strip() for ln in out.splitlines() if ln.startswith(("!!", "~~")) or (rc != 0 and ln.strip())]
            entry["result"] = f"rc={rc} recorded={recorded}" + (" | " + " / ".join(notes)[:400] if notes else "")
            if rc != 0:
                failures.append(f"record_signal_extras invalidation {day} rc={rc}: {(out.splitlines() or [''])[-1][:160]}")
        elif not items:
            entry["result"] = "記録できる項目なし（1行欄が無いか、集約した書き方）"
        else:
            entry["result"] = "dry-run"
        summary["invalidation"].append(entry)
        print(f"[sidecar] {day}: 主役 {leader or '—'} / invalidation {len(items)}件"
              + (f"（記録しない {len(skipped)}件）" if skipped else "") + (f" {entry['result']}" if entry["result"] else ""))

        grounds, why = find_crypto_grounds(text)
        g_entry = {"day": day, "etf": grounds[0] if grounds else "", "cme": grounds[1] if grounds else "", "result": why}
        if grounds and args.apply:
            rc, out = _run([str(ROOT / "tools" / "record_crypto_grounds.py"), day, grounds[0], grounds[1], args.origin])
            g_entry["result"] = ([ln for ln in out.splitlines() if ln.strip()] or [f"rc={rc}"])[-1]
            if rc != 0 and "already recorded" not in out:      # 記録済み(rc=1)は失敗ではない
                failures.append(f"record_crypto_grounds {day} rc={rc}: {g_entry['result'][:120]}")
        elif grounds:
            g_entry["result"] = "dry-run"
        summary["crypto_grounds"].append(g_entry)

        basis, why = find_expected_r_basis(text)
        b_entry = {"day": day, "basis": basis or "", "result": why}
        if basis and args.apply:
            rc, out = _run([str(ROOT / "tools" / "record_signal_extras.py"), "basis", day, basis, args.origin])
            b_entry["result"] = ([ln for ln in out.splitlines() if ln.strip()] or [f"rc={rc}"])[-1]
            if rc != 0:
                failures.append(f"record_signal_extras basis {day} rc={rc}: {b_entry['result'][:120]}")
        elif basis:
            b_entry["result"] = "dry-run"
        summary["expected_r_basis"].append(b_entry)
        print(f"[sidecar] {day}: crypto_grounds " + (f"etf={grounds[0]} cme={grounds[1]}" if grounds else "—")
              + f" / expected_r_basis {basis or '—'}"
              + "".join(f"（{e['result']}）" for e, v in ((g_entry, grounds), (b_entry, basis)) if not v))

    # 4) 週次 crypto の2行（未記録の週だけ）
    ctx_have, pred_have = _existing_weeks()
    for line in crypto_lines(convs, args.crypto_title):
        parts = line.split(",")
        kind, week = parts[0], parts[1] if len(parts) > 1 else ""
        if (kind == "CRYPTO_CTX" and week in ctx_have) or (kind == "CRYPTO_PRED" and len(parts) > 2 and (week, parts[2]) in pred_have):
            continue
        if args.apply:
            rc, out = _run([str(ROOT / "tools" / "record_crypto_context.py"), line])
            result = out.splitlines()[-1] if out else f"rc={rc}"
            if rc != 0:
                failures.append(f"record_crypto_context rc={rc}: {result[:160]}")
        else:
            result = "dry-run"
        summary["crypto"].append({"line": line, "result": result})
        print(f"[crypto] {line} -> {result}")

    # 5) 価格取得・採点・執行シミュレーション
    appended_any = args.apply and any(d["appended"] for d in summary["days"])
    if args.apply and (appended_any or args.force_score) and not args.no_score:
        if not args.no_fetch:
            rc, out = _run([str(ROOT / "src" / "fetch_market.py")])
            summary["fetch_market"] = out.splitlines()[-1] if out else f"rc={rc}"
            print("[fetch]", summary["fetch_market"])
            if rc != 0:
                failures.append(f"fetch_market rc={rc}: {summary['fetch_market'][:120]}")
        for name in ("score_prediction_log.py", "simulate_execution.py"):
            rc, out = _run([str(ROOT / "src" / name)])
            summary[name] = (out.splitlines()[-1] if out else "")[:300] + ("" if rc == 0 else f" (rc={rc})")
            print(f"[{name}]", summary[name][:160])
            if rc != 0:
                failures.append(f"{name} rc={rc}")
        rc, out = _run([str(ROOT / "tools" / "throughput_watch.py"), "--check-only"])
        st = [ln for ln in out.splitlines() if ln.startswith("status=")]
        summary["throughput"] = st[-1] if st else ""
        print("[throughput]", summary["throughput"])

    after = _ledger_rows() if args.apply else ledger
    summary["ledger_last_after"] = max((r["date"] for r in after), default="")
    summary["failures"] = failures
    for f in failures:
        print(f"[FAILED] {f}")
    if args.apply:
        SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
        SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    n_days = len(summary["days"])
    print(f"\n{'applied' if args.apply else 'dry-run'}: 取込 {n_days}日 / 飛ばした日 {len(summary['skipped_days'])} / "
          f"台帳の最終日 {last} → {summary['ledger_last_after']}"
          + (f" / 行数が10でない日: {summary['partial_days_in_ledger']}" if summary["partial_days_in_ledger"] else "")
          + (f" / 後段の失敗 {len(failures)}件（--sidecars-for / --force-score でやり直せる）" if failures else ""))
    if failures:
        return 3
    return 2 if summary["skipped_days"] else 0


if __name__ == "__main__":
    sys.exit(main())
