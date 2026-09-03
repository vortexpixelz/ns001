"""H1-only offline structural scaffolding for NS-001 E0.

This module has no executable entry point and no live JHTDB client.  Every
adapter operation is explicitly injected by an offline test.  The live adapter
always refuses while client-source evidence remains unresolved.
"""

from __future__ import annotations

import errno
import fcntl
import hashlib
import json
import math
import os
import socket
import subprocess
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence


CANONICAL_COMMIT = "0393315223df8ed90f20f0c821508cc98bea08d1"
FROZEN_PREREGISTRATION_SHA256 = (
    "a2a8523c065d4d41155aa29d367c888d49ab3032f6075b8cebbd2475ff1efd78"
)
FROZEN_PREREGISTRATION_PATH = (
    "preregistrations/e0/"
    "NS-001_E0_STRIDE_REFINEMENT_PREREG_FROZEN_2026-09-02.md"
)
FROZEN_SIDECAR_PATH = FROZEN_PREREGISTRATION_PATH.removesuffix(".md") + ".sha256"
H1_MANIFEST_SCHEMA = "ns001.h1.mock-manifest.v1"
H1_AUTHORIZATION_SCHEMA = "ns001.h1.mock-authorization-fixture.v1"
MAX_RETRIES = 2
RETRYABLE_HTTP_STATUSES = frozenset({500, 502, 503, 504})
LOGICAL_OPERATION_FIELDS = (
    "query_index",
    "stride",
    "partition_number",
    "first_flattened_index",
    "final_flattened_index",
    "requested_point_count",
)
_CONTEXT_SEAL = object()
_SESSION_SEAL = object()
_UNSUPPLIED = object()
_ISSUED_CONTEXTS: dict[int, "VerifiedContext"] = {}


class H1Refusal(RuntimeError):
    """A structural precondition failed closed."""


class LiveAdapterUnavailable(H1Refusal):
    """No live adapter is permitted during H1."""


class ContractError(H1Refusal):
    """A mock-only response contract was violated."""


class BudgetError(H1Refusal):
    """A logical operation exceeded or violated the frozen budget."""


class TemporaryDnsFailure(OSError):
    """Explicitly classified temporary DNS failure for offline fixtures."""


class HttpStatusError(RuntimeError):
    """HTTP status surfaced by an injected mock transport."""

    def __init__(self, status: int):
        self.status = status
        super().__init__(f"HTTP status {status}")


@dataclass(frozen=True)
class LogicalOperation:
    query_index: int
    stride: int
    partition_number: int
    first_flattened_index: int
    final_flattened_index: int
    requested_point_count: int

    def as_dict(self) -> dict[str, int]:
        return {
            "query_index": self.query_index,
            "stride": self.stride,
            "partition_number": self.partition_number,
            "first_flattened_index": self.first_flattened_index,
            "final_flattened_index": self.final_flattened_index,
            "requested_point_count": self.requested_point_count,
        }


def _validate_logical_operation_entry(entry: object) -> None:
    if (
        not isinstance(entry, Mapping)
        or any(type(key) is not str for key in entry)
        or set(entry) != set(LOGICAL_OPERATION_FIELDS)
    ):
        raise H1Refusal(
            "logical-operation entry must contain exactly the six required fields"
        )
    for field in LOGICAL_OPERATION_FIELDS:
        if type(entry[field]) is not int:
            raise H1Refusal(f"logical-operation field {field} must be an exact int")


def _build_operations() -> tuple[LogicalOperation, ...]:
    partitions = {
        16: (262_144,),
        8: (2_000_000, 97_152),
        4: (2_000_000,) * 8 + (777_216,),
    }
    operations: list[LogicalOperation] = []
    query_index = 0
    for stride in (16, 8, 4):
        first = 0
        for partition_number, count in enumerate(partitions[stride], start=1):
            query_index += 1
            operations.append(
                LogicalOperation(
                    query_index=query_index,
                    stride=stride,
                    partition_number=partition_number,
                    first_flattened_index=first,
                    final_flattened_index=first + count - 1,
                    requested_point_count=count,
                )
            )
            first += count
    return tuple(operations)


