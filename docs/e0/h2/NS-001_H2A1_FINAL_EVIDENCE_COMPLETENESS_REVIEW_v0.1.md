# NS-001 H2A1 final evidence completeness and independent retrieval review v0.1

## Scope and answer

Preparation branch `codex/e0-h2-preparation`; HEAD before `9a1c636fa9501534b9164a31346a8cb5ce62d73c`;
initial working tree clean. Review retrievals occurred from
2026-09-24T23:42:42.603107+00:00 through 2026-09-24T23:42:48.550679+00:00.
Only this review receipt is added, committed and pushed. All acquisition and reproduction
scratch files are outside the repository. No publication, dispatch, attestation creation,
workflow/settings/asset alteration, scientific execution, E0 or H2A2 work occurred.

**YES for independent reproduction of the existing custom custody verification.**
Anonymous external repository/release downloads, an independently downloaded official
verifier, empty configuration/cache and network-isolated verification reproduced both
ZIP and provenance verification and rejected wrong artifact/repository/signer inputs.
Jacob's installed verifier, credentials, logs, Actions artifacts and caches were not
used for reproduction. Local committed blobs were used only as comparison references,
not as verification input. The fresh verifier is a public, pinned toolchain prerequisite;
the reviewer needs a compatible Linux system with Python 3 and user/network namespaces.

**H2A1 external auditability remains PARTIAL.** The committed package lacks the separate
automatic immutable-release attestation and its durable verification material/checks,
explicitly required by the custody retrieval review and retained by the target re-freeze.
A successful custom custody signature is not a substitute for that platform record.
This review does not retrieve/create that missing evidence or waive the requirement.
The bounded review itself is complete despite this finding.

## Anonymous acquisition and stable locations

Every request used Python urllib GET with only User-Agent and Accept headers, no
Authorization, credential store, cookie jar or GitHub CLI authentication. Redirects were
followed; expiring signed redirect query strings are not retained. All 14 retrievals
below returned HTTP 200. The official CLI was downloaded afresh, not copied locally.

Repository evidence pin: `9a1c636fa9501534b9164a31346a8cb5ce62d73c`.
Repository archive: https://codeload.github.com/vortexpixelz/ns001/tar.gz/9a1c636fa9501534b9164a31346a8cb5ce62d73c

All **149 regular repository files** from that anonymous archive matched their respective
`git show 9a1c636fa9501534b9164a31346a8cb5ce62d73c:PATH` bytes. The initially clean checkout provides the matching local
comparison. All four historical evidence manifests verified: **87 file/hash entries**.
This includes every committed evidence-history file and all authority/instruction receipts.
Stable raw locator for any file is
`https://raw.githubusercontent.com/vortexpixelz/ns001/9a1c636fa9501534b9164a31346a8cb5ce62d73c/PATH`.
The bundle, root, manifest and verification README were additionally retrieved directly
through this full-commit raw URL and compared byte-for-byte to preserved local copies.

