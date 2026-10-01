# NS-001 H2A2 real CPython receipt implementation correction v0.1

Date: 2026-10-01 (America/New_York).
HEAD before: `4c788d22a7c007f1cb7f6f96ac801c4e0efb32ad`.
Canonical branch: `codex/e0-h2-preparation`.

**Implementation verdict: PASS — bounded OFFLINE correction of R1-R9.**
The 228 retained real-receipt tests and 52 new correction tests pass: **280 PASS**.
All independent-review false ACCEPT counterexamples are represented by permanent
bounded regressions and now fail closed. The correctly rejected malformed-frame
case still fails closed; the complete positive synthetic path and unchanged
positive repetition tests still pass. This result is an offline correction receipt,
not an independent re-review, native admission, or permission for a live experiment.

## Authority and changed files

One correction circuit was authorized, strictly for findings R1-R9 in the unchanged
independent review. The canonical checkout initially had a clean working tree at
HEAD above. Changes are limited to:

- `e0/h2/real_receipt_abi.py`
- `e0/h2/real_receipt_evidence.py`
- `e0/h2/real_receipt_integration.py`
- `e0/h2/real_receipt_observation.py`
- `tests/real_receipt_fixtures.py`
- `tests/test_e0_h2_real_receipt.py`
- `tests/test_e0_h2_real_receipt_correction.py`
- this correction receipt.

The original test module changes only its synthetic memory constructor (measured
CALL/entry bytes) and synthetic wrapper return PC (within the executable mapping).
No existing test was removed or its assertion weakened. The completion test module
and frozen policy module remain unchanged. No controller, debugger-launch API,
scientific client, dependency-lock implementation or system/package change is added.

## Finding results

### R1 — CLOSED OFFLINE

Setup consumes the entire ordered MI history. Notifications/events before completion
of all frozen Q1 readbacks refuse. Every setup stop must match the independently
frozen seven-stop wrapper/syscall/resize/RET/READY path, including raw independent
native stop associations. A receiver hardware monitor must be installed before the
first setup continuation, cannot be deleted, and remains armed through READY;
the caller hardware site must be installed in READY admission. Unexpected stops,
receiver hits, missing setup captures and unqualified console/log diagnostics fail
closed without matching a particular warning string.

Entry and sentinel counts come from raw MI and independent native stop records,
including setup history. Q1 predicates come from parsed readbacks, monitor history,
raw control capture checks, text comparison, setup syscall counts, native pairing
and custody associations. Independent native control records require exec wait
status, successful hardware programming results, effective native slot traps and
closed-gate restop; numeric fields cannot use boolean coercion. These offline
records do not authenticate a collector or prove that a control was actually run.

### R2 — CLOSED OFFLINE

MI tuples require result entries and retain their dict representation; list grammar
remains separate, including ordered repeated-name result lists. Async tokens, when
present, must match the outstanding execution command. One coherent running/stop
transition is required; duplicated or unrelated running events refuse. Result-before-
stop and stop-before-result remain supported by the existing suite. Contradictory
signal/exit fields cannot qualify a native stop. Unexpected records remain in raw
supporting capture and cannot be silently accepted.

### R3 — CLOSED OFFLINE

E's frozen qualification digest commits to the role-to-hash dossier. It binds every
required role except the qualification artifact itself, which is bound directly by
E to avoid a self-referential hash. Preparation compares the submitted artifacts
with the actual frozen hash-addressed files. All eleven roles are checked, including
controller, both launchers, bootstrap, MI parser, decoder, hash tool, guard, Q1,
provenance and qualification. Repetition requires independently replay-verified
packages and retains the tool-role commitment in semantic comparison. Self-consistent
hash-tool replacement after freeze refuses; the changed second attempt cannot form
an accepted repetition.

### R4 — CLOSED OFFLINE

