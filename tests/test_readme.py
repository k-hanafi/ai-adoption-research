from pathlib import Path


def test_readme_points_at_the_live_commands() -> None:
    text = Path("README.md").read_text(encoding="utf-8")
    assert "python -m production" in text
    assert "Stage 3 verification remain stubs" not in text
    assert "legacy_agent_march_2026" not in text
    assert "$0.16" in text
    assert "$0.171" in text
    assert "$0.157" in text
    assert "unread page stays null" in text
    assert "python -m production verify" in text
    assert "python -m citation_verification" in text
    assert "summary.jsonl" not in text
    assert "presentation/" in text
    assert "are not in git" in text
