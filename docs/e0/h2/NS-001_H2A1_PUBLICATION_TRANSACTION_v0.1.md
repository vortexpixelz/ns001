# NS-001 H2A1 publication transaction v0.1 — preflight STOP

## Frozen before publication

Preparation branch `codex/e0-h2-preparation`, HEAD
`50665ce64ebe1246a38e0aa9df35b8ae5b9c5847`; starting working tree clean.
Origin fetched; observed remote main `ef71e56263da8e4d0dfcd5228795356e38b27998`.
Planned tag `ns001-h1-audit-v1`; frozen target
`ef71e56263da8e4d0dfcd5228795356e38b27998`.
Frozen ZIP: `NS001_H1_AUDIT_BUNDLE_20260903.zip`, 51,103 bytes,
SHA-256 `a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`.
Frozen provenance: `NS001_H1_PUBLICATION_PROVENANCE.json`, 2,298 bytes,
SHA-256 `9f67d54f2852c386384b9ea1bd1c231bcbb572490bd8b94b9ce84396a7fbac89`.
These are frozen inputs, not observations of published objects.

## Blocking authorization inconsistency

The current instruction requires honoring the frozen receipts but also excludes
“publication of any other artifact” while explicitly authorizing only the ZIP upload.
The prepublication review specifies two uploaded assets, and the final readiness
recheck requires both exact ZIP and provenance asset staged before finalization.
The unchanged workflow downloads the provenance asset at line 134 and attests both
files. Publishing only the ZIP cannot satisfy that workflow; adding the required
second asset would exceed the latest explicit exclusion without clarification.

Phase 3 also proposes adding future observed fields to runtime provenance after
publication. The frozen prepublication review expressly says observations are not
inserted later into the frozen JSON. Its exact digest is a required dispatch input.
The workflow itself constructs the observed custody predicate; post-event observations
belong in that predicate and the evidence deposit, not a replacement provenance asset.
The existing receipts are mutually consistent on these points; the conflict is between
the latest execution wording and that frozen plan. No silent reinterpretation occurs.

Required resolution: explicitly authorize upload of the exact frozen provenance JSON
alongside the ZIP while the release is draft, finalize only after verifying both,
and preserve its digest unchanged. Keep observed IDs/timestamps/uploader in separate
post-event evidence and the workflow-generated predicate. No new authorization is
inferred by this receipt. STOP before creating any external publication object.

## Observed during this attempted preflight

No publication transaction attempted. Remote releases and tags remain empty, and
run inventory contains the same four pre-existing runs. No dispatch or mutation call
was made. Main matches the frozen target. No release/asset/run/signature IDs or
publication times exist to record. Remaining byte/tool/space preflight checks were
not repeated after the authorization conflict was identified; do not label the full
preflight passed. No NS-001 attestation lookup or creation was performed.

## Derived / verified after publication

Not applicable: no publication occurred. No external asset hashing, attestation
verification, negative verification or evidence-deposit creation was attempted.
Only this local STOP receipt is added. It remains uncommitted/unpushed because the
current execution instruction bounds commits/pushes to the post-event evidence
deposit, which cannot be created in this stopped preflight. Existing files unchanged.

## Closing state

- Preflight verdict: BLOCKED by authorization/provenance inconsistency.
- Tag created: NO.
- Release created: NO.
- Immutable-release verdict: not rechecked in this stopped preflight.
- Published target commit: none; intended target as above.
- Release ID / locator: none.
- Asset ID / locator: none.
- Published ZIP size / SHA-256: not applicable; frozen input values above only.
- Independent download/hash verdict: NOT RUN.
- Actual uploader: none observed.
- Release publication timestamp / asset creation timestamp: none.
- Final provenance SHA-256: no post-event provenance created; frozen input digest
  `9f67d54f2852c386384b9ea1bd1c231bcbb572490bd8b94b9ce84396a7fbac89` unchanged.
