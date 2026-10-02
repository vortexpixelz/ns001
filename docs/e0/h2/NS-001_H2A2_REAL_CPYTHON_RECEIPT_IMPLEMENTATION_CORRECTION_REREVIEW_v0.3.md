# NS-001 H2A2 real CPython receipt implementation correction re-review v0.3

Date: 2026-10-02 (America/New_York).
HEAD before / reviewed canonical checkpoint: `de918d0ec49edde7a795a363343902ab357edd74`.
Review branch: `codex/h2a2-v03-independent-rereview`.
Isolated worktree: `/home/jacob/.codex/worktrees/h2a2-v03-rereview/repo`.

**Implementation-slice verdict: VERIFIED WITH RESIDUAL ASSUMPTION.**
**Live-experiment readiness: READY_FOR_SEPARATE_AUTHORIZATION.**
This is not authorization to launch or attach GDB or run the live experiment.
No genuine native receipt exists from this review; E0 remains HOLD.

## Authority and method

One independent READ-ONLY OFFLINE conformance re-review of the receiver-thread
binding correction. The controlling v0.2 re-review and v0.3 correction receipt
were read as evidence, not accepted as proof. Reviewed the complete implementation
diff `de918d0^..de918d0`, the new tests, unchanged transcript/snapshot/custody,
retention/public replay paths, and frozen Q1 sections 5 and 7 and experiment
sections 6, 13. No generic fuzzing or reopening of the entire earlier audit.

The canonical checkout was clean at the requested checkpoint on
`codex/e0-h2-preparation`. A managed isolated worktree was created at that exact
checkpoint and switched to the new review branch. No existing branch was moved.
This receipt is the only repository file created or changed by this review.
Git metadata and writing this receipt in the isolated worktree use the authorized
sandbox escalation. Its eventual commit hash is reported outside its own bytes.

Independent probes use unchanged synthetic fixture builders and the existing
Store/Attempt/public_accept API, with a new standalone mutation driver under /tmp.
They do not call the new v0.3 test helpers. Fixture identity is read from custody,
then consistently rebound to PID=TID 707, preserving the existing sole-leader
admission rule. The conflicting identity is derived as 707+106=813; no 401 or 999
is hard-coded into the independent driver. Raw MI records, independent native-stop
metadata, control/admission records and capture mapping identities are altered
explicitly as described below. Every run checks durable terminal state and actual
public package replay, not merely an in-memory validation flag.

Ordinary offline Python tooling imports validators and fixtures. Protected
candidate bytes are never passed to compile/eval/exec/import. No GDB launch
(including version query), attachment, ptrace/native process control, live candidate
operation, genuine receipt, E0, dependency_runtime_lock work, merge, repair,
implementation/test edit or next bounded action occurred. These statements cover
this review's actions, not unrelated activity on the host. Git receipt publication
is the only network action. Scripts, logs and temporary stores remain outside the
repository; reproduction source and results are retained verbatim below.

## Thread-binding reproduction and source findings

The earlier concrete defect was a receiver hardware insertion result scoped to a
wrong thread while admitted/native/MI identities were correct. Independently
reproduced its semantics with admitted TID 707 and scope 813: REFUSED,
OBSERVER_UNQUALIFIED, public_accept=false. The additional requested wrong observed
receiver stop uses caller/admission 707, raw receiver MI TID 813 and native receiver
metadata 813: ABORTED, ATTEMPT_INCOMPLETE, public_accept=false. Leaving native
metadata at admitted 707 while MI reports 813 also cannot ACCEPT.

The different-live-thread variant inserts a retained thread-created event for 813
before the receiver transition and changes the receiver MI/native pair to 813.
It fails closed. This variant is deliberately outside the frozen sole-live-thread
admission policy: Transcript rejects the extra live thread before snapshot
comparison. It does not establish support for multithreaded admission. The direct
wrong-stop variants independently exercise the observed TID comparison.

Admitted identity is supplied by retained Preparation custody, then cross-checked
against sole task_ids, hardware control TIDs, retained live MI group/thread maps,
READY identity, independent native derivation/control and capture-map identity.
It is not authenticated native evidence in this synthetic review. Admission task_ids
contradicting custody refuse with OBSERVER_NOT_ARMED. Retained preparation is deep
copied; the original input bytes are checked before ATTEMPTED; public package replay
reconstructs and revalidates the retained preparation and observation.

