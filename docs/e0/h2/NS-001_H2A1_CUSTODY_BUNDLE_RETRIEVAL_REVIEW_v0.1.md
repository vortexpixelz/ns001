# NS-001 H2A1 custody-bundle preservation and retrieval review v0.1

## Scope and fresh observations

Read-only review on 2026-09-23 UTC. Preparation branch
`codex/e0-h2-preparation`, HEAD `15ce97f7c29d28d6e1a5d005a8003a8790f5c08d`,
initial tree clean. Default main remains
`ef71e56263da8e4d0dfcd5228795356e38b27998`. Remote workflow bytes match SHA-256
`236b8f30a27fa1c3c26f134c794f2e3e989b9b31d1e3adfbcfae18e21fa420bf`.
Immutable releases remain enabled; the workflow is unrun. Release/tag inventories
are empty; four pre-existing run IDs remain unchanged. Repository-digest and
correct owner-digest authenticated attestation queries return 404. These observations
are bounded, not universal proofs that no copy or attestation exists anywhere.

**VERIFIED:** Proposed inputs remain `ns001-h1-audit-v1`, title
`NS-001 H1 mock-only audit bundle v1`, target main commit above. ZIP is
`NS001_H1_AUDIT_BUNDLE_20260903.zip`, 51,103 bytes, SHA-256
`a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`.
Frozen proposed provenance is `NS001_H1_PUBLICATION_PROVENANCE.json`, 2,298 bytes,
SHA-256 `9f67d54f2852c386384b9ea1bd1c231bcbb572490bd8b94b9ce84396a7fbac89`.
It is still an embedded proposal, not a published asset. No input is changed here.

**VERIFIED:** Anonymous HTTPS GETs at full commit references retrieved the mandate,
adoption and prepublication receipt, each byte-equal to its local counterpart:

| Record | Commit | File SHA-256 |
| --- | --- | --- |
| Mandate spec | `4333e55beffbe6c7d5ac81eb580f1c5afe04a9bd` | `018af2f0661debd19b3321cb44a30c3b5bf76c7a597ce7c1640fb6b3bcea4a04` |
| Adoption | `cd6e3eb806fa5a5045daaf35904ea927cec68f55` | `1fc91cb4ca3490966adc9a1a6e7b6742f7d6df1bc9fb951004bd2fec2b9d3483` |
| Prepublication review | `15ce97f7c29d28d6e1a5d005a8003a8790f5c08d` | `9f7dfdc2b29aac20cebcd1ba46560e73a85e0e413aaf1c176f269876b699e896` |

Locators use `https://raw.githubusercontent.com/vortexpixelz/ns001/COMMIT/`
plus the respective existing `docs/e0/h2/NS-001_H2A1_..._v0.1.md` path:
`PUBLISHER_MANDATE_SPEC`, `PUBLISHER_MANDATE_ADOPTION`, `PREPUBLICATION_REVIEW`.
These pin bytes rather than a mutable branch. Continued hosting is a separate assumption.

## Minimum complete evidence set (definition only)

**REQUIRES FUTURE PUBLICATION OBJECT:** A complete custody packet must preserve:

1. Exact ZIP identity, filename and length, anonymously retrievable ZIP locator,
   and source H1 commit `6e33cb9ca7019e50e2f247ade9ae8c9a7b40d3ff`. The ZIP need
   not be duplicated inside the packet if its external bytes remain retrievable.
2. Repository ID `1354037143`, release ID, tag, dereferenced commit, asset IDs,
   fixed download URLs, release/asset states, actual author and both uploader IDs.
   Intended uploader is `vortexpixelz`, ID `202687650`; record actual observations.
3. Exact provenance bytes and digest, not reserialized JSON or a screenshot.
4. Raw release/asset/ref observation responses, acquisition UTC, URLs, relevant
   headers and redirect chain; distinguish service publication/creation timestamps
   from reviewer observation and cryptographically witnessed timestamps.
5. Complete custody Sigstore bundle: signed statement/envelope, signature,
   certificate and required verification material/log or timestamp proofs. A bundle
   digest, link, success badge or decoded predicate alone is insufficient.
6. Separate automatic immutable-release attestation and its verification material.
   Do not conflate this platform record with the one discretionary custody attestation.
