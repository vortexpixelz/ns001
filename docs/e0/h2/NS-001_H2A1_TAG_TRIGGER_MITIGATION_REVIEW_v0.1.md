# NS-001 H2A1 tag-trigger mitigation review v0.1

## Scope and exact current state

Read-only review, 2026-09-24 UTC. Preparation branch
`codex/e0-h2-preparation`, HEAD before
`50665ce64ebe1246a38e0aa9df35b8ae5b9c5847`. Origin fetched. Frozen target and
current origin/main are both `ef71e56263da8e4d0dfcd5228795356e38b27998`.
The sanity workflow bytes are identical at frozen target, current main and
preparation HEAD. No workflow or main modification is performed.

The existing uncommitted transaction STOP receipt is explicitly excluded from
this commit. Its initial SHA-256 is
`30f4c22bff968f02d24ea6fb9ad663ec0854354579cef984abbc6314575ce2de`;
verify it unchanged before/after the selective review commit/push.

Exact `on:` configuration of `.github/workflows/ns001-sanity.yml`:

```yaml
on:
  push:
    paths:
      - "Dockerfile"
      - "requirements.txt"
      - "Makefile"
      - "ns001_tau_check.py"
      - "run_experiment.py"
      - "protocols/**"
      - ".github/workflows/ns001-sanity.yml"
  workflow_dispatch:
```

There are no branches, branches-ignore, tags, tags-ignore or paths-ignore filters;
no pull_request/pull_request_target, schedule, release, workflow_call or workflow_run
trigger. The only job is `container-reproduction`, with no ref/event job-level `if`.
It checks out, builds the container, runs sanity and temporal-smoke protocols, checks
receipts and uploads them. Checkout/upload actions are steps, not reusable workflow
calls. No downstream dispatch or reusable workflow invocation appears in this file.
The other tracked workflow is manual-only custody; no additional scientific downstream
workflow is configured in the inspected trees. GitHub inventory additionally lists
its service-managed Dependabot workflow, not a scientific reusable invocation.

GitHub reports sanity workflow ID `347905226` active. Releases/tags remain empty;
run inventory has four old runs and no new custody/scientific run in this circuit.
For a normal push of `refs/tags/ns001-h1-audit-v1` at the frozen target, trigger
selection admits the sole job; its scientific steps are eligible to execute.
Actual completion still depends on runner/build success, which is not a safety guard.
Manual dispatch remains available independently; none is performed.

## Official event semantics and old-target consequence

