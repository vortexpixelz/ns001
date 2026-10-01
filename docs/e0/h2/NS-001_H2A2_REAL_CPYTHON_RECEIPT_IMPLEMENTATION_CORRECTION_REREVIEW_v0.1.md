# NS-001 H2A2 real CPython receipt implementation correction re-review v0.1

Date: 2026-10-01 (America/New_York).
HEAD before / independently reviewed checkpoint: `113f1b061beb96c60a055103cc6417e741d99a9f`.
Isolated review branch: `codex/h2a2-correction-rereview`.

**PARTIAL. Live-experiment readiness: NOT_READY.** The complete offline suite
independently passes **280 tests, zero skips**, and every original bounded R1-R9
counterexample now fails closed or has the required refusal/recovery disposition.
However, equivalent history/association omissions remain in R1 and R2, inconsistent
raw text channels still ACCEPT in R4, and recovery still loses a supported non-guard
fault in R9. Four new synthetic cases produce ACCEPTED and public_accept=True.
No implementation/test repair, live qualification or experiment is performed.

## Authority and method

One independent READ-ONLY OFFLINE review was authorized, followed by exactly this
receipt's commit/push on an isolated branch, with no merge or next action. The
controlling independent review and correction receipt are inputs, not trusted
verdicts. Frozen input-boundary, engine-provenance, observer, experiment and GDB Q1
contracts remain controlling. Earlier receipts retain their historical claim scope.

The provided isolated worktree initially had clean detached HEAD
`d9dcfbef1bea173b316bc968fd71421c982422c3`. The requested correction commit already
existed locally. This worktree was switched to a new review branch at that exact
commit; the canonical checkout/branch was not changed. Git worktree metadata required
sandbox escalation, which was approved. HEAD before here means the reviewed checkpoint.
The resulting receipt commit is reported outside its own bytes to avoid self-reference.

Method: inspect the correction diff and the five implementation modules, retained
review reproductions, correction tests/fixtures and controlling contracts; run the
whole real-receipt offline suite once; rerun the original script's first block
unchanged; faithfully reconstruct its lock/repetition tails with explicit negative
handling; independently probe only the materially touched invariants. Temporary
scripts/logs and synthetic stores live outside the repository. The reproduction
sources and exact outputs below are durable in this receipt. No generic fuzzing,
retuning, alternative observer or candidate execution was used.

Ordinary offline Python tooling imports validators/test fixtures. Protected source
remains literal bytes data; strings naming forbidden operations remain evidence
assertions. No candidate compile/eval/exec/import, GDB process (including version
query), debugger attachment, ptrace/native control, live CPython experiment,
scientific/client/E0 invocation, package mutation or dependency_runtime_lock action
occurred. Authorized Git publication is the only network operation in this circuit.

## Frozen authority and prior receipts

The following SHA-256 values were independently recomputed from retained bytes:

| Retained document in this directory | SHA-256 |
| --- | --- |
| NS-001_H2A2_REAL_CPYTHON_ENGINE_OBSERVER_QUALIFICATION_v0.1.md | `289d9b8dfb45fe518e4da33ef15bf3c9f26fa26c42ca6082b6276c8d3ce39865` |
| NS-001_H2A2_REAL_CPYTHON_ENGINE_PROVENANCE_REVIEW_v0.1.md | `3fd49cf843b582ddffed971281e226c2d1f419462c17150ca48e82a3b649453e` |
| NS-001_H2A2_REAL_CPYTHON_GDB_Q1_REVIEW_v0.1.md | `6ae726ee2bb2821e4f0a0667f4d4dcefcdd07d49dfdf6e1e0b32d35007eb9339` |
| NS-001_H2A2_REAL_CPYTHON_INPUT_BOUNDARY_SPEC_v0.1.md | `eae004d95046d2c2a83fd7813f4b0485ce792e358403a406859280f4c0fdc564` |
| NS-001_H2A2_REAL_CPYTHON_NATIVE_OBSERVER_DESIGN_v0.1.md | `cdca62d5f02a468353d4c0ba9113e3d4ced047f4b78f68c949b1141bbad1b075` |
| NS-001_H2A2_REAL_CPYTHON_RECEIPT_EXPERIMENT_DESIGN_v0.1.md | `b120fb71ca537d84926e0b81173d1f867f9e92cbde0c54696191c0a8cafee54d` |
| NS-001_H2A2_REAL_CPYTHON_RECEIPT_IMPLEMENTATION_COMPLETION_v0.1.md | `72362b1a3be2441f3c99fd10979a80d48efe48298cceb2655c065bfbf66b75b4` |
| NS-001_H2A2_REAL_CPYTHON_RECEIPT_IMPLEMENTATION_CORRECTION_v0.1.md | `7bdd4a4c3d482043fe02ebc8463994d7930218216af853e9b6746ac1c65eeb17` |
| NS-001_H2A2_REAL_CPYTHON_RECEIPT_IMPLEMENTATION_REVIEW_v0.1.md | `097f63ffc52313e36b8c3c5bd4e508364f220a9c44d81af506a7c954fb056cc9` |
| NS-001_H2A2_REAL_CPYTHON_RECEIPT_IMPLEMENTATION_v0.1.md | `1a8e7dce6aa3071c577623d78156e4d2c0067296d4f078f98ea7239e222f53b4` |

