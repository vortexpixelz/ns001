# NS-001 H2A1 platform-attestation credential-free review v0.1

## Scope, starting state and result

Preparation branch `codex/e0-h2-preparation`; HEAD before `dd3796dd137efef3de8816ece856a768ea6c2829`;
working tree initially clean. Review completed at 2026-09-25T10:22:36.088455+00:00.
Resumed the existing circuit at `/tmp/ns001-platform-review-location`, pointing to
`/tmp/ns001-platform-clean-8tk02n4s`. The already-started clean build completed successfully (exit 0).
Completed anonymous downloads were reused; no retrieval was restarted on continuation.
Only this receipt is added to repository content. No release, assets, workflows,
settings, attestations or scientific artifacts were changed. No E0 or H2A2 work.

**Remaining credential-free platform-verification gap: CLOSED.** An independent reviewer
can verify the preserved raw platform attestation without a GitHub login, stored token,
credential helper, Jacob's configuration, workflow logs or Actions caches/artifacts.
The official, unmodified sigstore-go v1.3.0 verification example was built from public
source with fresh public Go tooling and clean module/build caches. Both freshly downloaded
release assets passed offline verification against the anonymously downloaded committed
bundle and roots. Verification used new empty HOME/GH_CONFIG_DIR/cache paths and
`unshare -Urn`, disabling external networking. All expected signed bindings matched;
wrong bytes, signer, repository expectation, tag expectation and commit expectation failed.

H2A1 external auditability is **VERIFIED for the bounded prospective custody/publication
claim**, combining this last gap closure with the preserved prior retrieval/completeness
review. This does not establish historical custody, institutional authority, scientific
validity or close the eight substantive H2 scientific/engineering gates. E0 remains HOLD,
H2A2 UNSTARTED, Gate 1 PARTIAL. Accepted public-hosting/deletion assumptions still apply.

## Inputs and independently obtainable tooling

Every verification input below was publicly retrieved during this same circuit, before
continuation, or derived losslessly from those bytes. No unpublished local input was used.
All repository paths are pinned at `dd3796dd137efef3de8816ece856a768ea6c2829`.
Evidence base: `docs/e0/h2/evidence/ns001-h1-audit-v1-publication-stop-20260924/`.
Raw URL construction:
`https://raw.githubusercontent.com/vortexpixelz/ns001/dd3796dd137efef3de8816ece856a768ea6c2829/PATH`.

| Input | Location / provenance | SHA-256 |
| --- | --- | --- |
| Platform bundle | automatic-release-verification/release-attestation.bundle.json under evidence base | `d7b5d658b2e204e6360d87512da9a1d21c68360642c976590c6e2eda49092f93` |
| Complete preserved roots | attestation-verification/trusted_root.jsonl under evidence base | `65ca537f6ed8a47fd0e560c421baa1f6c1efb8b25fc200d8c5c02c0e92eb2b9c` |
| GitHub-only root used | Exact original JSONL line whose certificateAuthorities all identify fulcio.githubapp.com; no reserialization | `26b3382d5700afbcd84f980d1d5b6c52bff743dc2a8ee86b8b44c8e1245ce485` |
| ZIP | Public release download NS001_H1_AUDIT_BUNDLE_20260903.zip, 51103 bytes | `a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f` |
| Provenance | Public release download NS001_H1_PUBLICATION_PROVENANCE.json, 2298 bytes | `ff649229275d88be762e2b762b35b27c3aac8e252a070ac39b18bffc06142d12` |
| Fresh gh executable | Official v2.101.0 linux_amd64 archive; original archive hash 9bca2d1c16825f109907a23307628a2f0698fbf99662b73a5cf0b020293072b8 | `ea857a3f0f7d4276cf5848b236542c5048e2eaa7bdd1b6ddec238f8793e74bff` |
| Go archive | https://go.dev/dl/go1.27.1.linux-amd64.tar.gz ; matched official go.dev download metadata | `63d339f0da5ab53635a56f2490a7984dfe12dfcff22ad749f63edaf590168445` |
| sigstore-go v1.3.0 source archive | https://codeload.github.com/sigstore/sigstore-go/tar.gz/refs/tags/v1.3.0 | `54899c8c6fac035974a45218b6710c08dc310cbcd673e3f7c4a65744748ea4f3` |
| Official example source | examples/sigstore-go-verification/main.go from that source | `e06721fccf708a8c04e8b1baa2f1ced4bdf2a4671d37ec2f2619649fb3d2920c` |
| Module definition | sigstore-go v1.3.0 go.mod | `3d9d44920dd7e31996289ba337463d8b7f9314bbbc6fa92655914df0d74e4db7` |
| Module dependency checksums | sigstore-go v1.3.0 go.sum | `ba844dcff1068b5ee609eb39bc43d1b22cc802b080ca14e371d93a07fb1dbc36` |
| Built example executable | Fresh build, Go go1.27.1, linux/amd64, -mod=readonly -trimpath | `cb2c816415c9fa6cf724d0c2ace914886f98f3de8c8a307ae72561eb435789ee` |

