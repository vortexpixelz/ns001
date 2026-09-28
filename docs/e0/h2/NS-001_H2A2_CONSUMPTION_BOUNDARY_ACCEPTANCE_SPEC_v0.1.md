# NS-001 H2A2 consumption-boundary acceptance specification v0.1

## Basis, decision and authority

Preparation branch: `codex/e0-h2-preparation`.
Reviewed HEAD: `9414f490fba4465859a0298b45c5e3d2ee18be70`; initially clean.
This is a document-only prospective acceptance contract, not an implementation, test
result, runtime selection or execution authorization. Only this specification changes.
No interpreter, compiler, loader, client, scientific code or acceptance test was invoked.
Inspection used text readers, Git and file hashing only. No network research was performed.

**Implementation readiness: PARTIAL.** The bytes-only surrogate below has a defined
contract. Actual compiler-boundary acceptance remains blocked on selection/review of a
specific engine and an observation mechanism at that engine's real input boundary.
An ordinary wrapper reporting its outgoing argument is not sufficient. A live E0 entrypoint
has not been selected. Neither omission is filled by guessing or by promoting surrogate
success. The next action is independent document review, not implementation.

Repository authorities, all pinned at reviewed HEAD:

- `docs/e0/h2/NS-001_H2A2_EXTERNAL_TRUST_ROOT_NEXT_SCOPE_v0.1.md`.
- `docs/e0/h2/NS-001_H2A2_RUNTIME_TRUST_ROOT_CORRECTION_REVIEW_v0.1.md`.
- `docs/e0/h2/NS-001_H2A2_SNAPSHOT_HANDOFF_ACCEPTANCE_SPEC_v0.1.md`.
- `docs/e0/h2/NS-001_H2A2_HANDOFF_MECHANISM_SELECTION_v0.1.md`.
- `docs/e0/h2/NS-001_H2A2_RUNTIME_TRUST_ROOT_DESIGN_v0.1.md`.
- `docs/e0/h2/H2_EVIDENCE_CONTRACT_DRAFT.md`.

The existing first-slice contract and its historical evidence remain unchanged. This
contract adds a prospective downstream interface; it does not retrofit consumption claims
into the first slice or treat its already-closed descriptors as live inputs.

## 1. Real source path and the proposed consumption boundary

Read-only source inspection establishes the following distinctions:

| Repository evidence | What exists, and what it does not establish |
| --- | --- |
| `Dockerfile` | Python image tag `python:3.12.7-slim-bookworm`; entrypoint `["python","run_experiment.py"]`; `/app` working directory. This is an existing feasibility container recipe, not a digest-pinned runtime lock or approved E0 launch recipe. No image was built or run. |
| `run_experiment.py`, imports, `main`, `run` | Python script selected by pathname; imports NumPy and `ns001_tau_check`; reads a JSON protocol and can call scientific/network code. The post-operation source-file hashes do not prove which bytes produced loaded code. It is not an approved E0 entrypoint. |
| `ns001_tau_check.py`, imports and `main` | Python measurement engine/standalone CLI, including network retrieval. It must not be imported or executed for this slice. |
| `e0/hardening.py`, module header, `_verify_running_source`, `LiveGetDataAdapter`, `run_mock_attempts` | H1 scaffolding, explicitly no executable entrypoint or live client; imported-source consistency only. `run_mock_attempts` requires a guarded mock session. `LiveGetDataAdapter.fetch` refuses. These are not a production E0 main. |
| `preregistrations/e0/NS-001_E0_INTERFACE_DECISION_DRAFT.md` and `NS-001_E0_GETDATA_AMENDMENT_DRAFT.md` | Proposed GetData interface; no client selection; require reviewed source-only bootstrap or externally verified read-only runtime. Both remain drafts, not execution authority. |

**Actual candidate E0 entrypoint: not yet selected/implemented in the inspected design.**
The concrete source requiring future binding is Python; the mock module is an importable
scaffold, and the existing feasibility runner is a reference path only. Neither is silently
adopted for E0. Python 3.12/CPython is the proposed interface family for this specification,
not a measured or approved running engine.

