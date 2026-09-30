# NS-001 H2A2 real CPython input-boundary specification v0.1

## Basis, authority and readiness

HEAD before: `aa30310a5d9b1804bf7605d3826bfaf5d6075f1b`.
Branch: `codex/e0-h2-preparation`; initially clean.
This is one document-only specification, not an engine qualification, implementation,
acceptance run or authorization to invoke a compiler. **Implementation readiness: PARTIAL.**
The missing qualification is stated in section 6; no currently qualified real observer is
available in the retained evidence. Unknown engine/observer facts are not invented pins.

The preceding `NS-001_H2A2_POST_SURROGATE_NEXT_SCOPE_v0.1.md` is the scope authority.
The completed sealed same-object handoff and corrected surrogate slices remain frozen:
respectively independently VERIFIED and VERIFIED WITH RESIDUAL ASSUMPTION. Their contracts,
implementations, fixtures and evidence are not changed or re-reviewed. This new profile is
`ns001.h2a2.real-cpython-input-receipt.v1`; it cannot consume a surrogate ACCEPT as proof of
real entry or relabel the frozen `abc` fixture as compiled evidence.

Only administrative text/file/hash/Git operations are used in this circuit. No candidate
compiler/evaluator/executor, import machinery, application subprocess, acceptance harness,
scientific/client or E0 path is invoked. The requested Git commit/push is administrative;
it is not authorization for runtime subprocesses, research downloads or scientific traffic.
No dependency_runtime_lock work begins. All eight full H2 gates remain unresolved.

## 1. Exact boundary and interface

Candidate implementation family: **CPython 3.12**, with one exact patch release, build,
platform/ABI and image set to be independently qualified and frozen before implementation
acceptance. A version range is not qualification. A different family/version or incompatible
interface requires a new reviewed specification, not silent fallback.

Three distinct boundaries:

| Boundary | Meaning and disposition |
| --- | --- |
| A: public `builtins.compile` callable receiving entry | The actual native C entry implementing that builtin receives the invocation argument vector, including original source object B. This is the selected sufficient boundary. A Python wrapper or pre-call notification is not this entry. |
| B: deeper compiler/parser entry | May receive converted buffers, decoded text or other representations. Not claimed here and not inferred from A. |
| C: execution of returned code | Separate action; prohibited. No execution claim or acceptance path. |

“Python-level callable entry” names the public API boundary A, even though its implementation
is native. Evidence must show control actually reached that implementation entry with the
actual arguments. A name lookup, wrapper frame or planned vectorcall is only intent.

The sole positive invocation shape, notation only and NOT executed here, is:

`qualified_compile(B, "<ns001-h2a2-real-input-v1>", "exec", 0, True, 0, _feature_version=-1)`.

`qualified_compile` must be the retained actual builtin object, still identical to the
qualified interpreter's `builtins.compile`, with native target association checked at entry.
There are exactly six positional arguments and exactly one keyword, `_feature_version`.
No star expansion from uncontrolled objects, duplicate keywords or other keyword is allowed.
The fixed expected values/types are:

| Argument | Exact requirement |
| --- | --- |
| source | Exact immutable builtin bytes B, not subclass, str, bytearray, buffer view, AST or code object. |
| filename | Exact str `<ns001-h2a2-real-input-v1>`; diagnostic label only, never opened or resolved. |
| mode | Exact str `exec`; compilation grammar, not execution authority. |
| flags | Exact int 0; bool is not an int substitute. No AST-only, top-level-await or other flags. |
| dont_inherit | Exact bool true; no inherited future/compiler flags. |
| optimize | Exact int 0; no ambient `-1` optimization selection. |
| _feature_version | Exact int -1, explicitly fixed; no alternate parser feature selection. |

Version-matched primary evidence must establish the chosen build's exact builtin signature,
including this keyword and its behavior. Local declarations alone do not establish it. If
that shape is unsupported, refuse qualification; do not omit/change the argument to proceed.
Every explicit/default/hidden argument or build switch affecting this entry must be accounted
for in the qualified interface. No unknown extra source selector is allowed. The specific
native argument-vector ABI/offsets are qualification facts, not assumed from the API name.

## 2. Claim ceiling

Allowed positive wording, always with the stated synthetic/trusted-host assumptions:

> Exact protected bytes were independently witnessed as the source argument received by the qualified real CPython compile entry.