## R1-R9 individual dispositions

| Finding | Original reproduction at this checkpoint | Independent closure verdict |
| --- | --- | --- |
| R1 setup/lifetime | Early inferior, premature receiver and unexpected software diagnostic: REFUSED / OBSERVER_UNQUALIFIED. Fresh-token faithful versions also refuse; arbitrary unqualified log refuses. | PARTIAL: observation-phase monitor deletion and extra READY hardware site still publicly ACCEPT. |
| R2 MI/events | Unrelated async token, duplicate/rival running, contradictory signal, malformed register tuple and malformed frame: ABORTED / ATTEMPT_INCOMPLETE, public false. | PARTIAL: thread exit before receiver is retained but ignored and publicly ACCEPTs. |
| R3 frozen tools | hash_tool replacement + matching submitted pin: REFUSED / ENGINE_UNQUALIFIED. Attempt 2 replacement: first ACCEPTED, second REFUSED, compare_repetition=False. | CLOSED OFFLINE: all eleven required roles independently probed and refuse with ENGINE_UNQUALIFIED. |
| R4 derivation/raw text | Null buffer, negative FD plus null return PCs: REFUSED / INPUT_IO with OBSERVER_UNQUALIFIED diagnostic. Separate null/out-of-map PCs, FD mismatch, unmeasured FD, wrong count, absent raw text, changed raw bytes, map handle substitution and missing/changed CALL bytes all fail closed. | PARTIAL: contradictory measured MI text and supervisor/reference bytes still publicly ACCEPT; raw agreement remains missing. |
| R5 dict ABI | Exact retained 256-slot/one-byte-index mutation: REFUSED / OBSERVATION_MISSING, public false. READY all-dummy variant: REFUSED / WRONG_COMPILE_CALLABLE. | CLOSED OFFLINE: valid 256-slot/two-byte table independently decodes compile binding; width rule is size-derived. |
| R6 store custody | Original lock unlink/replacement: stale first check raises Invalid('lost custody'); new second Store raises the same. | CLOSED OFFLINE: no two valid writers; ordinary competing Store denied and original custody still valid. |
| R7 mutation/types | Original post-ATTEMPTED exec assertion: REFUSED / RECORD_INVALID, public false. Completion integer ones: ABORTED / ATTEMPT_INCOMPLETE. | CLOSED OFFLINE: detached snapshot/fingerprint and exact completion bool checks verified; independent custody-field mutation also refuses. |
| R8 package completeness | Remove capture.json and native-stops.json, rehash manifests/sidecar: public false. Independent removals of either file alone also public false. | CLOSED OFFLINE for inventory: retained ACCEPTED journal remains unchanged; complete raw inventory and replay are required. Replay still inherits the R1/R2/R4 semantic defects. |
| R9 recovery/refusal | Execution assertion plus incomplete completion: ABORTED / ATTEMPT_INCOMPLETE with EXECUTION_PROHIBITED diagnostic. Wrong mode + wrong seals: normal REFUSED / WRONG_PROTECTED_OBJECT with WRONG_ENTRYPOINT diagnostic; idempotent recovery. | PARTIAL: a supported protected-final substitution is still lost when MI parsing fails. |

The unchanged original script uses token 30 for additional setup commands, now
already occupied by the expanded baseline. Those exact cases refuse but do not
alone prove the intended invariant. Faithful reproductions use fresh token 5000,
retain the same extra receiver stop or diagnostic, and also refuse. This token-only
adaptation avoids silently weakening the old counterexample. Lock acquisition now
throws before the original tail can reach both check() calls; the faithful isolated
version explicitly reports each refusal. The original repetition tail now refuses
attempt 2 before attempted(); its faithful version retains that REFUSED and checks
compare_repetition=False. No mutation was removed to make an acceptance possible.

## Remaining blocking findings in the touched invariants

