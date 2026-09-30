# NS-001 H2A2 real CPython engine provenance review v0.1

Review date: 2026-09-30 (America/New_York).
HEAD before: `580b2392de3103953790f772e4757186418aaf39`.
Branch: `codex/e0-h2-preparation`; preflight working tree clean.

## Scope and verdict

**Engine-provenance verdict: ENGINE_PROVENANCE_QUALIFIED.**
This verdict qualifies only the acquisition/package/source/build origin and on-disk
identity of the exact candidate compiler-bearing image. It does not qualify a running
receiver, observer, callable/ABI decoder, loader/interposition measurement or experiment.
Real-boundary qualification remains NOT_QUALIFIABLE pending independent native observer
and live engine/callable association qualification. Implementation remains unauthorized.

Authority is the existing real input-boundary specification, sections 3 and 6:
`NS-001_H2A2_REAL_CPYTHON_INPUT_BOUNDARY_SPEC_v0.1.md`, SHA-256
`eae004d95046d2c2a83fd7813f4b0485ce792e358403a406859280f4c0fdc564`.
The preceding engine/observer review is unchanged, SHA-256
`289d9b8dfb45fe518e4da33ef15bf3c9f26fa26c42ca6082b6276c8d3ce39865`.
Its historical refusal remains valid for the evidence then retained. This additive
review discharges its engine-origin gap only; static builtin_compile coordinates and
all completed slices are preserved. No full H2 gate is promoted to passed.

This single document is the durable review receipt. Downloaded package/source/build
reference bytes and check manifests reside only in `/tmp/ns001-engine-review`; none
are installed, built, executed, or added to the repository. This document retains
origins, digests, checked relationships and limits; it is not a durable binary evidence
store or a frozen running-process descriptor E. Later observation must independently
freeze and validate its expected artifacts before any authorized invocation.

## 1. Installed-file identity and package-database identity

`dpkg-query -S /usr/bin/python3.12` returned `python3.12-minimal`.
Exact installed identity: `python3.12-minimal:amd64`, version
`3.12.3-1ubuntu0.17`, architecture `amd64`, source `python3.12`, source version
`3.12.3-1ubuntu0.17`, status `install ok installed`. Package control in the downloaded
.deb independently agrees with package/version/architecture/source.

Package database location is `/var/lib/dpkg`; evidence at review time:

| File | SHA-256 |
| --- | --- |
| `/var/lib/dpkg/status` | `8817657060abbc7bd517f7479046ef57d9b289b99aa6142b200a4c7c313f33fb` |
| `/var/lib/dpkg/info/python3.12-minimal.list` | `5a7081310b979fce51b7d2b5e3c97052321337ae0fdb9214489b14fbd5a84e16` |
| `/var/lib/dpkg/info/python3.12-minimal.md5sums` | `8d01dbbae07eec0273ec02c0d5e6f7a6bc6ab5f3065979a15f9e7c2bf2a37e18` |

Candidate executable SHA-256:
`e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f`.
ELF64 x86-64; file size 8,020,928 bytes; build ID
`337d65cf00021797985cc9f77c0cc334a9fbeb38`. Build ID is corroboration, not a byte pin.
Local MD5 `889a058bf0c9cf12e239a83a59a405d0` matches dpkg's file manifest, but this
weak local checksum is not the authentication basis.

## 2. Authenticated repository/package provenance and payload binding

Verification used `gpgv --status-fd 1 --keyring
/usr/share/keyrings/ubuntu-archive-keyring.gpg` on the cached security InRelease.
It returned a good signature and VALIDSIG for Ubuntu Archive Automatic Signing Key
(2018), full fingerprint `F6ECB3762474EDA9D21B7022871920D1991BC93C`.
Trust is rooted in this pre-existing Ubuntu archive keyring under the stated trusted
host/tooling assumption; its independent original enrollment was not reconstructed.
This scoped repository authentication does not resolve NS-001 external_trust_root.

| Evidence | Identity/check |
| --- | --- |
| Keyring SHA-256 | `80a36b0a6de2f69f49d2df75ef473ccde121e9e190b9ea01d20a4f63778d5c31` |
| InRelease origin | `https://security.ubuntu.com/ubuntu/dists/noble-security/InRelease` |
| Cached InRelease SHA-256 | `8afc11ef323263b203996af26549b7930fecd748be628cbc993d9f3de5a944d6` |
| Release fields | Suite noble-security; Codename noble; Date Wed, 30 Sep 2026 12:52:12 UTC; signature 12:52:56 UTC |
| Signed main/binary-amd64/Packages | size 5,797,350; SHA-256 `e34b36f1a53b33ae9604a0ed12f7e2465bc42a1473edf2bde3ce4cbf93d765d8` |
| Actual cached Packages | exact SHA-256 and size agreement with signed release |
| Package filename | `pool/main/p/python3.12/python3.12-minimal_3.12.3-1ubuntu0.17_amd64.deb` |
| Package size | 2,334,634 bytes |
| Signed-index package SHA-256 | `d452689b9660845345a4c3e05e4ad82c082d5474e04031b7aa47f1a6d5610a6e` |

