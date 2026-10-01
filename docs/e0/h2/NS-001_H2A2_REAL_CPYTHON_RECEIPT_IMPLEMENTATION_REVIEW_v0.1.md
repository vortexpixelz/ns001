# NS-001 H2A2 real CPython receipt implementation review v0.1

Date: 2026-10-01 (America/New_York).
Reviewed checkpoint / HEAD before: `48489e8abc1d9432365a1fdb1cdf8fce40c09070`.
Review branch: `codex/h2a2-real-receipt-review`.

**PARTIAL. Live-experiment readiness: NOT_READY.** The claimed 228 offline tests
independently pass, but the completed implementation does not conform to the frozen
contract. Nine concrete blocking findings are recorded below. This review authorizes
neither repairs nor live admission/receipt. None was performed.

## Authority, scope and method

The user authorized one independent read-only offline conformance circuit, exactly
this receipt, and its commit/push. Implementation, tests, controlling documents,
prior slices and evidence remain unchanged. Temporary synthetic stores and the
bounded review script are outside the repository. Ordinary tooling Python imports
are used for the authorized offline tests/reproductions; the protected candidate
is bytes data only. No candidate compile/eval/exec/import, GDB process/attachment,
ptrace, live CPython experiment, E0 or dependency_runtime_lock work occurred.

This worktree initially had clean detached HEAD
`d9dcfbef1bea173b316bc968fd71421c982422c3`. The requested checkpoint already existed
locally on the original checkout's `codex/e0-h2-preparation` branch. An isolated
review branch was created here from that exact checkpoint; the original checkout
was not changed. HEAD before in this review means the actual reviewed checkpoint.
The resulting review commit is reported outside these bytes to avoid self-reference.

All five real-receipt implementation modules, both real-receipt test modules and
the fixture helper were read in full, together with the five controlling documents
and both implementation receipts. The review traced preparation, raw MI parsing,
ABI decoding, witness construction, durable state transitions, recovery, manifests,
public acceptance and repetition. Prior receipt prose and test counts were treated
as claims to verify. No generic fuzzing or alternative mechanism was attempted.

| Controlling document in this directory | Reproduced SHA-256 |
| --- | --- |
| NS-001_H2A2_REAL_CPYTHON_INPUT_BOUNDARY_SPEC_v0.1.md | `eae004d95046d2c2a83fd7813f4b0485ce792e358403a406859280f4c0fdc564` |
| NS-001_H2A2_REAL_CPYTHON_ENGINE_PROVENANCE_REVIEW_v0.1.md | `3fd49cf843b582ddffed971281e226c2d1f419462c17150ca48e82a3b649453e` |
| NS-001_H2A2_REAL_CPYTHON_NATIVE_OBSERVER_DESIGN_v0.1.md | `cdca62d5f02a468353d4c0ba9113e3d4ced047f4b78f68c949b1141bbad1b075` |
| NS-001_H2A2_REAL_CPYTHON_RECEIPT_EXPERIMENT_DESIGN_v0.1.md | `b120fb71ca537d84926e0b81173d1f867f9e92cbde0c54696191c0a8cafee54d` |
| NS-001_H2A2_REAL_CPYTHON_GDB_Q1_REVIEW_v0.1.md | `6ae726ee2bb2821e4f0a0667f4d4dcefcdd07d49dfdf6e1e0b32d35007eb9339` |

Source references below are repository-relative paths and line numbers at the
reviewed checkpoint. All ACCEPT results below are synthetic validator results,
including its public_accept API; none is an observed native receipt.

## Blocking findings

### R1 — Q1 setup history and lifetime entry coverage are not enforced

References: `e0/h2/real_receipt_integration.py:190-243`, `:374-425`, `:486-497`.
Frozen requirements: Q1 sections 6-7; observer sections 6 and 8; experiment sections
4, 7 and 11. Readback must precede any inferior, unexpected internal diagnostics
must close admission, and premature/extra receiver entries must remain counted.

The setup Transcript is parsed, but preparation consumes only its readbacks. It
does not reconcile inferior inventory, setup stops, lifetime receiver hits or other
command-associated console/log streams with admission. Early ordering compares
show-command tokens with execution-command tokens; it does not prove no inferior
exists. decode_observation later initializes entry/sentinel counts to 1 and every
Q1 fact to True, rather than deriving full history across setup and observation.

