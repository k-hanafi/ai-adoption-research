"""Standalone eval harness for the three Stage 2 architecture packages.

CLI:
  python -m evals run-tuning <architecture> --stage screen
  python -m evals cost-preview <architecture> [--matrix screen]
  python -m evals open-dashboard

`run-benchmarks` and `run-verification` exit 2. The bake-off was skipped.
Citation checks run through `python -m production verify` and
`python -m citation_verification`.
"""

from evals.runner import run_panel

__all__ = ["run_panel"]
