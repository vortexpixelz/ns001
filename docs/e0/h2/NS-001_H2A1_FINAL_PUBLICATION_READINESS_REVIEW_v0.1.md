# NS-001 H2A1 final publication-readiness review v0.1

## Scope and decision

Read-only review, 2026-09-23 UTC. Preparation branch
`codex/e0-h2-preparation`; HEAD before
`e1d06a6b09b26a8dd8928c2f674aa2dc33a0b069`; initial working tree clean.
Origin fetched first. Current origin/main and GitHub default main remain
`ef71e56263da8e4d0dfcd5228795356e38b27998`; no main drift or content conflict.

**Publication-ready: PARTIAL. Separately authorized publication circuit may now
proceed: NO.** Frozen inputs and adopted scope are consistent, but the available
local verification toolchain does not implement the prescribed attestation
commands. This is a concrete execution prerequisite, not a request to prove future
publication facts before they can exist. No installation or repair is attempted.

## Findings

| Requirement | Classification | Evidence and limit |
| --- | --- | --- |
| Artifact identity | VERIFIED | Retained ZIP directly read, exact filename, 51,103 bytes and frozen SHA-256 below. No write/recompression occurred. |
| Release inputs | VERIFIED WITH RESIDUAL ASSUMPTION | Tag/release inventories empty; target workflow retrieved from GitHub by full commit; immutability enabled. Future service/account availability remains conditional. |
| Workflow controls | VERIFIED | Exact remote/local digest; manual-only; empty global permissions; job only id-token/attestations write; duplicate-key hook and both timestamp checks preserved. |
| Workflow execution readiness | VERIFIED WITH RESIDUAL ASSUMPTION | File is on default main, unrun; real signing success and hosted runtime are not tested or guaranteed. |
| Authority | VERIFIED WITH RESIDUAL ASSUMPTION | Specification/adoption and deposit-plan adoption match their original commits; scope is prospective maintainer authority, not third-party certification. Actual future uploader remains to be observed. |
| Provenance input | VERIFIED | Exact embedded JSON bytes rehashed; all 13 mandatory typed workflow fields independently compared to the actual expected dictionary. No guard/network execution used. |
| Deposit design | VERIFIED WITH RESIDUAL ASSUMPTION | Adopted GitHub-only, commit-pinned ordinary-content deposit can represent all required components; deletion/hosting risks accepted. Actual complete deposit is future evidence. |
| Operational attestation verification | BLOCKING / NEEDS ADDITIONAL EVIDENCE | `/usr/bin/gh` is 2.45.0 (Ubuntu 2.45.0-1ubuntu0.3); both `gh attestation download --help` and `gh attestation verify --help` return unknown command. Neither cosign nor sigstore is on PATH. No supported alternative has been established by this review. |
| Future release IDs, times, uploader, signatures, retrieval | REQUIRES FUTURE OBSERVATION | Must be observed and verified, never prefilled or inferred from this review. |

The PATH checks are not an exhaustive search of all software on the machine.
A separately validated compatible toolchain could resolve the blocker without
changing scientific artifacts, main or the workflow. Raw API access can potentially
retrieve signed bytes but is not a replacement for cryptographic verification.
The prior template commands were documented capabilities, not proof that this
machine had a compatible verifier. This review does not revise old receipt bytes.

## Frozen identities and scope consistency

- Tag: `ns001-h1-audit-v1` (unused).
- Title: `NS-001 H1 mock-only audit bundle v1`.
- Exact target: `ef71e56263da8e4d0dfcd5228795356e38b27998`.
- H1 source: `6e33cb9ca7019e50e2f247ade9ae8c9a7b40d3ff`; not the publication target.
- ZIP: `NS001_H1_AUDIT_BUNDLE_20260903.zip`, 51,103 bytes,
  SHA-256 `a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`.
- Local ZIP: `/home/jacob/Documents/NS-001/audit/2026-09-03/NS001_H1_AUDIT_BUNDLE_20260903.zip`.
- Provenance: `NS001_H1_PUBLICATION_PROVENANCE.json`, 2,298 bytes,
  SHA-256 `9f67d54f2852c386384b9ea1bd1c231bcbb572490bd8b94b9ce84396a7fbac89`.
- Workflow: `.github/workflows/ns001-h1-custody.yml`, SHA-256
  `236b8f30a27fa1c3c26f134c794f2e3e989b9b31d1e3adfbcfae18e21fa420bf`.
- Repository: `vortexpixelz/ns001`, ID `1354037143`.
- Expected publisher and both uploaders: `vortexpixelz`, ID `202687650`.

