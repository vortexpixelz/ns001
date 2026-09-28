# NS-001 H2A2 external trust-root next scope v0.1

## Basis and scope

Reviewed preparation HEAD: `fc9902950d3bb9366abb00a553b9796f8d525c45`.
Branch: `codex/e0-h2-preparation`; initial working tree clean.
This is one document-only scope review. It creates no mechanism, acceptance result,
runtime lock, gate decision or execution authorization. The only changed artifact is
this receipt; the requested administrative commit/push does not expand its scope.

The following sources are repository-relative paths pinned at the reviewed HEAD:

- `docs/e0/h2/NS-001_H2A2_RUNTIME_TRUST_ROOT_CORRECTION_REVIEW_v0.1.md`, especially findings 6–7, 10–14 and closing disposition: independently reviewed first-slice claim and residual assumptions.
- `docs/e0/h2/NS-001_H2A2_SNAPSHOT_HANDOFF_ACCEPTANCE_SPEC_v0.1.md`, sections 1–3: inert single-file identity and non-executing claim ceiling.
- `docs/e0/h2/NS-001_H2A2_HANDOFF_MECHANISM_SELECTION_v0.1.md`, basis and sections 1–2: sealed-copy finalization and live same-object association.
- `docs/e0/h2/NS-001_H2A2_RUNTIME_TRUST_ROOT_DESIGN_v0.1.md`, gate map and evidence lifecycle: source-to-engine consumption requirement and runtime-lock interface.
- `docs/e0/h2/NS-001_H2A2_READINESS_SCOPE_REVIEW_v0.1.md`, unresolved-gate table: ownership and prerequisites.
- `docs/e0/h2/H2_EVIDENCE_CONTRACT_DRAFT.md`: declaration-only status and eight unresolved substantive gates.

Earlier receipts retain their historical phase/status statements. Their earlier
UNSTARTED or PARTIAL labels are not contradictions to later scoped correction acceptance.
This review relies on the preserved independent review; it does not rerun that acceptance
suite or re-audit H2A1.

## 1. Established claim

Under the declared trusted Linux kernel, Python/harness, hashing, exclusive acquisition
and controlled-descriptor assumptions, the exact expected inert single-file bytes were
validated, copied into a sealed immutable handoff object, and that same protected object
was independently observed by the fixed non-executing consumer and observer. Required
independent evidence was checked before canonical ACCEPT serialization.

The fixture is `source.bin`, exactly ASCII `abc` without a newline, length 3, SHA-256
`ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`.
The finalized memfd is a validated, sealed copy, not the original acquisition file.
Live creation/duplication/association observations establish same-object handoff;
equal hashes alone do not. Independence is between reviewed observation roles within
a trusted harness, not independently authenticated processes or organizations.

The retained correction review supports this bounded claim and its historical
4-positive/84-negative evidence. It does not establish execution of source, actual
interpreter/process identity, dependency closure, or a production runtime trust root.
Sealing protects content/length; it is not proof of interpretation, execution or an
OS-level non-execution policy. No persistent live memfd was deposited.

## 2. Immediately adjacent unresolved boundary

The first unproven edge is **protected verified payload → actual source-consuming
loader/compiler input**. The present fixed consumer reads bytes and reports observations;
it is not a source loader. A future engine could otherwise reopen a pathname, use an
unbound cache/bytecode object, substitute a buffer, or receive different bytes after a
correct verification event. A successful current receipt says nothing about that edge.

The narrow next question is whether the designated consuming entry point receives the
complete protected bytes through one specified, witnessed route with substitution refused.
If a copy or decoding step is necessary, its identity, exact transformation and evidence
must be explicit; same-object identity must not be asserted across distinct objects.
Proving entry-point consumption alone still does not prove that resulting code was
executed by an authenticated runtime. Compiler transformation, resulting executable/code
identity and actual execution are downstream obligations, not silently included here.

This follows the existing design's source-consumption requirement. It is a proposed next
scope, not a modification of the frozen `abc` contract. That fixture must remain inert.
Any future executable synthetic fixture would require a separately approved contract and
execution authorization, and cannot replace the accepted first-slice fixture in place.

## 3. Evidence needed for the next boundary

A later closure decision would require the following, with expected identities fixed
before observations. This list describes needed evidence, not evidence produced here.

| Required evidence | What it must establish / refusal boundary |
| --- | --- |
| Reviewed consumption mechanism and authoritative interface semantics | One exact loader/compiler entry point, input type, ownership/lifetime and copy/decoding rules. No unspecified pathname reopening or fallback. If the interface cannot expose a defensible consumption boundary, stop rather than infer it from output. |
| Retained identity/provenance | Source fixture, manifest, protected-object contract, loader/observer sources and designated engine identity tied to retained bytes and immutable origins. A version string or self-reported digest is insufficient evidence of actual loaded-engine identity. |
| Independent association and input observation | Bind the finalized verified object to the actual entry-point input in the same attempt, recording complete length/content and any specified transformation. Observe the real consumption route, not only a wrapper's intended argument or the payload's own report. Retain independent evidence before success finalization. |
| Explicit alternate-input policy | Account for source paths, caches/bytecode, imports, plugins and generated inputs reachable at this boundary. Refuse unbound alternatives. State which routes are structurally absent and which require later evidence; do not equate a mocked refusal with runtime enforcement. |
| Separate positive and negative acceptance | Correct protected input reaches the designated entry point once; substituted handle/buffer, altered or incomplete input, wrong consumer/engine expectation, reopening and missing association evidence fail. Hash-to-load substitution, ambient import and stale bytecode need real boundary evidence where reachable; otherwise remain unresolved full-gate requirements. |
| Retained, independently checkable result | Bind validation, handoff, consumption observation and terminal evidence to one attempt; reject missing, substituted or cross-attempt evidence. Preserve exact inputs, expected results, refusal ordering and canonical outputs plus hashes, with observer/host assumptions explicit. Output equality alone cannot prove the route. |

