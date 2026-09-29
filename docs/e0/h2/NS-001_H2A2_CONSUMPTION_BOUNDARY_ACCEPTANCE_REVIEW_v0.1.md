# NS-001 H2A2 consumption-boundary acceptance review v0.1

## Decision and review basis

Branch `codex/e0-h2-preparation`; reviewed HEAD
`964b95f599ed88a378d26ea8b6b6b069445f1bbc`; initially clean.
Reviewed specification S:
`docs/e0/h2/NS-001_H2A2_CONSUMPTION_BOUNDARY_ACCEPTANCE_SPEC_v0.1.md`, SHA-256
`19606d64819ebfd94d701b842cecaba39f0597dadd5917a73e905b73ea5acfd9`.
All S line references below are pinned to that commit. This is a separate review turn,
not an independent organization or security principal. No implementation, runtime tests,
compiler/loader invocation or scientific/client execution was performed. Administrative
text reads, hashes, Git comparisons and the requested receipt commit/push are the only
operations. The specification and completed slice are not edited.

**Implementation-ready: NO for the requested no-invented-semantics criterion.** The
non-executing surrogate is a sound bounded direction, and the claim ceiling is explicit.
However, B1–B4 below are distinct contract issues that affect the surrogate itself. This
verdict is not based merely on the intentionally unqualified real engine or unselected
E0 entrypoint. It supersedes no historical acceptance and does not invalidate the completed
first sealed-memfd slice. The specification's PARTIAL label uses a different criterion;
under this review's requested rule, multiple substantive ambiguities require NO.

## 1. Real boundary and claim — VERIFIED as a proposed boundary

S:32–74 correctly separates Python input delivery from subsequent compilation/execution.
Read-only comparison with `e0/hardening.py` confirms its explicit no-entrypoint/mock-only
status and its disclaimer that associated source hashes do not establish loaded bytecode.
The existing `run_experiment.py` and Docker entrypoint are feasibility references, not
qualified E0 entrypoints. No live E0 entrypoint is selected by this review.

The Python compiler's bytes-argument entry is a legitimate candidate **input-receipt**
boundary. S's inspected importlib source route supplies data to compile; this does not
prove a particular loaded runtime or receiver. A bytes-callable surrogate can reproduce
that argument-passing shape. Actual future E0 source entry and actual execution of
compiler-produced code remain separate, unqualified boundaries.

S:84–98 disallows execution/compilation success, compiler correctness, trusted runtime,
locked dependencies/imports, scientific correctness and E0 success. Those exclusions are
adequate. The word consumption is explicitly limited to argument receipt, not evidence
that each byte was parsed, influenced code or executed. Retain that qualification whenever
reporting a result. A surrogate result cannot be relabelled real-profile ACCEPT.

## 2. Engine qualification — PARTIAL; profile separation needs repair (B3)

The minimum identity contract for a selected receiver must freeze:

- Profile and implementation/interface family: a fixed non-executing bytes-callable
  surrogate, or a specifically qualified real compiler entrypoint. These are not synonyms.
- Exact receiving callable/interface and independently checkable code identity, including
  the trusted association between the selected callable and the observed entry.
- Exact six typed arguments, mode and source-selection semantics; the filename is a
  diagnostic label, not a locator. No import, pathname or bytecode fallback.
- The source-redirection policy, environment/cwd boundary and the bootstrap assumptions
  under which observation is trusted.
- For a real engine, a version/build identity sufficient to select matching interface and
  observer semantics, plus an association with the actual consumer; a label alone fails.
  This is not a claim that the build or its complete runtime closure is trustworthy.

Full Python/runtime version locking is not logically necessary to prove a **conditional
surrogate argument-receipt** claim. Trusted harness/host assumptions can support a live
callable association; host executable hashes may be retained as descriptive provenance.
Conversely, calling a real compiler qualified requires evidence about that actual consumer,
not just the surrogate's source hash. Full stdlib/native/package closure remains deferred.

