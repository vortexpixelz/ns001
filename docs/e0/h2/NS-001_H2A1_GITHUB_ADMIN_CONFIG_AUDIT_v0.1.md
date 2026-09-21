# NS-001 H2A1 authenticated administrator/configuration audit v0.1

## Scope and identity

Review date: 2026-09-21 UTC. Branch `codex/e0-h2-preparation`; HEAD before
`447323a60b50c04c8c5a77ef2736358e180bcff5`. Initial working tree clean.
The preceding authority/custody specification and GitHub feasibility receipt remain
unchanged and govern the claim ceiling. This audit distinguishes account rights,
repository configuration, service capabilities, project mandate and publication.

Existing GitHub CLI authentication successfully identified `vortexpixelz`, account
ID `202687650`, type `User`. No login, credential creation/change, token display or
credential export occurred. All API calls used explicit GET. Repository identity:
`vortexpixelz/ns001`, ID `1354037143`, public, neither archived nor disabled, default
branch `main`, owned by that same personal account. This matches the intended
repository in prior receipts; it does not independently establish scientific or
custodial mandate. The authenticated account reports administrator rights through
both repository permissions and the collaborator-permission endpoint.

Local retained object was directly rehashed:
`/home/jacob/Documents/NS-001/audit/2026-09-03/NS001_H1_AUDIT_BUNDLE_20260903.zip`;
**51,103 bytes**, SHA-256
`a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`.
It remains unpublished in this circuit. No ZIP extraction or execution occurred.

## Authenticated observations

Endpoints below are relative to `https://api.github.com/`; values are observed
responses, not assumptions from documentation. Settings/inventories are reread
before commit. No write-capability probe was used.

| GET endpoint | Observed evidence | Meaning / limit |
| --- | --- | --- |
| `user` | Login/ID above; `plan.name` unavailable (`null` projection) | Authenticated personal identity established; billing plan not established. |
| `repos/vortexpixelz/ns001` | `admin`, `maintain`, `push`, `triage`, `pull` all true | Account repository rights established; token scopes for future writes were not tested. |
| `repos/vortexpixelz/ns001/collaborators/vortexpixelz/permission` | `permission: admin`, `role_name: admin` | Independent endpoint corroborates administrator role. |
| `repos/vortexpixelz/ns001/immutable-releases` | Successful response: `enabled: false`, `enforced_by_owner: false` | Feature configuration exposed and currently OFF; enabling is an explicit future settings change. |
| `repos/vortexpixelz/ns001/actions/permissions` | `enabled: true`, `allowed_actions: all`, `sha_pinning_required: false` | Actions enabled and no allowlist restriction shown; SHA pinning not enforced by this setting. |
| `repos/vortexpixelz/ns001/actions/permissions/workflow` | `default_workflow_permissions: read`, `can_approve_pull_request_reviews: false` | Read-only default; no automatic PR approval. Neither needs broadening for this route. |
| `repos/vortexpixelz/ns001/rulesets?includes_parents=true` | Empty list | No repository/parent rulesets returned. No test tag created. |
| `repos/vortexpixelz/ns001/releases?per_page=100` | Empty list | No releases, including drafts visible to this admin access. |
| `repos/vortexpixelz/ns001/tags?per_page=100` | Empty list | No tags returned. |
| `repos/vortexpixelz/ns001/actions/workflows` | Active reproducibility workflow `347905226`; dynamic Dependency Graph `347908986` | Existing workflows registered; neither establishes the needed custody attestation. |
| `repos/vortexpixelz/ns001/attestations/sha256:a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f` | HTTP 404 | No attestation retrieved. Does not distinguish missing subject evidence from endpoint/token eligibility restrictions. |

The remote commit endpoint resolves the exact reviewed HEAD. Remote workflow bytes
at that commit match local `.github/workflows/ns001-sanity.yml`, SHA-256
`e0cfb38e995793b3de388afad454cb7d69a01f8847bd304b249836dfca3d99e3`.
It has no custody attestation step. Its scientific-protocol jobs were not run.
This receipt path is outside its push path filters. No workflow file changed.

## Capability versus readiness

### Releases and exact tag binding

