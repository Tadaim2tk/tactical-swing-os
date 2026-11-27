"""朝の判断に渡す ATR10 の表（tools/atr_reference.py。2026-11-27）。

日次の本文は「SL幅は 1×ATR10 以上」を求めているのに、11月の本文は 27 日のうち 20 日で「ATR10 を計算できない」と書いていた。
規則だけがあって、計算の材料が渡っていなかった（docs/weekly_readout_2026-11-27.md §7.3）。
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import simulate_execution as sim

ROOT = Path(__file__).resolve().parents[1]
TODAY = pd.Timestamp("2026-11-27")


def _mod():
    spec = importlib.util.spec_from_file_location("atr_reference", ROOT / "tools" / "atr_reference.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ar = _mod()


def _frame(n: int, end: str, width: float = 2.0, last_width: float | None = None) -> pd.DataFrame:
    """終値 100 で横ばい、毎日の値幅が width の日足を n 本。最後の足（end のラベル）だけ値幅を変えられる。"""
    dates = pd.bdate_range(end=end, periods=n)
    w = np.full(n, width)
    if last_width is not None:
        w[-1] = last_width
    return pd.DataFrame({"date": dates, "open": 100.0, "high": 100.0 + w / 2, "low": 100.0 - w / 2, "close": 100.0})


def test_atr10_is_the_mean_true_range_of_the_ten_bars_ending_at_the_last_final_bar():
    # 11/26 が最後の足（まだ確定と認めない）。確定した最後の足は 11/25
    f = _frame(30, "2026-11-26", width=2.0, last_width=50.0)
    row = ar.compute_row("AAA", f, TODAY)
    assert row == {"asset": "AAA", "as_of": "2026-11-25", "close": 100.0, "atr10": 2.0, "atr10_pct": 2.0}


def test_the_forming_last_bar_is_not_used_even_when_its_range_is_huge():
    quiet = ar.compute_row("AAA", _frame(30, "2026-11-26", width=2.0, last_width=2.0), TODAY)
    wild = ar.compute_row("AAA", _frame(30, "2026-11-26", width=2.0, last_width=50.0), TODAY)
    assert quiet == wild


def test_a_last_bar_older_than_two_days_counts_as_final():
    f = _frame(30, "2026-11-24", width=2.0, last_width=12.0)      # 11/24 の足は、11/27 には確定している
    row = ar.compute_row("AAA", f, TODAY)
    assert row["as_of"] == "2026-11-24" and row["atr10"] == pytest.approx((9 * 2.0 + 12.0) / 10)


def test_the_definition_is_the_simulators_own():
    rng = np.random.default_rng(7)
    dates = pd.bdate_range(end="2026-11-20", periods=40)
    close = 100 + rng.normal(0, 1, 40).cumsum()
    f = pd.DataFrame({"date": dates, "open": close, "high": close + rng.uniform(0.2, 2, 40),
                      "low": close - rng.uniform(0.2, 2, 40), "close": close})
    row = ar.compute_row("AAA", f, TODAY)
    i = ar.last_final_index(f, TODAY)
    assert i == len(f) - 1 and row["atr10"] == float(f"{sim.atr_at_decision(f, i):.5g}")


def test_no_row_when_there_are_not_eleven_final_bars_or_no_prices():
    assert ar.compute_row("AAA", _frame(11, "2026-11-26"), TODAY) is None      # 確定した足は 10 本
    assert ar.compute_row("AAA", _frame(12, "2026-11-26"), TODAY) is not None  # 11 本
    assert ar.compute_row("AAA", pd.DataFrame(), TODAY) is None
    assert ar.compute_row("AAA", None, TODAY) is None


def test_numbers_keep_their_precision_across_very_different_scales():
    big = _frame(30, "2026-11-20", width=1234.5678)
    big[["open", "high", "low", "close"]] += 26000.0
    small = _frame(30, "2026-11-20", width=0.0612345)
    small[["open", "high", "low", "close"]] -= 95.2          # 終値 4.8（利回りの水準）
    assert ar.compute_row("NASDAQ", big, TODAY)["atr10"] == 1234.6
    row = ar.compute_row("US10Y", small, TODAY)
    assert row["atr10"] == 0.061234 or row["atr10"] == 0.061235
    assert row["atr10_pct"] == pytest.approx(1.28, abs=0.01)


def _frames(**kw):
    return {a: kw.get(a, _frame(30, "2026-11-20")) for a in ar.ASSET_ORDER}


def test_build_writes_one_row_per_asset_in_the_prompts_order():
    table, state = ar.build(_frames(), {}, TODAY, "2026-11-27T07:00:00Z")
    assert list(table.columns) == ar.COLUMNS and list(table["asset"]) == ar.ASSET_ORDER
    assert set(state.values()) == {"computed"} and set(table["updated_at_utc"]) == {"2026-11-27T07:00:00Z"}
    assert set(table["as_of"]) == {"2026-11-20"}


def test_an_asset_that_cannot_be_computed_keeps_its_previous_row_and_its_old_dates():
    first, _ = ar.build(_frames(), {}, TODAY, "2026-11-20T07:00:00Z")
    previous = {r["asset"]: dict(r) for _, r in first.iterrows()}
    frames = _frames(GOLD=pd.DataFrame(), BTC=_frame(30, "2026-11-23"))
    table, state = ar.build(frames, previous, TODAY, "2026-11-27T07:00:00Z")
    gold = table[table["asset"] == "GOLD"].iloc[0]
    assert state["GOLD"] == "kept_previous" and gold["as_of"] == "2026-11-20" and gold["updated_at_utc"] == "2026-11-20T07:00:00Z"
    btc = table[table["asset"] == "BTC"].iloc[0]
    assert state["BTC"] == "computed" and btc["as_of"] == "2026-11-23" and btc["updated_at_utc"] == "2026-11-27T07:00:00Z"
    assert state["ETH"] == "unchanged" and table[table["asset"] == "ETH"].iloc[0]["updated_at_utc"] == "2026-11-20T07:00:00Z"


def test_an_asset_with_no_previous_row_is_left_out_instead_of_written_as_zero():
    table, state = ar.build(_frames(GOLD=pd.DataFrame()), {}, TODAY, "2026-11-27T07:00:00Z")
    assert state["GOLD"] == "missing" and "GOLD" not in set(table["asset"]) and len(table) == len(ar.ASSET_ORDER) - 1
    assert not (table[["close", "atr10"]] == "").any().any()


def test_asset_list_matches_the_fetcher():
    import fetch_market
    assert sorted(ar.ASSET_ORDER) == sorted(fetch_market.ASSETS.values())


# --------------------------------------------------------------------------- コマンドとして
def _write_raw(raw: Path, frames: dict):
    raw.mkdir(parents=True, exist_ok=True)
    for a, f in frames.items():
        if f is not None and not f.empty:
            f.assign(date=f["date"].dt.strftime("%Y-%m-%d")).to_csv(raw / f"{a}.csv", index=False)


@pytest.fixture()
def fixed_today(monkeypatch):
    monkeypatch.setattr(ar, "_current_utc_date", lambda: TODAY)


def test_cli_writes_the_table_and_leaves_it_alone_when_nothing_changed(tmp_path, capsys, fixed_today):
    raw, out = tmp_path / "raw", tmp_path / "data" / "atr10_reference.csv"
    _write_raw(raw, _frames())
    assert ar.main(["--raw-dir", str(raw), "--out", str(out)]) == 0
    first = out.read_text(encoding="utf-8")
    assert first.splitlines()[0] == "asset,as_of,close,atr10,atr10_pct,updated_at_utc" and len(first.splitlines()) == 11
    assert first.splitlines()[1].startswith("GOLD,2026-11-20,100.0,2.0,2.00,")
    out.write_text(first.replace(first.splitlines()[1].split(",")[-1], "2026-01-01T00:00:00Z"), encoding="utf-8")   # 時刻だけ古くする
    marked = out.read_text(encoding="utf-8")
    assert ar.main(["--raw-dir", str(raw), "--out", str(out)]) == 0
    assert out.read_text(encoding="utf-8") == marked          # 1行も変わらなければ書き換えない（時刻も進めない）
    assert "変わった行は無い" in capsys.readouterr().out


def test_cli_warns_and_keeps_the_old_row_when_one_asset_has_no_prices(tmp_path, capsys, fixed_today):
    raw, out = tmp_path / "raw", tmp_path / "atr.csv"
    _write_raw(raw, _frames())
    assert ar.main(["--raw-dir", str(raw), "--out", str(out)]) == 0
    (raw / "GOLD.csv").unlink()
    _write_raw(raw, {"BTC": _frame(30, "2026-11-23")})
    capsys.readouterr()
    assert ar.main(["--raw-dir", str(raw), "--out", str(out)]) == 0
    text = capsys.readouterr().out
    assert "GOLD: kept_previous as_of=2026-11-20" in text and "::warning::計算できず、前回の行を残した資産: GOLD" in text
    table = pd.read_csv(out, dtype=str)
    assert list(table["asset"]) == ar.ASSET_ORDER and table.set_index("asset").loc["BTC", "as_of"] == "2026-11-23"


def test_cli_fails_and_touches_nothing_when_no_asset_can_be_computed(tmp_path, capsys, fixed_today):
    raw, out = tmp_path / "raw", tmp_path / "atr.csv"
    raw.mkdir()
    out.write_text("asset,as_of,close,atr10,atr10_pct,updated_at_utc\nGOLD,2026-11-20,100.0,2.0,2.00,2026-11-20T07:00:00Z\n", encoding="utf-8")
    before = out.read_text(encoding="utf-8")
    assert ar.main(["--raw-dir", str(raw), "--out", str(out)]) == 1
    assert out.read_text(encoding="utf-8") == before
    assert "::error::ATR10 を1資産も計算できなかった" in capsys.readouterr().out


def test_a_previous_file_with_other_columns_is_ignored_not_trusted(tmp_path):
    p = tmp_path / "atr.csv"
    p.write_text("asset,atr\nGOLD,1\n", encoding="utf-8")
    assert ar.read_previous(p) == {} and ar.read_previous(tmp_path / "nope.csv") == {}


def test_the_committed_table_follows_the_contract():
    # リポジトリに入っている表そのもの（朝の判断が読む）
    table = pd.read_csv(ROOT / "data" / "atr10_reference.csv", dtype=str, keep_default_na=False)
    assert list(table.columns) == ar.COLUMNS
    assert set(table["asset"]) <= set(ar.ASSET_ORDER) and table["asset"].is_unique and len(table) >= 1
    assert (pd.to_numeric(table["atr10"]) > 0).all() and (pd.to_numeric(table["close"]) > 0).all()
    assert pd.to_datetime(table["as_of"], format="%Y-%m-%d").notna().all()