| Anonymous source | Bytes | SHA-256 |
| --- | ---: | --- |
| https://codeload.github.com/vortexpixelz/ns001/tar.gz/9a1c636fa9501534b9164a31346a8cb5ce62d73c | 337957 | `9dcf8aa7eff2d04396fd03091c89df72e977a440340746d89d8854c0565689f3` |
| https://raw.githubusercontent.com/vortexpixelz/ns001/9a1c636fa9501534b9164a31346a8cb5ce62d73c/docs/e0/h2/evidence/ns001-h1-audit-v1-publication-stop-20260924/attestation-verification/README.md | 4570 | `ef28867b16a5f3537973985eeb7f8ce5a3cef78233d54d2cf01d6abc62d207f2` |
| https://raw.githubusercontent.com/vortexpixelz/ns001/9a1c636fa9501534b9164a31346a8cb5ce62d73c/docs/e0/h2/evidence/ns001-h1-audit-v1-publication-stop-20260924/attestation-verification/SHA256SUMS | 1511 | `0cc7bd3520ef97c4ece2999827c79f5442a9f012549c8c895d1a55f129514bc7` |
| https://raw.githubusercontent.com/vortexpixelz/ns001/9a1c636fa9501534b9164a31346a8cb5ce62d73c/docs/e0/h2/evidence/ns001-h1-audit-v1-publication-stop-20260924/attestation-verification/trusted_root.jsonl | 34634 | `65ca537f6ed8a47fd0e560c421baa1f6c1efb8b25fc200d8c5c02c0e92eb2b9c` |
| https://raw.githubusercontent.com/vortexpixelz/ns001/9a1c636fa9501534b9164a31346a8cb5ce62d73c/docs/e0/h2/evidence/ns001-h1-audit-v1-publication-stop-20260924/attestation-verification/sha256%3Aa055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f.jsonl | 11817 | `6e90aa97a0effa34e73a5c12acc3e96fefb032e5f1ea95eb4dbeaad00e13927b` |
| https://api.github.com/repos/vortexpixelz/ns001/releases/tags/ns001-h1-audit-v1 | 6537 | `26cd44a5bd5daa6ef99047c58272dae0ac9869bb1ccb038242222981e141f83e` |
| https://github.com/vortexpixelz/ns001/releases/tag/ns001-h1-audit-v1 | 205211 | `7f18c6060b993b7258c650aabb23f9e114f16c9577642bd0ccd3e321afc471c0` |
| https://api.github.com/repos/vortexpixelz/ns001/git/ref/tags/ns001-h1-audit-v1 | 374 | `c6fe1c67f0861bff43359f07a77c13a3878877c18a6c60d68bc07b5308738ae2` |
| https://github.com/vortexpixelz/ns001/releases/download/ns001-h1-audit-v1/NS001_H1_AUDIT_BUNDLE_20260903.zip | 51103 | `a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f` |
| https://github.com/vortexpixelz/ns001/releases/download/ns001-h1-audit-v1/NS001_H1_PUBLICATION_PROVENANCE.json | 2298 | `ff649229275d88be762e2b762b35b27c3aac8e252a070ac39b18bffc06142d12` |
| https://raw.githubusercontent.com/vortexpixelz/ns001/d9dcfbef1bea173b316bc968fd71421c982422c3/.github/workflows/ns001-h1-custody.yml | 9457 | `236b8f30a27fa1c3c26f134c794f2e3e989b9b31d1e3adfbcfae18e21fa420bf` |
| https://raw.githubusercontent.com/vortexpixelz/ns001/4333e55beffbe6c7d5ac81eb580f1c5afe04a9bd/docs/e0/h2/NS-001_H2A1_PUBLISHER_MANDATE_SPEC_v0.1.md | 13835 | `018af2f0661debd19b3321cb44a30c3b5bf76c7a597ce7c1640fb6b3bcea4a04` |
| https://raw.githubusercontent.com/vortexpixelz/ns001/cd6e3eb806fa5a5045daaf35904ea927cec68f55/docs/e0/h2/NS-001_H2A1_PUBLISHER_MANDATE_ADOPTION_v0.1.md | 6281 | `1fc91cb4ca3490966adc9a1a6e7b6742f7d6df1bc9fb951004bd2fec2b9d3483` |
| https://github.com/cli/cli/releases/download/v2.101.0/gh_2.101.0_linux_amd64.tar.gz | 15282175 | `9bca2d1c16825f109907a23307628a2f0698fbf99662b73a5cf0b020293072b8` |

Release HTML was available anonymously. Public release metadata reports release
396003416, published/immutable, nondraft, exactly two assets. Public tag ref is a direct
commit ref to `d9dcfbef1bea173b316bc968fd71421c982422c3`. Release title/body/target,
creation/publication timestamps and asset identifiers/names/sizes/digests/uploader IDs
match committed draft-finalization/release-after.json. Both asset downloads ended on
release-assets.githubusercontent.com and matched their service digests and frozen hashes:

| Asset | ID | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| NS001_H1_AUDIT_BUNDLE_20260903.zip | 586661162 | 51103 | `a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f` |
| NS001_H1_PUBLICATION_PROVENANCE.json | 586661207 | 2298 | `ff649229275d88be762e2b762b35b27c3aac8e252a070ac39b18bffc06142d12` |

Observed uploader ID is 202687650. Service created/published timestamps remain service
observations; they are distinct from the signature's verified transparency-log time.
The immutable field is an anonymous service observation here, not replacement evidence
for the missing platform release attestation. Full-commit paths fix content identity,
not perpetual availability. Accepted GitHub hosting/deletion risks remain unchanged.

## Required-object inventory and instruction assessment

All paths in this table are relative to the repository and pinned at the preparation
HEAD above unless a different explicit commit is stated.

