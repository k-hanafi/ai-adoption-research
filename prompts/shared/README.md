# Shared prompts

Blocks that more than one architecture can read.

Each architecture also has its own folder:

- `prompts/unified_adaptive_search/`
- `prompts/parallel_channel_search/`
- `prompts/signal_gated_search/`

Stage 1 reads `prompts/stage_1_classifier.txt`.
Unified Adaptive Search reads `prompts/stage_2_perplexity_prompt.txt` unless `prompts/unified_adaptive_search/research_prompt.txt` exists.