“Received” ends at A. It means neither every byte was parsed nor any code was produced.
ACCEPT must not assert compilation success, parser correctness, AST correctness, code-object
correctness, execution, import resolution, stdlib/package identity, runtime hermeticity,
dependency integrity, dependency_runtime_lock, full external_trust_root resolution,
scientific correctness or E0 readiness. Neither real-entry success nor this specification
promotes any of the eight full H2 gates to passed.

## 3. Minimum engine and callable identity

Before admitting a real invocation, a retained expected descriptor E must identify:

1. CPython implementation, exact release/build, relevant configuration and platform/ABI;
   version-matched authoritative source/interface evidence and its retained origin/digests.
2. Exact executable bytes and compiler-bearing image bytes (libpython if separate; otherwise
   the identified executable), authenticated acquisition origin and expected SHA-256 values.
3. A qualified measurement method associating the actual running process and mapped native
   compile entry with those retained images, not merely hashing an executable on disk.
4. The builtin object/type, native function target and calling convention; association of
   that target to the identified image's reviewed entry. Keep the object live. Compare the
   retained object, builtin binding and native target again at receiving entry. A matching
   `__name__`, `__module__`, version string, address alone or self-reported digest is insufficient.
5. Exact bootstrap, supervisor and observer artifact identities, attachment method, supported
   call ABI, measurement semantics and independently reviewed qualification record.

E is frozen independently before testing and content-addressed in the retained store.
Actual measurements cannot overwrite expected identities. No blank/wildcard pin is ACCEPT.
The engine image, native loader path and any interposition affecting this callable/observer
must be accounted for or qualification refuses. If instrumentation alters an image, the
actual instrumented image and change must be identified and qualified; an unmodified-image
hash cannot stand for it. A build ID alone is not a whole-image byte identity.

Loaded-image and host measurement honesty remain explicit residual assumptions. This is a
conditional identity-of-receiver claim, not proof against malicious process/kernel mutation.
Evidence must nevertheless associate the actual entry with the expected image; “trusted
interpreter” cannot replace that association altogether. Local paths, PIDs, raw addresses
and ASLR offsets are not stable canonical engine identities. A qualified method may use
live values privately and serialize deterministic association results and artifact identities.

These requirements do not establish full immutable native/stdlib/package closure. That
separate boundary is section 11. No installation, engine probe or native observation runs
in this circuit, and no concrete build or observer is declared qualified.

## 4. Protected input and one inert fixture

The one new positive fixture is exactly two bytes: hexadecimal **23 0a**, ASCII `#` followed
by LF, with no BOM or other bytes. Length **2**; SHA-256:
`32c4858e22cc2c967b42150fa550562a2c839c2cebcaab91cabdf6f4da020022`.
This digest was calculated over literal data only, without a Python/compiler invocation.
The source is a comment-only file: no imports, definitions, calls, filesystem/network/process
or client effects, dynamic execution mechanism, scientific content or E0 content. It is
suitable for compilation by a qualified engine, but **must never be executed**.

Use the **same immutable byte-preserving derivative mechanism**, instantiated for this new
fixture in a separately reviewed additive profile, not the old retained B or a modified
frozen `abc` implementation. The prior acceptance is not empirical acceptance of this new
fixture. No new conversion/object kind is required by the bytes API.

The future harness must freshly establish protected A: exclusive witnessed acquisition of
these exact bytes against a frozen expected fixture descriptor, complete equality/hash/length
validation, trusted creation and retained live association of a regular sealed memfd, exact
WRITE/GROW/SHRINK/SEAL seals, and size 2. Creation/fill/validation/sealing belong to one reserved
attempt. No prior receipt substitutes for a live capability or witnessed origin.

Derive B by exactly one bounded positioned read `pread(A,3,0)` returning exactly 2 bytes,
with A association, size and seals checked before and after. Short/error I/O refuses without
retry. B must be exact builtin bytes, length 2, full equality and digest as above. Retain A
and B live through terminal observation. Independent entry observation separately reads A
with the same bounded complete-read rule and compares it to the actual received bytes.

The sealing copy into A and the single A→B read are permitted copies. Measurement may use a
private copy for hashing only if its equality to the actual received argument is qualified;
it cannot replace that argument or its live reference association. No additional delivery
copy of B is allowed, including equal-byte substitution. No decode/encode, normalization,
trimming, appended newline, BOM change, decompression, reserialization or mutation is allowed
before entry. Deeper engine transformations after the selected public input boundary remain
outside the claim. No source pathname, FD alias, stdin, import or cache is a delivery fallback.

## 5. Observer evaluation and selected class