The future acceptance contract must distinguish input consumption from code generation
and execution. Tests and primary mechanism evidence must remain separate categories;
H2A0 declarations cannot substitute for either. No full `external_trust_root` rule is
promoted to passed by this scope review.

## 4. Relationship to dependency_runtime_lock

**Document design can remain isolated; unconditional runtime assurance cannot.** A
synthetic source-consumption contract can define the edge under an explicitly trusted,
designated engine/host and specify an identity input interface. This does not require
installing, selecting or proving a production runtime closure in the next document circuit.
Its eventual bounded findings would retain that engine/host assumption.

A claim that an identified real runtime executes the verified source needs evidence
linking the actual engine and its influential interpreter/native/library/dependency inputs
to the approved immutable closure. That is an interface to `dependency_runtime_lock`,
whose complete pinning, artifact hashes, immutable runtime, platform/native identity,
closure completeness and network-blocked installation acceptance remain separately owned.
Hashing a named executable alone does not discharge those obligations.

Accordingly, the next document may specify required identity fields and rejection on absent
or mismatched supplied evidence, but cannot mark runtime-lock evidence verified or its gate
closed. If a proposed consumption mechanism cannot be scoped without resolving that closure,
record the dependency and defer implementation; do not start a second gate by implication.

## 5. Smallest next circuit and exclusions

The smallest next circuit is **one offline, document-only acceptance-boundary specification
for protected-object-to-source-consumer input**, limited to the first edge in section 2.
It should select one proposed input-binding mechanism on paper, define the exact consumer
entry point and observation boundary, permitted transformations/lifetime, identity evidence
interface, deterministic ACCEPT/REFUSE criteria and minimum substitution/missing-evidence
matrix. It must explicitly retain trusted-engine assumptions and downstream execution limits.
If a defensible mechanism cannot be selected from the available evidence, its outcome must
be BLOCKED/PARTIAL with the missing evidence identified, not an invented guarantee.

This is one future document circuit only, subject to separate authorization. It is not
performed here. An implementation allowlist, fixture creation, engine installation, runtime
probe or acceptance run is not authorized by this recommendation. Implementation would
require later independent review and explicit authorization after the document decision.

Prohibited scope remains: edits to `e0/h2/runtime_trust_root.py` or
`tests/test_e0_h2_runtime_trust_root.py`; alteration of any frozen first-slice contract or
receipt; reinterpretation/execution of the `abc` fixture; H2A1 evidence or status changes;
scientific code, datasets, preregistration and frozen evidence changes; client selection,
imports or live JHTDB traffic; credentials, workflows, settings, publication objects or
attestations; runtime/dependency installation or locking; live process integration;
resource experiments; E0 execution; and work beginning another H2 gate.

All eight full gates remain unresolved: `external_trust_root`, `client_source`,
`response_contract`, `transport_accounting`, `dependency_runtime_lock`,
`maximum_partition_memory`, `amendment_freeze`, `final_manifest_package_audit`.
This receipt grants neither whole-gate readiness nor execution authority.

## Preservation and closing disposition

Method: repository document inspection and administrative byte comparisons only. No
implementation/test import, acceptance suite, fixture, memfd, loader, client, scientific
runtime or E0 execution occurred. Pre-commit comparison against the reviewed HEAD confirmed
all 202 pre-existing tracked files byte-identical, including implementation/tests, H2A1 and
frozen scientific artifacts. Only this new receipt was present in the working-tree changes.

- established claim: VERIFIED synthetic exact-byte validation and sealed same-object handoff to fixed non-executing observation roles, with preserved residual assumptions.
- next unresolved boundary: protected verified payload to actual source-consuming loader/compiler input; runtime execution remains downstream and unproven.
- required evidence: reviewed input-binding mechanism, retained identities/origins, independent actual-consumption association, alternate-input refusal evidence, bounded positive/negative tests and complete same-attempt records.
- dependency_runtime_lock relationship: isolated document/conditional synthetic scope is possible; actual immutable runtime/closure assurance remains a separate necessary interface for stronger execution claims.
- smallest next circuit: one document-only protected-object-to-source-consumer input acceptance-boundary specification; no implementation or test execution.
- prohibited scope: implementation/frozen-contract changes, runtime or scientific execution, H2A1 changes, live clients/credentials/publication/workflows and every other H2 gate.
- readiness verdict: READY for that separately authorized document-only circuit; NOT READY for runtime implementation or full-gate closure on this receipt.
- H2A1 status: VERIFIED for scoped prospective custody/publication auditability; unchanged.
- H2A2 status: first synthetic sealed-memfd handoff slice independently VERIFIED; next consumption boundary unproven; full external_trust_root and all eight substantive gates unresolved.
- E0 status: HOLD.
- one next bounded action only: obtain authorization for and prepare the single document-only protected-object-to-source-consumer input acceptance-boundary specification described above.
