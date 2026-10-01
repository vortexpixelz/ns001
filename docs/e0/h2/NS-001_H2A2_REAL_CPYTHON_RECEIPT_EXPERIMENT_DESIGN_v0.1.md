# NS-001 H2A2 real CPython receipt experiment design v0.1

Date: 2026-09-30 (America/New_York). HEAD before:
`9923e8203e347495b5f2970cecc7480efdd1c8c9`.
Branch: `codex/e0-h2-preparation`; initial working tree clean.

## Scope, decision and controlling evidence

One document-only design circuit. **Implementation readiness: PARTIAL.** Exactly
one concrete design question, Q1 in section 14, remains: the pinned GDB's precise
hardware-only initialization policy, including prevention of its internal software
breakpoints. The experiment's semantics below are fixed; Q1 blocks implementation
readiness and admission, rather than becoming an implementer's silent fallback.

This is a future offline, inert, single-attempt receipt experiment. Its receiving
boundary is the first instruction of the qualified CPython `builtin_compile`, before
argument conversion. Its successful path terminates the stopped child without
executing that instruction. No compiler return, parser progress or code object is
required. A caller stop alone is insufficient.

No observer, Python process, compiler, evaluator, source executor, import machinery,
test harness, build, installation, scientific/client path or E0 run is authorized or
performed by this circuit. Nothing is implemented. Read-only static image/header/
package inspection and official documentation research support this design; the
future experiment itself must use retained offline inputs. Git publication is the
explicitly requested administrative action. `dependency_runtime_lock` is not begun.

The following documents remain controlling and byte-for-byte unchanged:

| Document in this directory | SHA-256 |
| --- | --- |
| `NS-001_H2A2_REAL_CPYTHON_INPUT_BOUNDARY_SPEC_v0.1.md` | `eae004d95046d2c2a83fd7813f4b0485ce792e358403a406859280f4c0fdc564` |
| `NS-001_H2A2_REAL_CPYTHON_ENGINE_PROVENANCE_REVIEW_v0.1.md` | `3fd49cf843b582ddffed971281e226c2d1f419462c17150ca48e82a3b649453e` |
| `NS-001_H2A2_REAL_CPYTHON_NATIVE_OBSERVER_DESIGN_v0.1.md` | `cdca62d5f02a468353d4c0ba9113e3d4ced047f4b78f68c949b1141bbad1b075` |

The engine remains `ENGINE_PROVENANCE_QUALIFIED`; the selected external GDB/MI
architecture remains prospectively `OBSERVER_QUALIFIED`. Neither verdict says an
implemented observer has passed live admission. This document does not revise that
prior architecture verdict, set `observer.qualified=true`, or invent a completed E.
Prior H2A1 and H2A2 evidence belongs to its original slices, not this future attempt.

## 1. Exact experiment object

| Item | Fixed value |
| --- | --- |
| Profile | `ns001.h2a2.real-cpython-input-receipt.v1` |
| Source | Hex `23 0a`; ASCII `#` followed by LF, conventionally `#\n` |
| Length | 2 bytes, with no BOM, terminator or extra newline in the source |
| SHA-256 | `32c4858e22cc2c967b42150fa550562a2c839c2cebcaab91cabdf6f4da020022` |
| Source argument | Exact builtin `bytes` object B; no subclass or conversion |
| Filename | Exact `str` `<ns001-h2a2-real-input-v1>`; never opened |
| Mode | Exact `str` `exec`; grammar selection only |
| flags | Exact `int` 0 |
| dont_inherit | Exact `bool` True |
| optimize | Exact `int` 0 |
| _feature_version | Explicit exact `int` -1, sole keyword |
| Shape | Six positional arguments, one keyword; no defaults or star expansion |

The digest was independently recomputed here by hashing the literal two-byte data
with `sha256sum`; that is fixture verification, not evidence of native receipt.
There is no scientific source. The old surrogate's `abc` fixture stays unchanged.

The future controller reserves X before acquisition, creates one fresh memfd A,
writes exactly the fixture once, validates length and bytes against E, then applies
exactly `F_SEAL_WRITE|F_SEAL_GROW|F_SEAL_SHRINK|F_SEAL_SEAL` (mask 15). Require a
regular memfd, size 2, no writable mapping, and successful sealing. Short/error writes
refuse without repair. Controller retains its original capability until terminal
completion. The child receives an inherited descriptor for that same open object;
the pinned launcher closes all unrelated descriptors, preserves this one and the
private control channel, and records the inheritance chain. Child FD number,
pathname, inode or digest alone does not establish object identity. No payload FD
reopen through `/proc`, path alias or fallback is permitted.

B is the final exact `bytes` object returned by one child `os.pread(A,3,0)`, whose
actual syscall returns 2. The read is positioned, bounded, and never retried, even
on EINTR. Controller and observer check A association, size and seals before and
after derivation. Keep B, real builtin C and builtins module M strongly rooted through
termination. No additional delivery copy, decoding, normalization or replacement of
B is allowed. Observer-owned measurement copies do not become delivery objects.

## 2. Engine and observer admission

All checks are mandatory before the one-use compiler-dispatch gate opens. A failure
means STOP with a retained refusal/abort, not requalification, package repair, another
interpreter, another observer, or permission changes. Current static reads reproduce
the executable/GDB hashes, relevant installed package versions, ELF type and caller
disassembly; historical archive/build authentication remains the preserved provenance
receipt's evidence, not a newly downloaded/reverified archive in this circuit.