### RR1 — Receiver lifetime and complete hardware history still fail open (R1)

Source: `e0/h2/real_receipt_integration.py:1143-1173`, `:559-604`.
Authority: observer sections 3/6/8; experiment sections 4/7/11; Q1 sections 5-7.

validate_setup verifies receiver insertion, ordering and deletion only in the setup
Transcript. decode_observation does not reconcile later -break-delete commands with
that retained monitor. receiver_stays_armed reuses setup_facts.monitor_armed and the
admission string receiver_slot='armed'; it does not derive current lifetime state
from the observation commands. measured_witness additionally emits sentinel_active=True.

Independent reproduction inserts a successful `-break-delete 1` after the caller
snapshot and before the one CALL step. All later MI tokens and the associated native
receiver token shift by exactly one to preserve grammar/causal links. No stop, byte,
argument or completion mutation is involved. Result: ACCEPTED, diagnostics=[], public
ACCEPT true despite explicit receiver-monitor retirement before receipt.

A second bounded reproduction appends a successful enabled hardware insertion at
wrapper `0x4f6102` with breakpoint number 3 in READY. Receiver 1 and caller 2 were
already installed and remain enabled. The complete setup path/counters are otherwise
unchanged. It also produces ACCEPTED/public true. No complete inventory or sequential
retirement/slot-budget check rejects this extra active site. These are history
omissions beyond exact matching of the old premature-entry warning/stop fixtures.

Early readbacks, original setup hits and unknown diagnostic rejection are meaningful
improvements. Entry counts now derive from retained stops, rather than default 1;
that does not close lifetime instrumentation/control contradictions.

### RR2 — Thread exit is represented but cannot invalidate the pair (R2)

Source: `e0/h2/real_receipt_integration.py:122-134`, `:260-290`, `:542-559`.
Authority: observer sections 1/6/8; experiment sections 4/7/12; Q1 section 7.6.

The exit-notification branch accepts =thread-exited or =thread-group-exited once
there is any stop and no pending MI command. It neither invalidates custody nor
removes exited IDs. snapshot subsequently resolves the same stale groups/threads.
An exact `=thread-exited,id="401",group-id="i1"` between caller capture and receiver
step therefore produces ACCEPTED/public true, although a later receipt still claims
that exited thread. Raw preservation alone does not enforce the event invariant.

The grammar correction does distinguish tuple and list structures. Original invalid
register-names tuple refuses; valid baseline and matching-token tests pass. Rival
and identical duplicate running records refuse; unfamiliar async records are retained
in capture then ABORTED. The remaining exit inconsistency is concrete, not a claim
that every possible MI event is unsupported.

### RR3 — Separate binary text capture omits required raw-channel agreement (R4)

Source: `e0/h2/real_receipt_integration.py:467-477`, `:563-572`, `:1070-1105`.
Authority: experiment section 2 (actual executable text); Q1 section 7.2-3 (complete
unmasked stopped-child text must agree with qualified files and raw MI capture).

TextCapture requires complete binary range bytes, per-stop map associations, digest
and exact frozen reference equality. This supporting binary transport is compatible
with the frozen separation between canonical records and raw evidence. Keeping binary
ranges outside MI/JSON does not inherently change the architecture or weaken limits.

But the implemented comparison consumes MI text only at the two fixed sites (2-byte
CALL and 4-byte receiver). It never checks other measured MI executable bytes against
the supervisor range. admission.text.mi_sha256 is merely compared to the expected
reference digest; it is not derived from retained full-range MI measurements.

Independent bounded reproduction adds one actual addressed MI read at `0x500000`
returning `cc` in both native snapshots. That VA is within the required compiler
text range. The corresponding supervisor and frozen reference byte is `00`; all site
bytes and maps remain correct. Result: ACCEPTED/public true with no faults. This is
contradictory retained raw measurement, not an absence-of-authentication argument.

Transcript's 8 MiB total, MIParser's 8 MiB total/65,536-byte line and memory-read
bounds, parse's 8 MiB canonical bound and 4 MiB binary-range bound are unchanged.
The separately retained complete supervisor range closes the prior missing-binary
transport problem. It does not justify reducing Q1 raw agreement to site constants.
That omission contradicts the frozen design; the correction receipt's claim of
unchanged conformance cannot be accepted. No alternative limits/interface repair is
proposed or implemented here. Independently frozen native read primitive/reference
provenance remains a declared future admission obligation, not this concrete defect.

