from __future__ import annotations

from typing import Any, Optional

from agent_api.client import (
    execute_agent_call as _execute_agent_call,
    request_snapshot,
    require_api_key,
    web_search_tool,
)
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


def execute_agent_call(
    request_kwargs: dict[str, Any],
    *,
    channel_id: str,
    api_key: Optional[str] = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    return _execute_agent_call(
        request_kwargs,
        channel_id=channel_id,
        api_key=api_key,
        timeout=timeout,
    )


__all__ = [
    "DEFAULT_TIMEOUT",
    "build_request_kwargs",
    "execute_agent_call",
    "request_snapshot",
    "require_api_key",
]
