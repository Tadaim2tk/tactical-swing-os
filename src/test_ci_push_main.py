"""定期実行が main へ push する手順（tools/ci_push_main.sh）を、実物のスクリプトを走らせて確かめる。

2026-11-25: daily cycle と news narratives が同じ秒に push し、後になった daily cycle が
「cannot lock ref 'refs/heads/main': is at … but expected …」で弾かれた。push は1回きりで、取り込み直す
手順が無かったので、その日の夜間の台帳は main に入らないままジョブが赤で終わった。

ここでは手元に bare リポジトリ（origin の代わり）と、作業用・競合相手用の clone を作り、`git` を薄い包みに
差し替えてスクリプトをそのまま bash で走らせる。包みがやることは2つだけ:
- `git push git@github.com:…` を、手元の bare リポジトリへの本物の push に読み替える。場面によっては最初の
  N 回を「弾かれた」ことにし、その直前に競合相手のコミットを origin へ入れる（別の実行が先に push した場面）。
- 取り込み（pull）のたびに、鍵のファイルが置かれていないかを記録する。
それ以外の git は本物がそのまま動く（取り込み・rebase・コミットの中身は本物）。
"""
from __future__ import annotations

import os
import shutil
import stat
import subprocess
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "ci_push_main.sh"
WORKFLOWS = ROOT / ".github" / "workflows"
PUSHERS = ("daily_cycle.yml", "news_narratives.yml", "narrative_reliability.yml", "weekly_review.yml")
SECRET = "-----BEGIN TEST KEY-----\nnot-a-real-key\n-----END TEST KEY-----"
REAL_GIT = shutil.which("git")
BASH = shutil.which("bash")

pytestmark = pytest.mark.skipif(REAL_GIT is None or BASH is None, reason="git と bash が要る")

GIT_WRAPPER = r"""#!/usr/bin/env bash
# 包みの git。push 先の読み替えと、記録だけを行う。
REAL="__REAL_GIT__"
if [ "$1" = "push" ] && [[ "${2:-}" == git@github.com:* ]]; then
  n=$(( $(cat "$PUSH_T/push_calls" 2>/dev/null || echo 0) + 1 ))
  echo "$n" > "$PUSH_T/push_calls"
  printf '%s %s\n' "$2" "$3" >> "$PUSH_T/push_args"
  # 鍵が、push のあいだだけ置かれていること（中身も）を記録する
  key=$(printf '%s' "${GIT_SSH_COMMAND:-}" | sed -n 's/^ssh -i \([^ ]*\) .*/\1/p')
  if [ -n "$key" ] && [ -f "$key" ]; then cat "$key" > "$PUSH_T/key_seen_$n"; else echo "(no key file)" > "$PUSH_T/key_seen_$n"; fi
  printf '%s\n' "$key" >> "$PUSH_T/key_paths"
  # 権限（GNU の stat と BSD の stat で書き方が違う。GNU で `-f` は別の意味なので、先に GNU の書き方を試す）
  if stat -c '%a' "$key" > /dev/null 2>&1; then stat -c '%a' "$key" >> "$PUSH_T/key_modes"; else stat -f '%Lp' "$key" >> "$PUSH_T/key_modes" 2>/dev/null || echo "unknown" >> "$PUSH_T/key_modes"; fi
  if [ "$n" -le "$(cat "$PUSH_T/reject_first" 2>/dev/null || echo 0)" ]; then
    # 別の実行が先に push した場面。相手のコミットを origin に入れてから、弾かれたことにする。
    if [ -f "$PUSH_T/rival_$n.sh" ]; then bash "$PUSH_T/rival_$n.sh" > "$PUSH_T/rival_$n.log" 2>&1 || echo "rival failed" >> "$PUSH_T/rival_errors"; fi
    echo " ! [remote rejected] HEAD -> main (cannot lock ref 'refs/heads/main': is at X but expected Y)" >&2
    exit 1
  fi
  exec "$REAL" push "$PUSH_T/origin.git" "$3"
fi
if [ "$1" = "pull" ]; then
  # 取り込みのあいだ、鍵のファイルが置かれていないこと
  find "$TMPDIR" -type f | wc -l | tr -d ' ' >> "$PUSH_T/tmp_files_during_pull"
fi
exec "$REAL" "$@"
"""


