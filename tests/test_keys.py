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


def test_backup_extract_prefers_the_credentials_file(monkeypatch, tmp_path: Path) -> None:
    (tmp_path / "tavily_api_key.txt").write_text(
        "# note\nfile-tavily\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(keys, "CREDENTIALS_DIR", tmp_path)
    monkeypatch.setenv("TAVILY_API_KEY", "env-tavily")
    seen: dict[str, str] = {}

    class _Response:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, list[object]]:
            return {"results": []}

    class _Client:
        def __init__(self, *args: object, **kwargs: object) -> None:
            return None

        def __enter__(self) -> "_Client":
            return self

        def __exit__(self, *args: object) -> bool:
            return False

        def post(self, url: str, headers: dict[str, str] | None = None, json: object = None) -> _Response:
            seen["authorization"] = (headers or {})["Authorization"]
            return _Response()

    monkeypatch.setattr(
        "citation_verification.backup_fetch.httpx.Client",
        _Client,
    )
    from citation_verification.backup_fetch import execute_tavily_extract

    execute_tavily_extract("https://example.com/page")
    assert seen["authorization"] == "Bearer file-tavily"


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
