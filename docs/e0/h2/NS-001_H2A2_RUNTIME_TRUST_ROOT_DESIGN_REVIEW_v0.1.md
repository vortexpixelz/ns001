# NS-001 H2A2 runtime trust-root design review v0.1

## Scope and review basis

Preparation branch `codex/e0-h2-preparation`; HEAD before
`1dd65a6363a05fb5ff9101ac7ae348a07a42ffc3`; initial tree clean.
Reviewed `docs/e0/h2/NS-001_H2A2_RUNTIME_TRUST_ROOT_DESIGN_v0.1.md` at that commit.
Line references below refer to that immutable version. This is a separate adversarial
text review against the nine requested questions, not implementation/testing and not
independent human or third-party certification. Earlier design conclusions were not
accepted as proof of their own adequacy. Only this review receipt is created.

Finding classes describe document adequacy, not runtime evidence:
VERIFIED = explicit internally consistent requirement; VERIFIED WITH RESIDUAL ASSUMPTION
= valid within a named trusted-base assumption; PARTIAL = material specification gap;
BLOCKING = unresolved choice prevents an unambiguous implementation/acceptance verdict;
OUT OF SCOPE = intentionally deferred and not a pass. No control has been executed here.

Overall: **PARTIAL design; implementation-ready NO as written.** The architecture is a
reasonable set of necessary invariants, but not sufficient evidence/mechanism for the
whole stated runtime claim. The first slice can be made narrower and testable without
changing H2A1 or claiming a substantive H2 gate pass.

## Findings against the nine questions

### 1. Logical sufficiency of the trust boundary — PARTIAL / BLOCKING for the full claim

Lines 30–59 correctly require an externally anchored expected identity, protected
objects, no pathname reopen, an identified engine and a separately trusted observer.
These are necessary conditions. They do not specify how objects are protected, which
actual process consumes them, or how the observer binds its record to that process.
An immutable byte value handed to a test consumer proves at most a bounded handoff.
It does not prove that an interpreter compiled those bytes, that an executable came
from them, or that the observed runtime is the approved runtime.

The design acknowledges these limits at lines 275–280. Therefore this is not a hidden
claim that the first slice closes the full gate; it is a mismatch only if the headline
“verified source bytes → protected consumption by an identified runtime/process” is
used as the first slice's acceptance claim. Preserve the narrower claim explicitly:
“retained verified fixture bytes → exact bytes delivered to a fixed non-executing consumer.”
Runtime/engine/process/dependency binding stays OUT OF SCOPE for that slice.

**B1:** Before implementation, choose a non-executing consumer and define the exact
handoff observation and mutation semantics. Remove the first-slice alternative permitting
fixture execution (lines 254–255) from its approved contract, or separately review a
larger execution boundary. Do not demand a full production loader to test this primitive.

### 2. Gate ownership — VERIFIED

Lines 119–139 and 324–326 explicitly assign only an external_trust_root slice to H2A2;
dependency_runtime_lock is an interface and later closure. Client source, response,
transport, resource, amendment and final audit ownership is deferred. Describing their
required evidence is not claiming implementation ownership. All eight gates remain
unresolved and E0 authorization is separate. No accidental additional gate ownership
was found. No amendment to the declaration contract or H2A1 status is warranted.

### 3. First-slice operational properties — PARTIAL