Native derivation is substantially improved: raw setup registers/stack/buffer reads
reproduce pread result, object resize and return/root associations; zero/negative
and self-consistent unmeasured descriptor cases refuse. CALL and entry bytes are
required actual MI measurements. These strengths do not eliminate RR3.

### RR4 — Supported non-guard fault still disappears on decode exception (R9)

Source: `e0/h2/real_receipt_integration.py:539-564`, `:913-939`,
`e0/h2/real_receipt_evidence.py:657-678`.
Authority: input-boundary section 10; experiment section 12.

finish_observation persists guard faults before decoding. decode_observation records
OBJECT_SUBSTITUTION from protected_final only after constructing Transcript. A parse
exception therefore prevents the independently supplied final-seals mismatch from
being gathered, and recovery sees no supported-fault record for it.

Independent reproduction changes protected_final.seals from 15 to 0 and appends one
malformed MI line. Original capture.json retains both facts. Recovery is ABORTED /
ATTEMPT_INCOMPLETE, diagnostics=[], public false. The fail-closed terminal is correct,
but the supported substitution diagnostic is erased. This repeats the original
R9 class of generic Invalid -> incomplete recovery erasing an available fault.
Guard execution faults are now preserved and the original ranked normal refusal is
correct; the correction is incomplete for non-guard supported evidence.

## New regression-surface assessment

The above five fixed probes (two RR1, one RR2, one RR3, one RR4) are the new findings:
four false public ACCEPTs and one diagnostic-loss case. They concern only the touched
history/parser/raw-admission/recovery invariants. No generic fuzzing was performed.

R3 now binds all eleven roles to independent frozen material through E's qualification
hash; repetition requires verified packages and includes the role commitment. R5's
width rule matches the pinned header: size <=0xff uses one byte, <=0xffff two, then
four/eight; given power-of-two slots its cutoffs are 128/32768. Valid supported dicts
remain decoded. R6 compares fstat(open lock), current lstat(path) and retained device/
inode, checks one link and makes an observed custody failure permanent. This is a
local retained-store claim under frozen assumptions, not distributed locking.

R7 retains a deep detached preparation and canonical forensic snapshot; finish checks
both submitted and internal evidence against that snapshot. Completion booleans use
exact types. R8's mandatory inventory covers original capture/native stops, setup and
pair transcripts/order, admission/maps/derivation/arguments/completion, four source
captures, binary text, qualification, durable journal/request/registration/witness
and custody/reservation snapshots. Manifests are acyclic and hash-correct omissions
cannot be accepted. No missing-payload -> expected fixture fallback or deliberate
exception-to-ACCEPT path was found. The surviving success assumption in receiver
coverage and omitted raw reconciliation above are sufficient blockers.

## Independently executed suite

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_e0_h2_real_receipt*.py' -v
----------------------------------------------------------------------
Ran 280 tests in 86.895s

