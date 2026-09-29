# NS-001 H2A2 consumption-boundary acceptance specification v0.1

## Basis, correction and authority

Preparation branch: `codex/e0-h2-preparation`.
Correction base: `9544fbebc013979e53f978c54c07e3f1e682bd35`; initially clean.
This document-only correction addresses B1–B4 from
`docs/e0/h2/NS-001_H2A2_CONSUMPTION_BOUNDARY_ACCEPTANCE_REVIEW_v0.1.md`.
The earlier specification and independent review remain available at that commit; the
review is not edited. Only this specification and the new correction receipt change.
No compiler, interpreter, loader, client, application subprocess or live runtime is invoked.

**Surrogate implementation readiness: YES at the contract level, subject to independent
review and separate implementation authorization.** Concrete future implementation hashes
are acceptance inputs to freeze before testing, not permission to change the contract.
The real-engine profile remains unqualified and unavailable. No E0 entrypoint is selected.

The first sealed-memfd slice and its frozen contracts remain unchanged. Normative inherited
inputs are the snapshot-handoff acceptance specification, handoff-mechanism selection,
correction review, runtime-trust-root design and H2 evidence declaration contract in
`docs/e0/h2/`, all pinned at the correction base. Sections 1–3 below retain the previously
reviewed source-boundary, claim and protected-input design. Sections 4–10 replace the former
identity, witness, refusal and lifecycle provisions; no superseded provision is cumulative.

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

## 4. B3 — three separate identity boundaries

### A. Qualified surrogate, and only the surrogate

The receiver is a fixed, top-level Python function named `receive`, profile
`ns001.h2a2.compile-input-surrogate.v1`, with precisely six positional arguments from
section 3 and no defaults, variadic arguments, keyword overrides, closures or callback
parameters. Its only permitted body is checking these fixed types/values and returning
`("surrogate_received",3,F)` on the positive path. It may count/hash/compare immutable
bytes, but must not compile, evaluate, interpret, import, open files, launch processes,
access clients/network, mutate input or resolve a pathname. `mode="exec"` is inert
metadata, never an instruction to execute. Its returned tuple is not the independent witness.

Before testing, freeze exact SHA-256 identities of the retained implementation artifact
containing receive, observer artifact, and harness artifact. Name receive by artifact-relative
module name plus function name, and bind its live function/code-object references during
trusted bootstrap. Observer and supervisor are distinct functions/state within the pinned
harness/observer artifacts, not an unspecified fourth binary. Any supervisor source outside
those artifacts is forbidden by this profile. Verify artifact bytes before bootstrap; trust
that the reviewed bootstrap associates those bytes with these live functions. This is an
explicit assumption, not proof of Python loaded-bytecode origin. Rebinding the receiver or
its live code object after bootstrap is detected by comparison to the retained references.
A version string or matching input hash cannot substitute for receiver association.

The surrogate requires NO Python executable hash, compiler-library hash, full Python build
lock, stdlib/import/package closure or full ambient-environment closure. Those are not
ACCEPT fields. The trusted interpreter/harness is a declared assumption. The two artifact
roles may share a file; their identities are still recorded separately in the descriptor.
No real executable-substitution guarantee follows from substituting a surrogate callable.

Bootstrap may load only the reviewed harness, observer, receiver and their declared test
support before arming; its startup path is not the payload source channel. A harness filename
on bootstrap argv is allowed and not confused with a payload filename. Scientific modules,
clients and payload compilation are prohibited. Bootstrap runtime/import correctness is
assumed, not verified here. The supervisor then sets up an exclusive synthetic working
location, arms the monitors, and admits attempts through the fixed six-argument interface.
No user-provided source selector, PATH lookup, environment lookup, stdin, `-m`, `-c` or script
path can choose the payload or receiver during an attempt. The fixed request schema below
has no such channel; a nonempty source-environment or a different channel/cwd policy refuses.
This is explicit source-selection control, not a claim of a hermetic host environment.

### B. Later real engine: additional facts, not yet proven

