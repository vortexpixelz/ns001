# NS-001 H2A2 real CPython receipt implementation correction v0.2

Date: 2026-10-01 (America/New_York).
Branch: `codex/e0-h2-preparation`.
HEAD before: `5d26b68a665b7af07a33cb99fd765da47995873b`.

**Implementation verdict: PASS. RR1-RR4 CLOSED OFFLINE.**
Live-experiment readiness remains **NOT_READY**: this verdict is bounded synthetic
implementation evidence and does not authorize or establish a live native receipt.

## Authority and scope

One bounded OFFLINE implementation-correction circuit against the remaining RR1-RR4
in the unchanged correction re-review v0.1. No experiment redesign or substantive
frozen-design change. Earlier receipts retain their historical verdicts unchanged.
Only the following four files are authorized for this correction's commit and push:

- `e0/h2/real_receipt_integration.py`
- `tests/real_receipt_fixtures.py`
- `tests/test_e0_h2_real_receipt_correction_v2.py`
- `docs/e0/h2/NS-001_H2A2_REAL_CPYTHON_RECEIPT_IMPLEMENTATION_CORRECTION_v0.2.md`

The commit containing this receipt is reported separately to avoid self-reference.

## RR1 — Complete hardware history and receiver lifetime

**CLOSED OFFLINE.** Replay successful control results in retained record order across
setup and observation, carrying active breakpoint identities and addresses from setup
into the receipt pair. Receiver insertion precedes the first setup continuation.
Receiver deletion or replacement cannot be repaired by a later descriptor. Duplicate
or reused identities/sites, unknown retirement, unassociated hardware results,
ambiguous retirement results, inventory disagreement, extra slots and out-of-phase
insertion fail closed. Each execution phase requires its exact permitted active sites.

The frozen temporary sequence is wrapper entry, pread return (spanning syscall
entry/exit), post-resize, wrapper RET, retirement before blocked READY, then caller
admission. Receiver remains active throughout. Q1 section 5 and experiment section 5
control that sequence; the implementation does not invent a new experiment path.
The prior synthetic constructor omitted these temporary insert/delete commands. It now
retains the complete sequence and updates independent native-stop token associations;
qualification bytes and controlling documents are unchanged. Missing insertion and
missing retirement regressions refuse, while the complete positive baseline accepts.

Actual active counts derive from successful retained commands/results and reconcile
with independent native controls. Receipt receiver coverage and observer witness
sentinel state derive from replayed inventory, replacing the stale setup/descriptor
and sentinel success assumptions. Inventory readback must equal the replayed state.
No disabled or unexpected software/hardware site is promoted into qualifying evidence.

Faithful re-review deletion `-break-delete 1` after caller capture before CALL:
ABORTED / ATTEMPT_INCOMPLETE, public ACCEPT false. Faithful additional READY wrapper
hardware insertion: REFUSED / OBSERVER_UNQUALIFIED, public ACCEPT false. Independent
phase, deletion, omitted temporary-control and inventory variants also fail closed.

## RR2 — Process/thread custody

**CLOSED OFFLINE.** Creation and exit notifications update explicit live group/thread
state and retained seen identities. Each stop retains its contemporaneous live custody;
subsequent raw reads must still have that custody. Exit before the two completed
receipt captures aborts. Recreating a seen identity cannot restore custody. Commands
following terminal death are rejected. Snapshot association uses the live state at
the stop, allowing expected terminal death only after completed capture and preventing
later dead-thread claims from retrospectively qualifying a snapshot.

The exact retained `=thread-exited,id="401",group-id="i1"` between caller and receiver
now yields ABORTED / ATTEMPT_INCOMPLETE, public ACCEPT false. Group exit, unknown
thread exit and stale-identity recreation also fail closed. Single-thread baseline,
matching-token MI and death notifications after completed capture remain valid; final
completion/death-chain checks remain required.

## RR3 — All addressed MI compiler-text measurements

**CLOSED OFFLINE.** Every retained stopped MI memory read is bounded and associated
with its exact requested range. Reconcile every intersection with the qualified
compiler executable mapping against the actual supervisor binary bytes for that
stopped epoch, including setup, READY, caller and receiver. Supervisor text still
requires exact frozen-reference equality and backing-map identity. The caller/receiver
site reads remain mandatory. No missing MI coverage is generated from reference bytes;
reads outside compiler text remain object/other evidence. Ambiguous overlapping
snapshot reads continue to refuse, so conflicting overlap cannot qualify. Native and
mapping arithmetic retain bounded lengths and 64-bit overflow checks.

The separate complete binary transport remains intact. Transcript, parser, line,
memory-read and canonical-record size limits are unchanged.

Exact additional actual MI byte `cc` at `0x500000` versus supervisor/reference `00`:
ABORTED / ATTEMPT_INCOMPLETE, public ACCEPT false. Another address/range contradiction
and overlapping contradiction fail closed. Matching non-site MI bytes and a read
outside compiler text preserve positive acceptance and package replay.

