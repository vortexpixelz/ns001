# NS-001 H2A2 real CPython receipt implementation correction re-review v0.2

Date: 2026-10-01 (America/New_York).
HEAD before / reviewed checkpoint: `cda7eaa8f0bd8b62eb2f1e90d3961459c7fb29e1`.
Review branch: `codex/h2a2-v02-independent-rereview`.

**PARTIAL. Live-experiment readiness: NOT_READY.** The exact RR1-RR4 reproductions
now fail closed or preserve their required diagnostics. However, an equivalent RR1
monitor-coverage omission remains: retained receiver breakpoint scope for thread 999
is publicly accepted for receipt TID 401. The complete suite independently passes
308 tests with zero skips, failures or errors. Passing tests do not override this
reproduced conformance defect. No implementation or test repair is performed.

## Authority and method

One independent READ-ONLY OFFLINE conformance review of the v0.2 correction, followed
by exactly this receipt's commit and push on an isolated review branch. Controlling
rereview v0.1 and correction v0.2 were read as evidence, not trusted verdicts.
Reviewed the actual four-file correction diff against `5d26b68a665b7af07a33cb99fd765da47995873b`,
including the 192-line integration change and synthetic fixture schedule update.
Reviewed Transcript, setup/observation decoding, hardware replay, text reconciliation,
predecode persistence and public package replay, and spot-checked prior closed paths.
Frozen Q1/experiment contracts control the scope and phase conclusions.

The supplied isolated worktree began clean at detached `d9dcfbef1bea173b316bc968fd71421c982422c3`.
The canonical checkpoint already existed locally. The worktree was switched to a new
review branch at that exact checkpoint; canonical was not changed or merged.
Git metadata writes required sandbox escalation, which was approved. HEAD before
means the independently reviewed checkpoint. The eventual receipt commit is reported
outside its own bytes to avoid self-reference.

Temporary scripts, logs and synthetic stores stayed under /tmp. Ordinary offline
Python tooling imported validators and fixtures; protected candidate source stayed
literal bytes. No candidate compile/eval/exec/import, GDB launch (including version
query), GDB attachment, ptrace/live process control, native experiment, E0,
dependency_runtime_lock, package mutation or next bounded action occurred.
Only authorized Git publication uses the network. No generic fuzzing was performed.

## RR1-RR4 independent dispositions

| Finding | Faithful retained reproduction | Independent disposition |
| --- | --- | --- |
| RR1 receiver deletion | Successful `-break-delete 1` after caller snapshot, before CALL; shifted later MI/native tokens faithfully. ABORTED / ATTEMPT_INCOMPLETE; public false. | Exact deletion and extra-site cases corrected; RR1 remains PARTIAL because scope is omitted. |
| RR1 extra READY hardware | Enabled additional wrapper hardware site at `0x4f6102`, retaining earlier sites. REFUSED / OBSERVER_UNQUALIFIED; public false. | Active count/history rejects the extra site. |
| RR2 thread exit | Exact `=thread-exited,id="401",group-id="i1"` between caller and receiver. ABORTED / ATTEMPT_INCOMPLETE; public false. | CLOSED OFFLINE. |
| RR3 raw text disagreement | Actual addressed MI byte `cc` at `0x500000`, supervisor/reference `00`. ABORTED / ATTEMPT_INCOMPLETE; public false. | CLOSED OFFLINE. Matching non-site read remains ACCEPTED/public true. |
| RR4 supported diagnostic | Final seals 15 -> 0 plus malformed MI. ABORTED / ATTEMPT_INCOMPLETE with OBJECT_SUBSTITUTION; public false. | CLOSED OFFLINE. Execution guard plus incomplete completion retains EXECUTION_PROHIBITED. |

RR1's new replay carries active IDs/addresses from setup through observation, rejects
receiver retirement, duplicate/reused IDs, extra sites, incorrect temporary phases,
unassociated insertion results and inventory disagreement. Receiver remains in the
replayed inventory and active count is derived rather than fixed. The frozen sequence
(wrapper, pread return spanning syscall stops, post-resize, wrapper RET, blocked READY,
then caller) is reflected in retained fixture commands. Missing insert/retire variants
refuse and the full positive schedule accepts. However, membership/address alone
cannot establish qualifying receiver coverage for the selected thread; see blocker.

