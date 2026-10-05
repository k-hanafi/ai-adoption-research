# AI adoption research

This repo measures generative-AI use inside startups. Low-signal data filtering lives in `src/stage_1/`. The research agents are `signal_gated_search/`, `parallel_channel_search/`, and `unified_adaptive_search/`. Citation verification lives in `citation_verification/`.

The live batch command is `python -m production`. Run it from the checkout root. `python -m` runs that module with the same interpreter you use for the install below. The default research agent is Signal Gated Search (`sgs`). The editable install pulls dependencies. It does not install these packages. `pyproject.toml` sets `packages = []`.

## Install and test

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```

`python -m pip` uses that same interpreter.

## Run a batch

`dry-run`, `run`, and `verify` each require `--limit N` or `--all`. `verify --status` does not. The default company file, `crunchbase_data/stage2_input_dataset_p4_p5.jsonl`, is local and is not in git. The commands below use the fictional sample.

```bash
python -m production dry-run --limit 1 --dataset crunchbase_data/sample/stage2_input.sample.jsonl
python -m production status --dataset crunchbase_data/sample/stage2_input.sample.jsonl
```

A live `run` uses the same `--limit` and `--dataset` flags on the local company file. `python -m production dedupe` rewrites `findings_deduplicated.csv` from an existing `findings.csv`. Do not pass `--all` for a first run.

`--architecture` accepts `sgs`, `pcs`, and `uas`. The default is `sgs`. Writes go to `outputs/prod/<architecture>/`. `dry-run` writes nothing.

Signal Gated Search scouts use preset `low` and `web_search` only. Parallel Channel Search search depth is `medium`. Unified Adaptive Search search depth stays `low`.

## Check a citation

The batch command is `python -m production verify`. One findings file goes through `python -m citation_verification --findings path.jsonl`. `python -m evals run-verification` and `python -m evals run-benchmarks` exit 2. The bake-off was skipped.

Both commands need `outputs/prod/sgs/findings_deduplicated.csv`. A fresh checkout does not have that file.

```bash
python -m production verify --limit 1
python -m production verify --limit 1 --live
```

`verify` does not call a paid API until you pass `--live`. An unread page stays null on the verdict. `findings_verified.csv` leaves that cell blank.

## Plan spend for Signal Gated Search

Plan a full SGS batch at about $0.16 per company. The hill-climb 20 mean was $0.171. The skip-50 mean was $0.157. Those scoreboards stay on the machine that ran them.

`python -m evals.paid_probes` lists the historical probes and exits 2. It calls the Agent API only when you pass a probe name and `--live`. Five early SGS folders still refuse `--live`, because their scoreboards used an older scout preset or a shallower dig.

## Where the code lives

| Path | Role |
|---|---|
| `production/` | Batch runner for the research agents |
| `signal_gated_search/` | Research agent. Default for the batch. |
| `parallel_channel_search/` | Research agent. Three equal-depth channels. |
| `unified_adaptive_search/` | Research agent. One call per company. |
| `agent_api/` | Perplexity client |
| `contracts/schema.py` | Findings schema |
| `src/keys.py` | API keys. Importing it does not create output directories. |
| `src/stage_1/` | Low-signal data filtering. Website check and priority score. |
| `citation_verification/` | Citation verification. Page fetch and judge. |
| `evals/` | Tuning, cost preview, and paid-probe re-runs |

The proposal and stage decks under `presentation/` are not in git.

Put keys in `credentials/*.txt` or the matching environment variable. The tracked templates are `credentials/*.txt.template`. A credentials file wins over the environment variable.
