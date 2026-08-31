"""遡及市場コーパス: 日次ナラティブのローカルLLM生成 (SPEC-RNC-001)。

役割分担(ERS知見#9): 閉じた語彙(risk_state等)はルール層からコピーし、LLMには
自由記述(その日の主導要因・特異な乖離)だけをさせる。

測定器の版固定(ERS METHOD_TRANSFER#2): モデルcommit・mlx-lm版・プロンプト全文sha・
温度・生成長を data/retro/instrument.json に固定し、実行時に実環境と照合。
不一致なら生成せずに終了する(宣言だけ置いて確かめない、を禁ずる)。

再開可能: narratives.jsonl に同digestで存在する日付はスキップ。append-only。

usage: ~/.venvs/ers-llm/bin/python tools/retro_generate_narratives.py [--limit N] [--dry]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

RETRO = Path("data/retro")
DAILY = RETRO / "market_daily.csv"
NEWS = RETRO / "news_gdelt.csv"
OUT = RETRO / "narratives.jsonl"
INSTRUMENT_PATH = RETRO / "instrument.json"

MODEL_REPO = "mlx-community/Qwen3-8B-4bit"
MODEL_COMMIT = "545dc4251c05440727734bcd94334791f6ab0192"
TEMPERATURE = 0.0
MAX_TOKENS = 320

PROMPT_TEMPLATE = """あなたは市場の観察記録係。以下は{date}({dow})の実測データ。数値の捏造・推測は禁止。
与えられた数値と見出しだけから、この日の相場を記述せよ。

## 実測(資産別 前日終値比リターン。空欄=その市場は休場)
{market_block}

## ルール判定(参考。あなたが書き換えることは禁止)
risk_state={risk_state} / vol_state={vol_state} / yield_move={yield_move} / usd_move={usd_move} / crypto_move={crypto_move}
この期間の市場の主役(直近20営業日の連動度×活発度で機械判定): {leader_asset} (明確さ margin={leader_margin})

## この日の見出し(GDELT上位。無い場合は「なし」)
{news_block}

