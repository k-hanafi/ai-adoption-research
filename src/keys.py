"""API keys from credentials/*.txt, then the matching environment variable."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

CREDENTIALS_DIR = Path(__file__).resolve().parents[1] / "credentials"


def _load_credential(filename: str) -> str:
    cred_path = CREDENTIALS_DIR / filename
    if cred_path.is_file():
        lines = [
            line.strip()
            for line in cred_path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        if lines:
            return lines[0]
    env_var = filename.replace("_api_key.txt", "").upper() + "_API_KEY"
    return os.getenv(env_var, "")


@dataclass
class APIKeys:
    tavily: str = ""
    openai: str = ""
    perplexity: str = ""

    def __post_init__(self) -> None:
        if not self.tavily:
            self.tavily = _load_credential("tavily_api_key.txt")
        if not self.openai:
            self.openai = _load_credential("openai_api_key.txt")
        if not self.perplexity:
            self.perplexity = _load_credential("perplexity_api_key.txt")

    def validate(self) -> list[str]:
        missing = []
        if not self.tavily:
            missing.append("tavily (credentials/tavily_api_key.txt)")
        if not self.openai:
            missing.append("openai (credentials/openai_api_key.txt)")
        if not self.perplexity:
            missing.append("perplexity (credentials/perplexity_api_key.txt)")
        return missing

    def status(self) -> dict[str, bool]:
        return {
            "tavily": bool(self.tavily),
            "openai": bool(self.openai),
            "perplexity": bool(self.perplexity),
        }
