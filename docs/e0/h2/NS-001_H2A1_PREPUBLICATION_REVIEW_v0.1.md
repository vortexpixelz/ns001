# NS-001 H2A1 prepublication review v0.1

## Scope, evidence and present state

Review recorded 2026-09-23T17:40:50.684828+00:00.
Preparation branch `codex/e0-h2-preparation`, HEAD before
`b0f0ee18de8c56b71559108b4f3dd217535ecd6c`; initial tree clean.
Remote preparation matches. Remote default main is `ef71e56263da8e4d0dfcd5228795356e38b27998`.
Main workflow `.github/workflows/ns001-h1-custody.yml` was independently downloaded
and matches local bytes and SHA-256
`236b8f30a27fa1c3c26f134c794f2e3e989b9b31d1e3adfbcfae18e21fa420bf`.

The adopted specification and adoption receipt were read directly. Mandate remains
ADOPTED, self-declared and prospective. Current authenticated account is
`vortexpixelz`, ID `202687650`; public repository ID `1354037143` is unchanged.
Immutable releases are enabled. Releases and tags are absent. The four run IDs
remain `34488406675`, `33563351013`, `33563214294`, `33562657929`; none is the custody
workflow. H1-digest attestation lookup returns 404, a bounded negative observation,
not proof of universal absence. No workflow dispatch or publishing call is made.

This receipt freezes a proposal for later explicit approval. Independence means
fresh comparison of workflow bytes, mandate and current service observations, not
a second auditor or third-party certification. No publication authority is inferred
from recording these inputs. Only this receipt is created; no separate provenance
file or publication object is materialized in the repository.

## Exact proposed transaction inputs

| Input | Frozen proposal |
| --- | --- |
| Repository | `vortexpixelz/ns001`, ID `1354037143` |
| Tag | `ns001-h1-audit-v1`; one proposed lightweight tag, currently absent |
| Release title | `NS-001 H1 mock-only audit bundle v1` |
| Tag target / publication commit | `ef71e56263da8e4d0dfcd5228795356e38b27998`; full commit, never floating main |
| Release flags | final draft=false, prerelease=false, make_latest=false; proposed staging as draft before final publication |
| ZIP filename | `NS001_H1_AUDIT_BUNDLE_20260903.zip` |
| ZIP byte length | `51103` |
| ZIP SHA-256 | `a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f` |
| Historical H1 source | `6e33cb9ca7019e50e2f247ade9ae8c9a7b40d3ff` |
| Provenance filename | `NS001_H1_PUBLICATION_PROVENANCE.json` |
| Provenance byte length | `2298` |
| Provenance SHA-256 | `9f67d54f2852c386384b9ea1bd1c231bcbb572490bd8b94b9ce84396a7fbac89` |
| Publisher and both asset uploaders | personal account `vortexpixelz`, numeric ID `202687650`; no bot substitution |

Local ZIP was independently rehashed and length checked. The tag target preserves
current reviewed workflow availability; it does not reclassify that commit as the
H1 source or transport preparation history onto main. Tag/title are newly proposed
by this review, not previously approved execution inputs.

The two proposed uploaded assets are exactly the ZIP and provenance JSON. GitHub's
automatically generated source archives are not the H1 ZIP. Do not substitute them.
No generated release notes or extra publication assets are proposed here.

## Exact provenance and authority text

The JSON block below is the complete proposed provenance asset. Its exact bytes
are UTF-8 without BOM, LF line endings, two-space indentation, sorted keys, and
one final LF after the closing brace. Fence lines are excluded. This is an embedded
byte specification, not evidence that the asset exists externally. The proposed
release body is exactly the decoded `authority_text` value followed by one LF.
That body is deliberately event-neutral and does not invent future observations.