RR2 updates live thread/group maps on exits, snapshots contemporaneous maps, prevents
reuse with seen-ID sets, checks custody before subsequent reads and rejects premature
exit or commands after terminal death. Native and MI stops both bind to selected
PID/TID. Exact exit, process exit, stale recreation and unowned exit refuse. Baseline
and expected thread/group death after complete captures remain accepted. No stale
identity restoration or swallowed custody event was found in the touched path.

RR3 walks each stopped actual MI read, checks bounded addressed intersections with
that epoch's executable capture, and compares measured bytes to supervisor bytes.
Supervisor captures remain independently checked against complete frozen reference
bytes and map identity. Snapshot rejects ambiguous overlapping reads. Mandatory CALL
and receiver-site measurements remain actual reads; absent measurement cannot be
filled by reference data. Setup/READY comparisons and caller/receiver comparisons use
the same reconciliation routine. Non-site matching read at `0x500010` accepts;
other-address disagreement, overlap and overflow tests refuse. No 0x500000-specific
hack or expected-data fallback was found. Transcript 8 MiB, MI parser 8 MiB, 65,536-byte
line/read, canonical 8 MiB and separate binary 4 MiB bounds remain unchanged.

RR4 gathers supported guard, protected-final, dispatch, source-capture and map faults
before parsing, persists supported-faults.json and retains original capture bytes.
Later decode failure recovers using that file and unchanged ranking. Ancillary map
exceptions do not erase supported guard/object faults. Guard + incomplete completion,
malformed MI, combined guard/object + interruption and map fault + malformed MI retain
their diagnostics. Malformed MI alone has diagnostics=[]; no fault is fabricated.
Frozen recovery primary ATTEMPT_INCOMPLETE and normal refusal precedence remain intact.

## Concrete remaining blocker: receiver hardware scope omitted

Source: `e0/h2/real_receipt_integration.py:102-107`, `:1248-1264`, `:1300-1302`,
`:634`, `:675-676`; public replay at `:901-903` reuses the same decoder.
Authority: frozen GDB Q1 section 5 requires the expected inferior/thread scope;
section 7 requires actual receiver coverage throughout the qualified interval.

One bounded synthetic case changes exactly one retained receiver insertion result:

```text
before: bkpt={number="1",type="hw breakpoint",enabled="y",addr="0x69bff0"}
after:  bkpt={number="1",type="hw breakpoint",enabled="y",addr="0x69bff0",thread="999"}
receipt custody TID: 401
```

No command, site, slot, token, byte, native stop, native-control fixture, completion
or custody value is changed. The supplied result now explicitly restricts the
receiver monitor to a different, unowned thread. A result contradicting the permitted
unrestricted insertion/selected-thread custody must refuse; the validator cannot
silently ignore this extra supported scope fact or substitute the native-control
fixture for that contradiction.

Transcript checks type, enabled, address and selected forbidden fields but ignores
thread scope. Hardware replay stores only number -> address. `monitor_armed` tests
receiver-ID membership, so the derived sentinel/Q1 witness claims qualifying coverage
without checking scope. Public verification faithfully replays the same omission.

Observed twice with distinct temporary stores (first after retained probes, then in
an isolated standalone run): **ACCEPTED; primary=null; diagnostics=[]; public_accept=true**.
This is a false ACCEPT of contradictory retained evidence, not a claim about an
actual native run. The omission is present in the pre-v0.2 insertion validation;
v0.2's new history representation still drops it. Thus it is a remaining equivalent
RR1 omission, not evidence that v0.2 newly introduced the scope bug. No separate new
regression in the other touched invariants was reproduced. No repair is proposed or
implemented by this review.

## Prior closed spot-checks

