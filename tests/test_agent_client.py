from agent_api.client import execute_agent_call
from contracts.schema import RESPONSE_SCHEMA
from contracts.types import CompanyInput
from parallel_channel_search.agent_call import build_request_kwargs as build_pcs
from parallel_channel_search.prompting import RESPONSE_SCHEMA as PCS_SCHEMA
from signal_gated_search.agent_call import (
    build_dig_request_kwargs,
    build_scout_request_kwargs,
)
from signal_gated_search.prompting import DIG_RESPONSE_SCHEMA
from unified_adaptive_search.agent_call import build_request_kwargs as build_uas
from unified_adaptive_search.prompting import RESPONSE_SCHEMA as UAS_SCHEMA

COMPANY = CompanyInput(rcid=1, name="Jam", homepage_url="https://jam.dev")


def test_finding_schema_is_one_object() -> None:
    assert PCS_SCHEMA is RESPONSE_SCHEMA
    assert UAS_SCHEMA is RESPONSE_SCHEMA
    assert DIG_RESPONSE_SCHEMA is RESPONSE_SCHEMA


def test_pcs_dry_kwargs_stay_luna_medium() -> None:
    kwargs = build_pcs(COMPANY, "jobs")
    assert kwargs["model"] == "openai/gpt-5.6-luna"
    assert kwargs["max_steps"] == 50
    assert kwargs["reasoning"] == {"effort": "medium"}
    web = next(tool for tool in kwargs["tools"] if tool["type"] == "web_search")
    assert web["max_results"] == 20
    assert web["search_context_size"] == "high"
    assert [tool["type"] for tool in kwargs["tools"]] == ["web_search", "fetch_url"]
    assert "preset" not in kwargs


def test_uas_dry_kwargs_stay_low_xhigh() -> None:
    kwargs = build_uas(COMPANY)
    assert kwargs["model"] == "openai/gpt-5.6-luna"
    assert kwargs["max_steps"] == 10
    assert kwargs["reasoning"] == {"effort": "xhigh"}
    web = next(tool for tool in kwargs["tools"] if tool["type"] == "web_search")
    assert web["max_results"] == 10
    assert web["search_context_size"] == "medium"
    assert web["max_tokens"] == 2000


def test_sgs_scout_is_low_preset_without_fetch() -> None:
    kwargs = build_scout_request_kwargs(COMPANY, "jobs")
    assert kwargs["preset"] == "low"
    assert kwargs["tools"] == [{"type": "web_search"}]
    assert "fetch_url" not in [tool["type"] for tool in kwargs["tools"]]


def test_sgs_dig_search_stays_medium() -> None:
    kwargs = build_dig_request_kwargs(COMPANY, "owned", reasoning_effort="high")
    web = next(tool for tool in kwargs["tools"] if tool["type"] == "web_search")
    assert web["max_results"] == 20
    assert kwargs["max_steps"] == 50


def test_parse_failure_keeps_metered_cost(monkeypatch) -> None:
    class _Cost:
        total_cost = 0.42

    class _Usage:
        input_tokens = 3
        output_tokens = 4
        total_tokens = 7
        cost = _Cost()

    class _Response:
        id = "resp"
        model = "openai/gpt-5.6-luna"
        status = "completed"
        output_text = "not json"
        output = []
        usage = _Usage()
        error = None

    monkeypatch.setattr(
        "agent_api.client.create_response",
        lambda *args, **kwargs: _Response(),
    )
    monkeypatch.setattr(
        "agent_api.client.tool_use_from_response",
        lambda response: {
            "tool_calls_details": {},
            "tool_calls_cost_usd": None,
            "output_item_counts": {},
            "search_result_urls": 0,
            "citations": [],
            "tool_output_items": 0,
        },
    )
    meta = execute_agent_call({"input": "x", "max_steps": 50}, channel_id="jobs", api_key="k")
    assert meta["cost_usd"] == 0.42
    assert meta["error"].startswith("JSON parse error")
    assert meta["channel_id"] == "jobs"
    assert meta["findings"] == []
