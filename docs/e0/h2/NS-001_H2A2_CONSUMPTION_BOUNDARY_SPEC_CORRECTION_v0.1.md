# NS-001 H2A2 consumption-boundary specification correction v0.1

## Basis and bounded result

Preparation branch: `codex/e0-h2-preparation`.
Starting HEAD: `9544fbebc013979e53f978c54c07e3f1e682bd35`; initially clean.
This circuit corrects only B1–B4 from the independent consumption-boundary review.
It changes the acceptance specification and creates this receipt. No implementation,
fixture, test, interpreter/compiler/loader, application subprocess, client or live-runtime
path was invoked. Administrative shell text/file/hash/Git operations only. E0 remains HOLD.

Paths are relative to the repository root:

- Corrected S: `docs/e0/h2/NS-001_H2A2_CONSUMPTION_BOUNDARY_ACCEPTANCE_SPEC_v0.1.md`.
- Preserved R: `docs/e0/h2/NS-001_H2A2_CONSUMPTION_BOUNDARY_ACCEPTANCE_REVIEW_v0.1.md`.

S before SHA-256: `19606d64819ebfd94d701b842cecaba39f0597dadd5917a73e905b73ea5acfd9`.
S after SHA-256: `7757f0d7fb8c8f27d2c7516e68c065ea4313b3fd8f013f6674a1e2c5f81799b6`.
R unchanged SHA-256: `85ed8e3ce501cad05e1400137c8d9e2ed1a470cc8f29ae2ccf748a5db725ea01`.

**Implementation readiness: YES for the corrected surrogate contract, at document level.**
No actual test result, runtime qualification, independent correction acceptance or execution
authorization is claimed. The next action is independent document review. Concrete future
implementation artifact pins are frozen acceptance inputs after implementation review;
they are not undefined behavioral choices or authorization to generate them now.

## Corrections and paper consistency checks

### B1 — recovery lifecycle

S sections 5 and 8 introduce a synchronized unique reservation before preparation. A retained
custody namespace plus monotonic never-reused directory ordinal deterministically identifies
each attempt. Registration names retained expectation/request bytes. Uniqueness explicitly
depends on preservation of that store/namespace; no global randomness, timestamp or host
fingerprint is substituted for custody.

PREPARED is reached only after passing preconditions. ATTEMPTED is synchronized before
receiver dispatch. Normal ACCEPTED/REFUSED are terminal. Interrupted reservations recover
as a distinct ABORTED disposition, never as inferred acceptance or resumed consumption.
Recovery explicitly encodes raw journal hash/length, maximal valid-prefix hash/length,
last valid sequence and registration/request/witness hashes or their absence. These fields
repair the old unencodable prefix reference. An empty reservation is itself visible evidence.

The paper checks cover: crash after reservation before registration; interruption during
preparation; PREPARED without ATTEMPTED; ATTEMPTED without entry/terminal evidence; torn final
line; complete invalid record; interruption while writing recovery; repeated recovery; and
an existing valid normal terminal. S preserves all original bytes, prevents ID reuse and
makes recovery idempotent or stops on conflict. Failed storage synchronization stops dispatch.
These are contract checks, not simulated or executed crash tests.

Unique IDs mean fresh equal attempts have different whole-record hashes. The corrected
criterion is deterministic serialization given identical full inputs, including ID, plus
repeat-run semantic equality excluding only ID and derived link hashes. The historical
first slice's byte-identical repeated ACCEPT evidence remains untouched. No attempt is
relabelled or assigned a reused ID to manufacture byte equality.

### B2 — refusal predicates and precedence

S section 7 preserves all eighteen names while replacing overlapping predicates with
phase-specific definitions. Initial A validity is distinct from substitution after admission;
pre-binding derivative corruption is distinct from replacing retained B at delivery; candidate
request errors are distinct from malformed evidence records. Normal decisions serialize one
rank-selected primary code and only supported, rank-ordered secondary diagnostics.

Preparation proceeds through object, derivative, receiver, selection and hook checks,
stopping on failure. Missing observation is not evidence of an unobserved substantive fault.
Recovery first classifies lack of a valid terminal chain: complete invalid records produce
ABORTED/RECORD_INVALID; an incomplete/torn tail without such a record produces
ABORTED/ATTEMPT_INCOMPLETE. It cannot compete with normal acceptance.

Paper counterexamples from R now have explicit outcomes:

| Counterexample | Corrected classification |
| --- | --- |
| Valid initial A later replaced by equal-byte unrelated object | OBJECT_SUBSTITUTION; initial-object phase is no longer applicable. |
| Torn final journal line after valid prefix | ABORTED/ATTEMPT_INCOMPLETE, with raw tail and prefix preserved. |
| Complete malformed evidence record | RECORD_INVALID; recovery is ABORTED if no valid terminal chain exists. |
| Missing candidate expected-descriptor hash | EXPECTATION_INVALID; candidate request is not the journal schema. |
| Post-binding substitution plus a denied payload reopen | PATHNAME_REOPEN primary; OBJECT_SUBSTITUTION supported diagnostic. |
| Observer record omitted despite valid consumer return | OBSERVATION_MISSING; return cannot manufacture a witness. |

Each code has an isolated reachability test; N01–N20 retain the original bounded families.
Recovery subcases and cross-attempt witness binding address B1/B4 directly, not broad fuzzing.
Wrong-loader tests now explicitly concern the surrogate callable, not a fabricated proof of
Python executable-substitution resistance.

### B3 — identity/bootstrap boundary