Three separate mutations of otherwise valid input each produced ACCEPTED and
public_accept=True: inferior/thread creation before the first readback; a complete
commanded receiver stop at `0x69bff0` in setup before ATTEMPTED; and an additional
maintenance response explicitly reporting an unexpected inserted software
breakpoint. These contradict the submitted positive admission descriptors, which
are still accepted. This is a concrete evidence-consistency defect, independent of
whether a future trusted host can actually execute the frozen hardware policy.

### R2 — MI grammar and async event validation permit false valid transcripts

References: `e0/h2/real_receipt_observation.py:43-83`, `:126-159`;
`e0/h2/real_receipt_integration.py:92-117`, `:245-268`.
Frozen requirements: experiment sections 4 and 7, strict bounded MI parsing,
command/event associations and preservation of signals/unrelated events.

The grammar permits a `{...}` tuple containing bare values and returns a Python
list, erasing the distinction from a valid MI value list. Replacing native-pair
`register-names=["rip",...]` with invalid `register-names={"rip",...}` still
produced ACCEPTED/public ACCEPT. The integrated consumer therefore accepts a
malformed representation as valid register evidence.

Async record tokens are parsed but ignored when stops bind to execution_token.
Changing both stop prefixes to unrelated `999*stopped` still accepts. Repeated
`*running` events, including thread-id 999, also accept; execution_running is not
used to enforce a run/stop transition. Finally, adding `signal-name="SIGSEGV"`
to both otherwise qualified stop records still accepts: snapshot checks only a
subset of fields and does not reject contradictory signal evidence. These are
concrete parser/event differential cases absent from the submitted suite. A frame
tuple changed to a result list was also tried and correctly aborted; not every
malformation bypasses validation.

### R3 — Some tool pins are self-consistent replacements, not frozen identities

References: `e0/h2/real_receipt_policy.py:210-228`;
`e0/h2/real_receipt_integration.py:323-334`, `:813-856`;
`e0/h2/real_receipt_evidence.py:339-372`.
Frozen requirements: input specification sections 3, 6 and 9; experiment sections
2, 10 and 11, all tool identities frozen independently before registration.

The executable/package/version/ABI/site/GDB descriptor comparison is exact, and
each named artifact is hashed fully. However, most role pins are checked against
the bytes submitted alongside those same pins. E binds controller, bootstrap,
qualification, decoder and provenance, but does not bind launcher_gdb,
launcher_cpython, mi_parser or hash_tool to the already retained role dossier.
Store.freeze retains content hashes without a complete role-to-hash commitment
which preparation compares against. Presence of an old frozen artifact does not
prevent a new supplied artifact being used by the validator.

After freeze, changing only hash_tool bytes and its matching supplied pin, without
refreezing or changing E, produced ACCEPTED/public ACCEPT. The new hash is absent
from the hash-addressed frozen qualification directory. Two distinct accepted
attempts, with only the second using that replacement, also returned
compare_repetition=True. Thus tool identity changes can be omitted from semantic
comparison; preserving E hashes alone does not preserve all substantive identities.

### R4 — Native derivation/text admission accepts invalid or unsupported assertions

References: `e0/h2/real_receipt_observation.py:221-240`;
`e0/h2/real_receipt_integration.py:313-321`, `:378-425`, `:479-497`.
Frozen requirements: observer sections 4-6; experiment sections 2, 5 and 8; Q1
section 7, direct raw native derivation and complete independent unmasked text.

Derivation sites, syscall values, counts and pointer associations are supplied in
a dataclass; they are not derived from the setup transcript's native stops and
reads. original_buffer is never validated. FD(A) has no nonnegative/type check,
and return_pc_in/out are compared only to one another. A null original buffer,
or FD=-1 paired with syscall_fd=-1 and two null return PCs, each independently
produced ACCEPTED/public ACCEPT. Those cannot constitute the required successful
pread/call/return evidence even under an honest-capture assumption.