Transcript.snapshot derives observed TID from raw *stopped thread-id, compares it
to admitted custody, and resolves the contemporaneous thread-to-group-to-PID map.
Both caller and receiver use this path independently, so both must equal admitted
TID and each other. Native stop metadata must then equal each decoded stop; supplied
expected labels cannot overwrite an MI mismatch. Both-stop equality at wrong 813
still aborts. The admitted PID/TID 707 positive baseline and explicitly matching
thread/group scope accept, including durable public replay.

The v0.3 hardware replay derives the selected group from a retained initial setup
snapshot and validates it against custody. It keeps each active site's immutable
(address, observed thread restriction, observed group restriction) tuple. Every
successful insertion and inventory readback validates explicit scope; inventory
must exactly equal active scoped history. Wrong thread, wrong process group and
unsupported task restrictions refuse. An unrestricted site remains valid only
within the existing sole-process/thread admission. There is no fallback assigning
an expected TID to an observed restriction. Empty/malformed scope is not a success
default. No hard-coded 401/999, mismatch normalization, new success default, stale
thread-state reuse, mutable alias or fixture-metadata substitution was found in
the touched implementation. Existing address/phase semantics are unchanged.

## Lifetime and RR2-RR4 preservation

Hardware history is reconstructed from successful retained commands/results across
setup and observation, retaining active IDs, scoped sites, retirement and phase
count. The receiver is installed before first continuation and cannot be deleted,
replaced or reinserted; membership is checked on every retained execution result.
Exact inventories and two-site budget remain required. An extra unexpected READY
site refuses; receiver deletion between caller and receiver aborts. Existing suite
cases cover missing insertion/retirement, unassociated results, duplicate identities,
wrong initial phase and positive full schedule. Replacing address values with
scoped tuples preserved duplicate-address and phase checks through addresses().
No final setup descriptor can backfill missing lifetime/control history.

RR2 remains closed offline: early selected-thread exit, stale recreation and
substitution fail; exit state mutates live maps, seen IDs prevent reuse, snapshots
copy maps, and capture reads check custody continuity. Valid death only after
complete final capture still accepts, including public replay. These unchanged
paths were source-reviewed and independently exercised with alternate identities.

RR3 remains closed offline: actual MI byte disagreement with supervisor/reference
at 0x500000 aborts. Matching non-site bytes at 0x500010 accept. No source change to
raw text reconciliation or parser introduced by v0.3.

RR4 remains closed offline: supported final seals fault plus malformed MI preserves
OBJECT_SUBSTITUTION; synthetic execution-guard fault plus malformed MI preserves
EXECUTION_PROHIBITED. Both abort with ATTEMPT_INCOMPLETE and public false. These
fault labels are evidence, not actual execution operations.

## Independent results

Twenty bounded probes passed their asserted expectations (4 positive ACCEPTs,
16 negative NO ACCEPTs). All use admitted TID 707 and conflicting identity 813.

| Probe | Terminal / primary | public_accept | Diagnostics |
| --- | --- | --- | --- |
| alternate_valid_admission | ACCEPTED / none | true | none |
| matching_explicit_thread_and_group | ACCEPTED / none | true | none |
| original_wrong_receiver_hardware_scope | REFUSED / OBSERVER_UNQUALIFIED | false | none |
| A_correct_caller_wrong_receiver | ABORTED / ATTEMPT_INCOMPLETE | false | none |
| A_observed_mismatch_native_metadata_unchanged | ABORTED / ATTEMPT_INCOMPLETE | false | none |
| A_other_live_thread_receiver | ABORTED / ATTEMPT_INCOMPLETE | false | none |
| B_wrong_caller_correct_receiver | ABORTED / ATTEMPT_INCOMPLETE | false | none |
| C_matching_pair_differs_from_admission | ABORTED / ATTEMPT_INCOMPLETE | false | none |
| E_admitted_exit_before_receiver | ABORTED / ATTEMPT_INCOMPLETE | false | none |
| stale_identity_recreated | ABORTED / ATTEMPT_INCOMPLETE | false | none |
| substituted_thread_after_exit | ABORTED / ATTEMPT_INCOMPLETE | false | none |
| F_terminal_death_after_completed_capture | ACCEPTED / none | true | none |
| wrong_receiver_group_scope | REFUSED / OBSERVER_UNQUALIFIED | false | none |
| custody_cannot_override_retained_admission | REFUSED / OBSERVER_NOT_ARMED | false | none |
| receiver_deletion_before_receipt | ABORTED / ATTEMPT_INCOMPLETE | false | none |
| extra_active_hardware_site | REFUSED / OBSERVER_UNQUALIFIED | false | none |
| RR3_MI_supervisor_disagreement | ABORTED / ATTEMPT_INCOMPLETE | false | none |
| RR3_matching_non_site_read | ACCEPTED / none | true | none |
| RR4_supported_substitution_diagnostic | ABORTED / ATTEMPT_INCOMPLETE | false | OBJECT_SUBSTITUTION |
| RR4_supported_execution_diagnostic | ABORTED / ATTEMPT_INCOMPLETE | false | EXECUTION_PROHIBITED |

