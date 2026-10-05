# Parallel Channel Search prompts

The live PCS runner calls `parallel_channel_search.prompting.build_channel_prompt`.

## Layout

| File | Role |
|---|---|
| `shared_preamble.txt` | Shared mission, sibling map, use-vs-sell, standards, JSON schema |
| `channel_jobs.txt` | Jobs specialist contract (`{shared_preamble}` placeholder) |
| `channel_owned.txt` | Owned specialist contract |
| `channel_third_party.txt` | Third-party specialist contract |

`build_channel_prompt` expands `{shared_preamble}` from `shared_preamble.txt`, then fills `company_id`, `company_name`, `homepage_url`, and `short_description`.

## Design rules baked in

- Equal-depth specialists. Prompts steer the search. There is no domain-filter allowlist.
- Each agent knows the overall goal and the sibling rooms. The prompt does not mention UAS or SGS.
- Source-shape steering says where to look. It does not include March finding examples of what adoption looks like.
- Sibling rooms steer the search budget. They are not a veto. Report qualifying evidence even if it is off-room. Merge dedupes it.
- The hard exclude is use-versus-sell only.
