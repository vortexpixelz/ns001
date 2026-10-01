# NS-001 H2A2 real CPython native observer design v0.1

Date: 2026-09-30 (America/New_York). HEAD before:
`d85592da5ccae2a702772b0ceaf6952ef32d8cfd`.
Branch: `codex/e0-h2-preparation`; initial working tree clean.

## Scope and decision

**Observer verdict: OBSERVER_QUALIFIED**, in the expressly requested **document-only,
prospective architecture/evidence-contract sense**: one concrete mechanism is sufficiently
specified for a later bounded experiment. This is not a claim that an observer has been
implemented, attached, dynamically validated, or has witnessed receipt. In particular,
this verdict is not permission to set the existing witness's `observer.qualified=true`
without the separately reviewed, pinned implementation and successful live admission
checks below. The earlier runtime qualification refusal is not retrospectively erased.

Select an external GDB/MI observer, driven by a separate fail-closed supervisor, with
hardware execution stops at the actual builtin entry and its immediately preceding
native indirect-call instruction. Read only registers and raw inferior memory; decode
and hash outside the target. Use one fresh, single-threaded child per committed attempt,
an observer-controlled dispatch barrier, and clean observer-stop completion at entry.
No inferior function calls, injected observer, text patch, or returned-code execution
is necessary. The supporting caller stop establishes callable identity; the receiving
stop alone establishes receipt. They are not interchangeable evidence.

The exact local image and ABI support this design; there is no unresolved choice between
two mechanisms. Whether the intended future execution context permits tracing and two
hardware stops is **unmeasured**, not presumed successful. Those are mandatory admission
checks before dispatch; failure stops that experiment without policy changes or fallback.
No architectural impossibility is established by the present restricted shell's policy.
A design qualification does not satisfy the earlier specification's live qualification
requirements or produce a complete frozen expectation E by itself.

This circuit creates only this document. It does not attach/launch an observer, launch
Python (even for version output), invoke compile/eval/exec/import, execute candidate
source, install/build tools, alter interpreter/policy, begin dependency_runtime_lock,
or run E0. Read-only official documentation retrieval is research for this design;
the proposed experiment is offline. Git publication is the requested administrative act.

## Evidence basis and unchanged boundary

The controlling contract is
`NS-001_H2A2_REAL_CPYTHON_INPUT_BOUNDARY_SPEC_v0.1.md`, SHA-256
`eae004d95046d2c2a83fd7813f4b0485ce792e358403a406859280f4c0fdc564`.
The preserved engine-provenance receipt is
`NS-001_H2A2_REAL_CPYTHON_ENGINE_PROVENANCE_REVIEW_v0.1.md`, SHA-256
`3fd49cf843b582ddffed971281e226c2d1f419462c17150ca48e82a3b649453e`.
That receipt authenticates the executable's Ubuntu archive/package/build origin;
its historical source/build measurements are cited as retained evidence, not newly
reproduced downloads. Its temporary `/tmp/ns001-engine-review` materials are absent
in this session. Do not treat them as presently retained binary qualification inputs.

Current static reads independently reproduce these image facts:

| Fact | Exact observation |
| --- | --- |
| Executable | `/usr/bin/python3.12`, CPython 3.12.3, python3.12-minimal:amd64 `3.12.3-1ubuntu0.17` |
| Executable SHA-256 | `e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f` |
| ELF | ELF64 little-endian x86-64 System V, **ET_EXEC**, not PIE |
| Compiler-bearing image | This executable; DT_NEEDED: libm, libz, libexpat, libc; no libpython |
| Native boundary | `builtin_compile`, first instruction VA `0x69bff0`, file offset `0x29bff0` |
| First instruction | `f3 0f 1e fa` (`endbr64`), before unpacking/conversion |
| Method definition | VA `0xa49ae0`: name `0x70bde7`, method `0x69bff0`, flags `0x82`, doc `0x783a40` |
| Later operations | `_PyArg_UnpackKeywords` call `0x69c044`; filename conversion `0x69c067`; `_Py_SourceAsString` call `0x69c1c2` |
| Supporting dispatcher | FASTCALL-with-keywords vectorcall body VA `0x581f90`; native indirect call `0x581feb`; return PC `0x581fed` |

The native method flags are METH_FASTCALL | METH_KEYWORDS. `PyCMethod_New` at
`0x581b10` selects `0x581f90` for flags `0x82` (selection at `0x581c70`) and writes
that vectorcall pointer at callable offset `0x30`. The dispatcher saves callable
RDI in R12, arguments RSI in R13 and keyword tuple RCX in R14, clears bit 63 of
RDX, loads the method pointer from the callable's method definition, and issues
`call *%rax` at `0x581feb`. This is new corroborating static evidence from this exact
executable, not an assumption about a generic CPython dispatch path.