## RR4 — Supported faults survive later decoding failure

**CLOSED OFFLINE.** Gather independent guard, protected-final, dispatch, source-capture
and map-association faults before MI decoding, persist them durably in
`supported-faults.json`, and merge with later observed faults using the unchanged
frozen ranking. Malformed ancillary map data cannot prevent retention of already
supported guard/object faults. No diagnostic is manufactured from an unobserved MI
fact. Recovery-only ATTEMPT_INCOMPLETE and normal primary-code precedence are unchanged.

Exact protected-final seals `15 -> 0` plus malformed MI:
ABORTED / ATTEMPT_INCOMPLETE with `OBJECT_SUBSTITUTION` retained, public ACCEPT false.
Execution-guard plus incomplete completion still retains EXECUTION_PROHIBITED.
Execution plus malformed MI, combined supported faults plus interrupted observation,
and independently observed map mismatch plus malformed MI retain their diagnostics.
Malformed MI alone retains diagnostics=[]; no fault is invented to make the test pass.

## Prior closed findings

No redesign or expansion of R3/R5/R6/R7/R8. Their implementations outside the bounded
integration invariant repairs are unchanged. Existing regressions and retained
reproductions confirm:

| Finding | Result |
| --- | --- |
| R3 frozen tool roles | All eleven roles remain independently bound; replacements refuse; changed-role repetition false. |
| R5 dictionary ABI width | Invalid 256-slot/one-byte table refuses; valid two-byte table decodes compile binding. |
| R6 lock custody | Stale first and replacement second Store fail; ordinary competitor denied; original normal custody valid. |
| R7 admission/types | Detached admission mutations refuse; integer completion booleans abort. |
| R8 mandatory inventory | Rehashed omissions of capture/native stops/binary evidence cannot publicly accept; original journal remains historical. |

## Regression inventory and complete offline suite

New durable regressions: **28**, all in `test_e0_h2_real_receipt_correction_v2.py`.
They exercise real local Store/Attempt/Transcript/Decoder/public-accept replay using
synthetic evidence, rather than interpreting protected candidate bytes:

- `test_RR1_exact_receiver_delete_after_caller`
- `test_RR1_caller_retirement_after_caller`
- `test_RR1_unknown_retirement`
- `test_RR1_exact_extra_wrapper_at_READY`
- `test_RR1_other_derivation_site_at_READY`
- `test_RR1_duplicate_receiver_identity`
- `test_RR1_wrong_initial_derivation_phase`
- `test_RR2_exact_thread_exit_before_receiver`
- `test_RR2_process_exit_before_receiver`
- `test_RR2_stale_identity_recreation`
- `test_RR2_unowned_exit`
- `test_RR2_terminal_death_after_complete_capture`
- `test_RR3_exact_non_site_contradiction`
- `test_RR3_other_address_contradiction`
- `test_RR3_matching_non_site_read`
- `test_RR3_outside_text_is_not_compiler_evidence`
- `test_RR3_overlapping_contradiction`
- `test_RR3_overflow_rejected`
- `test_RR4_exact_seals_fault_before_malformed_MI`
- `test_RR4_execution_fault_before_incomplete_MI`
- `test_RR4_both_supported_faults_before_interruption`
- `test_RR4_no_fabricated_diagnostic`
- `test_RR1_complete_temporary_sequence_positive`
- `test_RR1_missing_temporary_retirement`
- `test_RR1_missing_temporary_insertion`
- `test_RR4_map_fault_survives_malformed_MI`
- `test_RR1_inventory_readback_extra_active_site`
- `test_RR1_unassociated_hardware_result`

