"""Append generated daily signals into the official signal ledger.

This bridges the automated daily generator output (`results/signals.csv`) into
`data/signal_log.csv`, which is the durable input used by weekly reviews and
prediction scoring. The append is intentionally conservative:

- append only new `signal_id` values
- preserve existing ledger rows
- expand the ledger header for newly generated columns
- mark rows with `origin=daily_cycle`
- write a machine-readable summary for dashboard/audit diagnostics
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


SIGNALS_PATH = Path("results/signals.csv")
LEDGER_PATH = Path("data/signal_log.csv")
SUMMARY_PATH = Path("results/signal_ledger_append_summary.json")
DEFAULT_ORIGIN = "daily_cycle"


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path, dtype=str, keep_default_na=False)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _json_safe(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:  # noqa: BLE001
            pass
    return str(value)


def _write_summary(payload: dict[str, Any], path: Path = SUMMARY_PATH) -> None:
    _ensure_parent(path)
    clean = {str(k): _json_safe(v) for k, v in payload.items()}
    path.write_text(json.dumps(clean, ensure_ascii=False, indent=2), encoding="utf-8")


def _ordered_union(ledger_columns: list[str], signal_columns: list[str]) -> list[str]:
    """Return a stable ledger schema that keeps existing columns first.

    New columns from generated signals are appended before trailing audit columns
    when possible. This keeps legacy readers stable while allowing Phase-6 fields
    from `results/signals.csv` to survive in the durable ledger.
    """
    audit_tail = [col for col in ["verified_status", "origin"] if col in ledger_columns]
    base = [col for col in ledger_columns if col not in audit_tail]
    missing_from_signals = [col for col in signal_columns if col not in ledger_columns]
    out = base + missing_from_signals + audit_tail
    for required in ["verified_status", "origin"]:
        if required not in out:
            out.append(required)
    return out


def append_generated_signals(
    signals_path: Path = SIGNALS_PATH,
    ledger_path: Path = LEDGER_PATH,
    summary_path: Path = SUMMARY_PATH,
    origin: str = DEFAULT_ORIGIN,
) -> dict[str, Any]:
    signals = _read_csv(signals_path)
    result: dict[str, Any] = {
        "status": "skipped",
        "signals_path": str(signals_path),
        "ledger_path": str(ledger_path),
        "signals_rows": int(len(signals)),
        "appended_rows": 0,
        "skipped_duplicates": 0,
        "rejected_rows": 0,
        "origin": origin,
        "error": "",
    }

    if signals.empty:
        result["error"] = f"{signals_path} missing or empty"
        _write_summary(result, summary_path)
        print(f"warning: {result['error']}")
        return result
    if "signal_id" not in signals.columns:
        result.update({"status": "failed", "error": "results/signals.csv has no signal_id column"})
        _write_summary(result, summary_path)
        print(f"error: {result['error']}")
        return result
    if "date" not in signals.columns:
        result.update({"status": "failed", "error": "results/signals.csv has no date column"})
        _write_summary(result, summary_path)
        print(f"error: {result['error']}")
        return result

    valid_mask = signals["signal_id"].astype(str).str.strip().ne("") & signals["date"].astype(str).str.strip().ne("")
    rejected = signals.loc[~valid_mask]
    signals = signals.loc[valid_mask].copy()
    result["rejected_rows"] = int(len(rejected))

    if ledger_path.exists():
        ledger = _read_csv(ledger_path)
    else:
        ledger = pd.DataFrame()

    existing_ids: set[str] = set()
    if not ledger.empty and "signal_id" in ledger.columns:
        existing_ids = set(ledger["signal_id"].astype(str))

    new_rows = signals.loc[~signals["signal_id"].astype(str).isin(existing_ids)].copy()
    result["skipped_duplicates"] = int(len(signals) - len(new_rows))

    ledger_columns = list(ledger.columns) if not ledger.empty else list(signals.columns)
    final_columns = _ordered_union(ledger_columns, list(signals.columns))

    if not new_rows.empty:
        if "verified_status" not in new_rows.columns:
            new_rows["verified_status"] = "unverified"
        else:
            new_rows["verified_status"] = new_rows["verified_status"].replace("", "unverified")
        new_rows["origin"] = origin

    merged = pd.concat(
        [ledger.reindex(columns=final_columns, fill_value=""), new_rows.reindex(columns=final_columns, fill_value="")],
        ignore_index=True,
    )

    # Write even when only the schema expanded; otherwise historical rows can
    # continue to hide generated Phase-6 columns from future review tools.
    _ensure_parent(ledger_path)
    merged.to_csv(ledger_path, index=False)

    result["appended_rows"] = int(len(new_rows))
    result["status"] = "success" if len(new_rows) or final_columns != ledger_columns else "skipped"
    result["ledger_rows_after"] = int(len(merged))
    result["ledger_columns_after"] = int(len(final_columns))
    result["latest_signal_date"] = str(pd.to_datetime(signals["date"], errors="coerce").max().date())
    _write_summary(result, summary_path)

    print(
        "signal ledger append: "
        f"status={result['status']} parsed={result['signals_rows']} "
        f"appended={result['appended_rows']} duplicates={result['skipped_duplicates']} "
        f"rejected={result['rejected_rows']}"
    )
    return result


def main() -> int:
    result = append_generated_signals()
    return 1 if result.get("status") == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