**B3 — BLOCKING:** S:137–142 unconditionally requires live executable/compiler-image
association without hash-to-launch gaps. S:302–305 still requires host executable pins and
reviewed launch argv for the surrogate, while S:258 and 270–273 allow a stand-in for its
executable-substitution test. It is unclear whether the surrogate must prove actual process
image binding or only test receiver selection under a trusted host assumption. Those choices
have different acceptance evidence and scope. The descriptor also has no distinct supervisor
hash despite S:138 naming one; whether supervisor equals harness is not fixed. S:181–186
prohibits filename argv/source-selection channels without explicitly separating harness
bootstrap from tested payload delivery. That separation matters to a runnable harness.

This review states the minimum claim distinction, but does not select a launch mechanism,
relax the existing MUSTs or fill concrete pins. A document repair must make the profile's
normative identity/launch obligations explicit before implementation. Lack of a live E0
entrypoint is not itself a blocker for a properly bounded surrogate.

## 3. Surrogate validity and protected object

**Surrogate validity: VERIFIED WITH RESIDUAL ASSUMPTION as a structural model.** It must
preserve exact bytes type/value/length, diagnostic argument semantics, actual receiving
entry, retained derivative identity, independently observed ordering/counts, and refusal
on substitution. Returning a precomputed expected receipt or observing only an outgoing
call would not qualify. It cannot prove actual compiler receipt, parsing, code generation,
execution, native consumer-image enforcement or dependency identity.

**Protected-object verdict: VERIFIED at the contract level.** S:100–133 specifies fresh
live sealed A, full fixed-size read into immutable exact bytes B, size 3, F/M/S, independent
byte comparison, exact Q/association checks, lifetime and no normalization/reopen. This is
a byte-preserving copy, not a claim that A and B are one object. Identity of the retained B
must be checked at entry; equal-byte substitution is forbidden. No serialization beyond
the specified raw copy is needed for B. An unrelated memfd or equal-byte replacement cannot
pass the written association requirements merely through hash equality.

No alternate-byte ACCEPT route is permitted by the intended object requirements. The
remaining risks are whether evidence implements that requirement, and how failures are
classified, rather than an unspecified allowed transformation. These are prospective
requirements, not a rerun of the first slice or proof of hostile-process isolation.

## 4. Observer qualification — PARTIAL (B4)

S:153–173 correctly requires receiving-entry observation, exact tuple and live A→B linkage,
selected-consumer association, ordering, one invocation, no reopen and finalization. An
in-process observer can be sufficient for the first surrogate's declared trust model:
it must be separate from the sender/receiver, observe the actual receiving code-object
entry before the body, retain references and make its own protected-object observations.
It must not infer a call from a return, read count, expected hash or consumer-generated W.

Residual assumptions: honest kernel, Python object/call machinery, supervisor and observer;
no hostile modification of hooks or evidence within that process. This is independence of
observation roles, not a separate security principal or proof against a compromised runtime.
A real C/compiler entrypoint cannot inherit qualification from a Python function-entry test.

**B4 — BLOCKING:** S:339–343 requires retained complete independent witness observations,
but defines only the W boolean/count/hash summary. It does not define the witness's minimum
record schema, event/order linkage to the attempt, or verifiable representation of the
A→B and selected-receiver associations. S:290–292 expressly leaves raw observations in a
separate attachment without binding its bytes in the canonical record. A receiver-return
summary and detailed independent trace are very different evidence, yet an implementer
must invent the trace/evidence interface and its completeness checks. S:190–193 also calls
for a fixed observation tuple and no-reopen guard coverage without fixing that tuple or
which observed operations establish the required coverage.

Mechanism neutrality is compatible with alternative instrumentation only when the required
observable evidence and checks are fixed. Exact syscall addresses or volatile identifiers
need not enter deterministic JSON, but the independent logical witness and its attachment
to this attempt must be defined. This is an acceptance-evidence decision, not ordinary
implementation formatting. No observer mechanism is selected in this review.

