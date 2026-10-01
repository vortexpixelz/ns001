# NS-001 H2A2 real CPython GDB Q1 review v0.1

Date: 2026-10-01 (America/New_York). HEAD before:
`8a6a72c8fcc2e7db44b329d9d7f666784a68f743`.
Branch: `codex/e0-h2-preparation`; initial and resumed working trees clean.

## Decision and scope

**Q1_CLOSED**, prospectively, for the pinned Linux x86-64 native target under
the complete policy below. Implementation readiness becomes **READY prospectively**;
this is not implemented-observer qualification, permission to run, a real receipt,
or E0 readiness. No GDB process was launched, no process attached, and no candidate
source compiled, evaluated, executed or imported in this circuit.

The decisive build-specific distinction is that `set may-insert-breakpoints off`
guards **software** insertion in `target_insert_breakpoint`, while
`target_insert_hw_breakpoint` delegates separately without that guard. Exec and
syscall catchpoints also use separate native operations. Add
`set may-write-memory off` before any inferior exists, explicit hardware user sites,
and in-place hardware stepping with displaced stepping disabled. Do not use the
aggregate `set observer on`, which also disables stopping and changes execution mode.

This is an insertion-denial policy, not a claim that GDB stops creating internal
breakpoint objects. The normal loader breakpoint remains an internal object whose
insertion is denied and whose shared-library location becomes disabled. The exact
nonfatal path is established below. An unexpected internal object, an insertion
error outside that path, or inability to continue safely fails admission; it never
authorizes temporarily enabling writes. No required observation relies on GDB's
internal loader-event stops or its automatically updated shared-library list.

The controlling experiment's no-patch object is the experiment inferior's executable
text, including its launcher and loader across exec. This review does not claim that
stock GDB performs no writes in its own process or no private feature-probe activity.
Those are explicitly distinguished in section 4; the frozen experiment is not weakened.

## 1. Custody and source-to-build evidence

The following controlling documents remain unchanged:

| Document | SHA-256 |
| --- | --- |
| `NS-001_H2A2_REAL_CPYTHON_RECEIPT_EXPERIMENT_DESIGN_v0.1.md` | `b120fb71ca537d84926e0b81173d1f867f9e92cbde0c54696191c0a8cafee54d` |
| `NS-001_H2A2_REAL_CPYTHON_NATIVE_OBSERVER_DESIGN_v0.1.md` | `cdca62d5f02a468353d4c0ba9113e3d4ced047f4b78f68c949b1141bbad1b075` |
| `NS-001_H2A2_REAL_CPYTHON_ENGINE_PROVENANCE_REVIEW_v0.1.md` | `3fd49cf843b582ddffed971281e226c2d1f419462c17150ca48e82a3b649453e` |

Read-only local measurements:

| Object | Measurement |
| --- | --- |
| Installed debugger | `/usr/bin/gdb`; `gdb:amd64` `15.1-1ubuntu1~24.04.1` |
| Debugger SHA-256 | `3832cc070ae1716e322105d3b39fb398695e5f031c9d39224cf227a8c2b889f6` |
| ELF build ID | `ce472a6ab791cee8365de57828ddd56443d3c862` |
| Target corroboration | Installed binary strings contain `x86_64-linux-gnu` and the software-insertion permission command/diagnostic; package is amd64 |
| CPython SHA-256 | `e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f`; `python3.12-minimal:amd64` `3.12.3-1ubuntu0.17` |
| Loader | `/lib64/ld-linux-x86-64.so.2`; SHA-256 `c20a2dc8917c755f02b94049356320fe1f62ac7d9f8994731f807d9df39302da`; libc6 `2.39-0ubuntu8.9` |
| Loader rendezvous | Exported `_dl_debug_state` value `0x2820`, size 5; relocated address is loader bias + `0x2820`, not a fixed process VA |

The exact Ubuntu source descriptor, original archive, Debian patch archive and binary
package were downloaded to `/tmp/ns001-gdb-q1` for static inspection. Only archives
were extracted; no build, installation, package configuration, patch application or
GDB invocation occurred. The binary package's extracted `usr/bin/gdb` is byte-identical
to the installed binary (`cmp` succeeded), not merely version-identical.

