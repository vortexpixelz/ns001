# NS-001 H2A2 handoff-mechanism selection v0.1

## Basis, scope and precedence

Preparation branch: `codex/e0-h2-preparation`.
Starting HEAD: `a90a6092c4de6a752de40d9b9ae163334c27a0ed`; working tree clean.
This document freezes **LINUX SEALED MEMFD HANDOFF**, profile
`ns001.h2a2.sealed-memfd.v1`, for the first future synthetic implementation slice.
It resolves B1 from `NS-001_H2A2_SNAPSHOT_HANDOFF_ACCEPTANCE_REVIEW_v0.1.md`.
The acceptance specification and review are pinned at starting HEAD in this directory.
They are preserved unchanged. This document is a prospective mechanism contract, not
implementation, test results, runtime assurance or permission to execute the next circuit.

The existing exact source/manifest/root rules, F/M/S constants, canonical serialization C,
ordered acquisition refusals and historical limitations remain applicable. The only payload
is `source.bin`, exactly `61 62 63`, length 3, SHA-256 F:
`ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`.
M is `4a9ebe2c4e275600d9a6c7864bb14c3d5a4c0b6a7c8bbf88193fc48f76affce0`;
S is `0ae1c30f2568188390fe05d092609eb122f3bee16c48f41fae9fe3f08e6ba432`.
No real scientific source replaces this fixture.

Explicit refinement of the abstract contract: the originally acquired buffer and the
memfd are distinct objects. Source validation authorizes one copy, not delivery. Successful
snapshot/handoff finalization occurs only after validating and sealing that copy and checking
it again. The same-object rule then binds that finalized memfd through both observations.
It does not assert that a file, a byte buffer and a memfd are one object. M/S remain logical
content identities; only the payload goes in memfd. The fixed canonical manifest is retained
by the validator, not reopened or interpreted by consumer/observer. The new role results
and mechanism evidence below refine the older consumer result profile explicitly; the old
four-field content tuple is reconstructed and checked by the validator. No historical
receipt is relabelled, edited or silently extended.

## 1. Frozen Linux primitive and lifecycle contract

All constants are symbolic platform definitions, never guessed integer values. No runtime
capability probe was performed in this circuit. The following is a future ordered procedure.

1. A single-threaded trusted harness allocates exclusive synthetic R, walks its absolute
   components through directory descriptors using `openat` with `O_DIRECTORY | O_NOFOLLOW |
   O_CLOEXEC | O_RDONLY`, and retains the final directory handle. No symlink component,
   alternate lexical R, filesystem root or alternate directory is accepted. Bind R by that
   live handle and `fstat` device/inode; the supplied handle must come from this acquisition.
   Descriptor-relative metadata/listing must establish exactly the two permitted regular,
   readable, single-link files. Open only those two with `O_RDONLY | O_NOFOLLOW | O_CLOEXEC |
   O_NONBLOCK` relative to R; recheck type/link count before reading. This avoids blocking
   on a substituted FIFO. The harness controls all mutation checkpoints and holds exclusive
   ownership during acquisition. Before/after checks detect scheduled changes, not hostile
   concurrency. ROOT_UNSTABLE refuses missing control or observed acquisition changes.
2. Validate manifest, source length and F under the existing contract. Retain the exact
   acquired bytes in a private immutable buffer; close acquisition handles after their
   final checks. No pathname-based source/manifest reopen is allowed after this success,
   including `/proc/.../fd` and `/dev/fd` alternatives. The later consumer never sees R.