Final complete offline command:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_e0_h2_real_receipt*.py' -v
Ran 308 tests in 109.730s
OK
```

**308 passed; 0 skips; 0 failures/errors; exit 0.** Includes 161 original, 67
completion, 52 prior correction and 28 v0.2 correction tests. Final verbose log
SHA-256: `42c4756c2d90703cd1c64ab2a3eec46e10b09b7cba1214bd4d4c84b77f0f7473`.
An initial development run exposed an out-of-range setup-path index for an extra
execution; it was repaired to raise Invalid and fail closed. Subsequent complete
runs passed, including the final unchanged implementation checkpoint above.

Retained original/correction re-review scripts were extracted to temporary files.
Their sources match the historical SHA-256 pins byte-for-byte; none of those receipts
was edited. The original script prefix is unchanged; its lock/repetition tails are
faithfully covered by the retained re-review probes and supplement, which explicitly
handle their now-correct refusals. All four final script runs exit 0: **65 outputs**
(35 probes, 1 text probe, 10 supplement, 19 original prefix). All five new RR1-RR4
re-review cases have public ACCEPT false; supported diagnostic retention is verified.
Only the positive baseline's explicit public_accept field is true.

| Script | Source SHA-256 | Output SHA-256 | Exit |
| --- | --- | --- | --- |
| probes.py | `32a98d9afcfbf09ba99b3d90fecbe88f9a698ced7b46e2563482a7d21c4eac19` | `6d161f41e173093c48e07b5cf9f574560d83ed891dbffd762edb2de51db003bf` | 0 |
| text-probe.py | `011609aa097ddbaa7a1aa616ff60299cdce29414495a8670adbe0478023814e0` | `334c52c01e89ef74e801a66a89df59901b2cec4b08711120f2345211d35958d9` | 0 |
| supplement.py | `73bcc844adecefc10a5bec0c362d6188305e97c7f9d5b353986ef04377bc2574` | `9da1e51b34d1dd05a01f214e2d70e0475f93a5cb77f7c371897abfdec919e79a` | 0 |
| original-prefix.py | `cfa7ae2f90fb6f58080d367f11ec606f28ca7da2269fbc4e28320013341dcdba` | `85e8292d47c22bb809a64d59d060e420a36431fff8789172d01bc373d41a71f9` | 0 |

## Preservation and precommit scope

Initial branch and HEAD matched the requested canonical checkpoint and the tree was
clean. All **234** checkpoint-tracked files were inventoried from canonical Git
bytes and compared by SHA-256 with current on-disk bytes. **232 remain unchanged**;
the only two modified existing paths are the authorized integration module and
synthetic fixture. The new test module and this one new v0.2 receipt complete the
four-file allowlist. No prior receipt or frozen document changes.
Baseline inventory JSON SHA-256:
`f4bb03e510b037cec57c2416f6ce370d797717a8aeaf77c107fb920f041daf08`.

This byte check preserves all frozen controlling documents, H2A1, prior verified
H2A2 slices, engine provenance, observer design, receipt experiment design, GDB Q1,
and every previous implementation/review/correction receipt including re-review v0.1.
The precommit check requires this exact allowlist, no unrelated tracked/untracked
changes, and no unexpected staged paths. Frozen policy/schema/ABI/evidence/observation
modules remain unchanged. No qualified artifact, package or installed tool was modified.

Static tool-file SHA-256 checks (no tool launch for these checks):

| File | SHA-256 |
| --- | --- |
| /usr/bin/python3.12 | `e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f` |
| /usr/bin/gdb | `3832cc070ae1716e322105d3b39fb398695e5f031c9d39224cf227a8c2b889f6` |
| /lib64/ld-linux-x86-64.so.2 | `c20a2dc8917c755f02b94049356320fe1f62ac7d9f8994731f807d9df39302da` |

**NO LIVE GDB / NO REAL CANDIDATE COMPILE.** No GDB launch/version query/attachment,
ptrace/native control, real candidate compile/eval/exec/import, live receipt experiment,
scientific/client/E0 execution, dependency_runtime_lock action or package/tool mutation
occurred. Offline Python imports only the validators/test fixtures; protected source
is inert bytes evidence. Git push of the authorized correction is the only planned
network mutation. This statement describes this circuit's actions, not surveillance
of unrelated host activity.

## Residual assumptions and gates

Retained/synthetic control and memory inputs are not authenticated native measurements.
Honest host/kernel/debug hardware, native collector correctness, pinned tool/decoder
provenance, local storage/custody and no hostile native writer remain residual
assumptions. Operational breakpoint programming, unmasked reading, native stop reasons,
actual custody/death and genuine live admission remain unperformed. Offline PASS is
bounded to the repaired invariants and tested cases, not proof of every future input.

- Implementation verdict: **PASS**, RR1-RR4 CLOSED OFFLINE; no reproduced false public ACCEPT remains.
- Frozen semantics: unchanged; no substantive frozen-design contradiction found.
- external_trust_root: **UNRESOLVED**; no genuine native receipt.
- dependency_runtime_lock: **UNRESOLVED; not begun**.
- H2A1: **VERIFIED + frozen**, unchanged scoped status.
- H2A2: sealed handoff VERIFIED; surrogate VERIFIED WITH RESIDUAL ASSUMPTION;
  narrow engine provenance and prospective observer/Q1 verdicts unchanged;
  this bounded offline implementation correction PASS, pending independent checkpoint
  re-review; live admission/receipt unperformed, readiness NOT_READY.
- E0: **HOLD**, unexecuted and unauthorized.
- One next bounded action: separately authorized independent READ-ONLY OFFLINE re-review
  of this committed correction checkpoint. Not performed here; no live experiment.

## Exact retained reproduction outputs

### probes.py

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
```

### text-probe.py

```text
{"probe": "NEW_R4_MI_text_differs_from_supervisor_reference", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "diagnostics": [], "public_accept": false}
```

### supplement.py

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

### original-prefix.py

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

Finish here. No next action performed.
