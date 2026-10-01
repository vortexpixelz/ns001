# NS-001 H2A2 real CPython receipt implementation v0.1

Date: 2026-10-01 (America/New_York).
HEAD before: `345c6497f4d715a5131e0ca386fd8eea9b221c6e`.
Branch: `codex/e0-h2-preparation`; initial working tree clean.

**Implementation verdict: PARTIAL.** This single implementation-only circuit adds
offline validation primitives and a synthetic acceptance suite. It does not implement
a complete future native experiment integration. The concrete remaining implementation
blockers below prevent declaring conformance PASS. No substantive frozen semantics
were changed and no design contradiction was found.

**NO GDB process, launch or attachment, real candidate compile, eval, exec or candidate
import occurred.** The two-byte fixture was used only as data in constructed snapshots
and comparisons. Administrative shell/Git commands and the offline Python unittest
runner executed; those tooling imports are not imports of the candidate. No scientific,
client, network experiment, E0, interpreter/GDB/package mutation or runtime-lock work
occurred. Authorized Git publication is administrative, separate from experiment traffic.

## Additive files

| Implementation file | Implemented surface |
| --- | --- |
| `e0/h2/real_receipt_policy.py` | Frozen engine/tool comparator, artifact hashes, Q1 initialization and phase plans, restricted MI vocabulary, ranked codes, deterministic encoding |
| `e0/h2/real_receipt_abi.py` | Explicit addressed snapshot reads, exact native object layouts, primitive/vector/callable/module/dict/root decoders |
| `e0/h2/real_receipt_observation.py` | Bounded MI2 parser/token association, immutable forensic record containers, derivation and paired-stop/byte/attempt evaluators |
| `e0/h2/real_receipt_evidence.py` | Exact canonical record validators, separate durable store/attempt namespace, immutable journal terminals, recovery, forensic encoding and manifest generation/verification |

Test file: `tests/test_e0_h2_real_receipt.py`.
The sole new receipt is this file. No other documentation or historical evidence changed.
There is no GDB connection/launcher, subprocess, ptrace, candidate compiler or delivery
function in these implementation files. The phase plan is data, not a runnable command
file; execution commands remain dependent on later qualified control/stop observations.

## Frozen design hashes

All five controlling files remain byte-identical to HEAD before:

| Controlling file in this directory | SHA-256 |
| --- | --- |
| `NS-001_H2A2_REAL_CPYTHON_INPUT_BOUNDARY_SPEC_v0.1.md` | `eae004d95046d2c2a83fd7813f4b0485ce792e358403a406859280f4c0fdc564` |
| `NS-001_H2A2_REAL_CPYTHON_ENGINE_PROVENANCE_REVIEW_v0.1.md` | `3fd49cf843b582ddffed971281e226c2d1f419462c17150ca48e82a3b649453e` |
| `NS-001_H2A2_REAL_CPYTHON_NATIVE_OBSERVER_DESIGN_v0.1.md` | `cdca62d5f02a468353d4c0ba9113e3d4ced047f4b78f68c949b1141bbad1b075` |
| `NS-001_H2A2_REAL_CPYTHON_RECEIPT_EXPERIMENT_DESIGN_v0.1.md` | `b120fb71ca537d84926e0b81173d1f867f9e92cbde0c54696191c0a8cafee54d` |
| `NS-001_H2A2_REAL_CPYTHON_GDB_Q1_REVIEW_v0.1.md` | `6ae726ee2bb2821e4f0a0667f4d4dcefcdd07d49dfdf6e1e0b32d35007eb9339` |

## Results and limits

**Q1 policy:** exact 26-command early initialization represented; fixed readback
names, hardware numeric sites, two-slot budget, one in-place CALL step, exec/syscall
ptrace semantics and independent unmasked text/inventory/death-chain admission
requirements represented. Memory writes, software breakpoints/fallback, displaced
stepping, inferior evaluation and alternate sites are denied. Every missing synthetic
admission fact refuses. Readback inputs currently use normalized `(show-name,
exact-set-command)` pairs; the MI parser does not yet derive those pairs or the
native admission facts from a complete captured Q1 transcript. Thus representation
and offline validation pass; integrated policy establishment remains PARTIAL.