7. Exact workflow source, file digest, signer/source commit and ref, action pin,
   actual run ID/attempt/actor, certificate identity/issuer and verified time evidence.
8. Copies of the adopted mandate/specification, adoption record and frozen proposal,
   with original full-commit references and digests. These preserve a prospective
   self-declaration, not a signed chat message or independent institutional authority.
9. Versioned verification instructions, verifier version and distribution digest,
   trusted-root material with independently authenticated source/version, verification
   outputs, a file/digest manifest, and explicit interpretation/failure rules.
   Roots supplied by the same packet must not be trusted merely because they are there.
10. Explicit H1 mock-only, E0 HOLD, H2A2 UNSTARTED and historical-custody limitations.
    Packet observations are attributable statements; copying API JSON into a packet
    does not turn it into GitHub-signed historical evidence.

A manifest inventories components; it does not hash itself recursively. Publish
its digest through the separately identified deposit record. Future object IDs,
actual timestamps and bundle hashes cannot be invented or frozen in advance.
No packet, separate archive or proposed component files are created by this review.

## Object lifetime and retrieval matrix

Classifications distinguish integrity from availability; “immutable” is not “immortal.”

| Object | Lifetime / retrieval classification | Finding |
| --- | --- | --- |
| Published immutable release ZIP/provenance | Immutable bytes; stable but deletable with release/repository; externally retrievable while public | VERIFIED WITH RESIDUAL ASSUMPTION; actual objects still required |
| Release title/body/latest designation | Mutable; externally retrievable | VERIFIED; never sole authority/verification record |
| Locked release tag | Fixed target while immutable release exists; availability conditional | VERIFIED WITH RESIDUAL ASSUMPTION |
| Full Git commit/blob | Content-addressed immutable bytes; stable but deletable/unavailable if hosting/access/reachability changes | VERIFIED WITH RESIDUAL ASSUMPTION; pinned raw records tested |
| Repository file at branch/main | Mutable locator | UNSUPPORTED as sole frozen evidence |
| Artifact attestation service record | Signed content; service collection deletable, availability/access conditional | PARTIAL; no permanent retention guarantee established |
| Runner-local bundle path | Ephemeral, later lost with runner | VERIFIED; not an external preservation mechanism |
| Workflow logs/summary | Ephemeral/retention-limited and deletable | UNSUPPORTED as sole durable packet |
| Workflow artifacts | Expiring/deletable; documented download requires sign-in/read access | UNSUPPORTED as anonymous durable archive |
| Actions caches | Evictable runtime acceleration data | UNSUPPORTED as custody archive |
| Live API response | Mutable service observation, not durable itself | VERIFIED WITH RESIDUAL ASSUMPTION; preserve raw observation separately |
| Retained original ZIP on local machine | Locally held only | VERIFIED; cannot satisfy independent external retrieval |

[Immutable-release documentation](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases)
protects assets/tag after publication while allowing title/body edits and release
deletion. It recommends attaching assets before publication. Thus an asset created
by this post-publication custody workflow cannot be added to that same frozen release.
This is a sequencing constraint, not a reason to weaken the workflow's immutable-release guard.

