# NS-001 H2A1 publication preparation v0.1

## Scope and preflight

Branch: `codex/e0-h2-preparation`; HEAD before:
`cd6e3eb806fa5a5045daaf35904ea927cec68f55`. Initial tree clean.
The publisher-mandate adoption receipt exists, records **ADOPTED**, and remains
unchanged. Its earlier prohibition on preparation described that earlier circuit;
the present user instruction explicitly authorizes only the preparation below.
Publication, workflow execution, E0 and H2A2 remain unauthorized.

Fresh authenticated reads identify personal account `vortexpixelz`, ID `202687650`,
with admin rights on public `vortexpixelz/ns001`, repository ID `1354037143`.
Release and tag inventories were empty. The H1 digest attestation query returned
404; no attestation was retrieved. E0 is HOLD; H2A2 is unstarted.

The user reports that `jwalkjcuo`, `symjaco` and `vortexpixelz` are connected accounts
and members of Symonic LLC. This is user-provided relationship context, not verified
corporate delegation. No account switch, membership audit, corporate authority claim
or expansion of the adopted personal-account mandate occurred.

## Immutable-release setting

Exact endpoint: `repos/vortexpixelz/ns001/immutable-releases`.
Before: `enabled: false`, `enforced_by_owner: false`.
One authorized PUT enabled repository release immutability.
Subsequent GET: **`enabled: true`, `enforced_by_owner: false`**.
No release, tag or asset was created. Owner-wide policy was not changed.
The setting is prospective; there are no existing releases to assess.

