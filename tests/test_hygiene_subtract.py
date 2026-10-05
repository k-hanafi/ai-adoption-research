import subprocess
from dataclasses import fields
from pathlib import Path

import parallel_channel_search.channels as pcs
import signal_gated_search.channels as sgs
import unified_adaptive_search.agent_call as uas
from evals.cli import main

ROOT = Path(__file__).resolve().parents[1]

_GONE = (
    "evals/configs/unified_adaptive_search.yaml",
    "evals/configs/parallel_channel_search.yaml",
    "evals/configs/signal_gated_search.yaml",
    "evals/configs/tuning/uas_screen_baseline.yaml",
    "evals/configs/tuning/uas_screen_effort_high.yaml",
    "evals/configs/tuning/uas_screen_search_high.yaml",
    "evals/configs/tuning/uas_screen_steps_15.yaml",
    "evals/tune/_rerun_search_high.py",
    "evals/tune/_retry_search_high_failures.py",
    "evals/tune/_max_none3_smoke.py",
    "evals/hooks/stage3_judge.py",
    "evals/hooks/__init__.py",
)


def test_run_benchmarks_exits_without_an_instance(capsys) -> None:
    before = set((ROOT / "evals" / "instances").glob("benchmark/**"))
    code = main(["run-benchmarks", "sgs", "--live"])
    captured = capsys.readouterr()
    after = set((ROOT / "evals" / "instances").glob("benchmark/**"))
    assert code == 2
    assert captured.out == ""
    assert "bake-off was skipped" in captured.err
    assert "python -m production verify" in captured.err
    assert "python -m citation_verification" in captured.err
    assert before == after


def test_run_verification_exits_without_an_instance(capsys) -> None:
    before = set((ROOT / "evals" / "instances").glob("verification/**"))
    code = main(["run-verification"])
    captured = capsys.readouterr()
    after = set((ROOT / "evals" / "instances").glob("verification/**"))
    assert code == 2
    assert captured.out == ""
    assert "bake-off was skipped" in captured.err
    assert "python -m production verify" in captured.err
    assert "python -m citation_verification" in captured.err
    assert before == after


def test_removed_files_are_gone() -> None:
    for rel in _GONE:
        assert not (ROOT / rel).exists(), rel


def test_cursor_plans_are_not_tracked() -> None:
    tracked = subprocess.check_output(
        ["git", "ls-files", ".cursor/plans"],
        cwd=ROOT,
        text=True,
    )
    assert tracked == ""
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".cursor/plans/" in ignore


def test_unread_knobs_are_gone() -> None:
    names = {item.name for item in fields(pcs.ChannelConfig)}
    assert "search_domain_filter" not in names
    assert "instruction_hint" not in names
    assert not hasattr(sgs, "DEFAULT_CHANNEL_PRIOR")
    assert not hasattr(sgs, "DEFAULT_DIG_PRESET")
    assert not hasattr(sgs, "DEFAULT_RESCUE_DIG_PRESET")
    assert not hasattr(uas, "from_preset_defaults")


def test_agents_md_names_the_live_command() -> None:
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "python -m production" in text
    assert "legacy_agent_march_2026" in text
    assert "python -m pytest -q" in text