| Candidate | Sufficiency for the selected boundary |
| --- | --- |
| Wrapper intent log or Python wrapper profile event | Insufficient: observes caller/wrapper, not actual builtin receipt. |
| Python profiling C-call notification | Insufficient alone: does not establish independently measured original arguments at the native receiving entry. It must not be treated as the surrogate's Python-frame witness. |
| Python/native audit hook with event named `compile` | Not qualified here. Event name alone proves neither engine origin, original object identity, all invocation parameters nor placement before conversions. User-generated same-named events must not count. |
| Qualified native entry observer | Proposed class: attached at the actual public builtin's native receiving entry, reading the received argument vector before conversion and independently associating the target image/call. Required for this profile unless a separately reviewed equivalence qualification proves another mechanism provides all the same facts. |

A deeper parser/audit event exposing converted input cannot silently substitute for original
B receipt. A caller-side hook with arguments is still intent until actual entry is observed.
This contract does not select an unverified probe address, ABI decoder or platform tool.
The native observer's exact attachment must be frozen in qualification before implementation.
It must observe, not replace the real consumer with a lookalike receiver.

The observer is separate from the fixture, compile result and delivery adapter. It must
have no input-success field populated from a consumer return or an expected test outcome.
Under the retained trusted host/process assumption, logical in-process independence can be
sufficient if the native attachment and own state are independently qualified. No cryptographic
attestation or hostile-interpreter isolation is implied. Attachment unavailable/replaced or
unreadable arguments cause refusal/abort; there is no fallback to intent/output logging.

## 6. Required qualification and actual-entry facts

**No currently qualified observer exists in this circuit's retained evidence.** The exact
missing qualification is one reviewed, build-specific engine/observer association package:
retained version-matched native entry/argument-conversion evidence; exact executable and
compiler-image pins with actual loaded-image association method; builtin target/call ABI;
observer artifact/attachment identity; and evidence that the observer measures original B
and every invocation parameter at actual entry, with ordering, coverage and failure behavior.
This is narrower than complete dependency-runtime closure, but cannot be presumed true.

A future qualification must exclude spoofed events, attachment to a caller/deeper transformed
buffer, unobserved alternate native targets, and callback/measurement paths that execute
user conversion methods. Only exact primitive argument types may be decoded. No arbitrary
repr, property, iterator or conversion can be called to record an unsupported object.

Minimum observer facts per attempt:

- Qualified engine/callable and observer identity hashes; observed association results.
- Actual native entry event from the qualified attachment, not a harness-supplied marker.
- Exact source type, actual length, independent SHA-256 and full equality; live `same_B`;
  live A association/seals/size and independent A-read equality to the incoming bytes.
- Six actual positional values/types and exactly the one keyword/value/type, including
  argument count and absence of unexpected/duplicate keywords. Unsupported values are
  recorded as unavailable/invalid, never coerced into expected parameters.
- Lifetime entry count plus per-attempt observer count; premature/duplicate/missing entry
  detection. Bootstrap must finish before arming; no incidental compile calls are admitted
  in the exclusive attempt interval. Unregistered entry stops the harness.
- Same attempt ID and E hash; actual dispatch token corresponding to synchronized ATTEMPTED;
  observed entry must follow that committed dispatch. Entry association cannot be reassigned.
- Retained observer completion and final association/guard status, including whether a return,
  exception or qualified observer stop was observed. Return is optional corroboration, never
  a substitute for entry. Unavailable facts stay null/unknown.

No independence claim is made from a native API declaration alone. Supplemental local
read-only evidence used here: `/usr/lib/python3.12/importlib/_bootstrap_external.py` at
source_to_code/get_code/exec_module; `/usr/include/python3.12/methodobject.h` and
`cpython/methodobject.h` for callable/native-target structures. They support interface
selection but do not qualify a running build, exact compile signature or probe. No missing
native evidence was fetched over a network or inferred from executing a candidate.

## 7. Compilation is distinct from execution

A later explicitly authorized experiment may let the exact real compile call process this
inert fixture. Mode `exec` selects grammar; it does not execute statements. Engine/compiler
and observer machinery do run. This is not “non-executing surrogate” work.

Generated code must never be passed to eval/exec, executed through a function object,
imported, marshalled/reloaded for execution or otherwise dispatched. The reviewed fixed
harness must have no such continuation; independently qualified execution-event coverage
must cover the candidate/result paths in its attempt interval. This is bounded reviewed
control-flow/observer evidence, not a global hostile-process sandbox assertion. Execution
or evidence of an execution attempt invalidates the circuit; it is never part of ACCEPT.