Derivation rejects null/invalid pointers, negative/incorrect FD values, null/out-of-
mapping return PCs and incomplete/contradictory pread/resize/return associations.
The descriptor is independently reproduced from setup registers and addressed reads:
wrapper arguments/return stack, syscall entry and exit, original buffer from the
native stack slot, returned bytes, post-resize pointer/bytes, RET RAX/return stack
and READY roots must agree. A self-consistent assertion cannot replace these reads.

The frozen Q1 review section 7.2-3 expressly requires independent supervisor
unmasked reads outside GDB's shadow layer. Supporting binary TextCapture artifacts
implement that existing offline input interface; no read primitive is launched.
They retain complete qualified ranges at launcher, post-exec, READY, caller and
receiver epochs, with file-handle/map/device/inode/offset/bias/sole-child associations.
Reference bytes are retained under the frozen qualification dossier's hashes.
Raw range length/hash/byte equality and map continuity are checked. The exact
3,026,877-byte compiler range and site bytes must be present. Addressed raw MI CALL
and receiver-site reads must independently agree with the fixed bytes and full
unmasked range; supplied digest labels alone are insufficient.

Binary supervisor ranges stay outside the MI transcript and supporting JSON rather
than hex-expanding two full text ranges into one transcript. The MI 8 MiB total,
65,536-byte record/read bounds and canonical-record 8 MiB bound remain unchanged;
individual binary ranges retain the existing 4 MiB admission bound. No exception,
parser-limit enlargement, duplicate full MI text requirement, or frozen substantive
semantics change was introduced. Separate manifests bind actual binary artifacts;
missing raw data is never reconstructed. Test references are explicitly synthetic,
not measurements of a real CPython process or a substitute live qualification.

### R5 — CLOSED OFFLINE

Dictionary index width follows the pinned CPython dk_size rule. A 256-slot table
requires two-byte indices; incompatible one-byte indices refuse. Existing size/
capacity/range/duplicate/stability bounds remain. The decoder additionally requires
an EMPTY slot for bounded lookup termination, rejecting the review's all-dummy
replacement. A valid 256-slot two-byte table is directly tested.

### R6 — CLOSED OFFLINE

Store creation retains lock device/inode identity before use. Opening and every
custody check compare the current lock path with its open capability and the
retained identity, require one link, and keep an observed custody failure terminal
for that writer. Replacing the pathname invalidates the stale writer and prevents
a second valid Store from binding the replacement. Ordinary competing flock
ownership also refuses. This is a local retained-store guarantee under the existing
exclusive-controller assumptions, not a distributed or hostile-filesystem claim.
Legacy stores missing identity evidence refuse; no automatic migration occurs.

### R7 — CLOSED OFFLINE

Attempt retains a detached deep snapshot plus exact canonical forensic bytes.
ATTEMPTED checks caller evidence against that snapshot; finish checks both caller
and internal snapshot consistency. Later prohibited-operation assertions are
retained separately and reconciled with observation guard records, rather than
lost behind an empty tuple. Completion requires exact bool values; integer 1 does
not become True. Malformed/incomplete completion becomes ABORTED with supported
faults retained, before clean completion witness fields can be emitted.

### R8 — CLOSED OFFLINE

Public ACCEPT requires capture.json, observer/native-stops.json, all frozen observer
artifacts, binary text captures, qualification material, custody snapshots, request,
registration, journal and witness. Hash-correct manifests alone are insufficient.
Verification reparses retained original preparation/observation, checks frozen tool
identities, rederives the native pair and witness, and reconciles original raw MI,
setup bytes/order, derivation/stops, maps, completion, arguments and binary artifacts.
Reduced/rehashed packages and contradictory original evidence fail public ACCEPT.
The immutable existing terminal remains preserved when packaging becomes incomplete.
No verifier creates or repairs a missing file.

### R9 — CLOSED OFFLINE