OK
```

Exit 0; **280 PASS, 0 skips**, comprising 161 original, 67 completion and 52 correction
tests. Verbose output contains 280 test results and no skipped entries. Complete log
SHA-256: `c951b7b09d0ae8838535be24c584ad6abbd1020d118441518241347cbf2a3d7c`.
The suite runs actual validators/durable temporary stores. It does not authenticate
synthetic captures as native events. Passing tests cannot override the false ACCEPTs.
Each independent reproduction run also finished with exit 0; outputs are retained below.

## Preservation and publication scope

All **233 tracked checkpoint files** were inventoried by SHA-256 and independently
rechecked unchanged before receipt creation. Only this receipt is added. The initial
and post-analysis tracked diffs were empty; implementation/test files were never
edited. Baseline inventory JSON digest:
`d0b30e17e9d5abe1bf34665873793d236dc24f3c00b6336dabcabb0006ca73de`.
Comparison from pre-implementation `345c6497f4d715a5131e0ca386fd8eea9b221c6e`
to this checkpoint lists only the additive real-receipt implementation/test files
and four implementation/review receipts. Frozen authority, H2A1 and earlier H2A2
slices have no changes in that comparison or this review.

Static file hashing reproduces the unchanged pinned tools (none launched):

| File | SHA-256 |
| --- | --- |
| /usr/bin/python3.12 | `e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f` |
| /usr/bin/gdb | `3832cc070ae1716e322105d3b39fb398695e5f031c9d39224cf227a8c2b889f6` |
| /lib64/ld-linux-x86-64.so.2 | `c20a2dc8917c755f02b94049356320fe1f62ac7d9f8994731f807d9df39302da` |

Publication is restricted to this receipt on the isolated review branch. Precommit
inventory/diff/index checks must contain exactly this path. No merge into canonical,
repair, rerun of a native experiment or follow-on action is authorized. Resulting
commit/push verification is reported separately. This preservation statement covers
this circuit's actions and retained files, not surveillance of unrelated host activity.

## Retained independent reproductions

The original source is extracted unchanged from the controlling independent review's
Python block. Its reproduced SHA-256 matches the retained original script pin:
`2547282264b0924cd13a7040dc9b4843301f909c2ef815e36f966f4618f3c88e`.
Run its unchanged prefix through the invalid-derivation cases (before the lock block)
as a script outside this repository, with cwd at this checkout and bytecode disabled.
The unchanged original lock/repetition tails assume their old false successes;
the faithful adaptations below record their new rejection instead of terminating
the rest of the review. No candidate source is interpreted by these scripts.

### original-prefix.py

Source SHA-256: `cfa7ae2f90fb6f58080d367f11ec606f28ca7da2269fbc4e28320013341dcdba`.
Output SHA-256: `85e8292d47c22bb809a64d59d060e420a36431fff8789172d01bc373d41a71f9`.

Source is the exact retained review block prefix described above; its original full source remains in the unchanged controlling receipt.

Exact output:

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

### probes.py

Source SHA-256: `32a98d9afcfbf09ba99b3d90fecbe88f9a698ced7b46e2563482a7d21c4eac19`.
Output SHA-256: `2367c5761e9d47b96be31c993564823656fad921a8cda26edf78165fa3e004f4`.

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


from e0.h2.real_receipt_policy import Invalid, parse
from e0.h2.real_receipt_integration import frozen_role_codes, compare_repetition

def extra_command(p, cmd):
    return replace(p, transcript=p.transcript + (Chunk('commands', mi_command(5000, cmd)), Chunk('stdout', b'5000^done\n')))

def setup_entry(e,p):
    extra=(Chunk('commands',mi_command(5000,'-exec-continue')),Chunk('stdout',b'5000^running\n*running,thread-id="all"\n*stopped,reason="breakpoint-hit",thread-id="401",stopped-threads="all",frame={addr="0x69bff0"}\n'))
    return e,replace(p,transcript=p.transcript+extra)
run('R1_faithful_premature_receiver_fresh_token',change_p=setup_entry)

def diag(e,p):
    extra=(Chunk('commands',mi_command(5000,'-interpreter-exec console "maintenance info breakpoints"')),Chunk('stdout',b'~"UNEXPECTED software breakpoint inserted at 0x581feb\\n"\n5000^done\n'))
    return e,replace(p,transcript=p.transcript+extra)
run('R1_faithful_software_diagnostic_fresh_token',change_p=diag)
run('R1_other_unqualified_history',change_p=lambda e,p:(e,replace(p,transcript=p.transcript+(Chunk('commands',mi_command(5000,'-interpreter-exec console "maintenance info breakpoints"')),Chunk('stdout',b'&"unclassified backend event\\n"\n5000^done\n')))))

# Allowed deletion in the observation history, after caller capture but before step.
def delete_monitor(o):
    chunks=[]
    for c in o.transcript:
        if c.channel=='commands' and b'-exec-step-instruction' in c.raw:
            # Use the original step token for delete, shift subsequent tokens by one
            # (including native stop link) to retain monotonic MI association.
            t=int(c.raw.split(b'-',1)[0])
            chunks.extend((Chunk('commands',mi_command(t,'-break-delete 1')),Chunk('stdout',f'{t}^done\n'.encode())))
            break
        chunks.append(c)
    import re
    tail=o.transcript[len(chunks)-2:]
    # Index of step in original, independent of appended deletion chunks.
    start=next(i for i,c in enumerate(o.transcript) if c.channel=='commands' and b'-exec-step-instruction' in c.raw)
    for c in o.transcript[start:]:
        raw=re.sub(rb'^([0-9]+)([-^])',lambda m:str(int(m[1])+1).encode()+m[2],c.raw)
        chunks.append(replace(c,raw=raw))
    natives=(o.native_stops[0],{**o.native_stops[1],'token':o.native_stops[1]['token']+1})
    return replace(o,transcript=tuple(chunks),native_stops=natives)
run('NEW_R1_monitor_deleted_between_caller_receiver',change_o=delete_monitor)

# A hardware site not in the retained setup path, with no slot/lifetime accounting.
def unexpected_hardware(e,p):
    return e,replace(p,transcript=p.transcript+(Chunk('commands',mi_command(5000,'-break-insert -h *0x4f6102')),Chunk('stdout',b'5000^done,bkpt={number="3",type="hw breakpoint",enabled="y",addr="0x4f6102"}\n')))
run('NEW_R1_extra_hardware_site_through_READY',change_p=unexpected_hardware)

# A known thread exits between snapshots; later evidence still claims its identity.
def exited(o):
    idx=next(i for i,c in enumerate(o.transcript) if c.channel=='commands' and b'-exec-step-instruction' in c.raw)
    return replace(o,transcript=o.transcript[:idx]+(Chunk('stdout',b'=thread-exited,id="401",group-id="i1"\n'),)+o.transcript[idx:])
run('NEW_R2_thread_exit_before_receiver',change_o=exited)
run('R2_unexpected_async_record',change_o=lambda o:replace(o,transcript=o.transcript+(Chunk('stdout',b'=unclassified,id="401"\n'),)))
run('R2_duplicate_running_same_thread',change_o=lambda o:replace(o,transcript=tuple(replace(c,raw=c.raw.replace(b'*running,thread-id="all"\n',b'*running,thread-id="all"\n*running,thread-id="all"\n')) for c in o.transcript)))

for role in ('controller','launcher_gdb','launcher_cpython','bootstrap','mi_parser','decoder','hash_tool','guard','qualification','q1','provenance'):
    def swap(p,role=role):
        arts={**p.artifacts,role:b'unfrozen-replacement-'+role.encode()}
        return replace(p,artifacts=arts,pins={**p.pins,role:digest(arts[role])})
    run('R3_frozen_role_'+role,after_freeze=swap)

for label,kwargs in [('null_buffer',dict(original_buffer=0)),('negative_fd',dict(fd=-1,syscall_fd=-1)),('null_return',dict(return_pc_in=0,return_pc_out=0)),('out_of_map_return',dict(return_pc_in=0x88800,return_pc_out=0x88800)),('unmeasured_fd',dict(fd=8,syscall_fd=8)),('wrong_pread_count',dict(count=2))]:
    run('R4_'+label,change_p=lambda e,p,kw=kwargs:(e,replace(p,derivation=replace(p.derivation,**kw))))
run('R4_digest_without_raw_text',change_p=lambda e,p:(e,replace(p,text_captures=())))
run('R4_missing_observation_text',change_o=lambda o:replace(o,text_captures=()))
run('R4_missing_actual_CALL_bytes',mutate_memory=lambda m:m.ranges.pop(0x581feb))
run('R4_changed_actual_CALL_bytes',mutate_memory=lambda m:m.ranges.__setitem__(0x581feb,bytearray.fromhex('ffd1')))
run('R7_other_preparation_mutation',after_attempted=lambda p,a:p.custody.__setitem__('controller','changed-controller'))
run('R9_original_execution_fault_incomplete',change_o=lambda o:replace(o,guard_operations=('execution',),completion={**o.completion,'pidfd_death_confirmed':False}))
run('NEW_R9_substitution_fault_before_MI_failure',change_o=lambda o:replace(o,protected_final={**o.protected_final,'seals':0},transcript=o.transcript+(Chunk('stdout',b'bad-mi\n'),)))

with tempfile.TemporaryDirectory(prefix='ns001-review-lock-') as td:
    root=Path(td)/'store'
    first=Store(root,NS,create=True)
    (root/'lock').unlink()
    (root/'lock').write_bytes(b'')
    for label,fn in [('stale_first',first.check),('new_second',lambda:Store(root))]:
        try:
            value=fn()
            print(json.dumps(dict(probe='R6_'+label,result='unexpected success')))
            if value is not None:value.close()
        except Invalid as exc:
            print(json.dumps(dict(probe='R6_'+label,error='Invalid',message=str(exc))))
    first.close()

with tempfile.TemporaryDirectory(prefix='ns001-review-repetition-') as td:
    store=Store(Path(td)/'store',NS,create=True)
    try:
        attempts=[]
        for ordinal in (1,2):
            x=NS+':'+str(ordinal)
            e,p=preparation(x)
            freeze(store,e,p)
            if ordinal==2:
                arts={**p.artifacts,'hash_tool':b'unfrozen-replacement-hash-tool'}
                p=replace(p,artifacts=arts,pins={**p.pins,'hash_tool':digest(arts['hash_tool'])})
            a=store.reserve(e,request(e))
            a.prepare(p)
            if a.events()[-1]['state']!='REFUSED':
                tried=a.attempted()
                a.finish(None,observation(p,x,e,tried))
            attempts.append(a)
        print(json.dumps(dict(probe='R3_changed_tool_repetition',states=[a.recover()['state'] for a in attempts],result=compare_repetition(*attempts))))
    finally:store.close()
```