3. Call `memfd_create` once, debug name `ns001-h2a2-handoff`, flags exactly
   `MFD_ALLOW_SEALING | MFD_CLOEXEC`. No huge pages, explicit executable flag, alternate
   backend or normal temporary-file fallback. Require a regular-file descriptor, size 0,
   close-on-exec set and initial `F_GET_SEALS` equal to 0. Record the creator handle privately
   as A and retain it until the circuit finishes. Type derives from witnessed creation,
   not from its debug name or filesystem metadata alone. [memfd_create documentation](https://man7.org/linux/man-pages/man2/memfd_create.2.html)
4. Copy exactly the validated three bytes with a single `pwrite(A, buffer, 0)` operation.
   Require return count 3; error or short write refuses without repair, completion loop,
   retry or another memfd. There is no mapping, asynchronous I/O or other writer. Require
   `fstat` length 3; independently read at offset 0 and recompute F before sealing.
5. Define Q = `F_SEAL_WRITE | F_SEAL_GROW | F_SEAL_SHRINK | F_SEAL_SEAL`.
   Apply Q in **one** `fcntl(A, F_ADD_SEALS, Q)` call, require success, then require
   `fcntl(A, F_GET_SEALS) == Q`, exactly, not merely a subset check. Q is the minimum
   selected set for content/length immutability and frozen seal state. No replacement
   with `F_SEAL_FUTURE_WRITE`. No writable shared mapping may exist; the positive path
   never creates any mapping. Seal application failure ends the attempt; do not unmap
   and retry to turn a failed candidate into success. [Linux sealing contract](https://man7.org/linux/man-pages/man2/F_GET_SEALS.2const.html)
6. Recheck sealed A's length, F and Q. Only now finalize the protected payload object and
   bind it to the successful validation event. Retain canonical manifest/root metadata
   privately with the frozen S; do not write metadata into the three-byte memfd.
7. Create C and O by two `fcntl(A, F_DUPFD_CLOEXEC, 0)` operations, directly from A.
   They are separate live descriptors to the same object; no fork, process transfer,
   socket or pathname reopen. Keep A, C and O open concurrently through all checks.
   Duplicated handles share the open-file description; close-on-exec is required on each.
   [Descriptor duplication](https://man7.org/linux/man-pages/man2/F_DUPFD.2const.html)
8. All verification/consumer/observer reads use one bounded `pread(fd, 4, 0)`, require
   exactly three returned bytes and `fstat` size 3. Short reads/errors refuse; no read-loop
   repair. `pread`/`pwrite` use explicit offsets and do not move the shared offset. No
   `read`, seek-based rewind protocol or dependence on another role's cursor is allowed.
   Thus no rewind is needed. [Positioned I/O](https://man7.org/linux/man-pages/man2/pread.2.html)
9. Run the fixed consumer once on C, then the independent observer once on O, with boundary
   checks below. Finalize evidence only after both return and A/C/O still match. Close
   all owned descriptors on termination; no persistent runtime object is deposited.

The exact four-seal profile intentionally refuses environments that add an extra initial
seal or deny these creation flags. Modern kernel memfd execution policies can change defaults;
this document neither changes that policy nor falls back to `MFD_EXEC`. An environment
requiring a different profile needs separate document authorization. The four-seal profile
is not an OS-level non-executable guarantee: non-execution is the fixed behavior boundary.
[Kernel memfd execution-policy documentation](https://docs.kernel.org/userspace-api/mfd_noexec.html)

## 2. Protected-object identity and same-object evidence

Stable content/policy identity is the tuple (profile, sealed-memfd type, length 3, F, Q).
It cannot distinguish two equal-content memfds. Same-object evidence additionally requires:

- Harness-witnessed one creation of A and direct duplication edges A->C and A->O. No
  caller-supplied descriptor, callback, dynamic dispatch, close/reuse, `dup2` replacement
  or mutable descriptor registry is allowed in the positive path.
- Required `fstat` device/inode equality among all three concurrently retained descriptors,
  at duplication, immediately before and after each role, and before final evidence.
  Each role independently obtains its own `fstat` information and seal state. The harness
  compares these observations with the still-live A and checks the actual handle passed.
- Independent length/F/Q checks by each role, plus final A check. Close-on-exec and regular
  type are checked on each handle. Sealed-object ancestry and handle association must be
  observed by the harness, not inferred from a returned hash.

Device/inode metadata is **required corroboration**, never cryptographic identity. Numeric
FDs are ephemeral process-local slots, not stable identifiers. The harness keeps ephemeral
A/C/O slots and raw metadata only during the test and reports checked relationships, not
numeric values, in canonical evidence. Keeping A open prevents reuse of its live inode
from masquerading as a newly created equal-byte object within the trusted kernel model.
No claim of equivalence against a malicious kernel, malicious harness or concurrent
uncontrolled descriptor-table mutation is made. No `kcmp`, ptrace permissions or process
identity assertion is required: creation/duplication provenance plus live metadata checks
are the chosen assurance under the explicit trusted single-process assumption.

## 3. Consumer and independent observer

Both roles are fixed functions in the proposed implementation module; before acceptance
runs its entire reviewed source SHA-256 K is pinned externally by the reviewer. The trusted
harness fixes function references before acquisition. Role identities are:

- consumer: `ns001.h2a2.identity-consumer.v1`, entrypoint `consume`;
- observer: `ns001.h2a2.identity-observer.v1`, entrypoint `observe`.

Each function receives only its duplicated handle as an input argument, never a pathname,
source byte buffer or the other role's result. Constants and expected bindings are fixed
in the trusted harness context. Each independently queries type/size/seals, reads its own
handle, computes its own SHA-256 and emits its observation. The observer does not call the
consumer or reuse its buffer/hash/boolean conclusions. Sharing the standard hash library
is permitted; independence is logical observation, not independent kernel or process trust.
The harness is a separate test role and does not accept either role's self-assertion that
its descriptor was the right one.

Both roles only inspect, count, hash, compare and return. Neither executes/evaluates/decodes
payload, parses scientific semantics, reopens any path, maps memory, writes, truncates,
adds seals, accesses network/credentials, spawns subprocesses or dynamically loads plugins.
Observation has no mutation beyond local bookkeeping and returning evidence. The harness
owns closing handles. Neither role can declare the final ACCEPT on its own.

## 4. Exact evidence profile and ACCEPT rule

Use the acceptance specification's C serialization: sorted object keys, compact ASCII
JSON, no BOM, whitespace suffix, clock, nonce, PID, path, numeric FD or inode in output.
All fields below are mandatory; unlisted fields are forbidden. Booleans are JSON booleans,
lengths/counts integers, digests lowercase 64-hex strings. Symbolic seal array L is exactly
`["F_SEAL_GROW","F_SEAL_SEAL","F_SEAL_SHRINK","F_SEAL_WRITE"]` in that order.

Each role's canonical successful observation has exactly these keys:
`role` (consumer or observer), `source_sha256` (K), `object_type` (sealed-memfd),
`byte_length` (3), `sha256` (F), `seals` (L), `reference_bound` (true).
The last field is supplied by harness validation of the actual handle and the role's
independently obtained ephemeral metadata, not a candidate-supplied success flag. The raw
internal return has exactly six keys: `byte_length` (measured integer), `sha256` (computed
lowercase digest), `seal_mask` (queried integer), `st_dev` and `st_ino` (measured integers),
and `regular_file` (measured boolean). The role checks regular type and expected values
before returning; the harness independently compares all observations. This internal
return is not emitted as a deterministic receipt. Wrong type, missing/extra fields or wrong
values in that internal measurement result refuse. Role functions and the harness must
be reviewed for this exact separation before acceptance runs.

Final canonical mechanism ACCEPT record has exactly:

| Key | Required value |
| --- | --- |
| profile | ns001.h2a2.sealed-memfd.v1 |
| verdict | ACCEPT |
| snapshot_sha256 | S |
| manifest_sha256 | M |
| source_sha256 | F |
| byte_length | 3 |
| implementation_sha256 | K |
| harness_sha256 | independently pinned whole test-module SHA-256 T |
| consumer | exact consumer observation above |
| observer | exact observer observation above |
| checks | object specified below |

`checks` has exactly `source_validated`, `copy_validated`, `sealed_revalidated`,
`creation_witnessed`, `duplication_witnessed`, `same_object`, `no_reopen`, all true,
and `consumer_calls`:1, `observer_calls`:1. These denote independently observed operations
in the trusted test harness; they cannot be filled from a manifest or copied old receipt.
Successful evidence thus includes both content and the concrete observation chain.

Final canonical REFUSE record has exactly `profile` (same profile ID), `verdict` (REFUSE),
`code` (one applicable code), `handoff_succeeded` (false). No embedded successful role
receipt. Per-case inventory separately retains test ID, expected code/verdict, actual
canonical record and its SHA-256, actual role call counts, and observations establishing
the failed checkpoint. Hash canonical records externally, not recursively. No raw slot,
inode, absolute path or exception message is needed in canonical records. Retain K/T,
reviewed test source and fixture constants so a reviewer can reproduce relationship tests.
K/T may not be fabricated now or chosen by the running candidate.

ACCEPT is a conjunction: exact original source/manifest/root validation; exact copied
bytes; successful Q establishment and exact query; revalidated sealed A; witnessed direct
duplicates; same-object checks; one independently successful consumer and observer; no
reopen/mutation violation; complete deterministic evidence. Otherwise REFUSE, no repair,
retry, backend substitution or fallback. A crash/missing record is a failed test, not ACCEPT.
No borrowed observation, equal hash alone or boolean self-report proves same-object use.
Identical successful reruns with the same K/T intentionally give identical record hashes;
this is not freshness authentication or a cryptographic execution attestation.

## 5. Failure ordering and bounded mechanism tests

Existing policy/root/member/manifest/source phases and codes precede these mechanism
phases. Within the added sequence below, first failed checkpoint wins; within a checkpoint
use the listed order. Protocol violations are checked before the prohibited action is
used for consumption. A harness-injected post-seal mutation request marks that circuit
ineligible for ACCEPT even when the kernel correctly rejects the syscall.

| Checkpoint | Ordered codes and conditions |
| --- | --- |
| Creation | MEMFD_CREATE (syscall unavailable/fails); MEMFD_CAPABILITY (flags/type/CLOEXEC/initial size or initial seals not the specified creation contract) |
| Copy | MEMFD_COPY_IO (error/short write or read); MEMFD_COPY_SIZE (size/read length not 3); MEMFD_COPY_DIGEST (hash not F) |
| Seal | MEMFD_SEAL_APPLY (F_ADD_SEALS error, including EBUSY); MEMFD_SEAL_SET (query failure or set not exactly Q) |
| Finalization | MEMFD_COPY_IO, MEMFD_COPY_SIZE, MEMFD_COPY_DIGEST on post-seal reread; HANDOFF_MUTATED if a previously finalized object's contents change |
| Delivery/role boundaries | HANDOFF_REOPEN (attempt to use pathname as consumption source); HANDOFF_MUTATION_ATTEMPT (scheduled forbidden write/size-change attempt); HANDOFF_SUBSTITUTED (association/ancestry/live metadata mismatch); HANDOFF_UNPROTECTED (missing protection or required seal query fails); CONSUMER_IDENTITY; OBSERVER_IDENTITY; MEMFD_HANDLE (duplication/stat/CLOEXEC failure not already classified) |
| Consumer measurements | CONSUMER_RESULT (error, malformed/wrong measurements, nondeterminism or call count) |
| Observer measurements | OBSERVER_RESULT (same conditions for observer) |
| Final evidence | EVIDENCE_INCOMPLETE (missing observations, incorrect canonical record or failed final association evidence) |

For real seal-query mismatch at a delivery boundary use HANDOFF_UNPROTECTED before calling
the role. Fault-injected wrong role return with intact boundaries uses its RESULT code.
Recheck same-object association before seal/hash checks on a substituted handle. Earlier
spec N13/N14/N26/N27 remain applicable with this profile's checkpoints; HANDOFF_MUTATED
is synthetic corrupted-state branch coverage if real sealing prevents mutation.

These are additions/adaptations to required N01–N31 and appended cases, not a new broad
fuzzing campaign. Each starts from the one fixed fixture with one named defect:

| ID | Deterministic mechanism defect / operation | Expected REFUSE code |
| --- | --- | --- |
| M01 | Create without MFD_ALLOW_SEALING; initial F_SEAL_SEAL prevents contract | MEMFD_CAPABILITY |
| M02 | F_ADD_SEALS fails; bounded adapter fault at that call | MEMFD_SEAL_APPLY |
| M03 | Omit one of Q's four bits, one subcase each, query final state | MEMFD_SEAL_SET |
| M04 | At finalized pre-delivery checkpoint attempt pwrite of one different byte at offset 0 | HANDOFF_MUTATION_ATTEMPT |
| M05 | Same checkpoint: ftruncate to 2, then separate fresh subcase to 4 | HANDOFF_MUTATION_ATTEMPT |
| M06 | Replace finalized A association with equal-byte separately created sealed memfd before consumer | HANDOFF_SUBSTITUTED |
| M07 | Substitute observer binding after consumer completes with equal-byte separately created sealed memfd | HANDOFF_SUBSTITUTED |
| M08 | Give consumer a different memfd while A/O remain original | HANDOFF_SUBSTITUTED |
| M09 | Give observer a different memfd while A/C remain original | HANDOFF_SUBSTITUTED |
| M10 | Copy three wrong bytes before sealing | MEMFD_COPY_DIGEST |
| M11 | Copy two or four bytes, completing faulty copy but reporting its actual length | MEMFD_COPY_SIZE |
| M12 | At handoff checkpoint attempt to reopen original pathname rather than use C/O | HANDOFF_REOPEN |
| M13 | Negative harness holds writable shared mapping before seal call, then attempts Q | MEMFD_SEAL_APPLY |
| M14 | Inject failed/short copy operation without completing the copy | MEMFD_COPY_IO |
| M15 | Wrong observer identity or wrong observer measurement result, separate subcases | OBSERVER_IDENTITY / OBSERVER_RESULT |

For M04/M05, require genuine kernel EPERM and unchanged length/F/Q, then terminate with
HANDOFF_MUTATION_ATTEMPT. The syscall rejection is protection evidence; outer REFUSE is
because the controlled protocol contains a forbidden mutation attempt. Do not claim the
bytes changed. If the syscall succeeds or fails for an unrelated reason, the acceptance
test FAILS regardless of any printed REFUSE; it does not prove protection. For M13 require
genuine EBUSY, stop, and unmap only during cleanup; no retry. Positive roles never map.
M02 fault injection is labelled synthetic and cannot replace M13 or real positive sealing.
M03 may exercise real reduced seal sets only in a quarantined negative object, never
passed to roles. M06–M09 keep original A open and use distinct live memfds; equal-byte
substitution must fail independently of hashes. M12 uses a test harness operation guard
that rejects the attempted reopen before actual path I/O; source inspection verifies no
consumer/observer path-opening code. This guard is a controlled-test boundary, not a
sandbox against arbitrary hostile code. Fault hooks belong only to the test harness;
there is no public callback or selectable consumer in the implementation interface.

Retain review-required SCHEMA_TYPE, duplicate precedence and ROOT_UNSTABLE cases with
existing specified codes. Preserve P2 source replacement/deletion after finalization as
positive isolation subcases of the one P1 acceptance rule. Only the test harness may
perform those scheduled pathname mutations; neither role nor validator reopens the
source for consumption. Run P1 twice in fresh roots for
identical canonical receipts. There is one positive predicate, not a second source-identity
policy. All pre-consumer refusals require zero consumer/observer calls; M07 permits one
consumer and zero observer calls. Result-stage failures allow only the calls already
reached, never retries. A skipped genuine-path test is an acceptance gap, never PASS.

## 6. Claims, residual assumptions and abort boundary

Strongest permitted claim, only after successful future implementation/acceptance:

> The exact expected single-file bytes were validated, copied into a sealed immutable
> handoff object, and the same protected object was independently observed by the fixed
> non-executing consumer and observer.

This claim is scoped to the declared trusted harness. It does not establish source-byte
execution, runtime/interpreter/kernel identity, dependency identity, client identity,
transport integrity, scientific correctness, E0 execution, the full external_trust_root
gate or any other H2 gate. All eight substantive H2 gates remain unresolved.

Linux memfd/sealing semantics, the kernel, standard hashing, test engine and reviewed
harness are residual trust assumptions. Future syscalls/queries test observable behavior;
they do not authenticate the kernel enforcing it. The same-process observer is logically
independent, not a security principal isolated from the validator. Descriptor-table control,
exclusive synthetic acquisition, correct source-to-callable loading and honest observation
remain explicit assumptions. Broader runtime/dependency locking is separate later work.
Nothing here promotes those assumptions to VERIFIED.

Stop on unavailable primitives/constants, unsupported initial/final seals, failure to
bind root/handles, unreviewed K/T, uncontrollable concurrency, inability to run a required
real protection test, unexplained evidence mismatch or any need to widen paths/claims.
Do not change host policy, use credentials, weaken seals, add a mutable backend or test
real scientific input to proceed. A failed circuit remains failed after cleanup.

## 7. Smallest future circuit and preservation

Future add-only paths, NOT created or implementation-authorized here:

- `e0/h2/runtime_trust_root.py`: one validator/sealed-memfd handoff, fixed consume function,
  fixed observe function, deterministic record construction; no external dependency.
- `tests/test_e0_h2_runtime_trust_root.py`: trusted synthetic harness, embedded abc/manifest
  fixture, one P1 positive predicate with repeat/P2 isolation subcases, existing bounded
  negative matrix and the mechanism-specific cases above; reviewed whole source pin T.
- `docs/e0/h2/NS-001_H2A2_RUNTIME_TRUST_ROOT_IMPLEMENTATION_RECEIPT_v0.1.md`: implementation
  source pins, actual canonical outputs/hashes, real-vs-synthetic results and limitations.

No persistent fixture directory or new evidence tree. Future fixture files exist only in
approved fresh temporary roots. Forbid all other repository paths, including prior H2A1/H2A2
receipts, `docs/e0/h2/evidence/**`, existing H2 verification code/tests, scientific code,
`preregistrations/e0/**`, protocols, datasets/results, workflows, clients, credentials,
publication objects and settings. No real source execution, live traffic or E0.

Implementation-ready: YES for this defined synthetic design, conditional on fresh explicit
implementation authorization and externally reviewed K/T before acceptance runs. This does
not assert Linux capability on this host, completed controls, passing tests or closure of
any gate. The next circuit remains separate.

This circuit used only document inspection, public Linux documentation, administrative
text/hash checks and Git preservation. No memfd, seal, fixture, test, runtime/client or
scientific execution occurred. Before commit, compare all prior tracked file bytes to
starting HEAD, confirm only this new document is changed and all three future paths remain
absent. No scientific artifacts or H2A1 bytes may change.

Observed pre-commit preservation result: PASS; all 195 previously tracked files are
byte-identical to starting HEAD, all three future paths are absent, and only this new
selection document appears in Git status. No mechanism implementation or test was run.

## Closing disposition

- selected mechanism: LINUX SEALED MEMFD HANDOFF, ns001.h2a2.sealed-memfd.v1.
- required primitive/seal contract: MFD_ALLOW_SEALING | MFD_CLOEXEC; one F_ADD_SEALS of Q; exact F_GET_SEALS equality; no mappings or fallback.
- protected-object identity: witnessed live memfd plus length/F/Q; concurrently retained direct duplicates and required device/inode corroboration, never cryptographic FD identity.
- consumer profile: fixed consume; handle-only seal/type/size/read/hash observation; no interpretation, execution, network, subprocess, reopen or mutation.
- independent-observer profile: fixed observe; separate handle-only independent measurements; same prohibitions.
- same-object evidence rule: witnessed A->C/A->O duplication, live metadata association at each checkpoint and independent matching content/seals under trusted harness.
- ACCEPT rule: all source/copy/seal/association/role/evidence checks pass exactly once; otherwise REFUSE.
- mechanism-specific REFUSE tests: M01–M15 and preserved N-matrix; real kernel mutation denial distinguished from synthetic refusal-branch injection.
- allowed claim: validated exact bytes copied to sealed object independently observed by fixed non-executing consumer and observer; no execution claim.
- residual assumptions: Linux kernel/sealing, test engine/hash library, exclusive fixture/descriptor control and honest reviewed harness; not VERIFIED runtime identity.
- future implementation paths: only the three add-only paths in section 7.
- implementation-ready: YES for the bounded design; implementation and acceptance not performed or authorized by this document circuit.
- H2A1 status: VERIFIED for scoped prospective custody/publication auditability; unchanged.
- H2A2 status: implementation UNSTARTED; all eight substantive H2 gates unresolved.
- E0 status: HOLD.
- one next bounded action only: expressly authorize one offline synthetic implementation/acceptance circuit restricted to the three future paths and this sealed-memfd profile.