| Property | Class | Review finding |
| --- | --- | --- |
| Offline | VERIFIED as intended scope | Lines 245–258 and abort rules forbid networking/live integration. Actual enforcement is unimplemented; do not report an observed network-isolation pass. |
| Synthetic | VERIFIED as intended scope | Tiny inert fixture, not NS-001 scientific input; embedded fixtures and disposable outside-checkout paths are specified. |
| Deterministic | PARTIAL | Synchronization rather than sleeps is specified. Post-verification mutation permits either original consumption or refusal; a safety invariant is clear, but the chosen implementation's exact expected result is not fixed. |
| Independently testable | PARTIAL | External-to-fixture handoff observation is required, but observer interface, oracle independence, expected-record schema and result/refusal schema are absent. |
| Reversible | VERIFIED WITH RESIDUAL ASSUMPTION | Three additive paths/disposable fixtures limit changes; assumes no hidden side effects or execution capability. Existing-file protection remains mandatory. |
| Unable to execute E0 | PARTIAL; BLOCKING if claimed as enforced capability | Prohibition and no integration are explicit. Optional executing fixture and unspecified callbacks/import surface prevent proving structural inability from this text alone. A fixed bytes-only consumer is the narrower answer. |
| Unable to touch live JHTDB/client infrastructure | PARTIAL; BLOCKING if claimed as enforced capability | No client/network operation is permitted, but no implemented capability boundary exists. Future API must not accept endpoint/client/transport/credential callbacks or arbitrary executable source. |

An intent prohibition is not a tested capability guarantee. This review neither claims
that a forbidden operation occurred nor requires implementing a production sandbox.

### 4. Positive test — VERIFIED at invariant level; PARTIAL as an executable contract

Lines 262–263 specify correct expected digest/length, exactly one invocation, matching
consumed bytes and a deterministic result. That is a clear positive invariant. A fixed
fixture, exact expected record, result fields and independent expected marker/oracle
must still be frozen before implementation. Expected hashes must not be derived from
the tested artifact and then treated as independent authorization of that same artifact.

### 5. Requested negative tests — PARTIAL / BLOCKING

| Negative | Present in design? | Class and precise missing criterion |
| --- | --- | --- |
| Wrong snapshot | Only wrong source digest/length; “snapshot” is not defined as a file set/root | PARTIAL: define whether identity is one byte object or an entire package. Do not claim a package check from one file hash. |
| Altered file | Explicit before-read rejection; after-read original-or-refuse invariant | VERIFIED for before acquisition; PARTIAL for fixed post-acquisition outcome. A later backing-file change need not invalidate a retained immutable copy, but replacement bytes must never be consumed. |
| Missing file | Missing/truncated *handoff result* and deletion *after* verification are covered | BLOCKING omission: initially missing/unreadable source must reject before consumer invocation; neither existing case covers this. |
| Extra file if forbidden | Global closure threat mentions extras; first slice permits adjacent stale .pyc fixture | BLOCKING ambiguity: either single-file scope with siblings excluded from the closure, or exact-set package scope that rejects extras. Do not simultaneously require accepting and rejecting the same extra .pyc case. |
| Wrong manifest | Future schema mentioned at lines 63–67, no first-slice manifest contract | BLOCKING if claimed: define a small typed identity record and malformed/unknown/duplicate fields, wrong values and refusal; or explicitly exclude manifests from the first slice's claims. |
| Wrong expected root/hash | Wrong digest is explicit; “root” can mean directory, package root digest or trust root | VERIFIED for wrong expected file hash; BLOCKING ambiguity for root: define object, scope, algorithm and independent expected value before making a root-verification claim. |

**B2:** Freeze one object model and identity-record contract plus initial missing-input,
malformed-record and extra-file policies. A full production manifest is unnecessary.
**B3:** Freeze one deterministic outcome for each phase-specific mutation, with zero
consumer calls on pre-consumption failure and no success record after failed acquisition.
The current allowed original-or-refuse invariant is safe, but not a complete fixed oracle.

### 6. Identity separation — VERIFIED conceptually / PARTIAL for snapshot identity

| Identity | Finding |
| --- | --- |
| Source identity | Commit/tree and source-file digest/length are distinguished (lines 65–72). |
| Snapshot/package identity | Closure is discussed but no exact membership/root-digest semantics are specified; first slice's single byte snapshot must not be relabeled package completeness. |
| Runtime identity | Actual executable/engine/platform is distinguished from source identity (lines 74–75). Not demonstrated by a fixed consumer marker. |
| Dependency/runtime closure | Transitive libraries/loaders/stdlib/build inputs explicitly separate (lines 73–75). Deferred gate, not satisfied by the test interpreter version. |
| Execution identity | Supervisor run/process/event/output relation distinguished from content hash or PID alone (lines 80–86, 154–166). Deferred for full execution. |

