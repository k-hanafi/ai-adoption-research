"""Request builder for one PCS channel.

Dry-run uses build_request_kwargs only. The live call is agent_api.client.
"""

from __future__ import annotations

from typing import Any, Optional

from agent_api.client import execute_agent_call, require_api_key, web_search_tool
from contracts.types import CompanyInput
from parallel_channel_search.channels import (
    DEFAULT_MAX_STEPS,
    DEFAULT_MODEL,
    DEFAULT_REASONING_EFFORT,
    DEFAULT_WEB_SEARCH_DEPTH,
)
from parallel_channel_search.prompting import RESPONSE_SCHEMA, build_channel_prompt

DEFAULT_TIMEOUT = 300.0


def build_request_kwargs(
    company: CompanyInput,
    channel_id: str,
    *,
    model: str = DEFAULT_MODEL,
    max_steps: Optional[int] = DEFAULT_MAX_STEPS,
    reasoning_effort: str = DEFAULT_REASONING_EFFORT,
    web_search_depth: str = DEFAULT_WEB_SEARCH_DEPTH,
) -> dict[str, Any]:
    kwargs: dict[str, Any] = {
        "model": model,
        "input": build_channel_prompt(company, channel_id),
        "response_format": RESPONSE_SCHEMA,
        "reasoning": {"effort": reasoning_effort},
        "tools": [
            web_search_tool(web_search_depth, fallback=DEFAULT_WEB_SEARCH_DEPTH),
            {"type": "fetch_url"},
        ],
    }
    if max_steps:
        kwargs["max_steps"] = max_steps
    return kwargs


def request_snapshot(request_kwargs: dict[str, Any]) -> dict[str, Any]:
    return {
        "model": request_kwargs.get("model"),
        "max_steps": request_kwargs.get("max_steps"),
        "reasoning": request_kwargs.get("reasoning"),
        "tools": request_kwargs.get("tools"),
        "has_response_format": "response_format" in request_kwargs,
        "input_chars": len(request_kwargs.get("input") or ""),
        "has_preset": "preset" in request_kwargs,
    }


__all__ = [
    "DEFAULT_TIMEOUT",
    "build_request_kwargs",
    "execute_agent_call",
    "request_snapshot",
    "require_api_key",
]
