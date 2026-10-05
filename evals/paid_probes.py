from __future__ import annotations

import argparse
import json
import shutil
import sys
import traceback
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any, Iterator, Optional

from evals.paths import (
    HILLCLIMB_PANEL_PATH,
    PCS_CONFIRM_PANEL_PATH,
    PROJECT_ROOT,
    SGS_SKIP_PANEL_PATH,
)

TIMEOUT_S = 600.0

_PANELS = {
    "hillclimb": HILLCLIMB_PANEL_PATH,
    "confirm": PCS_CONFIRM_PANEL_PATH,
    "skip": SGS_SKIP_PANEL_PATH,
}

_ARCH_LABEL = {
    "pcs": "parallel-channel-search",
    "sgs": "signal-gated-search",
    "uas": "unified-adaptive-search",
}

_SMOKE_5: tuple[dict[str, Any], ...] = (
    {
        "rcid": 97943259,
        "name": "Easy Fill AI",
        "homepage_url": "https://easyfill.ai",
        "short_description": "AI Based SaaS Data Collection and Analysis Tool",
        "march_stratum": "none",
        "march_findings": 0,
    },
    {
        "rcid": 1314132,
        "name": "CoverTree",
        "homepage_url": "https://covertree.com",
        "short_description": (
            "CoverTree is an InsurTech company that specializes in "
            "manufactured home insurance solutions."
        ),
        "march_stratum": "low",
        "march_findings": 1,
    },
    {
        "rcid": 103497,
        "name": "Statsig",
        "homepage_url": "https://www.statsig.com",
        "short_description": (
            "Statsig provides tools for A/B testing, feature management, "
            "and product analytics to help teams optimize product development."
        ),
        "march_stratum": "medium",
        "march_findings": 2,
    },
    {
        "rcid": 26492430,
        "name": "Tern Travel",
        "homepage_url": "https://www.tern.travel/",
        "short_description": (
            "Tern Travel builds an integrated platform that connects the "
            "travel advisor to travelers and suppliers."
        ),
        "march_stratum": "high",
        "march_findings": 6,
    },
    {
        "rcid": 610194,
        "name": "Jam",
        "homepage_url": "https://jam.dev/",
        "short_description": "1-click bug reports developers love. Try for free at jam.dev",
        "march_stratum": "high",
        "march_findings": 8,
        "tuning_holdout": True,
    },
)


def _smoke(*rcids: int) -> tuple[dict[str, Any], ...]:
    by_id = {int(row["rcid"]): row for row in _SMOKE_5}
    return tuple(by_id[rcid] for rcid in rcids)


@dataclass(frozen=True)
class Probe:
    name: str
    architecture: str
    workers: int
    panel: Optional[str] = None
    expected: Optional[int] = None
    companies: tuple[dict[str, Any], ...] = ()
    timeout: float = TIMEOUT_S
    reasoning_effort: Optional[str] = None
    scout_preset: Optional[str] = None
    dig_effort: Optional[str] = None
    check_sgs_defaults: bool = False

    @property
    def out_dir(self) -> Path:
        return PROJECT_ROOT / "outputs" / "stage2" / "test_runs" / self.name


def _probe(**kwargs: Any) -> Probe:
    return Probe(**kwargs)


PROBES: dict[str, Probe] = {
    probe.name: probe
    for probe in (
        _probe(
            name="pcs_hillclimb_20",
            architecture="pcs",
            workers=1,
            panel="hillclimb",
            expected=20,
            timeout=300.0,
            reasoning_effort="medium",
        ),
        _probe(
            name="pcs_hillclimb_20_medium_v2",
            architecture="pcs",
            workers=20,
            panel="hillclimb",
            expected=20,
            reasoning_effort="medium",
        ),
        _probe(
            name="pcs_hillclimb_20_high",
            architecture="pcs",
            workers=20,
            panel="hillclimb",
            expected=20,
            reasoning_effort="high",
        ),
        _probe(
            name="pcs_confirm_20_medium",
            architecture="pcs",
            workers=5,
            panel="confirm",
            expected=20,
            reasoning_effort="medium",
        ),
        _probe(
            name="pcs_confirm_20_high",
            architecture="pcs",
            workers=5,
            panel="confirm",
            expected=20,
            reasoning_effort="high",
        ),
        _probe(
            name="uas_hillclimb_20_xhigh",
            architecture="uas",
            workers=20,
            panel="hillclimb",
            expected=20,
            reasoning_effort="xhigh",
        ),
        _probe(
            name="sgs_smoke_5co",
            architecture="sgs",
            workers=1,
            companies=_SMOKE_5,
            expected=5,
        ),
        _probe(
            name="sgs_smoke_5co_low_scouts",
            architecture="sgs",
            workers=1,
            companies=_SMOKE_5,
            expected=5,
            scout_preset="low",
        ),
        _probe(
            name="sgs_smoke_covertree_tern_v2",
            architecture="sgs",
            workers=1,
            companies=_smoke(1314132, 26492430),
            expected=2,
        ),
        _probe(
            name="sgs_hillclimb_20_high",
            architecture="sgs",
            workers=4,
            panel="hillclimb",
            expected=20,
        ),
        _probe(
            name="sgs_hillclimb_20_medium",
            architecture="sgs",
            workers=4,
            panel="hillclimb",
            expected=20,
            dig_effort="medium",
        ),
        _probe(
            name="sgs_hillclimb_20_matched",
            architecture="sgs",
            workers=4,
            panel="hillclimb",
            expected=20,
            scout_preset="low",
            check_sgs_defaults=True,
        ),
        _probe(
            name="sgs_skip_50",
            architecture="sgs",
            workers=4,
            panel="skip",
            expected=50,
            scout_preset="low",
            check_sgs_defaults=True,
        ),
    )
}


