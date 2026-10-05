# Agent notes

The live batch command is `python -m production`. The default research agent is `sgs`.

Low-signal data filtering is `src/stage_1/`. The research agents are `signal_gated_search`, `parallel_channel_search`, and `unified_adaptive_search`. Citation verification is `citation_verification/`.

## Commands

Install this checkout, then run the tests. `python -m pip` uses the same interpreter that will import the package.

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```

Production commands:

```bash
python -m production dry-run --limit 1
python -m production run --limit 1
python -m production status
python -m production dedupe
python -m production verify --limit 1
```

A live `run` refuses to start unless you pass `--limit N` or `--all`. Do not start `--all`. Do not start a paid run unless Khaled asks.

`python -m evals.paid_probes` lists the historical research-agent probes and exits 2. It calls the Agent API only when you pass a probe name and `--live`.

Citation checks use `python -m production verify` and `python -m citation_verification`. `python -m evals run-benchmarks` and `python -m evals run-verification` exit 2. The bake-off was skipped.

## Where the code lives

| Path | Role |
|---|---|
| `src/keys.py` | API keys. Importing it does not create output directories. |
| `src/config.py` | Paths and processing settings. Importing it creates output directories. |
| `src/stage_1/` | Low-signal data filtering. Website check and priority score. |
| `agent_api/` | The one Perplexity Agent API client |
| `contracts/schema.py` | The shared findings JSON schema |
| `signal_gated_search/` | Research agent. Default for the batch. |
| `parallel_channel_search/` | Research agent. Three equal-depth channels. |
| `unified_adaptive_search/` | Research agent. One call per company. Search depth stays `low`. |
| `production/` | Batch runner for the research agents |
| `citation_verification/` | Citation verification. Page fetch and judge. |
| `evals/` | Tuning, cost preview, and the instance dashboard |

`src/stage_2/` exits on purpose. The live research agents are `signal_gated_search`, `parallel_channel_search`, and `unified_adaptive_search`.

Company panels in `evals/panel/` stay in git. Probe `summary.jsonl` files and paid per-company traces under `outputs/stage2/test_runs/` stay local. The paid-probe runner is `evals/paid_probes.py`.

## Knobs that stay put

`unified_adaptive_search` keeps `DEFAULT_WEB_SEARCH_DEPTH` at `low`. Signal Gated Search scouts use preset `low` and `web_search` only. Parallel Channel Search search depth is `medium`.