| Admission item | Exact requirement |
| --- | --- |
| Executable | `/usr/bin/python3.12`, regular expected executable; retain an open reference handle |
| Whole executable SHA-256 | `e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f` |
| Package | `python3.12-minimal:amd64`, `3.12.3-1ubuntu0.17`, installed; source `python3.12`, same version |
| Relevant package drift | `python3.12`, `libpython3.12-stdlib:amd64`, `libpython3.12t64:amd64` also `3.12.3-1ubuntu0.17`; compare recorded package fields, executable bytes and retained relevant metadata; any mismatch stops |
| Build corroboration | CPython 3.12.3; size 8,020,928; ELF build ID `337d65cf00021797985cc9f77c0cc334a9fbeb38`; build ID is not the byte pin |
| Architecture | ELF64 little-endian x86-64 System V LP64, 8-byte pointers/Py_ssize_t; ET_EXEC, non-Py_TRACE_REFS/non-debug layout |
| Compiler-bearing image | The executable itself; no libpython receiver; DT_NEEDED libm, libz, libexpat, libc |
| Receiver | `builtin_compile` first instruction VA `0x69bff0`, file offset `0x29bff0`; bytes `f3 0f 1e fa` |
| Caller | FASTCALL-with-keywords dispatcher `0x581f90`; CALL at `0x581feb` (`ff d0`), return PC `0x581fed` |
| Method definition | VA `0xa49ae0`, native target `0x69bff0`, flags `0x82` |
| GDB | `/usr/bin/gdb`, package `gdb:amd64` `15.1-1ubuntu1~24.04.1`; SHA-256 `3832cc070ae1716e322105d3b39fb398695e5f031c9d39224cf227a8c2b889f6` |
| Other experiment tools | Reviewed hashes/origin dossier for controller, native launchers, bootstrap, MI parser, raw decoder, hash tool, guard policy and qualification record; freeze before registration, never blank pins |
| Operational admission | Correct child/thread custody, allowed tracing, effective hardware stops, complete raw reads, successful death-chain admission, Q1 closed, durable writer and guards working |

Compare relevant package records, not the whole mutable dpkg status file as though
an unrelated package update changed the engine. Relevant drift after qualification
still refuses even if an executable version string looks plausible. A current
package label alone is not continuing authenticity; bind executable bytes to the
qualified digest and retain the provenance descriptor under its hash.

At the post-exec stop, READY, and both native stops, bind the actual child via its
retained pidfd, creation/parent relationship, MI inferior identity, sole TID and
`/proc/<pid>/exe` open handle. Hash the latter whole file and compare to the pin.
Record maps device/inode/file-offset associations to the retained reference handle.
For a mapping starting at S with file offset O, file byte F is at `S+(F-O)` when
within range; independently match ELF PT_LOAD segments and derive one consistent
load bias. This ET_EXEC requires bias zero. Still measure it: stack, heap and
libraries are randomized; an unexpected PIE/nonzero compiler bias refuses.

Independently read actual executable PT_LOAD code bytes and compare with the pinned
file, including caller, receiver and derivation wrapper. Code segment file range
is `0x020000` through `0x302fbc` inclusive, VA `0x420000` through `0x702fbc`.
Reject private text modification, software breakpoint patches, unexplained relocations,
writable executable pages, deleted/replaced backing image or mapping discontinuity.
Check mutable method/type data semantically, not against unrelocated file data.

Measure `/lib64/ld-linux-x86-64.so.2` and native maps relevant to dispatch/observation
against the retained observer qualification descriptor. Record an explicit environment
with no LD_PRELOAD, LD_AUDIT, alternate library or Python source-selection variables;
reject unexpected interposition. Freeze those narrow reference measurements offline
before attempts; missing reference material stops. This is receiver/observer association,
not a transitive runtime lock or authenticated origin claim for every mapped library.

## 3. Durable attempt lifecycle

Reuse the real input specification's exact schemas and the frozen store's durability
semantics in a later additive implementation; do not modify/reuse the surrogate store,
namespace, `abc` implementation or old live capabilities.

| Phase | Meaning and permitted transition |
| --- | --- |
| Reserved/registered | Exclusive retained namespace and monotonically reserved ordinal form X=`namespace:ordinal`; retain E, raw request and registration under exclusive custody before preparation |
| PREPARED | Acquisition/derivation, READY, engine/callable/observer/guard checks passed; append canonical sequence 0, `entered=false` |
| ATTEMPTED | Append and synchronize sequence 1, `entered=null`; binds predecessor and X; controller independently reads back exact bytes and digest, and witnesses successful file and directory fsync before gate release |
| OBSERVED | Logical phase only: complete raw native observation retained; **no new journal state/schema**; persist independent witness before terminal event |
| ACCEPTED / REFUSED | Normal terminal event with witness hash, actual entered status, unique primary code or null and ranked diagnostics; no subsequent operation |
| ABORTED | Separate terminal recovery record for interruption/incomplete/invalid retained attempt; originals retained, no resumed dispatch or promotion |

The controller owns the durable writer and dispatch capability. Read-back alone is
not evidence of persistence; a failed/unknown synchronization blocks release. Store
metadata loss, stale writer, conflicting custody or reused X stops. Empty retained
stores are not silently reinitialized. A precondition REFUSED may follow registration
or PREPARED without inventing ATTEMPTED or an entry. Terminal records are immutable.

The one-shot channel is bound internally to `(X, E_sha256, ATTEMPTED_event_sha256)`.
The child cannot assign an ID to a stop, mint a receipt, or obtain another token.
Observer failure/interruption can never produce ACCEPTED, even with plausible bytes.

## 4. Future GDB/MI supervisor and launch control

This is a command/control specification, not a runnable script. Q1 is an explicit
unfilled initialization prerequisite; the rest is a fixed sequence. Do not execute
any of it under this document's authority.

**Process model.** Controller launches GDB as its direct child using a pinned native
launcher that sets `PR_SET_PDEATHSIG=SIGKILL`, checks the expected parent before and
after setting it, and replaces itself with the pinned GDB. GDB launches a second
pinned native launcher as its direct inferior (`startup-with-shell off`). That launcher
sets and checks the same death signal against GDB, preserves only the inherited A
and control descriptors, disables core dumps, then replaces itself with the exact
CPython executable, same PID, ordinary credentials, no intervening shell or fork.
Here process image replacement means the OS operation, not Python's `exec` builtin.