Public asset URL prefix:
`https://github.com/vortexpixelz/ns001/releases/download/ns001-h1-audit-v1/`.
The fresh gh binary matches the previously pinned verifier; Jacob's installed binary
was not used for the actual clean verification tests. Its local path was only the
initial toolchain reference/help surface. Fresh configuration paths contained no login.
Go used GOPROXY=https://proxy.golang.org and GOSUMDB=sum.golang.org, isolated GOPATH/GOCACHE,
GOTOOLCHAIN=local and -mod=readonly; official source and dependency locks were not edited.

Trust bootstrap remains official HTTPS verifier/tool distribution and the authenticated
TUF root provenance documented in the committed toolchain/final completeness receipts.
The earlier final-completeness circuit independently obtained matching roots using fresh
public tooling and empty configuration/cache. This continuation did not repeat that
retrieval. Roots are not trusted merely because they accompany a bundle; reviewers can
reproduce the documented public TUF acquisition independently. Root bytes and authorities
contain no private account state. No trust bypass or credential injection was used.

## Convenience command and generic gh results

The preceding clean stage, retained in this circuit's temporary gh-checks.json, ran the
fresh gh with minimal environment, empty GH_CONFIG_DIR and `unshare -Urn`:

| Command family | Exit | Finding |
| --- | ---: | --- |
| gh release verify ns001-h1-audit-v1 -R vortexpixelz/ns001 --format json | 4 | CLI login guard; no cryptographic verdict. |
| gh release verify-asset ns001-h1-audit-v1 ZIP -R vortexpixelz/ns001 --format json | 4 | Same login guard. |
| gh attestation verify ZIP --bundle BUNDLE --custom-trusted-root ROOTS --repo vortexpixelz/ns001 --cert-identity https://dotcom.releases.github.com --predicate-type https://in-toto.io/attestation/release/v0.2 --format json | 1 | expected SourceRepositoryOwnerURI to be https://github.com/vortexpixelz, got empty. |

The automatic platform certificate is not a GitHub Actions workflow certificate and
has no Actions source-repository extensions. Generic gh attestation policy therefore
cannot verify it under its required repository extension policy. No unsupported flag
was invented to bypass this check. Convenience-command authentication is not a limitation
of the signed bundle or its underlying cryptographic verification library.

## Cryptographic policy and its limits

The pinned gh v2.101.0 go.mod uses sigstore-go v1.3.0. Official implementation references:

- https://github.com/cli/cli/blob/v2.101.0/pkg/cmd/release/shared/attestation.go
- https://github.com/cli/cli/blob/v2.101.0/pkg/cmd/attestation/verification/sigstore.go
- https://github.com/sigstore/sigstore-go/blob/v1.3.0/examples/sigstore-go-verification/main.go

The platform gh policy uses GitHub trust material, a signed RFC3161 timestamp, the release
SAN `https://dotcom.releases.github.com`, issuer-extension wildcard and an artifact digest.
The official example exposes supported flags to require an observer timestamp, constrain
the exact SAN, use the matching issuer-extension wildcard and verify the artifact digest.
CT/Rekor requirements were disabled because the platform policy uses GitHub timestamp
authorities rather than the public Sigstore CT/Rekor route. No identity or artifact check
was disabled; no unsafe WithoutArtifact/WithoutIdentities option was selected.

