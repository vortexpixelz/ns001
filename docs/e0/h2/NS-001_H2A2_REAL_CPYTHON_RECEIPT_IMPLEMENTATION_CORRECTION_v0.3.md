# NS-001 H2A2 real CPython receipt implementation correction v0.3

Date: 2026-10-02 (America/New_York).
Branch: `codex/e0-h2-preparation`.
HEAD before: `82a8d3b89f48a61df3a816d38995fb9a70bebf7f`.

**Implementation verdict: PASS. Sole remaining receiver-thread scope blocker CLOSED OFFLINE.**
Live admission/receipt remains unperformed and readiness **NOT_READY**. Offline PASS
does not authorize or establish a live experiment or genuine native receipt.

## Authority and files changed

One bounded OFFLINE correction of the single remaining RR1 thread-scope omission.
Frozen Q1/observer/experiment/input-boundary contracts remain controlling. No redesign,
new refusal code, reopened prior finding or substantive frozen-design change.

Exactly three authorized repository paths are changed/added:

- `e0/h2/real_receipt_integration.py`
- `tests/test_e0_h2_real_receipt_correction_v3.py`
- `docs/e0/h2/NS-001_H2A2_REAL_CPYTHON_RECEIPT_IMPLEMENTATION_CORRECTION_v0.3.md`

The receipt's resulting commit hash and push verification are reported outside its
own bytes. No prior receipt or test fixture is rewritten.

## Receiver-thread binding result

**CLOSED OFFLINE.** The retained independent v0.2 re-review changes the receiver
hardware insertion result to `thread="999"`, while both native/MI stops and admitted
custody remain TID 401. The attached instruction additionally requires a receiver
stop reporting 999. These are distinct raw evidence mutations; both are tested.

Before this correction, stop snapshots already derive their TID independently from
retained `*stopped` records. They require that observed TID to equal admitted custody
and resolve its contemporaneous live group to admitted PID. Native-stop TID must match
the decoded stop. Existing live-state/exit/reuse checks remain unchanged; no expected
label overwrites an observed stop mismatch. The omitted monitor-scope fact was the
concrete public-ACCEPT defect, not a missing stop-TID comparison.

Hardware replay now retains `(address, observed thread restriction, observed group
restriction)` for each active identity, rather than address alone. It derives the
selected process group from the first retained live setup snapshot for admitted
PID/TID and requires that identity to exist. Every successful insertion and inventory
readback checks explicit thread/process scope against that selected identity. Wrong
thread/group restrictions and unsupported task restrictions fail closed. Inventory
readback must agree with retained scoped state; it cannot silently drop/change scope.
Unrestricted sites remain valid under the frozen sole-process/thread admission.
Explicit scope matching the admitted thread remains valid. The monitor qualification
fact now includes retained scope as well as lifetime/inventory membership.

The existing sequential temporary-site schedule, retirement rules, slot budget,
stop custody, public replay and native-control checks remain in place. All selected
thread comparisons use submitted admitted identity plus retained evidence. No TID 401
or 999 is hard-coded into the implementation. A conforming alternate sole-leader
PID=TID 707 with matching receiver scope passes actual durable attempt and public replay;
using the old 401 scope against that admission refuses.

Frozen Q1 section 5 requires expected inferior/thread scope and section 7 continuous
receiver coverage. This repair enforces those existing requirements without changing
experiment semantics, schema, ranking or parser budgets.

## Faithful reproductions

The standalone Python block in correction re-review v0.2 was extracted byte-for-byte
outside the repository. Source SHA-256:
`ae8fa911c8262da3467a9d0b516ebc3351155d076bf48eda54bb3f98621352ff`.
It changes exactly one retained receiver insertion result; no stop/native-control,
address, slot, token, custody, completion or payload bytes change.

Before repair at the requested HEAD (exit 0):

```text
{"probe": "NEW_RR1_receiver_monitor_wrong_thread_scope", "state": "ACCEPTED", "primary": null, "diagnostics": [], "public_accept": true}
```

After repair (exit 0):

```text
{"probe": "NEW_RR1_receiver_monitor_wrong_thread_scope", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "OBSERVER_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "82a51346c965717a9000dcc9a49a41ec125f07bb7e7a7cac1d0f7a24647cc2dc"}, "public_accept": false}
```

