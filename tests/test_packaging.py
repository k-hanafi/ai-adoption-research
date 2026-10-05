from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def _runtime_lines(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            lines.append(line)
    return lines


def test_runtime_deps_match_requirements_txt() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert project["project"]["requires-python"] == ">=3.11"
    assert project["project"]["dependencies"] == _runtime_lines(
        (ROOT / "requirements.txt").read_text(encoding="utf-8")
    )
    assert project["project"]["optional-dependencies"]["dev"] == ["pytest>=8"]
    assert project["tool"]["setuptools"]["packages"] == []


def test_pytest_workflow_installs_editable_and_reads_only() -> None:
    text = (ROOT / ".github" / "workflows" / "pytest.yml").read_text(encoding="utf-8")
    assert "contents: read" in text
    assert 'python -m pip install -e ".[dev]"' in text
    assert "python -m pytest -q" in text
    assert 'python-version: "3.12"' in text