Exact output:

```text
{"probe": "R1_faithful_premature_receiver_fresh_token", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "OBSERVER_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "82a51346c965717a9000dcc9a49a41ec125f07bb7e7a7cac1d0f7a24647cc2dc"}, "public_accept": false}
{"probe": "R1_faithful_software_diagnostic_fresh_token", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "OBSERVER_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "82a51346c965717a9000dcc9a49a41ec125f07bb7e7a7cac1d0f7a24647cc2dc"}, "public_accept": false}
{"probe": "R1_other_unqualified_history", "result": {"attempt_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:1", "diagnostics": [], "entered": false, "previous_sha256": null, "primary_code": "OBSERVER_UNQUALIFIED", "schema": "ns001.h2a2.real-input.event.v1", "sequence": 0, "state": "REFUSED", "witness_sha256": "82a51346c965717a9000dcc9a49a41ec125f07bb7e7a7cac1d0f7a24647cc2dc"}, "public_accept": false}
{"probe": "NEW_R1_monitor_deleted_between_caller_receiver", "state": "ACCEPTED", "primary": null, "diagnostics": [], "public_accept": true}
{"probe": "NEW_R1_extra_hardware_site_through_READY", "state": "ACCEPTED", "primary": null, "diagnostics": [], "public_accept": true}
{"probe": "NEW_R2_thread_exit_before_receiver", "state": "ACCEPTED", "primary": null, "diagnostics": [], "public_accept": true}
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
{"probe": "R4_missing_observation_text", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "diagnostics": [], "public_accept": false}
{"probe": "R4_missing_actual_CALL_bytes", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "diagnostics": [], "public_accept": false}
{"probe": "R4_changed_actual_CALL_bytes", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "diagnostics": [], "public_accept": false}
{"probe": "R7_other_preparation_mutation", "state": "REFUSED", "primary": "RECORD_INVALID", "diagnostics": [], "public_accept": false}
{"probe": "R9_original_execution_fault_incomplete", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "diagnostics": ["EXECUTION_PROHIBITED"], "public_accept": false}
{"probe": "NEW_R9_substitution_fault_before_MI_failure", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "diagnostics": [], "public_accept": false}
{"probe": "R6_stale_first", "error": "Invalid", "message": "lost custody"}
{"probe": "R6_new_second", "error": "Invalid", "message": "lost custody"}
{"probe": "R3_changed_tool_repetition", "states": ["ACCEPTED", "REFUSED"], "result": false}
```

