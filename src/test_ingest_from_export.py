"""tools/ingest_from_export.py — 会話エクスポートからの取込を1コマンドにしたもの（2026-11-11）。

固定する原則:
1. 10資産10行そろった日だけ取り込む。そろわない日は理由を出して飛ばし、終了コード 2
2. dry-run は何も書かない
3. 主役・invalidation は本文に明示された値だけ。台帳に無い signal_id や集約した書き方は記録しない
4. 週次 crypto の2行は未記録の週だけ足す（2回目は何も足さない）
5. crypto_grounds・expected_r_basis は、本文の申告が全部読めて全部同じ値のときだけ記録する（2026-11-12。
   Codex の経路は記録し、この経路は記録していなかった。同じ入力から同じ記録にそろえる）
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


def _report(day, rows, leader="WTI", inval="", extras=""):
    jp = f"{int(day[:4])}年{int(day[5:7])}月{int(day[8:])}日"
    body = "\n".join([f"# Tactical Swing OS — {jp}", "", f"**本日の市場の主役：{leader}**", "", "本文" * 400, ""])
    if inval:
        body += f"`invalidation_check: {inval}`\n\n"
    if extras:
        body += extras + "\n\n"
    return body + "## 10. TSO_LOG\n\n```csv\n" + HEADER + "\n" + "\n".join(rows) + "\n```\n"


def _conv(title, texts):
    mapping = {}
    for i, t in enumerate(texts):
        mapping[f"n{i}"] = {"message": {"id": f"m{i}", "author": {"role": "assistant"}, "create_time": 1000 + i,
                                        "content": {"content_type": "text", "parts": [t]}}}
    return {"title": title, "mapping": mapping}


# 2026-11-10〜12 の実際の出力の形: 太字、コード、Markdown の \\_ エスケープ、同じ申告のくり返し、JSON のキー。
EXTRAS_1110 = ("**crypto_grounds: etf=無, cme=無**\n**expected_r_basis: subjective**\n\n"
               "crypto\\_grounds: etf=無, cme=無\n`expected_r_basis: subjective`\n\n"
               '```json\n{"crypto_grounds": {"etf": "有", "cme": "有"}, "expected_r_basis": "two_point"}\n```')


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
        _conv("TSO Daily Signal Log v2", [_report("2026-11-10", day10, "WTI", inval, EXTRAS_1110),
                                          _report("2026-11-11", day11, "US10Y")]),
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
    assert not (repo / "data" / "crypto_grounds_observations.csv").exists()
    assert not (repo / "data" / "expected_r_basis.csv").exists()
    assert "crypto_grounds etf=absent cme=absent / expected_r_basis subjective" in r.stdout    # 読むだけは読む


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
    # 本文の申告（JSON のキーの値 有/two_point ではなく、1行申告の 無/subjective）
    g = _rows(repo / "data" / "crypto_grounds_observations.csv")
    assert [(x["date"], x["etf_grounds"], x["cme_grounds"], x["source"]) for x in g] == [("2026-11-10", "absent", "absent", "chatgpt_app")]
    b = _rows(repo / "data" / "expected_r_basis.csv")
    assert [(x["date"], x["expected_r_basis"], x["source"]) for x in b] == [("2026-11-10", "subjective", "chatgpt_app")]
    assert summary["crypto_grounds"] == [{"day": "2026-11-10", "etf": "absent", "cme": "absent", "result": "recorded: 2026-11-10 etf=absent cme=absent"}]
    assert summary["expected_r_basis"][0]["basis"] == "subjective" and "recorded basis" in summary["expected_r_basis"][0]["result"]


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


def _ife():
    sys.path.insert(0, str(ROOT / "tools"))
    import ingest_from_export as ife
    return ife


def test_declarations_are_recorded_only_when_every_copy_is_readable_and_agrees():
    ife = _ife()
    ok = "**crypto_grounds: etf=有, cme=無**\nexpected_r_basis: subjective (new direction signals = none)\n"
    assert ife.find_crypto_grounds(ok) == (("present", "absent"), "")
    assert ife.find_expected_r_basis(ok) == ("subjective", "")
    # UI 部品で包まれた形と、全角の区切り
    assert ife.find_crypto_grounds("<text>{`crypto_grounds: ETF＝有、CME＝有（basis のみ）`}</text>")[0] == ("present", "present")
    # 食い違い: どちらも記録しない
    g, why = ife.find_crypto_grounds("crypto_grounds: etf=有, cme=有\n- crypto_grounds: etf=無, cme=無\n")
    assert g is None and "食い違う" in why
    b, why = ife.find_expected_r_basis("expected_r_basis: subjective\nexpected_r_basis: two_point\n")
    assert b is None and "食い違う" in why
    # 語彙の外が1つでも混じったら記録しない（読めた方だけを採らない）
    g, why = ife.find_crypto_grounds("crypto_grounds: etf=有, cme=有\ncrypto_grounds: etf=partial, cme=有\n")
    assert g is None and "読めない" in why
    b, why = ife.find_expected_r_basis("expected_r_basis: subjective\nexpected_r_basis: mixed\n")
    assert b is None and "読めない" in why
    # 片方しか書いていない
    assert ife.find_crypto_grounds("crypto_grounds: etf=有\n")[0] is None
    # 申告が無い・JSON のキーしか無い
    for text in ("本文だけ", '{"crypto_grounds": {"etf": "有"}, "expected_r_basis": "subjective"}'):
        assert ife.find_crypto_grounds(text) == (None, "本文に crypto_grounds の1行が無い")
        assert ife.find_expected_r_basis(text) == (None, "本文に expected_r_basis の1行が無い")


def test_missing_declarations_are_not_a_failure(repo):
    """2行はプロンプトの必須項目ではない（changelog (20) で外した）。無い日は記録しないだけで、終了コードは変えない。"""
    data = json.loads((repo / "export.json").read_text(encoding="utf-8"))
    for node in data[0]["mapping"].values():
        parts = node["message"]["content"]["parts"]
        parts[0] = parts[0].replace(EXTRAS_1110, "")
    data[0]["mapping"] = {k: v for k, v in data[0]["mapping"].items() if "2026年11月11日" not in v["message"]["content"]["parts"][0]}
    (repo / "export.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    r = _run(repo, "--apply")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "crypto_grounds — / expected_r_basis —" in r.stdout
    assert not (repo / "data" / "crypto_grounds_observations.csv").exists()
    assert not (repo / "data" / "expected_r_basis.csv").exists()


def test_sidecars_for_backfills_declarations_without_touching_the_ledger(repo):
    """取込済みの日に、後から2行だけ足せる（11/3〜11/11 を埋めた手順）。2回目は何も足さない。"""
    data = json.loads((repo / "export.json").read_text(encoding="utf-8"))
    data[0]["mapping"] = {k: v for k, v in data[0]["mapping"].items() if "2026年11月11日" not in v["message"]["content"]["parts"][0]}
    (repo / "export.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    assert _run(repo, "--apply").returncode == 0
    (repo / "data" / "crypto_grounds_observations.csv").unlink()        # 記録していなかった頃の状態に戻す
    (repo / "data" / "expected_r_basis.csv").unlink()
    ledger = (repo / "data" / "signal_log.csv").read_text(encoding="utf-8")
    r = _run(repo, "--apply", "--sidecars-for", "2026-11-10")
    assert r.returncode == 0, r.stdout + r.stderr
    assert (repo / "data" / "signal_log.csv").read_text(encoding="utf-8") == ledger and "[ingest]" not in r.stdout
    assert len(_rows(repo / "data" / "crypto_grounds_observations.csv")) == 1
    assert len(_rows(repo / "data" / "expected_r_basis.csv")) == 1
    snap = {p.name: p.read_text(encoding="utf-8") for p in (repo / "data").glob("*.csv")}
    r2 = _run(repo, "--apply", "--sidecars-for", "2026-11-10")
    assert r2.returncode == 0, r2.stdout + r2.stderr                     # 記録済みは失敗ではない
    assert {p.name: p.read_text(encoding="utf-8") for p in (repo / "data").glob("*.csv")} == snap


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