An installed source copy was inspected as supplemental interface evidence, without import:
`/usr/lib/python3.12/importlib/_bootstrap_external.py`, SHA-256
`97c6211750d63067712ad2cd74d50be33337f1fb1cd2c769022ced9b401edd92`.
Its `SourceLoader.get_code` can read source by pathname or return cached bytecode;
`source_to_code` passes data to `compile` with mode `exec`. `exec_module` is a separate
execution step. Thus merely matching the source file does not rule out a bytecode path.
This local source copy is not a retained authoritative engine release or runtime pin;
future real-engine acceptance requires retained, version-matched primary interface evidence.
It is not a hidden local prerequisite for the normative surrogate defined below.

Selected prospective input interface: the **bytes argument at entry to the identified
compiler callable**, conceptually `compile(B, filename, mode, flags, dont_inherit, optimize)`.
The source-facing object is B, not an FD number or a pathname. The controlled boundary ends
when that callable accepts the actual B argument; parser/compiler internal transformations
and generated code are downstream. A return value, syntax error or successful execution
cannot substitute for witnessing this entry. No assertion about all parser reads follows.

| Interface | Treatment in this contract |
| --- | --- |
| Script pathname | Existing runner route; disallowed as source delivery for this slice. |
| Module/import resolution or bytecode/build artifact | Existing Python alternatives; excluded from this top-level input route and not proven safe globally. |
| Sealed memfd descriptor | Protected acquisition source; no claim that Python's compiler callable accepts it directly. |
| stdin or file/stream launch | Not selected; buffering/EOF/launch semantics would need another contract. |
| Immutable in-memory bytes | Selected deterministic derivative, with complete byte-preserving read and independently witnessed callable-entry identity. |
| Other interfaces | Refuse; no fallback or inferred equivalence. |

## 2. Claim ceiling and profiles

Two mandatory, non-interchangeable profile names:

- `ns001.h2a2.compile-input-surrogate.v1`: input-boundary surrogate only.
- `ns001.h2a2.compile-input-real.v1`: actual selected compiler boundary, blocked pending
  the engine/observer qualification described below.

Strongest real-profile claim: **Exact previously verified protected bytes were supplied
to the identified compiler input boundary, and independent evidence bound the protected
object and its exact immutable byte derivative to that attempted consumption.**
Here “consumption” means receipt as the source input argument, not proof that every byte
influenced compilation, produced instructions or executed. The stronger primary-objective
wording must always carry this boundary definition.

Surrogate ACCEPT claims only receipt by the fixed non-executing surrogate under the trusted
harness. It MUST NOT say that CPython or another actual compiler received the input.

Both profiles prohibit claims of successful execution, runtime/compiler correctness,
dependency/imported-module/client identity, transport integrity, response or scientific
correctness, E0 success, or closure of either full `external_trust_root` or
`dependency_runtime_lock`. Host/kernel/harness/observer honesty and hash assumptions remain
explicit; in-process evidence is not attestation against a compromised interpreter.

## 3. Protected input and immutable derivative

Choose **B: a deterministic immutable derivative** because the selected source interface
accepts bytes, not a memfd. This is an interface requirement, not an interchangeable option.
Keep the first profile's inert payload, exactly `61 62 63`, length 3, hash F:
`ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`.
No executable scientific fixture is introduced. Frozen manifest/root identities M/S remain
`4a9ebe2c4e275600d9a6c7864bb14c3d5a4c0b6a7c8bbf88193fc48f76affce0` and
`0ae1c30f2568188390fe05d092609eb122f3bee16c48f41fae9fe3f08e6ba432`.

Future preparation must freshly establish the frozen protected-object rules and retain A
live for this attempted downstream handoff. A historical receipt alone cannot grant a new
FD that identity. Independent evidence must witness creation, validation, sealing and the
live association. A/C/O remain logical labels; no numeric FD or inode is a stable identity.
The four exact seals Q, type, size and association are checked before and after derivation
and at boundary completion. No pathname access to payload after validation is permitted,
including `/proc/.../fd` or `/dev/fd` aliases.

Derivation is exactly one bounded positioned `pread(A,4,0)` returning exactly 3 bytes,
with `fstat` size 3, Q and association intact before/after. Incomplete I/O refuses without
retry. B must be exact immutable bytes, length 3, hash F, full byte equality to the frozen
payload and independent protected-object read. No memoryview, bytearray, str or subclass
is accepted. Retain B live through boundary observation. No trim, newline/BOM adjustment,
decode/encode, normalization, decompression, concatenation, compilation or reserialization
is permitted before input entry. B is not the same object as A; witnessed derivation binds
them. The observer must check live B identity, not just accept a matching digest on a
substituted equal-byte object. Retain the original B reference to avoid identity reuse.