A real profile would additionally need retained implementation/runtime family, exact
version/build and interface documentation, executable and compiler-bearing image identities,
association of the running consumer with those identities, actual compiler-callable entry,
complete source argument/mode selection semantics, and a qualified receiving-entry observer.
Its observer must distinguish original input from compiler-transformed data and document
bypasses. No wrapper-intent report, surrogate trace or trusted-bootstrap assumption alone
qualifies that actual compiler. This contract always refuses the real profile with
PROFILE_UNQUALIFIED; it defines no real-engine ACCEPT path or implementation switch.

### C. Full runtime lock: separate, unresolved

Immutable interpreter/native/stdlib/package/import closure, reproducible offline installation,
all environmental influences and later executed-code provenance remain outside this slice.
Neither A nor identifying a consumer in B establishes those properties. Do not begin
`dependency_runtime_lock` to implement the surrogate.

## 5. B1 — registration, durable ordering and recovery

### Identity and custody boundary

One supervisor exclusively owns a retained evidence store. Before accepting work it obtains
an exclusive store lock; lock failure means no attempt starts. A retained `store.json` has
exactly `schema="ns001.h2a2.store.v1"` and `namespace` (64 lowercase hex characters assigned
and retained by the evidence custodian). The custodian must not reuse this namespace for a
new/clone/reset store. Namespace assignment is a custody input, not derived from a timestamp
or silently regenerated after restart. Uniqueness is within this preserved custody regime,
not a mathematical global-uniqueness or adversarial anti-rollback claim.

Under the lock reserve the next ordinal, one plus the largest existing attempt-directory
ordinal, starting at 1. Names are ordinary positive decimal integers without leading zeros.
Create that directory exclusively and synchronize its parent directory before preparation,
payload acquisition or receiver entry. Never delete or reuse any reserved directory, even
empty or malformed ones. Attempt ID is `namespace + ":" + decimal ordinal`. This is unique
and deterministic given the preserved store inventory. Conflicting/unknown entries or a
lost/rolled-back store stop work for custody review; no inferred safe ordinal.

The synchronized reservation is the start of a tracked attempt. Before it completes, no
preparation or receiver entry may occur; failure there is a store-registration failure,
not an invisible permitted consumption attempt. A reservation surviving a crash, even with
no files, is visible and will be recovered as ABORTED. This closes the former pre-PREPARED
gap. A crash before any reservation permits no consumer activity under this contract.

### Exact minimum records and persistence

Canonical serialization C in section 8 applies to every record. The store holds the frozen
expected descriptor E under its hash before any attempt that references it. Immediately
after reservation write `registration.json` with exactly:
`schema="ns001.h2a2.registration.v1"`, `attempt_id`, `expectation_sha256`,
`request_sha256`. The candidate request is retained as `request.json` (raw bytes even if
malformed), with request_sha256 over those exact bytes. Write request before registration.
Synchronize both files and the attempt directory before checks or consumer activity.
A missing/partial registration or request is an interrupted reserved attempt, not deletable
scratch space. Valid registration always names a valid retained expected E; missing E stops
preparation and becomes a refusal/recovery fact, never current-host auto-approval.

`events.jsonl` is append-only; each complete event is written and synchronized before the
next permitted action. PREPARED is persisted only after preconditions; ATTEMPTED must be
persisted and acknowledged by the supervisor before dispatch. Required witness bytes must
be synchronized before a normal terminal event refers to their hash. Use file synchronization
and synchronize directory entries when creating them, not just language-level flush.
The fault model is process interruption with an honest filesystem honoring successful sync;
media loss, malicious deletion, rollback, lying storage/kernel and process compromise are
residual assumptions. A sync/write error stops dispatch immediately; preserve available
bytes for recovery. No fallback store, retry of consumption or repair of an attempt.

### State machine

Registration is a durable precursor, not a successful validation state:

- RESERVED/registered → PREPARED → ATTEMPTED → ACCEPTED or REFUSED.
- RESERVED/registered → REFUSED for a precondition failure; no PREPARED fiction.
- PREPARED → REFUSED if a later pre-entry condition fails before committed dispatch.
- Any nonterminal reserved attempt → ABORTED by recovery after interruption.