Complete offline suite command (in the isolated worktree):

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_e0_h2_real_receipt*.py' -v
Ran 323 tests in 119.788s
OK
```

Exit 0; independently counted 323 verbose ok records, zero skips, failures or
errors. This includes all 15 v0.3 regressions and all 28 v0.2 regressions. Test
success does not override defects; no blocking defect was reproduced in the
independent cases or found in this bounded source review.

Independent reproduction command (exit 0):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:. python3 /tmp/ns001-v03-independent-probes.py
```

## Preservation

All **239 tracked checkpoint files** were byte-compared against their Git blobs at
`de918d0ec49edde7a795a363343902ab357edd74` in both canonical and isolated checkouts;
zero mismatches. This verifies implementation, all tests/fixtures, v0.3 correction
receipt, earlier review/correction receipts, frozen controlling documents and
prior H2A1/H2A2 verified slices without relying on status alone. Both trees were
clean before receipt creation. Repeat the same comparison before publication;
receipt-only staged/commit scope and canonical clean HEAD are checked separately.
No tracked baseline artifact is changed. Retained hashes below identify temporary
review evidence, not a native admission or external trust root.

| Evidence | SHA-256 |
| --- | --- |
| ns001-v03-independent-probes.py | `ae3ccb70fa3ca7b9dacf282f492564ec85d10fb25446a9afe9caa104cf13f03d` |
| ns001-v03-independent-probes.log | `853fbbc2732178f5b348462061712ee6c16ba08c6fada7e8237f14c0acedaa1c` |
| ns001-v03-suite.log | `8ae141047ee361b1b49a8f8a12cf9ba6c79639b583662a0f9ddee15271228e9a` |
| ns001-v03-preservation.json | `3e6bd92e4cd3ddbb84b0289601afb4039694fa8ab1b336d5e026158d833be7a9` |

## Verdict, claim ceiling and gates

- Thread-binding defect: CLOSED OFFLINE; all A-F cases satisfy required outcomes.
- Lifetime preservation: confirmed within this bounded retained-history review.
- RR2-RR4: remain CLOSED OFFLINE; no concrete regression reproduced.
- Blocking implementation issues: none found in this bounded scope.
- Implementation-slice verdict: **VERIFIED WITH RESIDUAL ASSUMPTION**.
- Live-experiment readiness: **READY_FOR_SEPARATE_AUTHORIZATION**. This is readiness
  for a separate authorization decision only, not live qualification or permission.
- Residual assumptions: already-declared honest host/kernel/debug hardware,
  collector/native-admission correctness, pinned tools/decoder/hash/storage,
  custody integrity and absence of hostile native writers. Retained synthetic
  records do not authenticate actual kernel hardware programming, native capture,
  live thread identity or death. No new residual assumption is introduced here.
- external_trust_root: **UNRESOLVED**; narrow provenance status unchanged; no genuine
  native receipt or full runtime integrity claim.
- dependency_runtime_lock: **UNRESOLVED; not begun**.
- H2A1: **VERIFIED + frozen**, unchanged scoped status.
- H2A2: sealed handoff VERIFIED; surrogate VERIFIED WITH RESIDUAL ASSUMPTION;
  narrow engine provenance and prospective observer/Q1 verdicts unchanged;
  this bounded real-receipt implementation re-review VERIFIED WITH RESIDUAL
  ASSUMPTION; live admission/receipt remains unperformed.
