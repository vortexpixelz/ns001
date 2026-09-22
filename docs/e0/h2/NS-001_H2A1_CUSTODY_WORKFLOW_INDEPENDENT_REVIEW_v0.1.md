# NS-001 H2A1 custody workflow independent review v0.1

## Scope and evidence

Branch `codex/e0-h2-preparation`; HEAD before
`736a29190c75ea2afc43c9e6a8feda8ab9d9a8ab`. Review date: 2026-09-22 UTC.
Initial tree clean. Reviewed `.github/workflows/ns001-h1-custody.yml` directly;
SHA-256 `fdbaa3ca10bec3a4f668b43f8f6efaa8e0fb37ea13bb18e2b42ade157d8fb251`
matches the preparation receipt. Independence here means new source inspection
and independently constructed offline probes, not another human or external audit
organization. No workflow, prior receipt or setting was edited.

**Workflow verdict: PARTIAL.** The core execution and byte-identity boundaries are
sound under the stated runtime/service assumptions. Two reproduced evidence-input
validation gaps prevent an unqualified fail-closed verdict. Recommend a narrowly
authorized correction before default-branch placement; no correction is made here.
Placement alone would not run the workflow, but is not approved by this review.

**VERIFIED:** Read-only GitHub observations show public repository `1354037143`,
default branch `main` at `2075dd6cc70e4a922b41c2f9a75107251ac090cf`; custody workflow
absent from that tree. Immutability remains enabled, not owner-enforced. Actions
remains enabled/all allowed/default read; PR approval remains disabled. No releases
or tags exist in the inspected inventories; run count is four with no new custody
run. The H1 digest attestation endpoint returns 404, which is not a comprehensive
absence proof. No attestation creation or dispatch operation was invoked.

**VERIFIED WITH RESIDUAL ASSUMPTION:** The user's separate identity check reports
account `vortexpixelz`, global Git author name `vortexpixelz`, email
`jwalkjcup@proton.me` verified/primary/public, and no local override. This review
accepts that as supplied current configuration evidence, not an independently
repeated email audit. Git author metadata and email verification do not authenticate
workflow predicates or imply corporate authority. No identity setting changed.

## Findings by boundary

| Boundary | Classification | Independent finding |
| --- | --- | --- |
| Trigger | VERIFIED | Only `workflow_dispatch`; no push, pull request, release, schedule, workflow_call or other automatic trigger. Job restricts repository name/ID, actor ID, triggering account, first attempt and acknowledgement input. |
| Permissions | VERIFIED WITH RESIDUAL ASSUMPTION | Top-level `{}`; job only `id-token: write`, `attestations: write`. No contents/package/settings/PR mutation grant or publishing step. Token scope is repository-wide for attestations, not cryptographically limited to this digest; reviewed code supplies that restriction. |
| H1 pinning | VERIFIED WITH RESIDUAL ASSUMPTION | Fixed filename, 51,103 bytes and SHA-256 below; file is read/hash-checked before action. No wildcard, selectable ZIP digest, alternate filename or fallback. Relies on SHA-256, runner integrity and pinned action behavior. |
| Release/asset binding | VERIFIED WITH RESIDUAL ASSUMPTION | Fixed repository; selected tag must match returned tag, immutable true and draft false. Tag resolves through bounded annotation traversal to input full commit. Exactly one matching asset per fixed name; uploaded state and uploader ID required. |
| Provenance interpretation | PARTIAL | Approved provenance digest and typed mandatory identity/scope fields checked, but duplicate JSON keys are accepted (F1). Extra narrative is not semantically certified. |
| Failure behavior | PARTIAL | Eighteen independently constructed failure cases reject; duplicate-key provenance and null publication time are accepted (F1/F2). No false ZIP match demonstrated. |
| Identity separation | VERIFIED WITH RESIDUAL ASSUMPTION | Maintainer ID, uploader ID, workflow SHA/ref and actor are separately represented; action provides actual signer certificate. Predicate fields are workflow claims, not themselves third-party identity/time proofs. |
| Automatic publication | VERIFIED | No release/tag/asset write or upload action exists. Attestation creation is the intended side effect only after a future authorized dispatch. |

**VERIFIED:** H1 filename `NS001_H1_AUDIT_BUNDLE_20260903.zip`, size 51,103,
SHA-256 `a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`;
source commit `6e33cb9ca7019e50e2f247ade9ae8c9a7b40d3ff`. The sole additional
subject is the fixed-name provenance JSON, pinned to the future approved input
digest. Both files enter one attestation; no arbitrary discovered subject is used.