Text admission compares submitted range/digest descriptors. Neither reference
text nor independently read supervisor text is required or hashed here. maps.stop1
and maps.stop2 are required to equal the serialized earlier admission text list,
rather than being decoded current maps/code/backing-handle observations. The setup
positive fixture contains readbacks only; its qualification text hashes are hashes
of short labels, despite a declared full executable-range length. This accepted
interface does not require the raw evidence stipulated by the frozen design.
The paired snapshots also contain no actual caller CALL-byte read or full code
comparison; expected `ffd0` in admission stands in for that measurement.

The compiler range is 3,026,877 bytes. Hex contents for just two complete MI text
captures require at least 12,107,508 bytes, exceeding Transcript's total 8,388,608
byte bound even before other evidence. No implemented separate raw text-capture
interface closes that gap. This is an implementation/interface gap, not a claim
that all trusted native-origin evidence could be authenticated without assumptions.

### R5 — Dictionary decoder accepts an incompatible pinned ABI layout

Reference: `e0/h2/real_receipt_abi.py:135-183`.
Frozen requirement: experiment section 6, supported layout, index width/capacity
and bounds must agree; malformed memory cannot become valid roots/bindings.

The decoder accepts any width in {1,2,4,8} if indexbytes/slots is integral. It does
not enforce the CPython width selected by dk_size. A 256-slot dictionary using
one-byte indices, with two apparently valid entries, was supplied at both native
stops. Both root/binding decodes succeeded and public ACCEPT remained True.
For the pinned CPython layout a 256-slot table uses two-byte indices: the current
decoder reads the wrong index interpretation and entry offset as valid evidence.
The version-matched local header `/usr/include/python3.12/internal/pycore_dict.h`
lines 97-105 corroborates this rule; it is supporting static layout evidence,
not runtime qualification. The frozen design independently requires malformed
layouts to fail closed.

An additional READY-only table with every empty index replaced by a dummy also
accepted; the width counterexample alone is sufficient for the blocking ABI verdict.
Other bounded bytes/tuple/vector/Unicode/PyLong/bool decoding has useful exact-type,
signed-length, normalization, terminator and range checks. No padding/fallback to
expected payload bytes was found. Those strengths do not close this dict defect.

### R6 — Lock-file replacement breaks exclusive retained store custody

Reference: `e0/h2/real_receipt_evidence.py:289-337`.
Frozen requirements: input specification section 9; experiment section 3,
exclusive retained ownership and lost/replaced custody must stop a stale writer.

The store flocks an open lock inode, but check() rereads only store.json and custody.
It does not bind the open lock to the current lock pathname/inode. In a temporary
store, replacing the lock file while the first Store remained open allowed a second
Store to acquire the new lock. Both check() calls passed. This demonstrates two
simultaneously admitted store writers after a custody replacement; it does not
require a hostile kernel or modifying any repository evidence.

The ordinary transition chain, durable ATTEMPTED gate, reserved-only recovery,
terminal refusal/abort rejection and incomplete-package terminal preservation are
otherwise exercised successfully by the suite. Their correctness under normal
conditions does not supply this missing custody check.

### R7 — Admission remains mutable and completion facts permit bool/int coercion

References: `e0/h2/real_receipt_evidence.py:557-579`;
`e0/h2/real_receipt_integration.py:444-501`;
`e0/h2/real_receipt_observation.py:355-362`.
Frozen requirements: continuous no-substitution/guard coverage, actual completion
facts and no execution attempt at any covered stage.

Frozen dataclasses contain mutable dictionaries. Attempt retains the caller's
Preparation object; finish does not revalidate/snapshot its full preparation and
guard state. Adding `exec` to its execution_operations after ATTEMPTED still
produced ACCEPTED/public ACCEPT with an empty observation.guard_operations tuple.
The receipt does not reconcile these two evidence inputs. This probe records a
synthetic operation assertion only; it never invokes exec on the candidate.

Replacing all completion booleans with integer 1 also produced ACCEPTED/public
ACCEPT. Equality with an expected dict treats 1 as True; exact types are not checked,
and measured_witness manufactures the normal observer_stop/end booleans afterward.
Missing keys/False completion do abort, but malformed required facts cannot become
clean completion through Python equality.

