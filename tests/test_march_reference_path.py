"""Panel rebuilds read the local March dump. The March agent is not in this repo."""

import subprocess
from pathlib import Path

from evals.paths import EVALS_PACKAGE_DIR, MARCH_STAGE2_JSONL, PROJECT_ROOT

_FORBIDDEN_IMPORTS = (
    "import legacy_agent_march_2026",
    "from legacy_agent_march_2026",
)


def test_march_jsonl_is_evals_reference_not_legacy_folder() -> None:
    assert MARCH_STAGE2_JSONL == (
        EVALS_PACKAGE_DIR / "references" / "march_2026_production.jsonl"
    )
    assert "legacy_agent_march_2026" not in str(MARCH_STAGE2_JSONL)


def _assert_moved_exit(main) -> None:
    try:
        main()
    except SystemExit as exc:
        message = str(exc)
    else:
        raise AssertionError("retired March command must exit instead of calling the API")
    assert "python -m production" in message
    assert "legacy_agent_march_2026" not in message


def test_live_march_runner_command_explains_the_move() -> None:
    from src.stage_2.production_agent_runner import main

    _assert_moved_exit(main)


def test_live_march_preset_command_explains_the_move() -> None:
    from src.tests.stage_2.run_preset_test import main

    _assert_moved_exit(main)


def test_live_python_does_not_import_march_snapshot() -> None:
    skip_parts = {
        "legacy_agent_march_2026",
        ".venv",
        "venv",
        "__pycache__",
        ".git",
    }
    hits: list[str] = []
    for path in Path(PROJECT_ROOT).rglob("*.py"):
        if any(part in skip_parts for part in path.parts):
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        text = path.read_text(encoding="utf-8")
        if any(needle in text for needle in _FORBIDDEN_IMPORTS):
            hits.append(str(path.relative_to(PROJECT_ROOT)))
    assert hits == []


def test_march_snapshot_is_not_tracked() -> None:
    tracked = subprocess.check_output(
        ["git", "ls-files", "legacy_agent_march_2026"],
        cwd=PROJECT_ROOT,
        text=True,
    )
    assert tracked == ""
    assert not (PROJECT_ROOT / "legacy_agent_march_2026").exists()