```json
{
  "artifact_name": "NS001_H1_AUDIT_BUNDLE_20260903.zip",
  "artifact_sha256": "a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f",
  "artifact_size": 51103,
  "authority_text": "This prospective preservation deposit is designated for the repository-defined NS-001 project by its authenticated maintainer, personal GitHub account vortexpixelz (account ID 202687650), for public repository vortexpixelz/ns001 (repository ID 1354037143), under the scoped mandate adopted in commit cd6e3eb806fa5a5045daaf35904ea927cec68f55, recorded at 2026-09-22T01:10:47Z. Its subject is the unchanged NS001_H1_AUDIT_BUNDLE_20260903.zip, 51103 bytes, SHA-256 a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f, preserving H1 source commit 6e33cb9ca7019e50e2f247ade9ae8c9a7b40d3ff for independent inspection. H1 remains H1_MOCK_ONLY_HOLD; reported historical mock tests are not new tests or scientific validation. The publication target ef71e56263da8e4d0dfcd5228795356e38b27998 is distinct from the H1 source checkpoint. Authority is a self-declared prospective maintainer mandate, not corporate, institutional, Symonic LLC, or third-party certification. This statement establishes no original creation time or place, original authorship, pre-publication custody, historical possession, or retrospective project authorization. Actual publication, uploader, signer, identifiers, service timestamps, witnessed timestamps and retrieval observations must be established separately from observed records; this text does not assert that those events have occurred. No scientific artifact is changed. E0 remains HOLD, Gate 1 remains PARTIAL, and H2A2 remains UNSTARTED. Publication does not authorize experiments or subsequent workflow execution.",
  "e0_status": "HOLD",
  "h1_source_commit": "6e33cb9ca7019e50e2f247ade9ae8c9a7b40d3ff",
  "h1_status": "H1_MOCK_ONLY_HOLD",
  "h2a2_status": "UNSTARTED",
  "historical_custody_established": false,
  "mandate_adoption_commit": "cd6e3eb806fa5a5045daaf35904ea927cec68f55",
  "mandate_recorded_at": "2026-09-22T01:10:47Z",
  "publication_commit": "ef71e56263da8e4d0dfcd5228795356e38b27998",
  "publisher_account_id": 202687650,
  "release_tag": "ns001-h1-audit-v1",
  "repository_id": 1354037143,
  "schema": "ns001.h1.publication-provenance.v1"
}
```

VERIFIED for internal consistency: all 13 typed mandatory workflow fields
match the actual embedded `expected` dictionary, checked by evaluating only that
literal dictionary expression with frozen inputs (no guard, download, or workflow
execution). JSON has unique keys and a deterministic digest. The authority text
qualifies the mandate, mock-only status and historical limits. Its extra narrative
is a publisher declaration; the workflow's typed checks do not independently prove
its truth. The adoption timestamp is the recorded session time, not a signed
message timestamp. No scientific result or retrospective certification is claimed.

The final observed publication record required by the mandate must be separate:
release/asset IDs and service/observation times do not yet exist and cannot honestly
be frozen now. They are not inserted later into this frozen JSON. Its prospective
statement is not a completed publication/custody receipt. Release title/body remain
mutable even when assets/tag are locked; authority text therefore also resides in
the digest-bound proposed asset.

## Exact future custody inputs and identity policy

These are dormant proposed inputs, not a dispatch instruction:

```json
{
  "release_tag": "ns001-h1-audit-v1",
  "publication_commit": "ef71e56263da8e4d0dfcd5228795356e38b27998",
  "provenance_sha256": "9f67d54f2852c386384b9ea1bd1c231bcbb572490bd8b94b9ce84396a7fbac89",
  "authorization": "ATTEST-EXACT-H1"
}
```

Proposed dispatch ref: `main`, only if it still resolves to `ef71e56263da8e4d0dfcd5228795356e38b27998`
and the workflow digest still matches. Stop for review on drift; do not substitute
another ref silently. Dispatch needs its own explicit authorization after published
assets independently pass verification. The acknowledgement string is not consent.
First run attempt only; check for prior custody runs/attestations before the single
mandated dispatch. Concurrency does not enforce a lifetime count.

Expected signer workflow: `vortexpixelz/ns001/.github/workflows/ns001-h1-custody.yml`.
Expected workflow ref:
`vortexpixelz/ns001/.github/workflows/ns001-h1-custody.yml@refs/heads/main`.
Expected certificate identity:
`https://github.com/vortexpixelz/ns001/.github/workflows/ns001-h1-custody.yml@refs/heads/main`.
Expected OIDC issuer: `https://token.actions.githubusercontent.com`.
Expected source/signer commit: `ef71e56263da8e4d0dfcd5228795356e38b27998` (distinct from the file SHA-256).
Expected trigger account/actor ID: `vortexpixelz` / `202687650`.
Pinned signing action remains `actions/attest@1e69f48acb82d1966a394da916b4c1698aa569d6`.
Expected predicate type:
`https://github.com/vortexpixelz/ns001/predicates/h1-custody/v1`.
Expected subjects: exactly the ZIP and provenance JSON with the SHA-256 values
above; accept names corresponding to the workflow's fixed `custody/` paths, never
an unrelated digest. No existing signer certificate or attestation is asserted.

The signer is the workflow identity, not the personal uploader. Separately verify
release author, both uploaders and dispatch actor against the account ID. GitHub
account authentication is not civil identity, corporate delegation or proof of
historical custody. Certificate claims and witnessed timestamps must be verified;
predicate fields alone are workflow assertions. Hosted runtime, TLS/service trust,
action behavior and future execution success remain residual assumptions.

## Post-publication verification plan (not executed)

1. Before any future authorized transaction, recheck account/repository IDs,
   enabled immutability, absent proposed tag/release, unchanged main/workflow and
   exact local ZIP/provenance hashes. Stop on conflict or drift, never overwrite.