Request and independent admission stages gather supported faults before applying
unchanged refusal precedence. Witness-derived faults are included before terminal
persistence. Wrong mode plus wrong seals now persists normal REFUSED with
WRONG_PROTECTED_OBJECT primary and WRONG_ENTRYPOINT diagnostic. Guard faults are
retained before decoding can interrupt; other measured faults survive incomplete
completion. Recovery retains them as deterministic diagnostics while
ATTEMPT_INCOMPLETE remains recovery-only. Terminal records, enum, ranking and
canonical schemas remain unchanged.

## Regression inventory

The 52 new test methods include one complete positive/public-replay control and
51 finding-specific checks: R1=11, R2=6, R3=3, R4=11, R5=3, R6=2, R7=4, R8=5,
R9=6. The exact independent-review constructions are adapted to the corrected
synthetic evidence interface; command tokens follow the longer measured setup.
Their underlying mutations are preserved, including all prior false ACCEPTs,
changed-tool repetition, correctly rejected malformed frame, all-dummy dict,
rehashed reduced package, replaced lock and both ranked/recovery cases.

- `test_R1_arbitrary_unqualified_log_also_blocks`
- `test_R1_failed_kernel_slot_programming`
- `test_R1_inferior_before_policy`
- `test_R1_missing_native_setup_measurement`
- `test_R1_native_control_exact_integer_result`
- `test_R1_native_controls_required`
- `test_R1_premature_receiver_in_setup`
- `test_R1_receiver_monitor_cannot_be_missing`
- `test_R1_receiver_monitor_cannot_be_retired`
- `test_R1_unexpected_software_diagnostic`
- `test_R1_unqualified_control_trap`
- `test_R2_contradictory_signal`
- `test_R2_duplicate_running_wrong_thread`
- `test_R2_malformed_frame_remains_rejected`
- `test_R2_malformed_register_names_tuple`
- `test_R2_matching_async_tokens_are_valid`
- `test_R2_unrelated_async_token`
- `test_R3_every_unanchored_tool_role`
- `test_R3_hash_tool_replacement_after_freeze`
- `test_R3_repetition_changed_tool_false`
- `test_R4_absent_actual_CALL_bytes`
- `test_R4_binary_text_mutation_with_unmodified_digest`
- `test_R4_changed_actual_CALL_bytes`
- `test_R4_invalid_return_mapping`
- `test_R4_missing_stop_text`
- `test_R4_negative_fd_and_syscall_fd`
- `test_R4_null_original_buffer`
- `test_R4_null_return_pcs`
- `test_R4_self_consistent_unmeasured_derivation`
- `test_R4_stop_map_handle_substitution`
- `test_R4_supplied_labels_without_raw_measurement`
- `test_R5_256_slots_one_byte_indices`
- `test_R5_no_empty_index_READY`
- `test_R5_valid_256_slots_two_byte_indices`
- `test_R6_ordinary_second_writer_denied`
- `test_R6_replaced_lock_two_writers_cannot_pass`
- `test_R7_completion_integer_ones`
- `test_R7_each_completion_bool_exact`
- `test_R7_internal_snapshot_change_blocks`
- `test_R7_post_ATTEMPTED_exec_assertion`
- `test_R8_rehashed_conflicting_map_file`
- `test_R8_rehashed_conflicting_setup_transcript`
- `test_R8_rehashed_contradictory_original_capture`
- `test_R8_rehashed_missing_binary_text`
- `test_R8_rehashed_missing_original_evidence`
- `test_R9_execution_fault_before_interruption`
- `test_R9_guard_execution_plus_incomplete_death`
- `test_R9_guard_fault_before_MI_parse_failure`
- `test_R9_incomplete_keeps_non_guard_fault`
- `test_R9_multiple_precondition_stages_keep_guard_diagnostics`
- `test_R9_wrong_mode_and_wrong_seals_ranked_refusal`
- `test_positive_raw_path_and_public_replay`

## Full offline verification

