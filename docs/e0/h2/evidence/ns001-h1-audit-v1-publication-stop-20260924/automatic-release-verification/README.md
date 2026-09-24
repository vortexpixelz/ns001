# Automatic immutable-release attestation: bounded preservation circuit

Starting preparation HEAD `510fa27e8cc5db085d36d163be2f2796bc70f2fc`;
branch `codex/e0-h2-preparation`; initial tree clean. This directory extends the
existing H2A1 evidence history; it does not replace any custom custody evidence or
STOP/failure history. No release, tag, asset, workflow, settings or scientific content
was changed. No dispatch, signing or attestation creation occurred.

## Release and verifier identity

Release: https://github.com/vortexpixelz/ns001/releases/tag/ns001-h1-audit-v1
Tag `ns001-h1-audit-v1`; release ID `396003416`.
Represented commit (Git SHA-1): `d9dcfbef1bea173b316bc968fd71421c982422c3`.
Repository `vortexpixelz/ns001`, ID `1354037143`; owner ID `202687650`.
Predicate type: `https://in-toto.io/attestation/release/v0.2`.

Pinned gh: `/home/jacob/.local/opt/ns001-gh/2.101.0/gh`, version 2.101.0,
executable SHA-256 `ea857a3f0f7d4276cf5848b236542c5048e2eaa7bdd1b6ddec238f8793e74bff`.
Portable installation provenance is in
`docs/e0/h2/NS-001_H2A1_ATTESTATION_VERIFICATION_TOOLCHAIN_v0.1.md`.
A reviewer may place the same validated executable elsewhere; the historical path
is not a requirement to access Jacob's machine.

Represented assets, also confirmed by fresh anonymous downloads twice:

| Name | Bytes | SHA-256 |
| --- | ---: | --- |
| NS001_H1_AUDIT_BUNDLE_20260903.zip | 51103 | a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f |
| NS001_H1_PUBLICATION_PROVENANCE.json | 2298 | ff649229275d88be762e2b762b35b27c3aac8e252a070ac39b18bffc06142d12 |

`release-json.stdout` is the **exact original stdout bytes** saved before parsing,
without normalization. It contains the complete Sigstore bundle and verification
result, not merely a success badge. SHA-256 `12874c0bce179bf5686b2461ac74b1b5ee542ad904b9e1ae3461735741c4cd75`.
ZIP JSON stdout SHA-256 `12874c0bce179bf5686b2461ac74b1b5ee542ad904b9e1ae3461735741c4cd75`.
Provenance JSON stdout SHA-256 `12874c0bce179bf5686b2461ac74b1b5ee542ad904b9e1ae3461735741c4cd75`.
These three successful JSON outputs happen to be byte-identical; each invocation and
its exit status are separately retained in commands-results.json. Human outputs and
stderr streams are preserved separately; SHA256SUMS hashes all retained files.

Exposed certificate metadata: SAN `https://dotcom.releases.github.com`;
certificateIssuer `CN=Fulcio Intermediate l1,O=GitHub\, Inc.`.
Verified timestamp: TimestampAuthority `timestamp.githubapp.com`,
`2026-09-24T19:52:11Z`. Verified identity SAN regex is
`^https://dotcom\.releases\.github\.com$`; issuer-extension matcher is `.*`.
No OIDC issuer extension, workflow signer, run ID or custom custody signer is claimed
for this separate platform attestation. Fields not returned are not fabricated.
The represented release ID, tag, repository, commit and asset hashes match the
previously preserved publication/custom-custody records.

## Original raw bundle preservation

The pinned release command help exposes JSON output but no standalone download or
local-bundle flag. Its official v2.101.0 source shows the supported retrieval route:

- https://github.com/cli/cli/blob/v2.101.0/pkg/cmd/release/verify/verify.go
- https://github.com/cli/cli/blob/v2.101.0/pkg/cmd/attestation/api/client.go
- https://github.com/cli/cli/blob/v2.101.0/pkg/cmd/release/shared/attestation.go

The first resolves the tag to the Git SHA-1, requests repository attestations with
predicate_type=release and filters initiator/tag; the second constructs the request
and downloads/decompresses the service-returned bundle URL. The last specifies the
platform certificate SAN policy. No endpoint or alternate verification policy was invented.

Using the pinned `gh api --method GET`, the same source-derived endpoint was read:
`repos/vortexpixelz/ns001/attestations/sha1:d9dcfbef1bea173b316bc968fd71421c982422c3?per_page=100&predicate_type=release`.
It returned one object, repository_id 1354037143, initiator github, full inline bundle
and a bundle_url. An independent anonymous urllib GET of that endpoint returned 200
and the same bundle; the expiring URL strings differ, not the signed material.

The exact service-returned bundle_url was fetched anonymously. Its original response
bytes are `release-attestation.bundle.snappy`, SHA-256
`a03112519fadb5c016f77e8169bc1ecf36caffe409f896dbead7cb5af624550e`.
Lossless Snappy decompression, without JSON parsing/reserialization or adding a newline,
produced `release-attestation.bundle.json`, SHA-256
`d7b5d658b2e204e6360d87512da9a1d21c68360642c976590c6e2eda49092f93`.
Decompressed JSON equals the bundle in both API responses and all three successful
verification outputs. The original compressed blob remains preserved alongside it.
Both contain the signed envelope, certificate and RFC3161 timestamp material.
No fabricated bundle or replacement attestation was produced.

API response envelopes contain expiring blob URL queries and were retained only in
temporary scratch storage; their hashes and comparison results are recorded in
raw-bundle-provenance.json. Reproduction never depends on those temporary envelopes
or URLs because original bundle bytes and verification outputs are deposited here.
raw-retrieval.json records the exact API command and anonymous HTTP status.

