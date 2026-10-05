# Portfolio hygiene plan

This program makes the public tree match the live batch system, then rewrites the root README.
A clone gets `pyproject.toml`, a pytest workflow, and `python -m production` as the batch command.
`python -m production` runs the `production` package as a program.
The March 2026 study stays in `legacy_agent_march_2026`.
Fourteen pull requests land in order from pr-1 through pr-14.
pr-14 is the only edit to `README.md`.
The operator reviews the stack and lands it. No owner merges.
This file in the repo is `docs/portfolio-hygiene-plan.md`. Execution has not started.

## How to read this

One box is one unit of work. Every box names the evidence that checks it. A nested box is a sub-step of the box above it. Check a box only when its evidence exists, a file, a log line, a screenshot, a test run, or a SHA. The body is a how-to. The appendices explain and record.

The program runs `pstack/skills/poteto-mode/playbooks/autopilot-stack.md`. The operator lands every PR. Owners stop at a verified stack link. pr-1, pr-3, pr-4, pr-5, pr-13, and pr-14 are review-gated and stop for the operator's click in chat.

Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

## Program checklist

### Arm the program

- [ ] State the protocol and this plan to the operator, then stop. Start execution only on the operator's explicit go.
- [ ] Read these from trunk at program start. Re-read them at every tick.
- [ ] `git show origin/main:pstack/skills/poteto-mode/playbooks/autopilot-stack.md`
- [ ] `git show origin/main:pstack/skills/swarm/SKILL.md`
- [ ] `git show origin/main:pstack/skills/poteto-mode/playbooks/opening-a-pr.md`
- [ ] `git show origin/main:pstack/skills/principle-sequence-verifiable-units/SKILL.md`
- [ ] `git show origin/main:pstack/skills/principle-subtract-before-you-add/SKILL.md`
- [ ] `git show origin/main:pstack/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md`
- [ ] On the operator's go, arm the audit tick as `/loop 1h` with the tick prompt below. Never leave the cadence to memory.
- [ ] Use this tick prompt, verbatim. "Re-read the execution playbook from trunk. Audit the operation against it and fix drift in this tick. Probe every active lane and judge progress by side effects only. Stand down a stuck lane and dispatch its replacement now. Then post a short status message to the operator in chat only when the audit found a tracked change that no earlier status message reported, such as a PR opened, a code-ready head, a round launched or closed, a verdict, a merge, a stuck agent and the action taken, a blocker added or cleared, or a decision only the operator can make. Name every such change and nothing else. Do not repeat a table, the merged list, or an unchanged blocker. If the audit found none, end the turn with no reply text. Either way, log this tick's row in your decision trail. The row names the items reported, or none."
- [ ] On the operator's hold or stand-down, send every owner a zero-writes order at once.

### Spawn owners

- [ ] Spawn one owner per PR with the full lifecycle in `playbooks/autopilot-stack.md`.
- [ ] Follow this dependency graph. Start dependent work only after its parent branch exists, and base the child on the parent branch.
- [ ] pr-1 branches from `main`.
- [ ] pr-2 after pr-1. pr-3 after pr-2. pr-4 after pr-3. pr-5 after pr-4. pr-6 after pr-5. pr-7 after pr-6. pr-8 after pr-7. pr-9 after pr-8. pr-10 after pr-9. pr-11 after pr-10. pr-12 after pr-11. pr-13 after pr-12. pr-14 after pr-13.
- [ ] Hold the file boundaries. pr-14 touches only `README.md` and `tests/test_readme_live_command.py`. pr-9 does not edit the three `agent_call.py` files. pr-11 does not edit `signal_gated_search/agent_call.py`. pr-13 does not delete `summary.jsonl` files.
- [ ] Hold the review gate. pr-1, pr-3, pr-4, pr-5, pr-13, and pr-14 change a command, a tracked-file policy, or the root README. They wait for the operator's review in chat with screenshots and a video before the root appends the next link.
- [ ] Name each branch `cursor/<short-name>-c464`.

### PR mechanics, for every PR

- [ ] Resolve the forge once. Default to `gh`. If `command -v origin` succeeds and Origin can resolve the repository, use `origin pr` for every PR operation. Record any fallback to `gh`. Never require `gt`.
- [ ] Open the PR ready, never draft, per Opening a PR. Use the run's built-in PR tool when it has one, else `origin pr create --status open --base <parent-branch>` or `gh pr create --base <parent-branch>` according to the resolved forge. A stack child targets its parent branch.
- [ ] Run `python -m pytest -q` before the PR-facing push. Push with hooks on.
- [ ] Run the deslop skill before each commit and the no-comments skill before review.
- [ ] Triage every Bugbot and security-reviewer comment per `pstack/skills/poteto-mode/references/bugbot-triage.md`.
- [ ] Rebase onto the parent tip before the code-ready report. Keep that merge base in fix rounds.

### Verdict and merge, for every PR

- [ ] At the code-ready head SHA and at each later push that changes the patch, run the swarm per `pstack/skills/swarm/SKILL.md`. One gates lane. The ten live lanes from the PR's Verify, live block. The perf lane from its Verify, perf block. Two or more audit lanes, each with its own focus, that read the diff and the receipts and distrust the PR body. The root audits the receipts in the stack-ready report before the verdict.
- [ ] Clean only when every lane is `PASS`. Findings go back to the owner, including a defect that a lane filed as a note. A new head gets a fresh swarm and a fresh verdict, except for results that stay valid under the patch-id rule in `playbooks/shipping.md`.
- [ ] No owner merges. A clean verdict appends the PR to the one linear stack. The operator lands the stack bottom-up after the review-gated clicks. Apply the patch-id rule in `playbooks/shipping.md` when a rebase rewrites SHAs.

### Boot recipe, for every live lane

Each live lane runs on its own cloud VM at the PR head. This repo has no web UI. Drive the CLI in the shell. `control-cli` from `cursor-team-kit` is not installed in the environment that wrote this plan. Appendix C records that gap. The lane still runs the named command and saves a screenshot of the terminal.

- [ ] `git fetch origin <head-branch> && git checkout <head SHA>`.
- [ ] Create a virtual environment and run `pip install -e .` when pr-1 or a later PR is the head. Wait until `python -m pytest -q` can import the tree.
- [ ] Deliver input only as the command in the lane box. Do not call paid APIs. Do not pass `--live` or `--all`.
- [ ] Save every screenshot to `/tmp/swarm-<pr-id>/worker-<n>/<slug>.png` and return the paths with the report.

## Add a project file and a pytest workflow, pr-1

**Depends on.** None. Branch from `main`.

**Files.**

- [ ] Create `pyproject.toml`.
- [ ] Create `.github/workflows/pytest.yml`.
- [ ] Edit `requirements.txt` so the dependency names match `pyproject.toml`.
- [ ] Keep `pytest.ini` `testpaths` and `norecursedirs` behavior.

**Build.**

- [ ] Declare the runtime dependencies `httpx` and `perplexityai`, and the test dependency `pytest`.
- [ ] Set the package layout so `python -m pytest` and `python -m production` still resolve from a clean install.
- [ ] Add a workflow that runs `python -m pytest -q` on push and on pull request.
- [ ] Leave `README.md` unchanged.

**You see.**

- [ ] `python -m pytest -q` prints a summary line that ends in `passed`.
- [ ] `pip install -e .` finishes with a successful install line. `pip` installs the project from `pyproject.toml`. The `-e` flag means the install points at this checkout.

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Run `python -m pytest -q` and record the passed count. The count stays at least 180.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `composer-2.5-fast` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Run `python -m pytest -q` at trunk and at the head. Save `/tmp/swarm-pr-1/worker-1/lane-1.png`. Pass when both runs end in `passed` and the head count is at least the trunk count.
- [ ] Lane 2. Run `pip install -e .` in a fresh virtual environment at the head. Save `/tmp/swarm-pr-1/worker-2/lane-2.png`. Pass when the install command exits 0.
- [ ] Lane 3. Run `python -m production --help` at the head. Save `/tmp/swarm-pr-1/worker-3/lane-3.png`. Pass when the help text contains `run`, `dry-run`, `status`, `dedupe`, and `verify`.
- [ ] Lane 4. Run `python -m evals --help` at the head. Save `/tmp/swarm-pr-1/worker-4/lane-4.png`. Pass when the help text still lists `run-tuning`, `run-benchmarks`, and `run-verification`.
- [ ] Lane 5. Run `python -m citation_verification --help` at the head. Save `/tmp/swarm-pr-1/worker-5/lane-5.png`. Pass when the help text exits 0.
- [ ] Lane 6. Confirm `git diff origin/main -- README.md` is empty at the head. Save `/tmp/swarm-pr-1/worker-6/lane-6.png`. Pass when the diff command prints no lines.
- [ ] Lane 7. Confirm `legacy_agent_march_2026/src/stage_2/production_agent_runner.py` still exists. Save `/tmp/swarm-pr-1/worker-7/lane-7.png`. Pass when the file exists and `git grep -n 'import legacy_agent_march_2026' -- '*.py'` prints no live import outside that folder.
- [ ] Lane 8. Confirm `.github/workflows/pytest.yml` names `python -m pytest -q`. Save `/tmp/swarm-pr-1/worker-8/lane-8.png`. Pass when the workflow file contains that command.
- [ ] Lane 9. Confirm `pyproject.toml` lists `httpx`, `perplexityai`, and `pytest`. Save `/tmp/swarm-pr-1/worker-9/lane-9.png`. Pass when all three names appear in the file.
- [ ] Lane 10. Run `git grep -I -E 'sk-|pplx-|tvly-'` and confirm it prints nothing. Save `/tmp/swarm-pr-1/worker-10/lane-10.png`. Pass when the search prints no key material.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. Seconds for `python -m pytest -q` on trunk and on the PR head.
- [ ] Probe. Run `python -m pytest -q` on trunk, then on the head, then on trunk again. Record all three durations.
- [ ] Baseline. Record the first trunk duration before the head run.
- [ ] Rule. Fail when the head duration is more than 10 percent above the first trunk duration.

