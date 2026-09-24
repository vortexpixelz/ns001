# NS-001 H2A1 tag-trigger mitigation placement v0.1

## Scope and preflight

Authorized trigger-only placement, 2026-09-24 UTC. Preparation branch
`codex/e0-h2-preparation`, HEAD before
`f11466d9cae93600b4c16c2913e32d3ac4fbd577`.
Origin fetched; old main matched reviewed target
`ef71e56263da8e4d0dfcd5228795356e38b27998`. Trigger bytes matched the review.
The only existing untracked file was the expected publication transaction STOP
receipt. It is excluded from this commit and preserved byte-for-byte, SHA-256
`30f4c22bff968f02d24ea6fb9ad663ec0854354579cef984abbc6314575ce2de`.

GitHub reported main protected=false; branch protection endpoint returned 404
Branch not protected; repository rulesets and effective main rules were empty.
Authenticated repository context had push permission. Direct one-file fast-forward
was permitted without PR, merge commit, protection bypass or settings changes.
Release/tag inventories were empty and run count was four, all pre-existing.

## Exact mitigation and static validation

Changed path: `.github/workflows/ns001-sanity.yml` only.
Added four lines under `on.push`, preserving all other bytes:

```diff
 on:
   push:
+    branches:
+      - '**'
+    tags-ignore:
+      - 'ns001-h1-audit-v1'
     paths:
```

YAML parsed successfully using PyYAML BaseLoader, retaining `on` as a string key.
Parsed before/after structures differ only by the two intended filter entries.
Jobs/steps/scripts/environment/permissions/artifact behavior are unchanged; the
entire jobs suffix was compared byte-for-byte. Existing paths list and manual
trigger were compared unchanged. No scientific protocol was executed for testing.

Static trigger findings, using the official semantics established in the preceding
mitigation review:

- Branch main and slash-containing feature/x remain eligible under identical path
  conditions; unrelated branch selection is unchanged.
- Exact tag ns001-h1-audit-v1 is excluded irrespective of changed paths.
- Other tags retain existing trigger selection; no broader tag namespace excluded.
- pull_request and schedule remain absent; workflow_dispatch remains unchanged.
- The mitigation commit itself matches the workflow's own path; its push is protected
  by the authorized commit-message skip instruction, not by the added tag filter.

These are syntax/structural and static selection checks, not a live tag-push test.
No test tag or scientific workflow run was created.

## Commit and placement evidence

Mitigation commit / new main:
`d9dcfbef1bea173b316bc968fd71421c982422c3`.
Sole parent: `ef71e56263da8e4d0dfcd5228795356e38b27998`.
Exact commit message:

```text
ci: exclude H1 audit tag from scientific sanity trigger [skip ci]
```

Prepared on local branch `codex/h1-tag-trigger-mitigation`, isolated worktree
`/tmp/ns001-tag-trigger-mitigation`; no temporary branch was pushed remotely.
Before push, one-path diff, parent and skip marker verified. Main was rechecked,
then this exact commit was fast-forward pushed to refs/heads/main without merge.
Independent GitHub commit and contents reads verified parent, sole changed path,
message marker and exact resulting bytes. Run inventory was inspected immediately
and again after independent checks: same four run IDs
`34488406675`, `33563351013`, `33563214294`, `33562657929`.
No scientific or custody workflow run from this circuit was observed. An unexpected
run would have caused STOP without cancellation, deletion or retry.

## Preservation and target consequence

All pre-existing preparation tracked files and STOP receipt remain byte-identical.
Preparation history was not placed on main. No workflow besides sanity changed.
The remote custody workflow retains SHA-256
`236b8f30a27fa1c3c26f134c794f2e3e989b9b31d1e3adfbcfae18e21fa420bf`.
Local retained ZIP independently rehashed: `NS001_H1_AUDIT_BUNDLE_20260903.zip`,
51,103 bytes, SHA-256
`a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`.
Frozen proposed provenance remains 2,298 bytes, SHA-256
`9f67d54f2852c386384b9ea1bd1c231bcbb572490bd8b94b9ce84396a7fbac89`.
Mandate and evidence-deposit plan are unchanged. Toolchain is not modified.
No release/tag/asset/attestation creation or workflow dispatch operation was issued;
empty release/tag lists and unchanged run inventory corroborate no publication.
No universal claim of attestation absence outside inspected repository activity.

Old target `ef71e56263da8e4d0dfcd5228795356e38b27998` is no longer authorized for
publication. New main `d9dcfbef1bea173b316bc968fd71421c982422c3` is only a candidate
for a subsequent separately authorized amendment/re-freeze. It is NOT silently
adopted as the publication target. No frozen input is changed in this circuit.

Next amendment must cover publication target, provenance publication_commit and
old-target reference in authority_text, exact serialized provenance bytes/size/digest,
release body derived from authority_text, dispatch publication_commit/provenance_sha256,
and signer/source verification commit constraints. Preserve old frozen records as
history rather than overwriting them. The current frozen provenance remains unchanged
and cannot truthfully serve the amended target without an explicit new freeze.

Unchanged future invariants: H1 ZIP identity, historical H1 checkpoint, all frozen
scientific artifacts, proposed tag ns001-h1-audit-v1, title NS-001 H1 mock-only audit
bundle v1, custody workflow bytes/digest, publisher mandate scope, adopted evidence
plan, pinned verifier and historical limitations. The new publication authorization
must reference the later amended values, not infer permission from this placement.

## Closing record

- Old main: `ef71e56263da8e4d0dfcd5228795356e38b27998`.
- New main / mitigation commit: `d9dcfbef1bea173b316bc968fd71421c982422c3`.
- Exact changed path: `.github/workflows/ns001-sanity.yml`.
- Exact semantic change: explicit all branches plus exclusion of exactly
  ns001-h1-audit-v1; existing paths/manual/jobs unchanged.
- Skip instruction: `[skip ci]`, verified in pushed commit message.
- Static trigger-verification result: PASS, no scientific execution.
- Push result: successful exact one-file fast-forward; independently read back.
- Scientific workflow run created: NO observed; run inventory unchanged.
- Publication workflow run created: NO observed; custody workflow unrun.
- Tag/release/asset/attestation inventory: no publication objects created; release/tag
  lists empty and no new run; no attestation operation invoked.
- Old target usable: NO.
- New target candidate: `d9dcfbef1bea173b316bc968fd71421c982422c3` only.
- Frozen inputs requiring amendment: target, target-dependent provenance/text/digest,
  release body, dispatch values and verification commit constraints.
- Frozen inputs remaining unchanged: ZIP/science, current historical provenance,
  tag/title, custody workflow, mandate, evidence plan and toolchain.
- Publication authorized: NO.
- H2A1: PARTIAL; trigger mitigation placed, target/provenance re-freeze still required.
- E0: HOLD; Gate 1 PARTIAL unchanged.
- H2A2: UNSTARTED.
- One next bounded action: separately authorize a target/provenance amendment and
  re-freeze for the new candidate commit, preserving old records and creating no
  publication objects or workflow runs.