### text-probe.py

Source SHA-256: `011609aa097ddbaa7a1aa616ff60299cdce29414495a8670adbe0478023814e0`.
Output SHA-256: `88272ef17c9ab3ec29a0feb5df30d9744dba43bec8a8e2bfa0932642041cded7`.

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



def incompatible_text(mem):
    mem.ranges[0x500000]=bytearray(b'\xcc')
run('NEW_R4_MI_text_differs_from_supervisor_reference',mutate_memory=incompatible_text)
```

Exact output:

```text
{"probe": "NEW_R4_MI_text_differs_from_supervisor_reference", "state": "ACCEPTED", "primary": null, "diagnostics": [], "public_accept": true}
```

### supplement.py

Source SHA-256: `73bcc844adecefc10a5bec0c362d6188305e97c7f9d5b353986ef04377bc2574`.
Output SHA-256: `1f017f81da25b37198aa0e1a099625dafcf7062b888695d4cb32917d27209c18`.

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



from e0.h2.real_receipt_policy import Invalid, parse
from e0.h2.real_receipt_evidence import manifest
from e0.h2.real_receipt_integration import text_maps
run('R4_stop_specific_map_substitution',change_o=lambda o:replace(o,text_captures=tuple(replace(c,mapping={**c.mapping,'handle':'other-file'}) for c in o.text_captures)))

def text_changed(e,p):
    cs=list(p.text_captures)
    cs[2]=replace(cs[2],raw=b'x'+cs[2].raw[1:])
    return e,replace(p,text_captures=tuple(cs))
run('R4_raw_text_changed_digest_unchanged',change_p=text_changed)
run('R4_syscall_fd_mismatch',change_p=lambda e,p:(e,replace(p,derivation=replace(p.derivation,syscall_fd=8))))

# Positive wider supported dictionary: exactly pinned 256-slot/two-byte layout.
from test_e0_h2_real_receipt import native_memory,C
mem=native_memory()
old=mem.ranges[DK]
header=bytearray(old[:32]); header[8:10]=bytes([8,9]); header[16:24]=(168).to_bytes(8,'little')
mem.ranges[DK]=header+bytes([0,0,1,0])+bytes([255]*508)+old[40:72]
print(json.dumps(dict(probe='R5_valid_256_slots_two_byte',compile_binding=Decoder(Snapshot(mem.reads())).dictionary(DICT)[0]['compile']==C)))

with tempfile.TemporaryDirectory(prefix='ns001-rereview-normal-lock-') as td:
    store=Store(Path(td)/'store',NS,create=True)
    try:
        store.check()
        try:
            second=Store(store.root);second.close()
            print(json.dumps(dict(probe='R6_normal_competitor',result='unexpected success')))
        except Invalid as exc:
            print(json.dumps(dict(probe='R6_normal_competitor',error='Invalid',message=str(exc))))
        store.check()
        print(json.dumps(dict(probe='R6_normal_original_custody',result='valid')))
    finally:store.close()

for missing in [('capture.json',),('observer/native-stops.json',),('capture.json','observer/native-stops.json')]:
    with tempfile.TemporaryDirectory(prefix='ns001-rereview-inventory-') as td:
        store=Store(Path(td)/'store',NS,create=True)
        try:
            e,p=preparation(X);freeze(store,e,p);a=store.reserve(e,request(e));a.prepare(p)
            tried=a.attempted();a.finish(None,observation(p,X,e,tried))
            journal=a.raw('events.jsonl')
            for name in missing:(a.path/name).unlink()
            files=_all_files(a)
            capfiles={n:raw for n,raw in files.items() if n.startswith('qualification/') or n.startswith('1/observer/')}
            (a.path/'capture-manifest.json').write_bytes(canonical(manifest('capture',X,digest(canonical(e)),capfiles)))
            raw=canonical(manifest('package',X,digest(canonical(e)),_all_files(a)))
            (a.path/'package-manifest.json').write_bytes(raw)
            (a.path/'package-manifest.sha256').write_bytes((digest(raw)+'\n').encode())
            print(json.dumps(dict(probe='R8_missing_'+','.join(missing),public_accept=public_accept(a,raw,a.raw('package-manifest.sha256'),_all_files(a),set()),terminal=a.recover()['state'],journal_unchanged=journal==a.raw('events.jsonl'))))
        finally:store.close()

with tempfile.TemporaryDirectory(prefix='ns001-rereview-refusal-') as td:
    store=Store(Path(td)/'store',NS,create=True)
    try:
        e,p=preparation(X);freeze(store,e,p)
        r=parse(request(e));r['parameters']['mode']='eval'
        a=store.reserve(e,canonical(r));a.prepare(replace(p,protected={**p.protected,'seals':0}))
        terminal=a.recover()
        print(json.dumps(dict(probe='R9_original_wrong_mode_wrong_seals',state=terminal['state'],primary=terminal['primary_code'],diagnostics=terminal['diagnostics'],idempotent=a.recover()==terminal)))
    finally:store.close()
```