**Review gate.** The operator reviews before merge.

- [ ] Copy lane 1 screenshots into `/opt/cursor/artifacts/pr-1-review-lane-1.png`.
- [ ] Record a 30 to 60 second video of the editable install and the pytest summary on a lane VM. Save it as `/opt/cursor/artifacts/pr-1-review.mp4`.
- [ ] Post the screenshots and the video in chat. Stop at stack-ready. Wait for the operator.

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] Bugbot triage done.
- [ ] Rebased onto the parent tip after the verdict, patch-id unchanged.
- [ ] The root appends this PR to the stack. The operator lands it. The owner does not merge.

## Write the short docs a new reader opens first, pr-2

**Depends on.** pr-1.

**Files.**

- [ ] Create `AGENTS.md`.
- [ ] Create `presentation/README.md`.
- [ ] Edit `prompts/parallel_channel_search/README.md`.
- [ ] Edit `prompts/signal_gated_search/README.md`.
- [ ] Edit `prompts/shared/README.md`.
- [ ] Edit `legacy_agent_march_2026/README.md`.
- [ ] Do not edit `README.md` in this PR.

**Build.**

- [ ] In `AGENTS.md`, name `python -m production` as the batch command, name `sgs` as the default architecture, and state that live code must not import `legacy_agent_march_2026`.
- [ ] In `presentation/README.md`, state that the HTML files in that folder are the February 2026 and March 2026 decks.
- [ ] Remove the design-only and not-wired claims from `prompts/parallel_channel_search/README.md`. `parallel_channel_search/agent_call.py` already calls `build_channel_prompt`.
- [ ] Remove the claim that a composer will substitute placeholders from `prompts/signal_gated_search/README.md`. `signal_gated_search/prompting.py` already expands them.
- [ ] State in `legacy_agent_march_2026/README.md` that `production/` is already on the tree.

**You see.**

- [ ] `AGENTS.md` contains the string `python -m production` and the string `legacy_agent_march_2026`.
- [ ] `git diff origin/main -- README.md` prints no lines.

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Run `python -m pytest tests/test_march_reference_path.py -q`. The file passes.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `composer-2.5-fast` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Run `python -m pytest -q` at trunk and at the head. Save `/tmp/swarm-pr-2/worker-1/lane-1.png`. Pass when both runs end in `passed`.
- [ ] Lane 2. Open `AGENTS.md` and find the batch command. Save `/tmp/swarm-pr-2/worker-2/lane-2.png`. Pass when the file contains `python -m production` and `sgs`.
- [ ] Lane 3. Open `presentation/README.md` and find the February and March labels. Save `/tmp/swarm-pr-2/worker-3/lane-3.png`. Pass when the file names February 2026 and March 2026.
- [ ] Lane 4. Open `prompts/parallel_channel_search/README.md` and search for `DESIGN ONLY`. Save `/tmp/swarm-pr-2/worker-4/lane-4.png`. Pass when that string is absent.
- [ ] Lane 5. Open `prompts/signal_gated_search/README.md` and search for `will substitute`. Save `/tmp/swarm-pr-2/worker-5/lane-5.png`. Pass when that string is absent.
- [ ] Lane 6. Open `legacy_agent_march_2026/README.md` and search for `upcoming`. Save `/tmp/swarm-pr-2/worker-6/lane-6.png`. Pass when that string is absent from the sentence about `production/`.
- [ ] Lane 7. Confirm `README.md` has the same blob hash on trunk and on the head. Save `/tmp/swarm-pr-2/worker-7/lane-7.png`. Pass when `git diff <parent> -- README.md` prints no lines. `<parent>` is the base branch of this PR.
- [ ] Lane 8. Confirm `presentation/stage_1_results.html` is still tracked. Save `/tmp/swarm-pr-2/worker-8/lane-8.png`. Pass when the file is listed by `git ls-files presentation/stage_1_results.html`.
- [ ] Lane 9. Confirm `legacy_agent_march_2026/presentation/production_results.html` is still tracked. Save `/tmp/swarm-pr-2/worker-9/lane-9.png`. Pass when the file is listed by `git ls-files legacy_agent_march_2026/presentation/production_results.html`.
- [ ] Lane 10. Run `python -m production --help`. Save `/tmp/swarm-pr-2/worker-10/lane-10.png`. Pass when the help text still shows the default architecture `sgs`.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. Seconds for `python -m pytest -q` on trunk and on the PR head.
- [ ] Probe. Run `python -m pytest -q` on trunk, then on the head, then on trunk again. Record all three durations.
- [ ] Baseline. Record the first trunk duration before the head run.
- [ ] Rule. Fail when the head duration is more than 10 percent above the first trunk duration.

**Review gate.** None. pr-2 is not review-gated.

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] Bugbot triage done.
- [ ] Rebased onto the parent tip after the verdict, patch-id unchanged.
- [ ] The root appends this PR to the stack. The operator lands it. The owner does not merge.

## Delete unused eval YAML and one-shot tune scripts, pr-3

**Depends on.** pr-2.

**Files.**

- [ ] Delete `evals/configs/unified_adaptive_search.yaml`.
- [ ] Delete `evals/configs/parallel_channel_search.yaml`.
- [ ] Delete `evals/configs/signal_gated_search.yaml`.
- [ ] Delete `evals/configs/tuning/uas_screen_baseline.yaml`.
- [ ] Delete `evals/configs/tuning/uas_screen_effort_high.yaml`.
- [ ] Delete `evals/configs/tuning/uas_screen_search_high.yaml`.
- [ ] Delete `evals/configs/tuning/uas_screen_steps_15.yaml`.
- [ ] Delete `evals/tune/_rerun_search_high.py`.
- [ ] Delete `evals/tune/_retry_search_high_failures.py`.
- [ ] Delete `evals/tune/_max_none3_smoke.py`.
- [ ] Edit `evals/paths.py` and remove `CONFIGS_DIR` and `TUNING_CONFIGS_DIR` when nothing else reads them.
- [ ] Edit the related-artifacts list at the top of `docs/decision-log.md`, and append one new entry. Do not rewrite older entries.

**Build.**

- [ ] Confirm with `git grep` that no Python file calls `yaml.safe_load` or reads those YAML paths.
- [ ] Leave `DEFAULT_WEB_SEARCH_DEPTH` in `unified_adaptive_search/agent_call.py` set to `low`.
- [ ] Point the decision-log index at the Python defaults in `parallel_channel_search/channels.py`, `signal_gated_search/channels.py`, and `unified_adaptive_search/agent_call.py`.
- [ ] Append a decision entry that the YAML files were not loaded and that the UAS file contradicted `DEFAULT_WEB_SEARCH_DEPTH`.

**You see.**

