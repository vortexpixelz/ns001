# NS-001 H2A2 readiness and scope review v0.1

## Review boundary and authoritative starting point

Preparation branch: `codex/e0-h2-preparation`.
HEAD before: `2c8afc856dbec8e052055b7fb481d1b2850d8407`; initial working tree clean.
This is one local read-only readiness/scope review, with this receipt as its only
repository-content write. No implementation, test execution, dependency installation,
network evidence acquisition, client import, credential access, scientific execution,
publication change or H2A1 modification occurred. The requested receipt commit/push
is the only remote write. H2A2 implementation remains UNSTARTED.

H2A1 is VERIFIED for scoped prospective custody/publication auditability, as recorded
in `docs/e0/h2/NS-001_H2A1_PLATFORM_ATTESTATION_CREDENTIAL_FREE_REVIEW_v0.1.md`
(lines 23–27 and closing verdicts) at the starting commit. That receipt explicitly
leaves the eight substantive H2 gates unresolved. This review accepts the preserved
verification outcome; it does not rerun or reopen H2A1.

The current frozen preregistration hashes to
`a2a8523c065d4d41155aa29d367c888d49ab3032f6075b8cebbd2475ff1efd78`, matching its
unchanged sidecar. H1 source is `6e33cb9ca7019e50e2f247ade9ae8c9a7b40d3ff`, scientific
base is `0393315223df8ed90f20f0c821508cc98bea08d1`; neither is the publication/workflow
target `d9dcfbef1bea173b316bc968fd71421c982422c3`.

## Exact purpose recoverable from existing records

The strongest explicit H2A2 assignment is a **separately authorized trust-root review**:
`docs/e0/h2/NS-001_H2A1_EXTERNAL_ANCHORS_REVERIFY_v0.1.md`, lines 174–183, requires
later substantive H2/H2A2 review of authority/content/custody and runtime binding.
`docs/e0/h2/H2A1_RECONCILIATION_REVIEW_RECEIPT.md`, lines 63–76, distinguishes this
runtime requirement from anchor matching and lists the eight remaining gates.

The exact runtime objective is supplied by the existing prospective drafts:

- `preregistrations/e0/NS-001_E0_INTERFACE_DECISION_DRAFT.md`, “Unresolved evidence”:
  a reviewed external source-only bootstrap OR an externally verified,
  content-addressed, read-only runtime must execute the exact bytes already read
  and verified, without timestamp-based or unchecked bytecode-cache substitution.
- `preregistrations/e0/NS-001_E0_GETDATA_AMENDMENT_DRAFT.md`, “Proposed structural
  controls”: H1 binds associated source files but does not prove those bytes
  produced executing Python bytecode; this must be resolved before any production
  callback is possible.
- `e0/h2/evidence_contract.py`, `GATE_REQUIREMENTS` (lines 376–552), fixes the
  required evidence/rule declarations. The module is declaration-only and never
  converts a true boolean or matching hash into a verified substantive gate.
- `docs/e0/h2/H2_EVIDENCE_CONTRACT_DRAFT.md`, “Evidence declarations and later
  verifier ownership”: authority/content, retained origin/custody/bytes, synthetic
  execution, report attribution and claim resolution are distinct later-verifier
  responsibilities, with independent review required.

**Scope qualification:** there is no existing complete numbered H2A2 implementation
specification or exact implementation file allowlist in the reviewed tracked records.
The records define later-H2 obligations and identify H2A2 with trust-root review;
they do not assign all eight gates wholesale to H2A2. This receipt therefore fixes
no new runtime architecture and does not pretend a proposed allowlist was previously
approved. Its narrow, evidence-supported purpose is to scope and subsequently prove
runtime trust binding, with the necessary authority/provenance/acceptance evidence.
The first circuit proposed below is design-only; actual proof requires later authorization.

Publication Sigstore/TUF trust roots authenticate publication signatures. The H2
`external_trust_root` gate concerns the runtime executing verified code. These are
different trust boundaries. Credential-free attestation verification does not prove
Python import safety, runtime immutability or JHTDB client behavior.

## Every unresolved H2 gate and its relationship to H2A2

All eight remain UNRESOLVED. The status comes from the governing declaration contract,
reconciliation receipt and latest H2A1 closure limits, not a newly executed gate evaluator.