Allowed metadata difference: the input filename argument is the fixed diagnostic label
`<ns001-h2a2-input-v1>`, not a path and never a locator. It makes no source-origin claim.
No other metadata change is allowed. Invocation arguments are exactly:
`source=B`, `filename="<ns001-h2a2-input-v1>"`, `mode="exec"`, `flags=0`,
`dont_inherit=true`, `optimize=0`. Types are exact bytes/str/str/int/bool/int;
booleans cannot stand for integers. AST, code object and imported-module inputs refuse.

## 4. Engine identity and independent observation

An expected identity descriptor must be frozen before any attempt, with retained hashes
for engine executable, compiler-bearing library (if separate), supervisor, consumer adapter,
observer and harness. It must name implementation/version, exact compiler entrypoint, launch
argv, environment and working-directory policy. A mutable `python` PATH lookup, image tag,
`sys.version` or source hash alone is insufficient. The live image/callable must be associated
with that expected selection without a hash-to-launch or callable-rebinding gap.

This is minimum selected-consumer identity, not a full library/dependency lock. The real
profile requires a reviewed mechanism for identifying the actual selected compiler callable
and observing its entry with the complete argument tuple. That mechanism and concrete
engine pins are **not yet supplied by the repository**. Missing qualification must produce
PROFILE_UNQUALIFIED; implementers may not improvise a Python wrapper, tracing hook or audit
hook and claim it is equivalent. Qualification must document whether a probe sees original
bytes or transformed input, whether it can veto before entry, and what bypasses it covers.
An event reporting outgoing intent or only a filename is insufficient.

Independent observation must establish all of:

1. Hooks/observers armed before the attempt; no earlier unbound entry occurred.
2. Live A provenance/association, seals and complete read; A→B derivation and retained B.
3. Expected consumer selected, exact incoming source object B and all five remaining
   arguments at the receiving boundary, once. Record intent and observed entry separately.
4. Independent protected-object read agrees byte-for-byte, and live identity checks show
   the received B is the derivative retained for this attempt, not an equal-byte substitute.
5. No payload reopen, source redirection, fallback or unapproved second invocation occurred.
6. Terminal observation and required evidence finalized before ACCEPT is serialized.

The observer must be distinct from the delivery function and must not infer receipt from
that function's success return. For the surrogate, an independently installed function-entry
observer bound to the fixed surrogate code object observes incoming arguments before its
body; a separately defined observer validates A and B. Counts come from entry events, not
read counts or return values. Consumer substitution is checked before dispatch and on entry.
This is a trusted harness boundary, not separate-process security.

For a future real profile, qualification must supply equivalent or stronger actual-entry
observation. Internal compiler correctness and downstream interpretation remain assumptions.
Wrong/absent observation cannot be repaired by rerunning the attempted consumption.

## 5. Source selection, environment and no reopen

At the selected bytes-callable interface no source pathname reopen is necessary. The fixed
filename is diagnostic. Direct caller-supplied bytes avoid the source/module resolver for
this one input; that fact does not prove ambient imports are globally blocked.

Future test startup uses a reviewed fixed executable selection and empty user-supplied
environment, with no credentials and no PATH lookup. Absolute launch arguments and an empty,
exclusive temporary working directory are independently checked before arming. No source
selection via stdin, `-m`, `-c`, filename argv, PYTHONPATH, PYTHONHOME, startup hooks or user
site is allowed. Runtime-internal paths/stdlib imports needed to run the harness remain
explicit trusted bootstrap inputs, not a proven lock. Unknown environment input refuses,
even if thought harmless. No environment values containing secrets may enter evidence.

The future surrogate has no source-open, evaluation, compilation, import, network, subprocess
or callback behavior. It only accepts the fixed typed tuple, counts/hashes/compares and returns
a fixed observation tuple. Test setup may create synthetic decoy paths before arming but
must never consume them. Independent no-reopen and unexpected-call guards must cover the
attempt interval; lacking coverage refuses. These guards are not a production sandbox.
If actual engine initialization requires uncontrolled source staging or reads, STOP; do not
add an immutable-file fallback to this profile.