**VERIFIED WITH RESIDUAL ASSUMPTION:** Inputs enter environment variables, not shell
code interpolation. Anonymous downloads send no credentials. Initial download URL
must equal the repository/tag/fixed-filename locator and final URL must use HTTPS.
The redirect chain/final host is not independently allowlisted: transport provenance
relies on GitHub's redirect behavior and TLS. Exact bytes remain hash-protected.
The hosted runner image/Python and service are mutable; this is not a runtime lock.
The attestation action reference is the full commit
`1e69f48acb82d1966a394da916b4c1698aa569d6`, not a floating version tag.

**VERIFIED WITH RESIDUAL ASSUMPTION:** The selected release is not hard-coded now;
future tag, commit and provenance digest inputs must be approved prospectively.
An unrelated release cannot cause different H1 bytes to pass, but matching files
in another approved-input immutable release can pass. No numeric release ID is
precommitted. Pre-release status is not rejected: immutable, non-draft prereleases
are allowed by this code. No prior requirement prohibited that designation.
Uploader must be account ID `202687650`; another bot/account will fail even if
otherwise legitimate. That restriction must not be silently relaxed.

## Reproduced findings requiring correction

### F1 — duplicate JSON keys accepted

**VERIFIED / REQUIRES AUTHORIZED CHANGE:** At workflow lines 78 and 116, ordinary
`json.loads` accepts duplicate object keys. At 126–128 the typed comparison sees
only the last value. A provenance document starting with
`"historical_custody_established": true` followed later by the same key set to
`false` passes when its actual digest is supplied. The exact ZIP guard still holds;
this requires a separately approved provenance digest and is not an arbitrary-byte
or unauthenticated bypass. Nevertheless, ambiguous/conflicting provenance can
reach signing, contrary to an unqualified fail-closed ambiguity claim.

Correction scope: reject duplicate keys when decoding provenance and API JSON,
including nested objects, and reject nonstandard JSON numeric constants; test
conflicting duplicates and valid unambiguous input. The current receipt does not
repair or reinterpret the existing bytes.

### F2 — required custody timestamps lack validation

**VERIFIED / REQUIRES AUTHORIZED CHANGE:** Line 134 copies `release['published_at']`
into the predicate without checking type/non-null/time syntax. A simulated immutable,
non-draft release with `published_at: null` passes all guard checks and produces a
predicate. Line 135 similarly copies asset creation time without validation.
A missing key would raise and stop; a present null does not. This is a malformed
service-evidence probe, not evidence that GitHub currently returns such a release.
It demonstrates reliance on API schema promises instead of locally failing closed
when required publication-custody time evidence is absent.

Correction scope: require usable timezone-bearing publication/asset timestamps
before predicate generation, retaining their service-reported status rather than
claiming cryptographically verified time. Add null/malformed timestamp rejection
checks. Do not substitute the runner clock for missing service evidence.

## Failure tests and remaining interpretation limits

**VERIFIED:** Twenty-one cases executed the unchanged extracted guard with mocked
network responses and temporary filesystem output. One valid fixture passed.
Eighteen cases rejected: missing release, missing asset, wrong ZIP bytes, wrong
uploader, provenance digest mismatch, incorrect scope, wrong field type, mutable
release, draft release, duplicate named asset, wrong size, non-uploaded asset state,
wrong tag, wrong locator, invalid commit input, wrong resolved commit, invalid tag
object type and network error. Two further probes reproduced F1/F2 acceptance.
No attestation action or GitHub workflow ran; the signed-action step is not covered
by these offline tests. The real retained ZIP was only read locally as fixture
bytes; it was not uploaded or extracted.

**VERIFIED WITH RESIDUAL ASSUMPTION:** Shell error handling and default step-success
conditions prevent signing after a failed guard. A job-level identity/acknowledgement
mismatch skips the job rather than asserting a failed custody check; a skipped or
successful workflow badge alone must never be taken as evidence of attestation.
The acknowledgement is not external authorization. Run-attempt restriction blocks
reruns of a run; separate manual dispatches can still create repeated attestations.
Concurrency is serialization, not a one-lifetime counter. A future authorized
operator must check the one-attestation mandate before dispatch. These were already
disclosed in preparation and are not silently strengthened by this review.