Exact output:

```text
{"probe": "R4_stop_specific_map_substitution", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "diagnostics": [], "public_accept": false}
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

## Final verdict and unchanged gates

- R1: PARTIAL (original cases rejected; RR1 remains).
- R2: PARTIAL (original cases rejected; RR2 remains).
- R3: CLOSED OFFLINE.
- R4: PARTIAL (original malformed derivation/raw-absence cases rejected; RR3 remains).
- R5: CLOSED OFFLINE.
- R6: CLOSED OFFLINE.
- R7: CLOSED OFFLINE.
- R8: CLOSED OFFLINE for mandatory inventory; replay inherits semantic blockers.
- R9: PARTIAL (both original cases corrected; RR4 remains).
- Implementation-slice verdict: **PARTIAL**.
- Live-experiment readiness: **NOT_READY**.
- external_trust_root: **UNRESOLVED**; no genuine native receipt.
- dependency_runtime_lock: **UNRESOLVED; not begun**.
- H2A1: **VERIFIED + frozen**, unchanged scoped receipt status; no new authority claim.
- H2A2: sealed handoff VERIFIED; surrogate VERIFIED WITH RESIDUAL ASSUMPTION;
  narrow engine provenance and prospective observer/Q1 verdicts unchanged;
  real-receipt offline implementation PARTIAL; live admission/receipt unperformed.
- E0: **HOLD**, unexecuted and unauthorized.
- One next bounded action: separately authorize an offline correction limited to
  RR1-RR4 with faithful regressions and a subsequent independent checkpoint review.
  Not authorized or performed in this circuit; no live experiment, merge or next action.

Finish here.