R3 remains CLOSED OFFLINE: all eleven frozen role replacements refuse; changed-tool
repetition has [ACCEPTED, REFUSED] and compare_repetition=False. R5 remains CLOSED
OFFLINE: invalid 256-slot one-byte table refuses, valid two-byte table decodes compile.
R6 remains CLOSED OFFLINE: replaced-lock stale writer and new writer both Invalid;
ordinary competitor denied, original normal custody valid. R7 remains CLOSED OFFLINE:
detached preparation mutation refuses; integer completion values abort; exact bools
are required. R8 remains CLOSED OFFLINE for mandatory inventory: rehashed capture and
native-stop omissions cannot publicly accept; historical ACCEPTED journal unchanged.
Public replay still inherits the newly demonstrated RR1 scope omission. These are
spot-checks, not a reopened full audit of R3/R5/R6/R7/R8.

## Independently executed verification

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_e0_h2_real_receipt*.py' -v
Ran 308 tests in 115.527s
OK
```

Exit 0; 308 PASS, 0 skips, 0 failures/errors. Verbose records independently counted.
Separate faithful v0.2 rerun:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:. python3 -m unittest test_e0_h2_real_receipt_correction_v2 -v
Ran 28 tests in 25.182s
OK
```

Exit 0; 28 PASS, zero skips/failures/errors. Includes valid matching non-site text,
terminal-death baseline, complete phase schedule, no-fabrication and recovery checks.

Retained Python blocks from rereview v0.1 were extracted byte-for-byte and run outside
the repository: probes.py, text-probe.py, supplement.py. The original review source
hash is 2547282264b0924cd13a7040dc9b4843301f909c2ef815e36f966f4618f3c88e;
its unchanged prefix hash is cfa7ae2f90fb6f58080d367f11ec606f28ca7da2269fbc4e28320013341dcdba.
Original lock/repetition tails use the faithful rereview adaptations recording their
now-correct refusals. Exactly 65 historical reproduction output records were rerun
and inspected (35 probes, 1 text, 10 supplement, 19 original prefix). All scripts exit
0; only explicit expected lock/competitor Invalid outputs occur. The additional scope
case is separate from those 65 and is retained below. Tests do not authenticate
synthetic evidence as genuine native events.

| Evidence | SHA-256 |
| --- | --- |
| complete suite | `52b0288e62b1ba17be718444112e8dd436bf5cf2dd23745785b34ce33b949e29` |
| 28-test rerun | `5a5d00a98f80406776621759b5e8b9d3a496ad95adc81f976ba691e573bdfe9f` |
| inventory | `1cf18184de623de6c5a9b8ec8f1c59a041e3496a597b233f8fd9d8bf074af7dd` |
| probes.py | `32a98d9afcfbf09ba99b3d90fecbe88f9a698ced7b46e2563482a7d21c4eac19` |
| text-probe.py | `011609aa097ddbaa7a1aa616ff60299cdce29414495a8670adbe0478023814e0` |
| supplement.py | `73bcc844adecefc10a5bec0c362d6188305e97c7f9d5b353986ef04377bc2574` |
| original-prefix.py | `cfa7ae2f90fb6f58080d367f11ec606f28ca7da2269fbc4e28320013341dcdba` |
| probes plus scope output | `d5a8ff3f20a86d69619f00597219aff1b41c5cd4e16679420f3d2cbfea4d8c27` |
| text output | `334c52c01e89ef74e801a66a89df59901b2cec4b08711120f2345211d35958d9` |
| supplement output | `9da1e51b34d1dd05a01f214e2d70e0475f93a5cb77f7c371897abfdec919e79a` |
| original prefix output | `85e8292d47c22bb809a64d59d060e420a36431fff8789172d01bc373d41a71f9` |
| standalone scope source | `ae8fa911c8262da3467a9d0b516ebc3351155d076bf48eda54bb3f98621352ff` |
| standalone scope output | `72fed07daff4a8c7b2f0b6bc667925edde096d5055be6869db9f5d746d5ca618` |

## Preservation