- Custody workflow run ID: none.
- Custody workflow conclusion: NOT DISPATCHED.
- Attestation created: NO.
- Attestation bundle SHA-256: none.
- Trusted-root preservation verdict: no transaction material created.
- Offline attestation verification verdict: NOT RUN.
- Negative verification verdict: NOT RUN.
- Evidence-deposit path / commit: none.
- External retrieval verdict: no publication objects to retrieve.
- Historical limitations preserved: YES.
- H2A1 final status: external auditability PARTIAL; no promotion.
- E0: HOLD; Gate 1 unchanged/PARTIAL.
- H2A2: UNSTARTED.
- Exact next bounded action: explicitly resolve the two-asset authorization and
  unchanged-provenance boundary before resuming preflight; do not publish yet.


## Resumed circuit after explicit boundary clarification

Recorded 2026-09-24T16:37:07.018196+00:00.
The earlier sections above are preserved verbatim as the initial STOP history.
The user explicitly resolved BOTH original conflicts: exactly two frozen release
assets (ZIP and provenance JSON) are authorized, and the frozen provenance bytes
must remain unchanged; service observations belong in the generated predicate,
transaction receipt and post-event evidence. Those conflicts are CLOSED. This
section records a distinct subsequent preflight STOP and supersedes the initial
closing state for current status. No external mutation occurred between attempts.

### Fresh checks after clarification

Origin fetched again. Preparation HEAD remains
`50665ce64ebe1246a38e0aa9df35b8ae5b9c5847`; current main remains
`ef71e56263da8e4d0dfcd5228795356e38b27998`. Tracked tree is clean; the sole expected
untracked file is this STOP receipt, whose bytes were preserved before appending.
Frozen target exists locally/remotely and its remotely retrieved custody workflow
matches SHA-256 `236b8f30a27fa1c3c26f134c794f2e3e989b9b31d1e3adfbcfae18e21fa420bf`.
The manual custody trigger, minimal permissions, duplicate-key rejection, timestamp
validation and H1 pinning remain unchanged. Original mandate/adoption/evidence-plan
bytes match their pinned commits. Active authenticated account is vortexpixelz,
ID 202687650, with repository push permission.

ZIP freshly rehashed at exactly 51,103 bytes with the frozen digest. Exact 2,298-byte
provenance was extracted from the frozen receipt and matches
`9f67d54f2852c386384b9ea1bd1c231bcbb572490bd8b94b9ce84396a7fbac89`.
No regeneration or insertion of future values. Frozen release body recovered from
its authority_text as prescribed. Temporary copies and a read-only preflight snapshot
are retained under `/tmp/ns001-publication-transaction`; these are transaction staging,
not a committed or externally published evidence deposit. Original files unchanged.

Pinned gh 2.101.0 binary digest matches its validated receipt; required commands
are available. Repository filesystem reports approximately 47.36 GB free and both
repository/temp space exceeded the 100 MiB preflight floor. Local and remote tag are
absent; releases/tags empty; four old runs only. Owner H1 attestation lookup returned
404, a bounded absence observation. Immutability enabled. These individual checks
passed, but the complete preflight does NOT pass because of the trigger below.

### New blocking condition: unintended live workflow on tag push

`.github/workflows/ns001-sanity.yml` at the frozen target is active on GitHub
(workflow ID `347905226`). Its `on.push` uses path filters with no branches/tags
filter. The job has no tag-skipping condition and includes live public-token
sanity and temporal-smoke protocol Docker runs. No such run was executed here.

[GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onpushbranchestagsbranches-ignoretags-ignore)
specifies that an unspecified branch/tag filter accepts both ref types.
[Path-filter semantics](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onpushpull_requestpull_request_targetpathspaths-ignore)
states that path filtering is not evaluated for tag pushes. Thus the existing
path filters cannot protect this transaction from an automatic scientific job
when the publication tag is pushed. Treat tag creation as unsafe for this bounded
transaction unless suppression is independently established and authorized.
This is not proof an E0 run occurred; none did. It is an unauthorized live-workflow
risk outside the single approved custody dispatch.