Exact JSON and release body remain those specified in the prepublication receipt
at `15ce97f7c29d28d6e1a5d005a8003a8790f5c08d`: UTF-8, LF, one terminal LF,
no BOM; body is decoded authority_text plus LF. There are no unresolved placeholders
inside that frozen asset. It is explicitly prospective and event-neutral, not a
completed publication receipt. IDs, actual uploader, service UTC-second timestamps,
observation times and witnessed signature timestamps belong in post-event records.
No fabricated times are inserted; none is needed to calculate the frozen digest.

Mandate specification is unchanged from `4333e55beffbe6c7d5ac81eb580f1c5afe04a9bd`;
adoption from `cd6e3eb806fa5a5045daaf35904ea927cec68f55`; deposit-plan adoption from
`e1d06a6b09b26a8dd8928c2f674aa2dc33a0b069`. Proposed language expressly disclaims
corporate/Symonic LLC, institutional, historical and independent certification.
Publication cannot certify earlier possession, authorship or original creation.
H1 remains mock-only, Gate 1 PARTIAL. The adopted hosting decision resolves the
previous plan-choice issue but does not create a bundle or validate a signature.

## Exact future transaction sequence — NOT EXECUTED

Every mutating step below requires a subsequent explicit execution instruction
covering that operation. A generic permission to publish must not silently include
dispatch or evidence-deposit creation. The current circuit authorizes none of them.

1. **Final preflight before any mutation:** resolve the toolchain blocker; establish
   supported download and cryptographic verification commands, versions and trusted
   roots, plus the ability to preserve their outputs. Re-fetch main; recheck the
   exact source/workflow/ZIP/provenance digests, clean preparation tree, adopted
   records, authenticated account rights, enabled immutability and absent exact
   tag/release. Confirm no prior custody attestation/run. Stop on unexpected main
   drift affecting the frozen dispatch identity; do not retarget silently.
2. **Exact tag:** if explicitly authorized, create one lightweight tag
   `ns001-h1-audit-v1` at the full target commit above; verify it resolves exactly.
   No floating target or tag overwrite. Recheck existing workflow triggers so this
   tag operation cannot launch an unintended scientific workflow.
3. **Draft release:** create one draft with that tag, frozen title and exact body,
   prerelease=false, make_latest=false. Verify association with the tag/target.
   Publication must not precede asset staging.
4. **Exact assets:** upload only the unchanged ZIP and exact frozen provenance JSON
   as the adopted personal account. Read back staged bytes and verify both digests,
   lengths, names and actual uploaders. No recompression or replacement fallback.
5. **Finalize once:** publish that draft with immutability enabled; verify immutable
   true, draft false, exact tag/commit, exactly the two uploaded assets and expected
   title/body/flags. Record actual release and asset IDs, canonical locators,
   uploader/author, publication/creation timestamps and observation UTC. Retain raw
   observations with provenance. Never invent an unknown field or alter frozen JSON.
6. **Independent published-byte check before signing:** download both assets
   anonymously from the exact repository/tag/filename release locators; compare
   hashes/lengths and typed provenance. Check usable `YYYY-MM-DDTHH:MM:SSZ`
   release published_at and ZIP asset created_at. Verify and preserve GitHub's
   separate automatic release attestation, not treating it as the custody statement.
7. **Single custody dispatch, only if explicitly authorized and preceding checks
   pass:** use ref `main` only while its commit remains the frozen target. Inputs:
   release_tag=`ns001-h1-audit-v1`, publication_commit=
   `ef71e56263da8e4d0dfcd5228795356e38b27998`, provenance_sha256=
   `9f67d54f2852c386384b9ea1bd1c231bcbb572490bd8b94b9ce84396a7fbac89`,
   authorization=`ATTEST-EXACT-H1`. These are frozen inputs validated against observed
   publication, not invented inputs containing release IDs or timestamps. The
   workflow fetches those observations itself. Require actor ID 202687650, first
   attempt, expected source/ref and a successful non-skipped run. No automatic rerun.
8. **Recover and verify signed material:** download complete custody bundle(s) via
   a supported authenticated/alternate route if necessary. Never rely only on a
   runner path or summary. Verify both subjects and the exact custom predicate,
   issuer, signer workflow/certificate identity, source/signer commit, verified
   timestamps and observed release/asset/provenance bindings using the pinned policy
   in the retrieval review. Stop if any material is missing or unverifiable.