## 6. ACCEPT and ordered REFUSE contract

ACCEPT requires the qualified profile, valid expected descriptors, fresh witnessed A,
complete exact B derivation, expected consumer/callable, exact arguments, armed independent
observers, one received-input event bound to B, no forbidden reopen or redirection, matching
independent observation, and complete terminal records. Source execution success is neither
required nor allowed in the surrogate. A real-profile entry can be evidenced even if a
compiler later rejects syntax, provided the permitted terminal outcome is independently
recorded; that outcome cannot turn missing entry evidence into ACCEPT.

The evaluator uses the following fixed order. Before invocation any failed prerequisite
stops dispatch. After an attempted entry, any newly discovered violation gives REFUSE.
When several predicates fail in the finalized evidence, choose the first listed code;
never retry a failed attempt. Where evidence cannot establish a predicate, use the missing
observation/record code rather than invent a substantive violation.

| Priority / stable code | Exact failed condition |
| --- | --- |
| 01 RECORD_INVALID | Invalid schema/types/canonical bytes, duplicate/unknown/missing fields, invalid sequence or cross-attempt reference. |
| 02 PROFILE_UNQUALIFIED | Real profile lacks reviewed engine/observer qualification, or profile is unknown. |
| 03 EXPECTATION_INVALID | Expected identities absent/malformed or derived from candidate observations rather than frozen descriptor. |
| 04 WRONG_PROTECTED_OBJECT | Presented A lacks witnessed provenance, expected membership/association, type, size or exact Q. |
| 05 WRONG_LOADER | Executable/compiler-bearing image or live consumer code identity differs from expected. |
| 06 SOURCE_REDIRECTION | Unexpected environment, PATH selection, cwd policy or redirected source channel. |
| 07 WRONG_ENTRYPOINT | Consumer entrypoint or fixed input parameters differ, including alternate filename/mode/flags. |
| 08 OBSERVER_NOT_ARMED | Entry precedes hook establishment or any unbound prior invocation is observed. |
| 09 PATHNAME_REOPEN | Any attempted payload pathname reopen or filesystem fallback after validation, whether bytes match or not. |
| 10 OBJECT_SUBSTITUTION | Previously valid A or B is replaced after binding, including equal-byte replacement or different FD object. |
| 11 INPUT_IO | Derivative read errors or returns fewer bytes than min(observed size,4); no inferred truncation. |
| 12 INPUT_TYPE | B is not exact bytes. |
| 13 INPUT_TRUNCATED | A complete observed byte argument has length below 3. |
| 14 INPUT_APPENDED | A complete observed byte argument has length above 3. |
| 15 INPUT_ALTERED | Length 3 but wrong bytes/hash. |
| 16 INVOCATION_COUNT | More than one entry, or normal terminal completion without exactly one expected entry. |
| 17 OBSERVATION_MISSING | Required independent association/read/entry/no-reopen evidence absent or mutually inconsistent. |
| 18 ATTEMPT_INCOMPLETE | Crash/abort/lost terminal observation or truncated valid journal prefix; never infer acceptance. |

Input-corruption tests must isolate 11–15 before an entry occurs; they must not also substitute
a bound object and expect a lower-priority input code. Missing entry evidence is 17; observed
zero entries on otherwise complete normal termination is 16; a crash without entry proof is
18 when other required observations up to that point are present. An unbound consumer call
before PREPARED is 08 in a recovered refusal record; it cannot become a normal ACCEPT.
A post-binding wrong source/object is 10 even when its bytes also differ. Refusals do not
claim prevention if discovered after entry: `attempted` and observation records expose that.

## 7. Bounded future substitution matrix

One positive P01: fresh exact fixture, witnessed Q/A→B, fixed tuple and expected surrogate,
one armed incoming-argument observation, matching independent read and complete record.
A fresh equal repetition must produce byte-identical canonical terminal evidence (same
fixed case label and expected descriptors); freshness is not claimed by that equality.

