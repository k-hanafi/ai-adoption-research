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


def _instance_tree() -> list[str]:
    root = ROOT / "evals" / "instances"
    if not root.exists():
        return []
    return sorted(
        str(path.relative_to(root))
        for path in root.rglob("*")
        if path.is_file()
    )


def test_run_benchmarks_exits_without_an_instance(capsys) -> None:
    before = _instance_tree()
    code = main(["run-benchmarks"])
    captured = capsys.readouterr()
    assert code == 2
    assert captured.out == ""
    assert "bake-off was skipped" in captured.err
    assert "python -m production verify" in captured.err
    assert "python -m citation_verification" in captured.err
    assert _instance_tree() == before


def test_run_verification_exits_without_an_instance(capsys) -> None:
    before = _instance_tree()
    code = main(["run-verification"])
    captured = capsys.readouterr()
    assert code == 2
    assert captured.out == ""
    assert "bake-off was skipped" in captured.err
    assert "python -m production verify" in captured.err
    assert "python -m citation_verification" in captured.err
    assert _instance_tree() == before


def test_removed_files_are_gone() -> None:
    for rel in _GONE:
        assert not (ROOT / rel).exists(), rel


def test_decks_scoreboards_and_requirements_are_not_tracked() -> None:
    tracked = subprocess.check_output(
        ["git", "ls-files"],
        cwd=ROOT,
        text=True,
    ).splitlines()
    assert "requirements.txt" not in tracked
    assert not any(
        path.startswith("presentation/") and path.endswith(".html") for path in tracked
    )
    assert not any(path.startswith("legacy_agent_march_2026/") for path in tracked)
    assert not any(path.endswith("/summary.jsonl") for path in tracked)
    instances = [path for path in tracked if path.startswith("evals/instances/")]
    assert instances == ["evals/instances/.gitkeep"]
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "presentation/*.html" in ignore
    assert "!outputs/stage2/test_runs/**/summary.jsonl" not in ignore
    assert "evals/instances/**" in ignore


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
    assert "default architecture is `sgs`" in text
    assert "signal_gated_search" in text
    assert "parallel_channel_search" in text
    assert "unified_adaptive_search" in text
    assert "legacy_agent_march_2026" not in text
    assert "python -m pytest -q" in text
