# NS-001 H2A1 external authority/custody specification v0.1

## Scope, evidence and claim classes

Branch: `codex/e0-h2-preparation`. HEAD before:
`6268d4f46f0851924464eb23ef8baaafae4619a3`. Review date: 2026-09-21 UTC.
Initial tree was clean. This is a proposed evidence standard and route comparison,
not a publication package, gate implementation, or gate decision. The sole new
repository artifact is this receipt. Its authorized commit/push is distinct from
publishing the ZIP or creating an archive, release, tag, DOI, or custody object.

Classification key used throughout: **R = REPOSITORY-DERIVED** (including retained
project archive bytes); **E = EXTERNAL-SOURCE-DERIVED**; **L = MATHEMATICAL / LOGICAL
CONSEQUENCE**; **P = POLICY / SPECIFICATION CHOICE**; **U = UNSUPPORTED**;
**N = NEEDS ADDITIONAL SOURCE CHECK**. Labels apply to each paragraph/table row
unless a narrower label is given. Recommendations and PASS rules are P, not
claims that the governing H2A0 contract already mandates this particular design.

R: Governing records read: `H2_EVIDENCE_CONTRACT_DRAFT.md`, original H2A1
verification/observation records, reconciliation receipt, and
`NS-001_H2A1_EXTERNAL_ANCHORS_REVERIFY_v0.1.md`. H2A0 distinguishes declarations
from authority/content/custody verification and disallows reuse of one canonical
byte identity across distinct requirement slots in a gate. This specification
must not be mistaken for those later verifiers or their evidence.

## Exact retained object and existing claims

R: Fresh direct read of the non-Git retained object establishes:

- Path: `/home/jacob/Documents/NS-001/audit/2026-09-03/NS001_H1_AUDIT_BUNDLE_20260903.zip`
- Filename: `NS001_H1_AUDIT_BUNDLE_20260903.zip`
- Byte length: **51,103**
- SHA-256: **`a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`**
- ZIP member prefix: `NS001_H1_AUDIT_BUNDLE_20260903/`.

R: Within that prefix, `MANIFEST.json` declares schema
`ns001.h1.external-audit-manifest.v1`, status `H1_MOCK_ONLY_HOLD`, nine payload
entries, and base `0393315223df8ed90f20f0c821508cc98bea08d1` to H1
`6e33cb9ca7019e50e2f247ade9ae8c9a7b40d3ff`. `SHA256SUMS.txt` declares coverage of
all members except itself; the manifest excludes itself and that checksum file.
The outer ZIP digest is pinned in H2A0 and the H2A1 observations/receipts, not by
a self-hash embedded inside the ZIP.

R: `SOURCE_VERSION.json` and `CHECKPOINT_RECEIPT.md` claim local source repository
`/home/jacob/Documents/NS-001/repo`, branch `codex/e0-getdata-hardening`, H1 tree
`f15c46c605b48c0eaac97943cb02e65c05e72031`, clean packaging checkout, creation
`2026-09-03T13:44:53+00:00`, no packaging network access, and no tests run during
packaging. The checkpoint receipt labels the 37-test result as reported, not
reproduced during packaging. These statements were read, not independently
historically authenticated. The preceding re-verification receipt records source
and patch correspondence; this circuit does not rerun those tests or promote
that correspondence to proof of packaging history.

L: Matching bytes cannot authenticate their narrator. The internal creation time
is not an external timestamp. A new authenticated deposit could establish custody
from deposit onward, and attributable assertions about earlier history. It cannot
prove the September 3 creation event or uninterrupted intervening custody without
additional contemporaneous evidence. Such a historical-proof claim is U today.

## Four minimum PASS criteria, fixed before route evaluation

P: These criteria apply to the exact ZIP and a **prospective, explicitly bounded
publication/custody claim**. They do not demand scientific endorsement by an
archive. Failure to satisfy any required component prevents overall PASS; PARTIAL
means relevant evidence exists but is insufficient, and FAIL means the specified
property is not demonstrated. FAIL here need not mean technical impossibility.