| Gate | Exact outstanding evidence objective | H2A2 relationship |
| --- | --- | --- |
| `external_trust_root` | Primary proof of `bytecode_substitution_blocked`, `exact_verified_bytes_executed`, `source_substitution_blocked`; retained immutable identity/source origin; separate offline acceptance for `ambient_import_refused`, `hash_to_load_substitution_refused`, `stale_pyc_refused`. | Direct intended trust-root subject. Publication custody satisfies only an input-provenance prerequisite, not this gate. |
| `client_source` | Select exact client source, pin its commit and license; retain acquisition bytes, origin and verified digest. | Required before applying a runtime proof to a production client. A narrow synthetic runtime design can precede selection; H2A2 is not authorized to select/download/import a client in this review or the proposed first circuit. |
| `response_contract` | Authoritative extraction, nine gradient columns/order, bounded dtype/shape variants; explicit fixture mapping and malformed-response refusal. | Later adapter evidence dependency; no basis to assign its full closure to the first H2A2 circuit. A signed H1 archive cannot supply these semantics. |
| `transport_accounting` | Enumerate initialization calls, exclude hidden calls, bound internal retries; observe all egress, count redirects, establish one retry owner. | Future live-client integration prerequisite. H2A2 design must preserve no-egress/no-credentials refusal, but must not claim transport accounting without exact client evidence. |
| `dependency_runtime_lock` | Hash/pin every transitive dependency; prove immutable runtime and interpreter/platform/native identities; independently accept complete closure and installation with networking blocked. | Direct interface to runtime trust-root design; necessary for eventual production closure. Exact environment/closure is missing. A bootstrap demonstration alone does not close it. |
| `maximum_partition_memory` | Prospective ceiling and fixed measurement environment; full 2,000,000-point path, process tree, swap policy, measured ceiling acceptance. | Deferred whole-path acceptance after approved client/runtime; no benchmarking or target-data execution now. |
| `amendment_freeze` | Approved prospective review, frozen amendment hash, unchanged original preregistration and consistent sidecar; retain reviewer identity/approval. | Later governance prerequisite. Existing GetData/interface documents remain drafts. H2A2 may not approve or freeze them by implication. |
| `final_manifest_package_audit` | Bind every artifact and exactly twelve operations without self-reference or embedded E0 authority; independent package hash/exclusion review and retained audit inputs/receipt. | Deferred final H2 package. H1 publication manifests are not this execution manifest or audit. |

Do not collapse the distinction between a gate being relevant to a safe runtime and
being explicitly assigned to the next phase. Only the first gate is directly named by
the H2A2 trust-root reference; runtime-lock and client interfaces must be accounted for,
and the remaining gates stay explicit deferred dependencies rather than assumed passes.

## Satisfied prerequisites and their claim ceilings

1. A stable preparation commit and clean checkout; immutable scientific/H1 identities
   and original preregistration/sidecar are available for comparison.
2. H2A0 already supplies declaration categories, ordered slots/rules, canonical identity
   rules and the invariant HOLD/no-gate-promotion boundary. This is a schema scaffold,
   not an implemented authority/content/runtime verifier.
3. H2A1 establishes prospective release/asset/custody identity, externally retrievable
   commit-pinned material, platform and custom signatures, credential-free reproduction
   and negative checks. Historical limitations and scoped maintainer adoption are retained.
4. The H1 mock-only scaffold explicitly refuses the live adapter. Its tests/receipts
   describe prior offline behavior; no new test result is claimed by this review.
5. The runtime defect and two permissible architectural directions are already stated:
   reviewed source-only bootstrap or externally verified immutable runtime. No need to
   reopen publication to formulate that runtime question.
6. There is sufficient documentary evidence to authorize a small offline design circuit.
   The current user instruction authorizes only this review, not that future circuit.

No H2A1 result authenticates an unselected future client's origin/license, proves
GetData/SOAP equivalence, proves gradient semantics or certifies executing bytecode.
The historical eight-point report is not retained numerical evidence and must not be
reconstructed or promoted into a response-contract acceptance result.

## Missing prerequisites, ordered by when they are needed

Before the first design circuit: a separate explicit authorization naming its one output
and exclusions. This receipt is not that authorization. No client or runtime installation
is needed for the proposed document-only task.

