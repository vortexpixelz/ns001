# NS-001 H2A1 external anchors: independent re-verification v0.1

## Scope and state

Branch: `codex/e0-h2-preparation`. HEAD before review:
`5fefcce5676c0f0ac8346d5eae10f71ab491509c`. Initial working tree: clean.
External observations: `2026-09-21T20:12:36.942833+00:00` UTC.
Public remote branch matched that HEAD; remote main was
`2075dd6cc70e4a922b41c2f9a75107251ac090cf`.

**Result: original local identity-only H2A1 verification reproduced; an
unqualified four-independent-external-anchor VERIFIED status is not established.
External auditability is PARTIAL.** E0 remains HOLD; Gate 1 remains PARTIAL.
H2A2 is unstarted. No experiment, JHTDB request, or scientific evaluation occurred.

This new receipt uses the existing `docs/e0/h2/` H2A1 convention instead of the
suggested `docs/e0-h2/` directory. Existing receipts and observations are preserved.
Inventory reviewed: `H2A1_EXTERNAL_ANCHOR_VERIFICATION_RECEIPT.md`,
`H2A1_EXTERNAL_ANCHOR_OBSERVATIONS.json`,
`H2A1_RECONCILIATION_REVIEW_RECEIPT.md`, the governing
`H2_EVIDENCE_CONTRACT_DRAFT.md`, and `e0/h2/external_anchor_verifier.py`.
The retained ZIP also contains a manifest, checksums, source-version record and
checkpoint receipt; these are project-produced evidence, not independent attestations.

## Independent verification method

Fetched public HTTPS Git objects from `https://github.com/vortexpixelz/ns001.git`
into a fresh temporary bare repository, with system/global Git configuration and
credential helpers disabled. Local repository refs were not changed by this check.
Read commit objects with replacements disabled and lazy fetching disabled;
recomputed Git commit SHA-1 using the object header, compared raw bytes to local
objects, and independently checked ancestry. Read remote blobs and compared their
bytes with the local frozen file. No declaration or sidecar was accepted as proof
of content. Hashes below are SHA-256 unless explicitly identified as Git IDs.

Read the retained ZIP without extracting or executing members; verified its whole
file digest, member coverage and source correspondence to freshly fetched objects.
Read the public GitHub PR #4 and releases APIs without credentials. Transport was
ordinary HTTPS, relying on the host's TLS trust store and GitHub's repository
mapping; no independent author attestation, signed timestamp, or retained TLS
transcript was established. This is adequate for the reported current retrieval
and byte comparisons, not an authenticated historical chain of custody.

## 1. H1 checkpoint

**Classification: VERIFIED WITH RESIDUAL ASSUMPTION.**