ACCEPTED and REFUSED are terminal and immutable. ABORTED is a terminal recovery disposition,
never a path to ACCEPTED or resumption. ATTEMPTED means committed dispatch, not proof of
receiver entry. Pre-entry failure has `entered=false`; post-entry refusal reports actual
observed entry. Missing entry evidence is unknown, not false. Unexpected early receiver
entry is recorded by the lifetime sentinel from section 6; it is never laundered into a
valid PREPARED/ATTEMPTED chain.

On restart, inspect every reservation before admitting a new attempt. A well-formed normal
terminal chain with valid referenced records remains terminal. Otherwise preserve ALL raw
files unchanged and create a separate ABORTED recovery record. Recovery is idempotent: if
its canonical bytes already exist and equal the independently recomputed expected result,
return that disposition; conflicting bytes stop the store for custody review. An interrupted
recovery write stays visible as a `.partial` file; after validating it as a prefix of the
recomputed record, complete recovery via a fresh temporary file and atomic final rename,
retaining the partial bytes. Never modify the original attempt journal. An invalid partial
recovery file stops automatic recovery. No additional consumer entry occurs during recovery.

Recovery explicitly binds both the entire raw journal and its maximal valid prefix, plus
registration/request/witness bytes or absence. It cannot declare successful receipt from
an incomplete normal attempt. Thus malformed/torn tails and pre-PREPARED crashes remain
visible. ABORTED is a refusal of completeness, not evidence that the consumer did or did not
run. The schemas in section 8 encode these bindings without inventing extra fields.

## 6. B4 — independent witness and source-operation coverage

### Independence and fixed observer location

An in-process witness is sufficient for this offline synthetic claim, under a trusted
harness/process assumption. No separate process is required. Its code path and state must
be distinct from receive and the delivery adapter: the receiver gets only the six arguments,
not the witness state, expected descriptor, writer or acceptance/finalization callback.
Observer state retains A, the exact B reference, selected receiver/function code object,
attempt ID and persisted ATTEMPTED acknowledgement. Consumer output cannot set witness facts.
The supervisor separately validates serialized witness content before finalizing acceptance.

Select a function-entry observer using the trusted Python profiling call-event interface,
bound to the retained `receive.__code__` reference, observing that entry's actual argument
locals before its body. A lifetime sentinel is installed before reservations and counts
receiver-entry events even when the per-attempt observer is unarmed. These may be separate
handlers driven by the same profiling dispatcher, with separate state. This explicitly
supports the early-entry negative test. If the profiling mechanism is unavailable, replaced
or already owned by an incompatible profiler, refuse; never silently use a returned tuple
as evidence. The contract relies on trusted profiling/object semantics, not real native
compiler-entry observability or hostile Python isolation.

At the receiving event the witness independently determines exact type, length and SHA-256
of actual source bytes; compares the reference to retained B; checks all five other typed
parameters; verifies receiver code identity; and checks A's live provenance/association,
length and Q. It separately reads A with the same bounded complete-read rule and compares
its bytes to the received source. It does not reuse the consumer's digest or result.
Keep A/B/receiver references live through terminal observation; equal-byte B replacement
fails reference association. Record actual return via the corresponding return event and
match it to the one call frame retained privately. An exception/aborted return is not the
fixed tuple; no arbitrary repr or exception text is serialized.

### No-reopen/fallback coverage in this bounded process

The reviewed delivery adapter, receiver and observer have no payload pathname operations.
All test-adapter requests for payload open/reopen, source-channel redirect or fallback go
through a fixed harness guard that records the request and denies it before I/O. Supported
operation labels are exactly `payload_open`, `payload_reopen`, `filesystem_fallback`,
`source_redirect`. Payload source access after sealing is through retained descriptors only.
Audit of the pinned attempt code must find no direct bypass via open/io/Path, /proc or /dev
aliases, imports, mmap, callback, subprocess or native extension calls; unsupported paths
make qualification fail rather than extending the claim. Evidence-journal writes by the
supervisor and pre-sealing synthetic acquisition are separate, allowed operations, not
payload reopen. This is coverage of the fixed trusted program and deliberate test adapters,
not interception of every hostile process syscall. A bypass contrary to reviewed code is
outside the trusted-process assumption and never called a verified sandbox.

