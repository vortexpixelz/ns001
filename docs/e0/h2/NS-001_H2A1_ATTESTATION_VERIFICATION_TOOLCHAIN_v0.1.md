# NS-001 H2A1 attestation verification toolchain v0.1

## Scope and installation

Preparation branch `codex/e0-h2-preparation`; starting HEAD
`a9c5b586af397c09e2b6805aa876a4db51253b99`; initially clean.
Only this receipt changes repository content. Public example validation uses the
GitHub CLI distribution, never the NS-001 H1 ZIP. No publication or dispatch.

Phase A: machine is x86_64, Linux Mint 22.2 Zara, Ubuntu noble base.
Existing `/usr/bin/gh` is version 2.45.0, dpkg package
`2.45.0-1ubuntu0.3`. PATH places user-local directories before `/usr/bin`, but
`command -v gh` resolves to `/usr/bin/gh`. Existing keyring authentication reports
active personal account vortexpixelz, SSH Git transport and scopes admin:public_key,
gist, read:org, repo, user. No token contents were exposed or credential changes made.

Selected official release: [cli/cli v2.101.0](https://github.com/cli/cli/releases/tag/v2.101.0),
reported latest and immutable by the official GitHub API at selection time.
Downloaded from its official release URL:
`https://github.com/cli/cli/releases/download/v2.101.0/gh_2.101.0_linux_amd64.tar.gz`
and the adjacent `gh_2.101.0_checksums.txt`.
Archive SHA-256 `9bca2d1c16825f109907a23307628a2f0698fbf99662b73a5cf0b020293072b8`
matched both the official checksum file and release API digest before execution.
Only the named regular binary member was extracted, without running an installer.

Pinned selected binary: `/home/jacob/.local/opt/ns001-gh/2.101.0/gh`.
Binary SHA-256 `ea857a3f0f7d4276cf5848b236542c5048e2eaa7bdd1b6ddec238f8793e74bff`.
No system package replaced, PATH/symlink changed, unrelated package upgraded,
repository file modified during installation or authentication switched.
All validation invoked that explicit binary. Plain `gh` remains the older system
version; future NS-001 commands must use the pinned absolute path.

Checksum bootstrap trusts official GitHub HTTPS/distribution. Subsequent release
and artifact signature checks strengthen provenance but do not remove the usual
bootstrap assumption of executing a verifier distributed by that provider.

## Command surface and trusted roots

All six requested help invocations returned exit 0:
`attestation --help`, `attestation download --help`, `attestation verify --help`,
`attestation trusted-root --help`, `release verify --help`,
`release verify-asset --help`.

`attestation trusted-root` succeeded using its supported default TUF trust path;
`attestation trusted-root --verify-only` also returned 0. Root material is saved
outside the repository at the installation directory's `trusted_root.jsonl`:
34,634 bytes; SHA-256
`65ca537f6ed8a47fd0e560c421baa1f6c1efb8b25fc200d8c5c02c0e92eb2b9c`.
It was actually used successfully in network-isolated verification, not merely
accepted as syntactically valid JSON. Trust bootstrap uses the selected official
CLI and its supported trust infrastructure, not arbitrary roots in an untrusted
packet. A later deposit must preserve appropriate root material and authenticated
provenance; this snapshot is not a promise to validate every future certificate.

## Existing public verification tests

All tests used `gh_2.101.0_linux_amd64.tar.gz` from cli/cli, not an NS-001 object.
The following operations returned 0, with stdout/stderr retained outside the repo:

1. `release verify v2.101.0 --repo cli/cli --format json`.
2. `release verify-asset v2.101.0 ARCHIVE --repo cli/cli --format json`.
3. `attestation verify ARCHIVE --repo cli/cli --format json` (online).
4. `attestation download ARCHIVE --repo cli/cli`.

Automatic release verification and generic workflow attestation verification are
separate successful checks. The retrieved generic bundle is
`sha256:9bca2d1c16825f109907a23307628a2f0698fbf99662b73a5cf0b020293072b8.jsonl`,
20,501 bytes, SHA-256
`d4e4d546b21e3517c53fa94908d4d8a7422128f48c78309b7a740bf654bc79b3`.
It is retained with the archive, checksum file, roots, help text and verification
outputs under `/home/jacob/.local/opt/ns001-gh/2.101.0/`.
These are public-example tool-validation materials, not the future NS-001 custody
evidence deposit. No claim of durable external publication of these local files.

Verified public certificate identifies:
`https://github.com/cli/cli/.github/workflows/deployment.yml@refs/heads/trunk`,
issuer `https://token.actions.githubusercontent.com`, source/signer commit
`0cf1092493af067646fc5f3db9421c6a6ec9c938`, GitHub-hosted runner, public repository
cli/cli and run `34980146643` attempt 1. These are public example identities only.

## Actual offline validation and identity controls

A fresh user/network namespace (`unshare -Urn`) disabled external networking.
`GH_CONFIG_DIR` pointed to an empty validation directory; GH/GITHUB token variables
were removed from the test environment and prompting disabled. No credentials were
needed. Verification used the saved archive, bundle and roots with explicit policy:

```sh
/home/jacob/.local/opt/ns001-gh/2.101.0/gh attestation verify ARCHIVE   --bundle BUNDLE --custom-trusted-root ROOTS --repo cli/cli   --cert-identity https://github.com/cli/cli/.github/workflows/deployment.yml@refs/heads/trunk   --cert-oidc-issuer https://token.actions.githubusercontent.com   --signer-digest 0cf1092493af067646fc5f3db9421c6a6ec9c938   --source-digest 0cf1092493af067646fc5f3db9421c6a6ec9c938   --source-ref refs/heads/trunk --deny-self-hosted-runners --format json
```

The full executed argument vector with absolute file paths is saved as
`offline-command.json`. Valid offline check returned 0. Changing repository to
`wrong/repository` returned 1 with a repository-owner mismatch; changing the exact
certificate workflow identity to `wrong.yml` returned 1. These are real negative
policy tests, not evidence that merely parsing options enforces identity.

**Correction to prior command template:** initial probing combined `--cert-identity`
with `--signer-workflow`; CLI 2.101.0 rejected that combination as mutually exclusive
before verification. The successful policy uses exact `--cert-identity` alone for
workflow SAN, together with repository, issuer, source/signer digest and ref controls.
`--signer-workflow` is a supported alternative, not an additional flag to combine.
The initial failures are not counted as successful negative verification tests;
the corrected negative cases above ran verification. Prior receipts remain unchanged.

## NS-001 readiness and anonymous retrieval boundary

The toolchain supports acquisition of a future signed bundle, local preservation,
local-bundle verification and repository/signer identity enforcement. For NS-001 use
repository `vortexpixelz/ns001`, exact certificate identity
`https://github.com/vortexpixelz/ns001/.github/workflows/ns001-h1-custody.yml@refs/heads/main`,
source/signer commit `ef71e56263da8e4d0dfcd5228795356e38b27998`, ref `refs/heads/main`,
issuer above, and custom predicate type
`https://github.com/vortexpixelz/ns001/predicates/h1-custody/v1`.
The CLI supports `--predicate-type`; the public example tested the default SLSA
predicate, not a nonexistent NS-001 custom attestation. Verify both exact NS-001
subjects and observed identifiers later, with the adopted preservation requirements.
Do not combine mutually exclusive identity flags or confuse file SHA-256 with Git SHA.

The prior anonymous-API 401 is not a blocker to the adopted local-bundle route.
An authorized operator may obtain the future bundle through authenticated access,
then preserve complete material and trusted-root provenance as commit-pinned ordinary
repository content for independent retrieval. The offline public test demonstrates
verification without API availability or credentials once adequate bytes are held.
It does not prove future NS-001 signing, acquisition or anonymous deposit retrieval;
those remain future observed gates. No NS-001 attestation lookup/verification test
was used as the public example, and no NS-001 signature was created.

## Preservation and closing verdicts

Before commit, compare original tracked hashes and remote main/settings/releases/
tags/runs with baseline. Main stays `ef71e56263da8e4d0dfcd5228795356e38b27998`;
custody workflow SHA-256 stays
`236b8f30a27fa1c3c26f134c794f2e3e989b9b31d1e3adfbcfae18e21fa420bf`.
NS-001 releases/tags remain empty and four pre-existing runs remain unchanged.
No creation/dispatch/settings mutation was issued. Only this receipt is added;
no scientific artifact, prior receipt, mandate or evidence-deposit object changed.

- Previous gh version: 2.45.0, system package unchanged.
- Selected gh version: 2.101.0, official release.
- Selected gh binary/path: `/home/jacob/.local/opt/ns001-gh/2.101.0/gh`.
- Installation provenance/checksum verdict: VERIFIED official checksum/API digest;
  public signed release and artifact verification passed, with bootstrap assumptions.
- gh attestation command verdict: PASS, all required command surfaces available.
- Trusted-root verdict: PASS retrieval, TUF verification and actual offline use.
- Public verification test verdict: PASS release, release-asset and generic attestation.
- Local-bundle verification verdict: PASS with external networking disabled and no
  CLI credentials; complete saved roots/bundle used.
- Signer/repository constraint verdict: PASS exact identity policy; wrong repository
  and signer rejected; prior incompatible flag combination corrected here.
- Anonymous-API dependency verdict: NOT REQUIRED for later verification of preserved
  complete bundles; future acquisition and external deposit still must succeed.
- NS-001 attestation-toolchain-ready: YES for this bounded capability requirement,
  using the absolute pinned binary and corrected policy syntax.
- Publication authorization: NO. Workflow dispatch remains unauthorized.
- H2A1: local identity VERIFIED; external auditability PARTIAL; all eight substantive
  H2 gates unresolved. Tool capability is not publication or evidence-gate closure.
- E0: HOLD; Gate 1 PARTIAL.
- H2A2: UNSTARTED.
- One next bounded action: separately authorize a final read-only readiness recheck
  incorporating this validated toolchain and corrected command syntax; do not publish
  or dispatch as part of that recheck.