| Case | Injection / required result |
| --- | --- |
| N01 | Wrong initial protected object, including equal-byte unrelated memfd → WRONG_PROTECTED_OBJECT. |
| N02 | Incomplete positioned read from correctly sized A → INPUT_IO. |
| N03–N05 | Complete derivative candidate truncated/appended/same-length altered before binding → INPUT_TRUNCATED / INPUT_APPENDED / INPUT_ALTERED. |
| N06 | Mutable/text/subclass derivative → INPUT_TYPE. |
| N07 | After valid binding give a different live A/FD object → OBJECT_SUBSTITUTION. |
| N08 | Valid A exists but another source B is delivered; test different-byte and equal-byte objects → OBJECT_SUBSTITUTION. |
| N09 | Alter a decoy source pathname, then attempt reopen → PATHNAME_REOPEN; no decoy execution or read needed. |
| N10 | Substitute expected executable/consumer selection → WRONG_LOADER before dispatch. Real executable substitution remains unproven by a surrogate stand-in. |
| N11 | Invocation filename/entrypoint selects another source → WRONG_ENTRYPOINT. |
| N12 | PATH/environment/cwd or input channel redirects selection → SOURCE_REDIRECTION; include PYTHONPATH and PYTHONHOME separately. |
| N13 | Entry before hooks armed / without prepared binding → OBSERVER_NOT_ARMED. |
| N14 | Remove independent entry/association evidence while consumer result remains valid → OBSERVATION_MISSING. |
| N15 | Controlled abort after ATTEMPTED with valid prefix and no terminal outcome → ATTEMPT_INCOMPLETE. |
| N16 | Filesystem fallback after protected read failure proposed by adapter → PATHNAME_REOPEN when observed; never perform it to obtain a positive. |
| N17 | Extra entry, and separately no entry on normal completion → INVOCATION_COUNT. |
| N18 | Change attempt linkage, omit schema field or duplicate key → RECORD_INVALID. |
| N19 | Missing expected identity descriptor → EXPECTATION_INVALID. |
| N20 | Request real profile without qualified engine/observer → PROFILE_UNQUALIFIED. |

These are adapter/boundary refusal tests, not fuzzing, compiler attacks or E0 runs. Tests
must use actual received arguments for binding checks, not an expected receipt substituted
for observed behavior. A stand-in for an executable identity failure must be labelled as
such; it does not prove kernel process-image enforcement. If multiple injections occur,
assert the ordered code and preserve all independently observed violations.

## 8. Complete attempt record and canonical serialization

This section fixes the logical evidence model; no files are created by this circuit.
A future supervisor must create an exclusive new evidence location, never truncate or
resume an old attempt, and retain incomplete prefixes on failure. A fixed `case_id` is a
test label, not a unique cryptographic run identity. An external custodian associates the
exclusive attempt location with its records. Replay resistance is outside this slice.

Canonical C: UTF-8 JSON, ASCII strings only, keys lexicographically sorted, no insignificant
whitespace, no duplicate keys, exactly the schema fields, integers in ordinary base-10
(no float/exponent/negative zero), booleans as true/false, null as null, no BOM, final LF
for each journal record. Reject input not equal to its canonical reserialization. Standard
JSON escaping applies; slash unescaped; control characters forbidden in field values.
Hashes are lowercase 64-hex SHA-256 of exact canonical bytes including LF. No timestamps,
PID, numeric FD/inode, temporary path or random ID in canonical output. Raw host observations
may live in a separately retained noncanonical witness attachment; canonical evidence binds
its logical facts, not volatile identifiers or a volatile attachment hash.

Expected descriptor E has exactly these fields:
`profile` (one of the two names), `case_id` (P01 or N01…N20, optional decimal subcase suffix
joined by a dot), `spec_sha256`, `engine_sha256`, `compiler_image_sha256`,
`adapter_sha256`, `observer_sha256`, `harness_sha256` (all hashes), `engine_label`,
`entrypoint` (nonempty ASCII strings), `input_sha256` (F), `input_length` (3),
`manifest_sha256` (M), `root_sha256` (S), `filename` (fixed diagnostic label),
`mode` (exec), `flags` (0), `dont_inherit` (true), `optimize` (0),
`launch_argv` (ordered ASCII string array), `environment` (empty object),
`cwd_policy` (`exclusive-empty-temp`). In the surrogate, compiler_image_sha256 equals
engine_sha256 and explicitly identifies the host executable only, not a used compiler.
Concrete engine/code hashes and absolute launch argv must be frozen in a separately reviewed
implementation plan before tests, not auto-approved from current observations. The spec hash
is external to this document, avoiding self-reference. A negative expectation test preserves
both the frozen E and the invalid candidate in its witness evidence.

