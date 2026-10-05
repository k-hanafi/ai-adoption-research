"""Paths and processing settings.

Importing this module creates output directories. API keys live in src.keys.
"""

from dataclasses import dataclass
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "crunchbase_data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
LOG_DIR = PROJECT_ROOT / "logs"
CHECKPOINT_DIR = PROJECT_ROOT / "checkpoints"
PROMPTS_DIR = PROJECT_ROOT / "prompts"

# Stage-specific output directories (all under OUTPUT_DIR; contents are gitignored)
STAGE1_OUTPUT_DIR = OUTPUT_DIR / "stage1"
STAGE1_TAVILY_DIR = STAGE1_OUTPUT_DIR / "tavily"
STAGE1_GPT_DIR = STAGE1_OUTPUT_DIR / "gpt"
STAGE2_OUTPUT_DIR = OUTPUT_DIR / "stage2"
STAGE2_TEST_RUNS_DIR = STAGE2_OUTPUT_DIR / "test_runs"
# Stage 2 input dataset (priority=4+5) lives with the Crunchbase source data
STAGE2_INPUT_DATASET_PATH = DATA_DIR / "stage2_input_dataset_p4_p5.jsonl"

# Ensure directories exist
for dir_path in [OUTPUT_DIR, LOG_DIR, CHECKPOINT_DIR,
                 STAGE1_OUTPUT_DIR, STAGE1_TAVILY_DIR, STAGE1_GPT_DIR,
                 STAGE2_OUTPUT_DIR, STAGE2_TEST_RUNS_DIR]:
    dir_path.mkdir(exist_ok=True)


# ─────────────────────────────────────────────────────────────────────────────
# PROCESSING SETTINGS
# ─────────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class ProcessingConfig:
    """Settings for batch processing and rate limiting."""
    # Concurrency
    max_concurrent_requests: int = 10
    batch_size: int = 100

    # Timeouts (seconds)
    http_timeout: float = 10.0       # Website health checks
    tavily_timeout: float = 30.0     # Tavily API calls
    openai_timeout: float = 120.0    # GPT-5-nano needs headroom for reasoning tokens

    # Rate limiting (requests per minute) — set to 95% of actual limits for safety
    tavily_rpm: int = 950       # Actual limit: 1000 RPM
    openai_rpm: int = 28500     # Actual limit: 30,000 RPM (gpt-5-nano)
    perplexity_rpm: int = 60

    # Checkpointing
    checkpoint_every: int = 100  # Save progress every N companies

    # Retry policy
    max_retries: int = 3
    retry_delay_base: float = 1.0  # Exponential backoff base


# ─────────────────────────────────────────────────────────────────────────────
# DEFAULT INSTANCES
# ─────────────────────────────────────────────────────────────────────────────

PROCESSING = ProcessingConfig()
