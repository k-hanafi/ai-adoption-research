# AI adoption research

This repo measures generative-AI use inside startups. The live batch command is `python -m production`. `python -m` runs that module with the interpreter that has this checkout installed. The default architecture is Signal Gated Search (`sgs`).

The March 2026 production run is frozen in `legacy_agent_march_2026/`. Live code does not import that folder.

## Install and test

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```

`python -m pip` uses that same interpreter.

## Run a batch

A live `run` refuses to start unless you pass `--limit N` or `--all`.

```bash
python -m production dry-run --limit 1
python -m production run --limit 1
python -m production status
python -m production dedupe
```

`--architecture` accepts `sgs`, `pcs`, and `uas`. The default is `sgs`. Writes go to `outputs/prod/`.

Signal Gated Search scouts use preset `low` and `web_search` only. Parallel Channel Search search depth is `medium`. Unified Adaptive Search search depth stays `low`.

## Check a citation

The batch command is `python -m production verify`. One findings file goes through `python -m citation_verification --findings path.jsonl`. `python -m evals run-verification` and `python -m evals run-benchmarks` exit 2. The bake-off was skipped.

```bash
python -m production verify --limit 1
python -m production verify --limit 1 --live
```

`verify` does not call a paid API until you pass `--live`. An unread page stays null.

## Plan spend for Signal Gated Search

Plan a full SGS batch at about $0.16 per company. The hill-climb 20 mean was $0.171. The skip-50 mean was $0.157. Those scoreboards are `outputs/stage2/test_runs/sgs_hillclimb_20_matched/summary.jsonl` and `outputs/stage2/test_runs/sgs_skip_50/summary.jsonl`.

`python -m evals.paid_probes` lists the historical probes and exits 2. It calls the Agent API only when you pass a probe name and `--live`. Five early SGS folders still refuse `--live`, because their scoreboards used an older scout preset or a shallower dig.

## March 2026 run

That run produced 2,062 findings. The dashboard is [`legacy_agent_march_2026/presentation/production_results.html`](legacy_agent_march_2026/presentation/production_results.html). HTML files in `presentation/` are earlier decks from that period.

## Where the code lives

| Path | Role |
|---|---|
| `production/` | Batch runner |
| `signal_gated_search/` | Default Stage 2 architecture |
| `parallel_channel_search/` | Three equal-depth channels |
| `unified_adaptive_search/` | One call per company |
| `agent_api/` | Perplexity client |
| `contracts/schema.py` | Findings schema |
| `src/keys.py` | API keys. Importing it does not create output directories. |
| `src/stage_1/` | Website check and priority score |
| `citation_verification/` | Page fetch and citation judge |
| `evals/` | Tuning, cost preview, and paid-probe re-runs |
| `legacy_agent_march_2026/` | Frozen March 2026 agent |

Put keys in `credentials/*.txt` or the matching environment variable. The tracked templates are `credentials/*.txt.template`. A credentials file wins over the environment variable.
