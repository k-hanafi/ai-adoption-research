# Signal Gated Search prompts

Scout semantics are frozen. A scout is a presence screen, not an adoption extract.

Contracts: [`scout_contracts.md`](./scout_contracts.md)

## Scout prompts

| File | Role |
|---|---|
| `scout_shared_preamble.txt` | Shared presence-detector shell |
| `scout_jobs.txt` | Jobs-room presence overlay |
| `scout_owned.txt` | Owned-room presence overlay |
| `scout_third_party.txt` | Third-party presence overlay |

`signal_gated_search.prompting.build_scout_prompt` expands `{shared_preamble}` and the company placeholders. The API `response_format` enforces the JSON shape. Code maps `evidence_bin` to confidence, then to `signal`.

## Dig prompts

| File | Role |
|---|---|
| `dig_shared_preamble.txt` | Adoption extract. Cold start. Presence is not adoption. |
| `dig_jobs.txt` | Jobs-room extract overlay (PCS `channel_jobs.txt`) |
| `dig_owned.txt` | Owned-room extract overlay. SGS includes the site and official accounts. PCS owned is host-only. |
| `dig_third_party.txt` | Third-party extract overlay. Independent narrators. Official company accounts are owned. |

Dig `response_format` reuses the PCS findings schema. Scout URLs are traces only. They are not dig input.