### Exact retained witness

One separate canonical `witness.json` is finalized before a normal terminal event. It has
exactly these keys (null means genuinely unavailable/unreached, not presumed success):

- `schema`: `ns001.h2a2.consumption-witness.v1`; `attempt_id`; `expectation_sha256`.
- `consumer_sha256`, `observer_sha256`, `harness_sha256`: expected artifact hashes;
  `entrypoint`: observed qualified name or null.
- `observations`: ordered array of records defined below.
- `violations`: unique stable refusal codes in section 7 rank order, independently supported
  by observations and the retained request; never invented to match an expected test result.

Each observation has exactly `index` (contiguous integer starting 0), `kind`, `data`.
Allowed kinds and exact data keys:

| kind | data fields and meaning |
| --- | --- |
| `protected` | `valid` bool, `initial` bool, `association` bool, `seals_exact` bool, `length` nonnegative int or null, `sha256` hash or null. Initial record describes admission; later record checks retained association. |
| `derived` | `type` bytes/nonbytes, `length` int or null, `sha256` hash or null, `from_retained_A` bool, `reference_retained` bool. Values come from the actual derivative candidate, not expected input. |
| `qualification` | `profile_allowed` bool, `capability_qualified` bool, `consumer_sha256` observed artifact hash or null, `artifact_match` bool, `callable_match` bool, `entrypoint` observed name or null, `parameters_match` bool, `source_selection_valid` bool. Independent Q/I checks against E and the retained request, including live receiver references. |
| `armed` | `sentinel_active` bool, `entry_hook_active` bool, `guard_active` bool, `consumer_bound` bool. |
| `dispatch` | `attempted_event_sha256` hash, `persisted` bool. Written only after actual sync acknowledgement. |
| `entry` | `consumer_match` bool, `entrypoint` ASCII string, `source_type` bytes/nonbytes, `length` int or null, `sha256` hash or null, `same_B` bool, `same_A` bool, `independent_A_equal` bool or null, `parameters_match` bool, `parameters` as below, `after_dispatch` bool, `hook_armed` bool. |
| `guard` | `operation` one of the four guard labels, `denied` bool. |
| `return` | `matches_entry` bool, `result` fixed_tuple/other/aborted. |
| `end` | `entry_count` nonnegative int from sentinel, `observer_entry_count` nonnegative int, `same_A` bool or null, `seals_exact` bool or null, `no_reopen` bool, `guard_coverage` bool, `outcome` returned/precondition_refused/aborted. |

`parameters` is null if no well-typed five-parameter tuple was available; otherwise an
object with exactly `filename`, `mode`, `flags`, `dont_inherit`, `optimize`, carrying actual
ASCII strings/int/bool/int values. Unsupported types or non-ASCII strings are not coerced:
parameters=null and parameters_match=false. Nonbytes source has length/hash null. Reference
comparisons and descriptor associations are performed live; only their logical results
are serialized. Their truth remains a trusted-witness assumption. Numeric IDs and volatile
addresses cannot substitute for observations.