The example uses WithObserverTimestamps(1), whereas gh's GitHub verifier uses
WithSignedTimestamps(1). For this exact bundle, the only verification timestamp material
is RFC3161; no transparency-log entry exists. The returned verified timestamp is explicitly
required to be TimestampAuthority in the binding check below. Thus the successful evidence
includes the required signed TSA timestamp, not a substituted local wall-clock time.

Certificate chain/signature, DSSE signature, asset digest, platform SAN and timestamp are
cryptographically verified by the library. Repository/tag/release/commit values are
**signed statement content**, not certificate extensions. Equality against the user's
expected values is a separate, fail-closed policy check applied only to successful verifier
output. Reading or base64-decoding an unverified bundle would not satisfy this procedure.
The issuer-extension wildcard is the platform's documented policy, not a fabricated
Actions OIDC issuer; chain validation still uses the trusted GitHub CA material.

## Reproduction from public material

Download the public inputs above and check their hashes. Use a fresh Go toolchain from
the pinned official archive, verify its checksum, then extract the pinned sigstore-go
source and verify archive/source/module hashes. Build the unmodified example in that
source directory with clean HOME, GOPATH and GOCACHE:

```sh
env -i PATH="$GO_BIN:/usr/bin:/bin" HOME="$CLEAN_HOME" GOPATH="$CLEAN_GOPATH" GOCACHE="$CLEAN_GOCACHE" GOPROXY=https://proxy.golang.org GOSUMDB=sum.golang.org GOTOOLCHAIN=local "$GO_BIN/go" build -mod=readonly -trimpath -o "$VERIFIER" ./examples/sigstore-go-verification
```

Paths are reviewer-selected absolute temporary paths, not Jacob-specific prerequisites.
Extract the GitHub root by reading the preserved JSONL as raw lines, selecting the unique
line whose certificateAuthorities URIs are all fulcio.githubapp.com, and writing that
line unchanged. Require the GitHub-root hash above. Preserve the complete JSONL too.
In a new empty configuration/cache and network namespace, run for ZIP and then provenance:

```sh
env -i PATH=/usr/bin:/bin HOME="$EMPTY_HOME" GH_CONFIG_DIR="$EMPTY_GH_CONFIG" XDG_CACHE_HOME="$EMPTY_CACHE" unshare -Urn "$VERIFIER" -artifact "$ASSET" -trustedrootJSONpath "$GITHUB_ROOT" -expectedSAN https://dotcom.releases.github.com -expectedIssuerRegex '.*' -requireTimestamp=true -requireCTlog=false -requireTlog=false -minBundleVersion 0.3 "$BUNDLE" > verified.json
```

Require exit 0 before processing verified.json. All flags above are from the unmodified
official example; they are **not gh flags**. Public build-time dependency acquisition is
separate from offline verification. The example requires no GH_CONFIG_DIR contents at all;
setting an empty one additionally makes the credential boundary explicit.

Run this exact equality policy on that successful JSON output (normal Python, no -O):

```python
import json,sys
# Input must be stdout from a successful, policy-constrained Sigstore verification.
def check(v,repo,tag,commit):
 s=v['statement']; p=s['predicate']; subjects=s['subject']
 assert v['signature']['certificate']['subjectAlternativeName']=='https://dotcom.releases.github.com'
 assert any(t['type']=='TimestampAuthority' for t in v['verifiedTimestamps'])
 assert s['predicateType']=='https://in-toto.io/attestation/release/v0.2'
 assert p['repository']==repo and p['repositoryId']=='1354037143'
 assert p['ownerId']=='202687650' and p['databaseId']=='396003416'
 assert p['tag']==tag
 uri='pkg:github/'+repo+'@'+tag
 assert p['purl']==uri
 assert len(subjects)==3
 assert any(x.get('uri')==uri and x['digest']=={'sha1':commit} for x in subjects)
 expected={'NS001_H1_AUDIT_BUNDLE_20260903.zip':'a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f','NS001_H1_PUBLICATION_PROVENANCE.json':'ff649229275d88be762e2b762b35b27c3aac8e252a070ac39b18bffc06142d12'}
 for name,digest in expected.items():
  assert sum(x.get('name')==name and x['digest']=={'sha256':digest} for x in subjects)==1
if __name__=='__main__':
 check(json.load(open(sys.argv[1])),*sys.argv[2:]);print('Signed bindings match expectations')
```