**Engine admission:** exact frozen executable path/hash, relevant package/source
versions, build ID/size, architecture/ABI/bias, compiler image, caller/receiver
coordinates/bytes, method/vectorcall, GDB and loader identity checked deterministically.
All named supporting artifact roles require nonempty bytes matching frozen hashes.
Tests use explicitly synthetic metadata/dossiers, never claim actual launcher/tool
qualification. Read-only executable/GDB/loader hashing before and after this circuit
reproduced the frozen identities; it does not establish mapped live identity.

**ABI decoder:** bytes, tuple, compact/noncompact Unicode (1/2/4-byte units), normalized
3.12 integers, exact True, PyCFunction, module, combined/general/split dictionaries,
seven-pointer argument vector and four roots decoded from synthetic captures.
Reads are explicit-length, bounded and overflow checked. Null/unmapped/partial/
overlapping captures, wrong exact types, malformed tags/indices/counts, oversized
objects and inconsistent terminators fail closed. No missing memory is padded.
Dictionary/header consistency is checked on the supplied snapshot; operational
repeat-read generation and proof of sole-thread snapshot stability remain future
capture integration obligations.

**Paired-stop validation:** checks strict caller-to-receiver ordering, PID/TID and
retained process-custody association, qualified reason labels, command tokens, PCs,
target/C, argument register/vector equality, RSP decrement, return PC, callable/module/
dict/roots and full exact arguments. Supporting derivation explicitly permits a
resize move and requires final post-resize/RET/READY B association, one syscall and
bounded result/capture. Labels and admission predicates are synthetic inputs here;
the implementation does not manufacture kernel stop provenance from matching PCs.

**Byte receipt:** native args[0] is decoded independently, exact PyBytes B identity
checked, length measured, complete payload captured and SHA-256 calculated externally
with hashlib. Full bytes, length and digest compare with independent A, derivation
and READY captures and the fixture comparator. Expected fixture data without a direct
capture fails. Equal bytes do not rescue a changed source identity. This is offline
validator acceptance only, not empirical real receipt or qualified native hashing.

**Lifecycle:** separate namespace, exclusive lifetime flock, retained custody and
reservation journal, request/registration/E links, PREPARED -> synchronized ATTEMPTED
-> witness/capture -> ACCEPTED/REFUSED. Hash-linked journal and readbacks validated.
Synchronization failure poisons the current writer; no dispatch API exists.
Terminal attempts and ABORTED recovery cannot resume; missing/replaced custody stops.
The positive test constructs a synthetic terminal after validating its raw capture.
Native preparation/admission is not yet integrated before PREPARED; the preparation
method currently enforces request selection/parameters, not all native admission.

**Refusal/recovery:** only frozen ranked codes, one primary and ranked deduplicated
diagnostics. Argument and source substitutions keep their existing distinct codes.
Interrupted/nonterminal records recover to separate ABORTED; complete invalid records
use RECORD_INVALID, otherwise ATTEMPT_INCOMPLETE. Torn tails and partial recovery files
are preserved, recovery conflict stops, valid existing terminals stay byte-identical.
Recovered terminals with incomplete packaging are not promoted to public ACCEPT.
Reserved-only cuts before attempt-directory/registration creation still lack a complete
integrated recovery path; the store refuses further reservation on retained mismatch.

**Deterministic evidence/package:** fixed canonical schemas reject unknown fields,
duplicates, noncanonical bytes and unsupported values. ASCII JSON, sorted keys and
exact final LF feed SHA-256. Volatile native records stay in separate forensic capture
encoding. Capture/package manifests use frozen key sets, sorted relative paths and
exact file lengths/digests, exclude self-reference and use an external hash sidecar.
Public acceptance requires a fixed minimum full observer/qualification inventory,
original retained bytes and verified capture/package links. Complete ordered package
persistence and capture-file production are not implemented; no public experiment
ACCEPT is produced by this circuit. Identical-input serialization passes; cross-attempt
semantic comparison stripping only permitted ID-derived links is not yet integrated.

## Offline test inventory

Final command:
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_e0_h2_real_receipt.py' -q`.
Final result: **161 tests, 0 failures, 0 errors, OK** (1.512 seconds).

