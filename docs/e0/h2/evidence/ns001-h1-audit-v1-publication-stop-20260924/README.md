# Partial publication failure evidence — STOP

This is a durable deposit of the stopped attempt, **not** a completed custody evidence
deposit and not a successful publication receipt. The commit containing this directory
pins these ordinary repository bytes. Files preserve exact API response/error bytes;
these are observations, not cryptographically signed service statements.

Fresh preflight passed from preparation commit 4b290f40def4135e4f2d6850baa3309580b4d623.
The tag ns001-h1-audit-v1 exists at d9dcfbef1bea173b316bc968fd71421c982422c3.
Draft release ID 396003416 exists, with zero assets, published_at=null, immutable=false.
Repository immutable releases remain enabled; a draft is not a finalized immutable release.
No upload succeeded, no finalization occurred, and no custody workflow was dispatched.
The API's draft HTML locator requires authorized access; no public release retrieval is claimed.

Failure: the attempted `gh api --hostname uploads.github.com` call generated the
wrong hostname api.uploads.github.com. This is an operator command construction
error, not evidence that the real GitHub upload endpoint is unavailable. The exact
command script and stderr are preserved. No corrected upload was attempted.
No deletion, replacement, retry, settings change or workflow rerun occurred.

Read-only checks for an authorized reviewer:

- GET /repos/vortexpixelz/ns001/git/ref/tags/ns001-h1-audit-v1
- GET /repos/vortexpixelz/ns001/releases/396003416 (draft requires authentication)
- Inspect release assets and published_at; compare preserved observations.
- Verify SHA256SUMS locally using sha256sum -c SHA256SUMS.
- Retrieve this directory through a commit-pinned GitHub contents/raw URL; do not
  confuse retrievability of failure evidence with public release/asset retrievability.

Frozen provenance remains in NS-001_H2A1_PUBLICATION_TARGET_REFREEZE_v0.1.md,
SHA-256 ff649229275d88be762e2b762b35b27c3aac8e252a070ac39b18bffc06142d12.
The H1 ZIP remains local and unchanged, 51103 bytes, SHA-256
 a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f.
The adopted prospective mandate, historical limitations and provider/deletion
assumptions remain unchanged. No historical custody, authorship, corporate or
institutional authority is established. H2A1 external auditability PARTIAL; E0 HOLD;
H2A2 UNSTARTED; Gate 1 PARTIAL and not advanced.

Next bounded action requires explicit user authorization: correct the upload invocation
and resume against the existing draft and tag, with fresh state checks; do not recreate
objects or dispatch under this stopped attempt.
