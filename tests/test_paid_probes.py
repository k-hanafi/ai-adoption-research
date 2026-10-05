from __future__ import annotations

from pathlib import Path

import pytest

from evals.paid_probes import (
    PROBES,
    _write_result,
    describe,
    dig_effort_override,
    is_complete_success,
    is_rate_limit,
    is_retryable,
    is_timeout,
    main,
    retry_kind,
)
from evals.paths import PROJECT_ROOT

RUNS = PROJECT_ROOT / "outputs" / "stage2" / "test_runs"


def test_rate_limit_ignores_cost_and_url_substrings() -> None:
    success = {
        "error": None,
        "cost_usd": 0.1429,
        "findings": [
            {
                "source_url": (
                    "https://www.linkedin.com/jobs/view/"
                    "founding-ml-engineer-4299954127"
                )
            }
        ],
    }
    assert is_rate_limit(success.get("error")) is False
    assert is_retryable(success.get("error")) is False
    assert is_complete_success(success) is True


def test_rate_limit_reads_real_error_strings() -> None:
    err = (
        "owned: RateLimitError: Error code: 429 - "
        "{'error': {'message': 'Request rate limit exceeded, please try again later.'}}"
    )
    assert is_rate_limit(err) is True
    assert is_retryable(err) is True
    assert retry_kind(err) == "429"


def test_timeout_is_retryable_without_matching_429() -> None:
    err = "jobs: APITimeoutError: Request timed out."
    assert is_rate_limit(err) is False
    assert is_timeout(err) is True
    assert is_retryable(err) is True
    assert retry_kind(err) == "timeout"


def test_confirm_medium_defaults_to_five_workers() -> None:
    assert PROBES["pcs_confirm_20_medium"].workers == 5


def test_resume_skips_only_error_free_json() -> None:
    assert is_complete_success({"error": None, "findings_count": 5}) is True
    assert is_complete_success({"error": None}) is True
    assert is_complete_success(
        {"error": "APITimeoutError: Request timed out.", "cost_usd": 0}
    ) is False
    assert is_complete_success(None) is False
    assert is_complete_success({}) is False


def test_smoke_timeouts_match_the_scripts() -> None:
    assert PROBES["sgs_smoke_5co"].timeout == 300.0
    assert PROBES["sgs_smoke_covertree_tern_v2"].timeout == 300.0
    assert PROBES["sgs_smoke_5co_low_scouts"].timeout == 600.0
    assert PROBES["pcs_hillclimb_20"].timeout == 300.0


def test_old_sgs_leashes_refuse_live(monkeypatch, capsys: pytest.CaptureFixture[str]) -> None:
    blocked = {
        "sgs_hillclimb_20_high",
        "sgs_hillclimb_20_medium",
        "sgs_smoke_5co",
        "sgs_smoke_5co_low_scouts",
        "sgs_smoke_covertree_tern_v2",
    }
    assert {name for name, probe in PROBES.items() if probe.live_block} == blocked

    def _boom(*_args, **_kwargs):
        raise AssertionError("execute must not run")

    monkeypatch.setattr("evals.paid_probes.execute", _boom)
    assert main(["sgs_hillclimb_20_high", "--live"]) == 2
    err = capsys.readouterr().err
    assert "fast scouts" in err
    assert "50 steps" in err


def test_keep_success_does_not_overwrite(tmp_path: Path) -> None:
    from threading import Lock

    result_path = tmp_path / "1.json"
    result_path.write_text('{"error": null, "findings_count": 3}\n', encoding="utf-8")
    summary = tmp_path / "summary.jsonl"
    summary.write_text('{"rcid": 1}\n', encoding="utf-8")
    _write_result(
        result_path,
        {"error": "APITimeoutError: Request timed out."},
        {"rcid": 1, "name": "Jam", "error": "APITimeoutError: Request timed out."},
        summary,
        Lock(),
    )
    assert json_text(result_path) == '{"error": null, "findings_count": 3}\n'
    assert summary.read_text(encoding="utf-8") == '{"rcid": 1}\n'
    backups = list(tmp_path.glob("1.*.failed.json"))
    assert len(backups) == 1


def json_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


PROBE_NAMES = (
    "pcs_confirm_20_high",
    "pcs_confirm_20_medium",
    "pcs_hillclimb_20",
    "pcs_hillclimb_20_high",
    "pcs_hillclimb_20_medium_v2",
    "sgs_hillclimb_20_high",
    "sgs_hillclimb_20_matched",
    "sgs_hillclimb_20_medium",
    "sgs_skip_50",
    "sgs_smoke_5co",
    "sgs_smoke_5co_low_scouts",
    "sgs_smoke_covertree_tern_v2",
    "uas_hillclimb_20_xhigh",
)


def test_catalog_names_the_historical_probes() -> None:
    assert sorted(PROBES) == sorted(PROBE_NAMES)
    assert list(RUNS.glob("*/run_*.py")) == []
    on_disk = {path.parent.name for path in RUNS.glob("*/summary.jsonl")}
    assert on_disk <= set(PROBES)


def test_main_refuses_without_live(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["pcs_confirm_20_medium"]) == 2
    err = capsys.readouterr().err
    assert "pcs_confirm_20_medium" in err
    assert "--live" in err
    assert describe(PROBES["pcs_confirm_20_medium"]) in err


def test_main_lists_probes_when_unnamed(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 2
    err = capsys.readouterr().err
    assert "pcs_confirm_20_medium" in err
    assert "sgs_skip_50" in err


def test_dig_effort_override_restores_package_high() -> None:
    import signal_gated_search.channels as channels
    import signal_gated_search.gate as gate
    import signal_gated_search.runner as runner

    before = (
        channels.DIG_EFFORT_BY_COUNT,
        gate.DIG_EFFORT_BY_COUNT,
        runner.DIG_EFFORT_BY_COUNT,
    )
    with dig_effort_override("medium"):
        assert gate.DIG_EFFORT_BY_COUNT[1] == "medium"
        assert runner.DIG_EFFORT_BY_COUNT[3] == "medium"
    assert channels.DIG_EFFORT_BY_COUNT == before[0]
    assert gate.DIG_EFFORT_BY_COUNT is before[1]
    assert runner.DIG_EFFORT_BY_COUNT is before[2]
    assert gate.DIG_EFFORT_BY_COUNT[1] == "high"


def test_execute_dry_does_not_append_over_success(tmp_path: Path, monkeypatch) -> None:
    from evals.paid_probes import execute

    probe = PROBES["sgs_smoke_covertree_tern_v2"]
    called = {"n": 0}

    def _boom(*_args, **_kwargs):
        called["n"] += 1
        raise AssertionError("architecture_run should not see a finished company")

    monkeypatch.setattr("evals.paid_probes.architecture_run", _boom)
    for row in probe.companies:
        path = tmp_path / f"{row['rcid']}.json"
        path.write_text('{"error": null, "cost_usd": 0.1}\n', encoding="utf-8")
    summary = tmp_path / "summary.jsonl"
    summary.write_text('{"rcid": 1}\n', encoding="utf-8")
    assert execute(probe, out_dir=tmp_path) == 0
    assert called["n"] == 0
    assert summary.read_text(encoding="utf-8") == '{"rcid": 1}\n'