| Property | Minimum PASS criterion (P) | Insufficient evidence (L) |
| --- | --- | --- |
| A. BYTE IDENTITY | An independent reviewer downloads the actual ZIP and recomputes 51,103 bytes and the pinned SHA-256 above, comparing with a preserved pre-publication identifier and an externally authenticated publication binding. Retain the downloaded-byte result and exact version/object identifier. | Filename, extracted-file equivalence, regenerated ZIP, sidecar alone, or service digest without reading the bytes. |
| B. RETRIEVABILITY | Anonymous retrieval from an identified external service, without the local machine or private repository state, succeeds for the exact version; record stable locator, object ID, retrieval UTC time and result. Preserve an addressable evidence record and state retention/deletion policy. | A DOI landing page alone, local path, expiring URL as sole locator, access-dependent draft, or promise of permanent availability. |
| C. AUTHORITY / ATTRIBUTION | The publication and provenance statement bind to an identifiable publisher account/organization whose identity and relationship to NS-001 are independently authenticated by a service, an independently anchored signing identity, or institution. Pin stable account/repository IDs and the scope of authority being accepted before publication. | A name/ORCID typed into metadata, Git author text, a key distributed only inside the ZIP, or a repository README asserting its own authority. |
| D. CUSTODY / PROVENANCE | A durable, externally verifiable deposit record binds exact ZIP digest, publisher/depositor identity, destination/version and service-observed time to an authenticated provenance statement. Verify signature/identity/trust chain or equivalent institutional deposit authentication. Independently retrieve and match the deposited bytes; distinguish service time, local observation time and asserted creation time. | Internal manifest/checksums, unsigned local receipt, self-asserted Git timestamp, upload URL alone, or unverified attestation badge. |

P: A GitHub account is an acceptable *account-level* attribution endpoint only if
that scope and its project-control binding are explicitly accepted. It does not
identify a legal person or independent scientific assessor. The external root
must be a service/identity trust anchor obtained outside the ZIP and local repo;
the project may remain the publisher. If “genuinely external” instead requires an
independent institution to endorse the historical claims, none of the evidenced
routes presently meets that stronger requirement. This ambiguity must be resolved
before a later publication PASS, not by changing criteria after upload.

P/L: Minimum custody here is authenticated **deposit onward**, with pre-deposit
history explicitly qualified. A full historical chain remains a separate unmet
claim. No service can turn an unsupported historical assertion into proof merely
by storing it. SHA-256 comparison assumes collision resistance; service identity,
PKI/signing roots, and future retention remain explicitly bounded trust assumptions.

## Candidate comparison: evidence now versus conditional capability