def _git(cwd: Path, *args: str, env=None) -> str:
    out = subprocess.run([REAL_GIT, *args], cwd=cwd, env=env, capture_output=True, text=True)
    assert out.returncode == 0, "git %s: %s" % (" ".join(args), out.stderr)
    return out.stdout.strip()


class Scene:
    """origin（bare）・作業用 clone（定期実行の checkout）・競合相手の clone。"""

    def __init__(self, tmp_path: Path):
        self.t = tmp_path
        self.env = dict(os.environ,
                        GIT_AUTHOR_NAME="tso-test", GIT_AUTHOR_EMAIL="tso-test@example.invalid",
                        GIT_COMMITTER_NAME="tso-test", GIT_COMMITTER_EMAIL="tso-test@example.invalid",
                        GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
        self.origin = tmp_path / "origin.git"
        _git(tmp_path, "init", "-q", "--bare", str(self.origin), env=self.env)
        _git(self.origin, "symbolic-ref", "HEAD", "refs/heads/main", env=self.env)
        seed = tmp_path / "seed"
        seed.mkdir()
        _git(seed, "init", "-q", env=self.env)
        _git(seed, "symbolic-ref", "HEAD", "refs/heads/main", env=self.env)
        (seed / "data").mkdir()
        (seed / "data" / "ledger.csv").write_text("date,value\n2026-11-24,1\n", encoding="utf-8")
        (seed / "data" / "narrative.csv").write_text("date,text\n2026-11-24,a\n", encoding="utf-8")
        (seed / "notes.txt").write_text("tracked but never committed by the bot\n", encoding="utf-8")
        _git(seed, "add", "-A", env=self.env)
        _git(seed, "commit", "-q", "-m", "seed", env=self.env)
        _git(seed, "push", "-q", str(self.origin), "main", env=self.env)
        self.work = tmp_path / "work"
        self.rival = tmp_path / "rival"
        for clone in (self.work, self.rival):
            _git(tmp_path, "clone", "-q", str(self.origin), str(clone), env=self.env)
        # 定期実行が作ったデータ追記のコミット（まだ push していない）
        with (self.work / "data" / "ledger.csv").open("a", encoding="utf-8") as f:
            f.write("2026-11-25,2\n")
        _git(self.work, "commit", "-q", "-am", "Append daily TSO ledgers [skip ci]", env=self.env)
        self.ledger_commit_subject = "Append daily TSO ledgers [skip ci]"
        self.bin = tmp_path / "bin"
        self.bin.mkdir()
        self.keys = tmp_path / "tmp"
        self.keys.mkdir()
        wrapper = self.bin / "git"
        wrapper.write_text(GIT_WRAPPER.replace("__REAL_GIT__", REAL_GIT), encoding="utf-8")
        sleeper = self.bin / "sleep"
        sleeper.write_text('#!/usr/bin/env bash\necho "$1" >> "$PUSH_T/sleeps"\nexit 0\n', encoding="utf-8")
        for path in (wrapper, sleeper):
            path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    def rival_pushes(self, attempt: int, path: str, line: str, message: str) -> None:
        """attempt 回目の push が弾かれる直前に、競合相手が origin へ入れるコミットを用意する。"""
        script = self.t / ("rival_%d.sh" % attempt)
        script.write_text(
            "set -e\ncd %s\n%s pull -q --rebase origin main\nprintf '%%s\\n' %s >> %s\n%s commit -q -am %s\n%s push -q %s HEAD:main\n"
            % (_q(self.rival), _q(REAL_GIT), _q(line), _q(path), _q(REAL_GIT), _q(message), _q(REAL_GIT), _q(self.origin)),
            encoding="utf-8")

    def run(self, *, reject_first: int = 0, branch=None, drop=(), extra_env=None):
        (self.t / "reject_first").write_text("%d\n" % reject_first, encoding="utf-8")
        env = dict(self.env, PATH="%s%s%s" % (self.bin, os.pathsep, os.environ["PATH"]), PUSH_T=str(self.t),
                   TMPDIR=str(self.keys), TSO_BOT_DEPLOY_KEY=SECRET, GITHUB_REPOSITORY="owner/repo")
        env.update(extra_env or {})
        for name in drop:
            env.pop(name, None)
        args = [BASH, str(SCRIPT)] + ([branch] if branch else [])
        out = subprocess.run(args, cwd=self.work, env=env, capture_output=True, text=True, timeout=120)
        return out

    # ---- 結果の読み取り
    def read(self, name: str) -> str:
        path = self.t / name
        return path.read_text(encoding="utf-8") if path.exists() else ""

    def push_calls(self) -> int:
        return int(self.read("push_calls").strip() or 0)

    def origin_subjects(self):
        return _git(self.origin, "log", "--format=%s", "main", env=self.env).splitlines()

    def origin_file(self, path: str) -> str:
        return _git(self.origin, "show", "main:%s" % path, env=self.env)

    def assert_key_was_handled_safely(self):
        """鍵は push のあいだだけ置かれ、取り込みのあいだと終了後には残っていない。"""
        for n in range(1, self.push_calls() + 1):
            assert self.read("key_seen_%d" % n).strip() == SECRET, "push %d は鍵のファイルを渡していない" % n
        # 鍵は、この試験が見張っている場所に置かれている（そうでないと、下の「残っていない」が空振りになる。
        # macOS の mktemp は型を渡さないと TMPDIR を見ないので、最初の版の試験は空振りしていた）
        paths = [line for line in self.read("key_paths").splitlines() if line]
        assert len(paths) == self.push_calls() and all(Path(p).parent.resolve() == self.keys.resolve() for p in paths), paths
        assert all(not Path(p).exists() for p in paths), "push のあとに鍵のファイルが残っている: %s" % paths
        assert set(self.read("key_modes").split()) == {"600"}, "鍵のファイルを持ち主以外が読める: %s" % self.read("key_modes")
        during_pull = [line for line in self.read("tmp_files_during_pull").split() if line]
        assert during_pull and set(during_pull) == {"0"}, "取り込みのあいだに鍵のファイルが残っている: %s" % during_pull
        assert list(self.keys.iterdir()) == [], "終了後に鍵のファイルが残っている"
        assert self.read("rival_errors") == "", self.read("rival_1.log") + self.read("rival_2.log")


def _q(value) -> str:
    return "'%s'" % str(value).replace("'", "'\\''")


@pytest.fixture
def scene(tmp_path):
    return Scene(tmp_path)


def test_the_push_goes_through_on_the_first_attempt(scene):
    out = scene.run()
    assert out.returncode == 0, out.stdout + out.stderr
    assert scene.push_calls() == 1 and scene.read("sleeps") == ""
    assert scene.read("push_args").strip() == "git@github.com:owner/repo.git HEAD:main"
    assert scene.origin_subjects()[0] == scene.ledger_commit_subject
    assert "2026-11-25,2" in scene.origin_file("data/ledger.csv")
    assert "pushed to main (attempt 1/5)" in out.stdout and "::warning::" not in out.stdout
    scene.assert_key_was_handled_safely()


def test_a_rejected_push_is_retried_after_taking_in_the_other_runs_commit(scene):
    """2026-11-25 の形: 別の定期実行が同じ瞬間に push していた。取り込み直して、2回目で入る。"""
    scene.rival_pushes(1, "data/narrative.csv", "2026-11-25,b", "Append narrative memory store [skip ci]")
    out = scene.run(reject_first=1)
    assert out.returncode == 0, out.stdout + out.stderr
    assert scene.push_calls() == 2
    # 相手のコミットも、こちらの台帳のコミットも main にある（どちらも失っていない）
    assert scene.origin_subjects()[:2] == [scene.ledger_commit_subject, "Append narrative memory store [skip ci]"]
    assert "2026-11-25,2" in scene.origin_file("data/ledger.csv")
    assert "2026-11-25,b" in scene.origin_file("data/narrative.csv")
    assert "::warning::push to main was rejected (attempt 1/5)" in out.stdout
    assert "pushed to main (attempt 2/5)" in out.stdout
    assert scene.read("sleeps").split() == ["5"]
    scene.assert_key_was_handled_safely()


def test_two_rejections_in_a_row_are_survived_with_a_longer_wait_each_time(scene):
    scene.rival_pushes(1, "data/narrative.csv", "2026-11-25,b", "rival one")
    scene.rival_pushes(2, "data/narrative.csv", "2026-11-25,c", "rival two")
    out = scene.run(reject_first=2)
    assert out.returncode == 0, out.stdout + out.stderr
    assert scene.push_calls() == 3 and scene.read("sleeps").split() == ["5", "10"]
    assert scene.origin_subjects()[:3] == [scene.ledger_commit_subject, "rival two", "rival one"]
    scene.assert_key_was_handled_safely()


def test_it_gives_up_in_red_and_says_the_data_is_not_on_main(scene):
    """最後まで弾かれた。黙って捨てない: 赤で終わり、この実行のデータが main に無いことを書く。"""
    out = scene.run(reject_first=99)
    assert out.returncode == 1, out.stdout + out.stderr
    assert scene.push_calls() == 5                                   # 既定の回数だけ試した
    assert scene.read("sleeps").split() == ["5", "10", "15", "20"]   # 最後の失敗のあとは待たない
    assert "::error::could not push to main after 5 attempts" in out.stdout
    assert "NOT on main" in out.stdout and "pushed to main" not in out.stdout
    assert scene.ledger_commit_subject not in scene.origin_subjects()
    scene.assert_key_was_handled_safely()


def test_the_number_of_attempts_can_be_set_and_nonsense_is_refused(scene):
    out = scene.run(reject_first=99, extra_env={"TSO_PUSH_ATTEMPTS": "2"})
    assert out.returncode == 1 and scene.push_calls() == 2
    assert "after 2 attempts" in out.stdout
    for bad in ("0", "many", "-1", "1.5"):
        refused = scene.run(extra_env={"TSO_PUSH_ATTEMPTS": bad})
        assert refused.returncode == 2 and "TSO_PUSH_ATTEMPTS" in refused.stdout, bad
    assert scene.push_calls() == 2                                   # 断った回は push していない


def test_a_change_to_the_same_lines_is_not_settled_by_the_machine(scene):
    """相手が同じファイルの同じ場所を書き換えていた。取り込みが衝突したら、やり直さずに落とす（どちらも上書きしない）。"""
    scene.rival_pushes(1, "data/ledger.csv", "2026-11-25,999", "rival rewrites the ledger")
    out = scene.run(reject_first=1)
    assert out.returncode != 0, out.stdout + out.stderr
    assert scene.push_calls() == 1                                   # 衝突のあと、push をやり直していない
    assert scene.origin_subjects()[0] == "rival rewrites the ledger"
    assert "2026-11-25,999" in scene.origin_file("data/ledger.csv") and "2026-11-25,2" not in scene.origin_file("data/ledger.csv")
    assert "pushed to main" not in out.stdout
    assert list(scene.keys.iterdir()) == []                          # 鍵は残していない


def test_uncommitted_changes_to_tracked_files_do_not_stop_the_pull(scene):
    """コミットしていない追跡ファイルの変更が残っていても、取り込み直しで止まらない。その変更は push されない。"""
    (scene.work / "notes.txt").write_text("edited during the run, never added\n", encoding="utf-8")
    scene.rival_pushes(1, "data/narrative.csv", "2026-11-25,b", "Append narrative memory store [skip ci]")
    out = scene.run(reject_first=1)
    assert out.returncode == 0, out.stdout + out.stderr
    assert scene.push_calls() == 2
    assert scene.origin_file("notes.txt") == "tracked but never committed by the bot"
    assert (scene.work / "notes.txt").read_text(encoding="utf-8") == "edited during the run, never added\n"
    scene.assert_key_was_handled_safely()


def test_another_branch_can_be_named(scene):
    """narrative_reliability は走った枝の名前を渡す。その枝を取り込み、その枝へ push する。"""
    out = scene.run(branch="main")
    assert out.returncode == 0 and scene.read("push_args").strip() == "git@github.com:owner/repo.git HEAD:main"
    _git(scene.work, "checkout", "-q", "-b", "side", env=scene.env)
    _git(scene.work, "push", "-q", str(scene.origin), "side", env=scene.env)
    (scene.work / "data" / "ledger.csv").write_text("date,value\nside,1\n", encoding="utf-8")
    _git(scene.work, "commit", "-q", "-am", "side commit", env=scene.env)
    out2 = scene.run(branch="side")
    assert out2.returncode == 0, out2.stdout + out2.stderr
    assert scene.read("push_args").split("\n")[1] == "git@github.com:owner/repo.git HEAD:side"
    assert _git(scene.origin, "log", "--format=%s", "-1", "side", env=scene.env) == "side commit"
    assert scene.origin_subjects()[0] == scene.ledger_commit_subject  # main は動かしていない


def test_without_the_key_or_the_repository_name_nothing_is_pushed(scene):
    for missing in ("TSO_BOT_DEPLOY_KEY", "GITHUB_REPOSITORY"):
        out = scene.run(drop=(missing,))
        assert out.returncode != 0 and missing in out.stderr, missing
    assert scene.push_calls() == 0 and scene.read("tmp_files_during_pull") == ""


# --------------------------------------------------------------------------- workflow の側
def _run_scripts(name: str):
    workflow = yaml.safe_load((WORKFLOWS / name).read_text(encoding="utf-8"))
    for job in workflow["jobs"].values():
        for step in job.get("steps", []):
            if "run" in step:
                yield step


def test_no_workflow_pushes_on_its_own():
    """push は tools/ci_push_main.sh だけが行う。workflow に1回きりの push を書き戻さない。"""
    offenders = []
    for path in sorted(WORKFLOWS.glob("*.yml")):
        for step in _run_scripts(path.name):
            if "git push" in step["run"]:
                offenders.append("%s: %s" % (path.name, step.get("name")))
    assert offenders == [], "workflow の中で直接 push している: %s" % offenders


def test_the_four_writers_call_the_script_right_after_their_commit():
    for name in PUSHERS:
        callers = [step for step in _run_scripts(name) if "tools/ci_push_main.sh" in step["run"]]
        assert len(callers) == 1, name
        step = callers[0]
        run = step["run"]
        assert run.index("git commit") < run.index("bash tools/ci_push_main.sh"), name
        assert "TSO_BOT_DEPLOY_KEY" in (step.get("env") or {}), name   # 鍵は、この手順にだけ渡す
        assert "|| echo" not in run.split("bash tools/ci_push_main.sh")[1].splitlines()[0], name  # 失敗を警告で流さない
        # 取り込み直しはスクリプトの中にある。workflow の側で先に済ませたつもりにしない。
        assert "git pull" not in run, name


def test_the_key_reaches_no_other_step():
    for name in PUSHERS:
        workflow = yaml.safe_load((WORKFLOWS / name).read_text(encoding="utf-8"))
        assert "TSO_BOT_DEPLOY_KEY" not in str(workflow.get("env") or {}), name
        for job in workflow["jobs"].values():
            assert "TSO_BOT_DEPLOY_KEY" not in str(job.get("env") or {}), name
            holders = [step.get("name") for step in job["steps"] if "TSO_BOT_DEPLOY_KEY" in str(step.get("env") or {})]
            assert len(holders) == 1, (name, holders)