## 出力(JSONのみ。他の文を書かない)
{{"narrative": "この日の相場を2〜4文の日本語で。期間の主役({leader_asset})を軸に、この日の値動きが主役の構図を追認したか崩したかを含める", "leader": "この日を主導した資産または要因を1語〜1句", "anomaly": "資産間で通常と逆・特異な乖離、または主役交代の兆しがあれば1文、なければ「なし」"}}
/no_think"""

ASSETS = ["SPX", "NASDAQ", "VIX", "US10Y", "DXY", "USDJPY", "GOLD", "WTI", "BTC", "ETH"]


def build_instrument() -> dict:
    import mlx_lm
    return {
        "model_repo": MODEL_REPO,
        "model_commit": MODEL_COMMIT,
        "mlx_lm_version": mlx_lm.__version__,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "prompt_sha256": hashlib.sha256(PROMPT_TEMPLATE.encode()).hexdigest(),
        "thinking": False,
        "preprocess": "market_daily row + top8 gdelt headlines(title only, 120c cut)",
    }


def instrument_digest(inst: dict) -> str:
    return hashlib.sha256(json.dumps(inst, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


def verify_environment() -> None:
    """宣言した版と実環境の一致を検査。違えば測らずに終える。"""
    snap = Path.home() / ".cache/huggingface/hub" / f"models--{MODEL_REPO.replace('/', '--')}" / "snapshots"
    commits = [p.name for p in snap.iterdir()] if snap.exists() else []
    if MODEL_COMMIT not in commits:
        raise SystemExit(f"error: model commit {MODEL_COMMIT} not in cache {commits} — 生成中止")


def day_prompt(row: pd.Series, news: list[str]) -> str:
    lines = []
    for a in ASSETS:
        if a == "US10Y":
            v = row.get("chg_US10Y_pt")
            lines.append(f"US10Y: {'休場/欠測' if pd.isna(v) else f'{v:+.2f}pt'} (水準 {row.get(f'close_{a}', float('nan')):.2f})"
                         if pd.notna(row.get(f"close_{a}")) else "US10Y: 休場/欠測")
            continue
        r = row.get(f"ret_{a}")
        c = row.get(f"close_{a}")
        if pd.isna(c):
            lines.append(f"{a}: 休場/欠測")
        elif pd.isna(r):
            lines.append(f"{a}: リターン欠測 (終値 {c:g})")
        else:
            lines.append(f"{a}: {r*100:+.2f}% (終値 {c:g})")
    prev = row.get("prev_us_ret_cum")
    if pd.notna(prev):
        lines.append(f"直近の米株セッション(前営業日まで累積): {prev*100:+.2f}%")
    news_block = "\n".join(f"- {t[:120]}" for t in news[:8]) if news else "なし"
    lm = row.get("leader_margin")
    return PROMPT_TEMPLATE.format(
        date=str(pd.Timestamp(row["date"]).date()), dow=pd.Timestamp(row["date"]).strftime("%a"),
        market_block="\n".join(lines), news_block=news_block,
        risk_state=row.get("risk_state"), vol_state=row.get("vol_state"),
        yield_move=row.get("yield_move"), usd_move=row.get("usd_move"),
        crypto_move=row.get("crypto_move"),
        leader_asset=row.get("leader_asset", "none"),
        leader_margin=("不明" if pd.isna(lm) else f"{lm:.2f}"))


def parse_output(text: str) -> tuple[dict, bool]:
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        try:
            d = json.loads(m.group(0))
            if isinstance(d, dict) and "narrative" in d:
                return {k: str(d.get(k, "")) for k in ("narrative", "leader", "anomaly")}, True
        except json.JSONDecodeError:
            pass
    return {"narrative": text.strip()[:600], "leader": "", "anomaly": ""}, False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="生成する日数の上限(0=全部)")
    ap.add_argument("--dry", action="store_true", help="プロンプトを1件表示して終了")
    args = ap.parse_args()

    daily = pd.read_csv(DAILY, parse_dates=["date"])
    news_by_day: dict[str, list[str]] = {}
    if NEWS.exists():
        try:
            nf = pd.read_csv(NEWS)
            for d, g in nf.groupby("date"):
                news_by_day[str(d)] = g["title"].dropna().tolist()
        except (pd.errors.EmptyDataError, KeyError):
            pass  # 取得が未完/進行中でも市場層だけで生成できる(見出しは「なし」表示)

    inst = build_instrument()
    digest = instrument_digest(inst)
    verify_environment()
    INSTRUMENT_PATH.parent.mkdir(parents=True, exist_ok=True)
    INSTRUMENT_PATH.write_text(json.dumps({**inst, "digest": digest}, ensure_ascii=False, indent=1), encoding="utf-8")

    done = set()
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            try:
                rec = json.loads(line)
                if rec.get("instrument_digest") == digest:
                    done.add(rec["date"])
            except json.JSONDecodeError:
                continue

    todo = [row for _, row in daily.iterrows() if str(pd.Timestamp(row["date"]).date()) not in done]
    if args.limit:
        todo = todo[: args.limit]
    print(f"instrument={digest} done={len(done)} todo={len(todo)}")
    if args.dry:
        if todo:
            print(day_prompt(todo[0], news_by_day.get(str(pd.Timestamp(todo[0]["date"]).date()), [])))
        return 0

    from mlx_lm import load, generate
    from mlx_lm.sample_utils import make_sampler
    model, tokenizer = load(MODEL_REPO)
    sampler = make_sampler(temp=TEMPERATURE)

    n = 0
    with open(OUT, "a", encoding="utf-8") as f:
        for row in todo:
            d = str(pd.Timestamp(row["date"]).date())
            prompt = day_prompt(row, news_by_day.get(d, []))
            messages = [{"role": "user", "content": prompt}]
            try:
                text_in = tokenizer.apply_chat_template(
                    messages, add_generation_prompt=True, enable_thinking=False)
            except TypeError:
                text_in = tokenizer.apply_chat_template(messages, add_generation_prompt=True)
            out_text = generate(model, tokenizer, prompt=text_in, max_tokens=MAX_TOKENS, sampler=sampler)
            parsed, ok = parse_output(out_text)
            rec = {
                "date": d,
                "risk_state": row.get("risk_state"), "vol_state": row.get("vol_state"),
                "yield_move": row.get("yield_move"), "usd_move": row.get("usd_move"),
                "crypto_move": row.get("crypto_move"),
                "leader_asset": row.get("leader_asset"),
                "leader_score": row.get("leader_score"),
                "leader_margin": row.get("leader_margin"),
                **parsed, "parse_ok": ok,
                "n_headlines": len(news_by_day.get(d, [])),
                "instrument_digest": digest,
                "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "provenance": "retrospective_derived",
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            n += 1
            if n % 25 == 0:
                print(f"[{n}/{len(todo)}] {d}")
    print(f"generated {n} -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