Claim supported: the intended H1 source checkpoint exists and its identity and
ancestry match the retained local object. Canonical project object:
[H1 commit](https://github.com/vortexpixelz/ns001/commit/6e33cb9ca7019e50e2f247ade9ae8c9a7b40d3ff).

- Git commit: `6e33cb9ca7019e50e2f247ade9ae8c9a7b40d3ff`;
  tree: `f15c46c605b48c0eaac97943cb02e65c05e72031`.
- Raw commit: 253 bytes;
  `875743e5a52a4fe6f0b3f834f62a5a9119defbedc17ebee23bcbbaf15b42296d`.
- Parent is anchor 2. It is an ancestor of both fetched branch heads. Remote and
  local raw bytes agree. Commit author/committer time is
  `2026-09-03T08:44:54-04:00`, a self-asserted field, not trusted time.

Existence and identity are verified by independent remote retrieval. Authority is
limited to accepting this GitHub repository as the canonical project record; the
commit has no embedded signature. [PR #4](https://github.com/vortexpixelz/ns001/pull/4)
currently reports merged at `2026-09-09T10:20:16Z`, head equal to H1, merge commit
`2075dd6cc70e4a922b41c2f9a75107251ac090cf`. This corroborates project integration;
it does not certify tests, loaded runtime, reviewer independence, or live behavior.
No historical 37-test or 79-test run was re-established by reading this object.

## 2. Scientific-base checkpoint

**Classification: VERIFIED WITH RESIDUAL ASSUMPTION.**

Claim supported: the intended baseline source tree and its ancestry to H1 remain
available and match local bytes. Canonical project object:
[scientific-base commit](https://github.com/vortexpixelz/ns001/commit/0393315223df8ed90f20f0c821508cc98bea08d1).

- Git commit: `0393315223df8ed90f20f0c821508cc98bea08d1`;
  tree: `e20dffc32c1461b0f7ef3a7bae209b19349b47fa`.
- Raw commit: 271 bytes;
  `943d1b94830de6d7031f48e94b9cabab9f03c02ce69f30454037b49f260faf52`.
- Parent: `0cac26bfd9b5ec8b916da64422c9e0f7fe9b0206`.
  Author/committer time: `2026-09-02T01:38:52-04:00`, self-asserted.

Existence, identity and local correspondence are verified. It is H1's direct
parent and an ancestor of both fetched heads. The unsigned project's designation
of this tree as the scientific base is not independent scientific validation or
proof of prior approval. No Gate 1 assumption is resolved by its identity.

## 3. Frozen preregistration

**Classification: VERIFIED WITH RESIDUAL ASSUMPTION.**

Claim supported: the exact frozen document bytes persist in the designated
historical commits, current remote heads, and local file. Canonical project object:
[commit-pinned frozen document](https://github.com/vortexpixelz/ns001/blob/0393315223df8ed90f20f0c821508cc98bea08d1/preregistrations/e0/NS-001_E0_STRIDE_REFINEMENT_PREREG_FROZEN_2026-09-02.md).

- Size: 9,923 bytes; SHA-256:
  `a2a8523c065d4d41155aa29d367c888d49ab3032f6075b8cebbd2475ff1efd78`.
- Git blob: `eaeb0805bd5950808705dc646bf8ee6063bdae88`.
- Base, H1, fetched main and fetched H2 branch blobs match the local file exactly.

Existence, byte identity and correspondence are verified independently of the
sidecar. Authority remains the project's freeze designation. Neither a digest nor
commit timestamp independently proves when freezing occurred, pre-outcome custody,
approval, scientific adequacy, or authorization to execute. An immutable reference
is available; no mutable branch webpage is needed for the identity claim.

## 4. H1 audit bundle

**Classification: PARTIAL.**

Claim supported: the retained archive is the exact previously declared byte object
and its included source material corresponds to H1. Retained source:
`/home/jacob/Documents/NS-001/audit/2026-09-03/NS001_H1_AUDIT_BUNDLE_20260903.zip`.
**No canonical externally retrievable archive or independent custody attestation
was identified in the inspected evidence.** This is not a broken local object.

- Size: 51,103 bytes; SHA-256:
  `a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`.
- Non-symlink file; 11 unique members; all 9 manifest payload length/hash rows and
  all 10 checksum rows verified. Checksums cover every member except themselves.
- Six source members match freshly fetched H1 blobs byte-for-byte. The included
  full-index binary patch matches the independently generated base-to-H1 diff.
- Internal manifest schema: `ns001.h1.external-audit-manifest.v1`; status:
  `H1_MOCK_ONLY_HOLD`; creation time `2026-09-03T13:44:53+00:00` is self-reported.

Existence and local identity are verified; source correspondence is independently
cross-checked. Authority and custody remain unverified: the archive describes its
origin as this repository, and its manifest/checkpoint receipt are internal claims.
Its location outside the checkout is storage separation, not independent authority.
Internal checksums cannot authenticate their own author. The receipt explicitly
reports historical tests rather than reproducing them during packaging, and does
not establish loaded-bytecode provenance or a production manifest.

The public releases API returned zero releases and no assets; neither fetched
current tree contains a ZIP path. These bounded searches do not prove that no copy
exists elsewhere. A hash preserves an immutable identity, not remote availability.
No new archive, upload, custody record, or substituted evidence was created.

## Provenance limits and discrepancies

The first three anchors have immutable project Git references and were independently
retrieved from GitHub. They are not merely local declarations, but they share one
publisher and do not constitute independent third-party trust roots. The fourth
has only local retrieval established; its source provenance is project-derived.
None requires mutable webpage prose for byte identity. Branch refs, PR metadata and
release listings are mutable observations, not immutable historical attestations.

For reproducibility, public API endpoints inspected were
`https://api.github.com/repos/vortexpixelz/ns001/pulls/4` and
`https://api.github.com/repos/vortexpixelz/ns001/releases?per_page=100`.
Observed response-byte digests were respectively
`357a7578d3fa406f114390f5eb3def3a4d0f98ba6d1a0b50ab07f68d8ead4d4e` and
`2ba33ca0557f1bb5b7ba88d67f9d0093c7185a36ec51fe2b7bd9372d3e001d6d`.
The response files are temporary inspection material, not a durable independent
attestation; the receipt preserves these observations and identifiers only.

There is no observed identity mismatch with prior H2A1. Its detailed receipt
explicitly defines independence as separately reading bytes, excludes custody and
authority, and leaves every substantive gate unresolved. That bounded claim
survives. Reading its headline “four external identities” as four independently
authoritative, externally retrievable anchors would overstate the evidence,
particularly for the ZIP. All four are locally auditable by a custodian with the
retained objects; **all four are not established as independently externally
auditable**. H2A1 remains VERIFIED only in its original byte-identity scope;
the stronger external-authority claim is PARTIAL, not VERIFIED.

## Residual gaps, preservation and boundary

H2A1 auditability gap: no established externally retrievable exact ZIP plus
authenticated provenance/custody binding. The first three additionally retain the
assumption that GitHub's project mapping and unsigned project designations identify
the intended authoritative records; historical authorship and timing are unproven.

Later substantive H2 work, including any separately authorized H2A2 trust-root
review, must address authority/content/custody and runtime binding as required by
the governing contract. This circuit neither implements nor passes those gates.
Missing client response-contract and request/transport accounting evidence concerns
the future live adapter, not the correctness of these Git/ZIP hash comparisons.
GitHub retrieval does not supply JHTDB response semantics, loaded-client provenance,
request accounting, dependency locks, resource bounds or final package approval.
All eight gates remain unresolved: `external_trust_root`, `client_source`,
`response_contract`, `transport_accounting`, `dependency_runtime_lock`,
`maximum_partition_memory`, `amendment_freeze`, `final_manifest_package_audit`.

Preservation check: all 37 pre-existing non-Git file hashes (including ignored
cache files), frozen preregistration and sidecar, prior receipts and scientific
artifacts must match the captured baseline before commit. Only this new receipt is
permitted in the commit. No test suite rerun is claimed; validation here is direct
object/hash/ancestry/archive verification. No missing evidence was repaired.
The workflow stops after publishing this receipt. Scientific/governance gates
remain unresolved independently of that workflow stop; no E0 permission follows.

**One recommended next bounded H2 action:** separately authorize an H2A1
preservation-only custody/retrievability closure for the existing exact H1 ZIP:
identify an approved archive destination and publish those unchanged bytes with
their digest and an explicit provenance/custody record. This would address
availability without itself establishing historical authority or passing H2A2.
Do not begin that action in this circuit.