## Executed checks and access boundary

- Authenticated normal CLI context: release verification PASS, ZIP verify-asset PASS,
  provenance verify-asset PASS, in both human and JSON forms (each exit 0).
- Altered temporary ZIP: exit 1, no matching attested subject for changed SHA-256
  902f7cce02a86f54afdbf0743fb7d28f4eaf06f9880f507859148b403f0d0868.
- Unrelated temporary file: exit 1, no matching attested subject for SHA-256
  0dfc16053499aa00cf7e7dc07b24c209bb9022814a7a25672384de19f9ec4df8.
- Clean environment: fresh public downloads again matched both hashes. Only PATH,
  new HOME/GH_CONFIG_DIR/XDG_CACHE_HOME, GH_PROMPT_DISABLED=1 and
  GH_NO_UPDATE_NOTIFIER=1 were supplied; no tokens or prior configuration/cache.
  Release and both verify-asset JSON commands each exited 4 at the CLI login guard.
  These are failed anonymous CLI attempts, not signature failures and not successful
  independent verification. Exact messages are in clean-*.stderr.
- Anonymous asset retrieval: PASS, four HTTP 200 downloads (initial and clean pair).
- Anonymous raw release-attestation API retrieval: PASS, HTTP 200 for this exact
  endpoint at this observation. Anonymous blob download: PASS, HTTP 200.
- CLI credential dependency: successful `gh release verify*` executions used existing
  configured authentication. Clean credential-free CLI execution is NOT demonstrated.
  The public endpoint did not require authentication for the observed direct GET;
  do not mislabel a client login guard as an observed server-side 401 requirement.
- Live release commands retrieve API/trust data. No offline platform-attestation
  verification was claimed or implemented here. Custody offline verification from
  the prior circuit remains valid and unchanged. Preserved platform bundles/results
  survive future API loss, but independent re-verification using a fully local platform
  policy remains untested by this bounded circuit.

## Reproduction instructions

Use the pinned official gh and choose fresh temporary paths. Download both fixed URLs
without credentials (for example Python urllib or curl without auth configuration):

`https://github.com/vortexpixelz/ns001/releases/download/ns001-h1-audit-v1/NS001_H1_AUDIT_BUNDLE_20260903.zip`

`https://github.com/vortexpixelz/ns001/releases/download/ns001-h1-audit-v1/NS001_H1_PUBLICATION_PROVENANCE.json`

Require exact sizes/hashes above before verification. Set GH to the validated binary,
ZIP and PROVENANCE to those fresh files. In a normally authenticated CLI context run:

```sh
"$GH" release verify ns001-h1-audit-v1 -R vortexpixelz/ns001
"$GH" release verify ns001-h1-audit-v1 -R vortexpixelz/ns001 --format json > release-json.stdout
"$GH" release verify-asset ns001-h1-audit-v1 "$ZIP" -R vortexpixelz/ns001
"$GH" release verify-asset ns001-h1-audit-v1 "$ZIP" -R vortexpixelz/ns001 --format json > zip-json.stdout
"$GH" release verify-asset ns001-h1-audit-v1 "$PROVENANCE" -R vortexpixelz/ns001
"$GH" release verify-asset ns001-h1-audit-v1 "$PROVENANCE" -R vortexpixelz/ns001 --format json > provenance-json.stdout
```

Capture stdout/stderr directly before parsing. Do not overwrite this committed packet;
reproduce in a temporary directory. Require exits 0 and the exact represented tag,
commit, repository, release ID and asset digests. Compare signed bundle contents, not
assumed formatting stability across future verifier versions. Decode the signed
statement only for inspection; use successful cryptographic verification for trust.

For negatives, copy ZIP to a temporary file and append `\nnegative-check\n`; make a
separate temporary unrelated file containing `NS001 unrelated local file negative check\n`.
Invoke verify-asset with each copy and require nonzero exit plus subject-mismatch error.
Never modify the real source ZIP. All actual argument vectors, paths, UTC times and
exit codes are in commands-results.json; public-downloads.json records fresh retrievals.
The scratch paths are historical provenance, not prerequisites for future verification.

To reproduce the anonymous access distinction, repeat the three JSON commands with
an empty HOME/config/cache and no token variables; this version currently exits 4.
Separately GET the exact API endpoint above without auth and inspect the inline bundle
and service-provided blob URL. Do not claim the CLI itself verified anonymously merely
because the underlying GET succeeds. Do not reuse expired blob URLs as durable locators.

Verify this directory with `sha256sum -c SHA256SUMS`. Pin all paths by the full Git
commit that contains this circuit; the manifest digest is recorded in the transaction
receipt. Its own hash is not recursively included. Earlier manifests and custody
instructions remain untouched. Publication hosting/deletion assumptions still apply.

## Narrow gap disposition and limits

The previously identified absence of separate automatic immutable-release attestation
and durable verification material/results is **CLOSED**: original raw bundle, exact
verified JSON/human results, negative results and versioned instructions now exist.
This is narrower than declaring all H2A1 auditability requirements satisfied.
Credential-free CLI reproduction did not pass; a consolidated independent review of
this newly deposited platform evidence has not been performed. H2A1 remains PARTIAL.
All earlier PARTIAL/STOP records remain historical observations, not contradictions.

Platform publication signatures do not establish original creation time/place,
pre-publication custody, authorship, corporate/institutional authority or scientific
validity. Existing self-declared prospective maintainer mandate and accepted GitHub
hosting/deletion limits remain unchanged. E0 HOLD; H2A2 UNSTARTED; Gate 1 PARTIAL.
Next bounded action, not performed: separately authorize a read-only independent review
of the added platform evidence and its credential-free verification route.
