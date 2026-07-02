from __future__ import annotations

"""シグナル発生時点のナラティブ整合判定を追記専用CSVへ保存する (SPEC-NQ-001)。

憲章「予測→保存→後日採点」の実装:
- 整合判定はシグナル当日の市場データで計算し、その場で記録する
- 既存レコードは決して上書きしない(最初の記録が正)
- 後からの再計算は後知恵バイアスを生むため禁止
"""

from pathlib import Path

import pandas as pd

try:
    import score_market_context as score_narratives
except Exception:  # noqa: BLE001 - 整合記録は任意機能。importfailで日次サイクルを止めない
    score_narratives = None
from calibration_io import read_csv
from time_utils import format_jst, format_utc, now_utc


RESULTS_DIR = Path("results")
SIGNALS_CSV = RESULTS_DIR / "signals.csv"
MARKET_CSV = RESULTS_DIR / "market_snapshot.csv"
ALIGNMENT_CSV = RESULTS_DIR / "signal_narrative_alignment.csv"
ALIGNMENT_COLUMNS = [
    "signal_id",
    "asset",
    "side",
    "rank",
    "narrative_alignment",
    "narrative_alignment_score",
    "narrative_comment",
    "recorded_at_jst",
    "recorded_at_utc",
]


def load_existing() -> pd.DataFrame:
    existing = read_csv(ALIGNMENT_CSV)
    if existing.empty:
        return pd.DataFrame(columns=ALIGNMENT_COLUMNS)
    return existing


def export_alignment() -> pd.DataFrame:
    generated_dt_utc = now_utc()
    recorded_at_jst = format_jst(generated_dt_utc)
    recorded_at_utc = format_utc(generated_dt_utc)

    signals = read_csv(SIGNALS_CSV)
    market = read_csv(MARKET_CSV)
    existing = load_existing()
    existing_ids = set(existing.get("signal_id", pd.Series(dtype=str)).astype(str)) if not existing.empty else set()

    if signals.empty:
        print("signals.csv is empty; nothing to record")
        return existing

    # 防御: score_market_contextに必要な関数が無いバージョンでも安全に劣化する
    if score_narratives is None or not (hasattr(score_narratives, "score_market_narratives") and hasattr(score_narratives, "evaluate_signal_alignment")):
        print("score_market_context does not expose alignment functions; skipping (alignment CSV unchanged)")
        return existing

    scores = score_narratives.score_market_narratives(market)
    alignment = score_narratives.evaluate_signal_alignment(signals, scores)
    if alignment.empty:
        print("no alignment rows computed")
        return existing

    alignment = alignment.copy()
    alignment["recorded_at_jst"] = recorded_at_jst
    alignment["recorded_at_utc"] = recorded_at_utc
    # 追記専用: 既に記録済みのsignal_idは決して更新しない(最初の記録が正)
    new_rows = alignment[~alignment["signal_id"].astype(str).isin(existing_ids)]
    new_rows = new_rows[[col for col in ALIGNMENT_COLUMNS if col in new_rows.columns]]

    combined = pd.concat([existing, new_rows], ignore_index=True) if not new_rows.empty else existing
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    combined.to_csv(ALIGNMENT_CSV, index=False)
    print(f"narrative alignment recorded: +{len(new_rows)} rows (total {len(combined)})")
    print("append-only: existing records were not modified")
    return combined


def main() -> int:
    export_alignment()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