def is_rate_limit(error: Optional[str]) -> bool:
    text = (error or "").lower()
    return "429" in text or "rate limit" in text or "ratelimit" in text


def is_timeout(error: Optional[str]) -> bool:
    return "timeout" in (error or "").lower()


def is_retryable(error: Optional[str]) -> bool:
    return is_rate_limit(error) or is_timeout(error)


def retry_kind(error: Optional[str]) -> str:
    if is_rate_limit(error):
        return "429"
    if is_timeout(error):
        return "timeout"
    return "failed"


def is_complete_success(payload: Optional[dict]) -> bool:
    return bool(payload) and not payload.get("error")


def load_companies(probe: Probe) -> list[dict[str, Any]]:
    if probe.companies:
        companies = [dict(row) for row in probe.companies]
    else:
        if probe.panel not in _PANELS:
            raise RuntimeError(f"{probe.name} has no panel")
        panel = json.loads(_PANELS[probe.panel].read_text(encoding="utf-8"))
        companies = list(panel.get("companies") or [])
    if probe.expected is not None and len(companies) != probe.expected:
        raise RuntimeError(
            f"{probe.name} expected {probe.expected} companies, got {len(companies)}"
        )
    return companies


def describe(probe: Probe) -> str:
    return (
        f"{probe.name} architecture={probe.architecture} workers={probe.workers} "
        f"timeout={probe.timeout} effort={probe.reasoning_effort} "
        f"scout_preset={probe.scout_preset} dig_effort={probe.dig_effort} "
        f"out={probe.out_dir}"
    )


@contextmanager
def dig_effort_override(effort: Optional[str]) -> Iterator[None]:
    if not effort:
        yield
        return
    import signal_gated_search.channels as channels
    import signal_gated_search.gate as gate
    import signal_gated_search.runner as runner

    ladder = {1: effort, 2: effort, 3: effort}
    saved = (
        channels.DIG_EFFORT_BY_COUNT,
        gate.DIG_EFFORT_BY_COUNT,
        runner.DIG_EFFORT_BY_COUNT,
    )
    channels.DIG_EFFORT_BY_COUNT = ladder
    gate.DIG_EFFORT_BY_COUNT = ladder
    runner.DIG_EFFORT_BY_COUNT = ladder
    try:
        yield
    finally:
        (
            channels.DIG_EFFORT_BY_COUNT,
            gate.DIG_EFFORT_BY_COUNT,
            runner.DIG_EFFORT_BY_COUNT,
        ) = saved


def _check_sgs_defaults(probe: Probe) -> None:
    if not probe.check_sgs_defaults:
        return
    from signal_gated_search.channels import (
        DEFAULT_DIG_EFFORT,
        DEFAULT_DIG_MAX_STEPS,
        DEFAULT_DIG_WEB_SEARCH_DEPTH,
        DEFAULT_SCOUT_PRESET,
    )

    if DEFAULT_SCOUT_PRESET != "low":
        raise RuntimeError(
            f"expected package scout_preset=low, got {DEFAULT_SCOUT_PRESET!r}"
        )
    if DEFAULT_DIG_EFFORT != "high":
        raise RuntimeError(f"expected package dig effort=high, got {DEFAULT_DIG_EFFORT!r}")
    if DEFAULT_DIG_MAX_STEPS != 50 or DEFAULT_DIG_WEB_SEARCH_DEPTH != "medium":
        raise RuntimeError(
            "expected digs 50/medium, got "
            f"{DEFAULT_DIG_MAX_STEPS}/{DEFAULT_DIG_WEB_SEARCH_DEPTH}"
        )