### R8 — Public package verification does not require all original raw evidence

Reference: `e0/h2/real_receipt_integration.py:688-750`.
Frozen requirement: experiment section 10, complete original raw capture and native
provenance; correct manifest hashes do not replace absent evidence.

After a temporary positive was written, removing capture.json and
observer/native-stops.json and recomputing the capture/package manifests and sidecar
over the reduced retained set still returned public_accept=True. The immutable
terminal and witness were preserved. Neither original file is in the verifier's
mandatory ACCEPT inventory, and the remaining raw records are not reparsed to
reestablish their native-origin links. This is a bounded package-verifier replay
showing a completeness defect; it is not an authorized repair or an assertion
that trusted storage spontaneously rewrites manifests.

Normal manifests correctly cover supplied files, sorted paths, exact lengths/hashes,
external sidecar and no recursive/self hash. Missing B.entry.bin without changing
manifests correctly fails, as the suite proves. These hash checks alone cannot
enforce the omitted mandatory original-evidence inventory.

### R9 — Refusal/recovery orchestration loses supported faults and stage semantics

References: `e0/h2/real_receipt_evidence.py:524-556`, `:638-659`;
`e0/h2/real_receipt_integration.py:443-504`, `:751-811`.
Frozen requirements: input specification section 10; experiment section 12,
ordered stages, one ranked primary, earlier supported faults retained in recovery.

An observation with guard_operations=('execution',) and incomplete confirmed-death
evidence recovered ABORTED/ATTEMPT_INCOMPLETE with diagnostics=[], dropping the
already supplied execution fault. The raw assertion survives in capture.json;
the recovery verdict does not expose the required supported diagnostic. This case
does not falsely ACCEPT, but fails the fixed recovery semantics and circuit-level
execution-violation reporting.

A correctly typed request with wrong mode plus a protected descriptor with wrong
seals throws Invalid('unsupported omission of faults') instead of producing the
ordered precondition refusal. Request value checks run before the frozen protected
input stage; measured_witness includes actual bad seals, witness_codes adds the
higher-ranked fault, but event receives only the earlier selected request fault.
Recovery then selects ATTEMPT_INCOMPLETE with no diagnostics. No normal ranked
refusal is persisted despite complete negative evidence.

CODES/ranked and normal event validators preserve the frozen enum, precedence,
unique primary and recovery-only ATTEMPT_INCOMPLETE. The blocking defect is the
integrated gathering/persistence path, not a competing enum or rank definition.

## Offline suite, strengths and limits

Executed at the reviewed checkpoint, without bytecode files:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_e0_h2_real_receipt*.py' -v
----------------------------------------------------------------------
Ran 228 tests in 36.220s

