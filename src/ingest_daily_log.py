"""Daily log ingestion (Phase 29.7) — ChatGPT/GPT出力から予測台帳への検証付き取込。

「ChatGPT のチャット内出力を手作業で CSV 整形して台帳に足す」工程を、
検証付きの1コマンドに置き換える:

    python src/ingest_daily_log.py --file inbox/2026-07-09.md --origin chatgpt_app
    (dry-run 確認後) ... --apply

入力は3形式を自動判別:
1. Markdown 全文（日次レポート貼り付け）中の ```csv フェンスブロック
2. 生CSVテキスト（ヘッダ行あり/なし両対応）
3. JSON 配列（codex exec の --output-schema 出力など）

検証（記録は広く・警告は正直に）:
- 必須: date が日付 / signal_id 非空 / 既存 signal_id との重複は skip
- 警告（記録はする）: 未知 asset / side・rank が既知enum外 / actionable なのに
  entry/SL 不整合 / **記録水準が実価格と桁違い（scale_mismatch の入口検知**
  — 6/9 NASDAQ の QQQ水準事故をここで即座に人間へ見せる)
- 拒否: 列がヘッダに対応づけられない行のみ（黙って捨てない: 全件表示）

origin 列（chatgpt_app / gpt_terminal / manual）を台帳に追加し、
生成経路別の成績比較（どちらの GPT 出力が予測精度で勝つか）を可能にする。
既定は dry-run（プレビューのみ）。--apply で追記し、追記後に遡及採点を自動実行。
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
from html import unescape as html_unescape
import sys
from pathlib import Path

import numpy as np
import pandas as pd

LEDGER_PATH = Path("data/signal_log.csv")
RAW_DIR = Path("data/raw")

KNOWN_SIDES = {"BUY", "SELL", "LONG", "SHORT", "NONE"}
KNOWN_RANKS = {"A", "B", "C", "NO_TRADE"}
ORIGINS = {"chatgpt_app", "gpt_terminal", "manual"}

CSV_BLOCK_RE = re.compile(r"```csv\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)
# 2026-11-06 から GPT-6 は CSV を ```csv フェンスではなく <CodeBlock language="csv">…</CodeBlock> で出す。
# どちらも同じ「CSVブロック」として読む（取込が止まった原因の一つ。#205）。
CODEBLOCK_RE = re.compile(r"<CodeBlock\s+language=\"csv\"[^>]*>\s*(.*?)</CodeBlock>", re.DOTALL | re.IGNORECASE)

# NO_TRADE 行で空欄にする8列（type の直後から expected_r まで）。
NO_TRADE_BLANK_COLS = ["entry_low", "entry_high", "sl", "tp1", "tp2", "rr", "win_prob", "expected_r"]
REGIME_VOCAB = {"RISK_ON", "RISK_OFF", "NEUTRAL", "MIXED", "EVENT", "UNKNOWN"}
NORMALIZATION_LOG_NAME = "ingest_normalizations.csv"   # 台帳と同じディレクトリに置く
NO_TRADE_ID_RE = re.compile(r"^(\d{8}_[A-Z0-9]+)_NO_TRADE_NONE$")
NOTE_COL, REJECT_COL, RAW_ID_COL = "_ingest_note", "_ingest_reject", "_raw_signal_id"


def _s(v) -> str:
    """欠損(None / NaN)を空文字として読む。JSON 入力の null を "None" や "nan" という文字列にしない
    (#210 Codex P2: 文字列化すると signal_id: null が空でない ID として通ってしまう)。"""
    if v is None:
        return ""
    try:
        if pd.isna(v):
            return ""
    except (TypeError, ValueError):
        pass
    return str(v).strip()


def _is_num_or_blank(v: str) -> bool:
    v = str(v).strip()
    if v == "":
        return True
    try:
        float(v)
        return True
    except ValueError:
        return False


def _repair_field_counts(text: str) -> tuple[str, dict[str, str], dict[str, str]]:
    """列数がヘッダと合わない行を、典型形だけ補正する。(本文, 補正メモ, 拒否理由) を返す。

    2026-11-11: 見送り4行が27列（type〜expected_r の空欄が7つ。1つ不足）で出た。
    pandas は足りない列を末尾の欠損として読むので、tq_score が expected_r に、
    regime が risk_pct に入り、**警告も出ずに1列ずれたまま台帳へ入る**ところだった。
    典型形（NO_TRADE 行の空欄の数え違い）は1つ補って揃え、それ以外の列数違いは拒否する。
    1列多い典型形（全行+1）は従来どおり _repair_extra_blank_before_tq_score が扱う。
    """
    lines = [ln for ln in text.splitlines() if ln.strip()]
    try:
        rows = list(csv.reader(lines))
    except csv.Error:
        return text, {}, {}
    if not rows:
        return text, {}, {}
    header = rows[0]
    n = len(header)
    need = {"signal_id", "type", "tq_score", "regime", *NO_TRADE_BLANK_COLS}
    if not need.issubset(header):
        return text, {}, {}
    i_type, i_regime = header.index("type"), header.index("regime")
    blanks = [header.index(c) for c in NO_TRADE_BLANK_COLS]
    i_sid = header.index("signal_id")
    counts = [len(r) for r in rows[1:]]
    if all(c == n for c in counts) or (counts and all(c == n + 1 for c in counts)):
        return text, {}, {}        # 揃っている、または全行+1（従来の補正に任せる）
    notes: dict[str, str] = {}
    rejects: dict[str, str] = {}
    out = [header]
    for r in rows[1:]:
        sid = r[i_sid].strip() if len(r) > i_sid else ""
        if len(r) == n:
            out.append(r)
            continue
        if len(r) == n - 1:
            cand = r[:i_type + 1] + [""] + r[i_type + 1:]
            ok = (all(cand[i].strip() == "" for i in blanks)
                  and cand[i_regime].strip().upper() in REGIME_VOCAB
                  and all(_is_num_or_blank(cand[header.index(c)]) for c in ("tq_score", "opp_score", "no_trade_score")))
            if ok:
                notes[sid] = f"列数{len(r)}（ヘッダ{n}）: 見送り行の空欄が1つ不足 → 1つ補って揃えた"
                out.append(cand)
                continue
        rejects[sid] = f"列数が{len(r)}（ヘッダは{n}）。典型形の補正にも当てはまらないため取り込まない"
        out.append((r + [""] * n)[:n])
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerows(out)
    return buf.getvalue(), notes, rejects


def _normalize_no_trade_vocab(df: pd.DataFrame) -> pd.DataFrame:
    """見送り行の side/rank/type と signal_id を台帳の約束へ揃える（原文は RAW_ID_COL とメモに残す）。

    台帳の約束は side=NONE, rank=NO_TRADE, type=NO_TRADE、signal_id=YYYYMMDD_ASSET_NONE_NO_TRADE
    （1,094行）。2026-11-10 から GPT は side=NO_TRADE, rank=NONE, type=NONE、
    signal_id=…_NO_TRADE_NONE と書き始めた。そのまま入れると rank=="NO_TRADE" で数える集計から
    見送りが消える。価格列が空の行に限って、語の置き場所だけを直す（判断の中身は変えない）。
    """
    need = {"signal_id", "side", "rank", "type", "entry_low", "entry_high", "sl"}
    if df.empty or not need.issubset(df.columns):
        return df
    df = df.copy()
    for col in (NOTE_COL, REJECT_COL, RAW_ID_COL):
        if col not in df.columns:
            df[col] = ""
    for idx, row in df.iterrows():
        side = _s(row["side"]).upper()
        rank = _s(row["rank"]).upper()
        typ = _s(row["type"]).upper()
        prices_blank = all(_s(row[c]) == "" for c in ("entry_low", "entry_high", "sl"))
        if not prices_blank or side in {"BUY", "SELL", "LONG", "SHORT"}:
            continue
        if not (side == "NO_TRADE" or rank == "NONE"):
            continue                      # 既に約束どおり（side=NONE, rank=NO_TRADE）か、別の語彙
        if side not in {"NO_TRADE", "NONE", ""} or rank not in {"NONE", "NO_TRADE", ""}:
            continue
        raw_sid = _s(row["signal_id"])
        if not raw_sid:
            continue                      # ID が無い行は validate_row が拒否する。ここでは触らない
        new_type = "NO_TRADE" if typ in {"NONE", "", "NO_TRADE"} else _s(row["type"])
        m = NO_TRADE_ID_RE.match(raw_sid)
        new_sid = f"{m.group(1)}_NONE_NO_TRADE" if m else raw_sid
        note = (f"見送り行の語彙を正規化: side/rank/type={_s(row['side'])}/{_s(row['rank'])}/{_s(row['type'])}"
                f" → NONE/NO_TRADE/{new_type}")
        if new_sid != raw_sid:
            note += f"、signal_id {raw_sid} → {new_sid}"
        df.at[idx, "side"], df.at[idx, "rank"], df.at[idx, "type"] = "NONE", "NO_TRADE", new_type
        df.at[idx, "signal_id"] = new_sid
        df.at[idx, RAW_ID_COL] = raw_sid
        prev = _s(df.at[idx, NOTE_COL])
        df.at[idx, NOTE_COL] = (prev + "；" if prev else "") + note
    return df


def _attach_notes(df: pd.DataFrame, notes: dict[str, str], rejects: dict[str, str]) -> pd.DataFrame:
    if df.empty or "signal_id" not in df.columns:
        return df
    df = df.copy()
    sid = df["signal_id"].map(_s)
    df[NOTE_COL] = sid.map(lambda x: notes.get(x, ""))
    df[REJECT_COL] = sid.map(lambda x: rejects.get(x, ""))
    df[RAW_ID_COL] = ""
    return df


def extract_rows(text: str) -> tuple[pd.DataFrame, str]:
    """入力テキストから行を抽出。(DataFrame, 形式名) を返す。失敗は空DF。"""
    text = text.strip()
    # 1) JSON 配列
    if text.startswith("["):
        try:
            data = json.loads(text)
            if isinstance(data, list) and data and isinstance(data[0], dict):
                return _normalize_no_trade_vocab(_attach_notes(pd.DataFrame(data), {}, {})), "json"
        except json.JSONDecodeError:
            pass
    # 2) Markdown 中の ```csv ブロック（複数あれば結合）
    blocks = CSV_BLOCK_RE.findall(text) + [html_unescape(b) for b in CODEBLOCK_RE.findall(text)]
    if blocks:
        frames = []
        for b in blocks:
            df = _parse_csv_text(b)
            if not df.empty:
                frames.append(df)
        if frames:
            return pd.concat(frames, ignore_index=True), "markdown_csv_block"
    # 3) 生CSV
    df = _parse_csv_text(text)
    if not df.empty:
        return df, "raw_csv"
    return pd.DataFrame(), "unrecognized"


def _parse_csv_text(text: str) -> pd.DataFrame:
    text = text.strip()
    if not text:
        return pd.DataFrame()
    try:
        first = text.splitlines()[0]
        if first.lower().startswith("date,"):
            text, notes, rejects = _repair_field_counts(text)
            df = pd.read_csv(io.StringIO(text), dtype=str, keep_default_na=False)
            df = _repair_extra_blank_before_tq_score(df)
            return _normalize_no_trade_vocab(_attach_notes(df, notes, rejects))
        # ヘッダ無し: 台帳ヘッダ(origin除く)を仮定して読めるか試す
        ledger_cols = _ledger_columns()
        base_cols = [c for c in ledger_cols if c != "origin"]
        df = pd.read_csv(io.StringIO(text), dtype=str, keep_default_na=False, header=None)
        if len(df.columns) == len(base_cols):
            df.columns = base_cols
            return _normalize_no_trade_vocab(_attach_notes(df, {}, {}))
        return pd.DataFrame()
    except Exception:  # noqa: BLE001 - 解析失敗は「認識できない形式」として正直に返す
        return pd.DataFrame()


def _blank_series(values: pd.Series) -> bool:
    return values.astype(str).str.strip().eq("").all()


def _repair_extra_blank_before_tq_score(df: pd.DataFrame) -> pd.DataFrame:
    """NO_TRADE行で expected_r と tq_score の間に余分な空欄が1つ入ったCSVを補正する。

    ChatGPT/Codex exec は NO_TRADE の空欄列を数え違え、全行に1フィールド多いCSVを
    出すことがある。pandas はその場合、先頭の date を暗黙indexとして吸収してしまうため、
    取り込み側では date=signal_id のように読めて全行rejectになる。典型形だけを狭く補正する。
    """
    if isinstance(df.index, pd.RangeIndex):
        return df
    cols = list(df.columns)
    if "tq_score" not in cols or "date" not in cols or "signal_id" not in cols:
        return df

    reset = df.reset_index()
    if reset.shape[1] != len(cols) + 1:
        return df

    drop_at = cols.index("tq_score")
    if drop_at >= reset.shape[1] or not _blank_series(reset.iloc[:, drop_at]):
        return df

    candidate_values = pd.concat([reset.iloc[:, :drop_at], reset.iloc[:, drop_at + 1:]], axis=1)
    if candidate_values.shape[1] != len(cols):
        return df
    candidate_values.columns = cols

    dates = pd.to_datetime(candidate_values["date"].astype(str), errors="coerce")
    signal_ids = candidate_values["signal_id"].astype(str).str.strip()
    if dates.notna().all() and signal_ids.ne("").all():
        return candidate_values
    return df


def _ledger_columns(path: Path = LEDGER_PATH) -> list[str]:
    if not path.exists():
        raise SystemExit(f"error: ledger not found: {path}")
    header = path.read_text(encoding="utf-8").splitlines()[0]
    return header.split(",")


def ensure_origin_column(path: Path = LEDGER_PATH) -> list[str]:
    """台帳ヘッダに origin 列が無ければ追加（既存行は空で埋める・冪等）。"""
    cols = _ledger_columns(path)
    if "origin" in cols:
        return cols
    lines = path.read_text(encoding="utf-8").rstrip("\n").split("\n")
    lines[0] = lines[0] + ",origin"
    lines[1:] = [l + "," for l in lines[1:]]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return cols + ["origin"]


def _anchor_close(asset: str, raw_dir: Path = RAW_DIR) -> float:
    p = raw_dir / f"{asset}.csv"
    if not p.exists():
        return float("nan")
    try:
        df = pd.read_csv(p)
        df.columns = [str(c).strip().lower() for c in df.columns]
        return float(pd.to_numeric(df["close"], errors="coerce").dropna().iloc[-1])
    except Exception:  # noqa: BLE001
        return float("nan")


def _raw_last_date(asset: str, raw_dir: Path = RAW_DIR):
    """資産の価格系列の最終バー日付。無ければ NaT。"""
    p = raw_dir / f"{asset}.csv"
    if not p.exists():
        return pd.NaT
    try:
        df = pd.read_csv(p)
        df.columns = [str(c).strip().lower() for c in df.columns]
        return pd.to_datetime(df["date"], errors="coerce").max()
    except Exception:  # noqa: BLE001
        return pd.NaT


def validate_row(row: pd.Series, existing_ids: set[str], raw_dir: Path = RAW_DIR) -> tuple[str, list[str]]:
    """(verdict, warnings) を返す。verdict: append / skip_duplicate / reject。"""
    warnings: list[str] = []
    sid = _s(row.get("signal_id"))
    if not sid:
        return "reject", ["signal_id が空"]
    reject_reason = _s(row.get(REJECT_COL))
    if reject_reason:
        return "reject", [reject_reason]
    note = _s(row.get(NOTE_COL))
    if note:
        warnings.append("補正: " + note)
    if sid in existing_ids:
        return "skip_duplicate", []
    date = pd.to_datetime(str(row.get("date") or ""), errors="coerce")
    if pd.isna(date):
        return "reject", [f"date が解釈不能: {row.get('date')!r}"]

    asset = str(row.get("asset") or "").strip()
    if not (raw_dir / f"{asset}.csv").exists():
        warnings.append(f"未知asset '{asset}' (価格系列なし -> 採点は invalid_data になる)")
    side = str(row.get("side") or "").strip().upper()
    if side and side not in KNOWN_SIDES:
        warnings.append(f"side '{side}' は既知enum外")
    rank = str(row.get("rank") or "").strip().upper()
    if rank and rank not in KNOWN_RANKS:
        warnings.append(f"rank '{rank}' は既知enum外")

    # 単位混在の入口検知: win_prob は 0〜1 の小数 (2026-07-01〜09 に %表記が24行混入した実績)
    win_prob = pd.to_numeric(row.get("win_prob"), errors="coerce")
    if pd.notna(win_prob) and not (0 <= float(win_prob) <= 1):
        warnings.append(f"win_prob {win_prob} が 0〜1 の範囲外 (%表記の疑い。契約は小数)")

    # actionable 整合 + 桁違い検知（QQQ水準事故の入口検知）
    entry_low = pd.to_numeric(row.get("entry_low"), errors="coerce")
    entry_high = pd.to_numeric(row.get("entry_high"), errors="coerce")
    sl = pd.to_numeric(row.get("sl"), errors="coerce")
    if side in {"BUY", "SELL", "LONG", "SHORT"}:
        if pd.isna(entry_low) or pd.isna(entry_high) or pd.isna(sl) or entry_low <= 0:
            warnings.append("方向ありなのに entry/SL が不完全 (方向Rは採点不能)")
        else:
            if entry_low > entry_high:
                warnings.append(f"entry_low({entry_low}) > entry_high({entry_high})")
            ref = (float(entry_low) + float(entry_high)) / 2
            if abs(ref - float(sl)) <= 0:
                warnings.append("risk_unit が 0 (reference == SL)")
            anchor = _anchor_close(asset, raw_dir)
            if not np.isnan(anchor) and anchor > 0:
                ratio = ref / anchor
                if ratio > 5 or ratio < 0.2:
                    warnings.append(
                        f"記録水準 {ref} が実価格 {anchor:.2f} と桁違い (x{ratio:.2f}) — "
                        "別商品の水準を記録していないか要確認 (採点では scale_mismatch 隔離)"
                    )
            # rr 自己整合検算 (#122 Codex P2: 2026-08-27 の3行で申告rrが記帳水準からの
            # 再計算(中点基準)と最大0.14乖離。過大側は B+ の RR>=1.5 条件を偽って満たす。
            # 台帳は申告値のまま記録し、乖離は取込時に警告として顕在化させる)
            tp1 = pd.to_numeric(row.get("tp1"), errors="coerce")
            rr = pd.to_numeric(row.get("rr"), errors="coerce")
            if pd.notna(tp1) and pd.notna(rr) and abs(ref - float(sl)) > 0:
                rr_calc = abs(float(tp1) - ref) / abs(ref - float(sl))
                if abs(rr_calc - float(rr)) > 0.10:
                    warnings.append(
                        f"rr {float(rr):.2f} が記帳水準からの再計算 {rr_calc:.2f} と乖離 (中点基準・許容0.10) — "
                        "申告のまま記録するが、RR条件(B+/A級)の判定には再計算値を優先すること"
                    )
    return "append", warnings


def ingest(text: str, *, origin: str, apply: bool, run_score: bool = True,
           ledger_path: Path = LEDGER_PATH, raw_dir: Path = RAW_DIR) -> dict:
    rows, fmt = extract_rows(text)
    result = {"format": fmt, "parsed": int(len(rows)), "appended": 0, "skipped_duplicate": 0,
              "rejected": 0, "warnings": 0, "applied": bool(apply), "origin": origin, "details": []}
    if rows.empty:
        result["error"] = "入力から行を抽出できなかった (csvブロック/生CSV/JSON配列のいずれか)"
        return result

    ledger_cols = ensure_origin_column(ledger_path) if apply else _ledger_columns(ledger_path)
    if "origin" not in ledger_cols:
        ledger_cols = ledger_cols + ["origin"]
    existing = pd.read_csv(ledger_path, dtype=str, keep_default_na=False)
    existing_ids = set(existing.get("signal_id", pd.Series(dtype=str)).astype(str))

    # 鮮度ガード: 取込む行の日付に対して価格系列が古すぎる場合は入口で大声で警告する。
    # data/raw は git 非追跡で CI が毎朝取得し直す設計のため、ローカルで fetch せずに
    # 採点すると古いバーで走る (7/23〜8/1 が全件 awaiting のまま 8/1 の OOS 判定を
    # 阻んだ事故の入口検知, 2026-08-02)。閾値6日は連休を許容しつつ1週間超の停止を捕まえる。
    STALE_RAW_MAX_LAG_DAYS = 6
    max_row_date = pd.to_datetime(rows.get("date"), errors="coerce").max()
    if pd.notna(max_row_date):
        stale = []
        for asset in sorted(set(rows.get("asset", pd.Series(dtype=str)).astype(str).str.strip()) - {""}):
            last = _raw_last_date(asset, raw_dir)
            if pd.notna(last) and (max_row_date - last).days > STALE_RAW_MAX_LAG_DAYS:
                stale.append(f"{asset}={last.date()}")
        if stale:
            result["stale_raw_warning"] = (
                f"価格系列が取込行({max_row_date.date()})より{STALE_RAW_MAX_LAG_DAYS}日超古い: "
                + ", ".join(stale) + " — このまま採点すると古いバーで走る。先に src/fetch_market.py を実行"
            )

    to_append: list[pd.Series] = []
    for _, row in rows.iterrows():
        verdict, warns = validate_row(row, existing_ids, raw_dir)
        detail = {"signal_id": str(row.get("signal_id") or "")[:40], "verdict": verdict, "warnings": warns}
        result["details"].append(detail)
        if verdict == "append":
            to_append.append(row)
            result["warnings"] += len(warns)
        elif verdict == "skip_duplicate":
            result["skipped_duplicate"] += 1
        else:
            result["rejected"] += 1

    if to_append and apply:
        add = pd.DataFrame(to_append)
        add["origin"] = origin
        _log_normalizations(add, origin, ledger_path)
        add = add.reindex(columns=ledger_cols, fill_value="")
        merged = pd.concat([existing.reindex(columns=ledger_cols, fill_value=""), add], ignore_index=True)
        merged.to_csv(ledger_path, index=False)
        result["appended"] = len(to_append)
        if run_score:
            import score_prediction_log
            score_prediction_log.main()
    elif to_append:
        result["appended"] = 0
        result["would_append"] = len(to_append)
    return result


def _log_normalizations(add: pd.DataFrame, origin: str, ledger_path: Path) -> int:
    """取込時に補正した行を、台帳の隣の追記型ログへ残す（原文の signal_id と補正内容）。

    台帳は申告値のまま記録するのが原則。語の置き場所や空欄の数だけを直した場合でも、
    直したことが後から追えないと「値は無修正」が嘘になる。本文の原文はアーカイブにある。
    """
    if NOTE_COL not in add.columns:
        return 0
    rows = add[add[NOTE_COL].astype(str).str.strip() != ""]
    if rows.empty:
        return 0
    path = ledger_path.parent / NORMALIZATION_LOG_NAME
    fields = ["date", "signal_id", "raw_signal_id", "note", "origin", "recorded_at"]
    have = set()
    if path.exists():
        with path.open(encoding="utf-8", newline="") as f:
            have = {r.get("signal_id", "") for r in csv.DictReader(f)}
    now = pd.Timestamp.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    new = [{"date": str(r.get("date", "")), "signal_id": str(r.get("signal_id", "")),
            "raw_signal_id": str(r.get(RAW_ID_COL, "") or ""), "note": str(r.get(NOTE_COL, "")),
            "origin": origin, "recorded_at": now}
           for _, r in rows.iterrows() if str(r.get("signal_id", "")) not in have]
    if not new:
        return 0
    write_header = not path.exists()
    with path.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if write_header:
            w.writeheader()
        w.writerows(new)
    return len(new)


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest a daily prediction log into data/signal_log.csv (validated).")
    parser.add_argument("--file", default=None, help="入力ファイル (省略時は stdin)")
    parser.add_argument("--origin", default="chatgpt_app", choices=sorted(ORIGINS),
                        help="この予測の生成経路 (成績の経路別比較に使う)")
    parser.add_argument("--apply", action="store_true",
                        help="実際に台帳へ追記する (省略時は dry-run プレビューのみ)")
    parser.add_argument("--no-score", action="store_true", help="追記後の自動採点を行わない")
    args = parser.parse_args()

    text = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
    result = ingest(text, origin=args.origin, apply=args.apply, run_score=not args.no_score)

    print(f"format={result['format']} parsed={result['parsed']} origin={result['origin']}")
    for d in result["details"]:
        mark = {"append": "+", "skip_duplicate": "=", "reject": "!"}[d["verdict"]]
        print(f" {mark} {d['signal_id']}: {d['verdict']}" + (f" | 警告: {'; '.join(d['warnings'])}" if d["warnings"] else ""))
    if result.get("stale_raw_warning"):
        print(f"!! STALE RAW DATA: {result['stale_raw_warning']}")
    if result.get("error"):
        print(f"error: {result['error']}")
        return 1
    if not result["applied"]:
        print(f"[dry-run] 追記候補 {result.get('would_append', 0)} 件。実行するには --apply を付ける")
    else:
        print(f"appended={result['appended']} skipped_dup={result['skipped_duplicate']} rejected={result['rejected']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