- [ ] `git ls-files evals/configs` prints nothing.
- [ ] `git grep -n DEFAULT_WEB_SEARCH_DEPTH -- unified_adaptive_search/agent_call.py` shows `low`.

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Add `tests/test_no_unused_eval_configs.py` that fails if `evals/configs` contains a YAML file or if `CONFIGS_DIR` remains in `evals/paths.py`.
- [ ] Run `python -m pytest tests/test_no_unused_eval_configs.py tests/test_pcs_prompting.py tests/test_sgs_prompting.py -q`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `composer-2.5-fast` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Run `python -m pytest -q` at trunk and at the head. Save `/tmp/swarm-pr-3/worker-1/lane-1.png`. Pass when both runs end in `passed`.
- [ ] Lane 2. Run `git ls-files 'evals/configs/**'`. Save `/tmp/swarm-pr-3/worker-2/lane-2.png`. Pass when the command prints nothing.
- [ ] Lane 3. Run `git ls-files 'evals/tune/_*.py'`. Save `/tmp/swarm-pr-3/worker-3/lane-3.png`. Pass when the command prints nothing.
- [ ] Lane 4. Open `unified_adaptive_search/agent_call.py` and read `DEFAULT_WEB_SEARCH_DEPTH`. Save `/tmp/swarm-pr-3/worker-4/lane-4.png`. Pass when the assignment is the string `low`.
- [ ] Lane 5. Run `git grep -n 'import yaml' -- '*.py'`. Save `/tmp/swarm-pr-3/worker-5/lane-5.png`. Pass when the command prints nothing.
- [ ] Lane 6. Run `python -m evals cost-preview unified-adaptive-search`. Save `/tmp/swarm-pr-3/worker-6/lane-6.png`. Pass when the command exits 0 and does not say it loaded a YAML file.
- [ ] Lane 7. Confirm `evals/tune/matrix.py` still defines the UAS screen arms. Save `/tmp/swarm-pr-3/worker-7/lane-7.png`. Pass when the file still contains `web_search_depth`.
- [ ] Lane 8. Confirm `docs/decision-log.md` still contains the heading for the 2026-08-16 SGS ship decision. Save `/tmp/swarm-pr-3/worker-8/lane-8.png`. Pass when the heading text `Skip bake-off, ship SGS` is still present.
- [ ] Lane 9. Confirm an appended heading dated with the PR date exists below that ship decision. Save `/tmp/swarm-pr-3/worker-9/lane-9.png`. Pass when the new entry names the deleted YAML paths and does not edit the older paragraphs.
- [ ] Lane 10. Run `python -m production dry-run --help`. Save `/tmp/swarm-pr-3/worker-10/lane-10.png`. Pass when the help text exits 0.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. Seconds for `python -m pytest -q` on trunk and on the PR head.
- [ ] Probe. Run `python -m pytest -q` on trunk, then on the head, then on trunk again. Record all three durations.
- [ ] Baseline. Record the first trunk duration before the head run.
- [ ] Rule. Fail when the head duration is more than 10 percent above the first trunk duration.

**Review gate.** The operator reviews before merge.

- [ ] Copy lane 1 screenshots into `/opt/cursor/artifacts/pr-3-review-lane-1.png`.
- [ ] Record a 30 to 60 second video of the empty `git ls-files` for `evals/configs` and the `low` default in `unified_adaptive_search/agent_call.py` on a lane VM. Save it as `/opt/cursor/artifacts/pr-3-review.mp4`.
- [ ] Post the screenshots and the video in chat. Stop at stack-ready. Wait for the operator.

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] Bugbot triage done.
- [ ] Rebased onto the parent tip after the verdict, patch-id unchanged.
- [ ] The root appends this PR to the stack. The operator lands it. The owner does not merge.

## Make the eval stub commands name the real verifier, pr-4

**Depends on.** pr-3.

**Files.**

- [ ] Edit `evals/cli.py`.
- [ ] Edit `evals/__init__.py`.
- [ ] Edit `evals/dashboard/landing.py`.
- [ ] Edit `evals/hooks/stage3_judge.py`.
- [ ] Create `tests/test_evals_cli_stubs.py`.
- [ ] Append one entry to `docs/decision-log.md`. Do not rewrite older entries.

**Build.**

- [ ] Change `run-benchmarks` so it does not call `create_stub_instance`.
- [ ] Change `run-verification` so it does not call `create_stub_instance`.
- [ ] Print that the bake-off was skipped and that citation checks run through `python -m production verify` and `python -m citation_verification`.
- [ ] Exit with code 2 for both commands.
- [ ] Make `evals/hooks/stage3_judge.py` raise `NotImplementedError` or become a one-line pointer module that no CLI calls. Do not add a second judge.

**You see.**

- [ ] `python -m evals run-verification` prints `python -m production verify` and exits 2.
- [ ] `python -m evals run-benchmarks uas` prints that the bake-off was skipped and exits 2.
- [ ] The command writes no directory under `evals/instances/`.

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] `tests/test_evals_cli_stubs.py` calls `main` with those argv lists and asserts exit code 2 and the printed command.
- [ ] Run `python -m pytest tests/test_evals_cli_stubs.py -q`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `composer-2.5-fast` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Run `python -m pytest -q` at trunk and at the head. Save `/tmp/swarm-pr-4/worker-1/lane-1.png`. Pass when both runs end in `passed`.
- [ ] Lane 2. Run `python -m evals run-verification` at the head. Save `/tmp/swarm-pr-4/worker-2/lane-2.png`. Pass when the exit code is 2 and the output contains `python -m production verify`.
- [ ] Lane 3. Run `python -m evals run-benchmarks uas` at the head. Save `/tmp/swarm-pr-4/worker-3/lane-3.png`. Pass when the exit code is 2 and the output says the bake-off was skipped.
- [ ] Lane 4. Run `python -m evals run-verification` at trunk and record that trunk writes a stub instance. The head must not write one. Save `/tmp/swarm-pr-4/worker-4/lane-4.png`. Pass when the head process creates no new directory under `evals/instances/`.
- [ ] Lane 5. Run `python -m evals cost-preview unified-adaptive-search` at the head. Save `/tmp/swarm-pr-4/worker-5/lane-5.png`. Pass when the command exits 0.
- [ ] Lane 6. Run `python -m citation_verification --help` at the head. Save `/tmp/swarm-pr-4/worker-6/lane-6.png`. Pass when the command exits 0.
- [ ] Lane 7. Run `python -m production verify --help` at the head. Save `/tmp/swarm-pr-4/worker-7/lane-7.png`. Pass when the help text exits 0.
- [ ] Lane 8. Confirm `evals/hooks/stage3_judge.py` is not imported by `evals/cli.py`. Save `/tmp/swarm-pr-4/worker-8/lane-8.png`. Pass when `git grep -n stage3_judge -- evals/cli.py` prints nothing.
- [ ] Lane 9. Confirm `git diff <parent> -- README.md` is empty. Save `/tmp/swarm-pr-4/worker-9/lane-9.png`. Pass when the diff prints no lines.
- [ ] Lane 10. Confirm `docs/decision-log.md` gained one appended entry and the 2026-08-16 ship heading is unchanged. Save `/tmp/swarm-pr-4/worker-10/lane-10.png`. Pass when the ship heading text is byte-identical to the parent and a new heading exists after it.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. Seconds for `python -m pytest -q` on trunk and on the PR head.
- [ ] Probe. Run `python -m pytest -q` on trunk, then on the head, then on trunk again. Record all three durations.
- [ ] Baseline. Record the first trunk duration before the head run.
- [ ] Rule. Fail when the head duration is more than 10 percent above the first trunk duration.

**Review gate.** The operator reviews before merge.

- [ ] Copy lane 1 screenshots into `/opt/cursor/artifacts/pr-4-review-lane-1.png`.
- [ ] Record a 30 to 60 second video of `python -m evals run-verification` exiting 2 with the production command in the output on a lane VM. Save it as `/opt/cursor/artifacts/pr-4-review.mp4`.
- [ ] Post the screenshots and the video in chat. Stop at stack-ready. Wait for the operator.

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] Bugbot triage done.
- [ ] Rebased onto the parent tip after the verdict, patch-id unchanged.
- [ ] The root appends this PR to the stack. The operator lands it. The owner does not merge.

## Stop tracking the agent plan files, pr-5

**Depends on.** pr-4.

**Files.**

- [ ] Delete the tracked files under `.cursor/plans/`.
- [ ] Edit `.gitignore` so `.cursor/plans/` is ignored.
- [ ] Keep `.cursor/rules/decision-log.mdc` tracked.
- [ ] Edit the related-artifacts list in `docs/decision-log.md` and append one entry. Do not rewrite older entries.

**Build.**

- [ ] Run `git rm` on each tracked file in `.cursor/plans/`.
- [ ] Leave the historical paragraphs that name those paths in place.
- [ ] Point the related-artifacts list at `docs/decision-log.md` as the record that remains in git.

**You see.**