| Required object / instruction | Location and finding |
| --- | --- |
| Exact ZIP and digest | attestation-verification/NS001_H1_AUDIT_BUNDLE_20260903.zip under the evidence history; exact public release copy also retrieved. PASS. |
| Exact provenance | Published JSON asset and exact UTF-8 JSON fenced block in docs/e0/h2/NS-001_H2A1_PUBLICATION_TARGET_REFREEZE_v0.1.md. Extracted block including final newline hashes identically to all 2298 public asset bytes; no reserialization needed. There is no standalone provenance JSON in the evidence directory, but its exact bytes are recoverable from committed content. PASS. |
| Release/tag/assets/uploader/timestamps | evidence history draft-finalization/release-after.json, tag-before.json, public-download-verification.json and transaction receipt; fresh public checks agree. PASS as observations. |
| Complete custom custody bundle | attestation-verification/sha256:a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f.jsonl; signed envelope, certificate and log proof retained. PASS. |
| Trusted roots | attestation-verification/trusted_root.jsonl; fresh public TUF acquisition from empty configuration/cache matched it. PASS. |
| Workflow/source | .github/workflows/ns001-h1-custody.yml at d9dcfbef1bea173b316bc968fd71421c982422c3; fresh raw retrieval hash 236b8f30a27fa1c3c26f134c794f2e3e989b9b31d1e3adfbcfae18e21fa420bf. Run 36072331955 attempt 1 is bound in the verified certificate; run.json is a preserved service observation. PASS. |
| Authority specification and adoption | NS-001_H2A1_PUBLISHER_MANDATE_SPEC_v0.1.md at 4333e55beffbe6c7d5ac81eb580f1c5afe04a9bd; NS-001_H2A1_PUBLISHER_MANDATE_ADOPTION_v0.1.md at cd6e3eb806fa5a5045daaf35904ea927cec68f55, both under docs/e0/h2. Historical raw downloads match current committed copies. PASS. |
| Accepted hosting/deposit limits | docs/e0/h2/NS-001_H2A1_EVIDENCE_DEPOSIT_PLAN_ADOPTION_v0.1.md; full current pin above. PASS. |
| Verifier acquisition/version/hash | docs/e0/h2/NS-001_H2A1_ATTESTATION_VERIFICATION_TOOLCHAIN_v0.1.md; fresh official release archive and extracted executable matched recorded SHA-256 values. PASS with documented official-distribution/TUF bootstrap assumptions. |
| Release/tag/hash/provenance instructions | Custody retrieval review, target re-freeze and transaction receipt provide required comparisons and frozen values. Earlier ef71... target and 9f67... provenance are historical proposals, superseded explicitly by target re-freeze; do not use their old command literally. PASS when read in chronology. |
| Offline and identity instructions | attestation-verification/README.md, verify-offline.py and verification-results.json, corrected toolchain policy and target re-freeze. Commands contain sufficient policy; helper hardcodes Jacob's absolute verifier path, and archived argv records contain historical local paths. Portability defect, not missing private evidence: relocated commands below actually succeeded. |
| Hash manifest / outputs | attestation-verification/SHA256SUMS inventories 17 files; transaction receipt pins manifest digest 0cc7bd3520ef97c4ece2999827c79f5442a9f012549c8c895d1a55f129514bc7. Earlier manifests remain valid. PASS. |
| Separate automatic immutable-release attestation | No corresponding complete bundle/verification material or successful NS-001 release-verification result found in the 149-file committed snapshot. Required by custody retrieval review minimum item 6 and target re-freeze. GAP. |

Evidence history base is
`docs/e0/h2/evidence/ns001-h1-audit-v1-publication-stop-20260924/`.
The existing README's acquisition commands describe the historical authenticated
acquisition, not a requirement to repeat attestation API calls. Independent reviewers
retrieve the deposited bundle/root from raw repository URLs instead.

## Actual independent verification

Fresh official Linux amd64 CLI archive SHA-256:
`9bca2d1c16825f109907a23307628a2f0698fbf99662b73a5cf0b020293072b8`.
Fresh executable SHA-256:
`ea857a3f0f7d4276cf5848b236542c5048e2eaa7bdd1b6ddec238f8793e74bff`.
Archive provenance is official GitHub HTTPS; no claim of independent institutional
endorsement or elimination of the verifier-distribution bootstrap assumption is made.
Only the named regular executable member was extracted; no installer ran.