| Official archive object | SHA-256 |
| --- | --- |
| [Source descriptor](https://archive.ubuntu.com/ubuntu/pool/main/g/gdb/gdb_15.1-1ubuntu1~24.04.1.dsc) | `98a1d43541a6ecd7bb342cc37136f90333a5504c270b8111833d650f367b577e` |
| [Original GDB 15.1 source](https://archive.ubuntu.com/ubuntu/pool/main/g/gdb/gdb_15.1.orig.tar.xz) | `38254eacd4572134bca9c5a5aa4d4ca564cbbd30c369d881f733fb6b903354f2` |
| [Ubuntu/Debian changes](https://archive.ubuntu.com/ubuntu/pool/main/g/gdb/gdb_15.1-1ubuntu1~24.04.1.debian.tar.xz) | `1afc1be525de13fc76ae6007d9111408b03370e566c63908700c9f212dfa9295` |
| [amd64 binary package](https://archive.ubuntu.com/ubuntu/pool/main/g/gdb/gdb_15.1-1ubuntu1~24.04.1_amd64.deb) | `7069c23ce3bc350646498e6607749c568f5c403b0db2204310a94baff3d85745` |

Both source archive hashes match the descriptor; the binary package hash matches the
local APT package metadata. This is archive/package association with direct binary
equality, not a reproducible build or a newly verified distribution signature chain.
The descriptor's signature was not independently authenticated here. That origin
assumption remains explicit and does not resolve `external_trust_root`.

Source references below identify paths within the hash-pinned original archive,
with its original line numbers. The active `debian/patches/series` was reviewed:
none changes the decisive breakpoint, solib-svr4, x86 debug-register or stepping
semantics cited here. The ptrace patch adds attach-error diagnostics; it does not
change resume or launch behavior. The two configure.nat patches concern GNU Hurd,
not the Linux x86-64 branch. Other active changes concern Fortran/TLS printing,
libcc1/build handling, remote strings and s390 instructions. Commented-out patches
were not treated as applied. `gdb/configure.nat:319-326` selects the x86/amd64 Linux
native modules; the base Linux configuration includes the ptrace/native startup code.

## 2. Exact software/hardware separation

The controlling source chain is:

1. `gdb/breakpoint.c:11979-12003`, `code_breakpoint::insert_location`, selects
   `target_insert_hw_breakpoint` for `bp_loc_hardware_breakpoint`; otherwise it calls
   `target_insert_breakpoint`.
2. `gdb/target.c:2356-2367`, `target_insert_breakpoint`, returns failure **before**
   delegating when `may_insert_breakpoints` is false. It emits the diagnostic
   `May not insert breakpoints`. Internal code breakpoints use this same guard.
3. `gdb/target.c:541-546`, `target_insert_hw_breakpoint`, delegates to the hardware
   target method without consulting that flag. Thus the manual's general wording
   about “all breakpoints” must not be read as a source-level hardware veto here.
4. `gdb/mem-break.c:38-69` would save original bytes and call
   `target_write_raw_memory` to insert the architecture trap. The x86 trap is the
   one-byte `0xcc` (`gdb/i386-tdep.c:613`).
5. `gdb/target.c:1652-1667`, `target_xfer_partial`, separately rejects writes when
   `may_write_memory` is false, including raw target-memory transfers. This also
   blocks other normal GDB target-memory writes; it is not relied on to prohibit
   a hardware debug-register operation.

Both permission flags must be false from before the first file/inferior through
confirmed inferior death. Do not toggle them after a patch and call the restored
bytes proof of non-patching. Software removal is permission-guarded too: this policy
must begin in a fresh GDB session with no existing inferior or inserted breakpoint.

## 3. Solib behavior and why denial need not prevent progress

`gdb/solib-svr4.c:3037-3060` calls `enable_break` whenever the native target has
execution and the SVR4 link-map layout is available. `enable_break` obtains loader
information using the link map, ELF interpreter, auxiliary-vector base and symbol
lookup. It calls `solib_add(..., auto_solib_add)` but does **not** use that setting as
a veto on creating event breakpoints.

`svr4_create_solib_event_breakpoints` (`2179-2192`) uses glibc probes when available,
or falls back to the rendezvous function. Both routes call
`create_solib_event_breakpoint`; `gdb/breakpoint.c:7947-7961` creates an internal
`bp_shlib_event`. That is a software location by default (`7500-7524`). These are
text patches in an ordinary writable-debugger configuration, even if user sites are
all hardware. The probe interface does not make them kernel tracepoints.

`stop-on-solib-events 0` suppresses user-visible stops. Its update routine only
disables probe locations classified `DO_NOTHING` (`solib-svr4.c:2000-2048`), not
every loader breakpoint. `auto-solib-add off` suppresses automatic symbol loading;
it still permits mapping a loader BFD and recording its section ranges. Neither is
the no-patch enforcement mechanism.

The exact progress-preserving path with this policy is:

* Keep normal local loader lookup (`sysroot /`, no nonexistent sysroot trick),
  `auto-solib-add off`, and `breakpoint auto-hw off`.
* `enable_break` opens the ELF interpreter, finds its load base, records the loader
  in the solib list, then creates the rendezvous breakpoint (`2315-2469`). At initial
  startup, the fallback loader list is supplied by `svr4_default_sos` (`1183-1208`),
  using `debug_loader_name` and `debug_loader_offset`. Automatic symbol loading is
  not needed for these mapped ranges.
* `target_insert_breakpoint` denies insertion, returning the generic failure that
  `insert_bp_location` constructs in `breakpoint.c:2899-2914`.
* For a software location associated with a known shared object, the failure branch
  at `breakpoint.c:2992-3024` sets `bl->shlib_disabled=1` and returns **zero**, rather
  than making the whole resume fail. `solib_name_from_address`
  (`gdb/solib.c:1163-1170`) checks the mapped solib ranges. The location was never
  inserted; it is not inserted and then removed.
* `should_be_inserted` (`breakpoint.c:2383-2393`) skips such locations. Re-creation
  after exec or later solib reset repeats the same denial; the guard stays false.

With automatic loader symbols off and no explicit loader-symbol command, the normal
initial path has no loader objfile for probe discovery and uses the single classic
loader rendezvous. If a previously qualified configuration legitimately exposes
loader probes, every such location must still be recognized, denied and accounted
for; it cannot be accepted ad hoc. For the exact policy here, qualification freezes
the classic rendezvous path, including its relocated loader range and event-object
inventory, before an attempt. Missing/mismatched loader files, a main-entry fallback,
unexpected probes or an unrecognized warning **refuse admission**.

In particular, a missing loader can cause `enable_break` to fall back to a main-image
symbol (`2470-2518`). Denying that insertion can be fatal because it is not a known
shared-library location. It is a safe failure, not the policy's success path. Do not
hide the loader with a fake sysroot, delete negative-number breakpoints and hope they
stay deleted, catch errors and blindly continue, or convert internal events to
hardware and consume unbudgeted debug slots.

Losing GDB's loader-event monitoring does not remove a frozen required observation:
process/image/map association already comes from pidfds, actual exec notification,
open executable identity, ELF offsets, independent `/proc` maps and live code bytes.
Treat GDB's shared-library list as potentially stale and never as that association's
authority. No `catch load`, symbol-based pending site, library initializer breakpoint
or automatic symbol-resolution service is needed by the numeric-site experiment.

## 4. Software-patch source inventory

| Mechanism | Exists on this build/path; ordinary text effect | Policy and capability impact |
| --- | --- | --- |
| SVR4 rendezvous and glibc solib probes | Yes; ordinary software locations overwrite loader instructions with `0xcc` | Deny before insertion; qualify classic loader association and nonfatal disabled-location path. Loader-event tracking is lost; independent map/image association remains. |
| Initial inferior startup | Native fork/TRACEME/exec startup uses kernel traps, not a breakpoint planted at main; solib setup follows | `startup-with-shell off`, ordinary run only. No `start`, run-with-start option or startup command file. Required launcher-to-CPython exec remains observable. |
| Loader-discovery fallback at main/start | Source path exists if interpreter/rendezvous discovery fails; can patch main-image text | Prevent writes and refuse this path. Working local loader identification is mandatory. |
| Exec catchpoint | Yes; Linux ptrace event, not a code location | Retain `catch exec`; permission guards do not block its native event method. |
| pread64 syscall catchpoint | Yes; ptrace syscall entry/return stops, not a code location | Retain `catch syscall 17`; no software insertion. |
| Explicit hardware user sites, including sequential derivation sites | Yes; x86 execute debug registers, no text patch | Require literal numeric `-break-insert -h`; slot or kernel-programming failure refuses. |
| Software user sites or automatic hardware selection | Available, but not required | Forbid plain break/tbreak and set `auto-hw off`; explicit `-h` remains hardware. This prevents internal locations being promoted into the user-slot budget. |
| Native single-instruction step | Yes; x86 hardware step via ptrace, no successor software breakpoints on this architecture | Only one forward `-exec-step-instruction` at the qualified CALL; no `nexti`, source step, reverse or run-to-return. |
| Displaced stepping | Available; copies an instruction into inferior scratch memory, possibly code storage | `displaced-stepping off` before startup. In-place hardware stepping preserves the required CALL/stack transition. Memory-write denial is an additional guard. |
| Step-resume, longjmp, exception/terminate and until/finish temporary sites | Source machinery exists and normally uses software locations when enabled | `stepi` preparation specifically skips longjmp setup; master breakpoints are created disabled. Forbid the commands/conditions that activate these paths. Unexpected activation stops under the guards. |
| Signal-delivery step-resume or permanent-trap skip | Source paths exist; can require a temporary software site or manipulate PC | No pending/delivered signal in the paired interval; stop on unexpected signals, never auto-continue. Caller bytes `ff d0` and receiver `f3 0f 1e fa` are not permanent `int3` sites. |
| Thread-library event breakpoints | Available through libthread_db; can be software | Disable auto-loading AND remove `$sdir`/`$pdir` from its search path as below. Native single-LWP control and independent task enumeration remain; no thread-library service is required. |
| JIT registration and overlay events | Available when special symbols/interfaces exist; software internal sites | No JIT reader, overlay support or such image/interface is admitted. CPython's dynamic symbol inspection found no `__jit`, `_ovly` or `_dl_debug_state` match. Qualify launchers and all admitted images separately; guard denies unexpected insertions. |
| IFUNC resolver/return, inferior calls, dprintf and trace/record machinery | Available; some use temporary software sites, injected instructions or memory writes | Literal resolved addresses only; no symbolic resolver invocation, inferior calls, dprintf, tracing or recording. `may-call-functions off` and tracepoint permissions off add enforcement. No required observation is lost. |
| Other architecture/remote fallback | Software stepping and remote insertion exist elsewhere in source | Admit only the pinned native amd64 target, one inferior, fixed architecture. No remote/multiarch/ABI substitution. |

References for the non-solib internal paths include `breakpoint.c:3609-3889`
(disabled master sites), `7480-7538` (location types), `infcmd.c:812-825`
(stepi skips longjmp), `infrun.c:2730-2909` (permanent traps, signals and displaced
steps), and `jit.c:869-931` (registration symbols). Missing runtime image inventory
is an admission failure, not evidence that no internal source exists.

Do not overgeneralize the permission guards: `nat/linux-ptrace.c:117-255` contains
a startup NX feature probe that writes `0xcc` into a private anonymous **RW** mapping
in GDB and forks a private probe child. `linux-nat.c:4199-4253` tests `/proc/self/mem`
by writing a GDB-local data variable. These bypass the inferior-memory permission
path, but neither patches the experiment inferior's executable text or installs a
software breakpoint in its launcher/CPython/loader. Account for these debugger-owned
helper processes separately; never mistake them for the experiment child or its
threads. This policy would not satisfy a different, broader prohibition on every
`0xcc` write anywhere in GDB and all its private feature probes. No such global
process-wide claim is made by the controlling no-inferior-text-patch requirement.

## 5. Hardware sites, exec, syscalls and paired transition

### Explicit user hardware sites

`gdb/mi/mi-cmd-break.c:329-389` maps `-h` to `bp_hardware_breakpoint` and passes
pending=false unless `-f` was supplied. `handle_automatic_hardware_breakpoints`
(`breakpoint.c:8407-8445`) excludes owners explicitly typed hardware; changing a
memory map does not turn an explicit `-h` site into software.

`x86-nat.c:154-162` requests `hw_execute`, length 1, at the exact address; lack of
resources returns `EBUSY`. `breakpoint.c:3028-3065,3337-3351` reports hardware
insertion failure, not a software retry. `nat/x86-linux-dregs.c:54-70,140-181`
programs the sole LWP's actual debug registers with `PTRACE_POKEUSER` before resume;
a kernel failure raises an error. The intermediate register mirror is not that
kernel write and is not proof of effective arming.

Require exactly one resolved location at each requested VA, hardware type, expected
inferior/thread scope, enabled status, no condition/ignore count/commands, no pending
or duplicate location, and no unexpected site. No `-f`, `-a`, `-t`, symbolic location,
regex, watchpoint, tracepoint or dprintf is permitted for these sites. The literal
address parser is not permission to evaluate an inferior expression.

The steady compile pair is caller `0x581feb` and receiver `0x69bff0`. During derivation,
keep the receiver monitor and use one other slot sequentially at `0x4f6102`,
`0x4f6224`, `0x4f6274`, `0x4f6299`; delete the retired location before inserting
the next. The pread and resize CALL coordinates are disassembly checks, not extra
simultaneous sites. Budget two distinct execute slots, with no data watchpoints or
internal hardware promotions. A machine having four architectural address registers
does not prove two are effectively available to this observer.

`always-inserted on` makes location insertion happen promptly and keeps sites in
place across ordinary stops. It does not bypass deferred native debug-register
programming or guarantee available slots. Neither on nor off is a no-software-patch
guard. The frozen blocked-channel resume/re-stop qualification is still required
before ATTEMPTED; an MI creation success or breakpoint-table row is insufficient.

### Exec and syscall mechanisms

`linux-nat.c:426-441` requests `PTRACE_O_TRACEEXEC` and `PTRACE_O_TRACESYSGOOD`;
`2115-2150` recognizes `PTRACE_EVENT_EXEC`, reopens the address-space memory handle
and reports an exec event. `insert_exec_catchpoint` (`632-635`) simply succeeds:
there is no inserted instruction. `inf-ptrace.c:74-109` and
`nat/fork-inferior.c:448` establish native startup through ptrace/exec traps.
Subsequent launcher-to-CPython exec association uses `catch exec`, then the frozen
independent process/image checks before CPython bootstrap resumes. The source also
requests EXITKILL for a launched inferior; this is not a measured effective flag
and does not replace the frozen parent-death chain.

`linux_nat_target::set_syscall_catchpoint` (`linux-nat.c:644-654`) does not plant a
breakpoint. `inf_ptrace_target::resume` (`inf-ptrace.c:256-286`) chooses `PT_SYSCALL`
(Linux `PTRACE_SYSCALL`) when syscall catching is enabled. Linux's tagged syscall
stops are classified and filtered by GDB. Use numeric `catch syscall 17`; retain
both entry and return, actual registers, one return of 2, and all frozen refusal
conditions. A catchpoint definition alone proves neither stop occurred. Retire it
after derivation before the compiler pair. No software insertion is needed for
either catchpoint.

### One CALL, then receiver entry

`mi_cmd_exec_step_instruction` (`mi/mi-main.c:197-205`) dispatches forward `stepi`.
`infcmd.c:1026-1035` sets a one-instruction step and `STEP_OVER_NONE`;
`infrun.c:2370-2378` uses software stepping only if the architecture provides that
hook. The admitted amd64/Linux initialization does not install a software-single-step
hook. `inf-ptrace.c:269-277` selects `PT_STEP`/`PTRACE_SINGLESTEP`, overriding syscall
resume mode for a step. This uses the x86 hardware single-step facility/trap flag.

With displaced stepping off, the inline step-over excludes only the current caller
address. `infrun.c:9048-9108` inserts other breakpoints; `breakpoint.c:2413-2432`
skips the location being stepped past, not the distinct receiver. The receiver
therefore remains enabled for the resumed LWP while the caller site is temporarily
omitted as necessary. At ordinary stops, always-inserted mode avoids the default
wholesale removal. Native register programming still occurs before each resume.

For the validated `ff d0` CALL, one successful hardware step reaches `0x69bff0`,
pushes `0x581fed`, and stops before the receiver's first instruction. This is a
source-supported mechanism, **not a guarantee against signals, broken hardware or
an operationally unqualified kernel**. Preserve raw native trap provenance and the
frozen PC/RSP/return-address/argument checks. Single-step and execution-breakpoint
reasons can interact; do not demand an invented second hardware trap or resume to
manufacture one. Qualification must establish the exact observed reason on this
host. No temporary software return breakpoint is required by this forward stepi.

## 6. Exact prospective initialization/control contract

This section is a specification only. None of these GDB commands was executed.
Launch the pinned GDB in a fresh session with `--nx --nh --interpreter=mi2`, no
positional executable, `--args`, command file, extra `-ex` or inherited startup
automation. The controller supplies the following early commands via individually
quoted `-iex` arguments, in the stated order, before any file/inferior is loaded:

```text
set auto-load off
set debuginfod enabled off
set may-insert-breakpoints off
set may-write-memory off
set may-insert-tracepoints off
set may-insert-fast-tracepoints off
set may-call-functions off
set libthread-db-search-path /dev/null
set startup-with-shell off
set non-stop off
set displaced-stepping off
set breakpoint auto-hw off
set breakpoint pending off
set auto-solib-add off
set stop-on-solib-events 0
set sysroot /
set solib-search-path
set breakpoint always-inserted on
set trust-readonly-sections off
set code-cache off
set stack-cache off
set pagination off
set debug breakpoint 1
set debug infrun 1
set debug linux-nat 1
set debug target 1
```

Purposes, and qualifications of those settings:

* `--nx --nh` suppress initialization files, including early/user/local startup
  commands; `auto-load off` disables the boolean auto-load facilities before loading
  any object. No GDB Python/Guile script, extension, pretty-printer, hook or user
  command is admitted. Debuginfod is off and its URL environment is empty, so symbol
  acquisition cannot introduce network material during the offline experiment.
* The two primary permissions enforce software-insertion/memory-write denial.
  The tracepoint and inferior-call permissions close unused mutation routes.
  Keep normal stopping and register-control permissions enabled; do not invoke
  observer mode. Internal debug-register control is necessary. Controller-issued
  memory/register assignment remains prohibited by the MI/CLI command allowlist.
* The explicit libthread_db search path contains neither `$sdir` nor `$pdir`.
  `/dev/null` is not a directory, and `auto-load off` causes the ordinary directory
  loader path to return false. This matters because `$sdir` system loading bypasses
  `auto_load_thread_db` (`linux-thread-db.c:1106-1174`). The setting is not a sysroot
  change and does not hide the ELF loader. Require no libthread_db layer loaded.
* Shell-free, all-stop, single-inferior operation preserves the custody model.
  Displaced stepping off prevents instruction-copy writes. Auto-hardware selection
  off prevents unbudgeted internal promotions; pending off rejects unresolved sites.
* Solib symbol/report settings reduce unused services but are not the write guard.
  Normal sysroot and empty extra solib search path retain local loader identification.
  Qualify the exact interpreter path/BFD/ranges; no missing-file fallback is allowed.
* Always-inserted on supplies stable breakpoint lifetime, subject to native deferred
  programming and inline caller-step exclusion. Raw inspection settings prevent
  executable-file substitution and normal code/stack caching from being mistaken
  for a current inferior read. They do **not** disable breakpoint shadow masking.
* Pagination off makes the supervised protocol noninteractive. The four debug
  settings retain breakpoint, run-control, native-event and target-operation
  diagnostics in the bounded forensic transcript. Logs are supporting evidence,
  not independent kernel measurements. Transcript overflow/loss refuses admission.

The launch environment must be explicitly frozen, with locale `C`, empty
`DEBUGINFOD_URLS`, no LD_PRELOAD/LD_AUDIT or alternative library/Python selection
variables, and the reviewed tool/bootstrap identity dossier. No later command may
change these permissions, execution mode, architecture, target, sysroot or policy.
An early-command failure may not terminate GDB automatically: the controller must
reject every startup error and obtain complete `show` readback before loading the
launcher. There must be no inferior yet, no user-defined hooks and no breakpoint.

Use tokened `-interpreter-exec console "show ..."` for each setting above, plus
`show may-stop`, `show may-write-registers` and `show observer`; require stopping
and register control on, observer off. Use `show auto-load` to confirm its individual
boolean settings. Settings/inspection commands are literal allowlisted strings,
not dynamically assembled expressions. Before file loading, also confirm empty
internal/user breakpoint and inferior-execution inventories.

Load only the qualified launcher using `-file-exec-and-symbols`; define
`-interpreter-exec console "catch exec"`; use ordinary `-exec-run` exactly once.
The OS startup trap is consumed by native startup; the required subsequent launcher
exec is reported by the catchpoint. At that stop bind the actual CPython image and
install the numeric receiver hardware site before bootstrap. Install numeric
`catch syscall 17` for the bounded derivation interval, then retire it. Use the
sequential hardware sites and compiler pair described above. Readback/inspection
uses `-break-list`, `maintenance info breakpoints` and the frozen raw-register and
memory commands. Neither breakpoint listing nor debug-register mirrors are arming
proof. No automatic restart, error-recovery resume, detach or alternate mechanism.

Recognize only the prequalified blocked loader-insertion diagnostics: their site
must be the pinned loader rendezvous in the current image epoch, software insertion
must have been denied before delegation, and their location must be non-inserted
and disabled by the source path in section 3. They are expected denials, not ignored
failed hardware commands. An MI error, an unexpected warning/site, missing loader
range, changed policy, or unexplained internal event closes the gate and terminates
the attempt under the frozen failure rules. Never set a permission on to “get past”
startup. The launcher admission must prove that the normal path actually progresses.

## 7. Runtime verification contract for a later authorized implementation

**No runtime admission evidence was collected here.** Configuration intent, static
source proof and measured admission must remain separate artifacts.

Before ATTEMPTED, a later qualification/implementation must retain all of:

1. Exact debugger/engine/loader and launcher/tool pins, target/architecture, complete
   early startup settings and readbacks, a continuous tokened MI/debug transcript,
   and sole controller custody. All permissions remain fixed from before initial
   launch. This supplies the source-enforced historical non-insertion argument;
   end-state byte equality alone cannot rule out a patch that was later restored.
2. Raw, unmasked live text comparisons at initial launcher admission, post-exec,
   READY, caller and receiver, and after any admitted mapping change. Cover all
   executable PT_LOAD file-backed ranges of each relevant image, including the
   loader; specifically CPython file `0x020000..0x302fbc` inclusive and every site.
   Bind file handles, maps, offsets and load biases independently. Reject code
   mutations, unqualified relocations, WX pages and partial reads. Compare exact
   bytes, not “no `0xcc` anywhere”: an image may legitimately contain that byte.
3. A raw read channel independently validated to bypass GDB's breakpoint shadow
   replacement. Ordinary `-data-read-memory-bytes` is **not** sufficient for this
   negative proof: `target.c:1621` substitutes saved bytes for software breakpoints.
   A supervisor's permitted, complete stopped-child memory reads outside that
   substitution layer must agree with the qualified files and the raw MI capture.
   Freeze and qualify that read primitive before attempts; unavailable access means
   refusal, never assuming that the MI view is unmasked. No second tracer or target
   mutation is introduced by this read-only requirement.
4. A complete internal and user breakpoint inventory for every image epoch. Every
   allowed loader object is accounted for as denied/non-inserted; no unexpected
   software location or successful software insertion exists. Retain the blocked
   call/result chain, not just a `<PENDING>` display. Breakpoint tables alone cannot
   establish the location's actual state. Any contrary diagnostic or unexplained
   gap invalidates admission even if code bytes later match.
5. Qualified non-Python native launcher controls showing both execute slots really
   stop before their instructions, slot exhaustion/permission failures do not fall
   back, exec and syscall entry/exit events operate, and the exact in-place CALL
   step keeps the receiver armed and stops before entry instruction execution.
   Retain actual native-stop provenance, successful kernel programming evidence
   appropriate to the reviewed witness, and same-LWP association. A debugger mirror
   or MI `^done` alone is insufficient. The candidate cannot be used to learn or
   repair qualification parameters.
6. In the real attempt, successful bounded programming while the private gate is
   closed, followed by an all-stop recheck, before PREPARED/ATTEMPTED. At the native
   pair require the exact CALL, RAX target, PC, RSP decrement, return address, full
   argument/root equality and expected native reason; no intervening signal or
   unrelated event and no extra resume to improve ambiguous evidence.
7. The unchanged death-chain, one-shot dispatch, derivation and durable-writer
   requirements. Runtime metadata must show a qualified current kernel/host state;
   source compatibility with GDB does not itself qualify ptrace/debug hardware.

The historical no-patch argument is conditional on the pinned GDB executing the
reviewed guarded paths, exclusive controller command custody, and the unchanged
honest-host/no-concurrent-writer assumptions. Snapshots plus an ordinary breakpoint
list are not promoted into independent proof of every intervening instruction.
If those source/custody assumptions are unacceptable, a separately authorized
architecture decision is needed; this document does not silently claim hostile-GDB
or hostile-kernel resistance.

## 8. Readiness, update context and action boundary

No required stock-GDB mechanism necessarily patches experiment-inferior text under
this contract. The permissions separate software from hardware, the qualified solib
denial path preserves progress, and ptrace supplies exec/syscall/single-step events.
Thus an impossibility verdict is not supported. There is no remaining narrower
source-policy question designated Q1. Future effective slot/stop/memory/death-chain
measurements are the already-required operational qualification, not invented
completed evidence or permission to execute the experiment.

The user's supplied update log reports out-of-space failures while writing initramfs
images and configuration failures for initramfs-tools/a kernel-image package. The
live GDB, CPython and loader pins were rechecked after that note and still matched.
This neither diagnoses which filesystem is full nor certifies package-manager,
kernel, boot or host health. It does not invalidate the byte-specific static source
review; it is material context for a later current-host/durability admission. No
update repair, cleanup, reboot, package mutation or dependency-runtime-lock work
was performed or authorized by this review.

Only this new review document is authorized for the commit/push. Precommit comparison
passed for all 219 previously tracked files; status showed exactly this one untracked
document and no tracked changes. Whitespace checking passed, and the three controlling
document hashes and debugger pin above were reproduced. The index is additionally
checked to contain only this path before committing. The action
record consists of read-only Git/static/package inspection, official source/package
downloads and extraction in temporary storage, document authoring and requested Git
publication. No GDB invocation (including version queries), ptrace attachment, Python
interpreter/test harness, candidate compile/eval/exec/import, experiment implementation,
GDB/package modification, scientific/client invocation or E0 execution occurred.
This describes this agent's actions, not a forensic assertion about every host process.

## Final receipt

- pinned GDB: `/usr/bin/gdb`, 15.1, Ubuntu `15.1-1ubuntu1~24.04.1`, amd64; SHA-256 `3832cc070ae1716e322105d3b39fb398695e5f031c9d39224cf227a8c2b889f6`; exact archive binary equality verified.
- software-breakpoint sources: loader rendezvous/probes, fallback startup sites, temporary step/signal/longjmp/exception sites, thread/JIT/overlay/IFUNC and optional user/call/trace mechanisms reviewed; inferior writes denied prospectively by the full policy.
- hardware-only user-site verdict: explicit numeric `-break-insert -h` has no software fallback on this path; slot/programming failure refuses; effective arming remains a measured admission requirement.
- exec-catchpoint mechanism: Linux `PTRACE_O_TRACEEXEC` / `PTRACE_EVENT_EXEC`, no software site.
- syscall-observation mechanism: `PTRACE_SYSCALL` entry/return stops for syscall 17 with GDB filtering, no software site.
- single-step mechanism: one forward in-place `PTRACE_SINGLESTEP`; displaced stepping off; caller exclusion preserves the distinct receiver; native reason must be qualified.
- solib/internal-breakpoint finding: objects may exist, but software insertion is denied; known-loader failure becomes a disabled, never-inserted location. Symbols-off and visible-stops-off alone are insufficient.
- exact initialization policy: section 6; deny software insertion and memory writes before any file/inferior; explicit hardware sites; fixed solib, auto-load, thread-library and stepping policy; unknown/error paths refuse.
- runtime verification contract: section 7; continuous policy/custody evidence, unmasked full text comparisons, internal-location accounting, effective native hardware/exec/syscall/step controls before ATTEMPTED; not performed here.
- Q1 verdict: **Q1_CLOSED** prospectively.
- implementation readiness impact: **READY prospectively** at the design level; implementation and live admission unperformed and separately authorized.
- architecture impact: retain external GDB/MI plus independent supervisor; no replacement or weakening. Prior OBSERVER_QUALIFIED verdict remains prospective.
- residual assumptions: archive/source-to-build association without a reproduced build or freshly authenticated signature chain; honest host/kernel/debug hardware and pinned tools; guarded-path/controller custody; no concurrent native writer; qualified bootstrap/read/durability controls; update log is not host-health clearance.
- external_trust_root status: **UNRESOLVED**.
- dependency_runtime_lock status: **UNRESOLVED; not begun**.
- H2A1 status: **VERIFIED + frozen**.
- H2A2 status: sealed-handoff **VERIFIED**; surrogate consumption **VERIFIED WITH RESIDUAL ASSUMPTION**; engine **ENGINE_PROVENANCE_QUALIFIED**; native observer **OBSERVER_QUALIFIED prospectively**; no real receipt created.
- E0 status: **HOLD**.
- one next bounded action only: separately authorize an implementation-only circuit for this frozen real-receipt design and Q1 policy, with no experiment execution; do not perform it in this circuit.