The positive sequence is exactly: protected(initial=true), derived, qualification, armed,
dispatch, entry, protected(initial=false), return, end. Qualification's booleans are all
true and its artifact/name match E. Entry's protected read/check is independent; the
following protected record records its results. Positive end counts are both 1 and all
required association/coverage checks true; return is fixed_tuple/matches_entry=true.
The profiler may collect the return before other code persists observations, but must retain
its observed order. All records are assembled in event order, not reordered to fit ACCEPT.
A guard event may occur anywhere after initial protection; it always prevents acceptance.
Early-entry tests may have an entry before armed/dispatch, reported by the sentinel with
hook_armed=false. Unknown facts are null or absent observations, never synthesized passes.
No additional observation kinds are permitted. Negative runs preserve actual observation
order: preparation kinds occur at most once in their listed order; dispatch at most once;
each observed entry has its own following protected check and return when those occur.
Repeated entry/return groups are retained for invocation-count faults. Sentinel-observed
premature entries may precede the preparation kinds; do not reorder them. Guard records
may interleave after protection. End occurs exactly once and last in a normal witness.
An interrupted witness may be a prefix; normal REFUSED requires an end record.
No witness result is inferred from expected bytes. Removing an entry/association record
while leaving a valid consumer return must lead to OBSERVATION_MISSING. The terminal event
binds the entire witness SHA-256, so attachment swapping or a witness from another attempt
is a detectable mismatch. The witness contains no terminal-event hash; there is no cycle.

## 7. B2 — staged validation and single-code precedence

Preserve the eighteen names, but the following predicates/order replace the old priority
numbers. A candidate request is not the frozen descriptor or evidence journal. Missing or
malformed candidate expectation fields are EXPECTATION_INVALID; malformed evidence records
are RECORD_INVALID. Initial A admission and later substitution are separate phases.

Preparation phases run in this exact order and stop on first failure: protected object (P),
derivative (D), receiver qualification (Q), source selection/invocation (I), then hooks (H).
E and request structural checks precede P. Retain observed secondary facts without running
new phases just to accumulate diagnostics. After ATTEMPTED, only monitoring/final evidence
checks apply; do not reclassify later A substitution as failed initial admission.

For a normally completed attempt, form the set of evidenced applicable codes below and
choose the smallest rank. Serialize exactly ONE `primary_code`; diagnostics contains only
the other supported codes, unique and rank ordered. Missing evidence does not imply that
an unobserved higher-ranked substantive violation occurred.

| rank / code | Phase and exact trigger; isolated reachability test |
| --- | --- |
| 1 RECORD_INVALID | Evidence journal/registration/witness has a complete but schema-invalid, noncanonical, wrong-ID/hash-linked record. Test complete altered witness linkage. Not candidate request validation; torn tail is handled by recovery below. |
| 2 EXPECTATION_INVALID | Candidate request absent/malformed or candidate expected-descriptor hash does not equal retained frozen E; E unavailable/invalid before dispatch. Test omitted candidate expected hash. |
| 3 WRONG_PROTECTED_OBJECT | P only: initial A type, size, Q, expected identity or witnessed origin/association invalid. Test unrelated equal-byte initial memfd. |
| 4 INPUT_IO | D only: bounded derivative read errors or is incomplete relative to min(observed size,4). Test short read of correctly sized A. |
| 5 INPUT_TYPE | D only: derivative candidate not exact bytes. Test bytearray candidate through labelled adapter. |
| 6 INPUT_TRUNCATED | D only: complete bytes candidate length less than 3. Test complete two-byte candidate before binding. |
| 7 INPUT_APPENDED | D only: complete bytes candidate length greater than 3. Test complete four-byte candidate before binding. |
| 8 INPUT_ALTERED | D only: length 3 but full bytes/hash differ. Test altered candidate before binding. |
| 9 PROFILE_UNQUALIFIED | Q: requested profile is not the fixed surrogate (real included), or declared program/observer capability audit is unqualified. Test real-profile request. |
| 10 WRONG_LOADER | Q: selected receiver artifact/function/code reference mismatches frozen surrogate identity. Also post-Q receiver rebinding detected at dispatch/entry. Test different live receiver, not Python executable substitution. |
| 11 SOURCE_REDIRECTION | I: source channel not protected_bytes, nonempty source_environment, or different cwd policy. Also guard source_redirect request. Test PYTHONPATH source override. |
| 12 WRONG_ENTRYPOINT | I: selected entrypoint or typed five input parameters differ from fixed tuple. Also differing actual parameters at entry. Test alternate diagnostic filename. |
| 13 OBSERVER_NOT_ARMED | H: required hook/guard not active; or sentinel witnesses entry without armed hook and persisted ATTEMPTED acknowledgement. Test premature entry with sentinel still active. |
| 14 PATHNAME_REOPEN | Monitoring: guard witnesses any payload_open/payload_reopen/filesystem_fallback request after validation. Denial still counts. Test denied decoy reopen. |
| 15 OBJECT_SUBSTITUTION | After successful admission/binding only: retained A association or B reference changes at dispatch/entry/final check. Test equal-byte replacement B or A. Never code 3 for this phase. |
| 16 INVOCATION_COUNT | Normal completion, reliable active sentinel evidence: count differs from 1 for a dispatched attempt. Test two entries or no entries with intact monitoring. No count requirement for precondition refusal. |
| 17 OBSERVATION_MISSING | Normal completion with missing/inconsistent required independent association, argument, coverage, entry or end evidence not already classified as structurally invalid. Test remove independent entry but keep valid return. A null unknown fact cannot satisfy ACCEPT. |
| 18 ATTEMPT_INCOMPLETE | Nonterminal attempt, interruption, incomplete/torn tail or absent normal terminal record: recovery disposition ABORTED only. Test interruption after ATTEMPTED. |

