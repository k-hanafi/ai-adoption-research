# Data that is and is not in git

This repo ships **code, prompts, and fictional schema samples**. It does not
ship the licensed Crunchbase dump, the probe scoreboards, or the full
production finding tables.

| Kind | In git? | Where |
|---|---|---|
| Full Crunchbase slice (~44k rows) | No | Local `crunchbase_data/44k_crunchbase_startups.csv` |
| Stage 2 queue (priority 4–5) | No | Local `crunchbase_data/stage2_input_dataset_p4_p5.jsonl` |
| Fictional input sample | Yes | `crunchbase_data/sample/` |
| Production findings / traces | No | Local `outputs/prod/{sgs,pcs,uas}/` |
| Fictional findings sample | Yes | `outputs/prod/sample/findings.sample.csv` |
| March master dump (~69MB) | No | Local `evals/references/march_2026_production.jsonl` |
| Eval company panels | Yes | `evals/panel/` |
| Probe `summary.jsonl` | No | Local `outputs/stage2/test_runs/` |

Probe `summary.jsonl` files record company id, cost, and finding count. They
stay on the machine that ran the probe. Per-company Agent dumps stay local.

To run production against the fictional sample:

```bash
python -m production dry-run --all \
  --dataset crunchbase_data/sample/stage2_input.sample.jsonl
```

Git history still contains the old dumps until a history rewrite, which we
are not doing unless Crunchbase or the PI asks.