def _company_input(meta: dict[str, Any]) -> dict[str, Any]:
    return {
        "rcid": meta["rcid"],
        "name": meta["name"],
        "homepage_url": meta.get("homepage_url"),
        "short_description": meta.get("short_description"),
    }


def architecture_run(probe: Probe, meta: dict[str, Any]) -> dict[str, Any]:
    company = _company_input(meta)
    if probe.architecture == "pcs":
        from parallel_channel_search.runner import run

        kwargs: dict[str, Any] = {"dry_run": False, "timeout": probe.timeout}
        if probe.reasoning_effort:
            kwargs["reasoning_effort"] = probe.reasoning_effort
        return run(company, **kwargs).to_dict()
    if probe.architecture == "uas":
        from unified_adaptive_search.runner import run

        kwargs = {"dry_run": False, "timeout": probe.timeout}
        if probe.reasoning_effort:
            kwargs["reasoning_effort"] = probe.reasoning_effort
        return run(company, **kwargs).to_dict()
    if probe.architecture == "sgs":
        from signal_gated_search.runner import run

        kwargs = {"dry_run": False, "timeout": probe.timeout}
        if probe.scout_preset:
            kwargs["scout_preset"] = probe.scout_preset
        return run(company, **kwargs).to_dict()
    raise RuntimeError(f"unknown architecture {probe.architecture!r}")


def _compact(
    result: dict[str, Any],
    meta: dict[str, Any],
    probe: Probe,
    error: Optional[str] = None,
) -> dict[str, Any]:
    traces = result.get("traces") or {}
    channel_results = traces.get("channel_results") or {}
    gate = traces.get("gate") or {}
    scout_results = traces.get("scout_results") or {}
    ledger = result.get("cost_ledger") or {}
    findings = result.get("findings") or []
    row: dict[str, Any] = {
        "rcid": meta["rcid"],
        "name": meta["name"],
        "probe": probe.name,
        "architecture": _ARCH_LABEL[probe.architecture],
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": result.get("dry_run"),
        "duration_seconds": result.get("duration_seconds"),
        "cost_usd": result.get("cost_usd"),
        "findings_count": result.get("findings_count"),
        "genai_adoption_found": result.get("genai_adoption_found"),
        "model_used": result.get("model_used"),
        "error": error or result.get("error"),
        "no_finding_reason": result.get("no_finding_reason"),
    }
    if probe.reasoning_effort:
        row["reasoning_effort"] = probe.reasoning_effort
    if probe.scout_preset:
        row["scout_preset"] = probe.scout_preset
    if probe.dig_effort:
        row["dig_effort"] = probe.dig_effort
    if channel_results:
        row["channel_finding_counts"] = {
            channel: (channel_results.get(channel) or {}).get("finding_count")
            for channel in ("jobs", "owned", "third_party")
        }
    if gate or scout_results:
        row["gate"] = {
            "dig_count": gate.get("dig_count"),
            "dig_channels": gate.get("dig_channels"),
            "reasoning_effort": gate.get("reasoning_effort"),
        }
        row["scout_bins"] = {
            channel: (scout_results.get(channel) or {}).get("evidence_bin")
            for channel in ("jobs", "owned", "third_party")
        }
    row["ledger"] = [
        {
            "name": component.get("name"),
            "preset": component.get("preset"),
            "cost_usd": component.get("cost_usd"),
            "ran": component.get("ran"),
            "skipped_reason": component.get("skipped_reason"),
        }
        for component in ledger.get("components") or []
    ]
    return row


def _load_payload(path: Path) -> Optional[dict]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def _backup_path(result_path: Path, kind: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = result_path.with_name(f"{result_path.stem}.{stamp}.{kind}.json")
    if backup.exists():
        backup = result_path.with_name(f"{result_path.stem}.{stamp}.{kind}b.json")
    return backup


def _failure_payload(meta: dict[str, Any], probe: Probe, exc: Exception) -> dict[str, Any]:
    return {
        "rcid": int(meta["rcid"]),
        "company_name": meta["name"],
        "architecture": _ARCH_LABEL[probe.architecture],
        "error": f"{type(exc).__name__}: {exc}",
        "traceback": traceback.format_exc(),
        "dry_run": False,
    }


def _write_result(
    result_path: Path,
    payload: dict[str, Any],
    compact: dict[str, Any],
    summary_path: Path,
    lock: Lock,
) -> None:
    existing = _load_payload(result_path) if result_path.exists() else None
    if is_complete_success(existing) and compact.get("error"):
        backup = _backup_path(result_path, "failed")
        backup.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(
            f"KEEP_SUCCESS {compact.get('rcid')} {compact.get('name')}: "
            f"left {result_path.name} in place, wrote failure to {backup.name}",
            flush=True,
        )
        return
    result_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    with lock:
        with summary_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(compact) + "\n")