All 236 tracked checkpoint files were hashed and checked byte-for-byte against
`git show cda7eaa:<path>` after analysis; zero changes. The inventory was also rechecked
against working files. This includes implementation/tests, correction v0.2, rereview
v0.1, all frozen controlling documents and prior verified H2A1/H2A2 slices. Initial
and post-analysis tracked diffs were empty. The only added repository path is this
receipt. Comparing pre-implementation `345c6497f4d715a5131e0ca386fd8eea9b221c6e`
with checkpoint lists only 16 additive real-receipt modules/tests/receipts; no earlier
frozen file or prior slice was modified. No merge or canonical update is performed.

Selected authority hashes independently computed:

| Document | SHA-256 |
| --- | --- |
| NS-001_H2A2_REAL_CPYTHON_ENGINE_OBSERVER_QUALIFICATION_v0.1.md | `289d9b8dfb45fe518e4da33ef15bf3c9f26fa26c42ca6082b6276c8d3ce39865` |
| NS-001_H2A2_REAL_CPYTHON_ENGINE_PROVENANCE_REVIEW_v0.1.md | `3fd49cf843b582ddffed971281e226c2d1f419462c17150ca48e82a3b649453e` |
| NS-001_H2A2_REAL_CPYTHON_GDB_Q1_REVIEW_v0.1.md | `6ae726ee2bb2821e4f0a0667f4d4dcefcdd07d49dfdf6e1e0b32d35007eb9339` |
| NS-001_H2A2_REAL_CPYTHON_INPUT_BOUNDARY_SPEC_v0.1.md | `eae004d95046d2c2a83fd7813f4b0485ce792e358403a406859280f4c0fdc564` |
| NS-001_H2A2_REAL_CPYTHON_NATIVE_OBSERVER_DESIGN_v0.1.md | `cdca62d5f02a468353d4c0ba9113e3d4ced047f4b78f68c949b1141bbad1b075` |
| NS-001_H2A2_REAL_CPYTHON_RECEIPT_EXPERIMENT_DESIGN_v0.1.md | `b120fb71ca537d84926e0b81173d1f867f9e92cbde0c54696191c0a8cafee54d` |
| NS-001_H2A2_REAL_CPYTHON_RECEIPT_IMPLEMENTATION_COMPLETION_v0.1.md | `72362b1a3be2441f3c99fd10979a80d48efe48298cceb2655c065bfbf66b75b4` |
| NS-001_H2A2_REAL_CPYTHON_RECEIPT_IMPLEMENTATION_CORRECTION_REREVIEW_v0.1.md | `ac2fbb7724b2be87eae8d05caf3d136d5286e3a7a06b2e2548f767e84d60b54b` |
| NS-001_H2A2_REAL_CPYTHON_RECEIPT_IMPLEMENTATION_CORRECTION_v0.1.md | `7bdd4a4c3d482043fe02ebc8463994d7930218216af853e9b6746ac1c65eeb17` |
| NS-001_H2A2_REAL_CPYTHON_RECEIPT_IMPLEMENTATION_CORRECTION_v0.2.md | `95af0c44dfae262500d577673c27dd20605e877d2ca22864d649141ed887f5e3` |
| NS-001_H2A2_REAL_CPYTHON_RECEIPT_IMPLEMENTATION_REVIEW_v0.1.md | `097f63ffc52313e36b8c3c5bd4e508364f220a9c44d81af506a7c954fb056cc9` |
| NS-001_H2A2_REAL_CPYTHON_RECEIPT_IMPLEMENTATION_v0.1.md | `1a8e7dce6aa3071c577623d78156e4d2c0067296d4f078f98ea7239e222f53b4` |

## Standalone bounded reproduction source and exact result