The [CPython 3.12.3 generated receiver](https://raw.githubusercontent.com/python/cpython/v3.12.3/Python/clinic/bltinmodule.c.h)
and [method dispatcher source](https://raw.githubusercontent.com/python/cpython/v3.12.3/Objects/methodobject.c)
corroborate the signatures and dispatch semantics. They are upstream explanatory
references, not substitutes for the authenticated Ubuntu-patched image. The prior
provenance receipt records the version-matched Ubuntu source/patch review; current
image disassembly controls concrete coordinates and register facts.

There is **no boundary contradiction**. The original PyObject source is reachable
through incoming args[0] before conversions. Neither the caller stop, an audit event,
`builtin_compile_impl`, nor `Py_CompileStringObject` replaces the selected boundary.
If a future mapped image or dispatch path contradicts these facts, STOP; do not move
the receiving point or substitute a different invocation to obtain a positive.

## 1. Required independently established observations

Every positive native witness must establish all of the following, with unavailable
facts remaining unknown, never filled from expected values:

1. The supervised child and its sole thread, stable identity and uninterrupted custody;
   correct process, not merely a matching executable name or recycled PID.
2. The authenticated executable identity, actual mapped compiler-bearing image and
   loader association, and the reviewed native receiving address in that mapping.
3. Actual hardware stop at that entry after the native call, with authenticated stop
   reason, thread and PC; not a supervisor READY/GO message or wrapper report.
4. The exact retained real builtin callable, still the live builtins binding, and its
   method definition/flags/native target; the paired dispatcher-to-entry transition.
5. Actual source PyObject pointer and exact builtin PyBytes type; actual signed length;
   a complete direct read of payload bytes; independently computed SHA-256.
6. Pointer identity with retained derivative B, continuously held alive; equal bytes
   from a different object are insufficient. Witness the original A-to-B derivation.
7. Live sealed A capability association, origin, size, exact seals and independent
   complete A read equal to the native source, with A retained through completion.
8. Actual six positional and one keyword arguments, exact primitive types, names,
   values and ordering; no implicit/default replacement or unobserved source selector.
9. One registered `namespace:ordinal` attempt ID and expectation E, the durable
   ATTEMPTED event digest, and causal observation after its successful synchronization.
10. Continuous qualified observer coverage, exactly one receiving entry for that
    attempt, no early/extra/ambiguous calls, complete terminal observer-stop evidence.
11. No intervening image, callable, retained object, observer or attempt substitution
    between qualification and observation; recheck at stops and fail on discontinuity.
12. Bounded source-operation and non-execution coverage, preserving the original
    specification's refusal/recovery rules and claim ceiling.

The claim ends at input receipt. It proves no parser progress, compilation success,
code-object correctness, execution, scientific result, full trust root, or runtime closure.

## 2. Candidate comparison for this installation

Read-only inventory: GDB `15.1-1ubuntu1~24.04.1` installed, `/usr/bin/gdb` SHA-256
`3832cc070ae1716e322105d3b39fb398695e5f031c9d39224cf227a8c2b889f6`.
`strace` 6.8 and binutils 2.42 are installed. `perf` and `bpftool` PATH entries are
shell dispatchers; actual binaries exist at `/usr/lib/linux-tools/7.0.0-31-generic/`.
`bpftool` is not installed as a separately named dpkg package. LLDB and bpftrace
were not found on PATH. None of these observers was launched. Current shell:
Yama=1, perf_event_paranoid=4, unprivileged_bpf_disabled=2; effective and bounding
capabilities zero, NoNewPrivs=1, Seccomp=2. These observations do not reveal the
seccomp allowlist or prove future attach/hardware-read success.

| Mechanism | Exact point, ABI and recoverable evidence | Process/attempt, mutation, privilege and limits |
| --- | --- | --- |
| **GDB hardware execution stops (selected)** | Explicit relocated addresses `0x581feb` and `0x69bff0`; no static symbol-name lookup required. Registers plus raw memory permit original PyObject, exact type/length/payload, external SHA-256 and all arguments. | Parent-supervised single child, private barrier and paired stops bind attempt. Debug registers, stops, signal handling and timing change; executable text is not patched. Needs permitted ptrace, hardware resources and readable memory. Offline with local images and startup automation disabled. Deterministic semantic witness possible; missing stops, partial reads, decoder errors or tool loss refuse/abort. Trust kernel, hardware, debugger/controller and bounded bootstrap. |
| GDB software breakpoint | Same coordinates and raw data, but must qualify INT3 insertion, PC adjustment and restored bytes at both sites. | Same process/barrier/ABI requirements and ptrace restrictions. Patches target text; disk digest alone then cannot describe observed code. Offline; deterministic witness possible with additional patch evidence. More mutation/accounting than hardware; no automatic fallback. |
| Direct ptrace supervisor | Same hardware debug-register sites, register set and exact memory decoder. `PTRACE_PEEKDATA` or full-count process-memory reads can recover all bytes/arguments; hash externally. | Can combine parent custody, barrier and stop handling in one native program. Must implement/debug thread stops, wait events, signal suppression, debug-register lifecycle, errors and observer-death handling. Same kernel permission restrictions as GDB; no installed qualified supervisor exists. Offline and potentially smaller trusted implementation, but more new mechanism to validate now; no stronger narrow claim. strace alone lacks native user-space receipt decoding. |
| perf/eBPF uprobe | Entry image file offset `0x29bff0`; supporting caller offset `0x181feb`. Kernel resolves mappings/ASLR; manually decode registers, PyObjects and every argument; userspace hashes complete captured payload. Two-byte source is small enough in principle. | Must filter stable process/thread identity and bind private barrier, prove no dropped events and coherent object/A/B state. Ordinary asynchronous events do not stop all relevant mutation while userspace rechecks. Uprobe instrumentation changes execution; stronger coherence requires extra control. Restrictive local perf/BPF policy, no effective capabilities; operational access unestablished. Existing perf/bpftool binaries are not a qualified loader/program. Offline possible; event loss, read faults, mismatched probe/image and buffer truncation must refuse. Greater privileged machinery and weaker simple snapshot coherence. |
| Native in-process instrumentation / debugger API | A hook at this exact instruction could capture registers and objects. GDB/MI supplies external transport only; LLDB API would still require the same decoder. Interposition on another compiler API is not this boundary. | Native injected hook/text rewrite or rebuilt interpreter changes observed artifacts and shares target failure domain. Must qualify modified image/hook and original argument preservation. Offline possible; injection/debugger permissions vary. No suitable qualified hook or LLDB installation found. Same-process honesty and hook integrity are extra assumptions. |
| Existing audit/USDT/profile hooks, wrapper logging, core snapshot, hardware branch trace | Audit/profile labels do not measure this original native vector. A core may preserve bytes but lacks this ordered receipt event; branch trace alone lacks argument contents. | No materially better installed mechanism found. Combining these with stops/decoder reconstructs the selected architecture or adds machinery. Expected bytes, wrapper digest, consumer return and trace labels cannot replace receipt. |

[GDB hardware-breakpoint documentation](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Set-Breaks.html)
supports stopping before an instruction without changing it, subject to hardware
resources. [GDB/MI raw memory operations](https://sourceware.org/gdb/current/onlinedocs/gdb.html/GDB_002fMI-Data-Manipulation.html)
provide transport for bytes; the controller must reject gaps/partial ranges rather
than concatenate a plausible result. These are capabilities, not local runtime tests.
[Linux ptrace](https://man7.org/linux/man-pages/man2/ptrace.2.html) and
[Yama](https://docs.kernel.org/admin-guide/LSM/Yama.html) describe access/parent-custody
constraints; parent-child tracing can satisfy Yama mode 1 but other restrictions
still apply. [Kernel uprobes](https://docs.kernel.org/trace/uprobetracer.html) use
object offsets and explicit argument fetching; an event is not automatically the
required coherent full witness.

The selected architecture is minimal in new observation machinery for this host:
existing external debugger, two hardware sites, one raw decoder and one durable
controller. A single wrapper/dispatcher observation proves only intent. A single
entry hit proves receipt but not by itself the stipulated retained callable/attempt
association. Paired native stops close that gap without changing the receiver.
Direct ptrace could later replace GDB only after separate qualification; it is not
an unresolved competing choice or an authorized fallback in this design.

## 3. Exact native ABI and primitive decoding

All offsets below are for this pinned non-Py_TRACE_REFS, non-debug, LP64 image;
8-byte pointers/Py_ssize_t, little endian. Installed version-matched headers and
actual disassembly support these layouts. Unsupported configuration or inconsistent
live layout refuses; do not apply them to an arbitrary Python 3.12 build.

At `builtin_compile` first instruction:

| Register/data | Decode |
| --- | --- |
| RDI | Module/self; must equal retained real builtins module M. **Not the callable object.** |
| RSI | Pointer to native PyObject* argument vector; validate bounded readable range |
| RDX | Signed positional count, exactly 6; no vectorcall offset flag at this boundary |
| RCX | Exact tuple kwnames, length 1, element exact str `_feature_version` |
| RSI + 8*i | Pointer args[i]; i=0..5 positional; i=6 sole keyword value |
| RSP | Read return address, expected `0x581fed` plus measured load bias |

At the preceding `0x581feb` stop: R12 is actual callable C; RAX must be measured
builtin entry; RDI=M, RSI=args, RDX=6, RCX=kwnames. Validate C/type/binding and all
pointers there. Keep the receiver hardware stop armed; execute only the indirect
CALL (native instruction stepping, never an inferior function-evaluation command).
Require the next receipt stop on the same thread at `0x69bff0`, stack reduced by 8,
return PC `0x581fed`, unchanged argument registers/vector and C in R12. Handle the
single-step and hardware-stop causes without counting one entry twice; ambiguous
trap reasons are refusal. A path bypassing this paired dispatch does not qualify
for this experiment even if it reaches the right bytes. This restriction does not
move the boundary: only the receiving PC produces the `entry` observation.

At the vectorcall body's initial entry `0x581f90`, RDX would instead be `nargsf`;
its bit 63 is stripped by the actual instruction at `0x581f95`. Do not confuse
that convention with the ordinary count at either selected stop.

| Object | Raw decoding rule |
| --- | --- |
| All objects | ob_type at +8; compare pointer to qualified mapped exact type, not type name or subtype flags. Validate each address/read/overflow before dereference. |
| PyBytes B | signed ob_size +16, ob_shash +24, payload +32. ob_shash is not SHA-256. Read exactly measured payload length; exclude terminating NUL. |
| Tuple | signed count +16, item pointers +24; bound count before reading. |
| Exact str | length +16, state word +32: kind=(state>>2)&7, compact bit 5, ASCII bit 6. Compact ASCII data +40; compact non-ASCII data +56; noncompact canonical-data pointer +56. Read length*kind bytes with overflow/range checks; decode 1/2/4-byte code units outside target. Validate flags, scalar values and exact required text. No UTF-8 conversion/cache or inferior Unicode API. |
| Exact int | CPython 3.12 lv_tag at +16, digits at +24, uint32 limbs/base 2^30. Size=tag>>3; sign=1-(tag&3), with zero sign code 1. Validate normalized digits and flags. Zero requires size 0/sign zero; -1 requires size 1/sign negative/digit 1. Do not use pre-3.12 signed-ob_size decoding. |
| Exact bool | ob_type must equal PyBool_Type; True pointer must equal mapped `_Py_TrueStruct`, with consistent native value. Reject bool where exact int is required. |
| C | Exact PyCFunction_Type; m_ml +16; m_self +24; vectorcall +48. m_ml must be expected method definition with flags 0x82 and target entry. |
| M | Exact PyModule_Type; md_dict +16 must be exact PyDict_Type. Decode actual `compile` binding and roots below, without invoking dictionary APIs. |

Type VAs: PyBytes `0xa2bee0`, PyTuple `0xa42c40`, PyUnicode `0xa472c0`,
PyLong `0xa3bf20`, PyBool `0xa2a3a0`, True `0xa2a360`,
PyCFunction `0xa3fb20`, PyModule `0xa3ff00`, PyDict `0xa3d840`.
Apply the verified image mapping/bias, not assumed universal addresses.

For direct dictionary reads, PyDictObject has ma_used +16, ma_version_tag +24,
ma_keys +32, ma_values +40. Keys header: log2_size +8, log2_index_bytes +9,
kind +10, nentries +24, indices +32; entries follow `32 + 2^log2_index_bytes`.
General entries are 24 bytes (hash, key, value); Unicode entries 16 bytes (key,
value). For split layout values come from ma_values[i]; for combined layout use
entry value. Bound counts/indices/shifts to mapped ranges and a frozen maximum
(e.g. 4096 entries for this tiny bootstrap); reject malformed/oversized layouts.
Skip deleted entries, compare exact decoded Unicode keys, require unique binding,
check counts and stable relevant roots/version across the stopped read. A linear
scan needs no target hash computation, equality method or dictionary lookup call.

Required actual values: filename `<ns001-h2a2-real-input-v1>` (exact str), mode
`exec` (exact str), flags 0 (exact int), dont_inherit True (exact bool), optimize
0 (exact int), `_feature_version` -1 (exact int). Record observed values; only then
compare to E. Subclasses, duplicate/extra keywords, coercion, missing arguments,
wrong count or unsupported objects do not inherit expected values.

## 4. Live image and callable association

Future supervisor retains exclusive custody of a fresh child from creation, with
pidfd or equivalent non-reused child/wait identity, process start identity and sole
TID. Never attach by process name or choose the first matching PID. Fail on unexpected
fork/clone/thread/exec transitions; no unobserved sibling may perform the invocation.
GDB all-stop mode is additional protection, not proof that every possible writer is
stopped. The future scope prohibits hostile external writers and shared mutable
payload storage; A seals and immutable B further constrain mutation.

Before bootstrap admission and again while stopped at receipt:

- Independently hash the actual `/proc/<pid>/exe` handle; compare whole bytes to the
  authenticated executable pin, not the pathname. Keep the backing handle open.
- Associate maps device/inode/offset and file-backed segments with that exact handle.
  For a mapping with start S and file offset O, a file byte F maps to S+(F-O) when
  in range. Derive ELF load bias from matching PT_LOAD entries and verify consistency.
  This image is ET_EXEC and expected bias zero; ASLR still affects stack/heap/libraries.
  An unexpected PIE/different image is refusal, not permission to generalize the decoder.
- Verify actual stopped readable executable code ranges against the reference image,
  including the full compiler image's executable PT_LOAD bytes and selected dispatcher/
  receiver instructions. Account for any relocations explicitly or refuse; do not
  equate file-backed maps with unmodified private pages. Check segment permissions,
  reject unexpected writable executable mappings and deleted/replaced backing identity.
  Mutable data are checked semantically (method table/type objects), not compared
  wholesale to unrelocated disk data. A disk hash alone never establishes this step.
- Measure the loader path/image/mapping and inventory native mappings relevant to
  dispatch/observation. Launch with a frozen explicit environment and no LD_PRELOAD,
  LD_AUDIT or alternate library selection; inspect actual mappings for extra native
  interposition. No libpython is the receiver here. A shared libpython with a plausible
  symbol cannot substitute for the executable. Unexpected mappings/patches on the
  measured path refuse. No transitive native/stdlib/package closure is asserted.
- Freeze observer executable, controller, raw decoder, command policy and bootstrap
  hashes before attempt registration; independently recheck them. Disable GDB init
  files, auto-loading, pretty-printers, debuginfod/network, Python command scripts and
  arbitrary command hooks. Restrict its command channel to the reviewed MI/register/
  memory/stop policy; never issue inferior calls or use target-side conditions.

The bounded bootstrap must retain C, B and M strongly through observation. It may
publish **only locator/control roots**, not receipt evidence: a private builtins key
`_ns001_observer_roots_v1` holding a tuple `(B, C, attempt_id, expectation_sha256)`.
Adding this control root does not replace `compile`, alter payload or filename, or
change any frozen completed slice. The observer independently decodes M's dictionary
and that tuple at READY and both native stops. It verifies the ordinary `compile`
value is exactly C, m_self=M, m_ml/flags/target/vectorcall match, and roots/B/C remain
identical. A bootstrap-provided address is only a hint until these native structures
are read and associated; a bootstrap-provided hash/boolean is never a measurement.
Bootstrap provenance and association of M to the actual interpreter builtins remain
part of the reviewed fixed bootstrap, with M corroborated by the real native self
argument and qualified builtin object. This is not protection against a malicious
interpreter manufacturing fake objects/modules.

Paired dispatcher/receiver observations additionally prove which C supplied that
call's target. Checking a dictionary name only at entry would leave that distinction
unproven. Recheck mapping/text/roots while stopped, maintain continuous attachment,
and stop on unexpected signal, state transition or observer discontinuity. A hash
before launch plus a later PC alone is insufficient substitution control.

## 5. Independent byte measurement and A-to-B custody

At receipt, first measure P=*(RSI). Require P equals retained B pointer from the
independently read READY roots, and exact native type PyBytes_Type. Read the signed
length L from P+16. Bound it before allocation/read; for the positive fixture L must
be exactly 2. Never read an unbounded corrupt length. Preserve the two actual bytes
read at P+32 as an observer-owned buffer, with full read counts and no gaps. Confirm
header/roots stable under the stopped snapshot; require ordinary trailing-NUL layout
consistency but do not hash the terminator. Hash **that captured buffer** externally
using pinned SHA-256 tooling; retain the capture and digest. Failed/partial reads
cannot be padded, retried into a positive or supplied from expected fixture data.

Only after measurement compare L and SHA-256/full byte equality with the frozen
fixture: hex `23 0a`, length 2, SHA-256
`32c4858e22cc2c967b42150fa550562a2c839c2cebcaab91cabdf6f4da020022`.
This fixture digest is a comparator, not native evidence. A harness digest, wrapper
bytes, expected buffer, consumer return, repr or PyBytes cached hash is inadmissible.

A must be fresh, witnessed, sealed regular memfd with exactly WRITE/GROW/SHRINK/SEAL
seals and size 2. The independent supervisor participates in the authorized acquisition
and retains its own capability to the **same** kernel object before dispatch; preserve
the kernel-backed inheritance/SCM_RIGHTS transfer chain if a descriptor crosses the
process boundary. No later `/proc/.../fd` pathname reopen is a payload fallback.
An FD number or matching inode alone is not the custody chain. Recheck seals/size/
association through the retained capability before/after measurement. Independently
`pread(A,3,0)` once, require exactly 2 bytes, hash/compare against actual P payload.
Do not ask the stopped inferior to execute fcntl/read/hash functions.

For B provenance the future observer must witness the single A-to-B read, not merely
accept the roots tuple's existence: trace the authorized pread syscall's FD association,
offset 0, count 3, successful result 2 and actual returned memory, and follow the
reviewed native read-wrapper return to its exact bytes object B before READY. If the
wrapper resizes/moves its temporary bytes allocation, follow that return pointer;
never equate the syscall buffer address automatically with final B. Capture wrapper
entry/return identity through the same raw debugger mechanism and exact-image method
resolution, maintain B's strong root through READY, and compare return B to root B.
The future implementation qualification must freeze this helper's address/return
tracking and any resize path before dispatch; it may not infer this transfer from a
Python success report. This is supporting derivation coverage, not another compile
receiving boundary. Its bounded temporary stop can be retired before the two compile
hardware sites are armed. A missing derivation link refuses `derived.from_A`/`same_B`.

The previous surrogate/handoff receipts establish their own completed slices, not
this future object's custody. Reuse their approved semantics in an additive experiment;
do not reuse stale live capabilities or convert byte equality into historical identity.

## 6. Attempt binding, independent control and ordering

Use one fresh child, one reserved ID and one invocation per attempt. No payload
nonce is needed; source and fixed filename remain unchanged. The unique committed
attempt ID, E digest, private one-shot channel and ATTEMPTED event digest are the
minimum control markers. The child cannot mint the observer's receipt or reopen the gate.

1. Controller reserves/registers ID under the retained store's existing namespace and
   ordinal rules. Freeze E/qualification artifacts before registration. Record raw
   request and PREPARED durably; bind the child/control channel to this ID internally.
2. Qualified bootstrap setup finishes outside the exclusive dispatch interval. Observe
   A acquisition/derivation, retain B/C/M, reach a blocked READY barrier, and inspect
   roots and live image while stopped. Lifetime compile-entry monitoring accounts for
   any bootstrap calls separately; none is silently reassigned to the attempt. The
   receiving breakpoint is active before opening the attempt window. Record baseline
   and cumulative counters, retaining unexpected calls rather than filtering by bytes.
3. Confirm effective hardware insertion, correct child/thread/address, complete observer
   coverage and relevant guards. A requested/pending breakpoint is not proof of arming.
   Admission cannot rely only on GDB's breakpoint-table label. The later implementation
   qualification must validate stop semantics and fail on inaccessible debug state or
   unavailable hardware; no software replacement, policy elevation or ignore count.
4. Persist ATTEMPTED through the existing writer, including file synchronization and
   required store-directory/custody synchronization. Independently validate/read back
   its exact canonical bytes/hash and predecessor chain. Read-back alone is not proof
   of durability: the supervisor must own/witness successful synchronization results.
5. Only then release the private one-use gate tied to `(ID,E,ATTEMPTED_digest)`. The
   supervisor's state machine binds every subsequent stop to this child and active ID.
   Channel identity and successful release, not a wall clock or nonce echoed by the
   harness, establish causal order. Lost/duplicate release refuses; no reattempt.
6. Observe the paired native transition, full arguments, actual B and independent A.
   Exactly one receiving entry, no unmatched supporting dispatch, no extra native
   entry regardless of its bytes. Do not select the first of multiple matching calls.
7. Perform the defined clean observer-stop completion below. Persist witness first,
   then the hash-linked terminal event. Observer failure, unknown completion or a
   nonterminal retained attempt recovers to ABORTED without rewriting/retrying it.

Other FASTCALL functions may reach the supporting dispatch site while preparing
bootstrap/control operations. Decode and retain their classification; only actual C
can form the intended pair. Other calls cannot count as native compile receipt. Any
unexpected compile entry before persisted release or during the active attempt is
refused. Single child/thread, unchanged roots, paired PCs/stack and the one-use gate
distinguish "some compile call" from "the call of committed attempt X".

## 7. Independence and acceptable residual assumptions

Independence from harness/consumer: receipt is generated by external native stop and
raw reads, not a harness event/digest or consumer result. Harness markers locate/control
state only. A malicious wrapper cannot manufacture a qualified kernel/debugger stop by
printing a message. The independently reviewed bootstrap still supplies the bounded
non-execution/control flow and roots; its honesty is an explicit scoped assumption,
not proof of independence from every harness action.

Independence from interpreter: controller, hashing, evidence store and byte decoder
run outside its address space; no Python reflection, repr, audit callback, conversion,
pretty-printer or target helper is evaluated to measure receipt. Killing the child
cannot edit the observer's already retained capture. This is stronger isolation than
an in-process hook, but a hostile native interpreter that deliberately fabricates
objects/control state is outside the claim.

Independence from kernel/host: **not provided or demanded**. Trust host/kernel/procfs,
ptrace/debug hardware, memory-read accuracy, GDB/controller/decoder/hash tools, file
synchronization/storage, process custody and no hostile concurrent native writer.
Trust the accepted Ubuntu acquisition chain within the prior provenance scope. Observer
tool hashes identify measured tools; they do not independently authenticate their
entire supply chain or dependencies. Freeze a truthful local origin dossier for those
tools under the trusted-host premise, not a fictitious authenticated archive claim.

No full runtime lock, hostile-root resistance, reproducible build, global execution
trace, perfect scheduling transparency or impossible adversarial-host guarantee is
asserted. Stops/debug registers and supervisor-controlled termination affect target
state/timing; "does not patch instructions" must not be called "non-invasive".

## 8. Deterministic evidence and fail-closed behavior

Use the existing real-input schema and observation ordering; do not extend its exact
key sets. This design supplies how `engine`, `callable`, `observer`, `dispatch`,
`entry`, `protected`, `completion` and `end` facts are measured. `derived` is supported
by the independently captured native read return. Expected values are comparison
inputs only. No positive required field is inferred from absence of an error.

Retain a separate observer-owned forensic transcript (register/memory ranges, full
read results, volatile PID/TID/maps/addresses, stop/step/counter records, causal control
and synchronization results), actual source capture and independent A capture. These
are qualification/supporting evidence outside the fixed canonical schema; do not
insert new raw-address/transcript-hash fields into its records. Package them alongside
original records under existing custody, with a separately retained manifest. They
permit audit of the deterministic assertions; canonical booleans alone are not a
self-authenticating proof. No volatile field is silently normalized into an identity.

Canonical witness records retain artifact hashes, ID/E/event links, measured length/
SHA-256, exact parameter values, ordered semantic predicates/counts and qualified
completion. Exclude volatile PIDs/FDs/inodes/addresses/times as the current contract
requires. Identical semantic inputs serialize identically; raw transcripts naturally
vary. Repetition comparisons strip only ID and derived link hashes as already specified,
never outcomes, measurements or observer failures. This design runs no repetitions.

| Failure | Mandatory disposition |
| --- | --- |
| Observer not attached, unavailable or replaced | Before dispatch: OBSERVER_UNQUALIFIED, no release; no compile. |
| Wrong PID/thread or lost child custody | No attachment_match/live association; refuse before dispatch; preserve uncertainty after it. |
| Wrong mapped executable/loader or changed text | ENGINE_UNQUALIFIED; STOP, no alternate image. |
| Wrong native address/method/callable | ENGINE_UNQUALIFIED or WRONG_COMPILE_CALLABLE according to actual failed predicate; never accept symbol-name resemblance. |
| Not armed, hardware slots unsupported or insertion ineffective | OBSERVER_NOT_ARMED / OBSERVER_UNQUALIFIED as applicable; do not release. |
| Breakpoint never reached, timeout or premature exit | After ATTEMPTED, OBSERVATION_MISSING if a complete qualified negative witness exists; otherwise incomplete attempt ABORTED. No presumed entered=false. |
| Source pointer unreadable or partial memory read | OBSERVATION_MISSING; retain received fragments only as failed evidence. Never pad, repair or silently retry into ACCEPT. |
| Unexpected object type | INPUT_TYPE for measured nonbytes; unavailable bytes/hash stay null. No coercion or repr. |
| Wrong length/payload | INPUT_TRUNCATED, INPUT_APPENDED or INPUT_ALTERED per existing exact fixture rules. |
| SHA-256 calculation/tool failure | Required measurement unavailable: OBSERVATION_MISSING, not comparison success. |
| B/root/A substitution | OBJECT_SUBSTITUTION or WRONG_PROTECTED_OBJECT according to phase; equal digest does not rescue it. |
| Wrong argument vector | WRONG_ENTRYPOINT; observed unsupported parameters remain null/invalid. |
| Multiple matching or any extra receiving calls | INVOCATION_COUNT; retain all actual counts/order, never choose one. |
| Ambiguous call/attempt pairing or entry before release | OBSERVATION_MISSING / OBSERVER_NOT_ARMED per supported predicates; no timestamp-only association. |
| Observer detaches/crashes/channel fails | Close gate; prevent further target progress/terminate under controller custody; incomplete attempt ABORTED. No last-known-good positive. |
| Incomplete/torn evidence or failed persistence | No ACCEPT; preserve raw records and recover ABORTED. Complete invalid retained records select RECORD_INVALID under existing recovery rules. |
| Prohibited source reopen/redirection or execution attempt | Existing PATHNAME_REOPEN/SOURCE_REDIRECTION/EXECUTION_PROHIBITED; execution invalidates whole circuit. |

Use the existing rank precedence and one primary code plus supported diagnostics,
not a new competing enum. Missing observation never becomes positive receipt or a
fabricated zero count. A complete normal refusal and interrupted recovery are distinct.

Observer loss must not leave a releasable child: the controller owns the gate and
retains process custody, with a qualified tracer-death/child-termination arrangement
(e.g. verified ptrace exit-kill support plus controller death handling). Do not assume
GDB automatically supplies this. Its reviewed implementation/admission must demonstrate
the chosen behavior before any attempt; otherwise refuse arming. Once the receiving
stop is reached, no ordinary resume/detach is permitted in the positive path.

## 9. One future experiment skeleton, not implemented or run

A separate authorization would first permit producing and reviewing the additive
controller/decoder/bootstrap/guard artifacts, freezing their hashes and expected E,
and performing the bounded mechanism admission checks in the actual intended context.
This document specifies an architecture; it does not invent future artifact hashes
or assert installed, qualified implementation exists. No package/tool install or
policy relaxation is implicit. Before any positive dispatch those implementation
obligations must have passed, including A-to-B return tracking and observer-death behavior.

The single experiment shape is:

`fresh inert protected A -> witnessed retained B -> READY/image/callable/observer checks
-> persisted ATTEMPTED -> one-use release -> actual native CALL -> builtin_compile
hardware stop -> direct argument/A measurement -> clean observer-stop -> durable evidence`.

**Qualified observer-stop:** at the first receiver instruction, keep the sole thread
stopped; finish exact measurement and final A/seal/association checks. Synchronize the
captured evidence. Deliberately terminate the still-stopped child under supervisor
control without resuming receiver instructions or running Python shutdown/finalizers;
wait for confirmed child termination while retaining supervisor A capability and
observation state. Record `completion.outcome=observer_stop`, then complete `end` and
witness/terminal persistence. Any unplanned exit, lost stop or ambiguous termination
is incomplete/ABORTED, never this completion. Killing an unobserved process is not
receipt. The completed native CALL has already transferred the actual vector to the
receiving PC; no parser instruction or returned code object is needed for this claim.

No returned code exists on this selected positive path. Non-execution coverage includes
the reviewed bootstrap and observer syscall/control guards before the stop, denial of
payload reopen/import/evaluation paths, and no resume after receipt. It is bounded
candidate/result coverage, not prohibition of the separately authorized bootstrap's
own startup machinery. An execution attempt at any covered stage invalidates the run.
The fuller specification's refusal/recovery coverage is not waived by this one skeleton;
a future implementation authorization must fix its artifact and test allowlist explicitly.

## 10. Preservation receipt and limitations of verification

Static tools used: Git, file/readlink, readelf, objdump, nm, sha256sum, dpkg-query,
text/header/document reads, and read-only official web references. No debugger,
perf/BPF observer, Python process, C build, runtime harness or acceptance test was run.
No tracefs writes, ptrace requests, hardware breakpoint programming, target memory
reads, package manager mutation, interpreter changes or dependency-lock work occurred
in this action record. Shell/Git administrative process execution is not an invocation
of Python's compile/eval/exec/import boundary. These claims describe this agent's
actions, not an omniscient audit of unrelated host processes.

Before authoring, all **217** pre-existing tracked files were SHA-256 inventoried.
The precommit comparison verified all of them unchanged, including H2A1, both completed
H2A2 slices and their code/tests/fixtures/evidence, engine-provenance receipt and E0
HOLD artifacts. The only repository addition is this design document. Before/after
state manifests also cover executable/shared image, GDB, actual perf/bpftool binaries
and dispatchers, strace/binutils/hash tools, ABI headers, loader, installed Makefile/
static archive, dpkg status and relevant package-info files. These are preservation
checks, not dependency_runtime_lock. No system-wide package-transaction audit is claimed.

The dpkg status SHA-256 at initial measurement was
`14fae6bad31fee302b658fde2c54b99e67d79f0d54d70ac7c1d1743ff32e5a7d`, different from
that historical receipt's package-database snapshot. The exact candidate executable,
package version and provenance-receipt bytes match; no inference of global package
stasis since the preceding session is made. Engine provenance remains scoped
ENGINE_PROVENANCE_QUALIFIED.

**Precommit preservation exception: commit and push withheld.** During this circuit,
`/var/lib/dpkg/status` changed to SHA-256
`86367f035b74dc688d139611d6f56a758c51f947760a9f9b8b9021c61098becb`.
The read-only `/var/log/dpkg.log` inspection records concurrent package activity:
brave-origin 1.96.59 -> 1.96.60 and configuration/triggers involving initramfs-tools,
linux-image-7.0.0-34-generic, desktop-file-utils, gnome-menus, man-db and mailcap.
The latest status-old comparison corroborates browser/desktop trigger transitions;
status-old does not equal our initial baseline, so it is not a complete reconstruction
of every intervening change. No installer/update command was issued by this agent.
The initiating actor of that other activity is not established here.

All 217 existing tracked-file checks pass. Of 103 selected interpreter/tool/header/
package-state manifest entries, 102 pass; only the global dpkg status file fails.
The measured interpreter, observer/static tools, loader, selected headers and relevant
package-info bytes remain unchanged. This supports narrow artifact preservation,
**not** the requested unqualified statement that package state was unchanged.
Do not reset the baseline after the fact, hide the failed check, reverse another
actor's updates, or silently weaken the user's precommit condition.

Only the requested new document is present in repository status; the index remains
unchanged. Whitespace and document-scope checks are performed, but no staging,
commit or push occurs because the explicit package-state precondition failed.
No runtime tests are appropriate to this authorized document-only circuit.
The design verdict concerns the measured exact image and is separate from this
administrative publication blocker. HEAD remains HEAD before. The document digest
is reported outside its own bytes to avoid self-reference.

## 11. Read-only package-state reconciliation, 2026-09-30

**Reconciliation verdict: A — unrelated administrative package activity; the
prospective design evidence remains intact.** The preceding withholding receipt
is preserved as the historical outcome of the design circuit. This follow-up uses
the user's explicit conditional publication authorization; it changes no observer
analysis, architecture, ABI, qualification requirement or design verdict.

APT history identifies one transaction at 18:03:30–18:05:28: an upgrade of
`brave-origin:amd64` from 1.96.59 to 1.96.60. Dpkg corroborates that upgrade and
configuration/trigger processing of desktop-file-utils, gnome-menus, man-db, mailcap,
initramfs-tools 0.142ubuntu25.8 and linux-image-7.0.0-34-generic
7.0.0-34.34~24.04.1. APT terminal output records failed initramfs generation for
7.0.0-31 and 7.0.0-34 because of insufficient space; the transaction ended with
dpkg error 1. Initramfs-tools and the 7.0.0-34 image remain half-configured.
No repair is attempted. The running kernel still reports `7.0.0-31-generic`, the
version inspected by the design. The initiating actor remains unidentified.

The complete available dpkg interval from 18:01 onward contains no transaction
affecting python3.12-minimal, python3.12, libpython3.12 packages, libc/loader, GDB,
binutils or their relevant debugger dependencies. Installed CPython packages remain
3.12.3-1ubuntu0.17; GDB remains 15.1-1ubuntu1~24.04.1 (binary version string 15.1),
binutils 2.42-4ubuntu2.10, and libc6/libc-bin 2.39-0ubuntu8.9. Relevant GDB and
binutils ELF dependency metadata was inspected read-only; no package in that
dependency set appears in the concurrent transaction. No full dependency lock is
inferred from this bounded reconciliation.

The retained 103-entry state manifest again passes for every entry except the
previously disclosed global dpkg status hash. All recorded executable/shared image,
GDB, loader, static tools, headers, package-info files and actual perf/bpftool image
pins match. In particular, executable SHA-256 remains
`e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f`, GDB remains
`3832cc070ae1716e322105d3b39fb398695e5f031c9d39224cf227a8c2b889f6`, and loader
remains `c20a2dc8917c755f02b94049356320fe1f62ac7d9f8994731f807d9df39302da`.
Current dpkg status still equals the disclosed post-transaction hash `86367f03…becb`.
The logs plus preserved artifact measurements reconstruct the exception sufficiently
for A; neither engine nor observer requalification is required by this transaction.

All 217 pre-existing tracked files remain unchanged, including completed H2A2 slices
and the engine-provenance receipt. Only this document receives the factual disclosure
and updated next-action record. No observer attachment, Python invocation,
compile/eval/exec/import, candidate execution, package mutation, runtime-lock or E0
action occurs. Only this document is authorized for commit/push; resulting Git
identities are reported outside its bytes. E0 remains HOLD.

## Closing record

- native boundary: actual builtin_compile first instruction, pinned executable VA 0x69bff0/file 0x29bff0, before source conversion; unchanged.
- required observations: correct process/image/native entry/callable/invocation, original PyObject/type/length/direct bytes/independent SHA-256, full arguments, retained B/sealed A, committed attempt, persisted-before-entry ordering, continuous no-substitution association and complete coverage.
- candidate mechanisms: GDB hardware/software, direct ptrace, perf/eBPF uprobes, native instrumentation/debugger APIs, existing hooks/core/branch trace; compared without numeric scoring.
- selected observer: external GDB/MI raw-memory observer plus independent supervisor; paired hardware dispatcher/receiver stops and observer-stop completion.
- ABI/argument decoding: System V AMD64 RDI=self, RSI=args, RDX=6, RCX=one-key tuple; args[0..6]; exact CPython 3.12 layouts; caller R12=C; no inferior evaluation.
- live engine association: authenticated hash -> actual child executable/mapped image and code -> method/callable/paired addresses -> actual entry/source -> supervisor-owned committed attempt; rechecked under stops.
- byte measurement rule: read actual args[0] exact PyBytes, measured length and complete payload directly; hash observer capture, compare independent retained A read and frozen expected bytes; pointer identity with retained B required.
- attempt-binding rule: one fresh child/ID, rooted B/C/ID/E, private one-use gate released only after independently witnessed synchronized ATTEMPTED; paired native call and exclusive coverage; no payload nonce.
- observer independence: measurement/hash/evidence outside consumer and interpreter; bounded bootstrap trust explicit; no hostile-host/kernel independence claimed.
- fail-closed conditions: absent/wrong attachment/image/address, unarmed/missing/extra/ambiguous calls, unreadable/wrong objects, partial read/hash failure, substitution, observer loss, incomplete evidence or prohibited operation; never promote absence.
- residual assumptions: honest host/kernel/debug hardware/storage and pinned tools/decoder; reviewed bootstrap and custody; no hostile native writer; archive trust as already scoped; operational tracing/hardware behavior must pass future admission, not presumed.
- observer verdict: OBSERVER_QUALIFIED for this prospective design/evidence contract only; no live observer or native receipt is qualified by this document alone.
- future real-boundary readiness: architecture specified for a separately authorized implementation/admission/experiment; no run authorization, no observed receipt, no complete E or live acceptance yet.
- external_trust_root status: UNRESOLVED.
- dependency_runtime_lock status: UNRESOLVED, not begun.
- H2A1 status: VERIFIED + frozen, unchanged.
- H2A2 status: sealed-handoff slice VERIFIED; surrogate consumption VERIFIED WITH RESIDUAL ASSUMPTION; completed slices frozen unchanged; real native receipt not yet observed.
- E0 status: HOLD.
- one next bounded action only: separately authorize one document-only implementation-and-qualification specification fixing the selected observer/controller/bootstrap/guard artifact allowlist and admission checks; no attachment or compile invocation. Not performed here.