FROZEN_OPERATIONS = _build_operations()


def canonical_json_bytes(value: Any) -> bytes:
    """Return the single H1 manifest hashing representation."""

    try:
        text = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise H1Refusal("value is not canonical JSON") from exc
    return text.encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_content_sha256(content: Mapping[str, Any]) -> str:
    return sha256_bytes(canonical_json_bytes(content))


def _is_within(path: Path, parent: Path) -> bool:
    return path == parent or parent in path.parents


def _absolute_string_path(value: object, field: str) -> Path:
    if not isinstance(value, str) or not value:
        raise H1Refusal(f"{field} must be a nonempty absolute path string")
    path = Path(value)
    if not path.is_absolute():
        raise H1Refusal(f"{field} must be absolute")
    return path


def _running_source_path() -> Path:
    source = Path(__file__)
    if not source.is_absolute():
        raise H1Refusal("associated H1 module source path must be absolute")
    lexical = Path(os.path.abspath(source))
    try:
        resolved = source.resolve(strict=True)
    except OSError as exc:
        raise H1Refusal("associated H1 module source is unavailable") from exc
    if lexical != resolved or not resolved.is_file():
        raise H1Refusal("associated H1 module source must not use a symlink alias")
    return resolved


# These values describe the source file associated with this imported module.
# H1 does not claim that Python compiled or loaded these particular bytes.
_LOADED_SOURCE_PATH = _running_source_path()
_LOADED_SOURCE_SHA256 = sha256_file(_LOADED_SOURCE_PATH)


def _verify_running_source(bound_path: Path, bound_digest: str) -> None:
    """Check manifest, initialization-time, and current source-file consistency."""

    current_path = _running_source_path()
    current_digest = sha256_file(current_path)
    if bound_path != _LOADED_SOURCE_PATH or bound_path != current_path:
        raise H1Refusal("runner source path disagrees with the initialization-time or current source file")
    if bound_digest != _LOADED_SOURCE_SHA256 or bound_digest != current_digest:
        raise H1Refusal("runner source digest disagrees with the initialization-time or current source file")


def _scrubbed_git_environment() -> dict[str, str]:
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
    environment.update(
        {
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_TERMINAL_PROMPT": "0",
            "GCM_INTERACTIVE": "Never",
            "SSH_ASKPASS_REQUIRE": "never",
        }
    )
    return environment


def _run_integrity_git(path: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
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
            "credential.helper=",
            "-C",
            str(path),
            *arguments,
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
        stdin=subprocess.DEVNULL,
        env=_scrubbed_git_environment(),
    )


def _git_toplevel(path: Path, field: str) -> Path:
    try:
        completed = _run_integrity_git(path, "rev-parse", "--show-toplevel")
        value = completed.stdout.strip()
        if not value:
            raise H1Refusal(f"{field} has no Git working-tree top level")
        return Path(value).resolve(strict=True)
    except (OSError, subprocess.SubprocessError) as exc:
        raise H1Refusal(f"{field} is not a Git working tree") from exc


