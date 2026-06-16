"""JP One-Share Swing Ledger (JP-LEDGER-001)。

JP個別株スイング仮説の記録・検証・振り返り台帳。

台帳の設計原則:
- 仮説ログ (jp_swing_signals.csv): 採用した仮説の全ライフサイクルを記録。
- 見送りログ (jp_swing_pass_log.csv): 検討したが見送った銘柄を記録（学習資産）。
- 台帳は入力データとして git 管理する（results/ の生成物とは別）。
- 採用条件の 4 edge: Narrative / Time / Price / Risk 全てを記録フォームに含める。
- outcome は 6 分類 (A〜F) で根本原因を分離する。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

DATA_DIR = Path("data")
SIGNALS_PATH = DATA_DIR / "jp_swing_signals.csv"
PASS_LOG_PATH = DATA_DIR / "jp_swing_pass_log.csv"

# ── 採用仮説台帳 ─────────────────────────────────────────────────
JP_SIGNAL_COLUMNS: list[str] = [
    # 基本識別
    "hypothesis_id",          # JP-YYYYMMDD-NNN
    "hypothesis_date",        # 仮説形成日 (YYYY-MM-DD)
    "ticker",                 # e.g. "7203.T"
    "company_name",           # e.g. "トヨタ自動車"
    "sector",                 # e.g. "輸送用機器"
    # Layer 1: 機械的スクリーニング
    "l1_rs_vs_topix_20d",     # TOPIX比 相対強度 20日 (float, 正で優位)
    "l1_volume_ratio_20d",    # 出来高/20日平均 (float, 1.5以上で合格目安)
    "l1_days_since_catalyst", # カタリスト発生からの日数 (int)
    "l1_price_chg_3d_pct",    # 直近3日騰落率% (float, 急騰チェック)
    "l1_price_chg_5d_pct",    # 直近5日騰落率% (float)
    # Layer 2: カタリスト解釈
    "narrative",              # なぜ今この株が動くか (1〜2文)
    "catalyst_type",          # earnings_beat/structural_change/theme/pricing_power/
                              # order_backlog/margin_improvement/other
    "catalyst_permanence",    # one_time/multi_week/structural
    "market_misread",         # 市場が誤読・未評価していると思われる点
    "narrative_edge",         # まだ解釈が広まっていない根拠
    "time_edge",              # なぜ今が旬か（早すぎず遅すぎない理由）
    # Layer 3: 執行可能性チェック
    "falsifier",              # 仮説崩壊条件（事前決定）
    "horizon_days",           # 10/20/30 (営業日)
    "confidence_pct",         # 0-100
    "l3_lag_survivable",      # 1日ラグ後も期待値が残るか (bool)
    "l3_min_fee_ok",          # 最低手数料負けしないか (bool)
    "l3_r_ratio",             # TP1到TP1距離/SL距離 (float, 1.5以上が目安)
    "l3_post_spike",          # 直近3日以内に急騰か (bool, True=危険)
    # 注文・約定
    "order_date",             # 注文日
    "expected_entry_price",   # 想定約定価格（翌営業日寄付推定）
    "actual_entry_date",      # 実際の約定日
    "actual_entry_price",     # 実際の約定価格
    "shares",                 # 株数
    "sl_price",               # SL価格
    "tp1_price",              # TP1価格
    "tp2_price",              # TP2価格 (任意)
    # 評価（約定後〜決済後に記入）
    "exit_date",
    "exit_price",
    "exit_reason",            # sl_hit/tp1_hit/tp2_hit/time_exit/manual_exit
    "holding_days",           # 実際の保有営業日数
    "buy_fee_jpy",            # 買い手数料（円）
    "sell_fee_jpy",           # 売り手数料（円）
    "gross_pnl_jpy",          # グロスPnL（円）
    "net_pnl_jpy",            # ネットPnL（円）
    "risk_jpy",               # リスク金額 (entry-sl)*shares
    "gross_r",                # グロスR
    "net_r",                  # ネットR
    "outcome_type",           # A/B/C/D/E/F (下記 OUTCOME_TYPES 参照)
    "thesis_correct",         # 仮説が正しかったか (bool, 人間が記入)
    "timing_correct",         # タイミングが正しかったか (bool, 人間が記入)
    "execution_degraded",     # ラグ/手数料で大きく不利化したか (bool)
    "outcome_note",           # 振り返りメモ
    "status",                 # pending/open/closed
]

# ── 見送りログ ────────────────────────────────────────────────────
JP_PASS_LOG_COLUMNS: list[str] = [
    "pass_id",                # PASS-YYYYMMDD-NNN
    "assessment_date",        # 検討日
    "ticker",
    "company_name",
    "sector",
    "pass_layer",             # layer1/layer2/layer3 (どの層で落ちたか)
    "pass_reason",            # too_chased/lag_kills_edge/min_fee_unviable/
                              # low_rr/no_falsifier/unclear_narrative/
                              # low_confidence/screening_failed/other
    "pass_detail",            # 見送り理由の詳細説明
    "catalyst_type",          # もし採用検討に達した場合のカタリスト種別
    "confidence_pct",         # もし採用していたとしたら何%か
    # 事後フォローアップ（~20営業日後に記入）
    "followup_date",
    "price_at_pass",          # 見送り時点の株価
    "price_at_followup",      # 追跡時の株価
    "change_pct",             # 騰落率
    "retrospective",          # win/loss/flat/unknown
    "lesson",                 # 学び・次回への注意点
]

# ── outcome 6分類 ─────────────────────────────────────────────────
OUTCOME_TYPES: dict[str, str] = {
    "A": "Thesis win — 仮説どおりに伸び、TP1/TP2 を達成した",
    "B": "Timing miss — 仮説は正しいがタイミングが早すぎ/遅すぎでSLに当たった",
    "C": "Execution loss — ラグ・手数料・寄付ギャップで仮説と無関係に負けた",
    "D": "Thesis fail — 仮説そのものが間違っていた",
    "E": "Market regime — 地合い悪化・マクロ変動で潰された（仮説は中立〜正しかった）",
    "F": "Lucky win — 仮説外の理由で価格が動いてTP達成（過信しない）",
}

# ── バリデーション ───────────────────────────────────────────────
VALID_CATALYST_TYPES = {
    "earnings_beat", "structural_change", "theme", "pricing_power",
    "order_backlog", "margin_improvement", "other",
}
VALID_CATALYST_PERMANENCE = {"one_time", "multi_week", "structural"}
VALID_HORIZON_DAYS = {10, 20, 30}
VALID_EXIT_REASONS = {"sl_hit", "tp1_hit", "tp2_hit", "time_exit", "manual_exit"}
VALID_PASS_LAYERS = {"layer1", "layer2", "layer3"}
VALID_PASS_REASONS = {
    "too_chased", "lag_kills_edge", "min_fee_unviable", "low_rr",
    "no_falsifier", "unclear_narrative", "low_confidence", "screening_failed", "other",
}
VALID_STATUSES = {"pending", "open", "closed"}


def validate_signal_row(row: dict[str, Any]) -> list[str]:
    """仮説台帳の1行を検証し、問題点のリストを返す（空リストなら合格）。"""
    errors: list[str] = []

    def req(field: str) -> None:
        v = row.get(field)
        if v is None or str(v).strip() == "" or str(v).lower() == "nan":
            errors.append(f"必須フィールドが空: {field}")

    req("hypothesis_id")
    req("hypothesis_date")
    req("ticker")
    req("narrative")
    req("falsifier")
    req("horizon_days")
    req("confidence_pct")
    req("status")

    hd = row.get("horizon_days")
    try:
        if int(hd) not in VALID_HORIZON_DAYS:
            errors.append(f"horizon_days は {VALID_HORIZON_DAYS} のいずれかにしてください: {hd}")
    except (TypeError, ValueError):
        errors.append(f"horizon_days が数値ではありません: {hd}")

    cp = row.get("confidence_pct")
    try:
        v = float(cp)
        if not (0.0 <= v <= 100.0):
            errors.append(f"confidence_pct は 0〜100 の範囲にしてください: {cp}")
    except (TypeError, ValueError):
        errors.append(f"confidence_pct が数値ではありません: {cp}")

    ct = row.get("catalyst_type")
    if ct and str(ct).strip() not in VALID_CATALYST_TYPES:
        errors.append(f"catalyst_type が不明: {ct}。有効値: {VALID_CATALYST_TYPES}")

    perm = row.get("catalyst_permanence")
    if perm and str(perm).strip() not in VALID_CATALYST_PERMANENCE:
        errors.append(f"catalyst_permanence が不明: {perm}")

    ot = row.get("outcome_type")
    if ot and str(ot).strip() and str(ot).strip() not in OUTCOME_TYPES:
        errors.append(f"outcome_type が不明: {ot}。有効値: {set(OUTCOME_TYPES.keys())}")

    st = row.get("status")
    if st and str(st).strip() not in VALID_STATUSES:
        errors.append(f"status が不明: {st}")

    # 必須 Falsifier が empty text でないか（ "未定" 等は拒否）
    falsifier = str(row.get("falsifier", "")).strip().lower()
    if falsifier in {"", "未定", "tbd", "none", "nan"}:
        errors.append("falsifier が未記入です。事前に仮説崩壊条件を決めてください。")

    return errors


def validate_pass_row(row: dict[str, Any]) -> list[str]:
    """見送りログの1行を検証し、問題点のリストを返す。"""
    errors: list[str] = []

    def req(field: str) -> None:
        v = row.get(field)
        if v is None or str(v).strip() == "" or str(v).lower() == "nan":
            errors.append(f"必須フィールドが空: {field}")

    req("pass_id")
    req("assessment_date")
    req("ticker")
    req("pass_reason")
    req("pass_detail")

    pl = row.get("pass_layer")
    if pl and str(pl).strip() not in VALID_PASS_LAYERS:
        errors.append(f"pass_layer が不明: {pl}")

    pr = row.get("pass_reason")
    if pr and str(pr).strip() not in VALID_PASS_REASONS:
        errors.append(f"pass_reason が不明: {pr}。有効値: {VALID_PASS_REASONS}")

    return errors


# ── I/O ──────────────────────────────────────────────────────────

def load_signals(path: Path = SIGNALS_PATH) -> pd.DataFrame:
    """仮説台帳を読み込む。ファイルがなければ空DFを返す。"""
    if not path.exists():
        return pd.DataFrame(columns=JP_SIGNAL_COLUMNS)
    try:
        df = pd.read_csv(path, dtype=str)
    except (pd.errors.EmptyDataError, OSError):
        return pd.DataFrame(columns=JP_SIGNAL_COLUMNS)
    for col in JP_SIGNAL_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df[JP_SIGNAL_COLUMNS]


def load_pass_log(path: Path = PASS_LOG_PATH) -> pd.DataFrame:
    """見送りログを読み込む。ファイルがなければ空DFを返す。"""
    if not path.exists():
        return pd.DataFrame(columns=JP_PASS_LOG_COLUMNS)
    try:
        df = pd.read_csv(path, dtype=str)
    except (pd.errors.EmptyDataError, OSError):
        return pd.DataFrame(columns=JP_PASS_LOG_COLUMNS)
    for col in JP_PASS_LOG_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df[JP_PASS_LOG_COLUMNS]


def save_signals(df: pd.DataFrame, path: Path = SIGNALS_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def save_pass_log(df: pd.DataFrame, path: Path = PASS_LOG_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def validate_signals_df(df: pd.DataFrame) -> list[dict[str, Any]]:
    """台帳全行を検証し、問題のある行の情報を返す。"""
    all_issues: list[dict[str, Any]] = []
    for i, row in df.iterrows():
        errors = validate_signal_row(row.to_dict())
        if errors:
            all_issues.append({"row_index": i, "hypothesis_id": row.get("hypothesis_id", ""), "errors": errors})
    return all_issues


def validate_pass_log_df(df: pd.DataFrame) -> list[dict[str, Any]]:
    """見送りログ全行を検証し、問題のある行の情報を返す。"""
    all_issues: list[dict[str, Any]] = []
    for i, row in df.iterrows():
        errors = validate_pass_row(row.to_dict())
        if errors:
            all_issues.append({"row_index": i, "pass_id": row.get("pass_id", ""), "errors": errors})
    return all_issues
