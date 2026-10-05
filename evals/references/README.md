# Frozen evaluation references

`march_2026_production.jsonl` is a local copy of the March Stage 2 findings dump. Panel builders (`evals/panel/build_*.py`) and `evals.paths.MARCH_STAGE2_JSONL` read this file when you regenerate a panel.

The file is not in git. It is about 69MB. Already-built panels under `evals/panel/*.json` do not need it at runtime.

The March deep-research agent is not in this repo. If you already have the dump, leave it at `evals/references/march_2026_production.jsonl`.