```python
"""Bounded offline review reproductions; repository sources/tests stay unchanged."""
import copy
from dataclasses import replace
import json
from pathlib import Path
import sys
import tempfile
sys.path.insert(0, str(Path.cwd() / 'tests'))
sys.path.insert(0, str(Path.cwd()))
from real_receipt_fixtures import preparation, observation, freeze
from test_e0_h2_real_receipt import NS, X, request, B, DK, DICT, Memory
from e0.h2.real_receipt_policy import canonical, digest, mi_command
from e0.h2.real_receipt_evidence import Store, public_accept
from e0.h2.real_receipt_integration import Chunk, preparation_codes, verify_package, _all_files
from e0.h2.real_receipt_abi import Decoder, Snapshot

def run(label, change_p=None, change_o=None, after_freeze=None, after_attempted=None, mutate_memory=None):
    with tempfile.TemporaryDirectory(prefix='ns001-review-') as td:
        store = Store(Path(td) / 'store', NS, create=True)
        try:
            e, p = preparation(X)
            if change_p:
                e, p = change_p(e, p)
            freeze(store, e, p)
            if after_freeze:
                p = after_freeze(p)
            a = store.reserve(e, request(e))
            a.prepare(p)
            if a.events()[-1]['state'] == 'REFUSED':
                return print(json.dumps(dict(probe=label, result=a.events()[-1], public_accept=public_accept(a, a.raw('package-manifest.json'), a.raw('package-manifest.sha256'), _all_files(a), set()))))
            tried = a.attempted()
            if after_attempted:
                after_attempted(p, a)
            o = observation(p, X, e, tried, mutate_memory=mutate_memory)
            if change_o:
                o = change_o(o)
            a.finish(None, o)
            terminal = a.recover()
            print(json.dumps(dict(probe=label, state=terminal['state'], primary=terminal.get('primary_code'), diagnostics=terminal.get('diagnostics'),
                public_accept=public_accept(a, a.raw('package-manifest.json'),
                    a.raw('package-manifest.sha256'), _all_files(a), set()))))
        except Exception as exc:
            print(json.dumps(dict(probe=label, error=type(exc).__name__, message=str(exc))))
        finally:
            store.close()



from e0.h2.real_receipt_integration import Transcript

def wrong_scope(e,p):
    changed=0
    chunks=[]
    for c in p.transcript:
        if c.channel=='stdout' and b'addr="0x69bff0"' in c.raw and b'bkpt=' in c.raw:
            c=replace(c,raw=c.raw.replace(b'addr="0x69bff0"',b'addr="0x69bff0",thread="999"'))
            changed+=1
        chunks.append(c)
    assert changed==1
    p=replace(p,transcript=tuple(chunks))
    t=Transcript(p.transcript)
    monitor=next(r.fields['bkpt'] for r in t.results.values() if r.fields.get('bkpt',{}).get('addr')==b'0x69bff0')
    assert monitor['thread']==b'999' and p.custody['tid']==401
    return e,p
run('NEW_RR1_receiver_monitor_wrong_thread_scope',change_p=wrong_scope)
```

```text
{"probe": "NEW_RR1_receiver_monitor_wrong_thread_scope", "state": "ACCEPTED", "primary": null, "diagnostics": [], "public_accept": true}
```

## Exact rerun reproduction outputs

### probes-and-scope.log