The prior readiness conclusion missed the tag-specific trigger semantics; that
conclusion cannot be relied upon for execution. The custody workflow itself is
unchanged and remains manual-only. No workflow/settings change or alternate tag
creation mechanism was attempted as a workaround. A recovery plan must account for
the workflow at the frozen target, not merely assume that editing current main
changes tag-trigger behavior. Current authorization prohibits workflow/settings
changes, so remediation requires a separate bounded instruction.

### Current closing state after resumed preflight

- Preflight verdict: BLOCKED by active scientific workflow's unfiltered tag push.
- Original authorization conflicts: RESOLVED by explicit user clarification.
- Publication transaction attempted: NO; no external mutation.
- Tag created: NO; intended `ns001-h1-audit-v1` remains absent.
- Release created: NO.
- Immutable-release verdict: enabled; no release exists to assess.
- Published target commit: none; intended `ef71e56263da8e4d0dfcd5228795356e38b27998`.
- Release ID / locator: none.
- Asset ID / locator: none.
- Published ZIP size / digest: not applicable; source identity freshly verified
  as 51,103 bytes / `a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`.
- Independent published download/hash verdict: NOT RUN, nothing published.
- Actual uploader: none; authenticated preflight account is not an observed uploader.
- Publication / asset creation timestamps: none.
- Final provenance SHA-256: no post-event object; frozen input unchanged at
  `9f67d54f2852c386384b9ea1bd1c231bcbb572490bd8b94b9ce84396a7fbac89`.
- Custody workflow run ID: none; conclusion NOT DISPATCHED.
- Attestation created: NO; bundle digest none.
- Trusted-root preservation: no transaction evidence created; installed toolchain unchanged.
- Offline / negative NS-001 attestation verification: NOT RUN.
- Evidence-deposit path / commit: none.
- External retrieval verdict: target/workflow read back; no published asset exists.
- Historical limitations preserved: YES.
- H2A1 final status: external auditability PARTIAL; execution readiness BLOCKED.
- E0: HOLD; Gate 1 PARTIAL unchanged.
- H2A2: UNSTARTED.
- Commit / push: none; same local receipt updated with both STOP events.
- Exact next bounded action: separately authorize a bounded mitigation plan for the
  active sanity workflow's tag-trigger behavior at the frozen publication target;
  do not create the tag or change workflows/settings in this stopped circuit.


## Exact re-frozen authorized publication attempt

### FROZEN BEFORE PUBLICATION

User explicitly authorized this exact publication circuit. Prior STOP sections above remain byte-preserved history.
Preparation HEAD `4b290f40def4135e4f2d6850baa3309580b4d623`; frozen target `d9dcfbef1bea173b316bc968fd71421c982422c3`.
Fresh preflight PASS at 2026-09-24T19:17:50.492035+00:00.
Tag `ns001-h1-audit-v1`; title `NS-001 H1 mock-only audit bundle v1`.
Exactly two frozen assets: ZIP (51103 bytes, SHA-256 a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f) and
`NS001_H1_PUBLICATION_PROVENANCE.json` (2298 bytes, SHA-256 ff649229275d88be762e2b762b35b27c3aac8e252a070ac39b18bffc06142d12).
Release body is the re-freeze JSON authority_text plus LF, unchanged.
Custody workflow digest `236b8f30a27fa1c3c26f134c794f2e3e989b9b31d1e3adfbcfae18e21fa420bf`.
Main, account/repository identities, immutability, unused tag, absent releases,
unchanged runs, exact tag-trigger exclusion, artifact bytes and pinned verifier pass.
Digest-specific attestation lookups returned 404, a bounded negative observation.
No frozen provenance fields will be modified with event observations.

### OBSERVED DURING PUBLICATION

Event records follow; publication mutations are single attempts, with STOP on any failure.

- 2026-09-24T19:18:38.840847+00:00 immediate-main-check: exit 0.

- 2026-09-24T19:18:39.603970+00:00 tag-created: exit 0.

- 2026-09-24T19:18:40.347074+00:00 draft-created: exit 0.

- 2026-09-24T19:18:40.709694+00:00 upload-NS001_H1_AUDIT_BUNDLE_20260903.zip: exit 1.