Final command, from the canonical checkout, with bytecode writes disabled:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_e0_h2_real_receipt*.py' -v
----------------------------------------------------------------------
Ran 280 tests in 84.653s

OK
```

Exit 0; 161 original tests + 67 completion tests + 52 correction tests; no skips.
Final verbose log SHA-256: `50f9b66bc887b0a82bd6b3acbdecadd00c3724ff6f0f0afee0183027f105f405`.
Logs and temporary editing helpers are outside the repository. Intermediate runs
exposed and corrected a fixture helper argument error. Later passing runs were
repeated only after further invariant corrections; the result above covers the
final implementation. `git diff --check` passes. No model, network test, fuzzing,
real observer, compiler, scientific client or broad alternative experiment was run.

## Preservation

All 231 tracked HEAD-before files are preserved except the six explicitly listed
existing implementation/fixture files. Existing documents have no diff against
HEAD before. All H2A1, earlier verified H2A2 implementation/test slices, frozen
engine/observer/experiment/Q1 documents, original implementation receipts and the
independent review receipt remain byte-identical. Five frozen controlling document
hashes reproduced their independent-review pins; receipt hashes are:

| Preserved receipt | SHA-256 |
| --- | --- |
| Original implementation v0.1 | `1a8e7dce6aa3071c577623d78156e4d2c0067296d4f078f98ea7239e222f53b4` |
| Implementation completion v0.1 | `72362b1a3be2441f3c99fd10979a80d48efe48298cceb2655c065bfbf66b75b4` |
| Independent review v0.1 | `097f63ffc52313e36b8c3c5bd4e508364f220a9c44d81af506a7c954fb056cc9` |

Precommit checks require precisely the eight listed files, no other tracked or
untracked changes, unchanged review/controlling documents and otherwise clean tree.
Only those files are authorized for commit/push. Resulting commit ID and remote
verification are reported outside this receipt to avoid self-reference.

**NO LIVE GDB / NO REAL CANDIDATE COMPILE.** No debugger launch/attachment,
ptrace call, candidate compile/eval/exec/import, E0, dependency_runtime_lock work,
system Python/GDB/package modification or scientific execution occurred in this
circuit. Python runs were ordinary offline test/edit tooling; source/operation
strings were data. This is a statement about this circuit's actions, not monitoring
unrelated host processes.

## Residual assumptions and status

Offline acceptance remains conditional on authenticated frozen tool/reference
material, honest native/supervisor capture provenance, guarded pinned GDB behavior,
exclusive controller/store custody and the existing honest-host/no-concurrent-writer
assumptions. Typed records, matching hashes and synthetic wait/register values do
not establish that the recorded controls or readings happened on a real host.
New role/setup/raw-range supporting evidence is required; historical incomplete
qualification dossiers do not gain completeness by reinterpretation or migration.
Operational admission, current-host compatibility, native read-channel qualification
and genuine native origin remain unperformed. PASS is bounded to this R1-R9 offline
correction and its regression suite. It does not authorize live admission/receipt.

- Implementation verdict: PASS (R1-R9 correction, offline).
- Independent re-review of this correction: not yet performed.
- Live-experiment readiness: NOT_READY; independent review and native admission outstanding.
- external_trust_root: UNRESOLVED; no genuine native receipt.
- dependency_runtime_lock: UNRESOLVED; not begun.
- H2A1: VERIFIED + frozen; unchanged scoped status, no new authority claim.
- H2A2: sealed handoff VERIFIED; surrogate VERIFIED WITH RESIDUAL ASSUMPTION;
  R1-R9 real-receipt offline correction PASS; live admission/receipt unperformed.
- E0: HOLD; unexecuted and unauthorized.
- One next bounded action only: separately authorize an independent OFFLINE
  conformance re-review of this correction commit, preserving frozen documents and
  prohibiting live GDB/candidate operations/E0/dependency-lock work. Not performed.

Finish at correction publication. No next action or live experiment is authorized
or performed by this receipt.