```text
{"probe": "R1_faithful_premature_receiver_fresh_token", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "OBSERVER_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "82a51346c965717a9000dcc9a49a41ec125f07bb7e7a7cac1d0f7a24647cc2dc"}, "public_accept": false}
{"probe": "R1_faithful_software_diagnostic_fresh_token", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "OBSERVER_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "82a51346c965717a9000dcc9a49a41ec125f07bb7e7a7cac1d0f7a24647cc2dc"}, "public_accept": false}
{"probe": "R1_other_unqualified_history", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "OBSERVER_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "82a51346c965717a9000dcc9a49a41ec125f07bb7e7a7cac1d0f7a24647cc2dc"}, "public_accept": false}
{"probe": "NEW_R1_monitor_deleted_between_caller_receiver", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "diagnostics": [], "public_accept": false}
{"probe": "NEW_R1_extra_hardware_site_through_READY", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "OBSERVER_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "82a51346c965717a9000dcc9a49a41ec125f07bb7e7a7cac1d0f7a24647cc2dc"}, "public_accept": false}
{"probe": "NEW_R2_thread_exit_before_receiver", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "diagnostics": [], "public_accept": false}
{"probe": "R2_unexpected_async_record", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "diagnostics": [], "public_accept": false}
{"probe": "R2_duplicate_running_same_thread", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "diagnostics": [], "public_accept": false}
{"probe": "R3_frozen_role_controller", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "ENGINE_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "00a91dfd0bc3dd8afda69ef79862b2f31d367b12e4a414340f445dd1c14a0139"}, "public_accept": false}
{"probe": "R3_frozen_role_launcher_gdb", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "ENGINE_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "00a91dfd0bc3dd8afda69ef79862b2f31d367b12e4a414340f445dd1c14a0139"}, "public_accept": false}
{"probe": "R3_frozen_role_launcher_cpython", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "ENGINE_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "00a91dfd0bc3dd8afda69ef79862b2f31d367b12e4a414340f445dd1c14a0139"}, "public_accept": false}
{"probe": "R3_frozen_role_bootstrap", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "ENGINE_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "00a91dfd0bc3dd8afda69ef79862b2f31d367b12e4a414340f445dd1c14a0139"}, "public_accept": false}
{"probe": "R3_frozen_role_mi_parser", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "ENGINE_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "00a91dfd0bc3dd8afda69ef79862b2f31d367b12e4a414340f445dd1c14a0139"}, "public_accept": false}
{"probe": "R3_frozen_role_decoder", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "ENGINE_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "00a91dfd0bc3dd8afda69ef79862b2f31d367b12e4a414340f445dd1c14a0139"}, "public_accept": false}
{"probe": "R3_frozen_role_hash_tool", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "ENGINE_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "00a91dfd0bc3dd8afda69ef79862b2f31d367b12e4a414340f445dd1c14a0139"}, "public_accept": false}
{"probe": "R3_frozen_role_guard", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": ["OBSERVER_UNQUALIFIED"], "entered": false, "previous_sha256": null, "primary_code": "ENGINE_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "239ba4cb5637627857a8eee0bca70010aecafb4d337c4d2e7a24fde374d79bb1"}, "public_accept": false}
{"probe": "R3_frozen_role_qualification", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": ["OBSERVER_UNQUALIFIED"], "entered": false, "previous_sha256": null, "primary_code": "ENGINE_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "239ba4cb5637627857a8eee0bca70010aecafb4d337c4d2e7a24fde374d79bb1"}, "public_accept": false}
{"probe": "R3_frozen_role_q1", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": ["OBSERVER_UNQUALIFIED"], "entered": false, "previous_sha256": null, "primary_code": "ENGINE_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "239ba4cb5637627857a8eee0bca70010aecafb4d337c4d2e7a24fde374d79bb1"}, "public_accept": false}
{"probe": "R3_frozen_role_provenance", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "ENGINE_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "00a91dfd0bc3dd8afda69ef79862b2f31d367b12e4a414340f445dd1c14a0139"}, "public_accept": false}
{"probe": "R4_null_buffer", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": ["OBSERVER_UNQUALIFIED"], "entered": false, "previous_sha256": null, "primary_code": "INPUT_IO", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "e36b00e2bdd75dd24dfda3d917a69527cd7205f2cb5e0c9d55babfc015755bbc"}, "public_accept": false}
{"probe": "R4_negative_fd", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": ["OBSERVER_UNQUALIFIED"], "entered": false, "previous_sha256": null, "primary_code": "INPUT_IO", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "e36b00e2bdd75dd24dfda3d917a69527cd7205f2cb5e0c9d55babfc015755bbc"}, "public_accept": false}
{"probe": "R4_null_return", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": ["OBSERVER_UNQUALIFIED"], "entered": false, "previous_sha256": null, "primary_code": "INPUT_IO", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "e36b00e2bdd75dd24dfda3d917a69527cd7205f2cb5e0c9d55babfc015755bbc"}, "public_accept": false}
{"probe": "R4_out_of_map_return", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "OBSERVER_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "82a51346c965717a9000dcc9a49a41ec125f07bb7e7a7cac1d0f7a24647cc2dc"}, "public_accept": false}
{"probe": "R4_unmeasured_fd", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "OBSERVER_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "82a51346c965717a9000dcc9a49a41ec125f07bb7e7a7cac1d0f7a24647cc2dc"}, "public_accept": false}
{"probe": "R4_wrong_pread_count", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": ["OBSERVER_UNQUALIFIED"], "entered": false, "previous_sha256": null, "primary_code": "INPUT_IO", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "e36b00e2bdd75dd24dfda3d917a69527cd7205f2cb5e0c9d55babfc015755bbc"}, "public_accept": false}
{"probe": "R4_digest_without_raw_text", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "OBSERVER_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "82a51346c965717a9000dcc9a49a41ec125f07bb7e7a7cac1d0f7a24647cc2dc"}, "public_accept": false}
{"probe": "R4_missing_observation_text", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "diagnostics": ["ENGINE_UNQUALIFIED"], "public_accept": false}
{"probe": "R4_missing_actual_CALL_bytes", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "diagnostics": [], "public_accept": false}
{"probe": "R4_changed_actual_CALL_bytes", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "diagnostics": [], "public_accept": false}
{"probe": "R7_other_preparation_mutation", "state": "REFUSED", "primary": "RECORD_INVALID", "diagnostics": [], "public_accept": false}
{"probe": "R9_original_execution_fault_incomplete", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "diagnostics": ["EXECUTION_PROHIBITED"], "public_accept": false}
{"probe": "NEW_R9_substitution_fault_before_MI_failure", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "diagnostics": ["OBJECT_SUBSTITUTION"], "public_accept": false}
{"probe": "R6_stale_first", "error": "Invalid", "message": "lost custody"}
{"probe": "R6_new_second", "error": "Invalid", "message": "lost custody"}
{"probe": "R3_changed_tool_repetition", "states": ["ACCEPTED", "REFUSED"], "result": false}
{"probe": "NEW_RR1_receiver_monitor_wrong_thread_scope", "state": "ACCEPTED", "primary": null, "diagnostics": [], "public_accept": true}
```

