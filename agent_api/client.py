from __future__ import annotations

import json
from typing import Any, Optional

from contracts.types import Finding
from src.keys import APIKeys

DEFAULT_TIMEOUT = 300.0

WEB_SEARCH_DEPTH: dict[str, dict[str, Any]] = {
    "low": {
        "search_context_size": "medium",
        "max_tokens": 2000,
        "max_tokens_per_page": 1000,
        "max_results": 10,
    },
    "medium": {
        "search_context_size": "high",
        "max_tokens": 4000,
        "max_tokens_per_page": 2000,
        "max_results": 20,
    },
    "high": {
        "search_context_size": "high",
        "max_tokens": 8000,
        "max_tokens_per_page": 4000,
        "max_results": 50,
    },
}


def web_search_tool(depth: str, *, fallback: str) -> dict[str, Any]:
    key = (depth or fallback).strip().lower()
    if key not in WEB_SEARCH_DEPTH:
        known = ", ".join(sorted(WEB_SEARCH_DEPTH))
        raise ValueError(f"Unknown web_search_depth {depth!r}. Choose: {known}")
    return {"type": "web_search", **WEB_SEARCH_DEPTH[key]}


def extract_json_object(text: str) -> str:
    start = text.find("{")
    if start == -1:
        return text
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    return text[start:]


def extract_message_text(output: list) -> str:
    from perplexity.types.output_item import MessageOutputItem

    texts: list[str] = []
    for item in output:
        if isinstance(item, MessageOutputItem):
            for part in getattr(item, "content", None) or []:
                text = getattr(part, "text", None)
                if text:
                    texts.append(text)
    return "".join(texts)


def extract_content_text(output: list) -> str:
    texts: list[str] = []
    for item in output or []:
        for part in getattr(item, "content", None) or []:
            text = getattr(part, "text", None)
            if text:
                texts.append(text)
    return "".join(texts)


def require_api_key(api_key: Optional[str] = None) -> str:
    if api_key:
        return api_key
    key = APIKeys().perplexity
    if not key:
        raise RuntimeError(
            "Perplexity API key required. "
            "Set credentials/perplexity_api_key.txt or PERPLEXITY_API_KEY."
        )
    return key


