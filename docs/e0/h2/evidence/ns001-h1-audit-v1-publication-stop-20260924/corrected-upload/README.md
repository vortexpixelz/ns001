# Corrected upload — verified unpublished draft

This continuation belongs to the existing publication transaction and existing failure
evidence deposit. Earlier files and their SHA256SUMS are unchanged historical records.
The new user instruction authorized exactly two uploads to draft 396003416, not
publication, workflow dispatch, signing or additional objects.

Fresh preflight resolved the pinned CLI tag lookup to draft ID 396003416 and verified
zero assets, target, body, identities, unchanged frozen bytes and absent custody runs.
Actual returned upload_url:
https://uploads.github.com/repos/vortexpixelz/ns001/releases/396003416/assets{?name,label}

Mechanism: pinned gh 2.101.0 release upload ns001-h1-audit-v1 FILE --repo vortexpixelz/ns001,
one file per invocation, no --clobber. Both invocations succeeded and were each followed
by direct release-ID readback. No retry, delete, replacement, tag/release creation or
finalization occurred. This uses the [official CLI upload command](https://cli.github.com/manual/gh_release_upload).

Independent downloads used fresh temporary paths and authenticated asset-ID GETs with
Accept: application/octet-stream, as described by [GitHub's release-asset API](https://docs.github.com/en/rest/releases/assets#get-a-release-asset).
These read back server bytes rather than rehashing only the upload inputs. Both sizes
and hashes match. No public anonymous draft-asset retrieval is claimed. Downloaded
artifact bytes are retained temporarily outside the repository; this deposit contains
observations and hashes, not another public upload of the unpublished ZIP.

State: exactly two verified assets; draft=true; published_at=null; immutable=false
because finalization has not occurred. Observed browser locators contain GitHub's
untagged draft identifier; they are preserved exactly and are not silently replaced
with future published locators. The tag itself resolves to the frozen target.
No custody run or attestation was created. Main unchanged. H2A1 external auditability
remains PARTIAL; E0 HOLD; H2A2 UNSTARTED; Gate 1 unchanged/PARTIAL.

Reproduce read-only verification using the pinned CLI, authenticated for draft access:

    gh api repos/vortexpixelz/ns001/releases/396003416
    gh api repos/vortexpixelz/ns001/releases/assets/586661162 -H 'Accept: application/octet-stream' > fresh-H1.zip
    gh api repos/vortexpixelz/ns001/releases/assets/586661207 -H 'Accept: application/octet-stream' > fresh-provenance.json
    sha256sum fresh-H1.zip fresh-provenance.json

Use the exact pinned binary /home/jacob/.local/opt/ns001-gh/2.101.0/gh in place of gh.
Expected digests are in download-verification.json and the unchanged re-freeze receipt.
This commit-pinned record is a verified-draft continuation, not completed publication
or a completed signed custody bundle. Existing mandate/historical limitations remain.
One next bounded action: obtain separate authorization to finalize this exact verified
draft after fresh checks. No finalization or workflow dispatch is authorized here.