Every event has exactly:
`schema` (`ns001.h2a2.consumption-event.v1`), `expectation_sha256` (hash of C(E)),
`sequence` (0-based contiguous int), `state` (below), `attempted` (bool), `code`
(null or table code), `previous_sha256` (null for first, otherwise previous C(event) hash),
`facts` (object specified below). Unexpected/missing fields refuse. Events are append-only;
flush PREPARED and ATTEMPTED before dispatch. This is a trusted-supervisor durability
requirement, not an assertion of power-loss durability from language buffering alone.

- PREPARED: sequence 0, attempted=false, code=null. facts has exactly `profile_qualified`,
  `expectations_valid`, `protected_valid`, `consumer_valid`, `selection_valid`,
  `observers_armed`, `derivative_valid` (all true). Not written if these checks fail.
- ATTEMPTED: sequence 1, attempted=true, code=null; facts is exactly `{}`. This means
  dispatch has been committed, not that the consumer actually entered.
- ACCEPTED: sequence 2, attempted=true, code=null; facts is exactly W below. It is written
  only after receiving-boundary and terminal evidence is complete and every acceptance
  predicate holds. Real profile claim and surrogate profile claim must remain distinct.
- REFUSED: terminal at sequence 0, 1 or 2 after the corresponding valid prefix, code is
  mandatory, attempted equals whether ATTEMPTED exists (or unbound entry was observed).
  facts is W with unknown/unreached values null. Pre-dispatch failure permits a lone REFUSED.
  Do not fabricate PREPARED facts to fill a failed precondition.

W has exactly: `protected_valid`, `derivation_bound`, `consumer_valid`, `selection_valid`,
`observers_armed`, `same_derivative`, `independent_agreement`, `no_reopen` (bool or null);
`received_length` (nonnegative int or null), `received_sha256` (hash or null),
`entry_count` (nonnegative int or null), `terminal_outcome` (null or one of
`surrogate_returned`, `compiler_returned`, `compiler_rejected`, `aborted`). ACCEPTED requires
all booleans true, length 3, F, count 1 and the appropriate non-aborted outcome.
Independent entry witness must also check the exact tuple against E; selection_valid includes
that comparison. W is the canonical summary, not an authenticated witness by itself.

Separate incoming-argument and protected-object witness observations must be retained and
independently checked before constructing W. Their source and complete logical evidence must
be available to a reviewer; a consumer's returned W or self-asserted true fields are not
acceptable. Live object relations are witnessed while references remain live; addresses and
FD numbers may not be reconstructed from hashes after the fact.

On controlled abort the supervisor appends REFUSED/ATTEMPT_INCOMPLETE to a valid prefix.
On supervisor crash, retain the prefix verbatim; a separate recovery report references its
hash and reports ATTEMPT_INCOMPLETE, without appending fictitious original events or resuming
the attempt. Malformed/truncated final record is retained raw; the reviewer records the
last valid prefix and refuses. No missing terminal record ever counts as ACCEPT. Recovery
reports use the same event schema as a standalone REFUSED, sequence 0, previous_sha256=null,
and W null except terminal_outcome=aborted; expectation_sha256 identifies E. Their distinct
external recovery location prevents misrepresenting them as the original journal.

## 9. Runtime-lock separation and smallest future slice

A bounded observation can establish that identified top-level input B reached an identified
entry under explicit trusted-engine/observer assumptions. It does not establish immutable
transitive runtime, interpreter implementation correctness, imports, native libraries,
bootstrap loading, reproducible installation or every later code-generation path. These
remain `dependency_runtime_lock` and subsequent external-trust-root evidence obligations.
The real consumer still needs minimum qualified identity; deferring the full lock does not
permit an arbitrary or unobserved engine. If minimum identity cannot be established without
full locking, STOP and record the dependency instead of silently beginning that gate.

**One smallest future implementation slice:** additive offline bytes-callable surrogate
using the fresh inert `abc` sealed-object derivative and the exact six-argument interface
above, fixed receiver and independent receiving-entry observer, P01/repetition and the bounded
N matrix. The receiver must never call compile/exec/eval/import, obtain a client, launch a
child, or access a network. Scientific paths and real E0 entrypoints are unavailable as
inputs. Receipt profile is always surrogate; a request for real profile refuses. The test
harness may inspect and hash its own approved inputs but cannot discover or run scientific
modules. No implementation file or test is created here, and no existing first-slice file
is authorized to change. Any reuse of first-slice logic must preserve its frozen behavior.

