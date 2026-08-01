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
import io
import json
import re
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


def extract_rows(text: str) -> tuple[pd.DataFrame, str]:
    """入力テキストから行を抽出。(DataFrame, 形式名) を返す。失敗は空DF。"""
    text = text.strip()
    # 1) JSON 配列
    if text.startswith("["):
        try:
            data = json.loads(text)
            if isinstance(data, list) and data and isinstance(data[0], dict):
                return pd.DataFrame(data), "json"
        except json.JSONDecodeError:
            pass
    # 2) Markdown 中の ```csv ブロック（複数あれば結合）
    blocks = CSV_BLOCK_RE.findall(text)
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
            df = pd.read_csv(io.StringIO(text), dtype=str, keep_default_na=False)
            return _repair_extra_blank_before_tq_score(df)
        # ヘッダ無し: 台帳ヘッダ(origin除く)を仮定して読めるか試す
        ledger_cols = _ledger_columns()
        base_cols = [c for c in ledger_cols if c != "origin"]
        df = pd.read_csv(io.StringIO(text), dtype=str, keep_default_na=False, header=None)
        if len(df.columns) == len(base_cols):
            df.columns = base_cols
            return df
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
    sid = str(row.get("signal_id") or "").strip()
    if not sid:
        return "reject", ["signal_id が空"]
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