### text.log

```text
{"probe": "NEW_R4_MI_text_differs_from_supervisor_reference", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "diagnostics": [], "public_accept": false}
```

### supplement.log

```text
{"probe": "R4_stop_specific_map_substitution", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "diagnostics": ["ENGINE_UNQUALIFIED"], "public_accept": false}
{"probe": "R4_raw_text_changed_digest_unchanged", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "OBSERVER_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "82a51346c965717a9000dcc9a49a41ec125f07bb7e7a7cac1d0f7a24647cc2dc"}, "public_accept": false}
{"probe": "R4_syscall_fd_mismatch", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": ["OBSERVER_UNQUALIFIED"], "entered": false, "previous_sha256": null, "primary_code": "INPUT_IO", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "e36b00e2bdd75dd24dfda3d917a69527cd7205f2cb5e0c9d55babfc015755bbc"}, "public_accept": false}
{"probe": "R5_valid_256_slots_two_byte", "compile_binding": true}
{"probe": "R6_normal_competitor", "error": "Invalid", "message": "exclusive custody unavailable"}
{"probe": "R6_normal_original_custody", "result": "valid"}
{"probe": "R8_missing_capture.json", "public_accept": false, "terminal": "ACCEPTED", "journal_unchanged": true}
{"probe": "R8_missing_observer/native-stops.json", "public_accept": false, "terminal": "ACCEPTED", "journal_unchanged": true}
{"probe": "R8_missing_capture.json,observer/native-stops.json", "public_accept": false, "terminal": "ACCEPTED", "journal_unchanged": true}
{"probe": "R9_original_wrong_mode_wrong_seals", "state": "REFUSED", "primary": "WRONG_PROTECTED_OBJECT", "diagnostics": ["WRONG_ENTRYPOINT"], "idempotent": true}
```

### original-prefix.log

