"""Citation verification. Fetch the page, then judge the citation.

Production package. Evals may import it. The implementation does not live under evals/.
"""

from citation_verification.runner import verify_finding, verify_findings
from citation_verification.types import VerdictResult, VerifyResult

__all__ = [
    "VerdictResult",
    "VerifyResult",
    "verify_finding",
    "verify_findings",
]