**STOP AND PRESERVE STATE:** AssertionError(('upload-NS001_H1_AUDIT_BUNDLE_20260903.zip', 'error connecting to api.uploads.github.com\ncheck your internet connection or https://githubstatus.com\n'))
No retry, deletion, replacement or dispatch authorized by this failure.

### OBSERVED DURING PUBLICATION — stopped state

- Tag creation succeeded: `ns001-h1-audit-v1` -> `d9dcfbef1bea173b316bc968fd71421c982422c3`.
- Draft release creation succeeded: ID `396003416`, tag_name `ns001-h1-audit-v1`,
  title `NS-001 H1 mock-only audit bundle v1`, exact frozen body.
- Observed draft locator: https://github.com/vortexpixelz/ns001/releases/tag/untagged-f16adb2dc90288a63b0c
  (not a publicly retrievable finalized release).
- Actual release author: `vortexpixelz`, ID `202687650`.
- GitHub reports release created_at `2026-09-24T17:00:40Z`; published_at is null.
  This is the API field as observed, not an inferred upload time or historical-custody claim.
- First upload failed before an asset was created. The command incorrectly used
  `gh api --hostname uploads.github.com`, which attempted `api.uploads.github.com`.
  Exact error: `error connecting to api.uploads.github.com`.
- This is an operator command construction error. It is not evidence of an outage
  at the actual upload endpoint. No automatic correction or retry was attempted.
- Readback: draft=true, immutable=false, assets=[]; no asset IDs, uploaders or upload timestamps exist.
- Finalization, download/hash verification, dispatch and signing were NOT ATTEMPTED.

### VERIFIED AFTER PUBLICATION — no finalized publication

Read-only post-failure verification confirms the exact tag target and draft state,
zero assets, main unchanged, immutable-release setting still enabled, and the same
four pre-existing workflow run IDs. No scientific or custody run was created.
There is no published-asset digest, custody attestation bundle, positive offline
verification or bounded negative verification result for this attempt.
The frozen ZIP/provenance hashes are input identities, not published hashes.

Failure evidence is preserved in
`docs/e0/h2/evidence/ns001-h1-audit-v1-publication-stop-20260924/` with exact
response/error bytes, attempted command, manifest and interpretation. This is a
partial failure-evidence deposit; it does not fulfill the completed custody-deposit
requirements. The repository commit containing it provides the immutable Git object
identifier; external retrieval of those bytes is verified after push. The historical
STOP prefix remains byte-identical. All pre-existing tracked artifacts remain unchanged.

### Current closing state — STOP AND PRESERVE STATE

- Preflight: PASS; publication attempted: YES; finalized publication: NO.
- Existing tag and draft release are preserved. No delete/recreate/replace/retry.
- Two asset IDs/locators: none; two published hashes: unavailable.
- Independent download: NOT RUN; actual uploader: none.
- Workflow run ID/result: none / NOT DISPATCHED.
- Attestation bundle digest: none; offline and negative verification: NOT RUN.
- Public release/asset retrieval: unavailable; draft remains unpublished.
- H2A1 final status: local byte identity VERIFIED; external auditability PARTIAL.
- E0 HOLD; H2A2 UNSTARTED; Gate 1 remains PARTIAL and unchanged.
- One next bounded action: request explicit authorization to correct the upload
  invocation and resume against the existing draft/tag after fresh state checks;
  do not recreate objects or dispatch as an automatic recovery.


## Corrected asset-upload circuit — verified draft only

### FROZEN BEFORE THIS CIRCUIT

Preparation HEAD `3ea97cab94cd2a0e99ee98ca5e49425f2d657135`.
The user explicitly authorized ONE corrected upload circuit against existing draft
`396003416`, with exactly the existing frozen ZIP and provenance JSON. Publication,
workflow dispatch, attestation creation, new tags/releases and clobbering are excluded.
All preceding STOP events and the failed invocation remain preserved verbatim.