**VERIFIED:** [GitHub push event reference](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#push)
describes commit/tag pushes, with the pushed tip commit and updated ref as event
context. A single normal tag push is in scope; bulk-tag exceptions are not a plan.

**VERIFIED:** [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onpushbranchestagsbranches-ignoretags-ignore)
allows both branches and tags when neither ref category is filtered. Defining only
one category excludes the other. Path filtering does not apply to tag pushes.

**VERIFIED:** [Workflow selection](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows#workflow-triggers)
uses workflow files/version at the event's associated commit/ref. Consequently, a
later main-only edit cannot repair the workflow used by a tag still pointing to
`ef71e56263da8e4d0dfcd5228795356e38b27998`. For the proposed workflow-level solution,
the publication target must become a new commit containing that solution. No old
commit rewriting, ref rewriting or implicit retargeting is acceptable.

## Minimal options compared — none implemented

All options retain the exact current paths list and manual trigger and alter no
job, action, container, scientific code, protocol or output logic. There are no PR
triggers to preserve/add. Manual behavior is unchanged by all three options.

### A — exact tag exclusion, recommended

Add under `push`:

```yaml
    branches: ['**']
    tags-ignore: ['ns001-h1-audit-v1']
```

This preserves existing branch selection, including slash-containing branch names,
and existing path filtering. Only this exact tag is excluded; other tags retain
current selection behavior. Broader namespace exclusions are not justified by a
single frozen tag. Adding tags-ignore WITHOUT branches would suppress branch pushes
and is rejected as a non-minimal behavioral change. No evidence establishes intent
to execute science on the custody publication tag; unrelated tag behavior is retained.

### B — branch pushes only, broader than necessary

Add only:

```yaml
    branches: ['**']
```

Branch/path behavior preserved; all tag pushes become excluded. No evidence in this
review establishes that every historical/future tag execution is unintended. Hence
this is not recommended without an explicit policy decision. Smaller textual diff
is not the smallest semantic change.

### C — positive plus negative tags, equivalent but unnecessary

Add:

```yaml
    branches: ['**']
    tags: ['**', '!ns001-h1-audit-v1']
```

Preserves branch/path behavior and other tags, excludes the exact tag. Ordered
positive/negative patterns are supported. Do not combine tags with tags-ignore.
There is no existing positive tag pattern requiring this more complex formulation.
A is preferred. All three options admit offline syntax/selection checks without
executing scientific protocols; they do not warrant dispatching live jobs as tests.

## Exact recommended diff and mitigation-push risk

Proposed file: `.github/workflows/ns001-sanity.yml` only.

```diff
 on:
   push:
+    branches: ['**']
+    tags-ignore: ['ns001-h1-audit-v1']
     paths:
       - "Dockerfile"
```

**VERIFIED RISK:** pushing a branch commit containing this change ordinarily matches
its own workflow-file path and the preserved branch filter. Thus the often-suggested
“push fix, then check no run” order is unsafe without an advance suppression mechanism.
The same applies to pushing a temporary implementation branch, not just main.

A future separately authorized one-file commit must include an exact `[skip ci]`
marker in its commit message BEFORE any remote push. [GitHub skip documentation](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs)
explicitly supports skipping push/PR workflows through this marker. It does not block
workflow_dispatch and does not disable ordinary pushes of later commits. It can leave
required checks pending; if branch protection blocks placement, STOP without bypassing
protection, settings changes or a new unmarked merge commit. This documented mechanism
protects installation of the proposed fix, not a tag at the old unchanged commit.

Recommended future commit subject: `Exclude H1 audit publication tag from sanity CI [skip ci]`.
The marker changes commit metadata only, while the tree diff remains one path.
It suppresses other push/PR workflows for that commit too; record that bounded effect.
Do not strip the marker through squash/reword/merge. The tag rule supplies the enduring
specific exclusion; do not rely solely on commit-message suppression for the future tag.

## Target amendment and preservation conflict

A new target can be a one-file, single-parent descendant of the frozen target.
No scientific bytes or preparation history need be added to main. After authorization,
create it locally from fresh verified main (only if still compatible), inspect its
exact tree/parent/diff, and publish that exact commit with the skip marker intact.
If current main later diverges, stop for review rather than broadly reconcile it.

**Important incompatibility:** preservation of the existing frozen provenance bytes
AND using a new publication target cannot both satisfy the current workflow contract.
The provenance explicitly contains `publication_commit` and repeats the old target
inside `authority_text`. The workflow compares publication_commit with dispatch input
and tag resolution. No workaround should leave it claiming the old target.

Therefore a separate explicit amendment/re-freeze is required, not an in-place edit
of old receipts or silent regeneration. Preserve all old frozen inputs as history.
Required prospective amendments are:

- Publication/tag target and target-dependent preflight/verification expectations.
- New version of proposed provenance: publication_commit and target text inside
  authority_text; recompute and freeze exact serialized bytes, size and SHA-256.
- Release body derived from that revised authority text.
- Dispatch publication_commit and provenance_sha256.
- Expected source/signer/workflow commit SHA for dispatch on new main and offline
  signer/source-digest constraints; record new reference commitment, retaining the
  same workflow path/ref policy and file digest if its bytes are unchanged.
- Updated publication authorization/readiness record identifying those amended values.

The old provenance hash `9f67d54f2852c386384b9ea1bd1c231bcbb572490bd8b94b9ce84396a7fbac89`
and exact bytes must stay preserved today and in historical receipts. They cannot
serve as the operative unchanged asset for the amended target. The present review
neither creates nor authorizes a replacement. If preserving that hash as the future
operative asset is non-negotiable, this recommended mitigation cannot proceed.

Unchanged: H1 ZIP filename/51,103 bytes/SHA-256
`a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`, historical H1
checkpoint, proposed tag/title, repository/account identities, publisher mandate,
evidence plan, scientific design/data/results/code and frozen E0 preregistration.
Custody workflow bytes/digest
`236b8f30a27fa1c3c26f134c794f2e3e989b9b31d1e3adfbcfae18e21fa420bf`
need no change; its invocation/verification commit binding does. E0 HOLD/H2A2
UNSTARTED and all historical limitations remain intact.

## Safe future order and testing plan

1. Obtain explicit authorization for this two-line trigger edit and marked one-file
   placement, plus agreement that target-dependent frozen inputs need a later
   separately reviewed amendment. No publication authorization follows automatically.
2. Locally create the one-file descendant with the skip marker. Do not push an
   unmarked precursor. Inspect the full tree diff and all event triggers first.
3. Offline parse the proposed YAML with GitHub-compatible handling of `on`; compare
   untouched jobs/paths/manual trigger bytes. Check the selection matrix below.
   A parser/truth table checks the model, not a live GitHub execution test.
4. Recheck current main, workflow inventory, skip semantics and applicable branch
   protection. Fast-forward main only to the exact reviewed marked commit if authorized
   and allowed; no unrelated merge. Independently verify remote bytes/parent/path,
   intact message marker and unchanged run inventory. Abort on unexpected run.
5. Independently review the fix; obtain/record explicit target/provenance amendment,
   preserving old inputs and freezing new bytes/digests/commit bindings in new records.
6. Repeat full readiness: artifact/provenance identity, unused tag/release, target/ref
   triggers, main/workflow digests, authority, immutability, toolchain policy, evidence
   preservation and publication sequence. Only then seek exact publication authorization.

Expected selection matrix (reasoned from official semantics, no remote test events):

| Event at mitigated commit | Expected |
| --- | --- |
| Tag ns001-h1-audit-v1, with any path list | Excluded |
| Another tag, absent a commit skip marker | Existing behavior retained |
| Branch main or feature/x, matching path, no skip marker | Selected |
| Branch main or feature/x, docs-only path, no skip marker | Existing path filtering |
| Branch update installing marked mitigation commit | Skipped by commit message |
| Manual workflow_dispatch | Existing manual behavior, no test dispatch |
| pull_request / schedule | Not configured |
| Tag ns001-h1-audit-v1 at old target | Still admitted; later main fix irrelevant |

Abort on drift, extra changed paths, missing marker, broader filter effects,
protection requiring unsafe integration, unexpected run, any frozen-byte mutation,
missing amendment authorization, or unresolved provenance/commit mismatch. Never
race/cancel a live run as the safety mechanism.

## No-workaround finding

No established publication mechanism within the existing frozen manual transaction
keeps the old target safely. API versus CLI, draft/final release sequencing, tag
creation as a release side effect, deletion/recreation and path filters do not supply
a demonstrated exemption. Global Actions disabling and racing cancellation are excluded.

There IS an official exception, which must not be hidden: events caused by a workflow's
repository `GITHUB_TOKEN` generally do not start additional workflows (apart from
specified exceptions). [GitHub documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow#triggering-a-workflow-from-a-workflow).
This is not the user's existing personal CLI authentication. Employing it would need
a separately designed publication workflow/token authority and execution, and could
change publisher/uploader bindings. No existing such authorized mechanism was found.
It is not an approved workaround here or the smallest workflow-filter mitigation.
Similarly, altering the old commit message to add a skip marker changes its SHA;
it cannot preserve the frozen old target. Old-target usability below is therefore
NO for the reviewed route, not a claim that GitHub has no suppression mechanisms.

## Preservation and closing verdicts

Only this new review receipt is staged/committed. All existing tracked files plus
the uncommitted STOP receipt are hash-compared before commit; main, settings,
release/tag/run inventories are checked unchanged. No mitigation, tag, release,
upload, dispatch, signature, scientific execution or evidence deposit is created.
The STOP receipt remains untracked and byte-identical.

- Trigger blocker: VERIFIED.
- Current tag-trigger behavior: old target admits the exact tag push; sole scientific
  job has no ref guard, making sanity/smoke steps eligible.
- Path-filter finding: VERIFIED, path filters do not protect tag pushes.
- Event-ref/workflow-version finding: VERIFIED; later main edit does not protect old tag target.
- Recommended mitigation: option A, exact tag exclusion with explicit all-branches inclusion.
- Exact proposed workflow diff: two added lines under push shown above; no jobs/path changes.
- Mitigation-commit trigger risk: YES, workflow self-path matches; use a separately
  authorized marked commit with `[skip ci]` before any push and preserve it during placement.
- Old target still usable: NO for this workflow-level mitigation route.
- New publication target required: YES, one-file descendant containing mitigation.
- Frozen inputs requiring amendment: target, provenance publication_commit and authority
  text, serialized digest/size, release body, dispatch values and signer/source commit policy.
- Frozen inputs remaining unchanged: original historical receipts/provenance bytes,
  H1 ZIP, custody workflow bytes, tag/title, mandate/evidence plan and all science;
  old provenance cannot also remain the operative asset for a new target.
- Publication authorized: NO.
- H2A1: PARTIAL; publication remains BLOCKED pending authorized mitigation/amendment.
- E0: HOLD; Gate 1 PARTIAL.
- H2A2: UNSTARTED.
- One next bounded action: explicitly authorize the proposed trigger-only mitigation
  and safely skipped one-file placement, acknowledging that a separate subsequent
  target/provenance re-freeze is required before publication.
