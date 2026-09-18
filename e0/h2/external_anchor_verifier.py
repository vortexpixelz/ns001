"""H2A1 local external-anchor identity checks; never a substantive gate decision.

Observations come from Git object bytes and fixed retained file paths, not from
submitted evidence declarations. Identity verification is not authentication of
historical custody, scientific validity, or independent reviewer approval.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from e0.h2.evidence_contract import (
    EXPECTED_ANCHOR_DECLARATIONS, GATE_REQUIREMENTS,
    H1_CHECKPOINT_COMMIT, SCIENTIFIC_BASE_COMMIT,
)

PREREGISTRATION = Path("preregistrations/e0/NS-001_E0_STRIDE_REFINEMENT_PREREG_FROZEN_2026-09-02.md")
BUNDLE = Path("audit/2026-09-03/NS001_H1_AUDIT_BUNDLE_20260903.zip")


def _git(repo: Path, *args: str) -> bytes:
    # No inherited environment, credential helpers, replacement objects, lazy
    # network object retrieval, global config, or prompts. Only local reads.
    return subprocess.run(
        ["/usr/bin/git", "--no-replace-objects", "-C", str(repo), *args],
        env={"PATH": "/usr/bin:/bin", "GIT_CONFIG_NOSYSTEM": "1",
             "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_TERMINAL_PROMPT": "0",
             "GIT_NO_LAZY_FETCH": "1"},
        check=True, capture_output=True, timeout=15,
    ).stdout


def _read_regular(path: Path) -> bytes:
    if path.is_symlink() or path.resolve() != path.absolute():
        raise ValueError("symlink evidence is not independently anchored")
    if not path.is_file():
        raise ValueError("retained regular file unavailable")
    return path.read_bytes()


def verify_external_anchors(repo: Path) -> dict:
    """Read fixed local sources. Missing/ambiguous evidence fails closed.

    The retained bundle lives outside the checkout, under its NS-001 parent.
    No caller-supplied observed digests or evidence declarations are accepted.
    The returned JSON is a diagnostic receipt, never an authorization token.
    """
    repo = Path(repo).absolute()
    observations = []
    for name, expected in EXPECTED_ANCHOR_DECLARATIONS.items():
        row = {"anchor": name, "expected": expected, "status": "BLOCKED"}
        try:
            if name.endswith("_commit"):
                row["source"] = f"{repo} Git commit object {expected}"
                raw = _git(repo, "cat-file", "commit", expected)
                observed = hashlib.sha1(
                    b"commit " + str(len(raw)).encode("ascii") + b"\0" + raw
                ).hexdigest()
                row.update(observed=observed, byte_count=len(raw),
                           raw_sha256=hashlib.sha256(raw).hexdigest())
                if observed != expected:
                    row.update(status="NOT VERIFIED", reason="raw commit identity mismatch")
                else:
                    # Pin ancestry to the observed HEAD, not a moving ref.
                    head = _git(repo, "rev-parse", "--verify", "HEAD").decode().strip()
                    row["observed_head"] = head
                    _git(repo, "merge-base", "--is-ancestor", expected, head)
                    _git(repo, "merge-base", "--is-ancestor",
                         SCIENTIFIC_BASE_COMMIT, H1_CHECKPOINT_COMMIT)
                    row.update(status="VERIFIED", reason="raw identity and ancestry match")
            else:
                path = repo / PREREGISTRATION if name.startswith("frozen_") else repo.parent / BUNDLE
                row["source"] = str(path)
                raw = _read_regular(path)
                observed = hashlib.sha256(raw).hexdigest()
                row.update(observed=observed, byte_count=len(raw))
                if observed != expected:
                    row.update(status="NOT VERIFIED", reason="retained byte digest mismatch")
                elif name.startswith("frozen_"):
                    # Compare working bytes with both immutable historical trees;
                    # a sidecar or copied expected digest is never evidence.
                    for commit in (SCIENTIFIC_BASE_COMMIT, H1_CHECKPOINT_COMMIT):
                        if _git(repo, "show", f"{commit}:{PREREGISTRATION.as_posix()}") != raw:
                            raise ValueError("historical preregistration bytes differ")
                    row.update(status="VERIFIED", reason="file and both historical blobs match")
                else:
                    row.update(status="VERIFIED", reason="independently read retained archive digest matches")
        except subprocess.CalledProcessError as exc:
            row.update(status="BLOCKED", reason=f"local Git evidence/ancestry unavailable (exit {exc.returncode})")
        except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
            row.update(status="BLOCKED", reason=f"{type(exc).__name__}: {exc}")
        observations.append(row)
    statuses = {row["status"] for row in observations}
    verdict = "VERIFIED" if statuses == {"VERIFIED"} else (
        "NOT VERIFIED" if "NOT VERIFIED" in statuses else "BLOCKED")
    return {"phase": "H2A1_EXTERNAL_ANCHORS_ONLY", "anchors": observations,
            "h2a1_verdict": verdict, "overall_status": "HOLD",
            "unresolved_h2_gates": [gate.gate_id for gate in GATE_REQUIREMENTS],
            "substantive_gate_resolved": False, "e0_authorized": False}


if __name__ == "__main__":
    result = verify_external_anchors(Path(__file__).resolve().parents[2])
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["h2a1_verdict"] == "VERIFIED" else 1)