OK
```

The complete verbose log SHA-256 is
`909a29477cc6276382a9c254a3912673a9e2877f3062a528c5363ef326588a24`.
This independently confirms the claimed count: 161 original tests plus 67 completion
tests. The tests meaningfully exercise code, including per-field engine mismatch,
ABI reads, direct source mutations, token/result errors, partial capture, actual
argument substitutions, fsync failure, reserved recovery, fixed write cuts,
terminal preservation and repeated positives. They are not merely printed expected
verdicts. However, their positive fixture mirrors admission labels/digests rather
than producing the full frozen raw history, and its negative mutations do not cover
the concrete bypasses above. Test PASS does not justify conformance PASS.

Scope/claim inspection found no live control API, candidate compile/eval/exec/import,
compiler/parser correctness, runtime/dependency integrity, gate-resolution or E0
readiness expansion in the reviewed slice. Literal source bytes are decoded/read/
hashed externally; no missing-payload -> expected-fixture fallback was found. Lone,
reversed, duplicate and mismatched normal native pairs generally fail/abort in
existing tests; R1/R2/R4/R5 still invalidate the full required pair associations.
Repetition uses canonical records and retains distinct IDs, but R3 proves a
substantive observed tool identity change can escape the compared record set.

## Preservation and publication checks

All 230 tracked checkpoint files were SHA-256 inventoried and checked unchanged.
The initial and post-review tracked diffs are empty. The only intended repository
addition is this receipt; precommit status/index/diff checks restrict publication
to it. Comparison of the checkpoint against pre-implementation
`345c6497f4d715a5131e0ca386fd8eea9b221c6e` lists only this slice's five implementation
modules, three test/helper files and two implementation receipts, confirming the
controlling documents, H2A1 and previous H2A2 slices were preserved across those
implementation commits as well as this review. No unrelated files were changed.

Read-only hashing reproduced the frozen local CPython/GDB/loader pins:

| Artifact | SHA-256 |
| --- | --- |
| /usr/bin/python3.12 | `e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f` |
| /usr/bin/gdb | `3832cc070ae1716e322105d3b39fb398695e5f031c9d39224cf227a8c2b889f6` |
| /lib64/ld-linux-x86-64.so.2 | `c20a2dc8917c755f02b94049356320fe1f62ac7d9f8994731f807d9df39302da` |

These are on-disk preservation checks, not live engine admission or dependency-lock
work. No debugger was launched even for a version query. No installation, package
mutation, native launch/build, candidate compilation/execution/import, scientific
client or E0 command occurred. This is an action-bounded statement about this review,
not surveillance of unrelated host processes. Only administrative branch/receipt
commit/push is authorized network publication.

## Retained bounded reproductions

The following script and its exact final output retain the review evidence without
depending on temporary storage. It uses the unchanged checkpoint fixtures to create
the baseline, then independent fixed mutations. Each complete flow invokes the
actual Store/Attempt/Transcript/Decoder/public_accept implementation. Scratch stores
are private temporary directories. The reduced-package case and lock-replacement
case modify only their own synthetic stores. No repo implementation/test is edited.
The malformed dictionary header is a byte-level mutation, not a native launch.
Reproduction script SHA-256:
`2547282264b0924cd13a7040dc9b4843301f909c2ef815e36f966f4618f3c88e`.
Final output SHA-256:
`760d0f24fa51dc71e89533a2c5f3a2406915b9d46581a85bfb43f0e799a81ac3`.
Run from the checkpoint repository with PYTHONDONTWRITEBYTECODE=1 and the script
saved outside the repository. The first draft needed its repository sys.path added;
an intermediate execution stopped at the R9 exception before it was explicitly
captured. The final execution completed with exit 0; intermediate runs did not
change repository files or findings.

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
                return print(json.dumps(dict(probe=label, result=a.events()[-1])))
            tried = a.attempted()
            if after_attempted:
                after_attempted(p, a)
            o = observation(p, X, e, tried, mutate_memory=mutate_memory)
            if change_o:
                o = change_o(o)
            a.finish(None, o)
            terminal = a.recover()
            print(json.dumps(dict(probe=label, state=terminal['state'], primary=terminal.get('primary_code'),
                public_accept=public_accept(a, a.raw('package-manifest.json'),
                    a.raw('package-manifest.sha256'), _all_files(a), set()))))
        except Exception as exc:
            print(json.dumps(dict(probe=label, error=type(exc).__name__, message=str(exc))))
        finally:
            store.close()

run('baseline')

def early_entry(e, p):
    extra = (Chunk('stdout', b'=thread-group-started,id="i1",pid="401"\n=thread-created,id="401",group-id="i1"\n'),
        Chunk('commands', mi_command(30, '-exec-run')),
        Chunk('stdout', b'30^running\n*running,thread-id="all"\n*stopped,reason="breakpoint-hit",thread-id="401",stopped-threads="all",frame={addr="0x69bff0"}\n'))
    return e, replace(p, transcript=p.transcript + extra)
run('premature_receiver_in_setup', change_p=early_entry)

def initial_inventory(e, p):
    notification = Chunk('stdout', b'=thread-group-started,id="i1",pid="401"\n=thread-created,id="401",group-id="i1"\n')
    return e, replace(p, transcript=(notification,) + p.transcript)
run('inferior_exists_before_policy_readback', change_p=initial_inventory)

def diagnostics(e, p):
    extra = (Chunk('commands', mi_command(30, '-interpreter-exec console "maintenance info breakpoints"')),
             Chunk('stdout', b'~"UNEXPECTED software breakpoint inserted at 0x581feb\\n"\n30^done\n'))
    return e, replace(p, transcript=p.transcript + extra)
run('unexpected_internal_diagnostic_in_setup', change_p=diagnostics)

def shifted_async(o):
    return replace(o, transcript=tuple(replace(c, raw=c.raw.replace(b'*stopped,', b'999*stopped,')) for c in o.transcript))
run('unrelated_async_token_999', change_o=shifted_async)

def repeated_running(o):
    return replace(o, transcript=tuple(replace(c, raw=c.raw.replace(b'*running,thread-id="all"\n',
        b'*running,thread-id="all"\n*running,thread-id="999"\n')) for c in o.transcript))
run('duplicate_running_with_wrong_thread', change_o=repeated_running)

def signal_fields(o):
    return replace(o, transcript=tuple(replace(c, raw=c.raw.replace(b'stopped-threads="all",frame=',
        b'stopped-threads="all",signal-name="SIGSEGV",frame=')) for c in o.transcript))
run('contradictory_signal_in_stop', change_o=signal_fields)

def tuple_as_list(o):
    return replace(o, transcript=tuple(replace(c, raw=c.raw.replace(b'frame={addr=', b'frame=[addr=').replace(
        b'frame=[addr="0x581feb"}', b'frame=[addr="0x581feb"]').replace(
        b'frame=[addr="0x69bff0"}', b'frame=[addr="0x69bff0"]')) for c in o.transcript))
run('MI_frame_tuple_replaced_by_result_list', change_o=tuple_as_list)

def scalar_tuple(o):
    # A malformed MI tuple of values is parsed as a list of values.
    return replace(o, transcript=tuple(replace(c, raw=c.raw.replace(
        b'register-names=[', b'register-names={').replace(b'"rsp"]', b'"rsp"}')) for c in o.transcript))
run('malformed_register_names_tuple_of_values', change_o=scalar_tuple)

def swap_hash_tool(p):
    artifacts = {**p.artifacts, 'hash_tool': b'unfrozen-replacement-hash-tool'}
    pins = {**p.pins, 'hash_tool': digest(artifacts['hash_tool'])}
    return replace(p, artifacts=artifacts, pins=pins)
run('unfrozen_hash_tool_after_freeze', after_freeze=swap_hash_tool)

def mutate_guard(p, a):
    p.guard['execution_operations'].append('exec')
run('execution_guard_change_after_attempted', after_attempted=mutate_guard)

def changed_dict(e, p):
    # No negative count or unmapped data; leave the two named active entries but
    # remove every EMPTY slot by replacing them with DUMMY slots.
    reads = list(p.ready.reads)
    for i, r in enumerate(reads):
        if r.address == DK:
            data = bytearray(r.data)
            data[34:40] = bytes([254] * 6)
            reads[i] = replace(r, data=bytes(data))
    return e, replace(p, ready=replace(p.ready, reads=tuple(reads)))
run('dict_no_empty_slot_READY', change_p=changed_dict)

def wrong_index_width(mem):
    old = mem.ranges[DK]
    header = bytearray(old[:32])
    header[8:10] = bytes([8, 8])
    header[16:24] = (168).to_bytes(8, 'little')
    mem.ranges[DK] = header + bytes([0, 1]) + bytes([255] * 254) + old[40:72]
run('dict_256_slots_with_one_byte_indices_at_native_pair', mutate_memory=wrong_index_width)
run('completion_integer_ones_instead_of_booleans', change_o=lambda o: replace(o,completion=dict.fromkeys(o.completion,1)))

def malformed_complete_guard(o):
    return replace(o, guard_operations=('execution',), completion={**o.completion, 'pidfd_death_confirmed': False})
run('known_execution_fault_lost_on_incomplete_completion', change_o=malformed_complete_guard)

def erase_package_artifact(p, a):
    pass

with tempfile.TemporaryDirectory(prefix='ns001-review-package-') as td:
    from e0.h2.real_receipt_evidence import manifest
    store = Store(Path(td) / 'store', NS, create=True)
    try:
        e, p = preparation(X)
        freeze(store, e, p)
        a = store.reserve(e, request(e))
        a.prepare(p)
        tried = a.attempted()
        a.finish(None, observation(p, X, e, tried))
        for name in ('capture.json', 'observer/native-stops.json'):
            (a.path / name).unlink()
        files = _all_files(a)
        capfiles = {n:b for n,b in files.items() if n.startswith('qualification/') or n.startswith('1/observer/')}
        (a.path / 'capture-manifest.json').write_bytes(canonical(manifest('capture', X, digest(canonical(e)), capfiles)))
        files = _all_files(a)
        raw = canonical(manifest('package', X, digest(canonical(e)), files))
        (a.path / 'package-manifest.json').write_bytes(raw)
        (a.path / 'package-manifest.sha256').write_bytes((digest(raw)+'\n').encode('ascii'))
        print(json.dumps(dict(probe='rehashed_package_missing_original_observation_and_native_stop_file',
            public_accept=public_accept(a,raw,a.raw('package-manifest.sha256'),_all_files(a),set()))))
    finally:
        store.close()

with tempfile.TemporaryDirectory(prefix='ns001-review-refusal-') as td:
    store = Store(Path(td) / 'store', NS, create=True)
    try:
        e, p = preparation(X)
        freeze(store, e, p)
        r = json.loads(request(e))
        r['parameters']['mode'] = 'eval'
        a = store.reserve(e,canonical(r))
        try:
            a.prepare(replace(p,protected={**p.protected,'seals':0}))
            print(json.dumps(dict(probe='wrong_protected_seals_and_wrong_mode',primary=a.events()[-1]['primary_code'])))
        except Exception as exc:
            print(json.dumps(dict(probe='wrong_protected_seals_and_wrong_mode',
                error=type(exc).__name__, message=str(exc), recovery=a.recover()['primary_code'])))
    finally:
        store.close()

run('derivation_original_buffer_null', change_p=lambda e,p: (e,replace(p,derivation=replace(p.derivation,original_buffer=0))))
run('derivation_negative_fd_and_null_return_pc', change_p=lambda e,p: (e,replace(p,derivation=replace(p.derivation,fd=-1,syscall_fd=-1,return_pc_in=0,return_pc_out=0))))

with tempfile.TemporaryDirectory(prefix='ns001-review-lock-') as td:
    root = Path(td) / 'store'
    first = Store(root, NS, create=True)
    (root / 'lock').unlink()
    (root / 'lock').write_bytes(b'')
    second = Store(root)
    try:
        first.check()
        second.check()
        print(json.dumps(dict(probe='replaced_lock_allows_two_active_stores', result='both check() pass')))
    finally:
        second.close()
        first.close()

with tempfile.TemporaryDirectory(prefix='ns001-review-repetition-') as td:
    from e0.h2.real_receipt_integration import compare_repetition
    store = Store(Path(td) / 'store', NS, create=True)
    try:
        attempts = []
        for ordinal in (1,2):
            x = NS + ':' + str(ordinal)
            e,p = preparation(x)
            freeze(store,e,p)
            if ordinal == 2:
                p = swap_hash_tool(p)
            a = store.reserve(e,request(e))
            a.prepare(p)
            tried = a.attempted()
            a.finish(None,observation(p,x,e,tried))
            attempts.append(a)
        print(json.dumps(dict(probe='repetition_with_changed_unfrozen_hash_tool',
            result=compare_repetition(*attempts))))
    finally:
        store.close()
```