- [ ] `git ls-files .cursor/plans` prints nothing.
- [ ] `git ls-files .cursor/rules/decision-log.mdc` prints that file.

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Add `tests/test_plans_untracked.py` that fails if `git ls-files .cursor/plans` prints a path.
- [ ] Run `python -m pytest tests/test_plans_untracked.py tests/test_march_reference_path.py -q`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `composer-2.5-fast` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Run `python -m pytest -q` at trunk and at the head. Save `/tmp/swarm-pr-5/worker-1/lane-1.png`. Pass when both runs end in `passed`.
- [ ] Lane 2. Run `git ls-files .cursor/plans`. Save `/tmp/swarm-pr-5/worker-2/lane-2.png`. Pass when the command prints nothing.
- [ ] Lane 3. Run `git ls-files .cursor/rules/decision-log.mdc`. Save `/tmp/swarm-pr-5/worker-3/lane-3.png`. Pass when the command prints `.cursor/rules/decision-log.mdc`.
- [ ] Lane 4. Run `git check-ignore -v .cursor/plans/sgs-design.md`. Save `/tmp/swarm-pr-5/worker-4/lane-4.png`. Pass when the command names `.gitignore`.
- [ ] Lane 5. Confirm `docs/decision-log.md` still contains `Skip bake-off, ship SGS`. Save `/tmp/swarm-pr-5/worker-5/lane-5.png`. Pass when that heading is present.
- [ ] Lane 6. Confirm the related-artifacts list no longer presents `.cursor/plans/` as a current path a clone contains. Save `/tmp/swarm-pr-5/worker-6/lane-6.png`. Pass when the index paragraph says the plan files are untracked.
- [ ] Lane 7. Confirm `README.md` is unchanged against the parent. Save `/tmp/swarm-pr-5/worker-7/lane-7.png`. Pass when `git diff <parent> -- README.md` prints no lines.
- [ ] Lane 8. Confirm `legacy_agent_march_2026/` is still tracked. Save `/tmp/swarm-pr-5/worker-8/lane-8.png`. Pass when `git ls-files legacy_agent_march_2026/README.md` prints that path.
- [ ] Lane 9. Confirm `prompts/citation_verification/judge.txt` is still tracked. Save `/tmp/swarm-pr-5/worker-9/lane-9.png`. Pass when `git ls-files prompts/citation_verification/judge.txt` prints that path.
- [ ] Lane 10. Run `python -m production --help`. Save `/tmp/swarm-pr-5/worker-10/lane-10.png`. Pass when the help text exits 0.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. Seconds for `python -m pytest -q` on trunk and on the PR head.
- [ ] Probe. Run `python -m pytest -q` on trunk, then on the head, then on trunk again. Record all three durations.
- [ ] Baseline. Record the first trunk duration before the head run.
- [ ] Rule. Fail when the head duration is more than 10 percent above the first trunk duration.

**Review gate.** The operator reviews before merge.

- [ ] Copy lane 1 screenshots into `/opt/cursor/artifacts/pr-5-review-lane-1.png`.
- [ ] Record a 30 to 60 second video of `git ls-files .cursor/plans` printing nothing and the decision-log rule file still tracked on a lane VM. Save it as `/opt/cursor/artifacts/pr-5-review.mp4`.
- [ ] Post the screenshots and the video in chat. Stop at stack-ready. Wait for the operator.

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] Bugbot triage done.
- [ ] Rebased onto the parent tip after the verdict, patch-id unchanged.
- [ ] The root appends this PR to the stack. The operator lands it. The owner does not merge.

## Delete channel fields and helpers nothing reads, pr-6

**Depends on.** pr-5.

**Files.**

- [ ] Edit `parallel_channel_search/channels.py`.
- [ ] Edit `signal_gated_search/channels.py`.
- [ ] Edit `unified_adaptive_search/agent_call.py`.

**Build.**

- [ ] Search the repo for `search_domain_filter`, `instruction_hint`, `DEFAULT_CHANNEL_PRIOR`, `DEFAULT_DIG_PRESET`, `DEFAULT_RESCUE_DIG_PRESET`, and `from_preset_defaults`.
- [ ] Delete those names when the search shows definitions and no readers.
- [ ] Delete the `hints` dict in `default_channel_configs` when it exists only to fill `instruction_hint`.
- [ ] Leave `DEFAULT_WEB_SEARCH_DEPTH`, `DIG_EFFORT_BY_COUNT`, and the live scout and dig defaults in place.

**You see.**

- [ ] `git grep -n instruction_hint -- '*.py'` prints nothing.
- [ ] `python -m pytest tests/test_pcs_prompting.py tests/test_sgs_prompting.py tests/test_sgs_gate.py -q` ends in `passed`.

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Extend `tests/test_pcs_prompting.py` or add a small test that `ChannelConfig` has no `search_domain_filter` field.
- [ ] Run `python -m pytest tests/test_pcs_prompting.py tests/test_sgs_runner.py tests/test_sgs_gate.py -q`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `composer-2.5-fast` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Run `python -m pytest -q` at trunk and at the head. Save `/tmp/swarm-pr-6/worker-1/lane-1.png`. Pass when both runs end in `passed`.
- [ ] Lane 2. Run `git grep -n search_domain_filter -- '*.py'`. Save `/tmp/swarm-pr-6/worker-2/lane-2.png`. Pass when the command prints nothing.
- [ ] Lane 3. Run `git grep -n from_preset_defaults -- '*.py'`. Save `/tmp/swarm-pr-6/worker-3/lane-3.png`. Pass when the command prints nothing.
- [ ] Lane 4. Run `git grep -n DEFAULT_CHANNEL_PRIOR -- '*.py'`. Save `/tmp/swarm-pr-6/worker-4/lane-4.png`. Pass when the command prints nothing.
- [ ] Lane 5. Run `python -m parallel_channel_search --help`. Save `/tmp/swarm-pr-6/worker-5/lane-5.png`. Pass when the command exits 0.
- [ ] Lane 6. Run a dry `python -m parallel_channel_search` request build if the CLI supports dry run without a key. If it requires a company fixture, run the dry path used in `tests/test_pcs_prompting.py`. Save `/tmp/swarm-pr-6/worker-6/lane-6.png`. Pass when the test file passes and no API call is made.
- [ ] Lane 7. Run `python -m signal_gated_search --help`. Save `/tmp/swarm-pr-6/worker-7/lane-7.png`. Pass when the command exits 0.
- [ ] Lane 8. Confirm `DEFAULT_SCOUT_PRESET` in `signal_gated_search/channels.py` is still `low`. Save `/tmp/swarm-pr-6/worker-8/lane-8.png`. Pass when the assignment is `low`.
- [ ] Lane 9. Confirm `DEFAULT_DIG_MAX_STEPS` is still 50. Save `/tmp/swarm-pr-6/worker-9/lane-9.png`. Pass when the assignment is 50.
- [ ] Lane 10. Confirm `README.md` is unchanged against the parent. Save `/tmp/swarm-pr-6/worker-10/lane-10.png`. Pass when `git diff <parent> -- README.md` prints no lines.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. Seconds for `python -m pytest -q` on trunk and on the PR head.
- [ ] Probe. Run `python -m pytest -q` on trunk, then on the head, then on trunk again. Record all three durations.
- [ ] Baseline. Record the first trunk duration before the head run.
- [ ] Rule. Fail when the head duration is more than 10 percent above the first trunk duration.

**Review gate.** None. pr-6 is not review-gated.

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] Bugbot triage done.
- [ ] Rebased onto the parent tip after the verdict, patch-id unchanged.
- [ ] The root appends this PR to the stack. The operator lands it. The owner does not merge.

## Move APIKeys out of the Stage 1 import side effect, pr-7

**Depends on.** pr-6.

**Files.**

- [ ] Create `src/keys.py` with `APIKeys` and `_load_credential`.
- [ ] Edit `src/config.py` so Stage 1 imports `APIKeys` from `src.keys` and the import of `src.config` no longer has to be the key loader for Stage 2.
- [ ] Edit `parallel_channel_search/agent_call.py`, `signal_gated_search/agent_call.py`, `unified_adaptive_search/agent_call.py`, and `citation_verification/judge.py` to import `APIKeys` from `src.keys`.
- [ ] Edit the live Stage 1 modules that import `APIKeys` from `src.config` so they import it from `src.keys`.
- [ ] Do not edit `legacy_agent_march_2026/`.

**Build.**

- [ ] Move the class in one change and delete the old class body from `src/config.py`.
- [ ] Keep the directory creation in `src/config.py` so Stage 1 behavior stays, and stop Stage 2 and Stage 3 from importing `src.config` only to read a key.
- [ ] Leave `citation_verification/backup_fetch.py` `_tavily_api_key` in place in this PR. A later PR can fold it into `src.keys` only if the fold stays inside pr-11.

**You see.**