Entry receipt does not require compilation success. An observed compiler exception after
valid entry can coexist with receipt ACCEPT if all receipt evidence completes and no safety
violation occurred. An explicitly qualified observer stop at entry can do so only when it
is a defined clean completion, not an interrupted process. This profile does not assume any
available hook can abort before parsing. Uncontrolled interruption is ABORTED regardless of
how much successful-looking entry evidence survived.

To substantiate a separate factual observation that compilation completed, a future monitor
would need a same-call qualified native return with a code-object result type, tied to its
entry; evidence of compiler-path entry alone proves only an attempted call. Code-object
return would not prove correctness or execution. This contract neither requires nor promotes
that ancillary observation into a successful-compilation claim. No code-object bytes/hash,
AST correctness or execution result belongs to this receipt ACCEPT. Absence of execution
requires the bounded control-flow and observation evidence, not an inference from compile's
name or successful return. No such compiler invocation is authorized or performed now.

## 8. Bounded substitution defenses and acceptance cases

Negative inputs remain labelled synthetic faults. Do not launch a wrong/unqualified engine
or execute an uncontrolled path merely to prove refusal. Pre-entry qualification failures
must refuse without dispatch. Observer evidence corruption tests must be labelled evidence
faults and must not be passed off as real native-substitution demonstrations.

| Case | Required bounded fault/evidence and disposition |
| --- | --- |
| P01 twice | Fresh A/B and unique attempts; real qualified entry witnesses exact fixture. Both ACCEPT only under section 9; compare semantic records without reusing IDs. |
| N01 engine | Wrong expected executable/image/build or live association → ENGINE_UNQUALIFIED before dispatch. Include environment/PATH alternate-engine selection refusal; never launch it. |
| N02 callable | Wrong object/native target, rebound/monkey-patched builtin or lookalike wrapper → WRONG_COMPILE_CALLABLE. Include after-qualification rebinding detection before dispatch. |
| N03 protected input | Unrelated equal-byte initial A → WRONG_PROTECTED_OBJECT; later A/B substitution → OBJECT_SUBSTITUTION, including equal-byte B. |
| N04 derivative | Bounded short/error read → INPUT_IO; actual nonbytes candidate → INPUT_TYPE; complete short/appended/changed candidates → INPUT_TRUNCATED/INPUT_APPENDED/INPUT_ALTERED before dispatch. Mutation examples are empty bytes, comment extension, or whitespace, not executable/scientific source. |
| N05 arguments | Wrong filename, mode, flags, inheritance, optimization, feature version, count or keyword shape → WRONG_ENTRYPOINT; no wrong-parameter compiler call needed. If a qualified entry witness observes a post-check parameter change, the same predicate applies there. |
| N06 sources | Attempted path reopen/FD-alias/fallback → PATHNAME_REOPEN through a denying adapter; stdin/module/import/cache/bytecode/AST or source environment selection → SOURCE_REDIRECTION (or INPUT_TYPE for a supplied nonbytes argument). No such source is consumed. |
| N07 native loading | Relevant library/loader/interposed-entry mismatch or missing native association → ENGINE_UNQUALIFIED; unrelated full closure stays out of scope. |
| N08 observer | Unqualified/replaced/unavailable observer → OBSERVER_UNQUALIFIED; qualified but unarmed/early entry → OBSERVER_NOT_ARMED. Missing actual entry evidence despite consumer return → OBSERVATION_MISSING. |
| N09 count/binding | Zero/two entries → INVOCATION_COUNT; wrong dispatch link/missing linkage → OBSERVATION_MISSING; complete wrong-ID/cross-attempt record → RECORD_INVALID, ABORTED on recovery. |
| N10 interruptions | Reservation, registration, PREPARED, ATTEMPTED, witness/journal write and recovery-write interruptions → ABORTED; original bytes retained; no retry/resumption/promotion. |
| N11 precedence | Denied reopen plus post-binding object substitution → PATHNAME_REOPEN primary with OBJECT_SUBSTITUTION diagnostic. Earlier failing stages do not run later phases to accumulate faults. |

Real positive entry and real actual-argument measurement are mandatory; a fully mocked native
observer cannot satisfy P01. Pre-dispatch negatives establish refusal defenses only; they do
not establish a native receiving event for refused inputs. At least actual-receipt association,
missing-entry rejection, count/order and cross-attempt linkage must be tested against genuine
qualified positive observations. Additional dangerous live substitution is not implicitly
required. If the observer cannot detect a delivery substitution when checking the actual
received object/parameters, its qualification fails even if pre-dispatch tests pass.

## 9. Deterministic evidence, lifecycle and ACCEPT

