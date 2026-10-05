import os
import subprocess
import sys
from pathlib import Path

import src.keys as keys
from src.keys import APIKeys

ROOT = Path(__file__).resolve().parents[1]


def test_file_beats_the_environment(monkeypatch, tmp_path: Path) -> None:
    (tmp_path / "openai_api_key.txt").write_text(
        "# comment\nfile-key\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(keys, "CREDENTIALS_DIR", tmp_path)
    monkeypatch.setenv("OPENAI_API_KEY", "env-key")
    loaded = APIKeys()
    assert loaded.openai == "file-key"


def test_environment_fills_a_missing_file(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(keys, "CREDENTIALS_DIR", tmp_path)
    monkeypatch.setenv("PERPLEXITY_API_KEY", "px-from-env")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    loaded = APIKeys()
    assert loaded.perplexity == "px-from-env"
    assert loaded.openai == ""
    assert "openai (credentials/openai_api_key.txt)" in loaded.validate()
    assert loaded.status()["perplexity"] is True


def test_an_explicit_key_is_kept(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(keys, "CREDENTIALS_DIR", tmp_path)
    monkeypatch.setenv("TAVILY_API_KEY", "env-key")
    assert APIKeys(tavily="passed").tavily == "passed"


def test_importing_keys_does_not_import_config() -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    subprocess.check_call(
        [
            sys.executable,
            "-c",
            "import src.keys, sys; assert 'src.config' not in sys.modules",
        ],
        cwd=ROOT,
        env=env,
    )
