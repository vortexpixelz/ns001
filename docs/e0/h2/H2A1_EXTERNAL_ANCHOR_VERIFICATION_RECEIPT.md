# H2A1 external-anchor verification receipt

**Verdict: VERIFIED (four external identities only). E0: HOLD, not authorized, not executed.**

## Reconciliation and scope

Branch: `codex/e0-h2-preparation`. Starting checkpoint:
`711b6c7f0cfd1c69694bff8a3fd134b585e633df`.
Public, credential-disabled HTTPS fetch confirmed main at
`2075dd6cc70e4a922b41c2f9a75107251ac090cf`. Reconciliation merge:
`a6156e98888c75c8cbdebb55dd598e85e9c243b2` (also the observation HEAD).
The merge introduced no tree changes. Governing boundary:
`H2_EVIDENCE_CONTRACT_DRAFT.md`, unchanged.

No JHTDB requests, credential reads, E0 execution, scientific-design changes,
frame/stride/threshold changes, or frozen-preregistration changes occurred.
Unrelated pre-existing untracked `docs/e1-openai/` files were left untouched.

## Independently read anchors

| Anchor | Exact expected and observed identity | Status |
| --- | --- | --- |
| H1 checkpoint | `6e33cb9ca7019e50e2f247ade9ae8c9a7b40d3ff` | VERIFIED |
| Scientific base | `0393315223df8ed90f20f0c821508cc98bea08d1` | VERIFIED |
| Frozen preregistration SHA-256 | `a2a8523c065d4d41155aa29d367c888d49ab3032f6075b8cebbd2475ff1efd78` | VERIFIED |
| H1 audit bundle SHA-256 | `a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f` | VERIFIED |

`H2A1_EXTERNAL_ANCHOR_OBSERVATIONS.json` retains exact source paths, byte counts,
observed identities, raw commit SHA-256 values, reasons, and observation HEAD.
Inputs remain retained in the local Git object store, frozen repository file,
and external archive. The archive is
`/home/jacob/Documents/NS-001/audit/2026-09-03/NS001_H1_AUDIT_BUNDLE_20260903.zip`
(51,103 bytes); it was hashed directly without extraction or execution.

Commit IDs were recomputed from raw commit bytes with Git's object header;
replacement objects were disabled. Both commits are ancestors of observation
HEAD, and scientific base is an ancestor of H1. The frozen file (9,923 bytes)
was read directly and compared byte-for-byte with both historical commit blobs.
The unchanged sidecar SHA-256 is
`0e1e5900aec22a55332c1bde18147c3f2ff5a55351a8d1bec6e504b3eb960de8`;
it was not used as proof of file contents. The entire preregistration directory
has no diff from the starting checkpoint.

Independence here means observations read from retained repository/artifact
bytes separately from expected declarations, not a second human reviewer or
independent historical custody authentication. No declaration labels, submitted
observed digests, or sidecars establish verification. Missing, inaccessible,
symlinked, or unanchored evidence fails closed; digest mismatches are
NOT VERIFIED. This verifies identities only, not bundle claims or authority.

## Offline validation

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`:
**79 tests passed** (1.633 seconds), including eight H2A1 tests.
Negative cases cover absent evidence, declaration text substituted for bytes,
Git failure/timeout, symlink evidence, failed ancestry, and historical-byte
mismatch. Synthetic success still leaves every gate unresolved and E0 on HOLD.
`git diff --check` passed. Local verifier reproduction:
`PYTHONDONTWRITEBYTECODE=1 python3 -m e0.h2.external_anchor_verifier`.

## Unresolved substantive gates and stop boundary

All eight remain unresolved:
`external_trust_root`, `client_source`, `response_contract`,
`transport_accounting`, `dependency_runtime_lock`, `maximum_partition_memory`,
`amendment_freeze`, `final_manifest_package_audit`.

In particular, matching external identities does not resolve external trust-root
authority/content/custody or its remaining required evidence. H2A1 does not
implement the other later-H2 verifiers or make any substantive gate decision.
Even a future full H2 pass would not authorize E0.

Single next authorized action: STOP and await explicit authorization for a
separately bounded next H2 step. No further H2 implementation or E0 run is
currently authorized.