Recovery has a deterministic completeness decision before normal evaluation: if there is
no fully validated normal terminal chain, produce ABORTED. Its primary code is RECORD_INVALID
if any retained COMPLETE record is structurally invalid; otherwise ATTEMPT_INCOMPLETE.
A partial final line/file is an interrupted write, not a complete invalid record. Earlier
supported violations are diagnostics only for recovery; incomplete attempts are never
normal ACCEPT/REFUSE. Thus a torn tail cannot ambiguously select codes 1 versus 18.
A retained normal terminal with invalid evidence is preserved raw but is not a valid
terminal chain; recovery documents its invalidity rather than rewriting it.

ACCEPTED requires no applicable refusal, positive witness sequence, exact F/length/B link,
qualified surrogate/parameters, one receiving event after persisted ATTEMPTED, fixed return,
complete no-reopen coverage and synchronized witness. It says nothing about compilation or
source execution. Normal precondition REFUSED may have zero entries and partial witness
observations ending in precondition_refused; it is not missing-entry refusal. Nonterminal
normal failure records are not retroactively completed from inferred observations.

## 8. Exact record schemas and deterministic encoding

C is UTF-8 ASCII-only JSON with keys sorted lexicographically, no whitespace except one
final LF, no BOM, unique keys, exact fields, ordinary decimal integers (no negative zero,
exponents or floats), JSON booleans/null, minimal JSON escaping (quote/backslash only;
control characters forbidden in strings), slash unescaped. Reject any noncanonical input.
Hash means SHA-256 of exact bytes including LF, lowercase 64 hex. No time/PID/FD/inode/
temporary path appears in canonical records. Hash raw invalid evidence without normalizing it.

Frozen E has exactly: `schema="ns001.h2a2.surrogate-expectation.v1"`, `spec_sha256`,
`consumer_sha256`, `observer_sha256`, `harness_sha256` (retained artifact hashes),
`entrypoint` (artifact module + `.receive`), `interface="bytes-six-positional.v1"`,
`profile="ns001.h2a2.compile-input-surrogate.v1"`, `input_length=3`, `input_sha256=F`,
`manifest_sha256=M`, `root_sha256=S`. These are independently reviewed expectations frozen
before the acceptance run; computed observations cannot overwrite them. Spec hash is computed
externally; this document does not embed its own hash. No runtime binary fields are required.

Candidate request has exactly: `expectation_sha256`, `profile`, `entrypoint`,
`source_channel`, `source_environment` (ASCII string-to-string object), `cwd_policy`,
`parameters` (five-field object from section 6), `case_id` (P01 or N01…N20, optionally dot plus
positive decimal subcase integer). It carries no payload pathname. The valid values are E's
profile/entrypoint, protected_bytes, empty object, exclusive-synthetic, and section 3's exact
parameters. Malformed structure/types yield EXPECTATION_INVALID; well-typed but wrong values
reach their specific Q/I predicates. Source object A and derivative candidate are live harness
inputs associated with request/attempt, not JSON-deserialized capabilities.