```text
{"probe": "baseline", "state": "ACCEPTED", "primary": null, "public_accept": true}
{"probe": "premature_receiver_in_setup", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "OBSERVER_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "82a51346c965717a9000dcc9a49a41ec125f07bb7e7a7cac1d0f7a24647cc2dc"}}
{"probe": "inferior_exists_before_policy_readback", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "OBSERVER_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "82a51346c965717a9000dcc9a49a41ec125f07bb7e7a7cac1d0f7a24647cc2dc"}}
{"probe": "unexpected_internal_diagnostic_in_setup", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "OBSERVER_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "82a51346c965717a9000dcc9a49a41ec125f07bb7e7a7cac1d0f7a24647cc2dc"}}
{"probe": "unrelated_async_token_999", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "public_accept": false}
{"probe": "duplicate_running_with_wrong_thread", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "public_accept": false}
{"probe": "contradictory_signal_in_stop", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "public_accept": false}
{"probe": "MI_frame_tuple_replaced_by_result_list", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "public_accept": false}
{"probe": "malformed_register_names_tuple_of_values", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "public_accept": false}
{"probe": "unfrozen_hash_tool_after_freeze", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "ENGINE_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "00a91dfd0bc3dd8afda69ef79862b2f31d367b12e4a414340f445dd1c14a0139"}}
{"probe": "execution_guard_change_after_attempted", "state": "REFUSED", "primary": "RECORD_INVALID", "public_accept": false}
{"probe": "dict_no_empty_slot_READY", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": ["OBSERVER_UNQUALIFIED"], "entered": false, "previous_sha256": null, "primary_code": "WRONG_COMPILE_CALLABLE", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "cb4e302632edec0fbce5060170aa6ec98c6099efa4205df4dddcf81701e23bf8"}}
{"probe": "dict_256_slots_with_one_byte_indices_at_native_pair", "state": "REFUSED", "primary": "OBSERVATION_MISSING", "public_accept": false}
{"probe": "completion_integer_ones_instead_of_booleans", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "public_accept": false}
{"probe": "known_execution_fault_lost_on_incomplete_completion", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "public_accept": false}
{"probe": "rehashed_package_missing_original_observation_and_native_stop_file", "public_accept": false}
{"probe": "wrong_protected_seals_and_wrong_mode", "primary": "WRONG_PROTECTED_OBJECT"}
{"probe": "derivation_original_buffer_null", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": ["OBSERVER_UNQUALIFIED"], "entered": false, "previous_sha256": null, "primary_code": "INPUT_IO", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "e36b00e2bdd75dd24dfda3d917a69527cd7205f2cb5e0c9d55babfc015755bbc"}}
{"probe": "derivation_negative_fd_and_null_return_pc", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": ["OBSERVER_UNQUALIFIED"], "entered": false, "previous_sha256": null, "primary_code": "INPUT_IO", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "e36b00e2bdd75dd24dfda3d917a69527cd7205f2cb5e0c9d55babfc015755bbc"}}
```

## Final verdict and unchanged gates

- RR1: PARTIAL; exact deletion/extra-site corrected, wrong-thread receiver false ACCEPT remains.
- RR2: CLOSED OFFLINE.
- RR3: CLOSED OFFLINE.
- RR4: CLOSED OFFLINE.
- Prior R3/R5/R6/R7/R8: remain CLOSED OFFLINE within prior scopes.
- New regression findings: one remaining RR1 scope omission; no distinct newly introduced regression reproduced.
- Blocking issues: retained receiver thread=999 accepted for receipt TID 401.
- Implementation-slice verdict: PARTIAL.
- Live-experiment readiness: NOT_READY.
- external_trust_root: UNRESOLVED; no genuine native receipt.
- dependency_runtime_lock: UNRESOLVED; not begun.
- H2A1: VERIFIED + frozen, unchanged scoped status.
- H2A2: sealed handoff VERIFIED; surrogate VERIFIED WITH RESIDUAL ASSUMPTION;
  narrow engine provenance and prospective observer/Q1 verdicts unchanged;
  real-receipt offline implementation PARTIAL; live admission/receipt unperformed.
- E0: HOLD, unexecuted and unauthorized.
- Publication scope: commit/push only this receipt on the isolated review branch; no merge.
- Next bounded action: separately authorize an offline correction of receiver scope
  conformance, followed by its separate independent review. Neither is performed here.

Finish here. No repair, merge, live experiment or next action performed.