Before any implementation: select and review one runtime trust-root architecture; define
threat model, bootstrap/root-of-trust assumptions, privilege boundary, trusted interpreter
and standard-library scope, permitted imports, source/bytecode/native loading behavior,
TOCTOU protection, exact-byte execution mechanism, failure/reporting behavior and independent
review ownership. Decide which authority/content and retained-provenance evidence will
support each rule. Define deterministic synthetic fixtures and expected failures before
coding. No broad claim against arbitrary privileged host compromise is justified.

Before claiming external_trust_root PASS: implement and independently review the selected
mechanism and provenance path; retain real primary evidence and separate synthetic
acceptance inputs/results for each contract rule, including ambient imports, stale .pyc
and substitution after hashing. Preserve category separation and no-reuse requirements;
one declaration or repeated byte identity is not multiple independent kinds of evidence.

Before production/runtime closure or E0 readiness: selected/pinned/licensed client;
authoritative response semantics; complete egress/retry accounting; complete hashed runtime
closure and offline-install acceptance; full memory acceptance; approved frozen amendment;
independent final package audit; and separate explicit E0 authorization. These later needs
do not prevent paper design, but do prevent a readiness or execution claim.

Current Dockerfile names `python:3.12.7-slim-bookworm` without an image content digest and
installs requirements during build. `requirements.txt` names numpy==2.5.2 but is not a
hashed transitive runtime closure. Neither is proof of the required immutable runtime.
No Docker build or dependency installation was performed to inspect them.

## Exact write boundaries

“Touch” below means create/modify/delete or execute/import as operational code; reading
existing text for evidence is permitted. A directory prefix is not a blanket write grant.

**Current authorized allowlist — exactly one file:**

`docs/e0/h2/NS-001_H2A2_READINESS_SCOPE_REVIEW_v0.1.md`

**Proposed first future circuit — exactly one new file, only after authorization:**

`docs/e0/h2/NS-001_H2A2_RUNTIME_TRUST_ROOT_DESIGN_v0.1.md`

This proposed filename does not yet exist and is a recommendation from this review,
not a historical requirement. It is the entire proposed first-circuit write allowlist.
No implementation or test file would be touched by that circuit.

**Possible later implementation allowlist, NOT authorized or frozen here:**

- `e0/h2/runtime_trust_root.py` — proposed new isolated verifier/bootstrap module;
- `tests/test_e0_h2_runtime_trust_root.py` — proposed new offline synthetic acceptance;
- `docs/e0/h2/NS-001_H2A2_RUNTIME_TRUST_ROOT_IMPLEMENTATION_RECEIPT_v0.1.md` — proposed
  new implementation receipt.

These are exact candidate paths, not permission to create them. The approved design
must determine whether these suffice and request a revised exact allowlist before any
other file, fixture, primary-source deposit, native runtime or package is written. No
existing record supplies a broader H2A2 file authorization.

**Explicitly forbidden in this review and proposed first circuit:**

- Every existing `docs/e0/h2/H2A1_*` and `docs/e0/h2/NS-001_H2A1_*` record, including
  observations, transaction receipt and final verification reviews; every file beneath
  `docs/e0/h2/evidence/ns001-h1-audit-v1-publication-stop-20260924/`.
- `e0/h2/external_anchor_verifier.py`, `tests/test_e0_h2_external_anchor_verifier.py`,
  `tests/test_e0_h2_custody_workflow_validation.py`.
- `e0/h2/evidence_contract.py`, `tests/test_e0_h2_evidence_contract.py`, and
  `docs/e0/h2/H2_EVIDENCE_CONTRACT_DRAFT.md`; no relabeling declarations as verified gates.
- `e0/hardening.py`, `tests/test_e0_hardening.py`; do not remove the live-adapter refusal.
- `preregistrations/e0/NS-001_E0_STRIDE_REFINEMENT_PREREG_FROZEN_2026-09-02.md` and its
  `.sha256` sidecar; both existing GetData/interface draft files in the same directory.
- `ns001_tau_check.py`, `run_experiment.py`, `EXPERIMENT.md`, `protocols/day_one.json`,
  `protocols/sanity.json`, `protocols/smoke.json`, all `docs/e1-openai/` scientific records.