Journal event has exactly: `schema="ns001.h2a2.consumption-event.v1"`, `attempt_id`,
`sequence` (0-based contiguous), `state`, `primary_code` (null or one code), `diagnostics`
(rank-ordered other codes), `previous_sha256` (null for 0, preceding event hash otherwise),
`witness_sha256` (null until terminal), `entered` (bool or null).

- PREPARED: first event, no code/diagnostics/witness, entered=false. Requires all phases pass.
- ATTEMPTED: after PREPARED, no code/diagnostics/witness, entered=null. Sync before dispatch.
- ACCEPTED: after ATTEMPTED, null code, empty diagnostics, witness hash mandatory, entered=true.
- REFUSED: first event, after PREPARED, or after ATTEMPTED; one code other than
  ATTEMPT_INCOMPLETE, witness hash mandatory, entered from actual observations (or null
  if unknown). No further journal events after normal terminal. Witness required even for
  ordinary precondition refusal; lack of it leads to ABORTED recovery, not a fabricated file.

Recovery file `recovery.json` has exactly:
`schema="ns001.h2a2.consumption-recovery.v1"`, `attempt_id`, `state="ABORTED"`,
`primary_code`, `diagnostics`, `registration_sha256`, `request_sha256`, `witness_sha256`
(each raw hash or null if absent), `journal_sha256` (hash of entire raw file, or null if absent),
`journal_length` (0 if absent, otherwise byte count), `valid_prefix_sha256` (hash of exact
maximal valid prefix bytes; empty-byte hash if none), `valid_prefix_length`,
`last_valid_sequence` (int or null), `entered` (bool or null from retained evidence only).
This distinct schema explicitly encodes the missing B1 prefix binding. Recovery never uses
an expectation hash as a substitute for attempt identity. Empty/missing journal differ via
journal_sha256. Recovery does not hash itself. Complete record invalidity and supported
secondary violations determine codes per section 7. Recovery with only an empty reservation
has all absent file hashes null, lengths 0, empty-prefix hash, entered=null and primary
ATTEMPT_INCOMPLETE. This is a deterministic distinct terminal disposition for that ID.

Canonical witnesses bind attempt IDs and expected descriptors; terminal events bind witness
bytes; recovery binds raw retained bytes. The expected source artifacts supply the reviewed
meaning of live comparisons. No cryptographic authenticity against a malicious witness is
claimed. Custody of the store, reservations and namespace is a required residual assumption.

Equal repetitions allocate different attempt IDs and therefore different whole-record hashes.
This intentionally replaces the earlier full-record byte-equality rule to satisfy unique
attempt identity. Determinism means equal full inputs INCLUDING attempt ID and observations
serialize identically. Tests must compare repeated serialization of the same retained record,
and compare repeat-run semantic observations after removing only attempt_id and its derived
link hashes; they must not reuse IDs or discard originals to manufacture byte equality.
The completed first slice's historical deterministic-ACCEPT claim is unchanged.

## 9. Bounded acceptance matrix and future implementation scope

One positive P01 uses fresh exact inert abc, retained A→B, qualified fixed receive, armed
witness/sentinel, persisted ATTEMPTED, the exact positive observation sequence, separate
witness and terminal ACCEPTED. Repeat fresh P01 and verify deterministic serialization and
semantic equality as section 8 specifies. No compiler function or E0 source is called.