def _git_head(git_root: Path) -> str:
    try:
        completed = _run_integrity_git(
            git_root, "rev-parse", "--verify", "HEAD^{commit}"
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise H1Refusal("git_root has no resolvable HEAD commit") from exc
    return _require_commit(completed.stdout.strip(), "source_head_commit")


def _validated_git_root(git_root: Path, package_root: Path) -> Path:
    supplied = Path(git_root)
    if not supplied.is_absolute():
        raise H1Refusal("git_root must be absolute")
    lexical = Path(os.path.abspath(supplied))
    try:
        resolved = supplied.resolve(strict=True)
    except OSError as exc:
        raise H1Refusal("git_root does not exist") from exc
    if lexical != resolved:
        raise H1Refusal("git_root must not use a symlink alias")
    if not resolved.is_dir() or _git_toplevel(resolved, "git_root") != resolved:
        raise H1Refusal("git_root must be the actual Git working-tree top level")
    if _git_toplevel(package_root, "package_root") != resolved:
        raise H1Refusal("package_root belongs to an unrelated Git working tree")
    return resolved


def validate_roots(package_root_value: object, run_root_value: object, git_root: Path) -> tuple[Path, Path]:
    """Resolve explicit roots and reject overlap, aliases, and Git-tree runs."""

    package_input = _absolute_string_path(package_root_value, "package_root")
    run_input = _absolute_string_path(run_root_value, "run_root")
    package_root = package_input.resolve(strict=True)
    if Path(os.path.abspath(package_input)) != package_root:
        raise H1Refusal("package_root must not use a symlink alias")
    if not package_root.is_dir():
        raise H1Refusal("package_root is not a directory")
    git_resolved = _validated_git_root(git_root, package_root)

    if run_input.exists():
        if run_input.is_symlink():
            raise H1Refusal("run_root must not be a symlink")
        run_root = run_input.resolve(strict=True)
    else:
        try:
            parent = run_input.parent.resolve(strict=True)
        except OSError as exc:
            raise H1Refusal("run_root parent must already exist") from exc
        run_root = parent / run_input.name

    if _is_within(run_root, git_resolved):
        raise H1Refusal("run_root must be outside the Git working tree")
    if _is_within(run_root, package_root) or _is_within(package_root, run_root):
        raise H1Refusal("package_root and run_root must not overlap")
    return package_root, run_root


def _require_hash(value: object, field: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise H1Refusal(f"{field} must be a SHA-256 hex digest")
    try:
        int(value, 16)
    except ValueError as exc:
        raise H1Refusal(f"{field} must be a SHA-256 hex digest") from exc
    return value.lower()


def _require_commit(value: object, field: str) -> str:
    if not isinstance(value, str) or len(value) != 40:
        raise H1Refusal(f"{field} must be a 40-character Git commit ID")
    try:
        int(value, 16)
    except ValueError as exc:
        raise H1Refusal(f"{field} must be a 40-character Git commit ID") from exc
    return value.lower()


def _require_run_id(value: object) -> str:
    if (
        not isinstance(value, str)
        or not value
        or len(value) > 128
        or any(character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-" for character in value)
    ):
        raise H1Refusal("run_id must use 1-128 ASCII letters, digits, dot, underscore, or hyphen")
    return value


def _verify_sidecar(sidecar: Path, preregistration: Path) -> None:
    fields = sidecar.read_text(encoding="utf-8").strip().split()
    if fields != [FROZEN_PREREGISTRATION_SHA256, preregistration.name]:
        raise H1Refusal("frozen preregistration sidecar content mismatch")


@dataclass(frozen=True, slots=True, init=False)
class VerifiedContext:
    """Immutable H1 source-file and structural checks issued by the integrity gate."""

    manifest_hash: str
    run_id: str
    package_root: Path
    run_root: Path
    operations: tuple[LogicalOperation, ...]
    operation_specs_hash: str
    scientific_base_commit: str
    source_head_commit: str
    runner_path: Path  # Source file associated with the imported H1 module.
    runner_sha256: str  # Digest of that associated source file.
    mock_only: bool
    _seal: object

    def __init__(self, *_args: object, **_kwargs: object) -> None:
        raise H1Refusal("VerifiedContext can only be issued by verify_h1_context")

    @classmethod
    def _issue(
        cls,
        seal: object,
        *,
        manifest_hash: str,
        run_id: str,
        package_root: Path,
        run_root: Path,
        operations: tuple[LogicalOperation, ...],
        scientific_base_commit: str,
        source_head_commit: str,
        runner_path: Path,
        runner_sha256: str,
    ) -> "VerifiedContext":
        if seal is not _CONTEXT_SEAL:
            raise H1Refusal("invalid verified-context issuer")
        context = object.__new__(cls)
        object.__setattr__(context, "manifest_hash", manifest_hash)
        object.__setattr__(context, "run_id", run_id)
        object.__setattr__(context, "package_root", package_root)
        object.__setattr__(context, "run_root", run_root)
        object.__setattr__(context, "operations", operations)
        object.__setattr__(
            context,
            "operation_specs_hash",
            sha256_bytes(canonical_json_bytes([operation.as_dict() for operation in operations])),
        )
        object.__setattr__(context, "scientific_base_commit", scientific_base_commit)
        object.__setattr__(context, "source_head_commit", source_head_commit)
        object.__setattr__(context, "runner_path", runner_path)
        object.__setattr__(context, "runner_sha256", runner_sha256)
        object.__setattr__(context, "mock_only", True)
        object.__setattr__(context, "_seal", _CONTEXT_SEAL)
        _ISSUED_CONTEXTS[id(context)] = context
        return context

    def binding_record(self) -> dict[str, object]:
        return {
            "manifest_content_sha256": self.manifest_hash,
            "run_id": self.run_id,
            "package_root": str(self.package_root),
            "run_root": str(self.run_root),
            "operation_specs_sha256": self.operation_specs_hash,
            "scientific_base_commit": self.scientific_base_commit,
            "source_head_commit": self.source_head_commit,
        }


def _require_verified_context(context: object) -> VerifiedContext:
    if (
        type(context) is not VerifiedContext
        or _ISSUED_CONTEXTS.get(id(context)) is not context
        or context._seal is not _CONTEXT_SEAL
        or context.mock_only is not True
    ):
        raise H1Refusal("an immutable context issued by the H1 integrity gate is required")
    return context


def verify_h1_context(
    manifest: Mapping[str, Any],
    authorization_fixture: Mapping[str, Any],
    *,
    git_root: Path,
) -> VerifiedContext:
    """Verify in-memory H1 fixtures and bound files without invoking callbacks."""

    if authorization_fixture.get("schema") != H1_AUTHORIZATION_SCHEMA:
        raise H1Refusal("authorization fixture is not H1 mock-only")

    content = manifest.get("content")
    if not isinstance(content, Mapping):
        raise H1Refusal("canonical manifest content is required")
    if content.get("schema") != H1_MANIFEST_SCHEMA or content.get("status") != "DRAFT_H1_OFFLINE_ONLY":
        raise H1Refusal("manifest is not an H1 offline draft")
    if content.get("mock_only") is not True or authorization_fixture.get("mock_only") is not True:
        raise H1Refusal("H1 fixtures must be marked mock_only")
    scientific_base_commit = _require_commit(
        content.get("scientific_base_commit"), "scientific_base_commit"
    )
    if scientific_base_commit != CANONICAL_COMMIT:
        raise H1Refusal("canonical scientific base commit mismatch")
    source_head_commit = _require_commit(
        content.get("source_head_commit"), "source_head_commit"
    )
    run_id = _require_run_id(content.get("run_id"))

    package_root, run_root = validate_roots(
        content.get("package_root"), content.get("run_root"), git_root
    )
    actual_source_head = _git_head(package_root)
    if source_head_commit != actual_source_head:
        raise H1Refusal("manifest source HEAD does not match the Git working tree")
    if authorization_fixture.get("run_id") != run_id:
        raise H1Refusal("authorization run_id mismatch")
    if authorization_fixture.get("package_root") != str(package_root):
        raise H1Refusal("authorization package_root mismatch")
    if authorization_fixture.get("run_root") != str(run_root):
        raise H1Refusal("authorization run_root mismatch")

    manifest_operations = content.get("logical_operations")
    if type(manifest_operations) is not list:
        raise H1Refusal("logical_operations must be a list")
    for entry in manifest_operations:
        _validate_logical_operation_entry(entry)
    expected_operations = [operation.as_dict() for operation in FROZEN_OPERATIONS]
    if manifest_operations != expected_operations:
        raise H1Refusal("logical-operation manifest mismatch")

    actual_manifest_hash = manifest_content_sha256(content)
    expected_manifest_hash = _require_hash(
        manifest.get("manifest_content_sha256"), "manifest_content_sha256"
    )
    if actual_manifest_hash != expected_manifest_hash:
        raise H1Refusal("manifest-content hash mismatch")
    if authorization_fixture.get("manifest_content_sha256") != expected_manifest_hash:
        raise H1Refusal("authorization manifest hash mismatch")

    artifacts = content.get("artifacts")
    if not isinstance(artifacts, Mapping) or set(artifacts) != {"code", "preregistration", "sidecar"}:
        raise H1Refusal("canonical content must bind exactly the verified artifacts")
    artifact_rows: list[tuple[str, str, str]] = []
    for label in ("code", "preregistration", "sidecar"):
        binding = artifacts.get(label)
        if not isinstance(binding, Mapping) or set(binding) != {"path", "sha256"}:
            raise H1Refusal(f"{label} artifact binding is malformed")
        relative = binding.get("path")
        if not isinstance(relative, str) or not relative:
            raise H1Refusal(f"{label} artifact path is required")
        artifact_rows.append((label, relative, _require_hash(binding.get("sha256"), f"{label}.sha256")))

    code_rel = artifact_rows[0][1]
    prereg_rel = artifact_rows[1][1]
    sidecar_rel = artifact_rows[2][1]
    if prereg_rel != FROZEN_PREREGISTRATION_PATH or sidecar_rel != FROZEN_SIDECAR_PATH:
        raise H1Refusal("frozen preregistration paths mismatch")

    resolved_files: list[tuple[str, Path, str]] = []
    for label, relative, expected_hash in artifact_rows:
        lexical_candidate = Path(os.path.abspath(package_root / relative))
        candidate = (package_root / relative).resolve(strict=True)
        if not _is_within(candidate, package_root) or not candidate.is_file():
            raise H1Refusal(f"bound {label} path escapes package_root")
        if label == "code" and lexical_candidate != candidate:
            raise H1Refusal("bound runner artifact must not use a symlink alias")
        resolved_files.append((label, candidate, expected_hash))

    running_source = _running_source_path()
    bound_code = resolved_files[0][1]
    if bound_code != running_source:
        raise H1Refusal(
            "manifest-bound runner source is not the source file associated with this imported module"
        )
    try:
        running_relative = running_source.relative_to(package_root).as_posix()
    except ValueError as exc:
        raise H1Refusal("associated H1 module source is outside package_root") from exc
    if code_rel != running_relative:
        raise H1Refusal("runner artifact path does not identify the associated module source")

    bound_code_digest = artifact_rows[0][2]
    _verify_running_source(bound_code, bound_code_digest)

    for label, candidate, expected_hash in resolved_files:
        actual_hash = sha256_file(candidate)
        if actual_hash != expected_hash:
            raise H1Refusal(f"{label} hash mismatch")
    preregistration = resolved_files[1][1]
    if sha256_file(preregistration) != FROZEN_PREREGISTRATION_SHA256:
        raise H1Refusal("preregistration is not the frozen artifact")
    _verify_sidecar(resolved_files[2][1], preregistration)

    return VerifiedContext._issue(
        _CONTEXT_SEAL,
        manifest_hash=actual_manifest_hash,
        run_id=run_id,
        package_root=package_root,
        run_root=run_root,
        operations=FROZEN_OPERATIONS,
        scientific_base_commit=scientific_base_commit,
        source_head_commit=source_head_commit,
        runner_path=bound_code,
        runner_sha256=bound_code_digest,
    )


class LiveGetDataAdapter:
    """Permanent H1 fail-closed placeholder; it never invokes callbacks."""

    def __init__(self, credential_provider: Callable[[], object], transport: Callable[..., object]):
        self._credential_provider = credential_provider
        self._transport = transport

    def fetch(self, *_args: object, **_kwargs: object) -> object:
        raise LiveAdapterUnavailable(
            "live GetData is unavailable until pinned client-source evidence is approved"
        )


class MockAdapterSession:
    """The guarded, budgeted mock-transport API provided by this H1 scaffold."""

    def __init__(self, *_args: object, **_kwargs: object) -> None:
        raise H1Refusal("MockAdapterSession must be created by its H1 integrity gate")

    @classmethod
    def create(
        cls,
        manifest: Mapping[str, Any],
        authorization_fixture: Mapping[str, Any],
        *,
        git_root: Path,
        credential_provider: Callable[[], object],
        transport: Callable[[LogicalOperation, str, object], object],
        context: object = _UNSUPPLIED,
        guard: object = _UNSUPPLIED,
        journal: object = _UNSUPPLIED,
        budget: object = _UNSUPPLIED,
    ) -> "MockAdapterSession":
        if cls is not MockAdapterSession:
            raise H1Refusal("mock session subclass substitution is forbidden")
        if any(value is not _UNSUPPLIED for value in (context, guard, journal, budget)):
            raise H1Refusal("caller-supplied context, guard, journal, or budget is forbidden")
        if not callable(credential_provider) or not callable(transport):
            raise H1Refusal("mock credential provider and transport must be callable")
        verified = verify_h1_context(manifest, authorization_fixture, git_root=git_root)
        verified = _require_verified_context(verified)
        owned_guard = RunGuard(verified)
        owned_guard.acquire()
        owned_journal: AppendOnlyJournal | None = None
        try:
            owned_journal = AppendOnlyJournal(verified)
            _verify_running_source(verified.runner_path, verified.runner_sha256)
            credential_marker = credential_provider()
            session = object.__new__(cls)
            session.context = verified
            session.__credential_marker = credential_marker
            session.__transport = transport
            session.__guard = owned_guard
            session.__journal = owned_journal
            session.__budget = OperationBudget(verified)
            session.__operation_lock = threading.Lock()
            session.__closed = False
            session.__poisoned = False
            session.__seal = _SESSION_SEAL
            session.__assert_bindings()
            return session
        except BaseException:
            if owned_journal is not None:
                owned_journal.close()
            owned_guard.release()
            raise

    def execute(self, operation: LogicalOperation, request_identity: str) -> object:
        """Run one frozen operation with budget checks preceding every callback."""

        if not self.__operation_lock.acquire(blocking=False):
            raise H1Refusal("another mock operation is already in progress")
        try:
            return self.__execute_exclusive(operation, request_identity)
        finally:
            self.__operation_lock.release()

    def __execute_exclusive(self, operation: LogicalOperation, request_identity: str) -> object:
        self.__require_active()
        while True:
            _verify_running_source(
                self.context.runner_path,
                self.context.runner_sha256,
            )
            attempt = self.__budget.begin_attempt(operation, request_identity)
            try:
                self.__journal.append(
                    {
                        "event": "attempt-start",
                        "query_index": operation.query_index,
                        "attempt": attempt,
                        "request_identity": request_identity,
                    }
                )
            except BaseException:
                self.__poison()
                raise

            try:
                value = self.__transport(
                    operation,
                    request_identity,
                    self.__credential_marker,
                )
            except BaseException as transport_error:
                retryable = is_retryable_error(transport_error)
                will_retry = retryable and attempt <= MAX_RETRIES
                try:
                    self.__journal.append(
                        {
                            "event": "attempt-finish",
                            "query_index": operation.query_index,
                            "attempt": attempt,
                            "status": "retryable-failure" if will_retry else "terminal-failure",
                            "error_type": type(transport_error).__name__,
                            "request_identity": request_identity,
                        }
                    )
                except BaseException:
                    self.__poison()
                    raise
                if will_retry:
                    continue
                self.__budget.finish_failure(operation)
                try:
                    self.__journal.append(
                        {
                            "event": "partition-status",
                            "query_index": operation.query_index,
                            "status": "failure",
                            "request_identity": request_identity,
                        }
                    )
                except BaseException:
                    self.__poison()
                    raise
                raise

            try:
                self.__journal.append(
                    {
                        "event": "attempt-finish",
                        "query_index": operation.query_index,
                        "attempt": attempt,
                        "status": "success",
                        "request_identity": request_identity,
                    }
                )
                self.__journal.append(
                    {
                        "event": "partition-status",
                        "query_index": operation.query_index,
                        "status": "success",
                        "request_identity": request_identity,
                    }
                )
                self.__budget.finish_success(operation)
            except BaseException:
                self.__poison()
                raise
            return value

    def close(self) -> None:
        if not self.__operation_lock.acquire(blocking=False):
            raise H1Refusal("cannot close while a mock operation is in progress")
        try:
            if not self.__closed:
                self.__closed = True
                self.__journal.close()
                self.__guard.release()
        finally:
            self.__operation_lock.release()

    def __assert_bindings(self) -> None:
        context = _require_verified_context(self.context)
        if (
            self.__seal is not _SESSION_SEAL
            or self.__guard.context is not context
            or self.__journal.context is not context
            or self.__budget._context is not context
            or self.__guard.lock_path != context.run_root.parent / f".{context.run_root.name}.h1-lock"
            or self.__guard.marker_path != context.run_root / "H1_MOCK_CONSUMED"
            or self.__journal.path != context.run_root / "attempts.jsonl"
            or tuple(context.operations) != FROZEN_OPERATIONS
        ):
            raise H1Refusal("mock session components do not match the verified context")

    def __require_active(self) -> None:
        self.__assert_bindings()
        if self.__poisoned:
            raise H1Refusal("mock session permanently stopped after receipt persistence failure")
        if self.__closed or not self.__guard.active:
            raise H1Refusal("mock session has no active exclusive run guard")

    def __poison(self) -> None:
        if self.__poisoned:
            return
        self.__poisoned = True
        self.__closed = True
        try:
            self.__journal.close()
        finally:
            self.__guard.release()


class RunGuard:
    """Create an exclusive, durable H1 mock run marker without overwriting."""

    def __init__(self, context: VerifiedContext):
        self.context = _require_verified_context(context)
        self.lock_path = context.run_root.parent / f".{context.run_root.name}.h1-lock"
        self.marker_path = context.run_root / "H1_MOCK_CONSUMED"
        self._fd: int | None = None

    def acquire(self) -> None:
        if self._fd is not None:
            raise H1Refusal("run guard already acquired")
        if self.context.run_root.exists() or self.lock_path.exists():
            raise H1Refusal("existing output or run marker refuses rerun")
        try:
            fd = os.open(self.lock_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError as exc:
            raise H1Refusal("exclusive run lock already exists") from exc
        self._fd = fd
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            lock_record = self.context.binding_record() | {"kind": "H1_MOCK_LOCK"}
            os.write(fd, canonical_json_bytes(lock_record) + b"\n")
            os.fsync(fd)
            self.context.run_root.mkdir(mode=0o700)
            marker_fd = os.open(
                self.marker_path,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o600,
            )
            try:
                marker_record = self.context.binding_record() | {
                    "kind": "H1_MOCK_CONSUMED",
                    "production_authorization": False,
                    "production_receipt": False,
                }
                os.write(marker_fd, canonical_json_bytes(marker_record) + b"\n")
                os.fsync(marker_fd)
            finally:
                os.close(marker_fd)
        except BaseException:
            os.close(fd)
            self._fd = None
            raise

    def release(self) -> None:
        if self._fd is not None:
            fcntl.flock(self._fd, fcntl.LOCK_UN)
            os.close(self._fd)
            self._fd = None

    @property
    def active(self) -> bool:
        return self._fd is not None


class AppendOnlyJournal:
    """Write newline-delimited H1 mock events with append and fsync."""

    def __init__(self, context: VerifiedContext):
        self.context = _require_verified_context(context)
        path = context.run_root / "attempts.jsonl"
        try:
            self._fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError as exc:
            raise H1Refusal("journal already exists") from exc
        self.path = path

    def append(self, event: Mapping[str, Any]) -> None:
        record = dict(event)
        record.update(self.context.binding_record())
        record["h1_mock"] = True
        record["production_receipt"] = False
        payload = canonical_json_bytes(record) + b"\n"
        written = 0
        while written < len(payload):
            count = os.write(self._fd, payload[written:])
            if count <= 0:
                raise OSError("short append-only journal write")
            written += count
        os.fsync(self._fd)

    def close(self) -> None:
        os.close(self._fd)


def is_retryable_error(exc: BaseException) -> bool:
    if isinstance(exc, HttpStatusError):
        return exc.status in RETRYABLE_HTTP_STATUSES
    if isinstance(exc, TemporaryDnsFailure):
        return True
    if isinstance(exc, (TimeoutError, ConnectionResetError)):
        return True
    return isinstance(exc, OSError) and exc.errno in {
        errno.ETIMEDOUT,
        errno.ECONNRESET,
        socket.EAI_AGAIN,
    }


class OperationBudget:
    """Enforce one sequential pass through the twelve frozen operations."""

    def __init__(self, context: VerifiedContext):
        verified = _require_verified_context(context)
        if tuple(verified.operations) != FROZEN_OPERATIONS:
            raise BudgetError("operation budget must exactly match the frozen plan")
        self._context = verified
        self._next = 0
        self._attempts: dict[int, int] = {}
        self._request_hashes: dict[int, str] = {}
        self._terminal_failure = False

    def begin_attempt(self, operation: LogicalOperation, request_identity: str) -> int:
        self._validate_operation(operation)
        if self._terminal_failure:
            raise BudgetError("logical-operation budget stopped after terminal failure")
        if self._next >= len(FROZEN_OPERATIONS):
            raise BudgetError("logical-operation budget exhausted")
        expected = FROZEN_OPERATIONS[self._next]
        if operation != expected:
            raise BudgetError("logical operations must execute once in frozen order")
        request_hash = _require_hash(request_identity, "request_identity")
        prior_hash = self._request_hashes.setdefault(operation.query_index, request_hash)
        if prior_hash != request_hash:
            raise BudgetError("retry request identity changed")
        attempts = self._attempts.get(operation.query_index, 0) + 1
        if attempts > 1 + MAX_RETRIES:
            raise BudgetError("retry budget exhausted")
        self._attempts[operation.query_index] = attempts
        return attempts

    def finish_success(self, operation: LogicalOperation) -> None:
        self._validate_operation(operation)
        if self._next >= len(FROZEN_OPERATIONS) or operation != FROZEN_OPERATIONS[self._next]:
            raise BudgetError("cannot finish an unbudgeted operation")
        self._next += 1

    def finish_failure(self, operation: LogicalOperation) -> None:
        self._validate_operation(operation)
        if self._next >= len(FROZEN_OPERATIONS) or operation != FROZEN_OPERATIONS[self._next]:
            raise BudgetError("cannot fail an unbudgeted operation")
        self._terminal_failure = True

    @staticmethod
    def _validate_operation(operation: object) -> None:
        if type(operation) is not LogicalOperation:
            raise BudgetError("logical operation must use the exact LogicalOperation type")
        try:
            _validate_logical_operation_entry(vars(operation))
        except H1Refusal as exc:
            raise BudgetError(str(exc)) from exc

    @property
    def completed_operations(self) -> int:
        return self._next


def run_mock_attempts(
    session: MockAdapterSession,
    operation: LogicalOperation,
    request_identity: str,
) -> object:
    """Use the session-owned budget and receipt path; never interpret values."""

    if type(session) is not MockAdapterSession:
        raise H1Refusal("a guarded H1 mock session is required")
    return session.execute(operation, request_identity)


@dataclass(frozen=True)
class MockResponseContract:
    """Fixture-defined extraction and columns; never production evidence."""

    extractor: Callable[[object], Sequence[Sequence[object]]]
    fixture_columns: tuple[str, ...]

    def validate(self, payload: object, *, expected_rows: int) -> tuple[tuple[float, ...], ...]:
        if not callable(self.extractor) or len(self.fixture_columns) != 9:
            raise ContractError("mock fixture must explicitly define nine columns")
        rows = self.extractor(payload)
        if len(rows) != expected_rows:
            raise ContractError("mock row count mismatch")
        validated: list[tuple[float, ...]] = []
        for row in rows:
            if len(row) != len(self.fixture_columns):
                raise ContractError("mock column count mismatch")
            values: list[float] = []
            for value in row:
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    raise ContractError("mock value is not numeric")
                number = float(value)
                if not math.isfinite(number):
                    raise ContractError("mock value is nonfinite")
                values.append(number)
            validated.append(tuple(values))
        return tuple(validated)