9. **One adopted evidence deposit, only if explicitly authorized:** preserve exact
   provenance, both categories of signed verification material, observation records,
   ZIP identity/locators, release/tag/commit/assets, observed uploader/times, workflow
   bytes/digest/ref, authority/adoption copies, verifier versions/roots/instructions
   and limitations, with a digest manifest. Use ordinary content on the preparation
   branch, one evidence-only commit, full commit SHA; no main change, second release
   or amendment to the immutable assets. Unknown post-event sizes/IDs must be recorded
   honestly; if the selected repository deposit cannot hold the material, STOP rather
   than choose a new provider or reduce the evidence set silently.
10. **External reproduction and final evaluation:** push the deposit, anonymously
    retrieve all pinned files, verify manifest/subject hashes and signed evidence
    without a privileged transient lookup. Record the actual deposit commit and
    verification results in the final transaction report, avoiding circular self-
    hashing. Re-evaluate H2A1 external auditability only from these observed results;
    do not infer substantive H2-gate passage, scientific validity or E0 authorization.

[GitHub immutable-release documentation](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases)
requires assets to be staged before immutable publication. The post-event deposit
therefore remains separate. Release title/body can remain mutable while assets/tag
are protected; administrative deletion remains possible.
[Attestation download documentation](https://cli.github.com/manual/gh_attestation_download)
and [verification documentation](https://cli.github.com/manual/gh_attestation_verify)
provide bundle retrieval and constrained signature-verification capabilities, but
the installed CLI lacks them. Documentation does not resolve local tool availability.

## Abort conditions and partial-transaction handling

**BLOCKING:** size/digest mismatch; changed workflow/trigger/permissions; wrong or
missing target; unexpected existing tag/release; immutability disabled; altered or
missing mandate/deposit adoption; provenance inconsistency; incompatible verifier
or unavailable trusted verification material; inability to preserve complete evidence;
material unexpected main change; wrong account/uploader; unusable service timestamps;
failed external retrieval/signature; or any operation outside explicit authorization.

Before publication, stop before further mutations and report any staged objects.
After publication, failure to obtain/verify/deposit evidence leaves H2A1 PARTIAL;
report exactly which objects already exist. Do not delete, recreate, replace assets,
move tags, rerun attestation or call a partial transaction complete. Recovery requires
separate bounded instructions. The sequence is not atomic and cannot promise rollback.

Residual assumptions: accepted GitHub hosting/deletion risk; service/TLS integrity;
hash security; hosted runner and pinned action behavior; valid external trust roots;
future authenticated material retrieval and anonymous deposit retrieval. Anonymous
attestation API access remains unassumed after the earlier 401. Actual event evidence
is REQUIRES FUTURE OBSERVATION, not a pre-existing certification.

## Preservation and closing verdicts

Current live inventories: no releases/tags, four old runs, no custody run.
The repository-digest attestation lookup remains 404, a bounded negative observation.
No publication, attestation, evidence deposit, dispatch or settings mutation occurs.
Only this receipt is added; all pre-existing tracked file hashes and main/settings/
publication/run inventories are compared before commit. No scientific tests or workflow
execution is performed. Static guard checks are source inspection, not new runtime tests.

- Artifact identity verdict: VERIFIED.
- Release-input verdict: VERIFIED WITH RESIDUAL ASSUMPTION.
- Workflow-readiness verdict: VERIFIED controls and placement; runtime/signing
  outcome requires future observation.
- Authority verdict: VERIFIED WITH RESIDUAL ASSUMPTION, scoped prospective mandate.
- Provenance-input verdict: VERIFIED, exact bytes and typed contract consistent.
- Evidence-deposit verdict: design ADOPTED and sufficient in scope; operational
  verification toolchain BLOCKING, actual deposit REQUIRES FUTURE OBSERVATION.
- Exact future publication transaction sequence: numbered steps 1–10 above; none run.
- Abort conditions: all listed integrity, identity, state, toolchain, preservation
  and authorization failures; preserve partial-state truth without silent recovery.
- Residual assumptions: GitHub deletion/hosting, service/runtime/trust-root integrity,
  future material acquisition and independent deposit retrieval as stated above.
- Publication-ready verdict: **PARTIAL**.
- Separately authorized publication circuit may now proceed: **NO** until a supported
  verification toolchain is established and the final preflight passes.
- H2A1: local identity VERIFIED; independent external auditability PARTIAL; all eight
  substantive H2 gates unresolved.
- E0: HOLD; Gate 1 PARTIAL.
- H2A2: UNSTARTED.
- One next bounded action: separately authorize establishment and offline capability
  validation of a supported attestation verification toolchain, with no publication,
  workflow dispatch, evidence deposit, main/workflow change, E0 or H2A2 work.
