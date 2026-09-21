# NS-001 H2A1 GitHub trust-root feasibility v0.1

## Review boundary and preserved object

Branch `codex/e0-h2-preparation`; HEAD before review
`b2dc54d7df2ce841d032188bdb8f241b2dd11167`; initial working tree clean.
Review date: 2026-09-21 UTC. Governing criteria are the unchanged
`NS-001_H2A1_EXTERNAL_AUTHORITY_CUSTODY_SPEC_v0.1.md`, not a newly weakened standard.
This is documentation/configuration feasibility, not implementation or publication.

Direct local read confirmed `NS001_H1_AUDIT_BUNDLE_20260903.zip`, at
`/home/jacob/Documents/NS-001/audit/2026-09-03/NS001_H1_AUDIT_BUNDLE_20260903.zip`,
**51,103 bytes**, SHA-256
`a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`.
No extraction, execution, upload or regeneration was performed.

**Finding:** GitHub mechanisms can support a prospective account/workflow-level
custody route. Current configuration is not demonstrated sufficient; publisher
mandate, settings and complete custody bindings remain unresolved. No present
four-property PASS is warranted. Documentation describes capability, not deployed
evidence. Historical custody cannot be manufactured by a new attestation.

## Current repository-visible evidence

Read-only, anonymous HTTPS GETs against `https://api.github.com/repos/vortexpixelz/ns001`
returned the following. No credentials were used for these inspections; no write
API, workflow dispatch, setting change or attestation command was invoked.

| Endpoint / local evidence | Observation | Requirement classification and limit |
| --- | --- | --- |
| Repository metadata | HTTP 200; ID `1354037143`; public; not archived; default branch `main`; owner `vortexpixelz`, ID `202687650`, type `User` | SATISFIABLE WITH CURRENT CONFIGURATION for public repository access and platform account mapping only. This is not an organization identity or scientific mandate. |
| `/releases?per_page=100` | HTTP 200; zero releases | PARTIAL / RESIDUAL ASSUMPTION: public release facility is plausible; no ZIP asset or actual immutable release exists to verify. Publisher release-write permission not established. |
| `/actions/workflows` | HTTP 200; active `NS-001 reproducibility`, ID `347905226`; active dynamic Dependency Graph, ID `347908986` | PARTIAL / RESIDUAL ASSUMPTION: registered active workflows are visible, not proof of all required execution permissions or attestation readiness. |
| `/actions/permissions` | HTTP 401, requires authentication | NEEDS ADDITIONAL SOURCE CHECK: enabled/allowed-actions policy and effective restrictions unknown. |
| `/immutable-releases` | HTTP 401, requires authentication | NEEDS ADDITIONAL SOURCE CHECK: enabled/enforced status unknown, not “disabled.” Docs require admin read access. |
| `/attestations/sha256:a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f` | HTTP 404 | NEEDS ADDITIONAL SOURCE CHECK: no attestation obtained. Anonymous failure does not prove authenticated inventory empty. |
| `.github/workflows/ns001-sanity.yml` at reviewed HEAD | No attestation action or custody-only job; existing job invokes scientific protocols. Receipt path is outside its push path filters. | SATISFIABLE AFTER EXPLICIT CONFIGURATION for a separate reviewed custody-only workflow; existing workflow must not be run or repurposed implicitly. |