No common hash label should hide these distinct objects. The first-slice result should
state only its exact object identity and handoff claim; runtime metadata may be recorded
as environment context without being mislabeled a verified runtime closure.

### 7. Residual assumptions — VERIFIED WITH RESIDUAL ASSUMPTION

Lines 55–59, 90–95, 115 and 181–192 explicitly retain interpreter/compiler/OS/hardware,
observer and privilege assumptions. A hash does not prove instruction semantics. The
source-only versus compiled path is not silently treated as equivalent evidence.
This is an adequate documentary limit. Future reports must not combine a VERIFIED
byte-identity subclaim with unverified runtime assumptions into an unconditional runtime
VERIFIED verdict. The fixed test harness and host remain trusted for the narrow experiment;
that assumption does not require proof against root-level host compromise in this slice.

### 8. Missing acceptance criteria — BLOCKING before implementation

B1–B3 are the implementation blockers, not the mere absence of implementation in a design.
Their acceptance contract also needs:

- bounded fixture size/type and exact expected digest/length supplied independently;
- regular-file/path policy, symlink/alias/nonregular refusal, and what constitutes the
  approved scratch boundary; no reading arbitrary host/credential paths;
- immutable handoff/result semantics with no lazy reread, caller-mutable buffer alias,
  arbitrary callback or exception path that can invoke the consumer after failure;
- a fixed non-executing consumer and an independently fixed oracle, invocation count,
  deterministic phase ordering, retained inputs and refusal reason/result shape;
- explicit handling of initially missing file versus missing post-verification path
  versus missing result, and whether stale/extra files are rejected or outside scope;
- exact meaning of “snapshot,” “manifest” and “root,” or explicit exclusion of package
  assertions; limit independent expectation checks to what the API actually accepts.

These are protocol/acceptance choices, not a demand to select a container, OS or production
loader. They can be resolved in one short document-only acceptance specification. No
code or tests were run to infer missing behavior. No additional H2 gate closure is needed
merely to write/test the smaller primitive once its bounded contract is approved.

### 9. Smallest defensible circuit — narrower proposal

The single trust boundary is defensible, but optional source execution and an undefined
package-root interpretation are unnecessary. Narrow it to **non-executing, single-file
fixture acquisition/identity validation and immutable snapshot handoff**.

Recommended contract choices for a separately authorized specification (not adopted or
implemented here): one tiny regular fixture file inside a dedicated disposable directory;
a separately pinned expected identity record, not a payload-chosen expectation; one exact
allowed filename/file set; an immutable retained byte value; a fixed consumer that only
compares/counts bytes and returns a fixed-format diagnostic. No eval, compile, exec,
subprocess launch, dynamic import, caller-supplied callback, production manifest or client.

An exact single-file fixture set would make the requested extra-file test meaningful:
reject an extra file at initial acquisition. An adjacent stale .pyc then belongs to that
refusal test, not a second test that expects successful acquisition with that extra file.
Define a snapshot-root digest only if its canonical input/serialization is frozen; otherwise
call it a file digest, not a package/trust-root digest. A small expected identity record can
cover wrong-manifest tests without introducing an execution manifest.

After a successful immutable acquisition, choose a fixed original-snapshot-consumption
outcome for path replacement/deletion: retained bytes remain the consumer's sole input.
This tests absence of a pathname reread; it does not promise the mutable directory still
matches its initial inventory at consumption, nor does it attest source execution.
Wrong identity record/hash, initial alteration/missing/nonregular input and initial extra
member must refuse before consumption. If the contract chooses a different coherent
policy, it must be explicit and reviewed before tests are written, not accepted post hoc.