- E0: **HOLD**, unexecuted and unauthorized.
- Publication: commit/push only this receipt to the new isolated review branch;
  verify remote ref matches receipt commit. No merge into canonical.
- Next bounded action: separately authorize the frozen live admission/receipt
  experiment subject to its existing gate checks. Not authorized or performed here.

## Retained independent reproduction source

This uses original fixture builders and unchanged durable harness methods; all
new mutation logic is visible below. Its 20 result lines follow verbatim.

```python
from dataclasses import replace
import json
from pathlib import Path
import subprocess
from test_e0_h2_real_receipt_correction import CorrectionTests
from test_e0_h2_real_receipt_correction_v2 import before_step
from real_receipt_fixtures import observation
from test_e0_h2_real_receipt import X
from e0.h2.real_receipt_integration import Chunk, text_maps
from e0.h2.real_receipt_policy import mi_command

# Use fixture-supplied identity as a source, never assume a specific fixture TID.
def chunks_rebind(chunks, old, new):
    fields=('thread-id','pid','id')
    return tuple(replace(c,raw=c.raw if c.channel!='stdout' else
        rebind_raw(c.raw,old,new,fields)) for c in chunks)
def rebind_raw(raw,old,new,fields):
    for key in fields:
        raw=raw.replace(f'{key}="{old}"'.encode(),f'{key}="{new}"'.encode())
    return raw

def preparation_rebind(p,new):
    old=p.custody['tid']
    return replace(p,custody={**p.custody,'pid':new,'tid':new},
        admission={**p.admission,'task_ids':[new],'controls':[{**n,'tid':new} for n in p.admission['controls']]},
        ready=replace(p.ready,pid=new,tid=new),transcript=chunks_rebind(p.transcript,old,new),
        native_derivation=tuple({**n,'pid':new,'tid':new} for n in p.native_derivation),
        native_controls=tuple({**n,'pid':new,'tid':new} for n in p.native_controls),
        text_captures=tuple(replace(c,mapping={**c.mapping,'pid':new,'tid':new}) for c in p.text_captures))
def observation_rebind(o,old,new):
    captures=tuple(replace(c,mapping={**c.mapping,'pid':new,'tid':new}) for c in o.text_captures)
    return replace(o,transcript=chunks_rebind(o.transcript,old,new),
        native_stops=tuple({**n,'pid':new,'tid':new} for n in o.native_stops),text_captures=captures,
        maps=tuple(text_maps(captures,e) for e in ('caller','receiver')))
def scope(p,suffix,address=0x69bff0):
    marker=f'addr="0x{address:x}"'.encode(); count=0; chunks=[]
    for c in p.transcript:
        if c.channel=='stdout' and b'bkpt=' in c.raw and marker in c.raw:
            c=replace(c,raw=c.raw.replace(marker,marker+suffix)); count+=1
        chunks.append(c)
    assert count==1
    return replace(p,transcript=tuple(chunks))
def stops(o,old,new,indices,native=True):
    chunks=[]; natives=list(o.native_stops); index=0
    for c in o.transcript:
        if c.channel=='stdout' and b'*stopped,' in c.raw:
            if index in indices:
                c=replace(c,raw=rebind_raw(c.raw,old,new,('thread-id',)))
                if native: natives[index]={**natives[index],'tid':new}
            index+=1
        chunks.append(c)
    assert index==2
    return replace(o,transcript=tuple(chunks),native_stops=tuple(natives))

def run(name,expected,prep=None,change=None,memory=None,diagnostic=None):
    t=CorrectionTests(); t.setUp()
    try:
        old=t.p.custody['tid']; selected=707; other=selected+106
        t.p=preparation_rebind(t.p,selected)
        if prep: t.p=prep(t.p,selected,other)
        t.a.prepare(t.p)
        if t.a.events()[-1]['state']!='REFUSED':
            tried=t.a.attempted()
            o=observation_rebind(observation(t.p,X,t.e,tried,mutate_memory=memory),old,selected)
            if change: o=change(o,selected,other)
            t.a.finish(None,o)
        terminal=t.a.recover(); accepted=t.public()
        result=dict(probe=name,admitted_tid=selected,other_tid=other,state=terminal['state'],
            primary=terminal['primary_code'],diagnostics=terminal['diagnostics'],public_accept=accepted)
        print(json.dumps(result,sort_keys=True),flush=True)
        assert accepted is expected
        assert (terminal['state']=='ACCEPTED') is expected
        if diagnostic: assert diagnostic in terminal['diagnostics']
    finally: t.tearDown()

run('alternate_valid_admission',True)
run('matching_explicit_thread_and_group',True,prep=lambda p,a,b:scope(p,f',thread="{a}",thread-groups=["i1"]'.encode()))
run('original_wrong_receiver_hardware_scope',False,prep=lambda p,a,b:scope(p,f',thread="{b}"'.encode()))
run('A_correct_caller_wrong_receiver',False,change=lambda o,a,b:stops(o,a,b,{1}))
run('A_observed_mismatch_native_metadata_unchanged',False,change=lambda o,a,b:stops(o,a,b,{1},False))
run('A_other_live_thread_receiver',False,change=lambda o,a,b:before_step(stops(o,a,b,{1}),notification=f'=thread-created,id="{b}",group-id="i1"\n'.encode()))
run('B_wrong_caller_correct_receiver',False,change=lambda o,a,b:stops(o,a,b,{0}))
run('C_matching_pair_differs_from_admission',False,change=lambda o,a,b:stops(o,a,b,{0,1}))
run('E_admitted_exit_before_receiver',False,change=lambda o,a,b:before_step(o,notification=f'=thread-exited,id="{a}",group-id="i1"\n'.encode()))
run('stale_identity_recreated',False,change=lambda o,a,b:before_step(o,notification=f'=thread-exited,id="{a}",group-id="i1"\n=thread-created,id="{a}",group-id="i1"\n'.encode()))
run('substituted_thread_after_exit',False,change=lambda o,a,b:before_step(stops(o,a,b,{1}),notification=f'=thread-exited,id="{a}",group-id="i1"\n=thread-created,id="{b}",group-id="i1"\n'.encode()))
run('F_terminal_death_after_completed_capture',True,change=lambda o,a,b:replace(o,transcript=o.transcript+(Chunk('stdout',f'=thread-exited,id="{a}",group-id="i1"\n=thread-group-exited,id="i1",exit-code="0"\n'.encode()),)))
run('wrong_receiver_group_scope',False,prep=lambda p,a,b:scope(p,b',thread-groups=["i2"]'))
run('custody_cannot_override_retained_admission',False,prep=lambda p,a,b:replace(p,admission={**p.admission,'task_ids':[b]}))
run('receiver_deletion_before_receipt',False,change=lambda o,a,b:before_step(o,'-break-delete 1'))
run('extra_active_hardware_site',False,prep=lambda p,a,b:replace(p,transcript=p.transcript+(Chunk('commands',mi_command(5000,'-break-insert -h *0x4f6102')),Chunk('stdout',b'5000^done,bkpt={number="98",type="hw breakpoint",enabled="y",addr="0x4f6102"}\n'))))
run('RR3_MI_supervisor_disagreement',False,memory=lambda m:m.ranges.__setitem__(0x500000,bytearray(b'\xcc')))
run('RR3_matching_non_site_read',True,memory=lambda m:m.ranges.__setitem__(0x500010,bytearray(b'\x00\x00')))
run('RR4_supported_substitution_diagnostic',False,change=lambda o,a,b:replace(o,protected_final={**o.protected_final,'seals':0},transcript=o.transcript+(Chunk('stdout',b'not valid MI\n'),)),diagnostic='OBJECT_SUBSTITUTION')
run('RR4_supported_execution_diagnostic',False,change=lambda o,a,b:replace(o,guard_operations=('execution',),transcript=o.transcript+(Chunk('stdout',b'not valid MI\n'),)),diagnostic='EXECUTION_PROHIBITED')
```