Fresh origin fetch and read-only preflight PASS. Tag `ns001-h1-audit-v1` resolves to
`d9dcfbef1bea173b316bc968fd71421c982422c3`; main unchanged. Direct release read and
pinned CLI tag resolution identify the same draft ID, correct target/body, unpublished
state and zero assets. Frozen ZIP is 51103 bytes / SHA-256
`a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`.
Frozen provenance is extracted byte-for-byte from the re-freeze JSON block, 2298 bytes /
SHA-256 `ff649229275d88be762e2b762b35b27c3aac8e252a070ac39b18bffc06142d12`.
Neither asset was regenerated or altered. No observed fields were inserted into provenance.
Pinned gh 2.101.0 binary hash matches; current account vortexpixelz / 202687650.
Same four prior run IDs; both digest-specific attestation lookups returned HTTP 404
(bounded negative observation, not universal absence proof).

### OBSERVED DURING CORRECTED UPLOAD

Actual release upload_url:
`https://uploads.github.com/repos/vortexpixelz/ns001/releases/396003416/assets{?name,label}`.
Host verified exactly `uploads.github.com`. The [official existing-release CLI command](https://cli.github.com/manual/gh_release_upload)
was used once per file, using `/home/jacob/.local/opt/ns001-gh/2.101.0/gh`:
`release upload ns001-h1-audit-v1 FILE --repo vortexpixelz/ns001`, without `--clobber`.
Each succeeded and was followed by direct readback of release ID 396003416 before proceeding.

| Asset ID | Name | Size | State | Service digest | Uploader / ID | created_at | updated_at | Observed browser locator |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 586661162 | NS001_H1_AUDIT_BUNDLE_20260903.zip | 51103 | uploaded | sha256:a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f | vortexpixelz / 202687650 | 2026-09-24T19:26:50Z | 2026-09-24T19:26:50Z | https://github.com/vortexpixelz/ns001/releases/download/untagged-f16adb2dc90288a63b0c/NS001_H1_AUDIT_BUNDLE_20260903.zip |
| 586661207 | NS001_H1_PUBLICATION_PROVENANCE.json | 2298 | uploaded | sha256:ff649229275d88be762e2b762b35b27c3aac8e252a070ac39b18bffc06142d12 | vortexpixelz / 202687650 | 2026-09-24T19:26:51Z | 2026-09-24T19:26:52Z | https://github.com/vortexpixelz/ns001/releases/download/untagged-f16adb2dc90288a63b0c/NS001_H1_PUBLICATION_PROVENANCE.json |

The draft locators above are GitHub's actual returned values. Their `untagged-...`
component is not rewritten into a presumed future published URL. Tag/target association
is verified independently. No third asset, deletion, replacement or retry occurred.

### VERIFIED AFTER UPLOAD — STILL NOT PUBLISHED

Both assets were independently fetched using authenticated asset-ID GETs with
`Accept: application/octet-stream`, stored in fresh temporary download paths, and hashed.
ZIP downloaded SHA-256: `a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`.
Provenance downloaded SHA-256: `ff649229275d88be762e2b762b35b27c3aac8e252a070ac39b18bffc06142d12`.
Both match the frozen inputs, service digests and exact sizes. Draft retrieval required
authenticated access; no anonymous public-asset availability is claimed.

Final readback: exactly two assets; draft=true; published_at=null; immutable=false.
No finalization request was issued. Same four existing workflow runs; no custody
workflow dispatch or attestation creation. Main and scientific artifacts unchanged.
The existing evidence deposit is extended only in its `corrected-upload/` subdirectory,
with original failure files unchanged. New exact readbacks, invocation/result records,
service identities/timestamps and independent hash results are committed with this receipt.
The commit containing this continuation pins its bytes; remote retrieval is checked after push.

- Fresh preflight: PASS.
- Corrected uploads: both succeeded; independent download verdict: PASS.
- Draft published: NO.
- Workflow dispatched: NO.
- Attestation created: NO.
- Existing tag/release preserved; no new tag/release created.
- H2A1: local byte identity VERIFIED; external auditability PARTIAL, pending publication/custody evidence.
- E0 HOLD; H2A2 UNSTARTED; Gate 1 unchanged/PARTIAL.
- One next bounded action: obtain separate authorization to finalize this exact verified
  draft after fresh checks. Do not finalize or dispatch within this circuit.