This faithfully models the bytes-argument input interface and substitution boundary only.
It does not model compiler internals or prove real compiler entry. Selection/qualification
of actual engine observation remains a later document decision; replacing the surrogate with
compile is a scope change requiring explicit authorization, not a configuration option.

## 10. Abort conditions, preservation and disposition

STOP rather than improvise if the actual proposed boundary cannot be identified; independent
incoming-input observation is unavailable; exact parameters/identity pins are missing; a
loader needs uncontrolled pathname reopening; a new staging backend or transformation is
needed; protection/object association cannot be retained; real compilation/execution would
be needed under surrogate authority; E0/scientific imports become reachable; minimum engine
identity is inseparable from full runtime locking; or evidence requires credentials,
network, live clients or unpublished state. Missing evidence remains PARTIAL/NOT VERIFIED.

Pre-commit preservation check: all 203 pre-existing tracked files match reviewed HEAD;
only this new specification changed. The completed first slice's implementation SHA-256 is
`d15ddd0b3d689592398987e62ce3135ee8a61e48ccd48cfa511d4870ac0b0023` and harness SHA-256 is
`67150d764cfde33e1d72837cf3ec518c3469a7f617ec19808d30c0762434b647`, unchanged.
H2A1, scientific artifacts, frozen contracts and prior receipts are unchanged. No runtime,
compiler/loader/client, tests or E0 were invoked; document inspection and Git operations only.

- identified real consumption boundary: proposed Python bytes argument at compiler entry; existing feasibility pathname/import routes inspected; live E0 entrypoint and actual engine/observer qualification remain unselected.
- allowed claim: exact protected-byte derivative received at the qualified input boundary; surrogate success says only surrogate receipt, never actual compilation/execution.
- prohibited claims: execution/runtime/compiler correctness, dependency/import/client/transport/response/scientific identity or correctness, E0 success and full-gate resolution.
- protected consumption object: immutable exact bytes B, witnessed byte-preserving derivative of a fresh valid sealed A; not an FD passed as source.
- loader/compiler identity requirements: frozen expected executable/compiler image and callable/observer/harness identity with live association; real profile blocked without qualification.
- independent observation rule: receiving-entry arguments and live A→B association independently witnessed before evidence finalization; outgoing intent alone fails.
- no-reopen rule: bytes delivery only; diagnostic filename cannot locate source; all payload reopens/fallbacks refuse.
- ACCEPT criteria: all identity, binding, single-entry, independent observation and complete-record checks; no execution-success requirement.
- REFUSE criteria: ordered stable codes 01–18; no retry, fallback or fabricated missing evidence.
- substitution-test matrix: P01 with equal repetition and N01–N20 bounded cases; surrogate/real evidence never conflated.
- attempt-record contract: canonical descriptor plus append-only PREPARED/ATTEMPTED/ACCEPTED or REFUSED events; preserved incomplete prefixes and distinct recovery refusal.
- dependency_runtime_lock boundary: minimum consumer identification required; complete interpreter/import/library/dependency closure remains deferred and unresolved.
- smallest future implementation slice: offline inert sealed-object-to-bytes-callable surrogate and independent entry observer only, after review and separate authorization.
- abort conditions: unidentified/unobservable boundary, missing identity, uncontrolled reopen, changed mechanism, E0/runtime scope expansion, inseparable locking or external/live evidence dependency.
- implementation-ready: PARTIAL; surrogate contract specified, actual compiler boundary lacks engine/observer qualification; no implementation authorized here.
- external_trust_root status: first non-executing handoff verified; actual compiler-input boundary unproven; full gate unresolved.
- H2A1 status: VERIFIED for scoped prospective custody/publication auditability; unchanged.
- H2A2 status: first slice independently VERIFIED; this downstream specification is prospective only; all eight full H2 gates unresolved.
- E0 status: HOLD.
- one next bounded action only: independent document-only review of this acceptance specification, including its surrogate claim ceiling, observer qualification gap and attempt/refusal determinism.