## 5. ACCEPT/REFUSE and substitution matrix — PARTIAL (B2)

ACCEPT conditions correctly require complete independent evidence, one entry, exact B,
qualified selected consumer and no unapproved source route. Compiler success is not a
surrogate criterion. The matrix contains all requested substitution families: initial wrong
object, changed bytes/length/type, post-binding object, wrong consumer, pathname/environment/
argument selection, unarmed entry, missing observation and incomplete attempt.

**B2 — BLOCKING:** The numbered list does not by itself define phase-specific predicates.
There are concrete competing results:

| Counterexample | Conflicting written requirements |
| --- | --- |
| Replace a valid A after binding with an unrelated equal-byte object | Code 04 covers presented A lacking expected association and precedes 10; N07 and S:239 demand OBJECT_SUBSTITUTION. A rule restricting 04 to initial validation is implied, but not stated in its predicate. |
| Truncate the final JSON event in a journal after a valid prefix | Code 01 covers invalid canonical/schema bytes; code 18 covers a truncated valid journal prefix; S:345–351 prescribes ATTEMPT_INCOMPLETE recovery for malformed/truncated final records. The evaluator/recovery classification precedence is not specified. |
| Missing expected identity descriptor | Code 01 covers missing fields while code 03 and N19 require EXPECTATION_INVALID. The invalid candidate versus journal/descriptor structural-validation boundary needs an explicit rule. |

The short-read versus complete bad-input cases are usefully distinguished at S:225–235;
those should not be collapsed. Wrong bytes injected before binding can test codes 12–15,
but the fixture/adaptor must label synthetic corruption rather than claim a sealed memfd
spontaneously changed. N13 needs independent evidence of the premature call despite the
normal entry observer being unarmed; otherwise only missing evidence is established.
That observation requirement belongs with B4, not an invented expected result.

These ambiguities need not allow ACCEPT, but they prevent stable deterministic refusal
codes without implementer interpretation. No request for broad fuzzing or extra scientific
cases follows. A stand-in WRONG_LOADER test remains a surrogate policy test, not runtime-lock
or actual executable-substitution evidence.

## 6. Attempt record — BLOCKING (B1)

PREPARED/ATTEMPTED/terminal states, append-only records and no acceptance of incomplete
prefixes are a useful foundation. ATTEMPTED is honestly defined as committed dispatch rather
than proof of entry. Deterministic sequence numbers and previous-record hashes suffice for
relative ordering in a trusted local attempt; timestamps would not authenticate the observer
or solve replay. No timestamp requirement is added.

**B1 — BLOCKING:** S:346–347 requires a recovery report to reference the interrupted prefix
hash, but the exact event schema at S:309–313 has no such field. S:350 fixes recovery's
previous_sha256 to null; expectation_sha256 identifies E, not the particular interrupted
prefix. W likewise has no prefix reference. A distinct recovery directory does not encode
the required reference or prevent associating the wrong equal-expectation attempt. A future
implementer must either add prohibited fields or invent an external binding record.

The claim that a failed attempt cannot disappear is also too broad for the specified
lifecycle: PREPARED is written only after all preparation checks. A crash during preparation,
or an unbound entry before PREPARED, may leave no registered attempt/journal evidence at all.
An exclusive directory is required, but its creation/registration ordering relative to those
operations is not specified. Existing controls prevent a retained incomplete record from
being counted as ACCEPT; they do not establish complete accounting of every failed attempt.
Power-loss durability is explicitly not promised and is not requested by this finding.

Repair needs a defined attempt-start/custody boundary and an encodable recovery association,
with failure/partial-record semantics. This review does not add states, fields or select a
persistence mechanism. B1 is independent of observer selection and refusal-code repair.

## 7. Runtime-lock separation and implementation decision