The API endpoint and permission semantics are documented in
[repository settings API](https://docs.github.com/en/rest/repos/repos#check-if-immutable-releases-are-enabled-for-a-repository)
and [attestations API](https://docs.github.com/en/rest/repos/attestations).
The 401/404 results remain evidence limits; they were not bypassed with credentials.
Account plan, release administration rights, workflow-token policy, Actions allowed
list, and any governing restrictions were not visible in these anonymous results.

## Mechanism review against the four fixed criteria

### 1. Byte identity

**SATISFIABLE AFTER EXPLICIT CONFIGURATION** for the complete authenticated binding;
ordinary local digest computation already works. An immutable release generates a
release attestation connecting tag, commit and assets. A workflow artifact
attestation can instead name actual file bytes through `subject-path`; a supplied
`subject-digest` merely signs the supplied identity unless independently checked.
The future workflow must read the retained ZIP and refuse any size/digest mismatch.
An independent reviewer must download and hash it, not trust a filename or badge.
[Immutable releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases),
[attestation generation](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations).

GitHub documents `gh release verify` and `gh release verify-asset` for release and
asset verification. Its generated source ZIP/tarball is excluded from that asset
verification and is not a substitute for the retained H1 ZIP. No verification
command was executed here because no release exists.
[Release integrity verification](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/verify-release-integrity).

### 2. Retrievability

**SATISFIABLE WITH CURRENT CONFIGURATION** for anonymous public hosting eligibility,
not a claim that this unpublished ZIP is currently retrievable. The asset API
supports unauthenticated public-resource downloads by asset ID and browser download
URL, with direct responses or redirects. A specific release tag/asset ID plus exact
digest gives a repeatable reference; a latest-release link or transient redirect
URL alone does not. Asset API metadata includes size, digest, uploader identity and
creation/update time. Those are service observations, not a complete signed chain.
[Release asset API](https://docs.github.com/en/rest/releases/assets).

Publication, retained anonymous retrieval evidence and continued availability are
still required. Repository visibility/retention and service access remain
assumptions. An attestation API or CLI path requiring authentication does not meet
the prior specification's anonymous evidence-package criterion by itself: a later
package would need anonymously downloadable verification bundles and independently
obtained trusted roots. Offline verification is documented, including root-rotation
and stale-root limitations.
[Offline verification](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/verify-attestations-offline).

### 3. Authority / attribution

**PARTIAL / RESIDUAL ASSUMPTION.** GitHub authenticates accounts and workflow context;
public metadata establishes this repository's current account-owner mapping.
It does not establish that this account is an independently approved scientific
custodian or that a typed author identity is a legal person. The actual owner is
a personal account, not an organization. Organization domain verification, where
applicable, demonstrates domain control, not endorsement of an experiment or ZIP.
[Organization domain verification](https://docs.github.com/en/organizations/managing-organization-settings/verifying-or-approving-a-domain-for-your-organization).

OIDC documents repository, actor and actor-ID context, but token claims must not
be assumed all preserved in an attestation certificate. Workflow initiator, signing
workflow and release-asset uploader can be different identities. Their relationship
must be explicitly evidenced for the selected route.
[OIDC reference](https://docs.github.com/en/actions/reference/security/oidc).

Before publication, the project must explicitly identify its authorized publisher
and accept the scope of account/workflow-level authority. Preserve that mandate
with identity authentication outside the ZIP's own claims; retain stable repository
and account IDs. A repository file declaring its own authority is insufficient.
This is a governance prerequisite already present in the prior specification, not
a claim that GitHub verifies project scientific authority.

### 4. Custody / provenance

**PARTIAL / RESIDUAL ASSUMPTION**, technically satisfiable prospectively after an
explicitly reviewed configuration and identity decision. Distinguish:

- A **release attestation** is GitHub-generated release/asset binding; it does not
  by itself authenticate every assertion in an accompanying historical narrative.
- An **artifact attestation** authenticates a workflow's signed claim about a digest.
  Its certificate identity and verified log/timestamp-authority times are externally
  supplied. Predicate content can be workflow-controlled; signing it authenticates
  the assertion's origin, not its truth. Verification must constrain repository,
  signer workflow/source digest, issuer and predicate type, not simply accept any
  valid signature. [CLI verification semantics](https://cli.github.com/manual/gh_attestation_verify).
- **Publisher/transfer assertions** must bind the actual retained bytes and separate
  workflow, initiator and uploader roles. Release API uploader/time observations
  assist correspondence, but do not establish that all these roles are identical.

Public-repository artifact attestations use Sigstore's public infrastructure and a
public transparency log. Trust extends beyond local repository prose to GitHub
OIDC, certificate/signature verification and witnessed signing times. A timestamp
shows when the signature was witnessed, not the ZIP's original creation time or
necessarily its release-publication time.
[Artifact attestation trust model](https://docs.github.com/en/actions/concepts/security/artifact-attestations).

A custom predicate can describe an import/verification/deposit of existing bytes;
using default build-provenance language to imply the historical ZIP was built by a
new workflow would be misleading. The official action supports custom predicates
and emits a verification bundle. A reviewed future statement must link ZIP and
provenance digests, account roles, release/asset identity and service observations;
its historical portions must remain explicitly self-asserted.
[Official attest action](https://github.com/actions/attest).

A prospective record can therefore establish that a specified authenticated
workflow/account asserted and deposited these bytes, subject to the accepted
identity policy and independent download check. It cannot prove September 3
creation, continuous earlier custody, truth of historical test claims, or runtime
provenance. Full field-level binding must be checked on actual future evidence;
no object exists to do that now. Historical custody is **NOT SATISFIABLE BY THIS
ROUTE** through a new deposit alone. Separate contemporaneous evidence could
address some historical facts; their permanent unknowability is not asserted.

## Immutability and configuration requirements

**NEEDS ADDITIONAL SOURCE CHECK** for current immutable-release configuration.
When enabled, documented protection locks release assets and associated tag; tag
movement and individual asset modification/deletion are prevented. Title, notes,
pre-release/latest designations remain mutable. The release itself can be deleted;
after deletion the tag can be deleted, but its name cannot be reused. Repository
resurrection protections do not guarantee perpetual download availability.
[Immutable-release guarantees](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases).

Enabling immutability requires explicit repository/owner configuration; no setting
was read successfully here and none changed. Release management requires write
access; enabling the repository setting requires administrative authority. Actual
rights must be confirmed, not inferred from an earlier branch push.
[Enabling immutability](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/prevent-release-changes),
[release management](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).

Artifact attestations are documented for public repositories on current plans;
legacy plans are excluded. A generating workflow needs `id-token: write`,
`attestations: write`, and appropriate content access. Artifact signing and
release publication permissions are separate. No attestation workflow is present
in the reviewed local configuration, and a listed active workflow does not prove
these prerequisites. The automatic immutable-release attestation is distinct from
a custom Actions custody attestation; do not assume one requires or supplies all
of the other's evidence. [Generation prerequisites](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations).

Required before any later publication:

1. Read-only authenticated/admin-visible confirmation of immutable-release status,
   owner enforcement, release publishing rights and relevant tag restrictions.
2. Confirmation of plan eligibility, Actions policy/allowed actions, effective job
   permissions and eligible runner context. No settings are inferred from 401.
3. Accepted publisher identity/mandate and permitted account/workflow/uploader roles;
   stable IDs, verification issuer, signer and predicate acceptance policy.
4. Separately reviewed custody-only workflow or equivalent deposit mechanism that
   reads the exact ZIP, checks its digest, preserves it, binds provenance honestly,
   and never invokes current scientific workflows or JHTDB. Any action dependencies
   and workflow identity must be pinned/reviewed before relying on their claims.
5. An explicit immutable release version/commit/asset binding, provenance statement,
   preserved verification bundle and anonymous retrieval instructions, followed by
   independent verification of actual publication evidence. These do not exist yet.
6. Retention/deletion policy and independently sourced verification roots. Mutable
   release notes alone cannot carry the required durable provenance statement.

## Preservation and closing verdicts

The 39 pre-existing non-Git repository file hashes and retained ZIP digest are
checked unchanged before commit. Only this receipt is added. All remote review
calls were GETs; no release, ZIP upload, attestation, setting mutation or workflow
dispatch occurred. The permitted external write is solely this receipt's branch
commit/push. No test suite or experiment was run. Hidden settings cannot be
certified globally unchanged against third-party activity; this review made no
setting writes. Public metadata/release/workflow observations are rechecked before
commit for visible discrepancies.

- **Byte identity:** SATISFIABLE AFTER EXPLICIT CONFIGURATION for authenticated
  release/attestation binding; exact local identity remains VERIFIED.
- **Retrievability:** SATISFIABLE WITH CURRENT CONFIGURATION for public hosting
  eligibility; actual ZIP and verification-package retrieval remain unestablished.
- **Authority:** PARTIAL / RESIDUAL ASSUMPTION; platform account mapping is known,
  accepted project mandate and complete role binding are not.
- **Custody:** PARTIAL / RESIDUAL ASSUMPTION; prospective custody is technically
  feasible after explicit configuration, evidence generation and verification.
- **Immutability:** NEEDS ADDITIONAL SOURCE CHECK; current setting is inaccessible
  anonymously. Documented assets/tag protection is not permanent retention.
- **Exact missing prerequisites:** the six items above, particularly admin-visible
  settings, publisher rights/mandate, Actions permissions/plan, custody-only signing
  workflow, exact publication bindings and anonymous verification evidence.
- **Claims GitHub cannot establish:** scientific approval, human/legal identity from
  an account name alone, truth of user predicates, earlier custody/creation, past
  test execution, loaded runtime provenance, permanent hosting, or E0 permission.
- **Historical custody:** unresolved; inherently not established by a new GitHub
  publication/attestation alone. Only additional historical evidence could change it.
- **GitHub alone:** not sufficient on current evidence. Conditionally capable as
  the hosting/account/workflow route for all four *prospective* criteria if project
  authority is explicitly accepted and external signature/time roots are validated.
  Literal GitHub-only trust omits Sigstore roots and the required authority choice.
- **Second external archival authority:** not inherently required by the fixed
  account-level prospective criteria. It may improve retention, but a second copy
  does not cure authority or historical custody. Independent institutional endorsement
  would require additional evidence if that stronger authority scope is chosen.
- **H2A1:** local identity VERIFIED; independent external auditability PARTIAL. All
  eight substantive gates remain unresolved: `external_trust_root`, `client_source`,
  `response_contract`, `transport_accounting`, `dependency_runtime_lock`,
  `maximum_partition_memory`, `amendment_freeze`, `final_manifest_package_audit`.
- **E0:** HOLD; no execution or JHTDB request. Gate 1 remains PARTIAL.
- **H2A2:** unstarted.
- **One recommended next bounded H2 action:** an authorized read-only administrator
  configuration audit of immutable-release status, release rights and Actions/
  attestation policy, retaining evidence of the presently inaccessible prerequisites.
  Do not change settings, publish, create attestations or begin that audit here.