**VERIFIED WITH RESIDUAL ASSUMPTION:** The custom predicate correctly says
verification of existing published bytes, not a historical build. It does not equate
the uploader with the workflow signer or assert corporate/historical authority.
Runner observation time and release API timestamps are claims/observations. Actual
certificate and verified witness timestamps require independent attestation
verification. The final step reports a bundle location/digest, not a permanent
anonymous archive; durable verification-material retrieval remains later work.
[GitHub verification semantics](https://cli.github.com/manual/gh_attestation_verify).

## Default-branch placement plan, not executed

**VERIFIED:** GitHub documents that `workflow_dispatch` receives events only when
the workflow file exists on the default branch. Current remote default branch is
`main`, and its tree lacks this file. Merely storing it on the preparation branch
does not complete that prerequisite.
[Workflow dispatch documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onworkflow_dispatch).

**REQUIRES AUTHORIZED CHANGE:** After F1/F2 are corrected and independently reviewed,
the minimal placement operation is one new commit based on freshly verified remote
`main`, adding **only** `.github/workflows/ns001-h1-custody.yml` with the approved
reviewed bytes, then an explicitly authorized update of `main` to include that
commit (through a one-file PR if required). Copy from the pinned reviewed commit;
verify the file digest and a one-path diff before updating main. Recheck the base
and abort on unexpected drift; do not rewrite main. Do not merge this entire
preparation branch or cherry-pick a multi-file preparation commit as a substitute
for the one-file operation. Receipts can remain referenced at their pinned branch
commits; the workflow requires no checkout or local helper file on main.

Current workflow bytes at `736a29190c75ea2afc43c9e6a8feda8ab9d9a8ab` are the
reviewed baseline, not an approved post-fix version. The source commit/digest for
placement must be selected only after authorized remediation/review. No new branch,
PR, cherry-pick, merge or main update was performed here.

**VERIFIED:** Remote main's existing `ns001-sanity.yml` matches the local file. Its
push path filters include that specific old workflow path and scientific files,
not this new workflow path. A one-file custody placement would not match those
observed scientific push filters; the custody workflow itself is manual-only.
Recheck triggers at placement time. Placement still creates a dispatchable capability
and needs its own authorization, even though it does not itself authorize a run.

## Preservation and final decisions

Only this review receipt is added. All 45 pre-existing non-Git repository hashes,
including the workflow and prior receipts, and the retained ZIP identity are checked
unchanged before commit. Settings, default main SHA, release/tag/run/workflow
inventories and the attestation-query result are reread for preservation. Review
network calls were GET only. No settings, identity settings, workflow execution,
release, tag, asset or attestation creation occurred. The requested receipt
commit/push is the sole repository change.

- **Workflow verdict:** PARTIAL; retain as prepared baseline, correct F1/F2 before
  approving default-branch placement or later execution.
- **Trigger verdict:** VERIFIED manual-only and constrained; not an authorization oracle.
- **Permissions verdict:** VERIFIED WITH RESIDUAL ASSUMPTION; minimal signing grants,
  no release/tag/asset mutation grant; runner/action trust still required.
- **Artifact-pinning verdict:** VERIFIED WITH RESIDUAL ASSUMPTION; exact H1 bytes,
  size and filename enforced; provenance is a separately digest-pinned second subject.
- **Release-binding verdict:** VERIFIED WITH RESIDUAL ASSUMPTION for tag/commit/assets;
  required timestamp completeness PARTIAL under F2.
- **Provenance/identity verdict:** PARTIAL under F1; identities otherwise separated,
  no historical/corporate claim promoted; signed evidence remains uncreated.
- **Failure-behavior verdict:** PARTIAL; 18 expected failures rejected, two additional
  malformed/ambiguous evidence cases accepted.
- **Default-branch requirement:** workflow must exist on default main for dispatch.
- **Exact minimal placement plan:** after authorized fixes/review, one file-only
  commit from current remote main, then separately authorized integration into main;
  preserve digest, recheck triggers, never dispatch as part of placement.
- **Preparation remains valid:** YES as preserved non-executed preparatory state;
  NO as an unqualified placement/execution-ready approval. Immutability stays enabled.
- **H2A1:** local identity VERIFIED; external auditability PARTIAL; all eight
  substantive H2 gates remain unresolved.
- **E0:** HOLD; no execution/JHTDB request. Gate 1 remains PARTIAL.
- **H2A2:** unstarted.
- **One recommended next bounded action:** separately authorize correction and offline
  verification of F1/F2 only on the preparation branch, with no main placement,
  settings changes, publication or attestation execution. Not begun here.