GitHub documents this administrative setting and immutable release asset/tag
protection. It does not make release metadata immutable or guarantee permanent
availability. [Repository API](https://docs.github.com/en/rest/repos/repos#enable-immutable-releases),
[immutable releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases).

## One custody-only workflow

Path: `.github/workflows/ns001-h1-custody.yml`.
SHA-256: `fdbaa3ca10bec3a4f668b43f8f6efaa8e0fb37ea13bb18e2b42ade157d8fb251`.

The workflow has only `workflow_dispatch`: no push, pull-request, release, schedule
or reusable-workflow trigger. Dispatch requires a future explicit execution
instruction; the confirmation input is an operator acknowledgement, not independent
proof of authorization. The job restricts repository ID/name, actor ID `202687650`,
triggering account `vortexpixelz` and first run attempt. One concurrency group
serializes runs. These restrictions do not impose an irreversible one-attestation
lifetime counter: a later operator must check prior attestations and authorize
only the single intended run. No dispatch was performed in this circuit.

Inputs, with no operative defaults: approved release tag, exact publication commit,
approved provenance SHA-256, and `ATTEST-EXACT-H1` acknowledgement. This is a
**post-publication custody verifier**: a future authorized publication must already
have created an immutable release and its exact assets. This workflow cannot publish
those assets itself and does not claim that signing predates publication.

Before signing, an inline standard-library Python guard:

- Confirms the public repository identity and an existing non-draft immutable release.
- Resolves its tag, including bounded annotated-tag dereferencing, to the approved
  full commit SHA; accepts no floating commit input.
- Requires exactly one named ZIP and one `NS001_H1_PUBLICATION_PROVENANCE.json`,
  both uploaded by the adopted personal account. A bot or another user is rejected;
  broadening that policy would require a separate review.
- Downloads anonymously from that repository's exact GitHub release locator,
  without passing tokens to redirects; enforces byte limits and SHA-256 matching.
- Requires the ZIP to be exactly 51,103 bytes with the fixed digest below. It neither
  extracts nor runs it. No arbitrary URL, artifact filename or ZIP digest is input.
- Requires provenance matching the approved digest and the typed identity/scope
  fields below. Extra narrative in the approved provenance remains a publisher claim.
- Produces a custom predicate about observation of existing published bytes, recording
  release/asset identifiers, uploader, observation time, workflow SHA/ref and actor.
  It explicitly disclaims historical custody, authorship and scientific authority.

The future provenance asset must be at most 65,536 bytes, valid JSON, and contain:
`schema: ns001.h1.publication-provenance.v1`; numeric `repository_id: 1354037143`;
numeric `publisher_account_id: 202687650`; exact `artifact_name`, `artifact_size`
and `artifact_sha256`; `h1_source_commit: 6e33cb9ca7019e50e2f247ade9ae8c9a7b40d3ff`;
`mandate_adoption_commit: cd6e3eb806fa5a5045daaf35904ea927cec68f55`;
`publication_commit` and `release_tag` matching approved inputs;
boolean `historical_custody_established: false`; `e0_status: HOLD`;
`h2a2_status: UNSTARTED`. This defines future guard inputs, not a provenance package
created now. The complete textual authority statement and evidence requirements of
the prior specification still apply beyond these mechanically checked fields.

One pinned action invocation signs the two verified files in one attestation, using
custom predicate type `https://github.com/vortexpixelz/ns001/predicates/h1-custody/v1`
(an identifier, not a claim that a schema web page has been published).
Action: `actions/attest@1e69f48acb82d1966a394da916b4c1698aa569d6`, resolved from
upstream v4 and inspected at that exact commit (`action.yml`, `src/main.ts`).
Registry publishing and storage-record creation are explicitly false.
There is no checkout, package installation, arbitrary build, upload-artifact action,
release-writing step or scientific code execution. The bundle digest/location is
reported after a future successful attestation; durable anonymous distribution of
that verification bundle remains a later separately authorized publication concern.
[Official action](https://github.com/actions/attest/tree/1e69f48acb82d1966a394da916b4c1698aa569d6).

### Permissions and identity limits

Workflow-level permissions are empty. Only the custody job requests:
`id-token: write` for signing identity and `attestations: write` for the attestation.
No contents-write, packages-write, artifact-metadata-write or PR approval grant.
Public retrieval uses no token. The existing repository settings remain:
Actions enabled; all actions allowed; default workflow permission read;
PR approval false; global SHA-pinning requirement false. The action's bundled code
is pinned; `ubuntu-24.04`, its Python runtime and GitHub service are not immutable
runtime images. No runtime-lock gate is passed by this workflow.

The signed workflow identity is not the human publisher identity. Future verification
must constrain issuer, repository and exact signer workflow/source; uploader/actor
fields and custom predicate claims require the stated interpretation. Settings and
source inspection establish preparation, not successful attestation generation or
plan eligibility through execution. No such test was attempted.

### Branch deployment limitation

The new file is prepared on the existing branch only. GitHub requires a manual
workflow file on the default branch before dispatch. `main` remains unchanged;
no merge, PR or default-branch change is made. Default-branch placement must be
separately authorized/reviewed before a future run. The workflow is therefore
prepared and remotely retained, **not yet dispatch-ready on the default branch**.
[Manual trigger requirements](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onworkflow_dispatch).

## Validation and preservation

YAML structure, manual-only trigger, exact two job permissions, and embedded Python
syntax passed local checks. Eleven offline mocked guard cases passed: matching
input, mutable release, draft release, wrong uploader, wrong size, duplicate asset,
wrong locator, corrupted ZIP bytes, provenance digest mismatch, wrong commit and
historical-custody overclaim. Network was replaced with in-memory responses; files
were confined to temporary directories. The real retained ZIP was read only and
never uploaded. The attestation action was not executed. These are guard checks,
not a live GitHub workflow or E0 test.

Before commit, all 43 pre-existing repository file hashes and the retained ZIP
hash/size are unchanged. Only the new workflow and this one receipt are added.
Authenticated read-only comparisons confirm the sole settings change is immutable
releases false → true. Releases/tags remain empty; workflow/run inventories and
H1 attestation-query response remain unchanged before push. The query's 404 is
not a universal nonexistence proof; absence of a creation operation and unchanged
run/inventory evidence support the bounded “none created in this circuit” finding.
The branch push is checked separately for exact remote workflow/receipt bytes.

## Closing receipt

- **Mandate state:** ADOPTED; the present instruction authorizes preparation only.
- **Immutable-release configuration:** enabled, not owner-enforced; verified by GET.
- **Custody workflow:** `.github/workflows/ns001-h1-custody.yml`, SHA-256
  `fdbaa3ca10bec3a4f668b43f8f6efaa8e0fb37ea13bb18e2b42ade157d8fb251`.
- **Actions permission state:** repository default read unchanged; custody job only
  `id-token: write` and `attestations: write`; no contents-write grant.
- **Changes made:** enabled repository immutability; added one manual-only custody
  workflow and this receipt. No default-branch placement or workflow execution.
- **Changes not made:** no other setting, prior workflow, prior receipt, frozen
  artifact, scientific design, account/organization policy or branch topology change.
- **Release created:** NO.
- **Tag created:** NO.
- **ZIP uploaded:** NO.
- **Attestation created:** NO.
- **H1 ZIP:** `NS001_H1_AUDIT_BUNDLE_20260903.zip`, 51,103 bytes, SHA-256
  `a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`;
  source commit `6e33cb9ca7019e50e2f247ade9ae8c9a7b40d3ff`.
- **H2A1:** local identity VERIFIED; external auditability PARTIAL. All eight
  substantive H2 gates remain unresolved; preparation is not external evidence closure.
- **E0:** HOLD; no execution or JHTDB request. Gate 1 remains PARTIAL.
- **H2A2:** unstarted.
- **One recommended next bounded action:** independent read-only review of the
  prepared custody workflow and future default-branch placement plan. No merge,
  dispatch, publication or follow-on preparation is authorized by this receipt.
