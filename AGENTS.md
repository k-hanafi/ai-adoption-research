# Agent notes

The live batch command is `python -m production`. The default architecture is `sgs`.

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

Citation checks use `python -m production verify` and `python -m citation_verification`. `python -m evals run-benchmarks` and `python -m evals run-verification` exit 2. The bake-off was skipped.

## Where the code lives

| Path | Role |
|---|---|
| `src/stage_1/` | Website check and priority score |
| `signal_gated_search/` | Default Stage 2 architecture |
| `parallel_channel_search/` | Three equal-depth channels |
| `unified_adaptive_search/` | One call per company. Search depth stays `low`. |
| `production/` | Batch runner |
| `citation_verification/` | Page fetch and citation judge |
| `evals/` | Tuning, cost preview, and the instance dashboard |
| `legacy_agent_march_2026/` | Frozen March 2026 agent |

Do not import `legacy_agent_march_2026` from live code. Do not import live code from that folder. `src/stage_2/` exits on purpose. The live Stage 2 runners are the three architecture packages.

Company panels and `summary.jsonl` files stay in git. Paid per-company traces under `outputs/stage2/test_runs/` stay local.

## Knobs that stay put

`unified_adaptive_search` keeps `DEFAULT_WEB_SEARCH_DEPTH` at `low`. Signal Gated Search scouts use preset `low` and `web_search` only. Parallel Channel Search search depth is `medium`.
