# NS-001 H2A1 publication target re-freeze v0.1

Recorded 2026-09-24T17:44:30.319546+00:00. Bounded target/provenance amendment only; publication authorization: **NO**.
Preparation branch: `codex/e0-h2-preparation`; HEAD before: `1ae63e08aac37b99f370891d354c8f6bfd9df231`.

## Basis and scope

Old target: `ef71e56263da8e4d0dfcd5228795356e38b27998`. New frozen target: `d9dcfbef1bea173b316bc968fd71421c982422c3`.
Fetched origin/main and independently read GitHub's main ref, commit-pinned workflow bytes,
release/tag/run inventories and immutability state. Main resolves to the new target,
a descendant of the old target. Their diff contains exactly `.github/workflows/ns001-sanity.yml`.
The new target includes push branches `['**']` and tags-ignore `['ns001-h1-audit-v1']`;
the publication-tag exclusion is VERIFIED. Custody workflow bytes are unchanged.
This amendment binds the proposal to that trigger mitigation; it grants no execution permission.

This receipt supersedes only operative target-dependent values in the original
`NS-001_H2A1_PREPUBLICATION_REVIEW_v0.1.md` and subsequent readiness, provenance,
and verification proposals that inherit its target. Historical observations, previous
hashes, prior receipts and the uncommitted publication STOP receipt remain historical,
byte-preserved records. They are not rewritten. No old temporary staging copy is an
operative new input: future preparation must extract the bytes below and verify their digest.

## Exact amendments and preserved values

| Target-dependent field | Re-frozen value |
| --- | --- |
| Publication/tag target; future release target_commitish | `d9dcfbef1bea173b316bc968fd71421c982422c3` |
| JSON publication_commit | `d9dcfbef1bea173b316bc968fd71421c982422c3` |
| JSON authority_text; release body | Only the embedded old target becomes the new target |
| Provenance SHA-256; expected provenance attestation subject digest | `ff649229275d88be762e2b762b35b27c3aac8e252a070ac39b18bffc06142d12` |
| Dispatch publication_commit and provenance_sha256 | New target and new digest above |
| Dispatch main-ref constraint; workflow/source/signer/run commit constraints | `d9dcfbef1bea173b316bc968fd71421c982422c3` |
| Verification --signer-digest and --source-digest; tag dereference constraint | `d9dcfbef1bea173b316bc968fd71421c982422c3` |

The provenance transformation replaces exactly two 40-byte target occurrences in the
original 2298-byte JSON. Parsed changed keys are exactly `publication_commit` and
`authority_text`. All other JSON bytes remain identical. Release body changes solely
by that same target substitution. Previous provenance digest
`9f67d54f2852c386384b9ea1bd1c231bcbb572490bd8b94b9ce84396a7fbac89` remains the historical freeze.

Preserved without amendment:

- Tag `ns001-h1-audit-v1`; release title `NS-001 H1 mock-only audit bundle v1`.
- ZIP `NS001_H1_AUDIT_BUNDLE_20260903.zip`, 51103 bytes, SHA-256
  `a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`.
- H1 source `6e33cb9ca7019e50e2f247ade9ae8c9a7b40d3ff`; H1 remains mock-only.
- Custody workflow `.github/workflows/ns001-h1-custody.yml`, SHA-256
  `236b8f30a27fa1c3c26f134c794f2e3e989b9b31d1e3adfbcfae18e21fa420bf`; manual-only trigger and permissions unchanged.
- Repository `vortexpixelz/ns001` / 1354037143; publisher, both uploaders and dispatch actor
  `vortexpixelz` / 202687650. Workflow signing identity is distinct from uploader identity.
- Mandate scope and adoption `cd6e3eb806fa5a5045daaf35904ea927cec68f55`, recorded
  `2026-09-22T01:10:47Z`; GitHub-only evidence-deposit plan adopted at
  `e1d06a6b09b26a8dd8928c2f674aa2dc33a0b069`, including deletion and retrieval assumptions.
- Provenance filename `NS001_H1_PUBLICATION_PROVENANCE.json`; length 2298 bytes.
- Release staging/verification sequence; final draft=false, prerelease=false,
  make_latest=false; exactly ZIP and provenance as proposed uploaded assets.
- Attestation toolchain and trusted-root policy from
  `NS-001_H2A1_ATTESTATION_VERIFICATION_TOOLCHAIN_v0.1.md`; pinned gh 2.101.0 and signing action unchanged.
- All scientific artifacts, frozen preregistration/sidecar, historical limitations,
  no retrospective custody/authorship/corporate/institutional certification, and Gate 1 PARTIAL.

## Exact new frozen provenance bytes

UTF-8 without BOM, LF, sorted keys, two-space indentation, exactly one final LF.
Fence lines excluded. SHA-256 `ff649229275d88be762e2b762b35b27c3aac8e252a070ac39b18bffc06142d12`. No standalone file is required by the existing
embedded-byte design. The final release body is exactly the decoded `authority_text`
value below plus one LF (UTF-8), SHA-256 `a06e846a597de66acccf44ac219925c3c5fc61dd50f815f3b2c946feeb6f4a24`. No generated notes or added wording.

