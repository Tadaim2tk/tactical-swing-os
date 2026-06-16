"""JP個別株スイング — アドバーサリーレビューチェックリスト (JP-ADV-001)。

仮説を採用する前に、各質問に明示的に答えることを求める。
「答えられない」は「見送り推奨」を意味する（false-confidence ルール）。
"""

from __future__ import annotations

from typing import NamedTuple


class CheckItem(NamedTuple):
    id: str
    category: str
    question: str
    fail_signal: str    # これに当てはまれば採用しない
    severity: str       # critical / high / medium


# ── Layer 2 アドバーサリー質問（カタリスト解釈）─────────────────
CATALYST_CHECKS: list[CheckItem] = [
    CheckItem(
        id="ADV-JP-001",
        category="catalyst",
        question="このカタリストは一過性（単発イベント）か、構造変化か？",
        fail_signal="一過性なのに数週間の保有を前提にしている",
        severity="critical",
    ),
    CheckItem(
        id="ADV-JP-002",
        category="catalyst",
        question="市場がこのカタリストをまだ十分に解釈していない根拠は何か？",
        fail_signal="「まだ知られていないはず」という根拠が希望的観測のみ",
        severity="critical",
    ),
    CheckItem(
        id="ADV-JP-003",
        category="catalyst",
        question="決算短信 / 開示資料を実際に読んだか？ 数字ではなくトーンの変化はあったか？",
        fail_signal="SNS・スクリーナーのサマリー情報のみで判断している",
        severity="high",
    ),
    CheckItem(
        id="ADV-JP-004",
        category="catalyst",
        question="同業他社と比較して、今この銘柄が動く理由はあるか（相対優位）？",
        fail_signal="セクター全体が動いているだけで個別の優位性がない",
        severity="high",
    ),
    CheckItem(
        id="ADV-JP-005",
        category="catalyst",
        question="「この銘柄を今から買う人」が増える具体的な筋道を描けるか？",
        fail_signal="「いつかは上がる」という根拠しか言えない",
        severity="high",
    ),
]

# ── Layer 3 アドバーサリー質問（執行可能性）─────────────────────
EXECUTION_CHECKS: list[CheckItem] = [
    CheckItem(
        id="ADV-JP-011",
        category="execution",
        question="直近3営業日で既に大きく上昇しているか？ラグ1日後に不利約定にならないか？",
        fail_signal="直近3日で+5%以上かつ急出来高あり",
        severity="critical",
    ),
    CheckItem(
        id="ADV-JP-012",
        category="execution",
        question="1株当たり株価 × 手数料率が最低手数料（52円）を下回っていないか？",
        fail_signal="1株コストが最低手数料に支配される水準（数千円台低位株）",
        severity="critical",
    ),
    CheckItem(
        id="ADV-JP-013",
        category="execution",
        question="TP1までの距離がSL距離の1.5倍以上あるか？",
        fail_signal="R比率が1.5未満",
        severity="critical",
    ),
    CheckItem(
        id="ADV-JP-014",
        category="execution",
        question="SLを設定した根拠（テクニカル的な意味のある水準）はあるか？",
        fail_signal="「何となく -5%」「直近安値 -少し」など根拠が曖昧",
        severity="high",
    ),
    CheckItem(
        id="ADV-JP-015",
        category="execution",
        question="horizon_days 内に株価が動くトリガー（イベント・需給）があるか？",
        fail_signal="特に何もないが上がるはずというだけ",
        severity="medium",
    ),
]

# ── 仮説品質チェック ─────────────────────────────────────────────
HYPOTHESIS_CHECKS: list[CheckItem] = [
    CheckItem(
        id="ADV-JP-021",
        category="hypothesis",
        question="Falsifierを具体的に1文で書けるか？（「株価が下がったら」は不可）",
        fail_signal="Falsifierが価格変動のみで仮説崩壊の根拠になっていない",
        severity="critical",
    ),
    CheckItem(
        id="ADV-JP-022",
        category="hypothesis",
        question="この仮説で負けるシナリオを3つ挙げられるか？",
        fail_signal="1つも思い浮かばない（過信の兆候）",
        severity="high",
    ),
    CheckItem(
        id="ADV-JP-023",
        category="hypothesis",
        question="似た過去の仮説（同銘柄・同カタリスト種別）でどんな結果だったか？",
        fail_signal="実績がないのに高い確信度（70%超）を設定している",
        severity="medium",
    ),
    CheckItem(
        id="ADV-JP-024",
        category="hypothesis",
        question="仮説形成は決算資料等の情報入手後か？（ナラティブ先読みバイアスチェック）",
        fail_signal="情報を見る前に「上がりそう」と思っていた",
        severity="high",
    ),
]

ALL_CHECKS: list[CheckItem] = CATALYST_CHECKS + EXECUTION_CHECKS + HYPOTHESIS_CHECKS


def run_checklist(answers: dict[str, str]) -> dict[str, list[dict[str, str]]]:
    """チェックリストに対する回答を評価する。

    answers: {check_id: "pass" | "fail" | "n/a"} の辞書。
    返値: {"critical_fails": [...], "high_fails": [...], "medium_fails": [...], "missing": [...]}
    """
    result: dict[str, list[dict[str, str]]] = {
        "critical_fails": [],
        "high_fails": [],
        "medium_fails": [],
        "missing": [],
    }
    for item in ALL_CHECKS:
        ans = str(answers.get(item.id, "")).strip().lower()
        entry = {"id": item.id, "question": item.question, "fail_signal": item.fail_signal}
        if ans == "fail":
            result[f"{item.severity}_fails"].append(entry)
        elif ans == "" or ans not in {"pass", "fail", "n/a"}:
            result["missing"].append(entry)
    return result


def adoption_decision(answers: dict[str, str]) -> dict[str, str]:
    """採用/見送りの推奨を返す。

    critical_fails が 1 件でもあれば採用禁止。
    high_fails が 2 件以上あれば見送り推奨。
    """
    r = run_checklist(answers)
    n_critical = len(r["critical_fails"])
    n_high = len(r["high_fails"])
    n_missing = len(r["missing"])

    if n_critical >= 1:
        decision = "blocked"
        reason = f"critical fail {n_critical}件。採用禁止。Falsifier・ラグ・コスト・R比率を再確認してください。"
    elif n_high >= 2:
        decision = "pass_recommended"
        reason = f"high fail {n_high}件。見送り推奨。pass_log に記録して学習資産にしてください。"
    elif n_missing >= 3:
        decision = "insufficient_data"
        reason = f"回答未記入 {n_missing}件。全項目に明示的に答えてから再判断してください。"
    else:
        decision = "adopt_eligible"
        reason = f"critical fail 0件、high fail {n_high}件、missing {n_missing}件。採用条件を満たします。"

    return {
        "decision": decision,
        "reason": reason,
        "critical_fails": n_critical,
        "high_fails": n_high,
        "medium_fails": len(r["medium_fails"]),
        "missing": n_missing,
    }


def checklist_text() -> str:
    """チェックリストのテキスト一覧を返す（確認・コピー用）。"""
    lines = ["JP One-Share Swing — Adversarial Checklist\n"]
    for item in ALL_CHECKS:
        lines.append(f"[{item.id}] [{item.severity.upper()}] {item.question}")
        lines.append(f"  ✗ 該当すれば見送り: {item.fail_signal}\n")
    return "\n".join(lines)