| Test class | Count | Coverage |
| --- | ---: | --- |
| ABITests | 19 | Every required object class/layout, bounded reads, missing bytes, wrong types, overflow, malformed Unicode/int/dict, split/general dict |
| LifecycleTests | 18 | Synthetic durable positive, immutable terminal, ABORTED idempotence/terminality, interruption, torn/invalid/cross-attempt records, recovery conflict, lost/replaced custody, reservation loss, stale writer, fsync failure, incomplete package |
| MITests | 18 | Token/result/async/stream/nested parsing, raw error retention, duplicate/injection/overflow refusal, outstanding-command control and forbidden observer commands |
| OfflineReceiptTests | 102 | Decoded positive and witness, every frozen engine field mismatch, artifact pins, byte mutations/type/source substitution, six argument mutations/count/keyword, both stops/order/PID/TID/return/entry count, ATTEMPTED links, derivation/resize/I/O/retry, independent A, observer loss, Q1 required facts/fallback and ranked codes |
| SerializationTests | 4 | Canonical rejection, deterministic manifests, changed-byte verification, traversal/self-reference rejection |

The initial 128-test run passed. After additional custody checks one intermediate
156-test run exposed an exception-type mismatch for missing custody; it was corrected
without changing disposition. Subsequent 156/158 runs passed. The final 161-test run
covers the current implementation/test bytes. No frozen tests or real observer tests
were executed. Synthetic records contain facts and raw bytes, never expected terminal
verdicts or consumer-written success fields; verdict assertions reside only in tests.

## Concrete implementation blockers / verdict

**PARTIAL**, not PASS and not STOP_DESIGN_CONTRADICTION:

1. Native launcher/death-chain, bounded bootstrap/control-channel/guard artifacts and
   their fixed preparation/one-shot-release state machine are absent. Offline predicates
   are represented, but no complete producer establishes them or blocks release through
   the frozen native control chain. No launch is authorized by this receipt.
2. MI-to-Q1 readback/admission translation and full raw derivation/stop/code-map capture
   integration remain absent. The parser, decoder and validators are composable
   primitives, not a qualified integrated observer. Missing operational provenance
   cannot be supplied by their synthetic positive result.
3. Precondition refusal witness/persistence orchestration, reserved-only write-cut
   recovery, the complete ordered package writer/full-stage cut matrix and restricted
   cross-attempt determinism comparison remain incomplete. Current stop/fail-closed
   behavior is not claimed to satisfy all frozen durable experiment obligations.

These are implementation gaps, not requests to relax the design. No real receipt
experiment, runtime mechanism-admission controls or next circuit were performed.

## Preservation, assumptions and status

All **220** pre-existing tracked files were inventoried before implementation and
verified unchanged before publication. This includes H2A1, the sealed-handoff and
surrogate code/tests/fixtures/receipts, all five controlling files, engine provenance,
observer/Q1 designs and E0 HOLD evidence. Only the four new implementation files,
one new test file and this receipt belong to the scoped commit.

The executable/GDB/loader baseline checks pass. No installer, package manager mutation,
debugger invocation, target attachment, candidate compile/eval/exec/import, runtime
probe or scientific/client/E0 command was issued. This is an action-bounded preservation
statement, not surveillance or attribution of unrelated host processes/package activity.
Global package state and full dependency integrity are not claimed.

Residual assumptions: synthetic snapshots are internally honest test inputs; supplied
native-stop/admission labels would require a separately qualified producer. Future
receipt still depends on honest host/kernel/procfs/debug hardware/storage, no hostile
native writer, pinned and reviewed tools/bootstrap/controller/guards, narrow provenance
trust and independent raw unmasked reads. Hashlib computes offline measurements here;
its qualified origin/runtime and a complete live tool dossier are not established.
No compiler/parser correctness, compilation success, candidate execution, runtime
immutability, transitive dependency closure or hostile-host resistance is established.

- external_trust_root: **UNRESOLVED**.
- dependency_runtime_lock: **UNRESOLVED**, untouched.
- H2A1: **VERIFIED + frozen**, unchanged.
- H2A2: sealed handoff **VERIFIED**; surrogate **VERIFIED WITH RESIDUAL ASSUMPTION**;
  completed slices frozen unchanged; real mechanism implementation **PARTIAL**;
  no real native receipt; all full H2 gates remain unresolved.
- E0: **HOLD**, no execution or authorization.
- One next bounded action only: separately authorize one implementation-only completion
  circuit for the enumerated integration/recovery/package blockers, with offline tests
  and no observer launch or candidate compile. Not performed here.

Resulting commit/push identities are reported outside this receipt to avoid self-reference.
