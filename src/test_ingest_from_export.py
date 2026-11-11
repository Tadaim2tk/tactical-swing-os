"""tools/ingest_from_export.py — 会話エクスポートからの取込を1コマンドにしたもの（2026-11-11）。

固定する原則:
1. 10資産10行そろった日だけ取り込む。そろわない日は理由を出して飛ばし、終了コード 2
2. dry-run は何も書かない
3. 主役・invalidation は本文に明示された値だけ。台帳に無い signal_id や集約した書き方は記録しない
4. 週次 crypto の2行は未記録の週だけ足す（2回目は何も足さない）
"""
from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "ingest_from_export.py"
ASSETS = ["GOLD", "BTC", "ETH", "WTI", "USDJPY", "SPX", "NASDAQ", "DXY", "US10Y", "VIX"]
HEADER = ("date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,"
          "expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,"
          "invalidation,verification_target,verified_status")


def _b(day, asset, side="BUY"):
    d = day.replace("-", "")
    return f"{day},{d}_{asset}_{side}_PULLBACK,{asset},{side},B,PULLBACK,100,102,95,112,118,1.83,0.55,0.3,70,70,30,0.25,MIXED,60,60,60,60,72,60,inv,vt,verified"


def _nt_canon(day, asset):
    d = day.replace("-", "")
    return f"{day},{d}_{asset}_NONE_NO_TRADE,{asset},NONE,NO_TRADE,NO_TRADE,,,,,,,,,40,30,80,,EVENT,42,40,35,30,39,32,x,y,verified"


def _nt_swapped(day, asset):
    d = day.replace("-", "")
    return f"{day},{d}_{asset}_NO_TRADE_NONE,{asset},NO_TRADE,NONE,NONE,,,,,,,,,40,30,80,0,EVENT,42,40,35,30,39,32,x,y,verified"


def _report(day, rows, leader="WTI", inval=""):
    jp = f"{int(day[:4])}年{int(day[5:7])}月{int(day[8:])}日"
    body = "\n".join([f"# Tactical Swing OS — {jp}", "", f"**本日の市場の主役：{leader}**", "", "本文" * 400, ""])
    if inval:
        body += f"`invalidation_check: {inval}`\n\n"
    return body + "## 10. TSO_LOG\n\n```csv\n" + HEADER + "\n" + "\n".join(rows) + "\n```\n"


def _conv(title, texts):
    mapping = {}
    for i, t in enumerate(texts):
        mapping[f"n{i}"] = {"message": {"id": f"m{i}", "author": {"role": "assistant"}, "create_time": 1000 + i,
                                        "content": {"content_type": "text", "parts": [t]}}}
    return {"title": title, "mapping": mapping}


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "data" / "raw").mkdir(parents=True)
    (tmp_path / "data" / "prediction_log_archive").mkdir()
    prev = [_b("2026-11-09", a) for a in ASSETS[:9]] + [_nt_canon("2026-11-09", "VIX")]
    (tmp_path / "data" / "signal_log.csv").write_text(
        HEADER + ",origin\n" + "\n".join(r + ",chatgpt_app" for r in prev) + "\n", encoding="utf-8")
    (tmp_path / "data" / "leader_observations.csv").write_text("date,leader_claimed,source,recorded_at\n", encoding="utf-8")
    (tmp_path / "data" / "invalidation_checks.csv").write_text("check_date,signal_id,invalidation_fired,source,recorded_at\n", encoding="utf-8")
    for a in ASSETS:
        (tmp_path / "data" / "raw" / f"{a}.csv").write_text("date,open,high,low,close\n2026-11-09,100,101,99,100\n", encoding="utf-8")
    day10 = [_b("2026-11-10", a, "SELL") for a in ASSETS[:8]] + [_b("2026-11-10", "US10Y"), _nt_swapped("2026-11-10", "VIX")]
    inval = ("20261109_GOLD_BUY_PULLBACK=not_fired, 20261109_BTC_BUY_PULLBACK=unknown, "
             "historical_pending_signals=unknown, 20991231_GOLD_BUY_PULLBACK=fired")
    day11 = [_b("2026-11-11", a) for a in ASSETS[:9]]            # 9行しか無い日
    # 2026-11-08 の実際の形: UI部品のタグで包まれ、CTX は行頭に来ない。本文中の言及(カンマ無し)は拾わない
    crypto = ("週次まとめ。前回の CRYPTO_PRED条件は達成。\n<text preserveWhitespace>{`CRYPTO_CTX,2026-11-02,MIXED,OUTFLOW,UNKNOWN,NONE,MEDIUM,HIT\n"
              "CRYPTO_PRED,2026-11-02,BTC,BELOW,78000,2026-11-13`}</text>\n")
    export = tmp_path / "export.json"
    export.write_text(json.dumps([
        _conv("TSO Daily Signal Log v2", [_report("2026-11-10", day10, "WTI", inval), _report("2026-11-11", day11, "US10Y")]),
        _conv("Crypto market update: macro vs regulation dynamics", [crypto]),
    ], ensure_ascii=False), encoding="utf-8")
    return tmp_path