The second bounded reproduction preserves the valid caller/admission and changes only
the receiver MI stop's observed TID to 999. It uses the unchanged retained run helper
and this mutation (also durably represented by the new regression):

```python
def wrong_receiver_stop(o):
    changed = 0
    chunks = []
    for c in o.transcript:
        if c.channel == 'stdout' and b'*stopped,' in c.raw and b'addr="0x69bff0"' in c.raw:
            c = replace(c, raw=c.raw.replace(b'thread-id="401"', b'thread-id="999"'))
            changed += 1
        chunks.append(c)
    assert changed == 1
    return replace(o, transcript=tuple(chunks))
run('receiver_stop_999_admitted_caller_401', change_o=wrong_receiver_stop)
```

Exact result (exit 0):

```text
{"probe": "receiver_stop_999_admitted_caller_401", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "diagnostics": [], "public_accept": false}
```

NO ACCEPT; public_accept=false in both cases. Existing frozen refusal/recovery paths
are used: OBSERVER_UNQUALIFIED for the admission-scope contradiction and recovery-only
ATTEMPT_INCOMPLETE for invalid observed stop association.

| Evidence | SHA-256 |
| --- | --- |
| Scope source | `ae8fa911c8262da3467a9d0b516ebc3351155d076bf48eda54bb3f98621352ff` |
| Scope before output | `72fed07daff4a8c7b2f0b6bc667925edde096d5055be6869db9f5d746d5ca618` |
| Scope after output | `b88f19b3c230f6f0e472ac3f7d88cec6d2bad2878a40596550f2b2fb0110f753` |
| Receiver-stop source | `5520c6d214b27d7795da09a12d1db3605bee92ada22763fae2f9e495475a990b` |
| Receiver-stop output | `1f3a60689e706f203d82f38d66dab1ad76a9e26f44251ff8c9c932136ba9851c` |

## Nearby regression inventory

**15 new bounded regressions**, synthetic captures and local temporary stores only.
Includes all six requested nearby cases and targeted monitor-scope/public-replay
checks. No concurrency fuzzing or alternative observer was introduced.

- `test_exact_rereview_receiver_monitor_scope_999`
- `test_caller_monitor_wrong_scope`
- `test_caller_stop_wrong_TID`
- `test_receiver_stop_wrong_TID`
- `test_both_stops_match_each_other_but_not_admitted_TID`
- `test_receiver_native_TID_cannot_replace_MI_mismatch`
- `test_other_created_live_thread_cannot_supply_receiver`
- `test_correct_unrestricted_baseline`
- `test_correct_explicit_selected_scope`
- `test_wrong_process_group_scope`
- `test_inventory_cannot_change_receiver_scope`
- `test_exit_before_receiver_fails_closed`
- `test_terminal_death_after_capture_remains_permitted`
- `test_generic_selected_TID_707_positive`
- `test_generic_selected_TID_707_rejects_old_401_scope`

Targeted final run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:. python3 -m unittest test_e0_h2_real_receipt_correction_v3 -v
Ran 15 tests in 12.268s
OK
```

15 PASS; 0 skips, failures/errors; exit 0. An initial development test constructor
used PID 401 with TID 707, violating the existing frozen sole-leader admission rule.
The constructor was corrected to PID=TID 707; that admission policy was not changed.

## Prior closures and full offline suite

All retained real-receipt tests ran. The prior 28 v0.2 regressions still pass, including
monitor deletion/history and complete temporary schedule, thread exit/stale identity,
MI/supervisor text contradiction/matching non-site reads, supported diagnostic
persistence, no fabricated diagnostics and terminal death after completed capture.

R3 frozen tool roles, R5 dictionary ABI width, R6 lock custody, R7 immutable admission
and exact bools, and R8 mandatory package inventory remain CLOSED OFFLINE within their
existing scoped tests. No redesign or implementation change in those areas. The new
scope check is exercised again during public package replay; positive baselines replay
successfully and negative admission/stop cases cannot publicly accept.

Final complete command and exact summary:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_e0_h2_real_receipt*.py' -v
Ran 323 tests in 119.917s

OK
```