S section 4 distinguishes three scopes. The surrogate needs reviewed retained receiver,
observer and harness artifact hashes; the exact fixed six-positional-argument receive
interface; live callable/code-object association under trusted bootstrap; fixed inert mode/
source semantics; and the specified observer location. Supervisor code resides in the
pinned harness/observer artifacts rather than an unspecified extra executable.

The surrogate requires no Python executable/compiler-library hash or full version, stdlib,
package, import or ambient-environment closure. Bootstrap may load reviewed test support;
its own filename is not a payload source channel. During the attempt, no source environment,
PATH selection, pathname fallback or alternate receiver resolution is allowed. Source-input
policy is distinct from proving a hermetic operating environment.

Actual Python engine identity/build/interface evidence and actual compiler-entry observation
remain additional, unproven requirements. The real profile always refuses in this surrogate
contract. Full runtime/dependency locking remains separately unresolved. The receiver's
trusted loaded-code association is explicitly not proof of bootstrap/bytecode authenticity.

### B4 — independently retained witness

S section 6 selects an in-process receiving-function entry observer plus a lifetime sentinel,
using trusted profiling call/return events and retained code/reference identity. Separate
observer state is inaccessible through the receiver's six arguments; no receiver-produced
summary can set it. The sentinel witnesses the premature-entry negative even while the
per-attempt entry observer is unarmed.

A separate canonical witness contains attempt/expectation identity, qualified source-artifact
identities, ordered protected/derived/qualification/armed/dispatch/entry/return/end observations
and any denied source operations. The entry observation independently computes actual received
length/digest, checks retained derivative identity and protected-object association, compares
actual invocation parameters and witnesses ordering against persisted ATTEMPTED. The terminal
event hashes the whole witness. Cross-attempt attachment substitution cannot pass an ID/hash
check. There is no circular terminal-hash requirement in the witness.

No-reopen evidence concerns the fixed reviewed attempt program and its denying source-operation
guard. Direct bypasses are forbidden at qualification; this is not a hostile-process syscall
sandbox. Only evidence-journal I/O and earlier synthetic acquisition are allowed outside that
payload guard. Independence means a separately computed and retained receiving observation,
not separate-process security. Trusted kernel, profiling/object machinery and harness/process
remain residual assumptions.

## Scope and preservation

Sections 1–3 retain the prior candidate boundary, inert abc fixture, sealed-object derivative
and claim ceiling. Downstream substantive edits are restricted to B1–B4 and their directly
necessary schemas, test expectations and readiness/status wording. R is preserved verbatim;
the completed first slice, H2A1 and every other gate are unchanged.

Pre-commit byte comparison: 205 pre-existing tracked paths at the starting commit; the
specification is the sole changed existing file. All 204 other files are byte-identical,
including R, all H2A1 evidence and scientific/frozen artifacts. Only the specification and
this new receipt appear in Git status; documentation whitespace checks pass.

First-slice implementation remains SHA-256
`d15ddd0b3d689592398987e62ce3135ee8a61e48ccd48cfa511d4870ac0b0023`;
its harness remains
`67150d764cfde33e1d72837cf3ec518c3469a7f617ec19808d30c0762434b647`.
No test suite, runtime/bootstrap/loader/compiler/client, scientific execution, workflow or
publication action occurred. Git commit/push applies only to the two authorized documents.

- B1 verdict: ADDRESSED at contract level; durable reservation and explicit terminal recovery binding, not runtime-tested.
- B2 verdict: ADDRESSED at contract level; staged applicability and deterministic single-primary precedence for normal/recovery results.
- B3 verdict: ADDRESSED at contract level; surrogate qualification separated from real engine and full runtime closure.
- B4 verdict: ADDRESSED at contract level; exact independent witness schema, receiving-entry observation and terminal attachment binding.
- recovery-state contract: reserved → PREPARED → persisted ATTEMPTED → ACCEPTED/REFUSED; interrupted nonterminal reservations → immutable ABORTED recovery, never resumed or promoted.
- refusal-precedence contract: phase-scoped predicates, rank-selected one primary and ordered supported diagnostics; torn versus complete-invalid records distinguished in recovery.
- surrogate identity contract: retained artifact hashes, fixed receive interface, live callable/code reference and observer association under trusted bootstrap; no runtime-binary lock requirement.
- future real-engine qualification boundary: actual compiler implementation/build/image/callable and real entry observer still unproven; real profile unavailable.
- witness independence rule: separate in-process state/code path, independently computed incoming bytes, live A→B linkage and exact invocation/order, separate hashed serialized witness; consumer return insufficient.
- residual assumptions: preserved exclusive evidence store/namespace, honest sync/storage/kernel, trusted interpreter/bootstrap/profile mechanism and harness/process; no malicious-host, rollback or full-lock guarantee.
- smallest future implementation slice: offline inert sealed-A-to-bytes-B surrogate plus independent witness and bounded refusal/recovery acceptance only; no source compilation/execution, network/client/E0 or runtime-lock work.
- implementation readiness: YES for the corrected surrogate document contract; independent review and separate authorization precede implementation.
- external_trust_root status: full gate unresolved; actual compiler consumption unproven; first sealed-handoff slice independently VERIFIED.
- H2A1 status: VERIFIED for scoped prospective custody/publication auditability; unchanged.
- H2A2 status: B1–B4 documentation correction only; completed first implementation slice unchanged; all eight full H2 gates unresolved.
- E0 status: HOLD.
- one next bounded action only: independent document-only review of the corrected specification and this correction receipt.