- `Dockerfile`, `requirements.txt`, `Makefile`, `.dockerignore`, `.gitignore`, `README.md`,
  `.github/workflows/ns001-h1-custody.yml`, `.github/workflows/ns001-sanity.yml`.
- The retained H1 ZIP at `/home/jacob/Documents/NS-001/audit/2026-09-03/NS001_H1_AUDIT_BUNDLE_20260903.zip`,
  committed/published copies and provenance, remote release/tag/assets/attestations/settings.
- Credential stores, .env files, target-data or run/output directories; no creation of
  E0 authorization, production manifests/packages, scientific receipts or result data.

All unlisted paths are denied for writes. Git metadata updates needed for the requested
receipt commit/push are bookkeeping, not authorization to change main or published refs.
Future fixture execution must use disposable external scratch space only when separately
authorized; no science/network/client/credential work is implied by “offline test.”

## Smallest defensible first H2A2 circuit and abort conditions

Recommend one **offline, document-only runtime trust-root design and acceptance-plan
circuit**, after separate authorization, producing only the proposed design path above.
It would use current committed specs as read-only inputs and:

1. Compare the two already-permitted architectural options against the three primary
   runtime guarantees and the three required negative acceptance cases.
2. Propose one mechanism or retain a justified unresolved choice; state trust assumptions,
   exact-byte execution boundary, import/bytecode/native-loading policy and TOCTOU handling.
3. Map each external_trust_root rule to primary/provenance/synthetic evidence and reviewer
   responsibility; identify runtime-lock/client dependencies that remain outside this slice.
4. Specify deterministic future tests and exact proposed implementation write paths.
   No code, fixtures, downloads, installs, test runs or runtime changes in this first circuit.
5. End with HOLD, unmet conditions and a separate authorization request for any later work.

Abort the future circuit with a bounded STOP finding in its authorized document if:

- preparation branch/authorized starting HEAD drifts, unexpected edits exist, an H1/H2A1
  input or frozen digest differs, or expected material is missing/ambiguous;
- a necessary claim requires unavailable authority/provenance, local-only hidden inputs,
  unsigned declarations treated as proof, or incompatible specs without a documented resolution;
- the proposed design cannot explain exact verified-byte execution, ambient import refusal,
  stale/unchecked bytecode refusal or hash-to-load/source substitution resistance within
  its declared threat model; do not weaken tests or promote the claim;
- a useful next step requires client acquisition/import, credentials, networking, an install,
  scientific/target-data access, a workflow run, an existing-file edit or any out-of-allowlist write;
- design review is being used to freeze an amendment, approve a package, mark a gate passed,
  alter historical evidence, broaden authority claims or infer E0 execution permission.

Record what is missing; do not repair it or automatically advance into a second circuit.
Production prerequisites being absent is a declared design boundary, not permission to
collect them during the design task. No next circuit is performed by this receipt.

## Closing verdict

- H2A2 purpose: narrowly scoped runtime trust-root review/proof of exact verified-code execution, with genuine authority/provenance/acceptance evidence; no historical all-gates implementation mandate found.
- Satisfied prerequisites: H2A1 prospective custody/publication VERIFIED, anchored inputs, unchanged frozen preregistration, H2A0 contract and known runtime defect.
- Remaining prerequisites: separate design authorization, architecture/threat/evidence/acceptance review; later implementation and all eight substantive gate closures remain missing.
- Allowed scope: this receipt only now; proposed next circuit is one new runtime trust-root design document only, separately authorized.
- Forbidden scope: every pre-existing file, H2A1 evidence, scientific/frozen records, live adapters, client/credential/network operations and external publication/runtime mutations.
- First bounded circuit: offline document-only runtime trust-root design and acceptance plan; not performed.
- Readiness verdict: READY TO PROPOSE/AUTHORIZE that bounded design circuit; NOT READY for implementation, substantive gate passage or E0. H2A2 implementation UNSTARTED.
- E0 status: HOLD; Gate 1 remains PARTIAL, unadvanced.
- H2A1 status: VERIFIED for scoped prospective custody/publication auditability, unchanged.
- One next bounded action only: obtain separate authorization for the one-file runtime trust-root design/acceptance-plan circuit. Stop here.