def _run(repo, *args):
    return subprocess.run([sys.executable, str(TOOL), str(repo / "export.json"), "--no-score", *args],
                          cwd=repo, capture_output=True, text=True)


def _rows(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_dry_run_writes_nothing(repo):
    before = (repo / "data" / "signal_log.csv").read_text(encoding="utf-8")
    r = _run(repo)
    assert r.returncode == 2, r.stdout + r.stderr            # 11/11 は9行なので飛ばす
    assert "[ingest] 2026-11-10" in r.stdout and "[skip] 2026-11-11" in r.stdout
    assert (repo / "data" / "signal_log.csv").read_text(encoding="utf-8") == before
    assert not list((repo / "data" / "prediction_log_archive").glob("*.md"))
    assert not (repo / "data" / "crypto_context_weekly.csv").exists()
    assert len(_rows(repo / "data" / "leader_observations.csv")) == 0


def test_apply_ingests_complete_days_only_and_records_sidecars(repo):
    r = _run(repo, "--apply")
    assert r.returncode == 2, r.stdout + r.stderr
    led = _rows(repo / "data" / "signal_log.csv")
    d10 = [x for x in led if x["date"] == "2026-11-10"]
    assert len(d10) == 10 and not [x for x in led if x["date"] == "2026-11-11"]     # 部分取込はしない
    vix = [x for x in d10 if x["asset"] == "VIX"][0]
    assert (vix["signal_id"], vix["side"], vix["rank"], vix["type"]) == ("20261110_VIX_NONE_NO_TRADE", "NONE", "NO_TRADE", "NO_TRADE")
    assert all(x["origin"] == "chatgpt_app" for x in d10)
    # 本文は両日ともアーカイブする（飛ばした日も原文は残す）
    names = sorted(p.name for p in (repo / "data" / "prediction_log_archive").glob("*.md"))
    assert names == ["2026-11-10_tso-daily-signal-log.md", "2026-11-11_tso-daily-signal-log.md"]
    assert _rows(repo / "data" / "leader_observations.csv")[0]["leader_claimed"] == "WTI"
    inv = {x["signal_id"]: x["invalidation_fired"] for x in _rows(repo / "data" / "invalidation_checks.csv")}
    assert inv == {"20261109_GOLD_BUY_PULLBACK": "not_fired", "20261109_BTC_BUY_PULLBACK": "unknown"}
    assert _rows(repo / "data" / "crypto_context_weekly.csv")[0]["week_start"] == "2026-11-02"
    assert _rows(repo / "data" / "crypto_predictions_weekly.csv")[0]["level"] == "78000"
    norm = _rows(repo / "data" / "ingest_normalizations.csv")
    assert norm[0]["raw_signal_id"] == "20261110_VIX_NO_TRADE_NONE"
    summary = json.loads((repo / "results" / "ingest_from_export_summary.json").read_text(encoding="utf-8"))
    assert [d["day"] for d in summary["days"]] == ["2026-11-10"] and summary["skipped_days"][0]["day"] == "2026-11-11"
    assert any("台帳に無い" in s for s in summary["invalidation"][0]["skipped"])
    assert any("signal_id の形でない" in s for s in summary["invalidation"][0]["skipped"])


def test_second_run_adds_nothing(repo):
    assert _run(repo, "--apply").returncode == 2
    snap = {p.name: p.read_text(encoding="utf-8") for p in (repo / "data").glob("*.csv")}
    r = _run(repo, "--apply")
    assert r.returncode == 2 and "[ingest]" not in r.stdout and "[crypto]" not in r.stdout
    assert {p.name: p.read_text(encoding="utf-8") for p in (repo / "data").glob("*.csv")} == snap


def test_no_daily_conversation_is_fatal(repo):
    (repo / "export.json").write_text(json.dumps([_conv("別の会話", ["x" * 2000])]), encoding="utf-8")
    r = _run(repo, "--apply")
    assert r.returncode == 1 and "取り出せなかった" in r.stdout


def test_conflicting_invalidation_id_stays_excluded():
    """fired, not_fired, not_fired と3回出ても、矛盾した ID は記録しない(#210 Codex P2)。"""
    sys.path.insert(0, str(ROOT / "tools"))
    import ingest_from_export as ife
    text = "invalidation_check: 20261109_GOLD_BUY_PULLBACK=fired, 20261109_GOLD_BUY_PULLBACK=not_fired, 20261109_GOLD_BUY_PULLBACK=not_fired, 20261109_BTC_BUY_PULLBACK=unknown"
    items, skipped = ife.parse_invalidation(text, {"20261109_GOLD_BUY_PULLBACK": "2026-11-09", "20261109_BTC_BUY_PULLBACK": "2026-11-09"}, "2026-11-10")
    assert items == ["20261109_BTC_BUY_PULLBACK=unknown"]
    assert sum("矛盾" in s for s in skipped) == 1


def test_failed_later_stage_is_reported_and_can_be_retried(repo):
    """後段(ここでは invalidation の記録)が失敗したら終了コード 3。--sidecars-for でやり直せる(#210 Codex P2)。"""
    inv_path = repo / "data" / "invalidation_checks.csv"
    inv_path.unlink()
    inv_path.mkdir()                       # 記録ツールが書けない状態を作る
    # 11/11(9行)を外して、取込自体は成功する形にする
    data = json.loads((repo / "export.json").read_text(encoding="utf-8"))
    daily = data[0]["mapping"]
    data[0]["mapping"] = {k: v for k, v in daily.items() if "2026年11月11日" not in v["message"]["content"]["parts"][0]}
    (repo / "export.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    r = _run(repo, "--apply")
    assert r.returncode == 3, r.stdout + r.stderr
    assert "[FAILED] record_signal_extras invalidation 2026-11-10" in r.stdout
    assert len([x for x in _rows(repo / "data" / "signal_log.csv") if x["date"] == "2026-11-10"]) == 10   # 取込は済んでいる
    summary = json.loads((repo / "results" / "ingest_from_export_summary.json").read_text(encoding="utf-8"))
    assert summary["failures"]
    # 直してからやり直す: 台帳は増えず、invalidation だけ入る
    inv_path.rmdir()
    inv_path.write_text("check_date,signal_id,invalidation_fired,source,recorded_at\n", encoding="utf-8")
    r2 = _run(repo, "--apply", "--sidecars-for", "2026-11-10")
    assert r2.returncode == 0, r2.stdout + r2.stderr
    assert len(_rows(inv_path)) == 2 and "[ingest]" not in r2.stdout
    assert len(_rows(repo / "data" / "leader_observations.csv")) == 1        # 主役は記録済みのまま(失敗扱いにしない)

