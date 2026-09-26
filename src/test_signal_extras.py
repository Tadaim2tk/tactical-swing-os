"""tools/record_signal_extras.py のガード（#157 Codex P2 対応を含む）。"""
import subprocess
import sys
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parents[1] / "tools" / "record_signal_extras.py"


def run(args, cwd):
    return subprocess.run([sys.executable, str(TOOL), *args], cwd=cwd,
                          capture_output=True, text=True)


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "expected_r_basis.csv").write_text(
        "date,expected_r_basis,source,recorded_at\n", encoding="utf-8")
    (tmp_path / "data" / "invalidation_checks.csv").write_text(
        "check_date,signal_id,invalidation_fired,source,recorded_at\n", encoding="utf-8")
    return tmp_path


def _rows(repo, name):
    import csv
    return list(csv.DictReader((repo / "data" / name).open(encoding="utf-8")))


def test_contradictory_duplicate_in_one_batch_is_rejected(repo):
    """矛盾する重複を先勝ちで黙って通さない。

    通すと (check_date, signal_id) が矛盾したまま append-only 台帳に入り、
    再実行しても両方「既存」になって通常の手順では直せなくなる。
    """
    r = run(["invalidation", "2026-09-09", "S1=fired,S1=not_fired"], repo)
    assert r.returncode != 0
    assert "矛盾" in r.stdout + r.stderr
    assert _rows(repo, "invalidation_checks.csv") == [], "1行も書かない"


def test_identical_duplicate_in_one_batch_writes_once(repo):
    _ledger(repo, [("2026-08-03", "S1", "WTI", "BUY")])   # 台帳に無い id は拒否される(#173)
    r = run(["invalidation", "2026-09-09", "S1=fired,S1=fired"], repo)
    assert r.returncode == 0
    assert len(_rows(repo, "invalidation_checks.csv")) == 1


def test_source_is_recorded_and_validated(repo):
    """経路を決め打ちしない。同じプロンプトをターミナル経路でも使うため。"""
    assert run(["basis", "2026-09-09", "two_point", "bogus"], repo).returncode != 0
    assert run(["basis", "2026-09-09", "two_point", "gpt_terminal"], repo).returncode == 0
    assert _rows(repo, "expected_r_basis.csv")[0]["source"] == "gpt_terminal"


def test_source_defaults_to_chatgpt_app(repo):
    run(["basis", "2026-09-09", "subjective"], repo)
    assert _rows(repo, "expected_r_basis.csv")[0]["source"] == "chatgpt_app"


@pytest.mark.parametrize("bad", ["S1=maybe", "S1", "=fired"])
def test_bad_invalidation_syntax_is_rejected(repo, bad):
    assert run(["invalidation", "2026-09-09", bad], repo).returncode != 0
    assert _rows(repo, "invalidation_checks.csv") == []


def test_append_only_across_runs(repo):
    _ledger(repo, [("2026-08-03", "S1", "WTI", "BUY")])   # 台帳に無い id は拒否される(#173)
    run(["invalidation", "2026-09-09", "S1=not_fired"], repo)
    run(["invalidation", "2026-09-09", "S1=fired"], repo)   # 2回目は無視される
    rows = _rows(repo, "invalidation_checks.csv")
    assert len(rows) == 1 and rows[0]["invalidation_fired"] == "not_fired"


def _ledger(repo, rows):
    """side 列だけ効く最小の台帳。列名は data/signal_log.csv と同じ。"""
    head = "date,signal_id,asset,side,rank,type\n"
    body = "".join(f"{d},{sid},{a},{side},B,PULLBACK\n" for d, sid, a, side in rows)
    (repo / "data" / "signal_log.csv").write_text(head + body, encoding="utf-8")


def test_undeclared_open_signal_is_warned(repo):
    """窓の内側にいる方向あり判断が申告から漏れたら黙って通さない。

    2026-09-09 に実際に起きた: GPT は8件申告したが台帳の未決着は11件で、
    9/3 GOLD・9/3 NASDAQ・9/4 GOLD が落ちていた。落ちた分は「発動しなかった」
    のか「聞かれなかった」のか区別できず、発動率の分母が黙って縮む。
    """
    _ledger(repo, [("2026-09-07", "A_WTI", "WTI", "BUY"),
                   ("2026-09-07", "A_GOLD", "GOLD", "BUY")])
    r = run(["invalidation", "2026-09-09", "A_WTI=not_fired"], repo)
    assert r.returncode == 0
    assert "A_GOLD" in r.stderr and "申告漏れ" in r.stderr
    assert "A_WTI" not in r.stderr
    assert len(_rows(repo, "invalidation_checks.csv")) == 1, "警告であって取込は止めない"


def test_no_trade_rows_are_not_warned(repo):
    """NO_TRADE 行に invalidation の発動は無い。分母に入れると発動率が薄まる。"""
    _ledger(repo, [("2026-09-08", "A_VIX", "VIX", "NONE")])
    r = run(["invalidation", "2026-09-09", "A_WTI=not_fired"], repo)
    assert "申告漏れ" not in r.stderr


def test_signal_past_the_window_is_not_warned(repo):
    """5本目の翌朝の確認を過ぎたものは聞き直す対象ではない。

    2026-09-01(火)の5本目は 9/8。9/9 の朝が 9/8 を観測する最後の確認で、9/10 には閉じる。
    """
    _ledger(repo, [("2026-08-03", "X", "WTI", "BUY"), ("2026-09-01", "OLD", "WTI", "BUY")])
    assert "OLD" in run(["invalidation", "2026-09-09", "X=not_fired"], repo).stderr
    assert "OLD" not in run(["invalidation", "2026-09-10", "X=not_fired"], repo).stderr