Example invocation: `python3 check-bindings.py verified.json vortexpixelz/ns001 ns001-h1-audit-v1 d9dcfbef1bea173b316bc968fd71421c982422c3`.
The asserted statement must include exactly the repository/tag URI subject with expected
Git SHA-1 and both named SHA-256 asset subjects, plus expected repository/owner/release IDs.
The two assets are each separately passed to the cryptographic verifier, so this procedure
checks actual local file digests as well as their expected digest strings.

## Observed positive and negative checks

| Check | Exit | Result | stdout SHA-256 | stderr SHA-256 |
| --- | ---: | --- | --- | --- |
| zip | 0 | verification PASS | `2d86911f34527ad7da2008f47de2e5a8514d0793c9b4becb6c8095a5c217525f` | `7b4998adb49b60b21796097dfa104e0b6fc96438d3feee6f375e7dc95695d3f8` |
| provenance | 0 | verification PASS | `2d86911f34527ad7da2008f47de2e5a8514d0793c9b4becb6c8095a5c217525f` | `7b4998adb49b60b21796097dfa104e0b6fc96438d3feee6f375e7dc95695d3f8` |
| altered-asset | 1 | failed to verify signature: provided artifact digests do not match digests in statement | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `68110a35b75b1a992f442cd41c06ecaec81f9ffedee2fb6a637bac727f8efe11` |
| wrong-signer | 1 | failed to verify certificate identity: no matching CertificateIdentity found, last error: expected SAN value "https://wrong.releases.github.com", got "https://dotcom.releases.github.com" | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `f5c0ef67acb61472e4b459a76548405bf159fbc57fa167579dd1b4c4c7253649` |

Altered asset was a temporary ZIP copy with literal bytes `negative` appended; originals
were unchanged. Wrong signer changed only expectedSAN to https://wrong.releases.github.com.
Both negatives exercised the cryptographic verifier and failed. No network access was
possible inside the user/network namespace, and no token/credential variables were supplied.

Separate signed-content equality checks, applied to the successful ZIP verification output:

| Expectation | Exit | Meaning |
| --- | ---: | --- |
| Correct repository/tag/commit/assets | 0 | All expected signed values match. |
| Repository wrong/repository | 1 | Signed repository/purl binding does not match expectation. |
| Tag wrong-tag | 1 | Signed tag does not match expectation. |
| Commit 0000000000000000000000000000000000000000 | 1 | Signed URI subject SHA-1 does not match expectation. |

These last three negatives do not pretend that a repository/tag is a certificate field.
The signature remains valid, but the combined verification-and-expectation policy rejects
the wrong expectation. No re-signing or alteration of the bundle was used.

The complete successful verification result is included here so this receipt does not
rely on temporary output files. Both assets produced the same statement and identity:

```json
{
  "mediaType": "application/vnd.dev.sigstore.verificationresult+json;version=0.1",
  "signature": {
    "certificate": {
      "certificateIssuer": "CN=Fulcio Intermediate l1,O=GitHub\\, Inc.",
      "subjectAlternativeName": "https://dotcom.releases.github.com"
    }
  },
  "verifiedTimestamps": [
    {
      "type": "TimestampAuthority",
      "uri": "timestamp.githubapp.com",
      "timestamp": "2026-09-24T19:52:11Z"
    }
  ],
  "verifiedIdentity": {
    "subjectAlternativeName": {
      "subjectAlternativeName": "https://dotcom.releases.github.com"
    },
    "issuer": {
      "issuer": "",
      "regexp": ".*"
    }
  },
  "statement": {
    "_type": "https://in-toto.io/Statement/v1",
    "subject": [
      {
        "uri": "pkg:github/vortexpixelz/ns001@ns001-h1-audit-v1",
        "digest": {
          "sha1": "d9dcfbef1bea173b316bc968fd71421c982422c3"
        }
      },
      {
        "name": "NS001_H1_AUDIT_BUNDLE_20260903.zip",
        "digest": {
          "sha256": "a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f"
        }
      },
      {
        "name": "NS001_H1_PUBLICATION_PROVENANCE.json",
        "digest": {
          "sha256": "ff649229275d88be762e2b762b35b27c3aac8e252a070ac39b18bffc06142d12"
        }
      }
    ],
    "predicateType": "https://in-toto.io/attestation/release/v0.2",
    "predicate": {
      "databaseId": "396003416",
      "ownerId": "202687650",
      "packageId": "1354037143",
      "purl": "pkg:github/vortexpixelz/ns001@ns001-h1-audit-v1",
      "repository": "vortexpixelz/ns001",
      "repositoryId": "1354037143",
      "tag": "ns001-h1-audit-v1"
    }
  }
}
```

## Interpretation and closing verdicts

The publicly attributable signer is GitHub's platform release identity, not the custom
custody workflow. It signs release predicate v0.2 with repository vortexpixelz/ns001,
release 396003416, tag ns001-h1-audit-v1 and a pkg:github URI subject whose SHA-1 is
publication target d9dcfbef1bea173b316bc968fd71421c982422c3. Both asset SHA-256 values
match the frozen expected values and fresh anonymous release bytes. This is a platform
publication binding, not proof of original creation, pre-publication custody, authorship,
corporate authority, project mandate endorsement or scientific validity. Prior scoped
self-declared maintainer authority and historical limitations remain unchanged.

The earlier immutable-release material/results absence was already closed by the prior
commit. This review closes its remaining credential-free cryptographic reproduction gap.
Previous PARTIAL receipts remain accurate stage records and are not rewritten. All prior
committed evidence is unchanged. Full-commit material availability and public toolchain
availability remain ordinary accepted retention/bootstrap assumptions; no perpetual
availability or supply-chain infallibility claim is made.

- Clean-environment verdict: PASS; fresh public tooling, minimal environment, empty GH_CONFIG_DIR/HOME/cache, offline verification in unshare -Urn.
- gh release verify credential requirement: YES, login guard in CLI 2.101.0; verify-asset also requires login in this tested invocation. These wrappers are not required by the raw-bundle route.
- Raw/bundle verification verdict: PASS, both assets, official unmodified sigstore-go v1.3.0 example. Generic gh attestation --bundle is incompatible with missing Actions extensions.
- Repository binding verdict: PASS through equality checks on cryptographically verified signed repository/IDs/purl; not an Actions certificate-extension claim.
- Tag/commit binding verdict: PASS; signed tag/purl and URI subject SHA-1 match frozen expectations; wrong tag and commit rejected by policy.
- Asset-digest binding verdict: PASS; both local asset digests verified cryptographically and both named signed subjects equal expected SHA-256 values.
- Negative-check verdict: PASS; altered asset, wrong signer, wrong repository, wrong tag and wrong commit rejected at their stated layers.
- Trusted-root verdict: PASS using publicly preserved roots with previously independently checked public TUF provenance; GitHub root selected losslessly. No private-state root required.
- Anonymous API dependency: NO for verification once public commit-pinned bundle/roots/assets are held. Current attestation API access is unnecessary; public repository/release/tool availability is a separate acquisition assumption.
- Local credential dependency: NONE for the successful raw-bundle route. No existing gh login, credential helper, home configuration, workflow log or Actions artifact/cache used.
- Remaining gap: **CLOSED**.
- H2A1 external auditability: **VERIFIED**, scoped to the accepted prospective custody/publication claim; no substantive scientific/engineering gate promotion.
- E0 status: **HOLD**; Gate 1 remains PARTIAL.
- H2A2 status: **UNSTARTED**.
- One next bounded action only: obtain separate authorization for a read-only H2A2 readiness/scope review. Do not begin H2A2 or execute E0. Not performed here.