**323 PASS; 0 skips; 0 failures/errors; exit 0.** Independently counted 323 verbose
`... ok` records. Includes 161 original, 67 completion, 52 v0.1 correction, 28 v0.2
correction and 15 v0.3 correction tests. Both bounded standalone reproductions exit 0.

Complete suite log SHA-256: `03eae87d895b7102d0fa6f387b54c18272eb7aeb193375456a57e37af18c5ff6`.
Targeted log SHA-256: `41cba597e1f9c8af872883e38aa4812148aafb108e1d4c7e0e944b239af10ee2`.

## Preservation and precommit scope

Initial HEAD and branch matched the requested canonical checkpoint; tree and index
were clean. All **237** tracked checkpoint files were inventoried before any edits.
**236 other tracked files remain SHA-256 byte-identical**; only the authorized
integration module is modified. The new regression module and this exactly one v0.3
receipt complete the three-file allowlist. Baseline inventory JSON SHA-256:
`6d19115c1022775ff0a24961c88e5d0747cd937e377f5b7834a1d2699063ee71`.

This includes unchanged frozen controlling documents, H2A1, prior verified H2A2
slices, engine provenance, observer design, experiment design, Q1 and all prior
implementation/review/correction receipts, including both independent correction
re-reviews and v0.2 correction. Policy, evidence, ABI, observation/parser modules,
existing tests and synthetic fixture remain unchanged.

Before staging/commit, verify exact allowlist, all 236 preservation hashes, clean
otherwise tracked/untracked tree, empty preexisting index, and no whitespace errors.
Commit/push is limited to these three paths on codex/e0-h2-preparation. The resulting
commit and remote ref verification are external to this receipt's bytes.

Static file hashes (files read only; none launched for this check):

| File | SHA-256 |
| --- | --- |
| /usr/bin/python3.12 | `e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f` |
| /usr/bin/gdb | `3832cc070ae1716e322105d3b39fb398695e5f031c9d39224cf227a8c2b889f6` |
| /lib64/ld-linux-x86-64.so.2 | `c20a2dc8917c755f02b94049356320fe1f62ac7d9f8994731f807d9df39302da` |

**NO LIVE GDB / NO REAL CANDIDATE COMPILE.** No GDB launch/version query/attachment,
ptrace/native control, real candidate compile/eval/exec/import, live receipt experiment,
E0/scientific/client execution, dependency_runtime_lock, package/tool mutation or
qualified-artifact mutation occurred. Offline Python imports validators/test fixtures;
protected source remains literal bytes. Temporary scripts/logs/stores remain outside
the repository. Authorized Git publication is the only network operation planned.
This statement covers this circuit's actions, not unrelated host activity.

## Residual assumptions, verdict and unchanged gates

Synthetic/retained evidence validation does not authenticate an actual native capture.
Host/kernel/debug hardware, native collector correctness, pinned tools/decoder,
storage/custody integrity and absence of hostile native writers remain residual
assumptions. Actual operational hardware programming, memory reads, trap reasons,
thread custody/death and live admission/receipt remain unperformed. PASS is bounded
to the repaired sole blocker and retained offline tests, not proof of all future inputs.

- Receiver-thread binding: **CLOSED OFFLINE**.
- Implementation verdict: **PASS**; no reproduced false public ACCEPT remains.
- Frozen substantive semantics: unchanged; no design contradiction found.
- external_trust_root: **UNRESOLVED**; no genuine native receipt.
- dependency_runtime_lock: **UNRESOLVED; not begun**.
- H2A1: **VERIFIED + frozen**, unchanged scoped status.
- H2A2: sealed handoff VERIFIED; surrogate VERIFIED WITH RESIDUAL ASSUMPTION;
  narrow engine provenance and prospective observer/Q1 verdicts unchanged;
  this bounded offline implementation correction PASS, pending separate independent
  checkpoint re-review; live admission/receipt unperformed, readiness NOT_READY.
- E0: **HOLD**, unexecuted and unauthorized.
- One next bounded action: separately authorize an independent READ-ONLY OFFLINE
  re-review of this committed correction checkpoint. Not performed here.

Finish here. No live experiment or next action performed.