The account has the documented push-level right to create releases. Release API
writes require appropriately scoped content-write credentials; workflow-modifying
target commits may additionally require workflow-write authorization. Admin role
does not demonstrate that every future automation credential has those scopes.
A new release tag can target an exact commit SHA through `target_commitish`; if a
tag already exists that argument does not move it. No tag/version is selected or
created here. The reviewed SHA is remotely resolvable; a future designated target
must be checked again and must distinguish publication commit from historical H1.
[GitHub release API](https://docs.github.com/en/rest/releases/releases#create-a-release).

Account-level release/tag capability is **READY NOW**, with no observed ruleset
barrier. This is a capability inference from rights and configuration, not proof
from a test write. The immutable route **REQUIRES EXPLICIT CONFIGURATION** because
immutability is disabled. GitHub exposes the setting to this repository and
requires administrative authority for enabling it.
[Repository API](https://docs.github.com/en/rest/repos/repos#check-if-immutable-releases-are-enabled-for-a-repository).

Before publishing an immutable release, drafts/assets and ordinary tag references
must not be treated as frozen. Once published with immutability, attached assets
and tag are locked; title/notes and pre-release/latest status remain mutable.
Release deletion is possible; after deletion the tag may be deleted but its name
cannot be reused. Thus immutability protects identity, not perpetual availability.
[Immutable releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases).

### Actions and attestations

Actions platform readiness is **READY NOW**. Attestation production **REQUIRES
EXPLICIT CONFIGURATION**: a reviewed custody-only job with explicit
`id-token: write`, `attestations: write`, and needed content access. If the job also
publishes a release, it needs content-write authority appropriate to that operation.
A restricted job-level grant can retain the repository's read-only default; there
is no reason to enable PR approval or set all workflows to write.
[Workflow permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions).

Public repositories on current GitHub plans are documented as eligible; legacy
plans are excluded. Visibility qualifies, but the account response did not expose
its plan. Plan/endpoint eligibility remains **NEEDS ADDITIONAL SOURCE CHECK**;
the attestation 404 is not evidence of feature support or its absence. No billing
change or plan upgrade is justified by this audit.
[Attestation prerequisites](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations).

A future workflow can hash this exact file and sign a subject binding, but must
reject a different digest/size and describe importing/depositing existing bytes,
not claim it historically built the ZIP. GitHub-generated immutable-release
attestations and workflow-generated artifact attestations are distinct. The former
bind release/tag/commit/assets; the latter needs a specifically configured workflow.
Neither alone supplies the entire required project provenance narrative.

Verification authenticates certificate repository/owner/workflow context and signed
witnessed times. The workflow predicate can contain user-controlled assertions.
The human authenticated today, a future workflow signer, trigger actor and asset
uploader need not coincide; the publication package must record actual roles.
GitHub verifies account/workflow actions, not historical assertions or scientific
approval. No attestation has been generated or verified here.
[Attestation verification semantics](https://cli.github.com/manual/gh_attestation_verify).

### Authority and anonymous retrieval

The account is both authenticated user and repository owner/admin. That establishes
personal-account control of the named publication surface, not a separate
organization's authority. Project-level publisher mandate and an authenticated
provenance statement are still required under the fixed H2A1 criteria. Repository
ownership cannot circularly certify the ZIP's historical custody. Authority is
**REQUIRES PUBLISHER AUTHORITY / MANDATE**, with account-control evidence now present.

Public release assets support anonymous retrieval. Future stable locators can use
`https://github.com/vortexpixelz/ns001/releases/download/<approved-tag>/<exact-filename>`
and the assigned asset ID endpoint, bound to release ID, commit, size and digest.
These are templates, not created objects. An independent reviewer needs the actual
ZIP, immutable version/asset identifiers, digest/size, provenance, attestation
bundle, independently sourced trust roots, signer/predicate policy and retrieval/
verification instructions. Anonymous availability must be tested after publication;
an access-controlled attestation lookup alone is insufficient.
[Release asset API](https://docs.github.com/en/rest/releases/assets).

## Four-property configuration gap table

| Required property | Current classification | Exact remaining gap |
| --- | --- | --- |
| Byte identity | PARTIAL / RESIDUAL ASSUMPTION | Local bytes match; external authenticated binding and independent download do not exist. Immutable-release setting and selected custody mechanism require configuration. |
| Retrievability | READY NOW for public-hosting capability; PARTIAL / RESIDUAL ASSUMPTION for artifact state | ZIP and verification material have not been published; anonymous exact-version retrieval is untested. |
| Authority / attribution | REQUIRES PUBLISHER AUTHORITY / MANDATE | Account control is authenticated; acceptance of that account as project custodian and its scoped provenance assertion are missing. |
| Custody / provenance | REQUIRES EXPLICIT CONFIGURATION | No custody workflow/package/deposit event exists; eligibility remains NEEDS ADDITIONAL SOURCE CHECK. Historical custody is NOT SUPPORTED by a prospective deposit alone. |

Required for the selected route, in a later separately authorized circuit:

1. Enable immutable releases before publishing the intended immutable release.
2. For the workflow-attestation variant, add a reviewed, pinned custody-only workflow
   and minimum job permissions; validate plan/endpoint eligibility and actual
   publishing credential scope before use. Do not invoke the scientific workflow.
3. Establish publisher mandate and exact prospective provenance/role bindings;
   select a noncolliding tag and designated commit and prepare the unchanged ZIP
   plus independent verification material. These are authority/package actions,
   not settings toggles, and remain unperformed.

Optional, not necessary changes: organization transfer/domain verification,
additional archive/DOI, repository-wide write defaults, PR-approval permission,
new rulesets, or repository-wide action SHA-pinning enforcement. A reviewed future
workflow should pin its own dependencies; global enforcement is separate. No
change to public visibility or Actions enablement is needed. No account upgrade
is currently demonstrated necessary. A second archive is not required in principle
for prospective account-level custody and would not establish earlier history.

## Preservation and final audit outcome

The 40 pre-existing repository file hashes and external ZIP digest are unchanged;
only this receipt may be added. Configuration, releases, tags, rulesets and workflow
inventory are compared with their initial observations before committing. Only GET
requests were used for the audit; no settings, releases, tags, attestations or
workflow dispatches were created/changed. The sole authorized publication is this
receipt's commit/push, not the ZIP or any trust-root object. No tests or experiments
were executed. The audit is complete within read-only access; unresolved eligibility
and authority questions are recorded, not silently repaired.

- **Repository identity:** public `vortexpixelz/ns001`, ID `1354037143`, personal owner.
- **Authenticated publisher identity:** `vortexpixelz`, ID `202687650`; this is the
  current authenticated principal, not a guarantee of a later workflow uploader.
- **Administrative rights:** READY NOW; verified admin role and repository rights.
- **Release capability:** READY NOW at account/repository level; future credential
  write scopes and chosen target must still be appropriate.
- **Immutable-release readiness:** REQUIRES EXPLICIT CONFIGURATION; disabled and
  not owner-enforced. No change made.
- **Actions readiness:** READY NOW; enabled, all actions allowed, default read.
- **Attestation readiness:** REQUIRES EXPLICIT CONFIGURATION; no custody workflow;
  plan/endpoint eligibility NEEDS ADDITIONAL SOURCE CHECK.
- **Anonymous-retrieval readiness:** READY NOW as public-hosting capability; exact
  ZIP/verification-package retrieval remains unestablished.
- **Publisher-authority verdict:** REQUIRES PUBLISHER AUTHORITY / MANDATE; account
  ownership established, scientific/custodial mandate not inferred.
- **Required changes:** immutable-release enablement; custody-only workflow/job
  permissions for the workflow route; mandate and package/version/role bindings.
  Eligibility and credential checks are prerequisites, not assumed settings changes.
- **Optional changes:** organization transfer, second archive/DOI, global write
  defaults, PR approval, new rulesets and global SHA enforcement are not required.
- **GitHub-only prospective route:** conditionally feasible, not operationally ready
  today. Settings/rights are now clearer; authority, workflow and eligibility gaps
  remain. External signature trust roots are still needed for verification.
- **Future publication:** may be considered only after gaps are closed and a separate
  explicit publication instruction; this audit grants no publication permission.
- **H2A1:** local byte identity VERIFIED; external auditability PARTIAL. All eight
  substantive gates remain unresolved: `external_trust_root`, `client_source`,
  `response_contract`, `transport_accounting`, `dependency_runtime_lock`,
  `maximum_partition_memory`, `amendment_freeze`, `final_manifest_package_audit`.
- **E0:** HOLD; no JHTDB request or execution. Gate 1 remains PARTIAL.
- **H2A2:** unstarted.
- **One recommended next bounded H2 action:** a publisher-mandate decision circuit
  explicitly accepting or rejecting `vortexpixelz` as NS-001's prospective custodian,
  with authority scope and historical limitations recorded; no configuration or
  publication in that circuit. Do not begin it here.
