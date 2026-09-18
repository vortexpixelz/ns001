"""Offline negative-path tests; synthetic bytes never establish real anchors."""
import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from e0.h2 import external_anchor_verifier as verifier


class ExternalAnchorTests(unittest.TestCase):
    def run_case(self, git=None, file=None):
        with patch.object(verifier, "_git", side_effect=git), patch.object(
            verifier, "_read_regular", side_effect=file
        ):
            return verifier.verify_external_anchors(Path("/synthetic/repo"))

    def test_missing_evidence_blocks_and_preserves_hold(self):
        result = self.run_case(OSError("missing object"), FileNotFoundError("missing file"))
        self.assertEqual(result["h2a1_verdict"], "BLOCKED")
        self.assertTrue(all(row["status"] == "BLOCKED" for row in result["anchors"]))
        self.assertEqual(len(result["unresolved_h2_gates"]), 8)
        self.assertEqual(result["overall_status"], "HOLD")
        self.assertFalse(result["e0_authorized"])
        self.assertFalse(result["substantive_gate_resolved"])

    def test_declaration_text_cannot_substitute_for_evidence(self):
        def declarations(*args):
            return b"a2a8523c065d4d41155aa29d367c888d49ab3032f6075b8cebbd2475ff1efd78"
        result = self.run_case(declarations, declarations)
        self.assertEqual(result["h2a1_verdict"], "NOT VERIFIED")
        self.assertTrue(all(row["status"] == "NOT VERIFIED" for row in result["anchors"]))

    def test_git_failure_and_timeout_fail_closed(self):
        for error in (subprocess.CalledProcessError(1, "git"), subprocess.TimeoutExpired("git", 15)):
            result = self.run_case(error, FileNotFoundError())
            self.assertEqual(result["h2a1_verdict"], "BLOCKED")

    def synthetic_case(self, failure=None):
        commit = b"tree synthetic\n\nfixture only\n"
        commit_id = hashlib.sha1(b"commit " + str(len(commit)).encode() + b"\0" + commit).hexdigest()
        payload = b"synthetic retained bytes"
        expected = {
            "h1_checkpoint_commit": commit_id,
            "scientific_base_commit": commit_id,
            "frozen_preregistration_sha256": hashlib.sha256(payload).hexdigest(),
            "h1_audit_bundle_sha256": hashlib.sha256(payload).hexdigest(),
        }
        def git(repo, *args):
            if args[0] == "cat-file":
                return commit
            if args[0] == "rev-parse":
                return b"fixture-head\n"
            if args[0] == "merge-base":
                if failure == "ancestry":
                    raise subprocess.CalledProcessError(1, "git")
                return b""
            if args[0] == "show":
                return b"changed" if failure == "historical" else payload
            raise AssertionError(args)
        with patch.object(verifier, "EXPECTED_ANCHOR_DECLARATIONS", expected):
            return self.run_case(git, lambda path: payload)

    def test_synthetic_matching_identities_still_leave_all_gates_unresolved(self):
        result = self.synthetic_case()
        self.assertEqual(result["h2a1_verdict"], "VERIFIED")
        self.assertEqual(len(result["unresolved_h2_gates"]), 8)
        self.assertFalse(result["e0_authorized"])
        self.assertFalse(result["substantive_gate_resolved"])
        self.assertEqual(result["overall_status"], "HOLD")
        for row in result["anchors"]:
            self.assertEqual(row["observed"], row["expected"])
            self.assertGreater(row["byte_count"], 0)
            self.assertIn("source", row)

    def test_matching_commit_bytes_without_ancestry_are_blocked(self):
        result = self.synthetic_case("ancestry")
        self.assertEqual(result["h2a1_verdict"], "BLOCKED")
        self.assertEqual([r["status"] for r in result["anchors"][:2]], ["BLOCKED"] * 2)

    def test_matching_file_digest_without_historical_bytes_is_blocked(self):
        result = self.synthetic_case("historical")
        self.assertEqual(result["anchors"][2]["status"], "BLOCKED")
        self.assertEqual(result["h2a1_verdict"], "BLOCKED")

    def test_file_read_requires_retained_regular_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "retained"
            path.write_bytes(b"independent bytes")
            self.assertEqual(verifier._read_regular(path), b"independent bytes")
            link = Path(temp) / "alias"
            link.symlink_to(path)
            with self.assertRaises(ValueError):
                verifier._read_regular(link)
            with self.assertRaises(ValueError):
                verifier._read_regular(Path(temp))

    def test_git_invocation_has_no_inherited_credentials_or_lazy_fetch(self):
        with patch.object(verifier.subprocess, "run") as run:
            run.return_value.stdout = b"raw"
            self.assertEqual(verifier._git(Path("/repo"), "cat-file", "commit", "abc"), b"raw")
            args, kwargs = run.call_args
            self.assertIn("--no-replace-objects", args[0])
            self.assertEqual(kwargs["env"]["GIT_NO_LAZY_FETCH"], "1")
            self.assertEqual(kwargs["env"]["GIT_CONFIG_GLOBAL"], "/dev/null")
            self.assertNotIn("HOME", kwargs["env"])


if __name__ == "__main__":
    unittest.main()