- [ ] `git grep -n 'from src.config import APIKeys' -- '*.py'` prints no hits outside `legacy_agent_march_2026/`.
- [ ] A dry import of `parallel_channel_search.agent_call` does not require the Stage 2 output directories to be created by that import. Importing `src.config` may still create them for Stage 1.

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Add `tests/test_api_keys_module.py` that loads `APIKeys` from `src.keys` with an env var and asserts the matching field.
- [ ] Run `python -m pytest tests/test_api_keys_module.py tests/test_citation_verification_judge.py tests/test_sgs_live.py -q`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `composer-2.5-fast` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Run `python -m pytest -q` at trunk and at the head. Save `/tmp/swarm-pr-7/worker-1/lane-1.png`. Pass when both runs end in `passed`.
- [ ] Lane 2. Run `git grep -n 'from src.config import APIKeys' -- '*.py'`. Save `/tmp/swarm-pr-7/worker-2/lane-2.png`. Pass when every hit is under `legacy_agent_march_2026/`.
- [ ] Lane 3. Run `python -c 'from src.keys import APIKeys; print(APIKeys.__module__)'`. Save `/tmp/swarm-pr-7/worker-3/lane-3.png`. Pass when the printed module is `src.keys`.
- [ ] Lane 4. Run `python -m pytest tests/test_api_keys_module.py -q`. Save `/tmp/swarm-pr-7/worker-4/lane-4.png`. Pass when the run ends in `passed`.
- [ ] Lane 5. Run `python -m production --help`. Save `/tmp/swarm-pr-7/worker-5/lane-5.png`. Pass when the command exits 0.
- [ ] Lane 6. Run `python -m citation_verification --help`. Save `/tmp/swarm-pr-7/worker-6/lane-6.png`. Pass when the command exits 0.
- [ ] Lane 7. Confirm `legacy_agent_march_2026/src/config.py` still defines `class APIKeys`. Save `/tmp/swarm-pr-7/worker-7/lane-7.png`. Pass when the class is still in that file.
- [ ] Lane 8. Confirm `src/stage_1/classifier.py` imports `APIKeys` from `src.keys` or through a re-export that does not duplicate the loader. Save `/tmp/swarm-pr-7/worker-8/lane-8.png`. Pass when `git grep -n 'from src.keys import APIKeys' -- src/stage_1/classifier.py` prints a hit.
- [ ] Lane 9. Confirm no file under `legacy_agent_march_2026/` changed against the parent. Save `/tmp/swarm-pr-7/worker-9/lane-9.png`. Pass when `git diff <parent> -- legacy_agent_march_2026` prints no lines.
- [ ] Lane 10. Confirm `README.md` is unchanged against the parent. Save `/tmp/swarm-pr-7/worker-10/lane-10.png`. Pass when `git diff <parent> -- README.md` prints no lines.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. Seconds for `python -m pytest -q` on trunk and on the PR head.
- [ ] Probe. Run `python -m pytest -q` on trunk, then on the head, then on trunk again. Record all three durations.
- [ ] Baseline. Record the first trunk duration before the head run.
- [ ] Rule. Fail when the head duration is more than 10 percent above the first trunk duration.

**Review gate.** None. pr-7 is not review-gated.

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] Bugbot triage done.
- [ ] Rebased onto the parent tip after the verdict, patch-id unchanged.
- [ ] The root appends this PR to the stack. The operator lands it. The owner does not merge.

## Put the finding JSON schema in contracts, pr-8

**Depends on.** pr-7.

**Files.**

- [ ] Create `contracts/schema.py` with the shared finding `RESPONSE_SCHEMA`.
- [ ] Edit `parallel_channel_search/prompting.py` and `unified_adaptive_search/prompting.py` to import that object and delete the pasted copies.
- [ ] Edit `signal_gated_search/agent_call.py` so `DIG_RESPONSE_SCHEMA` is the contracts object.
- [ ] Edit `tests/test_sgs_prompting.py` so it imports the schema from `contracts.schema`.

**Build.**

- [ ] Keep one schema object. SGS digs and both prompting modules must reference that object.
- [ ] Leave scout `SCOUT_RESPONSE_SCHEMA` in `signal_gated_search` for pr-12.

**You see.**

- [ ] `tests/test_sgs_prompting.py` assertion `DIG_RESPONSE_SCHEMA is RESPONSE_SCHEMA` passes when both names are the contracts object.

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Run `python -m pytest tests/test_sgs_prompting.py tests/test_pcs_prompting.py -q`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `composer-2.5-fast` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Run `python -m pytest -q` at trunk and at the head. Save `/tmp/swarm-pr-8/worker-1/lane-1.png`. Pass when both runs end in `passed`.
- [ ] Lane 2. Run `git grep -n RESPONSE_SCHEMA -- '*.py'`. Save `/tmp/swarm-pr-8/worker-2/lane-2.png`. Pass when the contracts module is the definition and the packages import it.
- [ ] Lane 3. Run `python -m pytest tests/test_sgs_prompting.py -q`. Save `/tmp/swarm-pr-8/worker-3/lane-3.png`. Pass when the run ends in `passed`.
- [ ] Lane 4. Confirm `contracts/schema.py` defines `RESPONSE_SCHEMA`. Save `/tmp/swarm-pr-8/worker-4/lane-4.png`. Pass when the name is in that file.
- [ ] Lane 5. Confirm `parallel_channel_search/prompting.py` does not contain a second pasted `json_schema` properties block for findings. Save `/tmp/swarm-pr-8/worker-5/lane-5.png`. Pass when `git grep -n '"AI_tool_used"' -- parallel_channel_search/prompting.py` prints nothing.
- [ ] Lane 6. Confirm `unified_adaptive_search/prompting.py` imports `RESPONSE_SCHEMA` from `contracts.schema`. Save `/tmp/swarm-pr-8/worker-6/lane-6.png`. Pass when the import line is present.
- [ ] Lane 7. Run `python -m parallel_channel_search --help`. Save `/tmp/swarm-pr-8/worker-7/lane-7.png`. Pass when the command exits 0.
- [ ] Lane 8. Run `python -m unified_adaptive_search --help`. Save `/tmp/swarm-pr-8/worker-8/lane-8.png`. Pass when the command exits 0.
- [ ] Lane 9. Confirm `README.md` is unchanged against the parent. Save `/tmp/swarm-pr-8/worker-9/lane-9.png`. Pass when `git diff <parent> -- README.md` prints no lines.
- [ ] Lane 10. Confirm `prompts/stage_2_perplexity_prompt.txt` is unchanged against the parent. Save `/tmp/swarm-pr-8/worker-10/lane-10.png`. Pass when `git diff <parent> -- prompts/stage_2_perplexity_prompt.txt` prints no lines.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. Seconds for `python -m pytest -q` on trunk and on the PR head.
- [ ] Probe. Run `python -m pytest -q` on trunk, then on the head, then on trunk again. Record all three durations.
- [ ] Baseline. Record the first trunk duration before the head run.
- [ ] Rule. Fail when the head duration is more than 10 percent above the first trunk duration.

**Review gate.** None. pr-8 is not review-gated.

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] Bugbot triage done.
- [ ] Rebased onto the parent tip after the verdict, patch-id unchanged.
- [ ] The root appends this PR to the stack. The operator lands it. The owner does not merge.

## Add one Perplexity agent client with tests and no caller switch, pr-9

**Depends on.** pr-8.

**Files.**

- [ ] Create `agent_api/__init__.py` and `agent_api/client.py`.
- [ ] Create `tests/test_agent_api_client.py`.
- [ ] Do not edit `parallel_channel_search/agent_call.py`, `unified_adaptive_search/agent_call.py`, or `signal_gated_search/agent_call.py` in this PR.

**Build.**

- [ ] Move the shared mechanics into `agent_api.client`. Those mechanics are the search-depth ladder, the JSON object extractor, `require_api_key`, and `execute_agent_call`.
- [ ] Match the Parallel Channel Search behavior where a parse failure keeps the metered `cost_usd` and sets an error on the result.
- [ ] Read keys through `src.keys.APIKeys`.
- [ ] Add tests that call the client with a fake HTTP response and assert the ladder for `low`, `medium`, and `high`, plus a parse failure.

**You see.**

- [ ] `python -m pytest tests/test_agent_api_client.py -q` ends in `passed`.
- [ ] `git diff <parent> -- parallel_channel_search unified_adaptive_search signal_gated_search` prints no lines.

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] `tests/test_agent_api_client.py` covers the depth ladder and a JSON parse failure without a network call.
- [ ] Run `python -m pytest tests/test_agent_api_client.py -q`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `composer-2.5-fast` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Run `python -m pytest -q` at trunk and at the head. Save `/tmp/swarm-pr-9/worker-1/lane-1.png`. Pass when both runs end in `passed` and the head count is greater than the trunk count.
- [ ] Lane 2. Run `python -m pytest tests/test_agent_api_client.py -q`. Save `/tmp/swarm-pr-9/worker-2/lane-2.png`. Pass when the run ends in `passed`.
- [ ] Lane 3. Confirm `agent_api/client.py` defines `execute_agent_call` and `require_api_key`. Save `/tmp/swarm-pr-9/worker-3/lane-3.png`. Pass when both names are defined in that file.
- [ ] Lane 4. Confirm the three architecture `agent_call.py` files are unchanged against the parent. Save `/tmp/swarm-pr-9/worker-4/lane-4.png`. Pass when `git diff <parent> -- parallel_channel_search/agent_call.py unified_adaptive_search/agent_call.py signal_gated_search/agent_call.py` prints no lines.
- [ ] Lane 5. Confirm `citation_verification/fetch.py` is unchanged against the parent. Save `/tmp/swarm-pr-9/worker-5/lane-5.png`. Pass when `git diff <parent> -- citation_verification/fetch.py` prints no lines.
- [ ] Lane 6. Run `python -m production --help`. Save `/tmp/swarm-pr-9/worker-6/lane-6.png`. Pass when the command exits 0.
- [ ] Lane 7. Run `python -m parallel_channel_search --help`. Save `/tmp/swarm-pr-9/worker-7/lane-7.png`. Pass when the command exits 0.
- [ ] Lane 8. Confirm the new tests do not read `credentials/`. Save `/tmp/swarm-pr-9/worker-8/lane-8.png`. Pass when `git grep -n credentials -- tests/test_agent_api_client.py` prints nothing.
- [ ] Lane 9. Confirm `DEFAULT_WEB_SEARCH_DEPTH` in `unified_adaptive_search/agent_call.py` is still `low`. Save `/tmp/swarm-pr-9/worker-9/lane-9.png`. Pass when the assignment is `low`.
- [ ] Lane 10. Confirm `README.md` is unchanged against the parent. Save `/tmp/swarm-pr-9/worker-10/lane-10.png`. Pass when `git diff <parent> -- README.md` prints no lines.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. Seconds for `python -m pytest -q` on trunk and on the PR head.
- [ ] Probe. Run `python -m pytest -q` on trunk, then on the head, then on trunk again. Record all three durations.
- [ ] Baseline. Record the first trunk duration before the head run.
- [ ] Rule. Fail when the head duration exceeds the first trunk duration by more than 60 seconds. The head suite contains the new client tests, so a percentage against the shorter trunk suite is the wrong comparison.

