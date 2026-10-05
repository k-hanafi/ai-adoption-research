"""SGS request builders and the presence-scout parse.

Scout calls use preset low and web_search only. Dig calls use the shared findings client.
"""

from __future__ import annotations

import json
from typing import Any, Optional

from agent_api.client import (
    create_response,
    extract_content_text,
    extract_json_object,
    execute_agent_call,
    require_api_key,
    web_search_tool,
)
from contracts.types import CompanyInput
from parallel_channel_search.agent_call import request_snapshot
from signal_gated_search.channels import (
    DEFAULT_DIG_MAX_STEPS,
    DEFAULT_DIG_MODEL,
    DEFAULT_DIG_WEB_SEARCH_DEPTH,
    DEFAULT_SCOUT_MAX_STEPS,
    DEFAULT_SCOUT_PRESET,
)
from signal_gated_search.prompting import (
    DIG_RESPONSE_SCHEMA,
    SCOUT_RESPONSE_SCHEMA,
    build_dig_prompt,
    build_scout_prompt,
)

DEFAULT_TIMEOUT = 300.0


def build_scout_request_kwargs(
    company: CompanyInput,
    channel_id: str,
    *,
    preset: str = DEFAULT_SCOUT_PRESET,
    max_steps: Optional[int] = DEFAULT_SCOUT_MAX_STEPS,
) -> dict[str, Any]:
    kwargs: dict[str, Any] = {
        "preset": preset,
        "input": build_scout_prompt(company, channel_id),
        "response_format": SCOUT_RESPONSE_SCHEMA,
        "tools": [{"type": "web_search"}],
    }
    if max_steps:
        kwargs["max_steps"] = max_steps
    return kwargs


def build_dig_request_kwargs(
    company: CompanyInput,
    channel_id: str,
    *,
    model: str = DEFAULT_DIG_MODEL,
    max_steps: Optional[int] = DEFAULT_DIG_MAX_STEPS,
    reasoning_effort: str,
    web_search_depth: str = DEFAULT_DIG_WEB_SEARCH_DEPTH,
) -> dict[str, Any]:
    kwargs: dict[str, Any] = {
        "model": model,
        "input": build_dig_prompt(company, channel_id),
        "response_format": DIG_RESPONSE_SCHEMA,
        "reasoning": {"effort": reasoning_effort},
        "tools": [
            web_search_tool(web_search_depth, fallback=DEFAULT_DIG_WEB_SEARCH_DEPTH),
            {"type": "fetch_url"},
        ],
    }
    if max_steps:
        kwargs["max_steps"] = max_steps
    return kwargs


def execute_dig_call(
    request_kwargs: dict[str, Any],
    *,
    channel_id: str,
    api_key: Optional[str] = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    return execute_agent_call(
        request_kwargs,
        channel_id=channel_id,
        api_key=api_key,
        timeout=timeout,
    )


def _usage_meta(response: Any, *, channel_id: str) -> dict[str, Any]:
    cost_usd = 0.0
    input_tokens = None
    output_tokens = None
    total_tokens = None
    if getattr(response, "usage", None):
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        total_tokens = response.usage.total_tokens
        if response.usage.cost and response.usage.cost.total_cost is not None:
            cost_usd = float(response.usage.cost.total_cost)
    return {
        "channel_id": channel_id,
        "response_id": getattr(response, "id", None),
        "model_used": getattr(response, "model", None),
        "response_status": getattr(response, "status", None),
        "cost_usd": cost_usd,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "evidence_bin": "none",
        "urls": [],
        "snippets": [],
        "rationale": "",
        "error": None,
        "transport_error": False,
        "raw_content_preview": None,
    }


def execute_scout_call(
    request_kwargs: dict[str, Any],
    *,
    channel_id: str,
    api_key: Optional[str] = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    response = create_response(request_kwargs, api_key=api_key, timeout=timeout)
    meta = _usage_meta(response, channel_id=channel_id)

    if getattr(response, "status", None) == "failed":
        err = getattr(response, "error", None)
        detail = f"{err.type}: {err.message}" if err else "unknown"
        meta["error"] = f"Agent API response failed: {detail}"
        return meta

    content = (getattr(response, "output_text", None) or "").strip()
    if not content:
        content = extract_content_text(list(getattr(response, "output", None) or [])).strip()
    if not content:
        meta["error"] = (
            f"Empty Agent API scout response (model={meta['model_used']}, "
            f"status={meta['response_status']})"
        )
        return meta

    meta["raw_content_preview"] = content[:500]
    try:
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            parsed = json.loads(extract_json_object(content))
        if not isinstance(parsed, dict):
            meta["error"] = f"JSON root must be an object, got {type(parsed).__name__}"
            return meta
        meta["evidence_bin"] = str(parsed.get("evidence_bin") or "none")
        urls = parsed.get("urls") or []
        snippets = parsed.get("snippets") or []
        meta["urls"] = [str(u) for u in urls] if isinstance(urls, list) else []
        meta["snippets"] = [str(s) for s in snippets] if isinstance(snippets, list) else []
        meta["rationale"] = str(parsed.get("rationale") or "")
    except json.JSONDecodeError as exc:
        meta["error"] = f"JSON parse error: {exc}"
    except Exception as exc:
        meta["error"] = f"Response parse error: {type(exc).__name__}: {exc}"
    return meta


__all__ = [
    "DEFAULT_TIMEOUT",
    "build_dig_request_kwargs",
    "build_scout_request_kwargs",
    "execute_dig_call",
    "execute_scout_call",
    "request_snapshot",
    "require_api_key",
]
