# NS-001 H2A1 custody workflow default-branch placement v0.1

## Authorized scope and baseline

This circuit implements the user's explicit authorization for one workflow-only
commit on current main. It does not authorize dispatch or publication.

- Preparation branch: `codex/e0-h2-preparation`.
- Preparation HEAD before: `abe49dc972b9c5b2ccf305f8c7f1f327258ff6a8`.
- Fetched origin/main before: `2075dd6cc70e4a922b41c2f9a75107251ac090cf`.
- Default branch independently reported by GitHub: `main`.
- Main after / placement commit: `ef71e56263da8e4d0dfcd5228795356e38b27998`.
- Exact changed path: `.github/workflows/ns001-h1-custody.yml`.
- Source: that path at correction commit `abe49dc972b9c5b2ccf305f8c7f1f327258ff6a8`.
- Workflow SHA-256: `236b8f30a27fa1c3c26f134c794f2e3e989b9b31d1e3adfbcfae18e21fa420bf`.

Initial preparation tree was clean. Main lacked the custody path; no conflict or
material drift was found. A temporary local branch `codex/h2a1-custody-placement`
was created from fetched origin/main in `/tmp/ns001-custody-placement`. Exact Git
blob bytes were copied from the correction commit, hashed, and committed alone.
Main was rechecked immediately before a normal fast-forward push. No preparation
history, tests, receipts, or other content was carried onto main. The placement
commit has exactly the previous main as its sole parent. No PR or merge was used.
The temporary branch/worktree is retained locally, clean, for inspection; no
remote temporary branch was published. The pre-existing local main pointer was
not repointed; authoritative main in this receipt means GitHub's default branch.

## Independent post-placement verification

Verified at 2026-09-23T16:09:58.383716+00:00 UTC using read-only GitHub API responses:

1. Main ref resolves to the placement commit above.
2. Contents API at that full commit returns workflow bytes with the exact digest.
3. Commit API returns exactly one changed path and the expected sole parent.
4. Source/destination bytes match; only `workflow_dispatch` is configured in the
   custody workflow. No dispatch operation was issued.
5. Main's existing `ns001-sanity.yml` push filters exclude this added path.
6. Repository run inventory remains the same four existing runs, IDs
   `34488406675`, `33563351013`, `33563214294`, `33562657929`; no new run observed.
7. Release and tag inventories remain empty. No release asset exists in those
   inventories. The H1 digest attestation query remains HTTP 404; this is a bounded
   negative observation, not a universal proof about all possible attestations.
8. Immutable-release setting remains enabled, not owner-enforced. No settings
   mutation, release/tag creation, asset upload, or attestation action was issued.

The H1 ZIP remains unpublished through the inspected repository release route.
Its retained local bytes remain 51,103 bytes, SHA-256
`a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`, filename
`NS001_H1_AUDIT_BUNDLE_20260903.zip`. No upload occurred. This does not assert
exhaustive absence from every external location.

All pre-existing preparation-branch tracked file hashes remain unchanged; only
this receipt is added there. Frozen scientific artifacts and prior receipts are
byte-preserved. Workflow execution was neither needed nor used for verification.
The preceding correction's 132 passing offline checks remain the evidence for its
validation logic; this placement changes no workflow bytes and does not rerun
scientific code. No new claim of runtime or attestation verification is made.

## Closing state

- One-file diff verdict: VERIFIED, exact reviewed bytes, sole-parent fast-forward.
- Trigger boundary: VERIFIED manual-only; default-branch presence now satisfied.
- Workflow run created: NO observed; unchanged complete current run inventory.
- Publication objects created: NO; release/tag inventories empty, no publication
  operations, attestation query unchanged as qualified above.
- Publisher mandate: ADOPTED, unchanged; placement does not expand its scope.
- H2A1: local identity VERIFIED; independent external auditability PARTIAL.
  All eight substantive H2 gates remain unresolved: external_trust_root,
  client_source, response_contract, transport_accounting, dependency_runtime_lock,
  maximum_partition_memory, amendment_freeze, final_manifest_package_audit.
- E0: HOLD; no execution or JHTDB request. Gate 1 remains PARTIAL.
- H2A2: UNSTARTED.
- One next bounded action: separately authorize a read-only prepublication review
  of the exact proposed release/tag/commit and provenance inputs, including durable
  verification-material retrieval, without publication or workflow dispatch.