The package was fetched read-only from
[Ubuntu security archive](https://security.ubuntu.com/ubuntu/pool/main/p/python3.12/python3.12-minimal_3.12.3-1ubuntu0.17_amd64.deb).
Its SHA-256 exactly equals the signed-index pin. `dpkg-deb --fsys-tarfile` and
`tar -xOf` streamed only `./usr/bin/python3.12` to `sha256sum`; the resulting SHA-256
exactly equals both the installed executable and the user-supplied pin above.
Thus the exact installed executable bytes are bound to an authenticated Ubuntu
archive package payload, independently of dpkg's local version label and MD5.

Chain: pre-existing trusted Ubuntu key -> verified InRelease -> SHA-256 Packages ->
SHA-256 .deb -> extracted executable SHA-256 -> measured installed executable.
No detached .deb signature is claimed or required for this archive authentication
model. The release's date is retained; no stronger historical installation custody,
rollback protection or continuing freshness guarantee is inferred.

## 3. Source package and build provenance

The same verified InRelease binds `main/source/Sources.xz`, size 288,896,
SHA-256 `5dc4aae8b6f5a477aa3f074a2a6dde9dffd29c90408b19998720bd74fae7e8a7`.
A read-only download from the security archive matched that hash. Its exact source
stanza is `python3.12`, version `3.12.3-1ubuntu0.17`, directory
`pool/main/p/python3.12`. All three downloaded source objects matched the stanza:

| Source object | Size | SHA-256 |
| --- | --- | --- |
| `python3.12_3.12.3-1ubuntu0.17.dsc` | 3,916 | `941700b999737d869b80c3b5a0adc0996a0fd760b982e18551bd2104da779384` |
| `python3.12_3.12.3.orig.tar.xz` | 20,625,068 | `56bfef1fdfc1221ce6720e43a661e3eb41785dd914ce99698d8c7896af4bdaa1` |
| `python3.12_3.12.3-1ubuntu0.17.debian.tar.xz` | 302,472 | `17b15629cb10825924cf7b85055255080ec773133ae0f8b8ce5ea2eec90dd200` |

Their canonical URLs are under
[Ubuntu source pool](https://security.ubuntu.com/ubuntu/pool/main/p/python3.12/).
The .dsc contains a PGP signature; its uploader signature was not separately verified.
Authentication instead follows the verified archive release/source-index hashes.
Upstream 3.12.3 alone is not the complete Ubuntu source: the Debian patch archive and
series are part of the exact source identity.

[Launchpad primary source publication 18725224](https://api.launchpad.net/1.0/ubuntu/+archive/primary/+sourcepub/18725224)
reports Published/Security, version `3.12.3-1ubuntu0.17`, published
2026-09-10T09:46:29.390018+00:00. Updates publication 18725624 reports the same
version, published 2026-09-10T12:29:16.614464+00:00. The Security publication's
`getBuilds` response directly associates the source with
[amd64 build 33562858](https://launchpad.net/~ubuntu-security-proposed/+archive/ubuntu/ppa/+build/33562858),
Successfully built, completed 2026-09-02T14:00:41.454756+00:00.
Its security-proposed PPA build location is a build origin, not an assertion that the
installed package came from an unauthenticated PPA: the final binary digest is independently
bound to Ubuntu's signed primary noble-security index.

The build's published files share the URL prefix
`https://launchpad.net/~ubuntu-security-proposed/+archive/ubuntu/ppa/+build/33562858/+files/`:

| Published build file | SHA-256 |
| --- | --- |
| `python3.12_3.12.3-1ubuntu0.17_amd64.changes` | `73e3df321e67334f87d0e447af3be884f6b253daf03a5c15704a18e3e033d06e` |
| `python3.12_3.12.3-1ubuntu0.17_amd64.buildinfo` | `febad4e4afc3376305c8eae79567db3e443a6f70b6f6d2154ab975e35ca0730c` |
| `buildlog_ubuntu-noble-amd64.python3.12_3.12.3-1ubuntu0.17_BUILDING.txt.gz` | `96701831e8ca7f0b75b2044d6b463abead8a10152d77bd9a115da751fced0638` |

Both .changes and .buildinfo list the exact .deb SHA-256
`d452689b9660845345a4c3e05e4ad82c082d5474e04031b7aa47f1a6d5610a6e` and size
2,334,634. The .changes also binds the .buildinfo hash/size 14,133. These downloaded
build files are not PGP-signed; their provenance is the authoritative HTTPS Launchpad
build/publication relationship, with independently authenticated package/source hashes.
The log is build-service evidence, not a cryptographic proof of compiler behavior.

## 4. Compiler/configuration and version-matched interface evidence

Buildinfo records Build-Origin Ubuntu, Build-Architecture amd64, version
`3.12.3-1ubuntu0.17`, Build-Date Wed, 02 Sep 2026 13:59:06 +0000,
Build-Path `/build/python3.12-PWfLPC/python3.12-3.12.3`, GCC packages
`gcc-13`, `gcc-13-x86-64-linux-gnu`, `gcc-13-base` at
`13.3.0-6ubuntu2~24.04.1`, DEB_BUILD_OPTIONS parallel=8,
DEB_BUILD_PROFILES noudeb and SOURCE_DATE_EPOCH 1788171506.
Build-Tainted-By explicitly includes `merged-usr-via-aliased-dirs` and
`usr-local-has-programs`; neither is concealed or converted into a reproducibility claim.

The build log identifies a build-static configuration for the executable, distinct
from the separate shared build. It records x86_64-linux-gnu-gcc, system expat,
computed gotos, dtrace, without ensurepip and the platform/library paths. The
bltinmodule.o commands record -O3, -DNDEBUG, frame pointers, hidden visibility,
FORTIFY_SOURCE=3, stack/clash protection and profile-generate followed by
profile-use/profile-correction. Link flags include -flto/fuse-linker-plugin;
configure's standalone with-lto check says no, so a blanket LTO-disabled claim would
be misleading. The complete flags are available in the hash-pinned log.
Local executable strings corroborate 3.12.3, Aug 31 2026 and GCC 13.3.0; no version
command or Python launch was performed. Installed shared-build Makefile metadata is
corroboration only and does not override the executable's static compiler-image role.

Read-only source text extraction identified:
`Python-3.12.3/Python/bltinmodule.c`, SHA-256
`e1acb65d489050a47681a932fd53ead498a7966c1e672605b64fc030d740c9a2`, and
`Python-3.12.3/Python/clinic/bltinmodule.c.h`, SHA-256
`5d250c78ef6d6f943a6501ec587557d6718e136934630b0d1eeca8c461a385dd`.
The clinic declaration has source, filename, mode, flags=0, dont_inherit=False,
optimize=-1 and keyword-only _feature_version=-1. Generated native entry is
`builtin_compile(PyObject *module, PyObject *const *args, Py_ssize_t nargs,
PyObject *kwnames)` before argument unpacking/conversion. A text search of all
Ubuntu packaging patches found no bltinmodule path, builtin_compile or
_feature_version changes. This supplies version-matched interface provenance;
it is not live argument decoding or observer qualification.

## 5. Native image provenance

For this candidate, the native compiler-bearing image is `/usr/bin/python3.12`
itself, with the authenticated executable hash above. ELF DT_NEEDED contains libm,
libz, libexpat and libc and no libpython. PT_INTERP is
`/lib64/ld-linux-x86-64.so.2`. Existing static builtin_compile identification at
VA 0x69bff0/file offset 0x29bff0 remains unchanged; no probe is attached.

The companion installed `/usr/lib/x86_64-linux-gnu/libpython3.12.so.1.0` belongs to
`libpython3.12t64:amd64`, installed version/source version `3.12.3-1ubuntu0.17`,
source python3.12, status install ok installed. Its SHA-256 is
`1021f236227334ded6d1bbbc4bb6f5d933f793d8397c969896cfbdf03ce96223`.
The same signed Packages index binds its .deb, size 2,348,034, SHA-256
`0d29f4763eb95b8a4283a4aca3ef1d9658629c618be1778def41bdc31be12b46`.
A read-only archive download matched that package digest; streamed .so payload
matched the installed shared-image digest. Buildinfo/changes associate that package
with the same source/build. This is inventory provenance, not the selected receiver
or permission to use a different compiler image. Native library closure and loader
interposition qualification remain outside this engine-origin circuit.

## 6. Local mutation, reproducibility and sufficiency

At measurement time, the full installed executable bytes equal the authenticated
archive payload. A present byte modification is excluded conditional on honest
hashing/read tools, archive trust and host/kernel observations. Historical
modify-and-restore, future mutation, concurrent hostile mutation, actual mapped
process bytes and loader/interposition effects are not excluded. File ownership
was nobody:nogroup, mode 0755; local ownership is not authenticated by payload hashes
and is not treated as immutable installation custody. This review authenticates
present bytes, not the historical installation transaction or a future process.

Reproducibility: **not independently demonstrated**. Buildinfo, compiler versions,
source/patch hashes, configuration and log are available; no rebuild or build-tool
execution was performed. Full reproducible-build proof is unnecessary for the narrow
claim that these exact bytes are the Ubuntu-published compiler-bearing image from
this declared source/build. Ubuntu archive/build-service honesty is an explicit
residual assumption, not mathematically verified source-to-binary equivalence.

Sufficiency is confined to provenance components of specification section 3(1)-(2):
exact local compiler image, authenticated reference acquisition, source/build origin,
platform and version-matched interface. No engine-provenance gap remains within
that scope. Section 3(3)-(5), runtime loaded-image association, target association,
bootstrap/observer identity, ABI semantics and actual receiving evidence remain
separately unqualified. The native image pin can be an expected reference in a later
independently reviewed qualification; this document does not itself instantiate E.

## 7. Preservation and administrative operation receipt

Preflight matched the requested branch/HEAD and clean tree. All 216 pre-existing
tracked files were hashed before work and checked unchanged before commit,
including H2A1, both completed H2A2 slices, code/tests/fixtures/evidence and prior
real-boundary documents. The only repository change is this new document.

Before commit, the executable, companion .so, installed Makefile, dpkg status and
all matching python3.12/libpython3.12 dpkg info-file hashes were compared with the
before-review manifest and were unchanged. Downloads/extractions wrote only to
/tmp. No package installation/update, apt refresh, Python/package modification,
candidate launch, observer attachment, compile/eval/exec/import, source execution,
runtime harness, dependency lock or E0 action occurred in this agent's operation
record. Reading build logs containing historical compiler commands did not execute
those commands. This is a scoped action-log and file-hash verification, not a global
trace of unrelated processes. E0 remains HOLD; no runtime tests were invoked.

Only this path is staged, whitespace/diff scope is checked, and this one document is
committed and pushed to the existing branch. Final commit/push and document digest
are reported outside the document to avoid self-referential hashes.

## Closing record

- candidate engine: CPython 3.12.3, `/usr/bin/python3.12`, ELF64 x86-64.
- installed package identity: python3.12-minimal:amd64 3.12.3-1ubuntu0.17; source python3.12, same version; install ok installed.
- executable hash binding: e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f equals authenticated .deb payload.
- repository provenance: verified Ubuntu noble-security InRelease -> Packages SHA-256 -> exact .deb SHA-256.
- build provenance: signed Sources -> exact .dsc/orig/Ubuntu patch archive; primary publication 18725224 -> amd64 build 33562858; buildinfo/changes exact binary digest match; GCC 13.3.0 build metadata available.
- native image provenance: compiler is authenticated executable; companion libpython3.12t64 shared-image payload independently matches, outside selected receiver role.
- local mutation assessment: current byte identity verified under trusted-host/tooling assumptions; historical/future/live mutation only bounded.
- reproducibility status: not independently demonstrated; unnecessary for this narrow provenance claim.
- residual assumptions: trusted pre-existing Ubuntu archive key enrollment, signature/hash tools and host/kernel; Ubuntu archive/build-service and HTTPS metadata honesty; no claim of hostile-host resistance or historical installation custody.
- engine-provenance verdict: ENGINE_PROVENANCE_QUALIFIED.
- qualification impact: engine-origin gap discharged only; real-boundary qualification remains NOT_QUALIFIABLE; native observer/live association unqualified; no implementation or invocation authorization.
- external_trust_root status: UNRESOLVED.
- dependency_runtime_lock status: UNRESOLVED, not begun.
- H2A1 status: VERIFIED + frozen, unchanged.
- H2A2 status: slice 1 sealed handoff VERIFIED; slice 2 synthetic consumption VERIFIED WITH RESIDUAL ASSUMPTION; both frozen unchanged; real boundary statically identified only.
- E0 status: HOLD.
- one next bounded action only: separately authorize one document-only native observer qualification design for this exact authenticated image, with no attachment or runtime invocation. Not performed here.