The fresh executable's `attestation trusted-root` command returned 0 using a new HOME,
GH_CONFIG_DIR and XDG_CACHE_HOME with a minimal environment and no token variables.
Its default TUF-authenticated output exactly matched the committed root SHA-256
`65ca537f6ed8a47fd0e560c421baa1f6c1efb8b25fc200d8c5c02c0e92eb2b9c`.
This separately checks the trust bootstrap; offline checks use the downloaded repository
root, not a root trusted merely because it accompanies a bundle. They occurred with
external networking disabled and before fresh TUF acquisition populated the new cache.

Positive inputs were the freshly downloaded public release ZIP and provenance. Bundle
and roots came from the anonymous commit archive. Each verification ran under
`unshare -Urn`, with an empty credential directory, empty cache and minimal environment.
No token variables, local keyring configuration, workflow logs or Actions artifacts
were passed. The original repository helper was not executed because of its absolute
local path; its exact recorded policy was relocated to these downloaded files.

| Case | Exit | Outcome | stdout SHA-256 | stderr SHA-256 |
| --- | ---: | --- | --- | --- |
| zip | 0 | PASS verification | `d8224352326e036d4f0ac0008504e1e1065e3478dfa8f57a0ec96ada9c4f70c7` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| provenance | 0 | PASS verification | `d8224352326e036d4f0ac0008504e1e1065e3478dfa8f57a0ec96ada9c4f70c7` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| wrong-artifact | 1 | PASS rejection | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `486941643d59bcaec905305a9ad2843539956d60f735745f77a05db562cfda19` |
| wrong-repository | 1 | PASS rejection | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `babbf057c2e0960327ecc5540fead45c9b1ed2d7e212b1812d11663f3b75df8a` |
| wrong-signer | 1 | PASS rejection | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `486941643d59bcaec905305a9ad2843539956d60f735745f77a05db562cfda19` |

Wrong artifact was a temporary copy with appended bytes. Wrong repository changed only
`--repo` to `wrong/repository`, rejected with SourceRepositoryOwnerURI mismatch. Wrong
signer changed only the expected certificate workflow filename to `wrong.yml`, rejected
with verification failure. Correct case succeeds with the same verifier, roots and
remaining policy. The original artifact was not modified. No attestation API call was
made. No numeric service attestation ID is needed for local signature verification;
certificate run URI and transparency log identifiers remain available in the bundle.

Verified certificate: repository vortexpixelz/ns001 (1354037143), owner 202687650,
GitHub-hosted runner, exact workflow SAN and issuer below, source/signer digest equal to
the frozen workflow commit, refs/heads/main, run 36072331955/attempts/1.
Verified Rekor time: 2026-09-24T23:21:50Z; log index 2945801585.

The following portable policy states the actual successful check. Set GH to the freshly
obtained pinned executable, E to the downloaded evidence directory, and ARTIFACT to the
freshly downloaded ZIP; repeat for the provenance JSON. Use absolute paths in a scratch
copy and a new empty directory for GH_CONFIG_DIR/HOME/cache. These are reviewer-chosen
locations, not dependencies on Jacob's paths. Check the archive/executable, manifest,
ZIP/provenance, bundle and root hashes listed above first.

```sh
env -i PATH=/usr/bin:/bin HOME="$EMPTY_HOME"   GH_CONFIG_DIR="$EMPTY_CONFIG" XDG_CACHE_HOME="$EMPTY_CACHE"   GH_PROMPT_DISABLED=1 GH_NO_UPDATE_NOTIFIER=1   unshare -Urn "$GH" attestation verify "$ARTIFACT"   --bundle "$E/sha256:a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f.jsonl"   --custom-trusted-root "$E/trusted_root.jsonl"   --repo vortexpixelz/ns001   --cert-identity https://github.com/vortexpixelz/ns001/.github/workflows/ns001-h1-custody.yml@refs/heads/main   --cert-oidc-issuer https://token.actions.githubusercontent.com   --signer-digest d9dcfbef1bea173b316bc968fd71421c982422c3   --source-digest d9dcfbef1bea173b316bc968fd71421c982422c3   --source-ref refs/heads/main   --predicate-type https://github.com/vortexpixelz/ns001/predicates/h1-custody/v1   --deny-self-hosted-runners --format json
```