Use a separate retained store/profile; never reuse a frozen slice's store, namespace or IDs.
Adopt its durable lifecycle semantics without editing its code/contracts: exclusive custody
lock; externally assigned retained namespace; exclusive monotonically increasing reservation
synchronized before preparation; retained E/request and registration before checks; PREPARED
only after qualification; ATTEMPTED synchronized before dispatch; separate witness synchronized
before a normal terminal event. ACCEPTED/REFUSED and recovered ABORTED are terminal. Missing
existing custody metadata stops, never recreates trust. An ABORTED attempt cannot append or
consume again through a retained live writer. Failed synchronization prevents dispatch.

The future additive implementation must retain the following evidence categories, with the
exact field layout below (no new schema is inferred from an old profile's fields):

- E: this spec digest, real profile, fixture length/digest, exact parameter vector, engine
  image/build/interface identities, bootstrap/observer/qualification artifact hashes and
  the fixed source-selection policy. Qualification pins must exist before attempts.
- Request/registration: actual proposed profile/parameters/case identity, exact raw request
  hash, E hash and unique `namespace:ordinal` attempt ID; no pathname source selector.
- Ordered append-only events: attempt ID, sequence, predecessor digest, state, exactly one
  primary refusal or null, ranked diagnostics, entered true/false/unknown, terminal witness
  digest or null. PREPARED → ATTEMPTED → ACCEPTED/REFUSED; precondition REFUSED allowed without
  fictional entry/ATTEMPTED. Execution attempts additionally invalidate the run.
- Independent witness: same ID/E, qualified association identities, ordered actual facts
  from section 6, denied source operations, single dispatch binding, actual-entry/observer
  counts, completion and no-execution coverage result. No consumer-written success flag.
- Recovery: distinct ABORTED record binding raw registration/request/witness/journal bytes
  or absence; full journal length/hash, maximal valid prefix length/hash and last valid
  sequence, entered only from retained evidence, recovery primary/diagnostics. No self hash.

The concrete engine/observer qualification inputs must be independently frozen before
implementation acceptance. The schema is defined here; native qualification remains missing.
No runtime invocation is permitted while that qualification is missing.

### Exact record layout

Every object has exactly the keys listed here; no implicit extension fields. Hash is 64
lowercase hexadecimal SHA-256; ID is custodian namespace plus positive decimal ordinal.
Unless marked nullable, values are required. Arrays preserve observed order. Unavailable
stage objects are null; required success facts cannot be null at ACCEPT. `schema` values
are `ns001.h2a2.real-input.<kind>.v1`, with kind as named below. The same canonical encoding
applies to every record. External qualification documents are retained bytes under their
hashes, not unversioned mutable URLs or self-asserted success strings.

- store: `schema`, `namespace` (64 lowercase hex). No replacement of missing retained metadata.
- expectation: `schema`, `spec_sha256`, `profile`, `fixture` (exact `length`, `sha256`),
  `parameters`, `engine`, `bootstrap_sha256`, `observer_sha256`, `qualification_sha256`,
  `source_policy` (literal `sealed-bytes-only`). `parameters` has exactly `filename`, `mode`,
  `flags`, `dont_inherit`, `optimize`, `_feature_version`, with section 1's exact types/values.
  `engine` has exactly `implementation` (CPython), `version`, `build_sha256` (retained build
  description), `abi`, `images`, `callable` (builtins.compile), `interface_sha256` (retained
  interface/ABI description). `images` is a role-sorted list of objects with exactly `role`,
  `sha256`, `origin_sha256`; roles are executable, compiler, and observer_native. Shared image
  roles remain separately identified. All version/ABI/role/name strings are printable ASCII.
- request: `schema`, `expectation_sha256`, `case_id` (P01 or N01–N11, optional decimal subcase),
  `profile`, `parameters`, `source_channel` (positive: protected_bytes), `source_environment`
  (ASCII string map, positive: empty), `cwd_policy` (positive: exclusive-synthetic). Raw malformed
  requests remain retained and hash-bound; they do not pass parsing by coercion.
- registration: `schema`, `attempt_id`, `expectation_sha256`, `request_sha256`.
- event: `schema`, `attempt_id`, `sequence` (nonnegative int), `state`, `primary_code` (code or
  null), `diagnostics` (ranked code array), `previous_sha256` (hash or null), `witness_sha256`
  (hash or null), `entered` (bool or null). PREPARED has sequence 0, entered=false and no codes
  or witness; ATTEMPTED follows PREPARED with entered=null and no codes/witness. Terminal
  ACCEPTED follows ATTEMPTED with entered=true, no codes and mandatory witness hash. REFUSED
  follows registration/PREPARED/ATTEMPTED, has one primary, mandatory witness hash and actual
  entered status. No event follows a terminal or an ABORTED recovery. Previous hash links the
  exact preceding event; null only for sequence 0.
- witness: `schema`, `attempt_id`, `expectation_sha256`, `qualification_sha256`,
  `observer_sha256`, `observations`, `violations` (ranked codes). Observations have exactly
  `index` (contiguous from zero), `kind`, `data`. Allowed kinds and exact data fields:

| kind | data fields |
| --- | --- |
| protected | initial, valid, association, seals_exact (bool); length (nonnegative int or null), sha256 (hash or null) |
| derived | exact_bytes, from_A, retained (bool); length, sha256 (as above) |
| engine | images_match, live_association, build_match (bool); interface_sha256 (hash or null) |
| callable | object_match, native_target_match, binding_match (bool) |
| observer | artifact_match, attachment_match, qualified, sentinel_active, armed (bool) |
| dispatch | attempted_event_sha256 (hash), persisted (bool) |
| entry | native_entry, engine_match, callable_match, after_dispatch, armed, exact_bytes, same_B, same_A, independent_A_equal, vector_valid, parameters_match (bool); length, sha256 (nullable as above); positional_count, keyword_count (nonnegative int); keyword_names (ASCII string array or null); parameters (six-field parameters object or null) |
| guard | operation (payload_open, payload_reopen, filesystem_fallback, source_redirect, or execution), denied (bool) |
| completion | linked_to_entry (bool); outcome (code_return, exception, observer_stop, unknown) |
| end | entry_count, observer_entry_count (nonnegative int); same_A, seals_exact (bool or null); no_reopen, observer_complete, execution_coverage, execution_attempted (bool) |

`entry.parameters` reports the six actual non-source values only if exact types/printable
strings can be represented; otherwise null and parameters_match=false. Unknown keyword
objects do not invoke conversion: keyword_names=null and vector_valid=false. A positive
entry has positional_count=6, keyword_count=1 and keyword_names=["_feature_version"].
Nonbytes input has null length/hash. Hashes and association booleans describe measured facts,
not expected values copied as observations. Truth remains conditional on qualified observation.

Positive order is exactly protected(initial=true), derived, engine, callable, observer,
dispatch, entry, protected(initial=false), completion, end. The entry's protected check
records its independent read. The required predicates in section 9 must all hold; completion
must be linked with outcome other than unknown, but code_return is not required. Qualified
observer_stop must be defined by the qualification record; otherwise it is incomplete.
Negative preparation retains only reached stages in order; repeated entry groups remain
in actual order; guard events may interleave; normal witness end occurs once and last.
Missing/early entry evidence must not be reordered into a positive sequence.

- recovery: `schema`, `attempt_id`, `state` (ABORTED), `primary_code`, `diagnostics`,
  `registration_sha256`, `request_sha256`, `witness_sha256`, `journal_sha256` (hash or null for
  absent file), `journal_length`, `valid_prefix_sha256`, `valid_prefix_length`,
  `last_valid_sequence` (nonnegative int or null), `entered` (bool or null). Empty journal and
  absent journal differ by journal_sha256. Recovery never hashes or rewrites itself.

State, qualification and witness semantic checks are required in addition to schema/type
and canonical-byte checks. A correctly shaped false observation cannot satisfy ACCEPT.

Canonical serialization must use ASCII-only JSON, sorted unique keys, minimal escaping,
ordinary integers, booleans/null, no floats/BOM/control characters and exactly one final LF.
SHA-256 covers exact bytes including LF. Reject noncanonical records and unknown schema
fields. Raw malformed bytes are hashed without normalization. No PID/FD/inode/address/time,
volatile exception text or temporary path enters canonical evidence. Retain volatile native
association details only through a qualification method whose deterministic assertions can
be reviewed; if that method cannot support the association claim, remain unqualified.

ACCEPT iff every following fact is positively established, not merely uncontradicted:

1. Qualified expected engine, native callable and independent observer are bound live.
2. Fresh protected A and B have exact type/bytes/length/hash/provenance and retained identity.
3. Actual received source is that B, matches independent A measurement, and the actual full
   positional/keyword vector equals section 1 with no alternate source route.
4. Exactly one actual qualified receiving entry follows persisted ATTEMPTED, bound to that
   attempt and dispatch; observer/sentinel evidence agrees and no unsupported event is hidden.
5. Source-operation policy and bounded no-execution coverage are complete; no prohibited
   substitution, evaluation, generated-code execution, scientific/client or E0 activity occurs.
6. Complete valid canonical records, witness attachment, hash links and terminal synchronization
   exist. No missing qualification, unknown required fact or interrupted completion is promoted.

Compilation success is not a seventh criterion. Code generation/execution is not inferred.
Repeat determinism compares serialization of identical full inputs and repeated semantic
observations removing only attempt ID and its derived link hashes. All original IDs/records
are retained; differences in engine, parameters, outcome or observer facts cannot be stripped.

## 10. Stable REFUSE/ABORT rules

New engine/observer/callable names distinguish this real profile; use prior names for shared
predicates. The user's ARGUMENT_SUBSTITUTION category maps to existing WRONG_ENTRYPOINT for
invocation values/shape and OBJECT_SUBSTITUTION for the retained source reference. There is
no duplicate serialized ARGUMENT_SUBSTITUTION code with competing precedence.

Preparation stages are structural record/expectation checks, protected input, derivative,
engine, callable, source selection/parameters, observer qualification/arming, then dispatch.
Stop at first failed stage; do not perform later checks just to accumulate diagnostics.
For actually evidenced normal faults, primary is the smallest rank below; diagnostics are
only other supported codes, deduplicated and rank ordered:

| Rank | Stable code / predicate |
| --- | --- |
| 1 | RECORD_INVALID: complete invalid canonical/schema/ID/hash-linked evidence. |
| 2 | EXPECTATION_INVALID: missing/invalid expected qualification descriptor or malformed candidate request. |
| 3 | WRONG_PROTECTED_OBJECT: invalid initial A origin/association/type/size/seals. |
| 4 | INPUT_IO: derivative read error or incomplete I/O. |
| 5 | INPUT_TYPE: supplied source candidate not exact bytes. |
| 6 | INPUT_TRUNCATED: complete candidate shorter than 2 bytes. |
| 7 | INPUT_APPENDED: complete candidate longer than 2 bytes. |
| 8 | INPUT_ALTERED: length 2 but bytes/digest differ. |
| 9 | PROFILE_UNQUALIFIED: different/unknown boundary profile. |
| 10 | ENGINE_UNQUALIFIED: missing qualification or mismatch of required executable/build/native-image/live engine association. |
| 11 | WRONG_COMPILE_CALLABLE: wrong/rebound builtin object or target under an otherwise identified engine. |
| 12 | SOURCE_REDIRECTION: alternate source channel/cache/import/environment selection. |
| 13 | WRONG_ENTRYPOINT: actual/proposed invocation vector differs from section 1. |
| 14 | OBSERVER_UNQUALIFIED: no accepted observer artifact/attachment/semantic qualification or replacement. |
| 15 | OBSERVER_NOT_ARMED: qualified observer not active before dispatch, or premature entry. |
| 16 | PATHNAME_REOPEN: denied payload pathname/alias/fallback operation. |
| 17 | OBJECT_SUBSTITUTION: later A association or retained B reference replaced. |
| 18 | INVOCATION_COUNT: committed attempt has other than one receiving entry. |
| 19 | OBSERVATION_MISSING: required entry/association/dispatch/completion evidence absent or contradictory. |
| 20 | EXECUTION_PROHIBITED: observed attempt to evaluate/execute/import source/result; stops the whole circuit irrespective of primary rank. |
| 21 | ATTEMPT_INCOMPLETE: recovery only, never normal REFUSED. |

A structurally valid E referring to missing engine qualification triggers ENGINE_UNQUALIFIED;
a malformed/missing E itself triggers EXPECTATION_INVALID. Observer qualification is distinct
from lack of evidence after a qualified attachment. Precondition refusal does not invent
zero-entry INVOCATION_COUNT. After dispatch, preserve observed entry facts; absent evidence
means unknown rather than presumed no entry. An object replacement remains OBJECT_SUBSTITUTION
rather than an initial admission failure, even if it also changes the incoming bytes.

Any interruption/nonterminal attempt recovers to ABORTED; complete invalid retained evidence
selects RECORD_INVALID, otherwise ATTEMPT_INCOMPLETE. Earlier supported faults are diagnostics.
A torn tail is not a complete invalid record. Recovery validates all record root types,
retains original files without repair and never retries consumption or promotes incomplete
receipt. Existing valid terminals remain byte-identical. A prior identical recovery is
idempotent; conflicting recovery or custody stops. Interrupted recovery writes remain visible;
only validated matching prefixes may be completed separately while preserving original bytes.

## 11. Separation from dependency_runtime_lock and STOP

Even a future PASS leaves interpreter installation reproducibility, stdlib closure,
package/import closure, full native dependency closure, environment closure, runtime
immutability after qualification and provenance of subsequently executed code unproven.
It establishes none of that gate's complete hashed closure or network-blocked installation
acceptance. Narrow compiler-bearing-image identification does not absorb the full gate.

STOP rather than improvise if engine identity/live association, builtin binding, native
argument observation, evidence durability or independent coverage is unavailable; if the
claim requires source/result execution; if complete runtime locking becomes inseparable from
the chosen narrow measurement; if network/client/scientific infrastructure is needed; or if
frozen slices need substantive modification. No path/observer/profile fallback is authorized.

## 12. One future slice, missing qualification and preservation

After separate qualification/schema review and explicit implementation/inert-compilation
authorization, the smallest slice is one additive offline synthetic harness/native observer
integration exercising this fixture at the single qualified real entry, with P01 repetition,
the bounded refusal/evidence cases above and preserved deterministic records. It never executes
returned code and never touches scientific/client/E0 paths. Its source/artifact allowlist must
be fixed by that later authorization; no frozen implementation is generalized in place.
This document grants no build/install/probe/compile/observer-test permission.

Readiness remains PARTIAL: the exact engine/native-entry observer qualification package in
section 6 is missing. This is a local qualification requirement, not a request to start
runtime-lock work. The one next action is a document-only engine/observer qualification review
against this contract, using retained primary evidence; no implementation or invocation.

Before commit, all 214 pre-existing tracked files were checked against their Git blob
identities, with no differences from HEAD before; only this new specification is changed.
This includes H2A1 and both frozen H2A2 slices.
No candidate compile/eval/exec/import/runtime/client/E0 or application subprocess invocation
occurred. Only this specification is committed/pushed. HEAD after is the resulting commit,
reported in the final response without a self-referential embedded hash.

- identified boundary: actual native receiving entry of the public real CPython builtin compile, before source conversion; not deeper parser or execution.
- allowed claim: exact protected bytes independently witnessed as source argument received by qualified real CPython compile entry, under explicit trust assumptions.
- prohibited claims: compilation/parser/AST/code-object success or correctness, execution/import resolution, stdlib/package/runtime/dependency integrity or hermeticity, full external_trust_root and E0 readiness.
- engine identity contract: exact CPython build/executable/compiler-bearing image plus actual loaded-entry association and qualified observer/bootstrap identities; no full closure claim.
- compile callable contract: retained real builtin/native target, six positional arguments and explicit _feature_version=-1; exact fixed values/types; no rebinding or fallback.
- protected input contract: fresh sealed A → single complete byte-preserving read → retained exact bytes B; independently compare original receiving argument and A.
- inert fixture: hex 23 0a, length 2, SHA-256 32c4858e22cc2c967b42150fa550562a2c839c2cebcaab91cabdf6f4da020022; never executed.
- observer requirement: independently qualified native receiving-entry argument observation; Python profile/audit labels alone insufficient; none currently qualified.
- compilation/execution distinction: future separately authorized compilation may occur; output success unnecessary; source/result execution prohibited and circuit-stopping.
- substitution channels: engine/native-loader/callable, bytes/reference/arguments, pathname/cache/import/environment and observer/attempt linkage.
- ACCEPT criteria: all six positive evidence requirements in section 9, canonical complete same-attempt records and no prohibited execution; no inference from return value.
- REFUSE/ABORT criteria: ranked unique primary plus supported diagnostics; interrupted attempts ABORTED and never resumed/promoted; custody/conflicts STOP.
- dependency_runtime_lock separation: full installation/native/stdlib/package/environment closure, immutability and later execution provenance remain unresolved.
- smallest future implementation slice: separately authorized additive offline inert native-entry receipt harness/observer with bounded positive/refusal/recovery evidence; not begun.
- implementation readiness: PARTIAL.
- if PARTIAL, exact missing qualification: build-specific native entry/argument observation and actual engine association package; no qualified observer exists yet.
- external_trust_root status: unresolved; real compiler input receipt remains unproven.
- dependency_runtime_lock status: unresolved; not begun or absorbed.
- H2A1 status: unchanged scoped VERIFIED.
- H2A2 status: sealed handoff VERIFIED and surrogate VERIFIED WITH RESIDUAL ASSUMPTION, frozen unchanged; real profile specified only; all eight full gates unresolved.
- E0 status: HOLD.
- one next bounded action only: separately authorize one document-only real-engine/observer qualification review; not performed.