```json
{
  "artifact_name": "NS001_H1_AUDIT_BUNDLE_20260903.zip",
  "artifact_sha256": "a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f",
  "artifact_size": 51103,
  "authority_text": "This prospective preservation deposit is designated for the repository-defined NS-001 project by its authenticated maintainer, personal GitHub account vortexpixelz (account ID 202687650), for public repository vortexpixelz/ns001 (repository ID 1354037143), under the scoped mandate adopted in commit cd6e3eb806fa5a5045daaf35904ea927cec68f55, recorded at 2026-09-22T01:10:47Z. Its subject is the unchanged NS001_H1_AUDIT_BUNDLE_20260903.zip, 51103 bytes, SHA-256 a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f, preserving H1 source commit 6e33cb9ca7019e50e2f247ade9ae8c9a7b40d3ff for independent inspection. H1 remains H1_MOCK_ONLY_HOLD; reported historical mock tests are not new tests or scientific validation. The publication target d9dcfbef1bea173b316bc968fd71421c982422c3 is distinct from the H1 source checkpoint. Authority is a self-declared prospective maintainer mandate, not corporate, institutional, Symonic LLC, or third-party certification. This statement establishes no original creation time or place, original authorship, pre-publication custody, historical possession, or retrospective project authorization. Actual publication, uploader, signer, identifiers, service timestamps, witnessed timestamps and retrieval observations must be established separately from observed records; this text does not assert that those events have occurred. No scientific artifact is changed. E0 remains HOLD, Gate 1 remains PARTIAL, and H2A2 remains UNSTARTED. Publication does not authorize experiments or subsequent workflow execution.",
  "e0_status": "HOLD",
  "h1_source_commit": "6e33cb9ca7019e50e2f247ade9ae8c9a7b40d3ff",
  "h1_status": "H1_MOCK_ONLY_HOLD",
  "h2a2_status": "UNSTARTED",
  "historical_custody_established": false,
  "mandate_adoption_commit": "cd6e3eb806fa5a5045daaf35904ea927cec68f55",
  "mandate_recorded_at": "2026-09-22T01:10:47Z",
  "publication_commit": "d9dcfbef1bea173b316bc968fd71421c982422c3",
  "publisher_account_id": 202687650,
  "release_tag": "ns001-h1-audit-v1",
  "repository_id": 1354037143,
  "schema": "ns001.h1.publication-provenance.v1"
}
```

## Final dormant workflow inputs and verification constraints

```json
{
  "release_tag": "ns001-h1-audit-v1",
  "publication_commit": "d9dcfbef1bea173b316bc968fd71421c982422c3",
  "provenance_sha256": "ff649229275d88be762e2b762b35b27c3aac8e252a070ac39b18bffc06142d12",
  "authorization": "ATTEST-EXACT-H1"
}
```

Dispatch ref remains `main`, requiring it to resolve to `d9dcfbef1bea173b316bc968fd71421c982422c3` with the exact unchanged
workflow digest. The acknowledgement string is not authorization. A future dispatch
requires separate authorization and successful publication verification; neither happens here.
The tag must dereference to `d9dcfbef1bea173b316bc968fd71421c982422c3`. Future run head, workflow commit
(`GITHUB_WORKFLOW_SHA`), attested source and signer digest must equal `d9dcfbef1bea173b316bc968fd71421c982422c3`.
Stop on drift; never silently substitute a ref or commit.

Verification retains repository `vortexpixelz/ns001`, source ref `refs/heads/main`, issuer
`https://token.actions.githubusercontent.com`, certificate identity
`https://github.com/vortexpixelz/ns001/.github/workflows/ns001-h1-custody.yml@refs/heads/main`,
and predicate type `https://github.com/vortexpixelz/ns001/predicates/h1-custody/v1`.
Both `--signer-digest` and `--source-digest` must be `d9dcfbef1bea173b316bc968fd71421c982422c3`. Use the toolchain receipt's
corrected `--cert-identity` policy without combining `--signer-workflow`.
Check both exact subject digests: unchanged ZIP and newly frozen provenance above.
Preserve all other verification requirements: immutable final release, exact asset
names/sizes/uploaders, anonymous byte retrieval, duplicate-key rejection, usable required
publication timestamps, signature/trust-root verification, separate automatic release
attestation checks, and commit-pinned durable post-event evidence deposit. No future IDs,
service timestamps, certificate or successful verification result are invented here.

## Verification and preservation

Offline checks pass: original provenance digest, exactly two replacements, unchanged
length/serialization, exactly two changed JSON keys, release-body derivation, and all
13 mandatory typed fields against the workflow's literal expected contract. This does
not execute the workflow or any scientific tests. Local ZIP bytes match the frozen
length/digest. All pre-existing tracked artifact hashes and the untracked STOP receipt
are compared against the preflight inventory before commit; only this receipt is added.
STOP receipt is excluded from staging and retains SHA-256
`30f4c22bff968f02d24ea6fb9ad663ec0854354579cef984abbc6314575ce2de`.

Read-only GitHub inventories show no releases or tags, hence no release assets;
H1-digest owner attestation lookup returns HTTP 404 (bounded negative observation,
not universal proof of absence). The four existing run IDs remain 34488406675,
33563351013, 33563214294 and 33562657929; no new custody or scientific run.
No publication, dispatch, attestation creation or settings mutation call is made.
Main remains `d9dcfbef1bea173b316bc968fd71421c982422c3` and immutable releases remain enabled.

## Final state

- Target-dependent proposal: RE-FROZEN to `d9dcfbef1bea173b316bc968fd71421c982422c3`; original records preserved.
- Tag-trigger mitigation: VERIFIED at the new target.
- Publication authorization: NO.
- H2A1: local byte identity VERIFIED; independent external auditability PARTIAL.
- E0: HOLD; no execution or query authorized or performed.
- H2A2: UNSTARTED.
- One next bounded action: separately authorized independent read-only readiness review of this amended target/provenance freeze; do not publish or dispatch.