Exact final output:

```text
{"probe": "baseline", "state": "ACCEPTED", "primary": null, "public_accept": true}
{"probe": "premature_receiver_in_setup", "state": "ACCEPTED", "primary": null, "public_accept": true}
{"probe": "inferior_exists_before_policy_readback", "state": "ACCEPTED", "primary": null, "public_accept": true}
{"probe": "unexpected_internal_diagnostic_in_setup", "state": "ACCEPTED", "primary": null, "public_accept": true}
{"probe": "unrelated_async_token_999", "state": "ACCEPTED", "primary": null, "public_accept": true}
{"probe": "duplicate_running_with_wrong_thread", "state": "ACCEPTED", "primary": null, "public_accept": true}
{"probe": "contradictory_signal_in_stop", "state": "ACCEPTED", "primary": null, "public_accept": true}
{"probe": "MI_frame_tuple_replaced_by_result_list", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "public_accept": false}
{"probe": "malformed_register_names_tuple_of_values", "state": "ACCEPTED", "primary": null, "public_accept": true}
{"probe": "unfrozen_hash_tool_after_freeze", "state": "ACCEPTED", "primary": null, "public_accept": true}
{"probe": "execution_guard_change_after_attempted", "state": "ACCEPTED", "primary": null, "public_accept": true}
{"probe": "dict_no_empty_slot_READY", "state": "ACCEPTED", "primary": null, "public_accept": true}
{"probe": "dict_256_slots_with_one_byte_indices_at_native_pair", "state": "ACCEPTED", "primary": null, "public_accept": true}
{"probe": "completion_integer_ones_instead_of_booleans", "state": "ACCEPTED", "primary": null, "public_accept": true}
{"probe": "known_execution_fault_lost_on_incomplete_completion", "state": "ABORTED", "primary": "ATTEMPT_INCOMPLETE", "public_accept": false}
{"probe": "rehashed_package_missing_original_observation_and_native_stop_file", "public_accept": true}
{"probe": "wrong_protected_seals_and_wrong_mode", "error": "Invalid", "message": "unsupported omission of faults", "recovery": "ATTEMPT_INCOMPLETE"}
{"probe": "derivation_original_buffer_null", "state": "ACCEPTED", "primary": null, "public_accept": true}
{"probe": "derivation_negative_fd_and_null_return_pc", "state": "ACCEPTED", "primary": null, "public_accept": true}
{"probe": "replaced_lock_allows_two_active_stores", "result": "both check() pass"}
{"probe": "repetition_with_changed_unfrozen_hash_tool", "result": true}
```