**Review gate.** None. pr-9 is not review-gated.

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] Bugbot triage done.
- [ ] Rebased onto the parent tip after the verdict, patch-id unchanged.
- [ ] The root appends this PR to the stack. The operator lands it. The owner does not merge.

## Switch Parallel Channel Search and signal-gated digs to the shared client, pr-10

**Depends on.** pr-9.

**Files.**

- [ ] Edit `parallel_channel_search/agent_call.py` and `parallel_channel_search/runner.py`.
- [ ] Edit the dig import in `signal_gated_search/agent_call.py`.
- [ ] Edit tests that import `execute_agent_call` or `require_api_key` from `parallel_channel_search.agent_call`.

**Build.**

- [ ] Replace the PCS copy of `execute_agent_call`, the depth ladder, and `require_api_key` with calls into `agent_api.client`.
- [ ] Point SGS digs at `agent_api.client` in this same PR, because they call the PCS function today.
- [ ] Keep PCS channel prompt building in `parallel_channel_search/prompting.py`.
- [ ] Delete the unused private helpers from `parallel_channel_search/agent_call.py` after the callers compile.

**You see.**

- [ ] `python -m pytest tests/test_pcs_prompting.py tests/test_sgs_runner.py tests/test_sgs_live.py -q` ends in `passed`.
- [ ] A dry PCS request uses the same model, steps, effort, and `web_search_depth` as the parent.

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Add a test that the PCS dry request kwargs match a recorded literal for model `openai/gpt-5.6-luna`, `max_steps` 50, effort `medium`, and search depth `medium`.
- [ ] Run `python -m pytest tests/test_pcs_prompting.py tests/test_sgs_prompting.py tests/test_sgs_runner.py -q`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `composer-2.5-fast` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Run `python -m pytest -q` at trunk and at the head. Save `/tmp/swarm-pr-10/worker-1/lane-1.png`. Pass when both runs end in `passed`.
- [ ] Lane 2. Run the new PCS kwargs test. Save `/tmp/swarm-pr-10/worker-2/lane-2.png`. Pass when the test ends in `passed`.
- [ ] Lane 3. Run `git grep -n 'def execute_agent_call' -- parallel_channel_search/agent_call.py`. Save `/tmp/swarm-pr-10/worker-3/lane-3.png`. Pass when the command prints nothing.
- [ ] Lane 4. Run `git grep -n agent_api -- signal_gated_search/agent_call.py`. Save `/tmp/swarm-pr-10/worker-4/lane-4.png`. Pass when the dig path imports `agent_api`.
- [ ] Lane 5. Run `python -m parallel_channel_search --help`. Save `/tmp/swarm-pr-10/worker-5/lane-5.png`. Pass when the command exits 0.
- [ ] Lane 6. Run `python -m signal_gated_search --help`. Save `/tmp/swarm-pr-10/worker-6/lane-6.png`. Pass when the command exits 0.
- [ ] Lane 7. Confirm SGS scout functions still exist in `signal_gated_search/agent_call.py` for pr-12. Save `/tmp/swarm-pr-10/worker-7/lane-7.png`. Pass when `git grep -n execute_scout_call -- signal_gated_search/agent_call.py` prints a definition.
- [ ] Lane 8. Confirm `unified_adaptive_search/agent_call.py` is unchanged against the parent. Save `/tmp/swarm-pr-10/worker-8/lane-8.png`. Pass when `git diff <parent> -- unified_adaptive_search/agent_call.py` prints no lines.
- [ ] Lane 9. Confirm `DEFAULT_WEB_SEARCH_DEPTH` for PCS in `parallel_channel_search/channels.py` is still `medium`. Save `/tmp/swarm-pr-10/worker-9/lane-9.png`. Pass when the assignment is `medium`.
- [ ] Lane 10. Confirm `README.md` is unchanged against the parent. Save `/tmp/swarm-pr-10/worker-10/lane-10.png`. Pass when `git diff <parent> -- README.md` prints no lines.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. Seconds for `python -m pytest -q` on trunk and on the PR head.
- [ ] Probe. Run `python -m pytest -q` on trunk, then on the head, then on trunk again. Record all three durations.
- [ ] Baseline. Record the first trunk duration before the head run.
- [ ] Rule. Fail when the head duration is more than 10 percent above the first trunk duration.

**Review gate.** None. pr-10 is not review-gated.

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] Bugbot triage done.
- [ ] Rebased onto the parent tip after the verdict, patch-id unchanged.
- [ ] The root appends this PR to the stack. The operator lands it. The owner does not merge.

## Switch Unified Adaptive Search and the citation fetch to the shared client, pr-11

**Depends on.** pr-10.

**Files.**

- [ ] Edit `unified_adaptive_search/agent_call.py` and `unified_adaptive_search/runner.py`.
- [ ] Edit `citation_verification/fetch.py`.
- [ ] Edit `evals/tune/orchestrator.py`.
- [ ] Edit `citation_verification/backup_fetch.py` only to route `_tavily_api_key` through `src.keys` if that helper still loads a key on its own.

**Build.**

- [ ] Delete the UAS copies of `execute_agent_call`, the depth ladder, `require_api_key`, and `from_preset_defaults` if pr-6 left any of them.
- [ ] Keep `DEFAULT_WEB_SEARCH_DEPTH = "low"` as the UAS default passed into the shared client.
- [ ] Update `citation_verification/fetch.py` so it imports `require_api_key` from `agent_api.client`.
- [ ] Update `evals/tune/orchestrator.py` the same way.

**You see.**

- [ ] `python -m pytest tests/test_citation_verification_fetch_parse.py tests/test_pcs_prompting.py -q` ends in `passed`.
- [ ] UAS dry kwargs still show `web_search_depth` `low`.

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Add a test that UAS dry request kwargs use search depth `low`, effort `xhigh`, and `max_steps` 10.
- [ ] Run `python -m pytest tests/test_citation_verification_fetch_parse.py tests/test_citation_verification_runner_dry.py -q`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `composer-2.5-fast` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Run `python -m pytest -q` at trunk and at the head. Save `/tmp/swarm-pr-11/worker-1/lane-1.png`. Pass when both runs end in `passed`.
- [ ] Lane 2. Run the new UAS kwargs test. Save `/tmp/swarm-pr-11/worker-2/lane-2.png`. Pass when the test ends in `passed` and the depth value is `low`.
- [ ] Lane 3. Run `git grep -n 'def execute_agent_call' -- unified_adaptive_search/agent_call.py`. Save `/tmp/swarm-pr-11/worker-3/lane-3.png`. Pass when the command prints nothing.
- [ ] Lane 4. Run `git grep -n require_api_key -- citation_verification/fetch.py`. Save `/tmp/swarm-pr-11/worker-4/lane-4.png`. Pass when the import is `agent_api.client` or `agent_api`.
- [ ] Lane 5. Run `git grep -n require_api_key -- evals/tune/orchestrator.py`. Save `/tmp/swarm-pr-11/worker-5/lane-5.png`. Pass when the import is `agent_api.client` or `agent_api`.
- [ ] Lane 6. Run `python -m unified_adaptive_search --help`. Save `/tmp/swarm-pr-11/worker-6/lane-6.png`. Pass when the command exits 0.
- [ ] Lane 7. Run `python -m citation_verification --help`. Save `/tmp/swarm-pr-11/worker-7/lane-7.png`. Pass when the command exits 0.
- [ ] Lane 8. Confirm `signal_gated_search/agent_call.py` scout execute function is unchanged against the parent except for edits pr-10 already made on the dig path. The diff of this PR against its parent does not rewrite `execute_scout_call`. Save `/tmp/swarm-pr-11/worker-8/lane-8.png`. Pass when `git diff <parent> -- signal_gated_search/agent_call.py` prints no lines.
- [ ] Lane 9. Confirm `prompts/stage_2_perplexity_prompt.txt` is unchanged against the parent. Save `/tmp/swarm-pr-11/worker-9/lane-9.png`. Pass when `git diff <parent> -- prompts/stage_2_perplexity_prompt.txt` prints no lines.
- [ ] Lane 10. Confirm `README.md` is unchanged against the parent. Save `/tmp/swarm-pr-11/worker-10/lane-10.png`. Pass when `git diff <parent> -- README.md` prints no lines.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. Seconds for `python -m pytest -q` on trunk and on the PR head.
- [ ] Probe. Run `python -m pytest -q` on trunk, then on the head, then on trunk again. Record all three durations.
- [ ] Baseline. Record the first trunk duration before the head run.
- [ ] Rule. Fail when the head duration is more than 10 percent above the first trunk duration.

