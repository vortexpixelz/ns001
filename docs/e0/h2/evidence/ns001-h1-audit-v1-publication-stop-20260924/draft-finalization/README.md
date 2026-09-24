# Existing draft finalization event

Continuation of the existing transaction evidence history; **not the final custody evidence deposit**.
The single authorized external mutation was PATCH /repos/vortexpixelz/ns001/releases/396003416
with exactly {"draft": false}. The pinned gh 2.101.0 tool issued one request, without
retry or any other mutation. Raw request, response, immediate readback and public byte
retrieval observations are preserved here. Previous failure and corrected-upload
records remain unchanged historical evidence.

Release 396003416 is published and immutable. Tag ns001-h1-audit-v1 still resolves to
d9dcfbef1bea173b316bc968fd71421c982422c3. Both existing asset IDs, names, sizes, digests,
labels, uploader identities and creation times are unchanged. Public locators changed
from GitHub's draft identifiers to the intended release tag as a service consequence.
The source target, title and body were not changed.

Both assets were downloaded from their public browser_download_url values into new
temporary paths without authentication; their exact lengths and SHA-256 values match
the frozen inputs. HTTP status was 200; final redirect host release-assets.githubusercontent.com.
Expiring redirect query strings are intentionally not recorded. Full asset metadata
is preserved in release-after.json; retrieval results in public-download-verification.json.
No claim of permanent availability or historical custody is implied.

No scientific or custody workflow run appeared; all four prior run IDs are unchanged.
No workflow was dispatched and no custody attestation was requested or created by this
circuit. GitHub's platform-managed immutable-release mechanisms are distinct from the
custom custody attestation and have not been verified here. No final evidence deposit,
signing verification, E0 execution or H2A2 work was undertaken.

Verify these record bytes with SHA256SUMS. To reproduce anonymous asset checks, download
both exact URLs in public-download-verification.json without credentials and compare
lengths and SHA-256. This directory is pinned by its containing Git commit. Service
JSON records are observed responses, not signed evidence. H2A1 external auditability
remains PARTIAL pending the separately authorized custody/signature and final audit work.

One next bounded action: obtain separate authorization for a fresh custody preflight
and exactly one dispatch of the frozen workflow; do not execute that action now.