## Final verdict and status

- scope verdict: VERIFIED — offline claim ceiling preserved; no prohibited action.
- Q1 policy verdict: PARTIAL — R1, R4, R7; intent/readbacks do not establish the required full history.
- engine admission verdict: PARTIAL — exact ENGINE comparison verified, frozen tool binding and raw live association incomplete (R3, R4).
- MI parser verdict: PARTIAL — malformed tuple acceptance and async/signal inconsistencies (R2).
- ABI decoder verdict: PARTIAL — incompatible dict index width accepted (R5).
- paired-stop verdict: PARTIAL — required history/native CALL/ABI associations can falsely pass (R1, R2, R4, R5).
- byte-receipt verdict: PARTIAL — actual payload/type/length/hash pipeline verified locally, derivation/A/native association blocked (R4, R5).
- lifecycle/recovery verdict: PARTIAL — retained lock replacement, mutable admission and recovery diagnostic loss (R6, R7, R9).
- evidence-package verdict: PARTIAL — public ACCEPT can omit original observation/native stop files (R8).
- refusal semantics verdict: PARTIAL — frozen ranking verified locally, integrated stage/diagnostic persistence fails (R9).
- determinism verdict: PARTIAL — distinct IDs/canonical comparison implemented, changed hash-tool identity can compare equal (R3).
- offline test verdict: 228 PASS, exit 0; concrete adversarial conformance coverage PARTIAL.
- preservation verdict: VERIFIED — all 230 existing tracked files unchanged; one receipt added; no live experiment or prohibited candidate operation.
- blocking issues: R1 through R9 above; reproduced against the unchanged checkpoint, none repaired.
- implementation-slice verdict: PARTIAL.
- live-experiment readiness: NOT_READY.
- external_trust_root status: UNRESOLVED; no genuine native receipt.
- dependency_runtime_lock status: UNRESOLVED; not begun.
- H2A1 status: VERIFIED + frozen, unchanged scoped status; no new authority claim.
- H2A2 status: sealed handoff VERIFIED; surrogate VERIFIED WITH RESIDUAL ASSUMPTION, unchanged; real receipt implementation PARTIAL; live admission/receipt unperformed.
- E0 status: HOLD; unexecuted and unauthorized.
- one next bounded action only: separately authorize one offline implementation/test correction circuit limited to R1-R9, with its own conformance review checkpoint and no live experiment. Not authorized or performed here.