Retain N01–N20 with these exact tests/results under section 7:
N01 initial unrelated A → WRONG_PROTECTED_OBJECT;
N02 short derivative read → INPUT_IO;
N03/N04/N05 complete short/long/altered pre-binding candidate → INPUT_TRUNCATED,
INPUT_APPENDED, INPUT_ALTERED;
N06 nonbytes → INPUT_TYPE;
N07 post-admission A substitution → OBJECT_SUBSTITUTION;
N08 post-binding B substitution, both different and equal bytes → OBJECT_SUBSTITUTION;
N09 denied altered-decoy pathname reopen → PATHNAME_REOPEN;
N10 wrong surrogate receiver → WRONG_LOADER;
N11 wrong typed parameter/entrypoint → WRONG_ENTRYPOINT;
N12 source-channel/environment/cwd redirection → SOURCE_REDIRECTION;
N13 sentinel-observed unarmed/premature entry → OBSERVER_NOT_ARMED;
N14 remove independent entry/association evidence with valid return → OBSERVATION_MISSING;
N15 interrupted attempt → ABORTED/ATTEMPT_INCOMPLETE;
N16 observed proposed filesystem fallback → PATHNAME_REOPEN;
N17 reliably counted zero/two entries → INVOCATION_COUNT;
N18 complete witness wrong-ID/schema corruption → RECORD_INVALID;
N19 missing candidate expectation hash → EXPECTATION_INVALID;
N20 real/unknown profile request → PROFILE_UNQUALIFIED.

N15 requires interruptions after reservation, registration, PREPARED, ATTEMPTED and during
a final journal write; each stays visible and recovers idempotently without consumer retry.
Recovery after a complete valid ACCEPTED/REFUSED leaves it unchanged. N18 additionally checks
that a complete invalid record yields ABORTED/RECORD_INVALID in recovery, while a torn tail
yields ABORTED/ATTEMPT_INCOMPLETE. N14 includes attempted witness swapping between two IDs;
wrong-ID is RECORD_INVALID, omission alone OBSERVATION_MISSING. These are repairs to the
existing boundaries, not broad fuzzing. Phase tests must preserve earlier passing conditions;
adapters that inject corrupt candidates are explicitly synthetic, not kernel failures.
For combined faults assert rank order, e.g. post-binding A substitution plus denied reopen
chooses PATHNAME_REOPEN and records OBJECT_SUBSTITUTION as a diagnostic. Never execute an
uncontrolled path merely to demonstrate refusal. Guards deny attempted source operations.

One smallest future circuit is an additive offline synthetic harness/receiver/witness that
demonstrates protected A → immutable B → qualified surrogate receive → independent witness
→ deterministic terminal evidence, including bounded controlled interruption/recovery tests.
It cannot execute scientific source, compile payload, import a client, access credentials/
network, invoke live runtime integration or E0, or resolve dependency_runtime_lock. The
trusted Python harness executes its own test logic only under separate future authorization.
No runtime invocation or implementation is authorized in this document correction.

## 10. Abort conditions and closing status

STOP on missing qualification artifacts, unavailable entry observation, unsupported profile,
loss of custody/namespace/lock, failed durable registration, unavailable protection/association,
unaccounted source operation, need for a different derivative or loading mechanism, or
any requirement for real-engine invocation, runtime locking, scientific/client/network/E0
activity. Preserve partial evidence; never repair a failed attempt into success.

- B1 contract: durable unique reservation before preparation; persisted ATTEMPTED; terminal normal states; explicit hash-bound idempotent ABORTED recovery.
- B2 contract: phase-specific predicates and fixed rank; one primary code with ordered supported diagnostics; deterministic separate recovery classification.
- B3 contract: pinned surrogate artifacts/live callable under trusted bootstrap only; actual engine and full runtime closure deferred.
- B4 contract: receiving-entry witness with own state/digest, exact separate serialization and terminal hash binding; in-process independence explicitly conditional.
- implementation-ready: YES for the corrected surrogate contract, pending independent review and separate implementation authorization; actual engine profile unavailable.
- external_trust_root status: first handoff slice independently VERIFIED; full gate and actual compiler consumption unresolved.
- H2A1 status: VERIFIED for scoped prospective custody/publication auditability; unchanged.
- H2A2 status: document correction only; completed first slice unchanged; all eight full H2 gates unresolved.
- E0 status: HOLD.
- one next bounded action only: independent document-only review of the corrected specification and correction receipt.