E: Public read-only GitHub API observations on this review date identify
[repository 1354037143](https://api.github.com/repos/vortexpixelz/ns001), public
`vortexpixelz/ns001`, owner account `vortexpixelz` ID `202687650`; the
[releases listing](https://api.github.com/repos/vortexpixelz/ns001/releases?per_page=100)
contains zero releases. This authenticates a platform account/repository mapping
under HTTPS trust, not the identity of a human custodian. No credentials were used.

R/N: Existing project records establish GitHub as an available repository service.
Search of tracked README, docs and preregistrations identified no project Zenodo
record, institutional archive, or project-domain custody facility. These are
comparison classes only; enrollment, authority and availability are unestablished.
The prior re-verification found no ZIP in the inspected remote trees. No new ZIP
location was identified here. Repository push capability does not prove release
administration rights or immutable-release settings.

P: The following are **current evidence grades for this ZIP**, not hypothetical
publication successes. A is FAIL externally even though local byte identity passes.
Authority PARTIAL means the platform/project mapping exists but no qualified ZIP
publication is bound to it. No candidate currently passes all four.

| Route | A | B | C | D | Classification basis |
| --- | --- | --- | --- | --- | --- |
| Ordinary GitHub release asset | FAIL | FAIL | PARTIAL | FAIL | E/R: service exists, no release/asset; publisher binding absent. |
| Repository file at mutable branch URL | FAIL | FAIL | PARTIAL | FAIL | R: no retained ZIP publication evidenced. |
| Exact commit/tree/blob reference containing ZIP | FAIL | FAIL | PARTIAL | FAIL | R/L: source commits exist, but are not the ZIP object. |
| Ordinary tagged release (including signed tag) | FAIL | FAIL | PARTIAL | FAIL | R/N: no ZIP release or independently anchored signing chain evidenced. |
| GitHub immutable release plus verifiable deposit package | FAIL | FAIL | PARTIAL | FAIL | E/N: documented class; project configuration and attestation sufficiency not verified. |
| Zenodo version DOI archive | FAIL | FAIL | FAIL | FAIL | N: no project record/account/deposit evidence. |
| Institutional or project-controlled domain/archive | FAIL | FAIL | FAIL | FAIL | N: no evidenced project facility or independently authenticated custodian. |

P/L: Conditional route evaluation below assumes the exact ZIP can be uploaded in
a later authorized circuit. “Capable” is a design assessment, not a current PASS.

| Route | Conditional capability and exact residual assumption | Mutability risk | Externality risk | Circularity risk |
| --- | --- | --- | --- | --- |
| Ordinary release asset | A/B capable by independent download; C/D PARTIAL without authenticated provenance plus durable event/identity binding. Assume GitHub correctly records uploader/time; stronger authentication still required. | Asset removal/replacement and mutable descriptive metadata. | Hosted externally but same project controls publication. | High if release prose is treated as self-authenticating custody. |
| Branch file | A/B capable for a captured download; version must be pinned to qualify package. C/D PARTIAL without external authentication. | Branch can move; repository availability can end. | Same publisher; storage independence only. | High if branch README authenticates its own contents. |
| Commit/tree/blob | A/B capable with exact ZIP blob, explicit SHA-256 and retained locator. C/D need externally anchored publisher/deposit proof; object identity alone supplies neither. | Byte substitution detectable; refs/repository retention not guaranteed. | Remote copy is not independent historical authority. | High if commit author/time is accepted as proof of depositor/time. |
| Ordinary tagged release | A/B possible for an attached exact ZIP; tag alone supplies no ZIP. C/D need authenticated signer plus external publication time and deposit binding. | Tag can move; signature protects signed object, not continued hosting. | Same publisher and potentially self-issued key. | High if key is trusted solely because the repo contains it. |
| Immutable release with attestations | Best evidenced platform candidate: potentially A–D capable with the full package below. Must check actual attestation subject, signer, timestamp, stable repo identity and uploader/provenance binding; no assumption these are all present. | Documented asset/tag locks reduce substitution; notes remain mutable and hosting is not perpetual. | GitHub can be external service root, not third-party scientific endorsement. | Reduced only by validated external trust chain; otherwise same circularity as ordinary release. |
| Zenodo version DOI | A/B plausible with exact version files; C/D remain PARTIAL until authenticated depositor/project identity and deposit evidence are obtained. DOI registration alone is insufficient. | Version distinction protects references; metadata/access may change and deletion is possible. | Archive independent of project; submitted creator metadata may still be self-asserted. | DOI pointing to project-authored prose does not authenticate that prose. |
| Institutional/project domain | A/B possible; C/D require verified control, institution/account attribution and externally authenticated custody log. No actual facility established. | Depends on unverified retention/version policy. | Independent institutional custodian could help; project domain alone is same publisher. | TLS domain control does not prove scientific or custodial assertions. |

E: GitHub documents asset/tag locking and release attestations binding release,
commit and assets, while release notes remain editable. Thus provenance must be
an authenticated bound object, not only release notes.
[Immutable releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases).
E: Its asset API documents IDs, size, digest, uploader and creation/update times,
and public downloads. Those fields are useful observations, not by themselves a
signed custody chain. [Release asset API](https://docs.github.com/en/rest/releases/assets).
E: Verification supports checking an immutable release and exact asset; generated
source archives are excluded. They must not replace this retained ZIP.
[Release verification](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/verify-release-integrity).

E/L: Signed Git objects can assist identity verification, but the signing identity
must itself be trusted externally and publication time is a separate claim.
[GitHub signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification).
E: Zenodo distinguishes version DOI from concept DOI (latest version); metadata
can change, access can be restricted, and deletion is possible under its stated
conditions. Use a version-specific record, not the concept DOI alone.
[Versioning](https://zenodo.org/help/versioning),
[record management](https://help.zenodo.org/docs/deposit/manage-records/).
N: Project-specific permissions, attestation coverage/verification, external signer
acceptance and archive depositor identity need a later read-only source check.

## Minimum prospective publication package (specification only)

P: All components below are required for the strongest defensible scoped claim:
exact identity, independent retrieval, authenticated account-level attribution and
custody **from deposit onward**, with earlier history qualified. Nothing here
specifies or creates an upload destination, tag, key, DOI or package file.

1. Original unchanged ZIP, filename, 51,103-byte size and pinned SHA-256. No
   recompression, regenerated source archive, or substitution of extracted files.
2. A versioned provenance statement naming the stable publisher/depositor identity,
   identity-authentication method, NS-001/H1 relationship, base/H1/tree identifiers,
   local digest observation, claimed source location and preservation procedure.
   Distinguish asserted original creation time from actual new deposit time; retain
   `H1_MOCK_ONLY_HOLD`, reported-test limits and unknown pre-deposit custody.
3. Externally authenticated binding of that statement's digest and ZIP digest to
   the deposit event: verifiable signature/attestation or equivalent institutional
   receipt, with signer/account identity, service timestamp, destination/object IDs,
   verification material and trust roots acquired independently of the package.
   A release attestation alone is insufficient unless its actual coverage and
   accompanying evidence establish all required bindings, including depositor.
4. Stable external retrieval locator plus immutable version/commit/blob or
   attested release/asset identifiers; explicit SHA-256 remains required regardless
   of Git/DOI identity. Record stable platform repository/account IDs and retained
   timestamped metadata. Keep provenance outside mutable release notes alone.
5. Independent anonymous download result recording time, endpoint/redirect outcome,
   size, computed digest and identity/attestation verification result; preserve the
   relevant public evidence and verification instructions so another reviewer can
   repeat it without the local checkout. State deletion/retention limitations.
6. Commit-pinned links to existing H2A1 receipts and H1 manifest/source context,
   clearly labeled project claims. These explain correspondence; they do not act
   as the sole authority for the new deposit. Avoid circular hashes: provenance
   names ZIP; external event binds ZIP and provenance; later verification record
   names that event. Do not require any object to include its own final digest.

P/L: Separate identifiable evidence objects are needed if later presented in H2
category slots; one ZIP/receipt must not be relabeled as several independent
proofs. This package does not establish runtime provenance, response semantics,
transport accounting, historical creation, scientific validity or E0 permission.

## Closing specification and status

- **Exact object (R):** `NS001_H1_AUDIT_BUNDLE_20260903.zip` at the path above,
  51,103 bytes, SHA-256 `a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`.
- **Minimum byte identity (P):** independent download hashes/length match the pinned
  object and externally authenticated publication binding.
- **Minimum retrievability (P):** successful anonymous exact-version retrieval,
  stable locator, preserved verification record and explicit retention limits.
- **Minimum authority (P):** externally authenticated publisher/project binding,
  stable identity and accepted scope; neither GitHub existence nor DOI alone.
- **Minimum custody (P):** authenticated digest–publisher–destination–time binding
  to the provenance statement and independent retrieval; historical gaps retained.
- **Candidate comparison (P/L):** plain hosting/commit/tag/DOI is insufficient alone;
  immutable attested release is the leading evidenced platform class. Zenodo or an
  institutional archive are conditional alternatives, not established project routes.
- **Any route capable of all four? (P/N):** conditionally yes, an immutable release
  with the specified external identity/custody evidence appears capable for a new
  deposit. No currently evidenced deployment passes all four; actual attestation
  coverage and accepted publisher identity remain unverified. None proves full
  historical custody merely by publication.
- **Exact package (P):** unchanged ZIP + size/digest + authenticated provenance +
  external event/identity/time binding + immutable locator/version + independent
  retrieval/verification record + explicitly subordinate receipt/manifest links,
  as specified in the six requirements above. Not created in this circuit.
- **Current wording (R/L):** “Original byte-identity verification holds; independent
  external auditability is PARTIAL.” remains accurate. Prior receipt unchanged.
- **H2A1 status:** local identity verified; external auditability PARTIAL. All eight
  substantive gates remain unresolved: `external_trust_root`, `client_source`,
  `response_contract`, `transport_accounting`, `dependency_runtime_lock`,
  `maximum_partition_memory`, `amendment_freeze`, `final_manifest_package_audit`.
- **E0 status:** HOLD; no execution or JHTDB request. Gate 1 remains PARTIAL.
- **H2A2 status:** unstarted. This specification does not implement its verifiers.
- **Preservation:** 38 pre-existing repository file hashes and the external ZIP
  digest are checked unchanged before commit; only this receipt may be added.
  No ZIP publication/upload, archive package, release, tag, DOI, credential change,
  or external custody object was created. The only authorized external write is
  this receipt's Git commit/push. No test rerun is claimed for a prose-only circuit.
- **One recommended next bounded H2 action (P):** a read-only H2A1 feasibility
  review mapping GitHub immutable-release attestation fields and verifiable
  publisher/depositor identity to the four fixed criteria, documenting any missing
  custody bindings and required authority choice. Do not publish, configure,
  create credentials, begin H2A2, or execute that recommendation in this circuit.