2. If separately authorized, stage the one release and both exact assets as draft,
   verify staging bytes and uploaders, then finalize. Do not publish an empty release
   and try adding assets afterward. At finalization verify immutable=true,
   draft=false, prerelease=false, exact tag and dereferenced target commit; record
   release author/ID/URL and both asset IDs/names/sizes/uploaders/digests/URLs.
3. Retrieve both assets anonymously from
   `https://github.com/vortexpixelz/ns001/releases/download/ns001-h1-audit-v1/`
   plus their exact filenames. Record retrieval UTC and redirect chain, enforce
   HTTPS, compute bytes/digests independently, compare to this receipt. Parse JSON
   with duplicate-key rejection and verify typed fields and complete authority text.
   Record release `published_at` and ZIP `created_at`, requiring usable
   `YYYY-MM-DDTHH:MM:SSZ`; keep service times distinct from independent observation.
4. Verify GitHub's automatic immutable-release attestation separately against the
   exact tag/commit/asset digests; retain its verification material. It is not the
   discretionary custody-workflow attestation. Record a missing/unverifiable record
   as failure, not an inferred signature.
5. Only after separate dispatch authorization, require a non-skipped successful
   custody run, first attempt, expected inputs/actor/ref/commit and exact workflow
   bytes. Retrieve its attestation bundle; independently verify both local subjects
   with repository, signer workflow, certificate identity, OIDC issuer, source and
   signer digests, and custom predicate type constrained as above. Check verified
   certificate/time evidence and cross-check all predicate release/asset/provenance
   identifiers and time observations. A success badge is insufficient.
6. Preserve the verified bundle, its digest, trusted verification material, actual
   observation record and an independently retrievable locator. Do not attempt to
   append these to the already immutable release. Recheck no scientific files,
   settings or unauthorized objects changed; retain E0 HOLD and H2A2 UNSTARTED.

[GitHub immutable-release documentation](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases)
confirms draft-first staging, asset/tag protection, mutable title/body, and the
separate automatic release attestation. It does not guarantee eternal availability.
[GitHub attestation verification documentation](https://cli.github.com/manual/gh_attestation_verify)
supports constraining signer/source identities and custom predicate type, checking
verified timestamps, and using downloaded bundles for offline verification.

## Residual gap and preservation

Publication-ready is PARTIAL for the complete external-auditability transaction:
the exact proposed inputs are consistent, but durable independently retrievable
custody verification material is not yet demonstrated. The unchanged workflow
reports a runner-local bundle path/hash and attestation URL; it does not upload a
bundle archive. Its future bundle cannot be added after immutable publication.
GitHub's attestation service may provide retrieval, but this review has no actual
bundle and has not established an anonymous durable route for this repository.
Do not infer failure of that route; do not infer it is proven. No extra release,
workflow change or second archive is silently authorized. Historical custody remains
unestablished and cannot be repaired by a new signature or deposit.

No publication object, dispatch or settings mutation occurred. Before committing,
compare main, settings, releases, tags, runs and H1 attestation response with the
initial read-only inventory, and verify all pre-existing tracked file hashes.
Only this receipt is added. No scientific tests or workflow were run; the prior
132-test correction result is not represented as a new run.

## Closing verdicts

- Proposed tag: `ns001-h1-audit-v1`.
- Proposed release title: `NS-001 H1 mock-only audit bundle v1`.
- Target commit: `ef71e56263da8e4d0dfcd5228795356e38b27998`.
- ZIP identity: `NS001_H1_AUDIT_BUNDLE_20260903.zip`, 51,103 bytes,
  SHA-256 `a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`.
- Provenance text verdict: VERIFIED as a bounded prospective statement; exact JSON
  bytes/digest frozen above; not completed publication evidence.
- Publisher/uploader identity verdict: VERIFIED current account context; actual
  future publisher/uploaders must be observed independently.
- Workflow-input verdict: VERIFIED internally consistent; dormant, not authorized.
- Attestation-input verdict: VERIFIED proposed identity/subject constraints;
  actual signed evidence and durable retrieval remain unverified.
- Post-publication verification plan: six ordered checks above; fail closed on any
  identity, byte, state, timestamp, signature or retrieval mismatch.
- Publication-ready verdict: PARTIAL, for the residual verification-material gap;
  execution permission is separately absent, not inferred from this readiness label.
- H2A1: local byte identity VERIFIED; independent external auditability PARTIAL;
  all eight substantive H2 gates remain unresolved.
- E0: HOLD. Gate 1 remains PARTIAL.
- H2A2: UNSTARTED.
- One next bounded action: separately authorize a read-only review of durable,
  independently retrievable custody-bundle preservation using the unchanged workflow
  and this exact release proposal; no publication or dispatch.