**Review gate.** None. pr-11 is not review-gated.

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] Bugbot triage done.
- [ ] Rebased onto the parent tip after the verdict, patch-id unchanged.
- [ ] The root appends this PR to the stack. The operator lands it. The owner does not merge.

## Switch signal-gated scouts to the shared client, pr-12

**Depends on.** pr-11.

**Files.**

- [ ] Edit `signal_gated_search/agent_call.py`.
- [ ] Edit `signal_gated_search/runner.py` if it imports a scout helper that moved.
- [ ] Edit `tests/test_sgs_live.py` and `tests/test_sgs_prompting.py` if import paths change.

**Build.**

- [ ] Route `execute_scout_call` through `agent_api.client`.
- [ ] Keep scout tools as `web_search` only, and keep `preset="low"` on the scout request.
- [ ] Delete the scout-only JSON parser when `agent_api.client` covers that parse.
- [ ] Leave dig prompt text and `decide_gate` in place.

**You see.**

- [ ] `python -m pytest tests/test_sgs_live.py tests/test_sgs_gate.py tests/test_sgs_prompting.py -q` ends in `passed`.

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Assert a dry scout request sends `preset` `low` and does not send `fetch_url`.
- [ ] Run `python -m pytest tests/test_sgs_live.py tests/test_sgs_runner.py tests/test_sgs_gate.py -q`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `composer-2.5-fast` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Run `python -m pytest -q` at trunk and at the head. Save `/tmp/swarm-pr-12/worker-1/lane-1.png`. Pass when both runs end in `passed`.
- [ ] Lane 2. Run the scout request test. Save `/tmp/swarm-pr-12/worker-2/lane-2.png`. Pass when the test ends in `passed`.
- [ ] Lane 3. Run `git grep -n 'def _extract_json_object' -- signal_gated_search`. Save `/tmp/swarm-pr-12/worker-3/lane-3.png`. Pass when the command prints nothing.
- [ ] Lane 4. Run `git grep -n 'def execute_agent_call' -- parallel_channel_search unified_adaptive_search signal_gated_search`. Save `/tmp/swarm-pr-12/worker-4/lane-4.png`. Pass when the command prints nothing.
- [ ] Lane 5. Run `python -m signal_gated_search --help`. Save `/tmp/swarm-pr-12/worker-5/lane-5.png`. Pass when the command exits 0.
- [ ] Lane 6. Confirm `DEFAULT_SCOUT_PRESET` is still `low`. Save `/tmp/swarm-pr-12/worker-6/lane-6.png`. Pass when the assignment is `low`.
- [ ] Lane 7. Confirm `DEFAULT_SIGNAL_THRESHOLD` is still 0.5. Save `/tmp/swarm-pr-12/worker-7/lane-7.png`. Pass when the assignment is `0.5`.
- [ ] Lane 8. Confirm `production/run.py` still maps `sgs` to `signal_gated_search.run`. Save `/tmp/swarm-pr-12/worker-8/lane-8.png`. Pass when the mapping is present.
- [ ] Lane 9. Confirm `README.md` is unchanged against the parent. Save `/tmp/swarm-pr-12/worker-9/lane-9.png`. Pass when `git diff <parent> -- README.md` prints no lines.
- [ ] Lane 10. Confirm `legacy_agent_march_2026/` is unchanged against the parent. Save `/tmp/swarm-pr-12/worker-10/lane-10.png`. Pass when `git diff <parent> -- legacy_agent_march_2026` prints no lines.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. Seconds for `python -m pytest -q` on trunk and on the PR head.
- [ ] Probe. Run `python -m pytest -q` on trunk, then on the head, then on trunk again. Record all three durations.
- [ ] Baseline. Record the first trunk duration before the head run.
- [ ] Rule. Fail when the head duration is more than 10 percent above the first trunk duration.

**Review gate.** None. pr-12 is not review-gated.

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] Bugbot triage done.
- [ ] Rebased onto the parent tip after the verdict, patch-id unchanged.
- [ ] The root appends this PR to the stack. The operator lands it. The owner does not merge.

## Replace the copied paid runner scripts with one script, pr-13

**Depends on.** pr-12.

**Files.**

- [ ] Create `evals/paid_probes.py`.
- [ ] Delete the thirteen `run_*.py` files under `outputs/stage2/test_runs/`.
- [ ] Keep every `summary.jsonl` under `outputs/stage2/test_runs/`.
- [ ] Edit `tests/test_pcs_confirm_medium_runner.py` so it imports the shared helpers from `evals/paid_probes.py`.

**Build.**

- [ ] Move the resume and 429 helpers that `tests/test_pcs_confirm_medium_runner.py` locks into `evals/paid_probes.py`.
- [ ] Keep the probe command able to target one existing run directory, one architecture, and one worker count without copying a new script.
- [ ] Do not delete or edit `summary.jsonl` files.

**You see.**

- [ ] `git ls-files 'outputs/stage2/test_runs/**/run_*.py'` prints nothing.
- [ ] `git ls-files 'outputs/stage2/test_runs/**/summary.jsonl'` still lists the scoreboards that were on the parent.

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] `tests/test_pcs_confirm_medium_runner.py` passes against `evals.paid_probes`.
- [ ] Run `python -m pytest tests/test_pcs_confirm_medium_runner.py tests/test_hillclimb_panel.py tests/test_pcs_confirm_panel.py -q`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `composer-2.5-fast` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Run `python -m pytest -q` at trunk and at the head. Save `/tmp/swarm-pr-13/worker-1/lane-1.png`. Pass when both runs end in `passed`.
- [ ] Lane 2. Run `git ls-files 'outputs/stage2/test_runs/**/*.py'`. Save `/tmp/swarm-pr-13/worker-2/lane-2.png`. Pass when the command prints nothing.
- [ ] Lane 3. Run `git ls-files 'outputs/stage2/test_runs/**/summary.jsonl'` and compare the list to the parent. Save `/tmp/swarm-pr-13/worker-3/lane-3.png`. Pass when the head list equals the parent list.
- [ ] Lane 4. Run `python -m pytest tests/test_pcs_confirm_medium_runner.py -q`. Save `/tmp/swarm-pr-13/worker-4/lane-4.png`. Pass when the run ends in `passed`.
- [ ] Lane 5. Run `python -m evals.paid_probes --help`. Save `/tmp/swarm-pr-13/worker-5/lane-5.png`. Pass when the command exits 0.
- [ ] Lane 6. Confirm `outputs/stage2/test_runs/pcs_confirm_20_medium/summary.jsonl` is still tracked. Save `/tmp/swarm-pr-13/worker-6/lane-6.png`. Pass when `git ls-files` prints that path.
- [ ] Lane 7. Confirm `outputs/stage2/test_runs/sgs_skip_50/summary.jsonl` is still tracked. Save `/tmp/swarm-pr-13/worker-7/lane-7.png`. Pass when `git ls-files` prints that path.
- [ ] Lane 8. Confirm the deleted script paths are absent. Save `/tmp/swarm-pr-13/worker-8/lane-8.png`. Pass when `git cat-file -e HEAD:outputs/stage2/test_runs/pcs_confirm_20_medium/run_twenty_medium.py` fails.
- [ ] Lane 9. Confirm `README.md` is unchanged against the parent. Save `/tmp/swarm-pr-13/worker-9/lane-9.png`. Pass when `git diff <parent> -- README.md` prints no lines.
- [ ] Lane 10. Confirm `docs/DATA.md` either still allows tracked `summary.jsonl` files or this PR updates that sentence in the same diff. Save `/tmp/swarm-pr-13/worker-10/lane-10.png`. Pass when the sentence in `docs/DATA.md` still says the scoreboards stay in git, or the diff updates that sentence and a reviewer can see it.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. Seconds for `python -m pytest -q` on trunk and on the PR head.
- [ ] Probe. Run `python -m pytest -q` on trunk, then on the head, then on trunk again. Record all three durations.
- [ ] Baseline. Record the first trunk duration before the head run.
- [ ] Rule. Fail when the head duration is more than 10 percent above the first trunk duration.

**Review gate.** The operator reviews before merge.

- [ ] Copy lane 1 screenshots into `/opt/cursor/artifacts/pr-13-review-lane-1.png`.
- [ ] Record a 30 to 60 second video of the empty `git ls-files` for `run_*.py` and the unchanged `summary.jsonl` list on a lane VM. Save it as `/opt/cursor/artifacts/pr-13-review.mp4`.
- [ ] Post the screenshots and the video in chat. Stop at stack-ready. Wait for the operator.

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] Bugbot triage done.
- [ ] Rebased onto the parent tip after the verdict, patch-id unchanged.
- [ ] The root appends this PR to the stack. The operator lands it. The owner does not merge.