def execute(
    probe: Probe,
    *,
    only: Optional[set[int]] = None,
    out_dir: Optional[Path] = None,
) -> int:
    from concurrent.futures import ThreadPoolExecutor, as_completed

    _check_sgs_defaults(probe)
    companies = load_companies(probe)
    if only:
        companies = [row for row in companies if int(row["rcid"]) in only]
        missing = only - {int(row["rcid"]) for row in companies}
        if missing:
            raise SystemExit(f"rcids not in {probe.name}: {sorted(missing)}")
    by_rcid = {int(row["rcid"]): row for row in companies}
    folder = out_dir or probe.out_dir
    folder.mkdir(parents=True, exist_ok=True)
    summary_path = folder / "summary.jsonl"
    write_lock = Lock()
    todo: list[dict[str, Any]] = []
    skipped = 0
    for meta in companies:
        rcid = int(meta["rcid"])
        result_path = folder / f"{rcid}.json"
        if result_path.exists():
            existing = _load_payload(result_path)
            if is_complete_success(existing):
                skipped += 1
                print(f"SKIP {rcid} {meta['name']}: {result_path.name} already complete", flush=True)
                continue
            kind = retry_kind((existing or {}).get("error"))
            backup = _backup_path(result_path, kind)
            shutil.move(str(result_path), str(backup))
            print(
                f"REQUEUE {rcid} {meta['name']}: failed {result_path.name} "
                f"backed up to {backup.name}",
                flush=True,
            )
        todo.append(meta)

    failed = 0
    ran = 0
    retry: list[dict[str, Any]] = []

    def _handle(meta: dict[str, Any], payload: dict[str, Any], compact: dict[str, Any], *, sequential: bool) -> None:
        nonlocal failed, ran
        rcid = int(meta["rcid"])
        result_path = folder / f"{rcid}.json"
        err = compact.get("error") or payload.get("error")
        if is_retryable(err) and not sequential:
            kind = retry_kind(err)
            backup = _backup_path(result_path, kind)
            backup.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            retry.append(meta)
            print(
                f"{kind.upper()} {rcid} {meta['name']}: backed up {backup.name}; "
                "will retry sequentially",
                flush=True,
            )
            return
        if compact.get("error"):
            failed += 1
        _write_result(result_path, payload, compact, summary_path, write_lock)
        ran += 1

    def _one(meta: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        payload = architecture_run(probe, meta)
        return payload, _compact(payload, meta, probe)

    with dig_effort_override(probe.dig_effort):
        if todo:
            with ThreadPoolExecutor(max_workers=min(probe.workers, len(todo))) as pool:
                futures = {pool.submit(_one, meta): meta for meta in todo}
                for future in as_completed(futures):
                    meta = futures[future]
                    try:
                        payload, compact = future.result()
                    except Exception as exc:
                        payload = _failure_payload(meta, probe, exc)
                        compact = _compact(payload, meta, probe, error=payload["error"])
                    _handle(meta, payload, compact, sequential=False)
        for meta in retry:
            rcid = int(meta["rcid"])
            print(f"RETRY {rcid} {meta['name']} sequential after retryable error", flush=True)
            try:
                payload, compact = _one(by_rcid[rcid])
            except Exception as exc:
                payload = _failure_payload(meta, probe, exc)
                compact = _compact(payload, meta, probe, error=payload["error"])
            _handle(by_rcid[rcid], payload, compact, sequential=True)

    print(
        f"PANEL_DONE probe={probe.name} live=True workers={probe.workers} "
        f"ran={ran} skipped={skipped} failed={failed} retried={len(retry)}",
        flush=True,
    )
    return 1 if failed else 0


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Re-run one historical Stage 2 paid probe. Refuses unless --live is set."
    )
    parser.add_argument("probe", nargs="?", choices=sorted(PROBES))
    parser.add_argument(
        "--live",
        action="store_true",
        help="Call the Agent API. Without this flag the command exits 2.",
    )
    parser.add_argument("--only", type=int, nargs="+", default=None)
    args = parser.parse_args(argv)
    if not args.probe:
        print("error: name a probe. Choose: " + ", ".join(sorted(PROBES)), file=sys.stderr)
        return 2
    probe = PROBES[args.probe]
    if not args.live:
        print(describe(probe), file=sys.stderr)
        print("error: pass --live to call the Agent API. This command does not spend money otherwise.", file=sys.stderr)
        return 2
    return execute(probe, only=set(args.only) if args.only else None)


if __name__ == "__main__":
    sys.exit(main())
