"""Request builder for one UAS company call.

Live defaults are model openai/gpt-5.6-luna, max_steps 10, reasoning effort xhigh, and web search depth low.

Dry-run uses build_request_kwargs only. The live call is agent_api.client.
"""

from __future__ import annotations

from typing import Any, Optional

from agent_api.client import execute_agent_call, require_api_key, web_search_tool
from contracts.types import CompanyInput
from unified_adaptive_search.prompting import RESPONSE_SCHEMA, build_company_prompt

DEFAULT_MODEL = "openai/gpt-5.6-luna"
DEFAULT_MAX_STEPS = 10
DEFAULT_REASONING_EFFORT = "xhigh"
DEFAULT_WEB_SEARCH_DEPTH = "low"
DEFAULT_TIMEOUT = 300.0
LEDGER_CONFIG_LABEL = "luna"


def build_request_kwargs(
    company: CompanyInput,
    *,
    model: str = DEFAULT_MODEL,
    max_steps: Optional[int] = DEFAULT_MAX_STEPS,
    reasoning_effort: str = DEFAULT_REASONING_EFFORT,
    web_search_depth: str = DEFAULT_WEB_SEARCH_DEPTH,
) -> dict[str, Any]:
    kwargs: dict[str, Any] = {
        "model": model,
        "input": build_company_prompt(company),
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


__all__ = [
    "DEFAULT_MAX_STEPS",
    "DEFAULT_MODEL",
    "DEFAULT_REASONING_EFFORT",
    "DEFAULT_TIMEOUT",
    "DEFAULT_WEB_SEARCH_DEPTH",
    "LEDGER_CONFIG_LABEL",
    "build_request_kwargs",
    "execute_agent_call",
    "require_api_key",
]