## Rewrite the root README after the tree matches it, pr-14

**Depends on.** pr-13.

**Files.**

- [ ] Edit `README.md`.
- [ ] Do not edit architecture runners in this PR.

**Build.**

- [ ] Open with the research question and the command `python -m production`.
- [ ] Name `sgs` as the ship architecture from the 2026-08-16 decision.
- [ ] Put the March counts in a prior-run section that links `legacy_agent_march_2026/presentation/production_results.html`.
- [ ] Name the citation rule that an unread page stays null.
- [ ] Remove the badge that calls the March 2,062 findings the current verified count, unless the sentence names the March run.
- [ ] State the SGS planning band as about $0.16 per company, from the hill-climb 20 mean $0.171 and the skip 50 mean $0.157 in `docs/decision-log.md`.

**You see.**

- [ ] `README.md` contains `python -m production` and does not contain the sentence `Stage 3 verification remain stubs`.
- [ ] The March dashboard link still resolves to a tracked HTML file.

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Add `tests/test_readme_live_command.py` that fails if `README.md` lacks `python -m production` or still contains `Stage 3 verification remain stubs`.
- [ ] Run `python -m pytest tests/test_readme_live_command.py tests/test_march_reference_path.py -q`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `composer-2.5-fast` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Run `python -m pytest -q` at trunk and at the head. Save `/tmp/swarm-pr-14/worker-1/lane-1.png`. Pass when both runs end in `passed`.
- [ ] Lane 2. Open `README.md` and find `python -m production`. Save `/tmp/swarm-pr-14/worker-2/lane-2.png`. Pass when the string is present.
- [ ] Lane 3. Open `README.md` and search for `Stage 3 verification remain stubs`. Save `/tmp/swarm-pr-14/worker-3/lane-3.png`. Pass when the string is absent.
- [ ] Lane 4. Open `README.md` and find the link to `legacy_agent_march_2026/presentation/production_results.html`. Save `/tmp/swarm-pr-14/worker-4/lane-4.png`. Pass when the link target is that path.
- [ ] Lane 5. Confirm that HTML file is tracked. Save `/tmp/swarm-pr-14/worker-5/lane-5.png`. Pass when `git ls-files` prints that path.
- [ ] Lane 6. Open `README.md` and find `$0.16` or `0.16` next to a sentence that names signal-gated search. Save `/tmp/swarm-pr-14/worker-6/lane-6.png`. Pass when the cost sentence names signal-gated search and the March section is separate.
- [ ] Lane 7. Confirm the file does not tell the reader to run `python -m evals run-verification` as the way to verify citations. Save `/tmp/swarm-pr-14/worker-7/lane-7.png`. Pass when the README points citation checks at `python -m production verify`.
- [ ] Lane 8. Run `python -m production --help` and compare the command names to the README. Save `/tmp/swarm-pr-14/worker-8/lane-8.png`. Pass when every command name in the help text that the README mentions exists in the help text.
- [ ] Lane 9. Run `python -m evals run-verification` and confirm the README does not call that command a working verifier. Save `/tmp/swarm-pr-14/worker-9/lane-9.png`. Pass when the process exits 2.
- [ ] Lane 10. Confirm `AGENTS.md` and `README.md` name the same batch command. Save `/tmp/swarm-pr-14/worker-10/lane-10.png`. Pass when both files contain `python -m production`.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. Seconds for `python -m pytest -q` on trunk and on the PR head.
- [ ] Probe. Run `python -m pytest -q` on trunk, then on the head, then on trunk again. Record all three durations.
- [ ] Baseline. Record the first trunk duration before the head run.
- [ ] Rule. Fail when the head duration is more than 10 percent above the first trunk duration.

**Review gate.** The operator reviews before merge.

- [ ] Copy lane 1 screenshots into `/opt/cursor/artifacts/pr-14-review-lane-1.png`.
- [ ] Record a 30 to 60 second video of the rendered `README.md` showing the production command and the March section as prior work on a lane VM. Save it as `/opt/cursor/artifacts/pr-14-review.mp4`.
- [ ] Post the screenshots and the video in chat. Stop at stack-ready. Wait for the operator.

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] Bugbot triage done.
- [ ] Rebased onto the parent tip after the verdict, patch-id unchanged.
- [ ] The root appends this PR to the stack. The operator lands it. The owner does not merge.

## Close the program

- [ ] Every box above is checked with its evidence.
- [ ] Reply to the operator with the stack root link, the stack tip link, a one-line verdict per PR, and anything parked.

## Appendix A. Prototype evidence

No prototype branch was cut. The open questions were settled by search in this checkout, or they are operator preferences with a default.

A search of `*.py` found no `import yaml` and no `yaml.safe_load`. `CONFIGS_DIR` is only assigned in `evals/paths.py`. That is why pr-3 deletes the YAML files.

`unified_adaptive_search/agent_call.py` sets `DEFAULT_WEB_SEARCH_DEPTH` to `low`. `evals/configs/unified_adaptive_search.yaml` says `medium`. No loader reconciles them. pr-3 does not change the Python constant.

A search found `search_domain_filter`, `instruction_hint`, `DEFAULT_CHANNEL_PRIOR`, `DEFAULT_DIG_PRESET`, `DEFAULT_RESCUE_DIG_PRESET`, and `from_preset_defaults` only at their definitions. pr-6 searches again before it deletes them. If that search finds a reader, the owner keeps the name and says so in the PR body.

The license file is unproven as a choice. The default is no `LICENSE` file in this program. The operator can name a license after pr-1, and that file is a separate one-file PR, not a silent add.

Pytest duration on trunk was not measured in this planning turn. Each perf box records it at execution.

## Appendix B. Alternatives rejected

One pull request for the whole cleanup was rejected. A reviewer cannot separate a YAML deletion from a client extraction or from the README.

Rewriting `README.md` in pr-1 was rejected. The decision log says the README rewrite comes later, and the tree still contradicts that file.

Deleting `legacy_agent_march_2026/` was rejected. The 2026-08-16 and 2026-08-20 decisions keep the snapshot runnable and unimported. `tests/test_march_reference_path.py` locks that boundary. `src/stage_1/` stays duplicated inside the snapshot for that reason.

Keeping the YAML as documentation was rejected. The UAS file states a search depth the production path does not use.

Merging the three `run()` functions into one architecture was rejected. Parallel Channel Search, signal-gated search, and Unified Adaptive Search are the comparison. The shared piece is the Perplexity call.

Changing `DEFAULT_WEB_SEARCH_DEPTH` from `low` to `medium` was rejected. That would change paid behavior to match an unused file.

A git history rewrite of the old Crunchbase CSV was rejected for this program. `docs/DATA.md` says to ask Jan Bena before `git filter-repo`. HEAD already untracks those dumps.

Leaving `run-benchmarks` and `run-verification` as stub instance writers was rejected. `citation_verification/` and `python -m production verify` already exist, and the 2026-08-16 decision skipped the bake-off.

## Appendix C. Risks

`control-cli` is not installed here. Live lanes run shell commands and save a terminal screenshot. A lane that needs a browser has no control skill. None of these PRs change a web UI.

`git show origin/main:pstack/skills/...` will fail in this repo. The pstack skills are not vendored on `main`. They live in the Cursor plugin cache that wrote this plan. Owners read those plugin copies when the `git show` path is missing, and they record that fallback in the decision trail.

pr-3 is review-gated because deleting the YAML is a preference the operator can reverse. If the operator rejects pr-3, pr-11 must edit `evals/tune/_rerun_search_high.py`, `evals/tune/_retry_search_high_failures.py`, and `evals/tune/_max_none3_smoke.py` instead of assuming they are gone.

pr-7 and pr-10 through pr-12 are behavior-preserving only if the dry request kwargs match the parent. The unit boxes name those literals. A mismatch is a failed lane, not a follow-up.

pr-13 deletes scripts that a local shell alias might call. The `summary.jsonl` files stay. The review video shows the empty script list and the surviving scoreboards.

Paid commands are out of bounds for every lane. `--live` and `--all` are not part of verification.

## Appendix D. Links and reading list

Read `docs/decision-log.md` from the 2026-08-16 ship entry through the 2026-08-20 data entry before pr-3, pr-4, or pr-14.

Read `production/__main__.py`, `production/run.py`, and `evals/cli.py` before pr-4.

pr-9 and pr-10 run the architect skill before coding, because the client crosses package boundaries. The refactoring model line is `grok-4.7-high`.

pr-14 follows the technical-writing skill and the unslop skill. The README is a how-to plus a short explanation of the prior March run. It is not a second decision log.

Each owner keeps a decision trail per the show-me-your-work skill. The trail stays uncommitted unless the operator asks to commit it.