For release/tag reproduction, anonymously GET the release/tag-ref endpoints listed
above; require nondraft + immutable, release ID 396003416, direct tag commit d9dc...,
exactly the two tabled assets and uploader 202687650. GET both browser_download_url
values; require the exact lengths and hashes. JSON provenance must reject duplicate
keys and match the target-re-freeze block byte-for-byte. Compare its typed fields to
the workflow's frozen contract, require false historical_custody_established and
HOLD/UNSTARTED, and compare both subject digests and predicate release/asset/run bindings.
Read mandate/adoption limitations at their historical pins before interpreting authority.

Both current asset hashes, all shared provenance/predicate fields and release/asset IDs
match. Provenance contains three fields not duplicated inside predicate.artifact:
authority_text, h1_status, mandate_recorded_at. That is not a contradiction: the signed
statement binds the digest of the complete provenance file as its second subject.
An initial review-harness assertion mistakenly required whole-object equality; it was
corrected to compare shared fields and the complete signed provenance digest, after
confirming the exact three-field difference. No evidence bytes were changed.

## Authority, historical boundaries and consistency

Mandate is a self-declared prospective maintainer designation associated with account
202687650 and repository 1354037143. Historical authenticated account observations are
recorded declarations; GitHub's signature authenticates workflow/repository provenance,
not the civil identity of the chat author or institutional endorsement of the mandate.
Adoption/specification references are present and correctly bounded. No corporate,
Symonic LLC, authorship or historical ownership claim is justified or made.

H1 source 6e33cb9ca7019e50e2f247ade9ae8c9a7b40d3ff remains distinct from publication
and workflow commit d9dcfbef1bea173b316bc968fd71421c982422c3. Historical proposal,
STOP, failed-upload, draft, finalization, custody and verification records describe
successive states. Old empty inventories and earlier unauthorized/unstarted statuses
are not present-state contradictions; later explicitly bounded authorizations/events
supersede them without rewriting history. The corrected mutually exclusive identity
flags and changed target/provenance are explicitly documented. No unresolved factual
contradiction was found in the reviewed current identity, signed material, manifests,
release observations, authority limits and scientific HOLD statements. This is a
bounded review, not certification of every historical service assertion.

No creation time/place, original authorship, pre-publication custody, institutional
certification, corporate authority or scientific validation is established. The
bundle's observed_at is a signed workflow assertion; Rekor time is the separately
verified log time. No scientific gate is advanced by custody verification.

## Final verdicts

- Release retrieval verdict: PASS; release page/metadata/tag and both exact assets anonymously retrieved.
- Evidence-deposit retrieval verdict: PASS; full-commit archive, 149 matching regular files, all 87 historical manifest entries verified.
- Bundle retrieval verdict: PASS; archive and direct raw download, original SHA-256 6e90aa97a0effa34e73a5c12acc3e96fefb032e5f1ea95eb4dbeaad00e13927b.
- Trusted-root retrieval verdict: PASS; archive/raw retrieval and independent fresh TUF output match SHA-256 65ca537f6ed8a47fd0e560c421baa1f6c1efb8b25fc200d8c5c02c0e92eb2b9c.
- Independent reproduction verdict: PASS for custom custody verification of ZIP and provenance, exact identity policy and three rejection checks; full broader evidence-completeness claim remains PARTIAL.
- Authority-boundary verdict: PASS as self-declared prospective repository-maintainer authority only.
- Historical-limitations verdict: PASS; explicit and consistent across provenance, bundle and receipts.
- Local-only dependency verdict: NONE for demonstrated custody reproduction; existing helper has a hardcoded path requiring relocation, documented here. No required private files, logs, Actions artifacts/caches, current credentials or anonymous attestation API were used.
- Unresolved evidence gaps: separate automatic immutable-release attestation, durable verification material and its required verification outputs are absent from the committed package. Existing helper/instructions are scattered and path-specific, but the portable policy above resolves reproduction for this review without editing them. No standalone provenance JSON is committed; exact committed fenced-block recovery was verified, so this is not a missing-byte blocker.
- H2A1 external auditability: **PARTIAL**. Custom custody reproducibility verified; do not equate it with full required evidence completeness.
- E0 status: **HOLD**; Gate 1 remains PARTIAL and unchanged.
- H2A2 status: **UNSTARTED**.
- One next bounded action only: separately authorize read-only retrieval, verification and durable preservation of the existing automatic immutable-release attestation material; do not create a new attestation or rerun custody. Not performed here.