def test_same_day_signal_is_not_warned(repo):
    """当日出した判断はまだ確認しようがない。"""
    _ledger(repo, [("2026-09-09", "TODAY", "WTI", "BUY")])
    r = run(["invalidation", "2026-09-09", "X=not_fired"], repo)
    assert "TODAY" not in r.stderr


def test_already_fired_signal_is_not_warned(repo):
    """一度 fired と記録したものは以後聞かない(契約: fired になるまで毎日)。"""
    _ledger(repo, [("2026-09-08", "GONE", "WTI", "BUY")])
    assert run(["invalidation", "2026-09-08", "GONE=fired"], repo).returncode == 0
    r = run(["invalidation", "2026-09-09", "X=not_fired"], repo)
    assert "GONE" not in r.stderr


def test_previously_recorded_same_day_counts_as_declared(repo):
    """漏れた分だけ追記する2回目の実行が、1回目の申告を漏れ扱いしない。

    runbook 1d の手順そのもの。ここを見ないと追記のたびに警告が逆さまになる
    （#161 Codex P2）。
    """
    _ledger(repo, [("2026-09-07", "A_WTI", "WTI", "BUY"),
                   ("2026-09-07", "A_GOLD", "GOLD", "BUY")])
    assert "A_GOLD" in run(["invalidation", "2026-09-09", "A_WTI=not_fired"], repo).stderr
    r = run(["invalidation", "2026-09-09", "A_GOLD=unknown"], repo)
    assert "申告漏れ" not in r.stderr, "1回目の A_WTI を漏れ扱いしない"
    assert len(_rows(repo, "invalidation_checks.csv")) == 2


def test_other_day_record_does_not_count_as_declared(repo):
    """別の日の記録では今日の申告漏れは埋まらない。毎日聞き直すのが契約。"""
    _ledger(repo, [("2026-08-03", "OTHER", "WTI", "BUY"), ("2026-09-07", "A_WTI", "WTI", "BUY")])
    assert run(["invalidation", "2026-09-08", "A_WTI=not_fired"], repo).returncode == 0
    r = run(["invalidation", "2026-09-09", "OTHER=not_fired"], repo)
    assert "A_WTI" in r.stderr


def test_final_day_is_observed_on_the_morning_after_even_on_a_weekend(repo):
    """5本目が金曜なら、土曜の朝の確認がその値動きを観測する最初で最後の機会(#172 Codex P1)。

    2026-09-12(土)の判断の5本目は 9/18(金)。9/19(土)の朝にまだ聞く。ここで閉じると
    最終日の発動が永久に落ち、発動率が系統的に低く出る(実例: 20260912_BTC_SELL)。
    日曜(9/20)には閉じる。平日カウントは週末に進まないので、日曜を開けたままにしない。
    """
    _ledger(repo, [("2026-08-03", "X", "WTI", "BUY"), ("2026-08-03", "Y", "WTI", "BUY"), ("2026-09-12", "BTC_SAT", "BTC", "SELL")])
    assert "BTC_SAT" in run(["invalidation", "2026-09-19", "X=not_fired"], repo).stderr
    for c in ("2026-09-20", "2026-09-21"):
        assert "BTC_SAT" not in run(["invalidation", c, "Y=not_fired"], repo).stderr, c


def test_last_business_day_of_the_window_is_still_open(repo):
    """5本目の当日朝(9/18 金)はまだ窓の内側。ここで外すと最後の1日を聞き漏らす。"""
    _ledger(repo, [("2026-08-03", "X", "WTI", "BUY"), ("2026-09-12", "BTC_SAT", "BTC", "SELL")])
    r = run(["invalidation", "2026-09-18", "X=not_fired"], repo)
    assert "BTC_SAT" in r.stderr


# --- 台帳に無い / 判断日より前の確認は記録しない、--check-only は書かない（#173 Codex P2） ---

def test_check_before_signal_date_is_refused(repo):
    """9/22 に 9/24 の判断を確認した行は時系列上あり得ない。入口で止める。"""
    _ledger(repo, [("2026-09-24", "BTC_24", "BTC", "BUY")])
    r = run(["invalidation", "2026-09-22", "BTC_24=not_fired"], repo)
    assert r.returncode != 0 and "前の確認日" in r.stdout + r.stderr
    assert _rows(repo, "invalidation_checks.csv") == []


def test_unknown_signal_id_is_refused(repo):
    """台帳に無い signal_id は転記ミスか未取込。黙って記録しない。"""
    _ledger(repo, [("2026-09-24", "BTC_24", "BTC", "BUY")])
    r = run(["invalidation", "2026-09-25", "BTC_42=not_fired"], repo)
    assert r.returncode != 0 and "台帳" in r.stdout + r.stderr
    assert _rows(repo, "invalidation_checks.csv") == []


def test_check_only_reports_gaps_without_writing(repo):
    """突合だけ見る用。記録コマンドを読み取りに使って偽の行を作った事故の再発防止。"""
    _ledger(repo, [("2026-09-24", "BTC_24", "BTC", "BUY"), ("2026-09-24", "GOLD_24", "GOLD", "BUY")])
    r = run(["invalidation", "2026-09-25", "BTC_24=not_fired", "--check-only"], repo)
    assert r.returncode == 0 and "GOLD_24" in r.stderr
    assert _rows(repo, "invalidation_checks.csv") == [], "何も書かない"