**Runtime-lock separation: VERIFIED in intent, PARTIAL in normative profile application.**
With trusted host/harness assumptions, exact protected-input derivation and actual surrogate
entry association can be tested without proving Python binary trust, stdlib/import closure,
package dependencies or the complete environment closure. Explicit source-selection inputs
must still be checked; an empty declared environment is not proof of all hidden runtime
influences. Binary hashes record identity, not trust, completeness or correctness.

For a real compiler-receipt claim, matching the selected consumer to an observed entry is
required. Complete immutable runtime, transitive libraries/imports, offline installation and
later execution provenance remain separate obligations. B3 requires a decision about which
minimum identity assertions the surrogate actually accepts; it does not authorize building
a runtime lock or selecting a production E0 entrypoint.

Multiple substantive repairs remain: B1 record/recovery lifecycle, B2 phase-specific refusal
semantics, B3 profile-specific identity/bootstrap scope, B4 independent witness contract.
Therefore implementation-ready is **NO**, not PARTIAL. There is no exact single missing
decision to report. The next circuit should repair the document contract, preserving this
review and all frozen history; it must not implement or resolve another H2 gate.

## Preservation and closing disposition

Pre-commit comparison: all 204 pre-existing tracked files are byte-identical to reviewed
HEAD; only this new receipt changed. First-slice implementation SHA-256 remains
`d15ddd0b3d689592398987e62ce3135ee8a61e48ccd48cfa511d4870ac0b0023`; test harness remains
`67150d764cfde33e1d72837cf3ec518c3469a7f617ec19808d30c0762434b647`.
H2A1, the reviewed specification, scientific artifacts and all earlier receipts remain
unchanged. No Python interpretation/compilation, loader, scientific client, test harness,
application subprocess or live runtime path was invoked. Administrative shell/Git/file
inspection only; E0 remains HOLD.

- boundary verdict: VERIFIED as a candidate input-receipt boundary; surrogate, future E0 entrypoint and actual execution remain distinct.
- claim verdict: VERIFIED; no compilation/execution/runtime-lock/E0 success implication permitted.
- engine-qualification verdict: PARTIAL; B3 requires profile-specific identity/bootstrap obligations; real engine remains unqualified.
- surrogate-validity verdict: VERIFIED WITH RESIDUAL ASSUMPTION as an argument-binding model, not real compiler evidence.
- protected-object verdict: VERIFIED at specification level; exact immutable derivative and live provenance binding are explicit.
- observer-qualification verdict: PARTIAL; role independence is sufficient under trusted-process assumptions, but B4 witness/coverage contract is missing.
- ACCEPT/REFUSE verdict: PARTIAL; B2 phase/record classification overlaps prevent deterministic implementation as written.
- attempt-record verdict: BLOCKING; B1 recovery-prefix binding is unencodable and preparation interruption accounting is incomplete.
- substitution-defense verdict: PARTIAL; intended defenses cover requested families, but independent evidence and ordered failure semantics require repair.
- runtime-lock separation verdict: PARTIAL operationally; full closure correctly deferred, B3 leaves surrogate minimum identity ambiguous.
- blocking issues: B1 attempt/recovery lifecycle; B2 refusal phase semantics; B3 surrogate versus real identity/bootstrap requirements; B4 retained independent witness contract.
- implementation-ready: NO.
- if PARTIAL, exact single missing decision: not applicable; multiple independent substantive issues remain.
- external_trust_root status: full gate unresolved; first non-executing sealed-handoff slice remains independently VERIFIED.
- H2A1 status: VERIFIED for scoped prospective custody/publication auditability; unchanged.
- H2A2 status: downstream consumption specification reviewed but not implementation-ready; all eight full H2 gates remain unresolved.
- E0 status: HOLD.
- one next bounded action only: one document-only corrective specification circuit addressing B1–B4, without implementation, real-engine invocation or another H2 gate.