The kernel's parent-death setting survives ordinary exec but has credential-change
exceptions; parent-thread lifetime also matters. The future launch qualification
must verify those exact parent/credential/thread conditions, reject preexisting
parent death, and demonstrate GDB-loss and controller-loss killing with non-Python
inert launcher controls before accepting this arrangement. No assumption that GDB
automatically sets ptrace EXITKILL is made. Retain pidfds for GDB and the inferior;
controller termination uses pidfd SIGKILL, not a potentially reused numeric PID.
GDB hang/MI timeout closes the gate and kills; controller failure kills GDB and in
turn the inferior. No shutdown/finalizer continuation is part of a terminal path.
These semantics follow [Linux PR_SET_PDEATHSIG](https://man7.org/linux/man-pages/man2/PR_SET_PDEATHSIG.2const.html);
the arrangement itself has not been tested here.

**MI configuration and permitted commands.** GDB starts with `--nx --nh --interpreter=mi2`,
startup automation/auto-loading, pretty-printers, Python scripts, debuginfod/network
and arbitrary command hooks disabled before loading a file. Freeze locale and exact
environment. Use all-stop mode, numeric addresses, monotonically assigned MI command
tokens, one outstanding command at a time, and a bounded parser that preserves all
async records. Inferior stdout/stderr use separate channels and cannot inject MI.
`-file-exec-and-symbols` identifies the native launcher initially; a qualified exec
catchpoint associates image replacement with CPython before bootstrap progress.
No `run --start`, `next`, `finish`, inferior calls, expression evaluation, Python
reflection, memory/register writes, target-side condition, ignore count, detach,
automatic retry or debugger restart is permitted. Restricted CLI commands through
`-interpreter-exec console` are only the frozen settings, catchpoint setup and
maintenance inspection in the reviewed policy. Q1 must supply its missing exact
initialization commands; a settings error stops, never triggers a fallback.

Future sequence:

1. Freeze E/qualification, reserve/register X, acquire/seal A and launch the custody
   chain. Catch the inferior's OS exec into CPython. Validate its image/ABI before
   continuing. Install lifetime receiver monitoring before Python bootstrap runs.
   Startup/bootstrap compile calls, if any, are recorded in a separate setup epoch
   with no X dispatch linkage; their bounded continuation belongs only to a separately
   reviewed fixed bootstrap, never the inert candidate. No hidden startup call can
   count as X's receipt. Unexpected setup calls refuse. Freeze the expected setup
   control path/counts in qualification, not by learning from an acceptance run.
2. Run only the reviewed setup/bootstrap, with no scientific/client modules. Complete
   setup imports and callable/root establishment before the exclusive derivation/
   attempt interval. Establish the one A-to-B derivation in section 5. Reach READY
   blocked on the private controller channel; interrupt into an all-stop snapshot
   while the gate remains closed. Verify only one thread and no children.
3. Decode M/C/B and the root tuple from raw memory; verify ordinary `compile` binding.
   Revalidate maps, code, A, complete derivation and observer identity. Arm the two
   compile sites using `-break-insert -h *ADDRESS` (ADDRESS resolved as in section 2),
   no pending/multiple location, no auto-continue. Retire derivation-only sites.
4. Verify actual effective insertion under the qualified GDB backend policy, successful
   kernel programming and same-thread stop behavior. `-break-list`, GDB's requested
   state, and maintenance debug-register **mirrors** are supporting data only. The
   earlier launcher admission must exercise both hardware slots, complete reads and
   failure refusal without Python/source compilation. When a bounded pre-release
   resume is needed to program hardware, the child remains blocked at the closed
   channel; stop it again and verify insertion before proceeding. Hardware-slot/
   permission failure stops. No software replacement or policy elevation.
5. Persist PREPARED then ATTEMPTED as in section 3. Synchronize forensic admission
   evidence and independently validate the journal chain. Send exactly one complete
   framed token on the private channel; partial/duplicate token closes the channel
   and aborts. Only then issue the permitted `-exec-continue` to let the blocked child
   complete its fixed path to the sole call. Deadline: 30 seconds of controller
   monotonic time for a required control/stop event; timeout is failure, never evidence
   that no entry occurred. Retain timing only in forensic records.
6. At caller stop 1, read raw registers and memory using register-number mapping from
   `-data-list-register-names`, `-data-list-register-values x`, and numeric
   `-data-read-memory-bytes ADDRESS COUNT`. Require C in R12, target in RAX, full
   measured vector/roots/maps and same X. Supporting dispatcher hits by known setup/
   barrier operations are classified and retained under the frozen bootstrap trace;
   none counts as receipt. Unexpected relevant calls or a second selected C refuse.
7. Leave receiver stop armed; issue exactly one `-exec-step-instruction` at the native
   CALL. Require the very next stopped snapshot to satisfy section 7, before any
   receiver instruction. Freeze the pinned backend's hardware/single-step trap
   classification during operational qualification; a bare `end-stepping-range` or
   matching PC without qualified native-stop provenance is insufficient. Do not
   resume again to turn an ambiguous step into a later plausible receipt.
8. Capture entry data, direct B bytes and independent A read; persist it while the
   child stays stopped. Verify final A/roots/maps/counters, then SIGKILL the stopped
   child via its retained pidfd. Confirm death with pidfd state plus debugger exit
   event under custody. No normal resume/detach. Close observer session after complete
   transcript drain; material teardown failure means ABORTED. Persist witness and
   terminal evidence in section 10's order.

The documented [MI hardware-breakpoint command](https://sourceware.org/gdb/current/onlinedocs/gdb.html/GDB_002fMI-Breakpoint-Commands.html),
[single-instruction step](https://sourceware.org/gdb/current/onlinedocs/gdb.html/GDB_002fMI-Program-Execution.html),
and [raw register/memory commands](https://sourceware.org/gdb/current/onlinedocs/gdb.html/GDB_002fMI-Data-Manipulation.html)
support this command vocabulary. They do not demonstrate local runtime behavior.

## 5. Independent A-to-B derivation, including resize

Static inspection in this circuit locates the exact `pread` method-table entry at
file offset `0x6602e0`, VA `0xa612e0`: name VA `0x7125dc` (`pread`), wrapper VA
`0x4f6102`, flags `0x80` (METH_FASTCALL), doc VA `0x92d260`. These are measurements
of the same hash-pinned executable, not names inferred from objdump's nearest exported
symbol label. The wrapper's disassembly supplies this bounded path:

| Location | Observation required in the future |
| --- | --- |
| `0x4f6102` | Exact real pread wrapper entry, three exact-int arguments FD(A), 3, 0; capture incoming stack/return PC and wrapper identity |
| `0x4f621f` | Native call to `pread64@plt`; buffer is `*(RBP-0x38)+32`, count RBX=3, FD R13D, offset R14=0 |
| pread64 syscall entry/exit | x86-64 syscall 17; FD in RDI, buffer RSI, count RDX=3, offset R10=0; exactly one entry/return with signed RAX=2; retain returned two bytes directly |
| `0x4f6224` | Native pread return; RAX=2 before subsequent handling; no error/retry branch allowed |
| `0x4f626f` | Call `_PyBytes_Resize(&buffer,2)` because requested 3 differs from returned 2 |
| `0x4f6274` | Post-resize load of final buffer; stack slot `RBP-0x38` is authoritative for final object pointer, not original syscall buffer |
| `0x4f6299` | Wrapper RET, RAX is final B; stack return PC must match wrapper entry; decode B here and preserve association into READY roots |

Use one temporary derivation hardware slot sequentially for wrapper entry, pread
return, post-resize and wrapper RET, plus an entry/return syscall catchpoint. The
receiver monitor remains active; the caller compile slot is not needed yet. At the
wrapper entry install the next temporary address while stopped; at each reached
point validate the frame and set the next address before resuming. Syscall entry and
exit additionally establish FD/offset/count/result and captured bytes. Any negative
syscall result, second syscall, signal, unsupported branch or null final B terminates
before the wrapper can retry. The post-resize pointer and final RAX must agree; any
move is recorded, not mistaken for substitution. After RET, retain the same B through
the fixed immediate root-store path; READY and both compile stops must reference it.
No Python digest or success flag can fill a missing native link.

These temporary stops are necessary because syscall buffer identity is not final
PyBytes identity when a resize occurs. They prove derivation, not receipt; they are
retired before paired compile observation. No third compile boundary or return stop
is introduced. The [CPython 3.12.3 pread implementation](https://raw.githubusercontent.com/python/cpython/v3.12.3/Modules/posixmodule.c)
corroborates the resize/error paths; the installed-image coordinates above control.

## 6. Actual ABI and argument decoding

At the first `builtin_compile` instruction the registers are:

| Register/range | Required independent measurement |
| --- | --- |
| RDI | self M, actual builtins module; **not** callable C |
| RSI | Native `PyObject *const *args`, not a Python tuple |
| RDX | Signed `nargs`=6; vectorcall high offset bit already cleared by dispatcher |
| RCX | Exact tuple kwnames, size 1, exact str `_feature_version` |
| `RSI + 8*i`, i=0..6 | Seven actual object pointers: six positional values, then the keyword value |
| RSP | Actual return address `0x581fed` plus measured bias |
| R12 | Preserved callable C from stop 1; corroboration of paired association |

At dispatcher **initial** entry RDX is nargsf, but instruction `0x581f95` clears
bit 63. Do not apply that initial vectorcall convention at either selected stop.
Native vector, tuple, PyBytes, Unicode, PyLong, bool, builtin/module and dictionary
decoding are all required; four register names alone are not sufficient evidence.

Use exact image-relative type pointers: PyBytes `0xa2bee0`, PyTuple `0xa42c40`,
PyUnicode `0xa472c0`, PyLong `0xa3bf20`, PyBool `0xa2a3a0`, True `0xa2a360`,
PyCFunction `0xa3fb20`, PyModule `0xa3ff00`, PyDict `0xa3d840`. Measure bias first.

| Native object | External raw decoder rule |
| --- | --- |
| Header | ob_type +8 equals the exact mapped type; no name/subtype/duck-typing substitute |
| bytes | signed size +16, cached hash +24 ignored, payload +32; read measured length, separately check trailing NUL |
| tuple | signed size +16, item pointers +24; require kwnames size 1 before reading it |
| str | signed length +16, state uint32 +32: kind bits 2..4, compact bit 5, ASCII bit 6; compact ASCII data +40, compact non-ASCII data +56, noncompact canonical pointer +56; decode 1/2/4-byte little-endian units externally and compare exact text |
| int | CPython 3.12 lv_tag +16, uint32 base-2^30 digits +24; size=tag>>3, sign code=tag&3 (0 positive, 1 zero, 2 negative; 3 invalid); validate normalized size/digits, permit only defined flag bit 2; zero size/sign=0/1, -1 size/sign/digit=1/2/1 |
| bool | exact PyBool type and True singleton pointer, consistent value; refuse bool for flags/optimize/feature-version |
| C | exact PyCFunction; m_ml +16, m_self +24, vectorcall +48; definition `0xa49ae0`, self M, target entry, flags 0x82 and vectorcall `0x581f90` |
| M | exact PyModule, md_dict +16 exact dict; independently inspect actual `compile` and control-root bindings |

The bootstrap's only locator/control root is M's
`_ns001_observer_roots_v1=(B,C,X,E_sha256)`. Decode it at READY and both stops,
require exact tuple size 4 and exact ASCII strings for X/E, and require ordinary
`compile` binding equals C. Independently establish M from qualified bootstrap/
builtin self association; a harness-provided address is only a locator hint.

Raw dict decoding follows the preserved observer layout: ma_used +16, version +24,
ma_keys +32, ma_values +40; keys log2_size +8, log2_index_bytes +9, kind +10,
nentries +24, indices +32; entries start `keys+32+2^log2_index_bytes`.
General entries are 24 bytes (hash/key/value), Unicode entries 16 (key/value).
Split values use ma_values[i]; combined values come from entries. Validate kind,
index width/capacity/ranges, used counts and unique decoded keys; skip deleted entries.
Freeze maxima: 4096 slots/entries, 65536 index bytes, 4096 code units per control
string, seven argument pointers, four root pointers, one keyword. Check arithmetic,
readable mapped ranges and exact full-length MI results before each read. Do not
allocate from unbounded target sizes. Unsupported/malformed layout refuses.

At each stop re-read required headers/roots/version after capture; require stability
under the sole-thread stopped snapshot. Extract **observed** arguments before comparing
to section 1. Preserve actual invalid values when representable; unavailable values
remain null, never replaced with defaults. No inferior lookup, repr, hashing, Unicode
conversion or arbitrary object callback is invoked.

## 7. Paired hardware stops

Both are required by this contract; eliminating either weakens the specified claim.

| Stop | Proves | Does not prove |
| --- | --- | --- |
| 1: `0x581feb`, immediately before native `call *%rax` | Actual selected C in R12, m_ml/self/vectorcall/binding, target RAX, measured full argument vector and roots, armed receiver, active X after durable release | That control reached the receiver |
| 2: `0x69bff0`, before first receiver instruction | Actual native receiving entry with original arguments, same child/TID, measured B/A/parameters | Alone, which retained callable supplied that invocation or durable dispatch causality |

Require strict stop 1 → single native CALL → stop 2; same PID identity/TID, unchanged
RDI/RSI/RDX/RCX and vector pointers, unchanged B/C/M roots, RSP decreased by exactly
8, stack return `0x581fed`, entry PC exact and no intervening unrelated event.
Retain both complete snapshots, command token/results and trap provenance. Only stop
2 creates `entry.native_entry=true`; it is counted once even if the backend reports
coincident stepping/hardware reasons. Ambiguous reason, lone stop, wrong ordering,
unmatched call, signal, changed roots or second entry fails closed. No parser/return
breakpoint is required. Derivation and launch control stops have distinct purposes.

The fact that [hardware breakpoints can stop before an instruction without patching it](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Set-Breaks.html)
does not by itself settle GDB's internal startup instrumentation; that is Q1.

## 8. Byte receipt rule and compilation boundary

At stop 2 set P to the **read** pointer args[0]. Require exact PyBytes type, P equal
to the independently tracked final B pointer, and actual signed length 2. Read exactly
two bytes directly from P+32 into an observer-owned buffer; retain full address-range
and read-count evidence. Read failures/gaps cannot be padded, supplied from the fixture,
or retried into ACCEPT. Negative lengths are invalid layout; measured nonnegative
length <2 or >2 gives the appropriate length refusal without an unbounded payload read.

Hash the captured two-byte buffer independently outside the inferior with the pinned
SHA-256 tool. Compare full bytes AND digest AND length to retained derivation/READY B
capture and E. Independently recheck the supervisor's retained A capability and issue
one `pread(A,3,0)` for the entry comparison, requiring result 2, exact seals/size and
same-object custody. Hash this separate capture and compare it byte-for-byte to P.
Expected digests, Python cached hashes, wrapper statements and compiler results are
never receipt evidence. Missing derivation, equal-byte different B, or different A
fails even if all digests happen to match.

Receipt is bound to X by registration/E, durable ATTEMPTED digest, controller-owned
channel release, roots, continuous process/observer custody and the ordered native
pair. Volatile time or an echoed token alone cannot make that association.

**Do not allow builtin_compile to return in this experiment.** After complete capture
and final checks, synchronize raw evidence and terminate while stopped at entry. A
qualified deliberate kill plus confirmed death is `completion.outcome=observer_stop`.
Unexpected death, partial evidence or loss of custody is not this completion. No
returned code object exists on the positive path. No eval/exec/import of candidate
or result, no E0, and no post-entry resume are allowed. Compilation success is neither
required nor observed. The separately reviewed bootstrap's own startup code is
accounted for as setup, not confused with executing the protected source.

## 9. Minimum bounded future case matrix

Each listed subcase runs once; P01 runs twice with fresh A/B and distinct X as required
by the prior specification. No fuzzing, adaptive cases, retries or wrong-engine launch.
Mode P is a real pre-dispatch refusal; mode R is a fault in retained genuine positive
observation/evidence replay; mode L is a bounded live interruption/no-dispatch control.
R cases prove validator behavior, not a live native substitution. Originals remain
untouched and every variant has its own case-labelled evidence. Replay covers the
actual-received-object/parameter predicates in addition to preparation checks.

| Case | Fixed mutation/control | Required disposition |
| --- | --- | --- |
| P01, twice | Exact positive flow, fresh X/A/B | ACCEPTED only on complete real observations |
| N01.1 P | Wrong requested executable path, without launching it | ENGINE_UNQUALIFIED |
| N01.2 P | One changed hex digit in executable comparator | ENGINE_UNQUALIFIED; never alter system executable |
| N07.1 R | Compiler map associated with wrong image handle/digest | ENGINE_UNQUALIFIED |
| N07.2 R | Receiver address shifted +1 | ENGINE_UNQUALIFIED |
| N02.1 P | Proposed retained callable differs from ordinary builtin binding; do not call it | WRONG_COMPILE_CALLABLE |
| N03.1 P | Equal-byte B with a different object identity | OBJECT_SUBSTITUTION |
| N03.2 P | Unrelated equal-byte A offered initially | WRONG_PROTECTED_OBJECT |
| N03.3 R | Later A/root/B identity changed in entry record | OBJECT_SUBSTITUTION |
| N04.1 P | Complete source `23` (length 1) | INPUT_TRUNCATED |
| N04.2 P | Complete source `23 0a 0a` (length 3) | INPUT_APPENDED |
| N04.3 P | Complete source `20 0a` (length 2) | INPUT_ALTERED |
| N04.4 P | str with text `#\n`, not bytes | INPUT_TYPE |
| N04.5 L | Inject one short/error derivation read before compiler dispatch | INPUT_IO; no internal EINTR retry |
| N05.1 through N05.8 P | In order, wrong filename, mode, flags, dont_inherit, optimize, feature version, positional count, keyword name/count | WRONG_ENTRYPOINT; no substituted compiler invocation |
| N05.9 R | Actual received filename differs although prepared filename matches | WRONG_ENTRYPOINT |
| N03.4 R | Actual source pointer differs although prepared B matches | OBJECT_SUBSTITUTION |
| N08.1 P | Observer identifies another PID than retained child | OBSERVER_UNQUALIFIED; never attach to unrelated PID |
| N08.2 P | Requested but ineffective/pending hardware site | OBSERVER_NOT_ARMED; no release |
| N08.3 L | Armed child never reaches compile; timeout control, no candidate call | Complete negative witness: OBSERVATION_MISSING; otherwise ABORTED |
| N08.4 R | Actual two-byte memory read delivers only first byte | OBSERVATION_MISSING; no repair/padding |
| N09.1 R | Duplicate genuine entry group, including identical bytes | INVOCATION_COUNT; never select one |
| N09.2 R | Entry without its paired caller, or reversed pair, each once | OBSERVATION_MISSING |
| N09.3 R | Cross-attempt ID/registration link substituted | RECORD_INVALID; ABORTED if found by recovery |
| N09.4 R | Well-shaped but wrong ATTEMPTED digest/causal link | OBSERVATION_MISSING |
| N10.1 L | Kill GDB after ATTEMPTED, including once after capture before completion | ABORTED; retained child death under custody, no ACCEPT |
| N10.2 L | Kill controller after ATTEMPTED | ABORTED on later recovery; death-chain controls must already pass |
| N10.3 L | Interrupt each of reservation, registration, PREPARED, ATTEMPTED, witness, terminal-journal and recovery writes, one fixed cut per stage | ABORTED for nonterminal/torn record; preserve a fully durable valid terminal unchanged |
| N06.1 P | Denied payload pathname reopen | PATHNAME_REOPEN; no file opened |
| N06.2 P | Proposed stdin/import/cache source channel | SOURCE_REDIRECTION; no import performed |
| N11.1 R | Denied reopen and later object substitution both evidenced | PATHNAME_REOPEN primary, OBJECT_SUBSTITUTION diagnostic |

For N05.1–8 use respectively `<wrong>`, `eval`, exact int 1, False, exact int -1,
exact int 0, positional count 5, keyword `_wrong_feature_version` (one keyword).
These are refused request data, not executed source/argument changes. N09.2's two
variants and N10.1's two cut points are fixed, not an open mutation family. For
N10.3 the fixed cut is halfway through that stage's record bytes before fsync;
for reservation use its reservation record. A recovery cut is recovered again only
under the existing idempotent/conflict rules, never by resuming the compiler attempt.
The bounded matrix is not general runtime security coverage.

## 10. Exact evidence package and durability order

Use the existing `ns001.h2a2.real-input.*.v1` schemas and key sets unchanged. No
new canonical state, raw PID field, transcript field or competing refusal enum is
inserted into them. Each new experimental store is separate from frozen stores.

| Retained artifact | Contents and linkage |
| --- | --- |
| `store.json`, custody/lock/reservation records | Original namespace/custodian, monotonic reservations and exclusive lifetime ownership |
| `expectation.json` | E: profile/spec digest, exact fixture/parameters, engine/interface/build/image identities, bootstrap/observer/qualification hashes and sealed-bytes-only policy |
| `qualification/` | Hash-addressed controlling documents, engine admission descriptor, narrow tool origin/identity records, resolved Q1 policy, bootstrap/launcher/controller/decoder/guard bytes and mechanism-admission evidence |
| `X/request.json`, `X/registration.json` | Original request bytes and exact X/E/request-digest association |
| `X/events.jsonl` | Ordered canonical PREPARED/ATTEMPTED/terminal event chain; no OBSERVED state |
| `X/witness.json` | Ordered semantic observations, exact measurements, parameters, dispatch link, counts, coverage and observer_stop completion |
| `X/observer/mi.commands`, `mi.stdout`, `mi.stderr` | Exact bytes in channel order, including errors/asynchronous notifications; no line filtering or overwrite |
| `X/observer/order.jsonl` | Supervisor read-event sequence, channel and byte offsets/counts, MI command tokens and relevant gate/fsync/signal/exit events; arrival order is not cross-channel wall-clock proof |
| `X/observer/admission.json`, `maps.before`, `maps.stop1`, `maps.stop2` | Actual executable/package/loader associations and narrow measured identities; maps retain necessary volatility |
| `X/observer/derivation.json`, `stop1.json`, `stop2.json`, `arguments.json` | Raw register snapshots, addressed memory read requests/results, type/layout decoding, derivation return/resize chain, independent full argument values and required associations |
| `X/observer/B.derived.bin`, `B.ready.bin`, `B.entry.bin`, `A.entry.bin` | Exact observed bytes only, each positive file length 2; captures and independent hashes, never constructed from E |
| `X/observer/completion.json` | Still-stopped capture completion, final A/roots/maps, termination request and actual death confirmation; no fabricated compiler return |
| `X/recovery.json` when needed | Original-byte/prefix hashes, absence markers and ABORTED result under existing recovery contract |
| `X/capture-manifest.json`, `X/package-manifest.json`, `X/package-manifest.sha256` | Separate supporting manifests, defined below; do not extend fixed witness schema |

Supporting JSON is ASCII-only canonical JSON with sorted unique keys, integer sizes,
no floats/BOM and one final LF. Define each manifest with exactly `schema`,
`attempt_id`, `expectation_sha256`, `entries`; schema literals are
`ns001.h2a2.real-receipt.capture-manifest.v1` and
`ns001.h2a2.real-receipt.package-manifest.v1`. Each path-sorted entry has exactly
`path` (store-root-relative ASCII path without traversal), `length` and `sha256`. Include every
actually retained raw fragment, not empty expected placeholders. Capture manifest
lists finalized observer/qualification evidence. Package manifest lists those files,
capture manifest, store/custody snapshots, E, request, registration, full journal,
witness or recovery and any partial files. No manifest lists itself; the external
sidecar is the SHA-256 of exact package-manifest bytes plus LF. No recursive hash.

Normal completion order is: capture/confirmed child death → drain and synchronize
observer files → write/fsync capture manifest and its directory → write/fsync witness
→ append/fsync terminal event and store directory → write/fsync package manifest and
sidecar/directory → independent completeness/hash verification. Store owns the final
terminal write; child/MI output cannot write it. The public experiment verdict is
ACCEPT only after this final package verification. A crash after a valid durable
ACCEPTED event but before final packaging leaves that event byte-identical and the
package **incomplete: no public ACCEPT**; it is not rewritten as ABORTED. Nonterminal
attempts recover ABORTED. Post-terminal packaging loss cannot be repaired by a new
dispatch or an automatic completion claim.

PIDs/TIDs, process start identity, addresses/ASLR bias, descriptor numbers, device/
inode, raw timing and debugger numbers are forensic association fields only. Stable
identity is the pinned artifacts/descriptor hashes, X, E and causal journal/control
links. Canonical witness remains free of volatile values. Same semantic input yields
the same canonical serialization; raw transcripts/maps/manifests can differ between
runs. P01 comparison removes only X and its derived link hashes from semantic
comparison, never measurements, failures, arguments or counts; originals are retained.

## 11. ACCEPT criteria

ACCEPT iff all are positively evidenced:

1. E and the retained qualification package are valid, complete and independently
   frozen; engine/observer admission, including resolved Q1, passes with no drift.
2. The correct native receiver is reached via its qualified paired actual callable,
   with live image and exact child/thread association.
3. Exactly one X has a durable ATTEMPTED preceding its one-use release and exactly
   one qualifying entry, with no unmatched/early/extra entry or ambiguous pairing.
4. The actual original source is independently decoded exact PyBytes B, length 2,
   complete direct bytes `23 0a`, independent digest and full byte equality.
5. B is the observed final object from the single A read/resize/return; its identity
   is retained, and independent A capture plus exact seals/custody agrees at entry.
6. Every actual positional/keyword object, exact type/count/value and callable/root
   association matches; no default/coercion/harness-intent substitution is used.
7. Guards and bounded coverage are complete; no source redirection/reopen/execution,
   scientific/client activity, post-entry resume or observer discontinuity occurred.
8. Clean observer_stop and confirmed child death precede complete synchronized
   witness/terminal/package evidence and its verified hash links.

No observation, unknown required fact, incomplete capture or missing artifact can
satisfy these conditions. Compiler success and execution evidence are not criteria.

## 12. REFUSE, ABORT and precedence

Retain the input specification's precedence exactly:

`RECORD_INVALID > EXPECTATION_INVALID > WRONG_PROTECTED_OBJECT > INPUT_IO >
INPUT_TYPE > INPUT_TRUNCATED > INPUT_APPENDED > INPUT_ALTERED > PROFILE_UNQUALIFIED >
ENGINE_UNQUALIFIED > WRONG_COMPILE_CALLABLE > SOURCE_REDIRECTION > WRONG_ENTRYPOINT >
OBSERVER_UNQUALIFIED > OBSERVER_NOT_ARMED > PATHNAME_REOPEN > OBJECT_SUBSTITUTION >
INVOCATION_COUNT > OBSERVATION_MISSING > EXECUTION_PROHIBITED`.

Here `>` means earlier rank selects primary among **actually evidenced** faults,
not severity. Rank remaining diagnostics uniquely; do not perform later stages merely
to collect codes. Any EXECUTION_PROHIBITED invalidates the whole circuit regardless
of primary rank. `ATTEMPT_INCOMPLETE` is recovery-only, not a normal REFUSED code.
Argument substitution maps to WRONG_ENTRYPOINT; source-reference substitution maps
to OBJECT_SUBSTITUTION; do not create a competing ARGUMENT_SUBSTITUTION code.

Complete qualified normal negative observations produce REFUSED. Wrong executable,
hash, maps/address, callable, source/type/length/content, parameters, PID, incomplete
read or count/binding failure maps as in section 9. Stop before dispatch for admission
failures. Observed source replacement retains OBJECT_SUBSTITUTION as a supported
diagnostic even when a higher-ranked measured type/content fault also exists.

Unexpected signal/exit, observer/channel loss, ambiguous termination, failed/torn
persistence or incomplete nonterminal evidence produces ABORTED on recovery; complete
invalid retained records select RECORD_INVALID, otherwise ATTEMPT_INCOMPLETE. Earlier
supported faults remain diagnostics. Preserve original bytes and partial files. A
failed observer is never converted to clean observer_stop. Breakpoint timeout is
OBSERVATION_MISSING only with a complete qualified negative witness, otherwise ABORTED.
Unknown entry count is not serialized as an invented zero: incomplete capture cannot
form the complete witness and instead uses recovery's nullable entered/prefix facts.

All ABORTED/REFUSED/ACCEPTED attempts are terminal; no retry, ID reuse, late callback,
automatic evidence repair or resumed consumption. Existing valid terminals remain
unchanged. Custody conflict or incompatible recovery stops rather than overwrites.

## 13. Claim ceiling and residual assumptions

The strongest successful statement, conditional on the assumptions below, is:

> For this bounded offline inert attempt, the qualified CPython builtin_compile native receiving entry independently received the exact protected source bytes associated with attempt X.

This does **not** establish compiler correctness, parser correctness, generated-code
correctness, successful compilation, execution, runtime dependency integrity, import
integrity, full external_trust_root resolution, dependency_runtime_lock resolution,
scientific validity, E0 authorization or E0 readiness.

Residual assumptions are honest host/kernel/procfs, ptrace/debug hardware and memory
read semantics; ordinary filesystem/fsync durability; correct pinned GDB/controller/
decoder/hash tools and reviewed native launch/bootstrap/guards; Ubuntu provenance
trust within its recorded scope; no hostile concurrent native memory writer; and
truthful narrow origin dossiers for tools without reconstructed supply chains.
Observer independence is from harness-generated receipt assertions and inferior
hashing/results, not from all bootstrap behavior or a malicious kernel/interpreter.
Stops, debug registers and termination affect state/timing. Nothing is claimed
non-invasive, reproducibly built, transitively hermetic or hostile-root resistant.

## 14. Implementation readiness and one unresolved design question

**PARTIAL — Q1 only:** What exact initialization/control policy for the pinned
`/usr/bin/gdb` prevents **all internal software breakpoint insertion** throughout
launcher/exec/bootstrap/derivation/paired observation while preserving the required
hardware breakpoints and syscall/exec catchpoints?

Why this is substantive: requesting `-break-insert -h` specifies the two user sites,
but does not constrain debugger-internal shared-library/step machinery. Installed
GDB strings identify `svr4_create_solib_event_breakpoints`; this is a warning to
inspect the exact backend, not proof that a patch happened. Official documentation
describes internal shared-library event breakpoints. `auto-solib-add off` controls
symbol loading, and `stop-on-solib-events 0` controls reporting; neither is asserted
here to prohibit internal text patches. Conversely, globally disabling breakpoint
insertion cannot simply be assumed compatible with required hardware stops.
See [GDB maintenance/internal breakpoints](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Maintenance-Commands.html).

Thus this document freezes **no text patch**, forbids fallback, and leaves precisely
that command-policy question open. It does not falsely claim an exact executable
GDB recipe has been completed. An answer must supply a reviewed, build-specific
command/backend contract with safe failure semantics; if stock GDB cannot satisfy
it, stop for a separately authorized architecture decision. Do not patch GDB, swap
observers, add software breakpoints or weaken the frozen observer document here.

The selected parent-death chain, pread resize/object tracking, ABI, durable state
machine, paired transition, termination, artifacts, criteria and negatives above
are design decisions, not additional unresolved alternatives. Future implementation
artifact hashes, fixed-bootstrap qualification and actual hardware/permission/stop/
death-chain tests remain required implementation and admission work; no success is
presumed. They are not populated with invented values to obtain READY. No live
experiment is authorized while Q1 or any admission requirement is unsatisfied.

One next bounded action only: separately authorize a **document-only review of Q1
against the pinned GDB's backend and initialization semantics**, producing one closure
or impossibility receipt without running/attaching GDB or implementing anything.
That action is not performed in this circuit.

## 15. Preservation receipt

The sole authorized new repository artifact is this document. Pre-commit verification
checked all 218 pre-existing tracked paths against their Git blob identities and
HEAD before: no differences. The initial index was clean and the only untracked path
was this document. The three controlling SHA-256 values above were independently
rechecked and match. Staging is restricted to this document. Frozen H2A1, sealed-handoff, surrogate implementations/tests/
fixtures/evidence, engine provenance and observer design are unchanged. No tests
are run: their imports/runtime activity would exceed this document-only circuit.

The session's operations are static reads, text editing, literal-data hashing,
read-only official references and scoped administrative Git publication. No GDB
launch/attachment, Python launch, candidate compile/eval/exec/import, implementation,
E0 invocation or dependency_runtime_lock work occurs. This is a scoped action-log
receipt, not a machine-wide audit of unrelated processes. Commit/push verification
and the resulting HEAD are reported outside this file to avoid self-referential
commit hashes. E0 remains HOLD.

- experiment boundary: one future offline inert native input receipt; terminate at entry.
- fixture: `23 0a`, length 2, SHA-256 `32c4858e22cc2c967b42150fa550562a2c839c2cebcaab91cabdf6f4da020022`.
- engine admission: exact qualified executable/package/GDB pins plus live maps/code/ABI/callable and observer checks; any failure STOP.
- attempt lifecycle: reserved/registered → PREPARED → durable ATTEMPTED → logical OBSERVED → ACCEPTED/REFUSED; interruption ABORTED; no schema extension.
- GDB/MI supervisor design: external controller, launch/death custody chain, one-use barrier, direct native reads, confirmed stopped-child termination; Q1 blocks the initialization policy.
- ABI decoding: real native vector plus kwnames tuple and exact primitive/callable/module/dict layouts; no harness-intent evidence.
- paired-stop design: caller `0x581feb`, receiver `0x69bff0`; ordered single CALL, same objects/thread, stack return `0x581fed`; both required.
- byte receipt rule: actual PyBytes/type/length/direct capture/independent SHA-256; retained final B identity and independently read sealed A equality, same X/native pair.
- substitution matrix: fixed P01 twice and bounded N01–N11 subcases; pre-dispatch, replay and live interruption evidence distinguished; no fuzzing.
- evidence package: unchanged canonical schema plus raw MI/maps/registers/bytes/arguments/derivation/completion and acyclic hash manifests; incomplete package cannot yield public ACCEPT.
- ACCEPT criteria: all eight positive predicates in section 11; compilation success unnecessary.
- REFUSE/ABORT criteria: inherited ranked faults; interruption/ambiguity/incompleteness fail closed, immutable terminal/recovery semantics.
- claim ceiling: exact protected bytes received at builtin_compile for X only; no parser/compiler/code/execution/dependency/import/full-gate/E0 claim.
- residual assumptions: trusted host/kernel/debugger/controller/decoder/hash/storage, reviewed bootstrap and no hostile native writer; no full runtime closure.
- implementation readiness: PARTIAL, exactly Q1 hardware-only GDB initialization policy unresolved.
- external_trust_root status: UNRESOLVED; no real receipt established by this document.
- dependency_runtime_lock status: UNRESOLVED and not begun.
- H2A1 status: VERIFIED and frozen, unchanged.
- H2A2 status: sealed handoff VERIFIED; surrogate VERIFIED WITH RESIDUAL ASSUMPTION; engine provenance qualified and observer architecture prospectively qualified; real receipt not performed.
- E0 status: HOLD.
- one next bounded action only: separately authorized document-only Q1 closure/impossibility review; not performed.