def create_response(
    request_kwargs: dict[str, Any],
    *,
    api_key: Optional[str] = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> Any:
    from perplexity import Perplexity

    key = require_api_key(api_key)
    client = Perplexity(api_key=key, max_retries=0)
    create_kwargs = dict(request_kwargs)
    create_kwargs["timeout"] = timeout
    return client.responses.create(**create_kwargs)


def parse_findings(raw_findings: Any, *, channel_id: Optional[str] = None) -> list[Finding]:
    findings: list[Finding] = []
    if not isinstance(raw_findings, list):
        return findings
    for idx, row in enumerate(raw_findings):
        if not isinstance(row, dict):
            continue
        try:
            findings.append(
                Finding(
                    finding_id=int(row.get("finding_id") or idx + 1),
                    AI_tool_used=str(row.get("AI_tool_used") or ""),
                    use_case=str(row.get("use_case") or ""),
                    business_function=str(row.get("business_function") or ""),
                    evidence_description=str(row.get("evidence_description") or ""),
                    source_url=str(row.get("source_url") or ""),
                    source_type=str(row.get("source_type") or ""),
                    channel=channel_id,
                )
            )
        except (TypeError, ValueError):
            continue
    return findings


def usage_fields(response: Any) -> dict[str, Any]:
    cost_usd = 0.0
    input_tokens = None
    output_tokens = None
    total_tokens = None
    usage = getattr(response, "usage", None)
    if usage:
        input_tokens = usage.input_tokens
        output_tokens = usage.output_tokens
        total_tokens = usage.total_tokens
        cost = getattr(usage, "cost", None)
        if cost is not None and getattr(cost, "total_cost", None) is not None:
            cost_usd = float(cost.total_cost)
    return {
        "response_id": getattr(response, "id", None),
        "model_used": getattr(response, "model", None),
        "response_status": getattr(response, "status", None),
        "cost_usd": cost_usd,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
    }


def load_json_object(content: str) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    try:
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            parsed = json.loads(extract_json_object(content))
    except json.JSONDecodeError as exc:
        return None, f"JSON parse error: {exc}"
    except Exception as exc:
        return None, f"Response parse error: {type(exc).__name__}: {exc}"
    if not isinstance(parsed, dict):
        return None, f"JSON root must be an object, got {type(parsed).__name__}"
    return parsed, None


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


def tool_use_from_response(response: Any) -> dict[str, Any]:
    from perplexity.types.output_item import (
        FetchURLResultsOutputItem,
        MessageOutputItem,
        SearchResultsOutputItem,
    )

    tool_calls_details: dict[str, int] = {}
    tool_calls_cost_usd = None
    if getattr(response, "usage", None):
        usage = response.usage
        raw_details = getattr(usage, "tool_calls_details", None) or {}
        for name, detail in raw_details.items():
            inv = getattr(detail, "invocation", None)
            if inv is None and isinstance(detail, dict):
                inv = detail.get("invocation")
            if inv is not None:
                tool_calls_details[str(name)] = int(inv)
        cost = getattr(usage, "cost", None)
        if cost is not None and getattr(cost, "tool_calls_cost", None) is not None:
            tool_calls_cost_usd = float(cost.tool_calls_cost)

    output_item_counts = {
        "search_results": 0,
        "fetch_url_results": 0,
        "message": 0,
        "other": 0,
    }
    citations: list[str] = []
    for item in response.output or []:
        if isinstance(item, SearchResultsOutputItem):
            output_item_counts["search_results"] += 1
            for sr in item.results or []:
                if getattr(sr, "url", None):
                    citations.append(sr.url)
        elif isinstance(item, FetchURLResultsOutputItem):
            output_item_counts["fetch_url_results"] += 1
        elif isinstance(item, MessageOutputItem):
            output_item_counts["message"] += 1
        else:
            output_item_counts["other"] += 1

    return {
        "tool_calls_details": tool_calls_details,
        "tool_calls_cost_usd": tool_calls_cost_usd,
        "output_item_counts": output_item_counts,
        "search_result_urls": len(citations),
        "citations": citations,
        "tool_output_items": (
            output_item_counts["search_results"]
            + output_item_counts["fetch_url_results"]
        ),
    }


def execute_agent_call(
    request_kwargs: dict[str, Any],
    *,
    channel_id: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    response = create_response(request_kwargs, api_key=api_key, timeout=timeout)
    tool_use = tool_use_from_response(response)
    meta: dict[str, Any] = {}
    if channel_id is not None:
        meta["channel_id"] = channel_id
    meta.update(usage_fields(response))
    meta.update({
        "citations": tool_use["citations"],
        "tool_use": {
            "tool_calls_details": tool_use["tool_calls_details"],
            "tool_calls_cost_usd": tool_use["tool_calls_cost_usd"],
            "output_item_counts": tool_use["output_item_counts"],
            "search_result_urls": tool_use["search_result_urls"],
            "tool_output_items": tool_use["tool_output_items"],
            "max_steps_ceiling": request_kwargs.get("max_steps"),
        },
        "raw_content_preview": None,
        "genai_adoption_found": False,
        "findings": [],
        "no_finding_reason": None,
        "no_finding_analysis": None,
        "error": None,
    })

    if response.status == "failed":
        err = response.error
        detail = f"{err.type}: {err.message}" if err else "unknown"
        meta["error"] = f"Agent API response failed: {detail}"
        return meta

    content = (response.output_text or "").strip()
    if not content:
        content = extract_message_text(list(response.output or [])).strip()
    if not content:
        output_types = [type(item).__name__ for item in (response.output or [])]
        meta["error"] = (
            f"Empty Agent API response (model={response.model}, "
            f"status={response.status}, output_types={output_types})"
        )
        return meta

    meta["raw_content_preview"] = content[:500]
    parsed, error = load_json_object(content)
    if error:
        meta["error"] = error
        return meta
    meta["findings"] = parse_findings(parsed.get("findings"), channel_id=channel_id)
    meta["genai_adoption_found"] = bool(parsed.get("genai_adoption_found", False))
    meta["no_finding_reason"] = parsed.get("no_finding_reason")
    meta["no_finding_analysis"] = parsed.get("no_finding_analysis")
    return meta
