from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

from e0.hardening import (
    AppendOnlyJournal,
    BudgetError,
    CANONICAL_COMMIT,
    ContractError,
    FROZEN_OPERATIONS,
    FROZEN_PREREGISTRATION_PATH,
    FROZEN_SIDECAR_PATH,
    H1_AUTHORIZATION_SCHEMA,
    H1_MANIFEST_SCHEMA,
    H1Refusal,
    HttpStatusError,
    LOGICAL_OPERATION_FIELDS,
    LiveAdapterUnavailable,
    LiveGetDataAdapter,
    LogicalOperation,
    MockAdapterSession,
    MockResponseContract,
    OperationBudget,
    RunGuard,
    TemporaryDnsFailure,
    VerifiedContext,
    is_retryable_error,
    manifest_content_sha256,
    run_mock_attempts,
    sha256_file,
    verify_h1_context,
    _git_head,
    _git_toplevel,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LOGICAL_OPERATION_FIELDS = (
    "query_index",
    "stride",
    "partition_number",
    "first_flattened_index",
    "final_flattened_index",
    "requested_point_count",
)


class IntSubclass(int):
    pass


def isolated_git(*args, text=False):
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update(
        {
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_TERMINAL_PROMPT": "0",
            "GCM_INTERACTIVE": "Never",
            "SSH_ASKPASS_REQUIRE": "never",
        }
    )
    return subprocess.run(
        [
            "git",
            "-c",
            "commit.gpgsign=false",
            "-c",
            "tag.gpgsign=false",
            "-c",
            f"core.hooksPath={os.devnull}",
            "-c",
            f"core.attributesFile={os.devnull}",
            "-c",
            "credential.helper=",
            *map(str, args),
        ],
        check=True,
        capture_output=True,
        text=text,
        env=env,
    )


class H1Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="ns001-h1-")
        self.base = Path(self.temp.name)
        self.package = REPO_ROOT
        self.git_root = REPO_ROOT
        self.outside = self.base / "outside"
        self.run_root = self.outside / "run-001"
        self.outside.mkdir()
        prereg = self.package / FROZEN_PREREGISTRATION_PATH
        sidecar = self.package / FROZEN_SIDECAR_PATH
        code = self.package / "e0" / "hardening.py"
        self.source_head = isolated_git(
            "-C", self.package, "rev-parse", "HEAD", text=True
        ).stdout.strip()

        content = {
            "schema": H1_MANIFEST_SCHEMA,
            "status": "DRAFT_H1_OFFLINE_ONLY",
            "mock_only": True,
            "run_id": "synthetic-run-001",
            "scientific_base_commit": CANONICAL_COMMIT,
            "source_head_commit": self.source_head,
            "package_root": str(self.package.resolve()),
            "run_root": str(self.run_root),
            "logical_operations": [op.as_dict() for op in FROZEN_OPERATIONS],
            "artifacts": {
                "code": {
                    "path": "e0/hardening.py",
                    "sha256": sha256_file(code),
                },
                "preregistration": {
                    "path": FROZEN_PREREGISTRATION_PATH,
                    "sha256": sha256_file(prereg),
                },
                "sidecar": {
                    "path": FROZEN_SIDECAR_PATH,
                    "sha256": sha256_file(sidecar),
                },
            },
        }
        self.manifest = {
            "content": content,
            "manifest_content_sha256": manifest_content_sha256(content),
        }
        self.authorization = {
            "schema": H1_AUTHORIZATION_SCHEMA,
            "mock_only": True,
            "run_id": content["run_id"],
            "manifest_content_sha256": self.manifest["manifest_content_sha256"],
            "package_root": str(self.package.resolve()),
            "run_root": str(self.run_root),
        }
        network_error = AssertionError("network forbidden in H1 tests")
        self.network_patchers = [
            mock.patch("socket.socket", side_effect=network_error),
            mock.patch("socket.create_connection", side_effect=network_error),
            mock.patch("socket.getaddrinfo", side_effect=network_error),
            mock.patch("socket.gethostbyname", side_effect=network_error),
            mock.patch("socket.gethostbyname_ex", side_effect=network_error),
            mock.patch("socket.gethostbyaddr", side_effect=network_error),
            mock.patch("socket.getnameinfo", side_effect=network_error),
        ]
        for patcher in self.network_patchers:
            patcher.start()

    def tearDown(self) -> None:
        for patcher in reversed(self.network_patchers):
            patcher.stop()
        self.temp.cleanup()

    def verified(self, *, git_root=None):
        return verify_h1_context(
            self.manifest,
            self.authorization,
            git_root=self.git_root if git_root is None else git_root,
        )

    def _set_run_root(self, name: str) -> None:
        self.run_root = self.outside / name
        self.manifest["content"]["run_root"] = str(self.run_root)
        self.manifest["content"]["run_id"] = name
        self.authorization["run_root"] = str(self.run_root)
        self.authorization["run_id"] = name
        self._rehash_manifest()

    def _assert_no_run_outputs(self, run_root: Path) -> None:
        lock = run_root.parent / f".{run_root.name}.h1-lock"
        self.assertFalse(run_root.exists())
        self.assertFalse(lock.exists())
        self.assertFalse((run_root / "H1_MOCK_CONSUMED").exists())
        self.assertFalse((run_root / "attempts.jsonl").exists())

    def _assert_manifest_operation_schema_refusal(self, entry: object) -> None:
        manifest = json.loads(json.dumps(self.manifest))
        authorization = json.loads(json.dumps(self.authorization))
        manifest["content"]["logical_operations"][0] = entry
        digest = manifest_content_sha256(manifest["content"])
        manifest["manifest_content_sha256"] = digest
        authorization["manifest_content_sha256"] = digest
        credential = mock.Mock(return_value="synthetic-marker")
        transport = mock.Mock()

        with self.assertRaisesRegex(H1Refusal, "logical-operation"):
            MockAdapterSession.create(
                manifest,
                authorization,
                git_root=self.git_root,
                credential_provider=credential,
                transport=transport,
            )
        credential.assert_not_called()
        transport.assert_not_called()
        self._assert_no_run_outputs(Path(manifest["content"]["run_root"]))

    def _create_package_repo(self, name: str, *, code_path="e0/hardening.py"):
        package = self.base / name
        (package / "e0").mkdir(parents=True)
        prereg = package / FROZEN_PREREGISTRATION_PATH
        prereg.parent.mkdir(parents=True)
        shutil.copyfile(REPO_ROOT / FROZEN_PREREGISTRATION_PATH, prereg)
        sidecar = package / FROZEN_SIDECAR_PATH
        shutil.copyfile(REPO_ROOT / FROZEN_SIDECAR_PATH, sidecar)
        copied_code = package / "e0" / "hardening.py"
        shutil.copyfile(REPO_ROOT / "e0" / "hardening.py", copied_code)
        if code_path != "e0/hardening.py":
            alias = package / code_path
            alias.parent.mkdir(parents=True, exist_ok=True)
            alias.symlink_to(copied_code.name)
        template = self.base / f"{name}-empty-template"
        template.mkdir()
        isolated_git("init", "-q", f"--template={template}", package)
        isolated_git("-C", package, "add", ".")
        isolated_git(
            "-C",
            package,
            "-c",
            "user.name=NS-001 H1 fixture",
            "-c",
            "user.email=h1-fixture@example.invalid",
            "commit",
            "-q",
            "-m",
            "synthetic H1 fixture",
        )
        source_head = isolated_git(
            "-C", package, "rev-parse", "HEAD", text=True
        ).stdout.strip()
        run_root = self.outside / f"{name}-run"
        code = package / code_path
        content = {
            "schema": H1_MANIFEST_SCHEMA,
            "status": "DRAFT_H1_OFFLINE_ONLY",
            "mock_only": True,
            "run_id": f"{name}-run",
            "scientific_base_commit": CANONICAL_COMMIT,
            "source_head_commit": source_head,
            "package_root": str(package.resolve()),
            "run_root": str(run_root),
            "logical_operations": [op.as_dict() for op in FROZEN_OPERATIONS],
            "artifacts": {
                "code": {"path": code_path, "sha256": sha256_file(code)},
                "preregistration": {
                    "path": FROZEN_PREREGISTRATION_PATH,
                    "sha256": sha256_file(prereg),
                },
                "sidecar": {
                    "path": FROZEN_SIDECAR_PATH,
                    "sha256": sha256_file(sidecar),
                },
            },
        }
        digest = manifest_content_sha256(content)
        manifest = {"content": content, "manifest_content_sha256": digest}
        authorization = {
            "schema": H1_AUTHORIZATION_SCHEMA,
            "mock_only": True,
            "run_id": content["run_id"],
            "manifest_content_sha256": digest,
            "package_root": str(package.resolve()),
            "run_root": str(run_root),
        }
        return package, manifest, authorization

    def test_valid_context_and_frozen_operations(self) -> None:
        self.assertEqual(LOGICAL_OPERATION_FIELDS, EXPECTED_LOGICAL_OPERATION_FIELDS)
        context = self.verified()
        self.assertTrue(context.mock_only)
        self.assertEqual(context.run_id, "synthetic-run-001")
        self.assertEqual(context.scientific_base_commit, CANONICAL_COMMIT)
        self.assertEqual(context.source_head_commit, self.source_head)
        self.assertEqual(len(context.operations), 12)
        self.assertEqual([op.requested_point_count for op in context.operations[:3]], [262_144, 2_000_000, 97_152])
        self.assertEqual(sum(op.requested_point_count for op in context.operations if op.stride == 4), 256**3)
        for stride in (16, 8, 4):
            selected = [op for op in context.operations if op.stride == stride]
            self.assertEqual(selected[0].first_flattened_index, 0)
            for previous, current in zip(selected, selected[1:]):
                self.assertEqual(current.first_flattened_index, previous.final_flattened_index + 1)
            self.assertEqual(selected[-1].final_flattened_index + 1, (1024 // stride) ** 3)

    def test_manifest_operation_field_types_refuse_before_callbacks(self) -> None:
        valid = FROZEN_OPERATIONS[0].as_dict()
        for field in EXPECTED_LOGICAL_OPERATION_FIELDS:
            expected = valid[field]
            invalid_values = (
                ("boolean", bool(expected)),
                ("float", float(expected)),
                ("int-subclass", IntSubclass(expected)),
                ("string", str(expected)),
                ("null", None),
            )
            for invalid_type, invalid_value in invalid_values:
                with self.subTest(field=field, invalid_type=invalid_type):
                    if invalid_type in {"float", "int-subclass"} or (
                        invalid_type == "boolean" and expected in {0, 1}
                    ):
                        self.assertEqual(invalid_value, expected)
                    entry = valid | {field: invalid_value}
                    self._assert_manifest_operation_schema_refusal(entry)

    def test_manifest_operation_keys_and_entry_shape_refuse_before_callbacks(self) -> None:
        valid = FROZEN_OPERATIONS[0].as_dict()
        for missing in EXPECTED_LOGICAL_OPERATION_FIELDS:
            with self.subTest(missing=missing):
                entry = dict(valid)
                del entry[missing]
                self._assert_manifest_operation_schema_refusal(entry)

        self._assert_manifest_operation_schema_refusal(valid | {"unexpected": 1})
        self._assert_manifest_operation_schema_refusal(list(valid.values()))
        self._assert_manifest_operation_schema_refusal(None)

    def test_manifest_binds_associated_module_source_file(self) -> None:
        context = self.verified()
        binding = self.manifest["content"]["artifacts"]["code"]
        running_source = Path(sys.modules[verify_h1_context.__module__].__file__).resolve()
        self.assertEqual((context.package_root / binding["path"]).resolve(), running_source)
        self.assertEqual(sha256_file(running_source), binding["sha256"])
        self.assertEqual(context.runner_path, running_source)
        self.assertEqual(context.runner_sha256, binding["sha256"])

    def test_post_initialization_source_replacement_is_detected(self) -> None:
        real_source = REPO_ROOT / "e0" / "hardening.py"
        real_source_before = sha256_file(real_source)
        package, manifest, authorization = self._create_package_repo(
            "load-time-mismatch"
        )
        copied = package / "e0" / "hardening.py"
        approved_bytes = copied.read_bytes()
        copied.write_bytes(
            approved_bytes + b'\nH1_SYNTHETIC_LOAD_MARKER = "earlier-bytes"\n'
        )
        module_name = "_ns001_load_time_mismatch_hardening"
        spec = importlib.util.spec_from_file_location(module_name, copied)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        calls = {"credential": 0, "transport": 0}
        try:
            spec.loader.exec_module(module)
            self.assertEqual(module.H1_SYNTHETIC_LOAD_MARKER, "earlier-bytes")
            copied.write_bytes(approved_bytes)
            with self.assertRaisesRegex(
                module.H1Refusal, "initialization-time or current source file"
            ):
                module.MockAdapterSession.create(
                    manifest,
                    authorization,
                    git_root=package,
                    credential_provider=lambda: calls.__setitem__(
                        "credential", calls["credential"] + 1
                    ),
                    transport=lambda *_args: calls.__setitem__(
                        "transport", calls["transport"] + 1
                    ),
                )
        finally:
            sys.modules.pop(module_name, None)
        self.assertEqual(calls, {"credential": 0, "transport": 0})
        self.assertEqual(sha256_file(real_source), real_source_before)

    def test_substituted_and_copied_runner_refuse_before_callbacks(self) -> None:
        calls = {"credential": 0, "transport": 0}

        def credential():
            calls["credential"] += 1

        def transport(*_args):
            calls["transport"] += 1

        substitute = REPO_ROOT / "tests" / "test_e0_hardening.py"
        binding = self.manifest["content"]["artifacts"]["code"]
        binding.update(
            {
                "path": "tests/test_e0_hardening.py",
                "sha256": sha256_file(substitute),
            }
        )
        self._rehash_manifest()
        with self.assertRaisesRegex(H1Refusal, "associated with this imported module"):
            MockAdapterSession.create(
                self.manifest,
                self.authorization,
                git_root=self.git_root,
                credential_provider=credential,
                transport=transport,
            )
        self.assertEqual(calls, {"credential": 0, "transport": 0})

        package, manifest, authorization = self._create_package_repo("copied-package")
        with self.assertRaisesRegex(H1Refusal, "associated with this imported module"):
            MockAdapterSession.create(
                manifest,
                authorization,
                git_root=package,
                credential_provider=credential,
                transport=transport,
            )
        self.assertEqual(calls, {"credential": 0, "transport": 0})

    def test_symlink_aliased_runner_refuses_before_callbacks(self) -> None:
        package, manifest, authorization = self._create_package_repo(
            "symlink-package", code_path="e0/runner-link.py"
        )
        calls = {"credential": 0, "transport": 0}
        with self.assertRaisesRegex(H1Refusal, "symlink alias"):
            MockAdapterSession.create(
                manifest,
                authorization,
                git_root=package,
                credential_provider=lambda: calls.__setitem__(
                    "credential", calls["credential"] + 1
                ),
                transport=lambda *_args: calls.__setitem__(
                    "transport", calls["transport"] + 1
                ),
            )
        self.assertEqual(calls, {"credential": 0, "transport": 0})

    def test_separately_imported_runner_refuses_before_callbacks(self) -> None:
        copied = self.base / "separately-imported-hardening.py"
        shutil.copyfile(REPO_ROOT / "e0" / "hardening.py", copied)
        module_name = "_ns001_separately_imported_hardening"
        spec = importlib.util.spec_from_file_location(module_name, copied)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        calls = {"credential": 0, "transport": 0}
        try:
            spec.loader.exec_module(module)
            with self.assertRaisesRegex(
                module.H1Refusal, "associated with this imported module"
            ):
                module.MockAdapterSession.create(
                    self.manifest,
                    self.authorization,
                    git_root=self.git_root,
                    credential_provider=lambda: calls.__setitem__(
                        "credential", calls["credential"] + 1
                    ),
                    transport=lambda *_args: calls.__setitem__(
                        "transport", calls["transport"] + 1
                    ),
                )
        finally:
            sys.modules.pop(module_name, None)
        self.assertEqual(calls, {"credential": 0, "transport": 0})

    def test_each_bound_hash_mismatch_refuses(self) -> None:
        refusal_patterns = {
            "code": "runner source digest disagrees",
            "preregistration": "preregistration hash mismatch",
            "sidecar": "sidecar hash mismatch",
        }
        for artifact, refusal_pattern in refusal_patterns.items():
            with self.subTest(artifact=artifact):
                manifest = json.loads(json.dumps(self.manifest))
                authorization = json.loads(json.dumps(self.authorization))
                binding = manifest["content"]["artifacts"][artifact]
                self.assertNotEqual(binding["sha256"], "0" * 64)
                binding["sha256"] = "0" * 64
                digest = manifest_content_sha256(manifest["content"])
                manifest["manifest_content_sha256"] = digest
                authorization["manifest_content_sha256"] = digest
                calls = {"credential": 0, "transport": 0}
                with self.assertRaisesRegex(H1Refusal, refusal_pattern):
                    MockAdapterSession.create(
                        manifest,
                        authorization,
                        git_root=self.git_root,
                        credential_provider=lambda: calls.__setitem__(
                            "credential", calls["credential"] + 1
                        ),
                        transport=lambda *_args: calls.__setitem__(
                            "transport", calls["transport"] + 1
                        ),
                    )
                self.assertEqual(calls, {"credential": 0, "transport": 0})
                run_root = Path(manifest["content"]["run_root"])
                lock = run_root.parent / f".{run_root.name}.h1-lock"
                self.assertFalse(run_root.exists())
                self.assertFalse(lock.exists())
                self.assertFalse((run_root / "H1_MOCK_CONSUMED").exists())
                self.assertFalse((run_root / "attempts.jsonl").exists())
        original = self.manifest["manifest_content_sha256"]
        self.manifest["manifest_content_sha256"] = "0" * 64
        with self.assertRaises(H1Refusal):
            self.verified()
        self.manifest["manifest_content_sha256"] = original

    def test_updated_artifact_digest_requires_new_authorized_manifest_hash(self) -> None:
        self.manifest["content"]["artifacts"]["code"]["sha256"] = "0" * 64
        with self.assertRaises(H1Refusal):
            self.verified()

    def test_manifest_mutation_refuses(self) -> None:
        self.manifest["content"]["scientific_base_commit"] = "0" * 40
        with self.assertRaises(H1Refusal):
            self.verified()

    def test_sidecar_content_mismatch_refuses_after_file_hash_matches(self) -> None:
        package, manifest, authorization = self._create_package_repo(
            "sidecar-content-mismatch"
        )
        copied = package / "e0" / "hardening.py"
        module_name = "_ns001_sidecar_content_hardening"
        spec = importlib.util.spec_from_file_location(module_name, copied)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        try:
            spec.loader.exec_module(module)
            sidecar = package / FROZEN_SIDECAR_PATH
            sidecar.write_text(
                "0" * 64 + "  invalid-frozen-preregistration-name.md\n",
                encoding="utf-8",
            )
            manifest["content"]["artifacts"]["sidecar"]["sha256"] = sha256_file(
                sidecar
            )
            digest = manifest_content_sha256(manifest["content"])
            manifest["manifest_content_sha256"] = digest
            authorization["manifest_content_sha256"] = digest
            with self.assertRaisesRegex(
                module.H1Refusal,
                "frozen preregistration sidecar content mismatch",
            ):
                module.verify_h1_context(
                    manifest,
                    authorization,
                    git_root=package,
                )
        finally:
            sys.modules.pop(module_name, None)

    def test_path_validation_refuses_relative_overlap_and_symlink(self) -> None:
        original = self.manifest["content"]["run_root"]
        self.manifest["content"]["run_root"] = "relative/run"
        self._rehash_manifest()
        with self.assertRaises(H1Refusal):
            self.verified()

        inside = self.package / "runs" / "run-001"
        self.manifest["content"]["run_root"] = str(inside)
        self.authorization["run_root"] = str(inside)
        self._rehash_manifest()
        with self.assertRaises(H1Refusal):
            self.verified()

        target = self.outside / "target"
        target.mkdir()
        symlink = self.outside / "symlink-run"
        symlink.symlink_to(target, target_is_directory=True)
        self.manifest["content"]["run_root"] = str(symlink)
        self.authorization["run_root"] = str(symlink)
        self._rehash_manifest()
        with self.assertRaises(H1Refusal):
            self.verified()
        self.manifest["content"]["run_root"] = original

    def test_git_root_must_be_actual_top_level_without_aliases(self) -> None:
        nested = self.package / "e0"
        unrelated = self.base / "unrelated"
        template = self.base / "empty-template"
        template.mkdir()
        isolated_git("init", "-q", f"--template={template}", unrelated)
        fake = self.base / "fake"
        (fake / ".git").mkdir(parents=True)
        alias = self.base / "package-alias"
        alias.symlink_to(self.package, target_is_directory=True)
        for label, supplied in (
            ("nested", nested),
            ("unrelated", unrelated),
            ("fake", fake),
            ("symlink", alias),
        ):
            with self.subTest(label=label), self.assertRaises(H1Refusal):
                self.verified(git_root=supplied)

    def test_temporary_git_setup_ignores_hostile_user_configuration(self) -> None:
        hooks = self.base / "hostile-hooks"
        hooks.mkdir()
        hook_marker = self.base / "hook-ran"
        hook = hooks / "pre-commit"
        hook.write_text(f"#!/bin/sh\nprintf ran > '{hook_marker}'\nexit 1\n", encoding="utf-8")
        hook.chmod(0o700)
        hostile_config = self.base / "hostile-gitconfig"
        hostile_config.write_text(
            "[commit]\n"
            "\tgpgsign = true\n"
            "[core]\n"
            f"\thooksPath = {hooks}\n"
            "[user]\n"
            "\tsigningKey = forbidden-test-key\n",
            encoding="utf-8",
        )

        with mock.patch.dict(
            os.environ,
            {
                "GIT_CONFIG_GLOBAL": str(hostile_config),
                "GIT_CONFIG_NOSYSTEM": "0",
                "GIT_TERMINAL_PROMPT": "1",
            },
        ):
            package, _manifest, _authorization = self._create_package_repo(
                "hostile-config-package"
            )
        self.assertFalse(hook_marker.exists())
        self.assertEqual(
            isolated_git("-C", package, "rev-list", "--count", "HEAD", text=True).stdout.strip(),
            "1",
        )

    def test_integrity_git_checks_ignore_hostile_repository_redirection(self) -> None:
        alternate, _manifest, _authorization = self._create_package_repo(
            "redirected-alternate"
        )
        alternate_head = isolated_git(
            "-C", alternate, "rev-parse", "HEAD", text=True
        ).stdout.strip()
        self.assertNotEqual(alternate_head, self.source_head)
        hostile_config = self.base / "integrity-hostile-gitconfig"
        hostile_config.write_text("[core]\n\tbare = true\n", encoding="utf-8")
        hostile_environment = {
            "GIT_DIR": str(alternate / ".git"),
            "GIT_WORK_TREE": str(alternate),
            "GIT_COMMON_DIR": str(alternate / ".git"),
            "GIT_INDEX_FILE": str(self.base / "redirected-index"),
            "GIT_CONFIG_GLOBAL": str(hostile_config),
            "GIT_CONFIG_SYSTEM": str(hostile_config),
            "GIT_CONFIG_NOSYSTEM": "0",
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "core.bare",
            "GIT_CONFIG_VALUE_0": "true",
            "GIT_TERMINAL_PROMPT": "1",
        }

        with mock.patch.dict(os.environ, hostile_environment):
            self.assertEqual(_git_toplevel(REPO_ROOT, "target"), REPO_ROOT)
            self.assertEqual(_git_head(REPO_ROOT), self.source_head)
            self.assertEqual(self.verified().source_head_commit, self.source_head)
            self.manifest["content"]["source_head_commit"] = alternate_head
            self._rehash_manifest()
            with self.assertRaisesRegex(H1Refusal, "source HEAD"):
                self.verified()

    def test_manifest_source_head_must_match_actual_git_head_before_callbacks(self) -> None:
        calls = {"credential": 0, "transport": 0}
        self.assertEqual(self.verified().source_head_commit, self.source_head)
        self.manifest["content"]["source_head_commit"] = "0" * 40
        self._rehash_manifest()

        with self.assertRaisesRegex(H1Refusal, "source HEAD"):
            MockAdapterSession.create(
                self.manifest,
                self.authorization,
                git_root=self.git_root,
                credential_provider=lambda: calls.__setitem__(
                    "credential", calls["credential"] + 1
                ),
                transport=lambda *_args: calls.__setitem__(
                    "transport", calls["transport"] + 1
                ),
            )
        self.assertEqual(calls, {"credential": 0, "transport": 0})

    def _rehash_manifest(self) -> None:
        digest = manifest_content_sha256(self.manifest["content"])
        self.manifest["manifest_content_sha256"] = digest
        self.authorization["manifest_content_sha256"] = digest

    def test_live_adapter_fails_without_callbacks(self) -> None:
        calls = {"credential": 0, "transport": 0}

        def credential():
            calls["credential"] += 1

        def transport():
            calls["transport"] += 1

        with self.assertRaises(LiveAdapterUnavailable):
            LiveGetDataAdapter(credential, transport).fetch()
        self.assertEqual(calls, {"credential": 0, "transport": 0})

    def test_hash_failure_precedes_mock_credential_and_transport(self) -> None:
        calls = {"credential": 0, "transport": 0}
        self.manifest["content"]["artifacts"]["code"]["sha256"] = "0" * 64
        self._rehash_manifest()

        def credential():
            calls["credential"] += 1
            return "synthetic-marker"

        def transport(*_args):
            calls["transport"] += 1

        with self.assertRaisesRegex(H1Refusal, "runner source digest disagrees"):
            MockAdapterSession.create(
                self.manifest,
                self.authorization,
                git_root=self.git_root,
                credential_provider=credential,
                transport=transport,
            )
        self.assertEqual(calls, {"credential": 0, "transport": 0})
        self.assertFalse(self.run_root.exists())
        lock = self.run_root.parent / f".{self.run_root.name}.h1-lock"
        self.assertFalse(lock.exists())
        self.assertFalse((self.run_root / "H1_MOCK_CONSUMED").exists())
        self.assertFalse((self.run_root / "attempts.jsonl").exists())

    def test_run_guard_refuses_existing_output_and_rerun(self) -> None:
        context = self.verified()
        guard = RunGuard(context)
        guard.acquire()
        marker = context.run_root / "H1_MOCK_CONSUMED"
        original = marker.read_bytes()
        guard.release()
        with self.assertRaises(H1Refusal):
            RunGuard(context).acquire()
        self.assertEqual(marker.read_bytes(), original)

    def test_existing_partial_receipt_refuses_before_callbacks_and_is_unchanged(self) -> None:
        calls = {"credential": 0, "transport": 0}
        self.run_root.mkdir()
        partial = self.run_root / "attempts.jsonl"
        partial.write_bytes(b'{"partial":true')
        before = partial.read_bytes()

        def credential():
            calls["credential"] += 1
            return "synthetic-marker"

        def transport(*_args):
            calls["transport"] += 1

        with self.assertRaises(H1Refusal):
            MockAdapterSession.create(
                self.manifest,
                self.authorization,
                git_root=self.git_root,
                credential_provider=credential,
                transport=transport,
            )
        self.assertEqual(partial.read_bytes(), before)
        self.assertEqual(calls, {"credential": 0, "transport": 0})

    def test_existing_lock_refuses_before_callbacks_and_is_unchanged(self) -> None:
        context = self.verified()
        lock = RunGuard(context).lock_path
        lock.write_bytes(b"existing-lock\n")
        before = lock.read_bytes()
        calls = {"credential": 0, "transport": 0}

        def credential():
            calls["credential"] += 1

        def transport(*_args):
            calls["transport"] += 1

        with self.assertRaises(H1Refusal):
            MockAdapterSession.create(
                self.manifest,
                self.authorization,
                git_root=self.git_root,
                credential_provider=credential,
                transport=transport,
            )
        self.assertEqual(lock.read_bytes(), before)
        self.assertEqual(calls, {"credential": 0, "transport": 0})

    def test_context_and_component_substitution_refuse_before_callbacks(self) -> None:
        calls = {"credential": 0, "transport": 0}

        def credential():
            calls["credential"] += 1

        def transport(*_args):
            calls["transport"] += 1

        with self.assertRaises(H1Refusal):
            VerifiedContext()
        with self.assertRaises(H1Refusal):
            RunGuard(object.__new__(VerifiedContext))
        for field in ("context", "guard", "journal", "budget"):
            with self.subTest(field=field), self.assertRaises(H1Refusal):
                MockAdapterSession.create(
                    self.manifest,
                    self.authorization,
                    git_root=self.git_root,
                    credential_provider=credential,
                    transport=transport,
                    **{field: object()},
                )
        class SubstituteSession(MockAdapterSession):
            pass

        with self.assertRaises(H1Refusal):
            SubstituteSession.create(
                self.manifest,
                self.authorization,
                git_root=self.git_root,
                credential_provider=credential,
                transport=transport,
            )
        self.assertEqual(calls, {"credential": 0, "transport": 0})
        self.assertFalse(self.run_root.exists())

    def test_run_id_mismatch_refuses_before_callbacks(self) -> None:
        calls = {"credential": 0, "transport": 0}
        self.authorization["run_id"] = "substituted-run"
        with self.assertRaisesRegex(H1Refusal, "run_id"):
            MockAdapterSession.create(
                self.manifest,
                self.authorization,
                git_root=self.git_root,
                credential_provider=lambda: calls.__setitem__(
                    "credential", calls["credential"] + 1
                ),
                transport=lambda *_args: calls.__setitem__(
                    "transport", calls["transport"] + 1
                ),
            )
        self.assertEqual(calls, {"credential": 0, "transport": 0})
        self.assertFalse(self.run_root.exists())

    def test_lock_marker_and_journal_share_verified_binding(self) -> None:
        session = MockAdapterSession.create(
            self.manifest,
            self.authorization,
            git_root=self.git_root,
            credential_provider=lambda: "synthetic-marker",
            transport=lambda *_args: {"mock": "response"},
        )
        request_hash = hashlib.sha256(b"binding request").hexdigest()
        run_mock_attempts(session, FROZEN_OPERATIONS[0], request_hash)
        session.close()

        lock = json.loads(
            (self.outside / ".run-001.h1-lock").read_text(encoding="utf-8")
        )
        marker = json.loads(
            (self.run_root / "H1_MOCK_CONSUMED").read_text(encoding="utf-8")
        )
        journal = json.loads(
            (self.run_root / "attempts.jsonl").read_text(encoding="utf-8").splitlines()[0]
        )
        for field in (
            "manifest_content_sha256",
            "run_id",
            "package_root",
            "run_root",
            "operation_specs_sha256",
            "scientific_base_commit",
            "source_head_commit",
        ):
            self.assertEqual(lock[field], marker[field])
            self.assertEqual(marker[field], journal[field])

    def test_append_only_journal_and_retry_receipts(self) -> None:
        calls = []

        def credential():
            return "synthetic-marker"

        def transport(operation, request_identity, marker):
            calls.append((operation.query_index, request_identity, marker))
            if len(calls) < 3:
                raise TimeoutError("synthetic timeout")
            return {"mock": "response"}

        session = MockAdapterSession.create(
            self.manifest,
            self.authorization,
            git_root=self.git_root,
            credential_provider=credential,
            transport=transport,
        )
        request_hash = hashlib.sha256(b"fixed mock request").hexdigest()
        result = run_mock_attempts(
            session,
            FROZEN_OPERATIONS[0],
            request_hash,
        )
        session.close()
        self.assertEqual(result, {"mock": "response"})
        self.assertEqual(len(calls), 3)
        self.assertEqual({item[1] for item in calls}, {request_hash})
        events = [json.loads(line) for line in (self.run_root / "attempts.jsonl").read_text().splitlines()]
        self.assertEqual([event["event"] for event in events], [
            "attempt-start", "attempt-finish",
            "attempt-start", "attempt-finish",
            "attempt-start", "attempt-finish", "partition-status",
        ])
        self.assertTrue(all(event["h1_mock"] and not event["production_receipt"] for event in events))

    def test_all_operation_budget_refusals_precede_transport(self) -> None:
        request_hash = hashlib.sha256(b"budgeted request").hexdigest()

        def new_session(name):
            self._set_run_root(name)
            calls = {"transport": 0}

            def transport(*_args):
                calls["transport"] += 1
                return {"mock": "response"}

            session = MockAdapterSession.create(
                self.manifest,
                self.authorization,
                git_root=self.git_root,
                credential_provider=lambda: "synthetic-marker",
                transport=transport,
            )
            return session, calls

        unknown = LogicalOperation(99, 99, 1, 0, 0, 1)
        mismatched = LogicalOperation(
            **(
                FROZEN_OPERATIONS[0].as_dict()
                | {
                    "requested_point_count": FROZEN_OPERATIONS[0].requested_point_count - 1,
                }
            )
        )
        for name, operation in (
            ("unknown-operation", unknown),
            ("mismatched-operation", mismatched),
            ("out-of-order-operation", FROZEN_OPERATIONS[1]),
        ):
            with self.subTest(case=name):
                session, calls = new_session(name)
                with self.assertRaises(BudgetError):
                    run_mock_attempts(session, operation, request_hash)
                self.assertEqual(calls["transport"], 0)
                session.close()

        session, calls = new_session("repeated-operation")
        run_mock_attempts(session, FROZEN_OPERATIONS[0], request_hash)
        self.assertEqual(calls["transport"], 1)
        with self.assertRaises(BudgetError):
            run_mock_attempts(session, FROZEN_OPERATIONS[0], request_hash)
        self.assertEqual(calls["transport"], 1)
        session.close()

        session, calls = new_session("thirteenth-operation")
        for operation in FROZEN_OPERATIONS:
            run_mock_attempts(session, operation, request_hash)
        self.assertEqual(calls["transport"], 12)
        with self.assertRaises(BudgetError):
            run_mock_attempts(session, FROZEN_OPERATIONS[-1], request_hash)
        self.assertEqual(calls["transport"], 12)
        session.close()

    def test_malformed_session_operations_preserve_operation_and_retry_budget(self) -> None:
        calls: list[int] = []

        def transport(operation, *_args):
            calls.append(operation.query_index)
            if operation == FROZEN_OPERATIONS[0] and calls.count(1) < 3:
                raise TimeoutError("synthetic timeout")
            return {"mock": "response"}

        session = MockAdapterSession.create(
            self.manifest,
            self.authorization,
            git_root=self.git_root,
            credential_provider=lambda: "synthetic-marker",
            transport=transport,
        )
        journal = self.run_root / "attempts.jsonl"
        before = journal.read_bytes()
        valid = FROZEN_OPERATIONS[0].as_dict()
        malformed: list[tuple[str, LogicalOperation]] = []
        for field in EXPECTED_LOGICAL_OPERATION_FIELDS:
            expected = valid[field]
            invalid_values = (
                ("boolean", bool(expected)),
                ("float", float(expected)),
                ("int-subclass", IntSubclass(expected)),
                ("string", str(expected)),
                ("null", None),
            )
            for invalid_type, invalid_value in invalid_values:
                malformed.append(
                    (
                        f"{field}-{invalid_type}",
                        LogicalOperation(**(valid | {field: invalid_value})),
                    )
                )

        bypassed = object.__new__(LogicalOperation)
        bypassed.__dict__.update(valid)
        bypassed.__dict__["stride"] = 16.0
        malformed.append(("bypassed-construction", bypassed))

        mutated = LogicalOperation(**valid)
        object.__setattr__(mutated, "stride", 16.0)
        malformed.append(("mutated-after-construction", mutated))

        missing = object.__new__(LogicalOperation)
        missing.__dict__.update(valid)
        del missing.__dict__["partition_number"]
        malformed.append(("missing-field", missing))

        extra = LogicalOperation(**valid)
        object.__setattr__(extra, "unexpected", 1)
        malformed.append(("extra-field", extra))

        rejected_request = hashlib.sha256(b"malformed operation").hexdigest()
        for label, operation in malformed:
            with self.subTest(case=label), self.assertRaisesRegex(
                BudgetError, "logical-operation|LogicalOperation"
            ):
                run_mock_attempts(session, operation, rejected_request)
            self.assertEqual(calls, [])
            self.assertEqual(journal.read_bytes(), before)

        accepted_request = hashlib.sha256(b"accepted operation").hexdigest()
        result = run_mock_attempts(
            session,
            FROZEN_OPERATIONS[0],
            accepted_request,
        )
        self.assertEqual(result, {"mock": "response"})
        self.assertEqual(calls, [1, 1, 1])
        events = [json.loads(line) for line in journal.read_text().splitlines()]
        starts = [event for event in events if event["event"] == "attempt-start"]
        self.assertEqual([event["attempt"] for event in starts], [1, 2, 3])

        run_mock_attempts(session, FROZEN_OPERATIONS[1], accepted_request)
        self.assertEqual(calls, [1, 1, 1, 2])
        session.close()

    def test_concurrent_operation_refuses_without_consuming_sequence(self) -> None:
        entered = threading.Event()
        release = threading.Event()
        calls = []
        worker_errors = []

        def transport(operation, *_args):
            calls.append(operation.query_index)
            if operation == FROZEN_OPERATIONS[0]:
                entered.set()
                if not release.wait(timeout=5):
                    raise AssertionError("concurrency test release timed out")
            return {"mock": "response"}

        session = MockAdapterSession.create(
            self.manifest,
            self.authorization,
            git_root=self.git_root,
            credential_provider=lambda: "synthetic-marker",
            transport=transport,
        )
        request_hash = hashlib.sha256(b"concurrent request").hexdigest()

        def run_first():
            try:
                run_mock_attempts(session, FROZEN_OPERATIONS[0], request_hash)
            except BaseException as exc:
                worker_errors.append(exc)

        worker = threading.Thread(target=run_first)
        worker.start()
        self.assertTrue(entered.wait(timeout=5))
        with self.assertRaisesRegex(H1Refusal, "already in progress"):
            run_mock_attempts(session, FROZEN_OPERATIONS[0], request_hash)
        self.assertEqual(calls, [1])
        release.set()
        worker.join(timeout=5)
        self.assertFalse(worker.is_alive())
        self.assertEqual(worker_errors, [])

        run_mock_attempts(session, FROZEN_OPERATIONS[1], request_hash)
        self.assertEqual(calls, [1, 2])
        events = [
            json.loads(line)
            for line in (self.run_root / "attempts.jsonl").read_text().splitlines()
        ]
        first_starts = [
            event
            for event in events
            if event["event"] == "attempt-start" and event["query_index"] == 1
        ]
        self.assertEqual([event["attempt"] for event in first_starts], [1])
        session.close()

    def test_reentrant_operation_refuses_without_consuming_sequence(self) -> None:
        calls = []
        refusals = []
        request_hash = hashlib.sha256(b"reentrant request").hexdigest()
        session = None

        def transport(operation, *_args):
            calls.append(operation.query_index)
            if operation == FROZEN_OPERATIONS[0]:
                try:
                    run_mock_attempts(session, operation, request_hash)
                except H1Refusal as exc:
                    refusals.append(str(exc))
            return {"mock": "response"}

        session = MockAdapterSession.create(
            self.manifest,
            self.authorization,
            git_root=self.git_root,
            credential_provider=lambda: "synthetic-marker",
            transport=transport,
        )
        run_mock_attempts(session, FROZEN_OPERATIONS[0], request_hash)
        self.assertEqual(calls, [1])
        self.assertEqual(len(refusals), 1)
        self.assertIn("already in progress", refusals[0])

        run_mock_attempts(session, FROZEN_OPERATIONS[1], request_hash)
        self.assertEqual(calls, [1, 2])
        session.close()

    def test_post_transport_receipt_failures_permanently_stop_session(self) -> None:
        request_hash = hashlib.sha256(b"receipt failure request").hexdigest()
        original_append = AppendOnlyJournal.append

        for failed_event in ("attempt-finish", "partition-status"):
            with self.subTest(failed_event=failed_event):
                self._set_run_root(f"fail-{failed_event}")
                calls = {"transport": 0}

                def transport(*_args):
                    calls["transport"] += 1
                    return {"mock": "response"}

                session = MockAdapterSession.create(
                    self.manifest,
                    self.authorization,
                    git_root=self.git_root,
                    credential_provider=lambda: "synthetic-marker",
                    transport=transport,
                )
                marker = self.run_root / "H1_MOCK_CONSUMED"
                journal = self.run_root / "attempts.jsonl"
                marker_before = marker.read_bytes()

                def failing_append(journal_object, event):
                    if event["event"] == failed_event:
                        raise OSError(f"synthetic {failed_event} persistence failure")
                    return original_append(journal_object, event)

                with mock.patch.object(AppendOnlyJournal, "append", new=failing_append):
                    with self.assertRaisesRegex(OSError, "persistence failure"):
                        run_mock_attempts(
                            session,
                            FROZEN_OPERATIONS[0],
                            request_hash,
                        )
                journal_after_failure = journal.read_bytes()
                self.assertEqual(calls["transport"], 1)
                with self.assertRaisesRegex(H1Refusal, "permanently stopped"):
                    run_mock_attempts(
                        session,
                        FROZEN_OPERATIONS[0],
                        request_hash,
                    )
                self.assertEqual(calls["transport"], 1)
                self.assertEqual(marker.read_bytes(), marker_before)
                self.assertEqual(journal.read_bytes(), journal_after_failure)
                session.close()

    def test_terminal_http_400_is_not_retried(self) -> None:
        calls = {"count": 0}

        def transport(*_args):
            calls["count"] += 1
            raise HttpStatusError(400)

        session = MockAdapterSession.create(
            self.manifest,
            self.authorization,
            git_root=self.git_root,
            credential_provider=lambda: "synthetic-marker",
            transport=transport,
        )
        request_hash = hashlib.sha256(b"request").hexdigest()
        with self.assertRaises(HttpStatusError):
            run_mock_attempts(
                session,
                FROZEN_OPERATIONS[0],
                request_hash,
            )
        self.assertEqual(calls["count"], 1)
        with self.assertRaises(BudgetError):
            run_mock_attempts(session, FROZEN_OPERATIONS[0], request_hash)
        session.close()

    def test_closed_session_refuses_transport(self) -> None:
        calls = {"transport": 0}

        def transport(*_args):
            calls["transport"] += 1

        session = MockAdapterSession.create(
            self.manifest,
            self.authorization,
            git_root=self.git_root,
            credential_provider=lambda: "synthetic-marker",
            transport=transport,
        )
        session.close()
        with self.assertRaises(H1Refusal):
            run_mock_attempts(
                session,
                FROZEN_OPERATIONS[0],
                hashlib.sha256(b"request").hexdigest(),
            )
        self.assertEqual(calls["transport"], 0)

    def test_raw_socket_create_connection_and_dns_are_blocked(self) -> None:
        with self.assertRaisesRegex(AssertionError, "network forbidden"):
            socket.socket()
        with self.assertRaisesRegex(AssertionError, "network forbidden"):
            socket.create_connection(("127.0.0.1", 9))
        with self.assertRaisesRegex(AssertionError, "network forbidden"):
            socket.getaddrinfo("example.invalid", 443)

    def test_retry_classification(self) -> None:
        retryable = [
            TimeoutError(),
            ConnectionResetError(),
            TemporaryDnsFailure(),
            HttpStatusError(500),
            HttpStatusError(502),
            HttpStatusError(503),
            HttpStatusError(504),
        ]
        terminal = [
            HttpStatusError(400),
            HttpStatusError(408),
            HttpStatusError(429),
            HttpStatusError(501),
            ValueError(),
            ContractError("bad response"),
        ]
        self.assertTrue(all(is_retryable_error(exc) for exc in retryable))
        self.assertTrue(all(not is_retryable_error(exc) for exc in terminal))

    def test_operation_budget_order_identity_and_exhaustion(self) -> None:
        request_hash = hashlib.sha256(b"request").hexdigest()
        budget = OperationBudget(self.verified())
        with self.assertRaises(BudgetError):
            budget.begin_attempt(FROZEN_OPERATIONS[1], request_hash)
        budget.begin_attempt(FROZEN_OPERATIONS[0], request_hash)
        with self.assertRaises(BudgetError):
            budget.begin_attempt(FROZEN_OPERATIONS[0], hashlib.sha256(b"changed").hexdigest())
        budget.finish_success(FROZEN_OPERATIONS[0])
        for operation in FROZEN_OPERATIONS[1:]:
            budget.begin_attempt(operation, request_hash)
            budget.finish_success(operation)
        self.assertEqual(budget.completed_operations, 12)
        with self.assertRaises(BudgetError):
            budget.begin_attempt(FROZEN_OPERATIONS[-1], request_hash)

    def test_mock_response_contract_requires_explicit_extraction_and_columns(self) -> None:
        columns = tuple(f"fixture-column-{index}" for index in range(9))
        contract = MockResponseContract(
            extractor=lambda payload: payload["fixture_matrix"],
            fixture_columns=columns,
        )
        payload = {"fixture_matrix": [[float(index) for index in range(9)] for _ in range(2)]}
        rows = contract.validate(payload, expected_rows=2)
        self.assertEqual(len(rows), 2)
        with self.assertRaises(ContractError):
            contract.validate(payload, expected_rows=3)
        with self.assertRaises(ContractError):
            contract.validate({"fixture_matrix": [[0.0] * 8]}, expected_rows=1)
        with self.assertRaises(ContractError):
            contract.validate({"fixture_matrix": [[False] + [0.0] * 8]}, expected_rows=1)
        with self.assertRaises(ContractError):
            contract.validate({"fixture_matrix": [[float("nan")] + [0.0] * 8]}, expected_rows=1)


if __name__ == "__main__":
    unittest.main()