The permitted claim would be VERIFIED byte identity/handoff **within the trusted test
harness**, with residual engine/host assumptions stated. Runtime/process provenance,
all-import exclusion, dependency closure, arbitrary-code containment and all eight gate
passes remain OUT OF SCOPE. This experiment would not execute source code as source.

## Scope, authorization and preservation

**Exact smallest authorized implementation slice: NONE in this circuit.** The user
has authorized this review receipt only. The narrower proposal above is eligible for
a separate specification/authorization, not permission to implement now.

If later approved, retain the design's proposed three-file implementation allowlist:
`e0/h2/runtime_trust_root.py`, `tests/test_e0_h2_runtime_trust_root.py`, and
`docs/e0/h2/NS-001_H2A2_RUNTIME_TRUST_ROOT_IMPLEMENTATION_RECEIPT_v0.1.md`.
No existing file or directory-wide write grant follows. No fixture execution, tests,
imports of NS-001 modules, downloads, client calls, credential access, runtime changes,
scientific execution or E0 occurred in this review. Administrative text reading/writing,
Git-object comparison and hashing are not execution of the proposed runtime.

The next recommended action is one separately authorized document-only acceptance
contract at proposed new path
`docs/e0/h2/NS-001_H2A2_SNAPSHOT_HANDOFF_ACCEPTANCE_SPEC_v0.1.md`, resolving B1–B3.
Do not modify the reviewed design or begin implementation as part of that recommendation.
The path is a proposal from this review, not an existing authorization or historical spec.

Before commit, all pre-existing tracked files are compared to the starting commit,
covering H2A1 and scientific/frozen material; only this review receipt may be new.
The reviewed design remains unchanged. No external-state freshness or runtime test
result is asserted: this is a local design review with its requested receipt commit/push.

Observed preservation check: PASS; all 192 pre-existing tracked files match the
starting commit byte-for-byte, including H2A1, reviewed design and scientific material.
Frozen preregistration/sidecar match the expected SHA-256. Only this new receipt exists
outside the tracked inventory. No proposed runtime/client/scientific execution occurred.

## Closing verdicts

- Design verdict: **PARTIAL**; sound invariants and honest claim ceilings, incomplete first-slice acceptance contract; full runtime/process sufficiency not established.
- Scope-boundary verdict: **VERIFIED as documentary boundaries**, not demonstrated runtime confinement.
- Gate-ownership verdict: **VERIFIED**; external_trust_root slice only, runtime-lock interface, other gates deferred; all eight unresolved.
- First-slice verdict: **PARTIAL / BLOCKING for implementation as written**; narrow to a fixed non-executing single-file snapshot consumer.
- Positive-test verdict: **VERIFIED invariant / PARTIAL executable contract**; exact fixture/record/oracle still needed.
- Negative-test verdict: **PARTIAL / BLOCKING**; initial missing file, extra-member policy, manifest/root meaning and phase-specific deterministic outcomes need specification.
- Residual assumptions: **VERIFIED WITH RESIDUAL ASSUMPTION**; trusted host/interpreter/observer/harness and independently approved expectations remain explicit.
- Blocking issues: **B1** non-executing consumer and claim boundary; **B2** exact snapshot/identity-record/root/file-set contract; **B3** deterministic mutation/refusal/output/observer acceptance matrix.
- Implementation-ready: **NO**, pending resolution/approval of B1–B3 and separate implementation authorization.
- Exact smallest authorized implementation slice: **NONE now**. Recommended future slice: non-executing single-file identity validation and immutable snapshot handoff under the proposed three-file allowlist.
- H2A1 status: **VERIFIED**, scoped prospective custody/publication auditability; unchanged.
- H2A2 status: **design reviewed; implementation UNSTARTED**; all eight substantive gates unresolved.
- E0 status: **HOLD**; Gate 1 PARTIAL, unchanged.
- One next bounded action only: separately authorize the one-file snapshot-handoff acceptance specification resolving B1–B3; no implementation. Not performed here.
