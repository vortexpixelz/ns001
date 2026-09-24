# Existing custody attestation preservation and offline verification

Preparation HEAD: a191990ba33922fcacea79005608e74dafee6dd2.
Acquisition observation: 2026-09-24T23:39:47.239513+00:00.
Run 36072331955: completed/success, attempt 1, workflow/source commit
`d9dcfbef1bea173b316bc968fd71421c982422c3`; raw API observation in run.json.
Initial sandbox network attempt failed before retrieval; authorized network access succeeded.

## Original acquisition

Pinned executable `/home/jacob/.local/opt/ns001-gh/2.101.0/gh`, version 2.101.0,
SHA-256 `ea857a3f0f7d4276cf5848b236542c5048e2eaa7bdd1b6ddec238f8793e74bff`.
From this directory the successful read-only commands were:

```sh
/home/jacob/.local/opt/ns001-gh/2.101.0/gh release download ns001-h1-audit-v1 --repo vortexpixelz/ns001 --pattern NS001_H1_AUDIT_BUNDLE_20260903.zip --dir .
/home/jacob/.local/opt/ns001-gh/2.101.0/gh attestation download NS001_H1_AUDIT_BUNDLE_20260903.zip --repo vortexpixelz/ns001 --predicate-type https://github.com/vortexpixelz/ns001/predicates/h1-custody/v1
/home/jacob/.local/opt/ns001-gh/2.101.0/gh attestation trusted-root > trusted_root.jsonl
```

The original download output `sha256:a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f.jsonl` is retained byte-for-byte:
SHA-256 `6e90aa97a0effa34e73a5c12acc3e96fefb032e5f1ea95eb4dbeaad00e13927b`. No decoded or reserialized replacement was made.
The exact published ZIP is retained, 51103 bytes, SHA-256
`a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`.
Roots: `trusted_root.jsonl`, SHA-256 `65ca537f6ed8a47fd0e560c421baa1f6c1efb8b25fc200d8c5c02c0e92eb2b9c`.
Roots were obtained via the pinned CLI's default authenticated TUF trust mechanism,
covering public Sigstore and GitHub; trust bootstrap is the previously validated official
CLI, not mere inclusion of roots in this packet. Preserve that independent trust assumption.

## Checks and independent reproduction

Run `python3 verify-offline.py` on Linux with unshare user/network namespace support.
It uses an empty temporary GH_CONFIG_DIR, removes GitHub token environment variables,
and runs each verifier under `unshare -Urn` with external networking disabled.
Exact argument vectors and exit statuses are in verification-results.json; raw outputs
are in positive.*, wrong-artifact.*, wrong-identity.*. The script overwrites those
output files on reproduction; reproduce in a temporary copy to retain original evidence.

Exactly one positive returned 0. One temporary ZIP copy with appended bytes returned 1
(signature/artifact verification failed). One exact temporary ZIP copy with repository
constraint `wrong/repository` returned 1 with SourceRepositoryOwnerURI mismatch.
The exact signer identity, OIDC issuer, signer/source commit, source ref, custom predicate,
and GitHub-hosted runner constraints remain enforced. The identity negative tests the
repository component of the repository/signer policy. The original ZIP was not modified.

Verified repository: vortexpixelz/ns001, ID 1354037143; owner ID 202687650.
Signer: `https://github.com/vortexpixelz/ns001/.github/workflows/ns001-h1-custody.yml@refs/heads/main`.
Issuer: `https://token.actions.githubusercontent.com`. Certificate-bound run invocation:
https://github.com/vortexpixelz/ns001/actions/runs/36072331955/attempts/1.
Rekor log index: 2945801585; integrated Unix time: 1790292110
(2026-09-24T23:21:50Z). Full log key ID and certificate fields are in identity-summary.json.
The signed statement also names the provenance subject; this circuit verifies the ZIP only.
No numeric GitHub attestation service ID was returned by the downloaded bundle.

No future anonymous attestation API is needed to verify these preserved local bytes.
Future acquisition of missing copies still depends on archive/repository availability.
SHA256SUMS inventories every file here except itself; its digest is in the transaction
receipt. Git commit identity pins the receipt and manifest without recursive hashes.

This circuit does not complete the broader final evidence audit: the distinct automatic
immutable-release attestation and full independent deposit retrieval remain separate work.
Prospective custody only; no historical custody/authorship/institutional authority claim.
H2A1 external auditability PARTIAL; this ZIP custody verification PASS. E0 HOLD,
H2A2 UNSTARTED, Gate 1 PARTIAL. No run, attestation, release, tag, asset, workflow or
settings mutation occurred. Next bounded action, not performed: separately authorize
final evidence completeness and independent retrieval review.
