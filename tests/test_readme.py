from pathlib import Path


def test_readme_contains_the_full_writeup() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "python -m production verify" in readme
    assert "python -m citation_verification" in readme
    assert "## How to use" in readme