```jsonl
{"admitted_tid": 707, "diagnostics": [], "other_tid": 813, "primary": null, "probe": "alternate_valid_admission", "public_accept": true, "state": "ACCEPTED"}
{"admitted_tid": 707, "diagnostics": [], "other_tid": 813, "primary": null, "probe": "matching_explicit_thread_and_group", "public_accept": true, "state": "ACCEPTED"}
{"admitted_tid": 707, "diagnostics": [], "other_tid": 813, "primary": "OBSERVER_UNQUALIFIED", "probe": "original_wrong_receiver_hardware_scope", "public_accept": false, "state": "REFUSED"}
{"admitted_tid": 707, "diagnostics": [], "other_tid": 813, "primary": "ATTEMPT_INCOMPLETE", "probe": "A_correct_caller_wrong_receiver", "public_accept": false, "state": "ABORTED"}
{"admitted_tid": 707, "diagnostics": [], "other_tid": 813, "primary": "ATTEMPT_INCOMPLETE", "probe": "A_observed_mismatch_native_metadata_unchanged", "public_accept": false, "state": "ABORTED"}
{"admitted_tid": 707, "diagnostics": [], "other_tid": 813, "primary": "ATTEMPT_INCOMPLETE", "probe": "A_other_live_thread_receiver", "public_accept": false, "state": "ABORTED"}
{"admitted_tid": 707, "diagnostics": [], "other_tid": 813, "primary": "ATTEMPT_INCOMPLETE", "probe": "B_wrong_caller_correct_receiver", "public_accept": false, "state": "ABORTED"}
{"admitted_tid": 707, "diagnostics": [], "other_tid": 813, "primary": "ATTEMPT_INCOMPLETE", "probe": "C_matching_pair_differs_from_admission", "public_accept": false, "state": "ABORTED"}
{"admitted_tid": 707, "diagnostics": [], "other_tid": 813, "primary": "ATTEMPT_INCOMPLETE", "probe": "E_admitted_exit_before_receiver", "public_accept": false, "state": "ABORTED"}
{"admitted_tid": 707, "diagnostics": [], "other_tid": 813, "primary": "ATTEMPT_INCOMPLETE", "probe": "stale_identity_recreated", "public_accept": false, "state": "ABORTED"}
{"admitted_tid": 707, "diagnostics": [], "other_tid": 813, "primary": "ATTEMPT_INCOMPLETE", "probe": "substituted_thread_after_exit", "public_accept": false, "state": "ABORTED"}
{"admitted_tid": 707, "diagnostics": [], "other_tid": 813, "primary": null, "probe": "F_terminal_death_after_completed_capture", "public_accept": true, "state": "ACCEPTED"}
{"admitted_tid": 707, "diagnostics": [], "other_tid": 813, "primary": "OBSERVER_UNQUALIFIED", "probe": "wrong_receiver_group_scope", "public_accept": false, "state": "REFUSED"}
{"admitted_tid": 707, "diagnostics": [], "other_tid": 813, "primary": "OBSERVER_NOT_ARMED", "probe": "custody_cannot_override_retained_admission", "public_accept": false, "state": "REFUSED"}
{"admitted_tid": 707, "diagnostics": [], "other_tid": 813, "primary": "ATTEMPT_INCOMPLETE", "probe": "receiver_deletion_before_receipt", "public_accept": false, "state": "ABORTED"}
{"admitted_tid": 707, "diagnostics": [], "other_tid": 813, "primary": "OBSERVER_UNQUALIFIED", "probe": "extra_active_hardware_site", "public_accept": false, "state": "REFUSED"}
{"admitted_tid": 707, "diagnostics": [], "other_tid": 813, "primary": "ATTEMPT_INCOMPLETE", "probe": "RR3_MI_supervisor_disagreement", "public_accept": false, "state": "ABORTED"}
{"admitted_tid": 707, "diagnostics": [], "other_tid": 813, "primary": null, "probe": "RR3_matching_non_site_read", "public_accept": true, "state": "ACCEPTED"}
{"admitted_tid": 707, "diagnostics": ["OBJECT_SUBSTITUTION"], "other_tid": 813, "primary": "ATTEMPT_INCOMPLETE", "probe": "RR4_supported_substitution_diagnostic", "public_accept": false, "state": "ABORTED"}
{"admitted_tid": 707, "diagnostics": ["EXECUTION_PROHIBITED"], "other_tid": 813, "primary": "ATTEMPT_INCOMPLETE", "probe": "RR4_supported_execution_diagnostic", "public_accept": false, "state": "ABORTED"}
```

Finish here. No repair, merge, live experiment, dependency lock or next action.
