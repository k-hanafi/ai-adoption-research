"""PCS channel ids and equal-depth defaults."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


CHANNEL_IDS = ("jobs", "owned", "third_party")

# Legacy preset label (scaffolding). Prefer explicit knobs below for prod/benchmark.
DEFAULT_EQUAL_DEPTH_PRESET = "low"

DEFAULT_MODEL = "openai/gpt-5.6-luna"
DEFAULT_MAX_STEPS = 50
DEFAULT_REASONING_EFFORT = "medium"
DEFAULT_WEB_SEARCH_DEPTH = "medium"


def equal_depth_config_label(
    model: str = DEFAULT_MODEL,
    max_steps: int = DEFAULT_MAX_STEPS,
    reasoning_effort: str = DEFAULT_REASONING_EFFORT,
    web_search_depth: str = DEFAULT_WEB_SEARCH_DEPTH,
) -> str:
    """Stable ledger/preview label from explicit knobs (not a Perplexity preset)."""
    model_tag = model.rsplit("/", 1)[-1].replace(".", "_")
    return f"{model_tag}_steps{max_steps}_{reasoning_effort}_search_{web_search_depth}"


@dataclass
class ChannelConfig:
    channel_id: str
    enabled: bool = True
    preset: str = DEFAULT_EQUAL_DEPTH_PRESET
    model: str = DEFAULT_MODEL
    max_steps: int = DEFAULT_MAX_STEPS
    reasoning_effort: str = DEFAULT_REASONING_EFFORT
    web_search_depth: str = DEFAULT_WEB_SEARCH_DEPTH


def default_channel_configs(
    preset: str = DEFAULT_EQUAL_DEPTH_PRESET,
    enabled_channels: Optional[tuple[str, ...]] = None,
    *,
    model: str = DEFAULT_MODEL,
    max_steps: int = DEFAULT_MAX_STEPS,
    reasoning_effort: str = DEFAULT_REASONING_EFFORT,
    web_search_depth: str = DEFAULT_WEB_SEARCH_DEPTH,
) -> list[ChannelConfig]:
    # None means all channels. An explicit empty tuple means none enabled.
    if enabled_channels is None:
        enabled = set(CHANNEL_IDS)
    else:
        enabled = {str(channel).strip().lower() for channel in enabled_channels}
    return [
        ChannelConfig(
            channel_id=cid,
            enabled=cid in enabled,
            preset=preset,
            model=model,
            max_steps=max_steps,
            reasoning_effort=reasoning_effort,
            web_search_depth=web_search_depth,
        )
        for cid in CHANNEL_IDS
    ]