[Actions artifact documentation](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts)
states default log/artifact retention is 90 days and artifact download requires
sign-in/read access. [Cache documentation](https://docs.github.com/en/actions/concepts/workflows-and-actions/dependency-caching)
describes dependency reuse; it supplies no custody preservation guarantee.

## Attestation retrieval: documented capability versus observed access

**VERIFIED / PARTIAL:** The appropriate documented personal-owner lookup is
`GET https://api.github.com/users/vortexpixelz/attestations/sha256:a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`.
[User attestation API](https://docs.github.com/en/rest/users/attestations)
documents anonymous access for public resources and also attestation deletion.
Anonymous probes, both with and without `X-GitHub-Api-Version: 2026-03-10`, returned
401 Requires authentication. An authenticated versioned request returned 404.
No extant attestation was available for a positive retrieval test. These observations
do not prove anonymous retrieval of a future real public bundle impossible, nor do
the documentation claims prove it works here. The earlier repository-path 404 is
not sufficient evidence about this owner-level retrieval capability.

**VERIFIED WITH RESIDUAL ASSUMPTION:**
[CLI download](https://cli.github.com/manual/gh_attestation_download) supports saving
bundles for offline use; [CLI verification](https://cli.github.com/manual/gh_attestation_verify)
supports local bundles, custom predicate type and signer/source constraints.
A successful authenticated download could seed a later anonymous packet deposit;
it is not itself proof of anonymous public availability. Preserve and verify actual
signed bundles, not workflow-authored predicate claims alone.

## Minimum external location strategy

**VERIFIED WITH RESIDUAL ASSUMPTION:** Two logical locations are needed with this
unchanged workflow: (A) frozen ZIP/provenance release assets; (B) a post-publication,
post-attestation evidence deposit containing the complete packet. The original
immutable release cannot contain its own later-generated custody bundle. Service
lookup alone has not met the required retrieval test or retention assurance.

A minimum GitHub-only candidate is a separately authorized evidence-only Git commit
on the preparation branch after the future event, containing the packet files and
manifest. Record its full commit, tree and per-file SHA-256 values, then independently
retrieve every file anonymously via full-commit raw URLs. Keep that commit reachable;
never use the branch tip, mutable release body, logs or local runner path as the sole
locator. This does not require changing main, changing this workflow, creating a
second release, or modifying the frozen original release. It remains a proposed
mechanism, not an approved or demonstrated deposit. No exact future deposit commit
can be supplied before its unknown evidence bytes exist.

**GitHub-only: conditionally sufficient**, if content-addressed retention on a public
repository with deletion/availability risk is accepted and the complete packet passes
anonymous retrieval and independent signature verification. It eliminates dependence
on mutable branch contents, not dependence on continued GitHub hosting. GitHub alone
is not a guarantee against repository deletion, access changes or service loss.

**Second archive:** a separate post-event evidence object is required for this
recommended route; a second provider or independent archival authority is not
inherently required for the scoped prospective claim. If survival of GitHub/account
loss is required, an independently administered mirror/archive becomes necessary.
No lifetime requirement was silently invented here. A second immutable release would
exceed the adopted one-release bound and require separate scope approval; it is not
the minimum proposed route. Another archive cannot establish missing historical custody.

## Exact independent reviewer sequence (future, read-only)

1. Obtain the published packet's full commit/manifest digest from its attributable
   deposit record. Retrieve all named components from pinned external locators,
   without repository credentials or the publisher's local machine. Missing deposit
   identifiers mean STOP, not guessing a branch head. Download the ZIP and provenance
   from `https://github.com/vortexpixelz/ns001/releases/download/ns001-h1-audit-v1/`
   plus their exact frozen filenames. Use HTTPS and record redirect observations.
2. Hash the ZIP, provenance and packet files independently; compare size/digest to
   the frozen values above and packet manifest. Recover exact provenance bytes.
3. Resolve tag `ns001-h1-audit-v1` to
   `ef71e56263da8e4d0dfcd5228795356e38b27998`; verify immutable, nondraft release,
   repository/asset IDs, actual account uploaders and locators. Verify the distinct
   automatic release attestation. Compare live state to preserved observations;
   report differences, do not silently substitute newer evidence.
4. Parse provenance with duplicate-key rejection; check all typed mandatory fields
   against the frozen proposal, including false historical-custody claim, H1 source,
   adoption, target, tag and HOLD/UNSTARTED statuses. Check required service timestamps
   as usable UTC seconds; do not reinterpret them as original ZIP creation times.
5. Verify each of the ZIP and provenance against the saved custody bundle using an
   independently obtained verifier/trust root. A proposed command template is:

```sh
gh attestation verify SUBJECT_FILE --bundle CUSTODY_BUNDLE_FILE \
  --repo vortexpixelz/ns001 \
  --signer-workflow vortexpixelz/ns001/.github/workflows/ns001-h1-custody.yml \
  --cert-identity https://github.com/vortexpixelz/ns001/.github/workflows/ns001-h1-custody.yml@refs/heads/main \
  --cert-oidc-issuer https://token.actions.githubusercontent.com \
  --signer-digest ef71e56263da8e4d0dfcd5228795356e38b27998 \
  --source-digest ef71e56263da8e4d0dfcd5228795356e38b27998 \
  --source-ref refs/heads/main \
  --predicate-type https://github.com/vortexpixelz/ns001/predicates/h1-custody/v1 \
  --deny-self-hosted-runners --format json
```

`SUBJECT_FILE` and `CUSTODY_BUNDLE_FILE` are explicit future local download paths,
not unresolved identity policy. Run once per subject; require both exact digests
in the intended statement. Confirm installed verifier supports these documented
options; record version/digest. For fully offline verification use independently
validated preserved roots through `--custom-trusted-root`. Do not disable verification
to accommodate an error. Inspect verified certificate/time data and cross-check
predicate release, asset, provenance, workflow, run and actor bindings against the
packet. The workflow file SHA-256 is distinct from signer/source Git commit IDs.
6. Verify copied mandate/adoption bytes against the pinned references and digests;
   confirm scoped prospective personal-account authority, actual uploader versus
   workflow signer separation, and no corporate or historical certification.
7. Confirm H1 mock-only, no new scientific result, E0 HOLD and H2A2 UNSTARTED.
   Report any inaccessible or unverified component instead of declaring complete
   external auditability. Observations and signed assertions retain their distinct
   evidentiary roles; signature validity does not prove every predicate assertion true.

## Fail-closed conditions and preservation

**UNSUPPORTED as complete auditability:** a missing ZIP/provenance/bundle/authority
record; branch-only or unstable locator without immutable identity; digest mismatch;
unverifiable signer, trust root or timestamp proof; evidence only in logs/artifacts;
reserialized provenance replacing exact bytes; unmatched release/publisher/subject
bindings; a badge substituted for attestation; private/authenticated-only access when
anonymous retrieval is required; or a packet available only locally. A deleted object
can fail availability even when previously verified hashes remain correct.

**NEEDS ADDITIONAL SOURCE CHECK / REQUIRES FUTURE PUBLICATION OBJECT:** actual future
anonymous bundle access, valid signed material, repository retention commitment,
exact packet deposit identifiers and retrieval of every component remain unverified.
No promise of permanent service retention was identified. The complete packet cannot
exist before the events it records; this is an execution dependency, not scientific
validation. The review is complete as a bounded specification with these open items.

Only this receipt is added. Pre-existing tracked bytes are compared to the starting
hash inventory; main, settings, runs, release/tag lists and attestation query are
reread before commit. No release/tag/asset/attestation/second archive is created;
no dispatch, settings change, main edit, scientific execution or tests are performed.
The receipt commit/push is the sole authorized external write.

## Closing verdicts

- Minimum custody-bundle contents: the ten-component evidence set above, including
  exact provenance, complete signed bundles, source/authority copies and verifier policy.
- Durable evidence objects: immutable release bytes and pinned full-commit packet
  bytes, conditional on external retention; actual post-event packet still required.
- Ephemeral evidence objects: runner files, logs, run summaries, expiring workflow
  artifacts and caches; none is a sole preservation source.
- Stable retrieval plan: fixed release asset URLs plus a separately authorized
  post-event evidence commit, exact full-commit raw URLs and a digest manifest.
- GitHub-only preservation sufficient: CONDITIONAL; not demonstrated end-to-end,
  and not independent of GitHub deletion/availability risks.
- Second archive required: separate evidence deposit YES for recommended route;
  second archival provider NO inherently, unless independent survival is required.
- Independent reviewer procedure: retrieve, hash, verify release/tag/commit,
  provenance, attestation, authority scope and historical limits as specified above.
- Exact unresolved retrieval assumptions: future packet completeness/signatures,
  anonymous access (owner API currently 401), full-commit retention, verifier/root
  availability, durable deposit identifiers and accepted deletion/hosting risk.
- Publication-ready verdict: PARTIAL; mechanism specified, not implemented or proved.
- H2A1: local byte identity VERIFIED; external auditability PARTIAL; all eight
  substantive H2 gates remain unresolved.
- E0: HOLD; Gate 1 PARTIAL.
- H2A2: UNSTARTED.
- One next bounded action: obtain explicit acceptance or revision of the proposed
  post-event evidence-commit preservation plan and its hosting/deletion assumptions,
  without authorizing publication, dispatch or creation of the packet.
