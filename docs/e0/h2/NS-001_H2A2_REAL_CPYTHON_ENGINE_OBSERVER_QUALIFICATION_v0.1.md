# NS-001 H2A2 real CPython engine/observer qualification v0.1

## Scope and decision

Review date: 2026-09-30. HEAD before:
`3f28b3519321d8a16501fc6a09b0400911cdca4e`, branch
`codex/e0-h2-preparation`, initially clean; 215 tracked regular files.
Authority: `NS-001_H2A2_REAL_CPYTHON_INPUT_BOUNDARY_SPEC_v0.1.md`, SHA-256
`eae004d95046d2c2a83fd7813f4b0485ce792e358403a406859280f4c0fdc564`.
This is one document-only qualification review. It implements nothing.

**Qualification verdict: NOT_QUALIFIABLE on the presently retained local evidence;
future implementation readiness: NO.** A concrete executable and native receiving
entry are identifiable. A qualified engine descriptor and qualified native observer
cannot yet be frozen under sections 3 and 6 of the existing specification. There are
multiple independent gaps, so PARTIAL (exactly one narrow unresolved issue) would
misstate the result. In particular, local package labels do not authenticate the
engine acquisition/build origin, and a GDB executable hash does not qualify an
observer, its bootstrap or its ability to operate in this execution context.

This is a current qualification refusal, not a proof that CPython/GDB are inherently
incapable or that a different interpreter, architecture change or full runtime lock
is mathematically necessary. The requested verdict taxonomy does not separately name
"multiple evidence gaps, architectural impossibility unestablished"; NOT_QUALIFIABLE
is used conservatively for that current non-admissibility, with this limitation made
explicit. No claim is weakened and no unresolved requirements are hidden in a single
nominal missing package to obtain PARTIAL. Narrow qualification may remain possible
without dependency_runtime_lock, but this circuit has not established it.

## Read-only evidence and exact candidate engine

Only administrative shell/file/hash/package/Git inspection was performed, plus the
explicitly allowed version command `/usr/bin/python3 -I -S -VV`. Its output was:

`Python 3.12.3 (main, Aug 31 2026, 10:18:26) [GCC 13.3.0]`.

No Python `-c`, script, module, interactive session, builtin compile/eval/exec/import,
acceptance test, observer attachment or target execution was requested. The version
command executes the interpreter's administrative version path, not candidate source;
it must not be described as zero interpreter process launches. No test suite was run.
There were no installs or research network requests. Git publication is separately
requested administrative traffic.

| Descriptor fact | Observed value and qualification limit |
| --- | --- |
| Selected executable | `/usr/bin/python3.12`; `/usr/bin/python3` resolves to it. Use the absolute versioned path in any future design. |
| Executable SHA-256 | `e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f` |
| Implementation/build | Local CPython 3.12.3; version output above; dpkg records `python3.12`, `python3.12-minimal`, `libpython3.12-minimal`, `libpython3.12-stdlib`, `libpython3.12-dev:amd64` as `3.12.3-1ubuntu0.17`. These are local assertions, not authenticated origin evidence. |
| Platform/ABI | ELF64, little-endian x86-64, System V; ELF type EXEC; local configuration SOABI `cpython-312-x86_64-linux-gnu`; pointer/size_t sizes 8; installed pyconfig undefines Py_DEBUG/Py_TRACE_REFS and enables WITH_PYMALLOC. Headers describe an ABI candidate, not proof of the loaded build. |
| ELF build ID | `337d65cf00021797985cc9f77c0cc334a9fbeb38`; corroboration only, not a replacement for SHA-256. |
| Compiler-bearing image | The executable itself. Its dynamic table has NEEDED libm, libz, libexpat and libc, **no libpython**. It contains the compile method table and receiving code. Executable/compiler roles therefore share the executable hash. |
| Other installed libpython | `/usr/lib/x86_64-linux-gnu/libpython3.12.so.1.0`, SHA-256 `1021f236227334ded6d1bbbc4bb6f5d933f793d8397c969896cfbdf03ce96223`; installed but not this executable's declared compiler image. Do not attach there merely because it exists. |
| Loader | ELF interpreter `/lib64/ld-linux-x86-64.so.2`, resolving to `/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2`; SHA-256 `c20a2dc8917c755f02b94049356320fe1f62ac7d9f8994731f807d9df39302da`. No live mapping or interposition measurement performed. |
| Build metadata | Installed Makefile records GCC target `x86_64-linux-gnu-gcc`, `-DNDEBUG -g -O2 -Wall`, frame pointers, hidden visibility, stack protection, and `--enable-shared` among configure arguments. The latter describes the installed build configuration and does not override the executable's actual NEEDED table. Full release build flags/source-to-binary provenance are not independently authenticated here. |

PATH inspection found `python3` through `/usr/bin` and `/bin`; those are aliases of
the selected installation, not two measured engines. No unversioned `python` was
found on PATH. No second candidate executable was found in the inspected usual
locations (`/usr/local/bin`, `/opt`, local-share search); this is not an exhaustive
inventory of home directories, containers, bundled apps or virtual environments.
Absolute executable and image hashes remove selection ambiguity prospectively;
shebangs, PATH, virtualenv selection or a debugger's embedded Python must never stand
in for that selection. In particular GDB's Python scripting runtime is not the target.

### Minimum admissible descriptor versus available pins

Retain the existing schema without extensions: `implementation`, `version`,
`build_sha256`, `abi`, `images`, `callable`, `interface_sha256`; image roles executable,
compiler and observer_native, each with `sha256` and authenticated `origin_sha256`.
Also freeze the independently retained bootstrap, observer and qualification artifacts
required by the expectation record. Build/interface descriptions must include these
exact image identities, the target entry/ABI and the loaded-image measurement method.
The same executable must appear in both executable/compiler roles.

The measured hashes above are candidate pins, **not a complete valid E**. Missing
origin evidence, exact source/build association and observer/bootstrap qualification
cannot be filled with local package names, this document's hash, empty values or an
invented digest. No expectation record or artifact store was created. No full native,
stdlib or package dependency closure was attempted.

## Concrete native receiving entry

Local primary evidence: actual executable bytes and disassembly; installed CPython
headers; symbol/relocation records in the installed static archive. No web source,
generic release tag or nearby debug image was substituted for this build. The installed
`/usr/src/python3.12` contains grammar/ASDL material, not the required bltinmodule
implementation source found by this search. The exact executable build-ID debug file
was absent. `nm -a` reports the executable stripped; dynamic exports do not name the
static builtin receiver.

Nevertheless the receiving address is recoverable without executing Python code:

1. `strings -t x` finds the builtin signature at executable file offset `0x383a40`,
   virtual address `0x783a40`:
   `compile($module, /, source, filename, mode, flags=0, dont_inherit=False, optimize=-1, *, _feature_version=-1)`.
2. A read-only binary scan for that doc pointer finds its PyMethodDef at file offset
   `0x648ae0`. The writable LOAD maps file `0x627dc8` to VA `0xa28dc8`, so this table's
   VA is **`0xa49ae0`** (not file offset plus the read-only segment bias).
3. Its four fields are name pointer `0x70bde7` (bytes `compile\0`), native function
   pointer **`0x69bff0`**, flags **`0x82`** (METH_FASTCALL | METH_KEYWORDS), and doc pointer
   `0x783a40`. `objdump -s` confirms those exact fields.
4. Installed `libpython3.12.a` has `bltinmodule.o` local symbol `builtin_compile` at
   section offset `0x410`. Its disassembly corroborates the executable entry's prologue
   and unpacking/conversion sequence; it is supporting evidence, not assumed byte
   identity between archive and linked executable.
5. Executable entry `0x69bff0` begins `f3 0f 1e fa` (endbr64). Its first instructions
   preserve/use the incoming vector. `_PyArg_UnpackKeywords` is called at `0x69c044`;
   filename conversion `PyUnicode_FSDecoder` at `0x69c067`; on the non-AST source path,
   `_Py_SourceAsString` at **`0x69c1c2`**, then `Py_CompileStringObject` at `0x69c1eb`.
   The first instruction is therefore before source conversion and argument unpacking.

The concrete boundary is the native Argument Clinic receiver conventionally named
`builtin_compile`, not a Python wrapper, not `Py_CompileStringObject`, and not an
assumed separately materialized `builtin_compile_impl`. Optimization can incorporate
implementation code into the receiver. Objdump's nearest-export label
`PyInit__tokenize+0x2230` at this stripped address is not the function's semantic name.

Python-level association to establish later: exact live `PyCFunction_Type` object
in the actual builtins module under `compile`; retained identical callable object;
`m_ml` referencing the expected method definition; `ml_meth` and flags matching the
entry. Native entry's first parameter is module/self, **not the callable object**,
so hitting the address alone cannot prove which retained builtin object was invoked.
A separate synchronized object/binding/dispatch association is essential.

The installed header's `_PyCFunctionFastWithKeywords` signature is
`(PyObject *self, PyObject *const *args, Py_ssize_t nargs, PyObject *kwnames)`.
For the System V AMD64 entry ABI, expected registers are RDI=self, RSI=args,
RDX=positional count, RCX=kwnames; this count is not a vectorcall `nargsf` value with
an offset flag. For the fixed call, RDX=6; args[0] is B, args[1..5] the other five
positional objects, and args[6] the value for the one keyword in kwnames. This is a
static decoder specification, not an implemented or dynamically validated decoder.

**Boundary confidence: high for the inspected image's static pre-conversion receiver;
unqualified for actual-process receipt/observer association.** These addresses are
build-specific coordinates, not stable cross-build interfaces or canonical identities.
No live builtin object, registers, mapping or source argument was observed.

## Offline observer candidates

No observer was attached, launched against an inferior, installed or implemented.
GDB package: `15.1-1ubuntu1~24.04.1`; `/usr/bin/gdb` SHA-256
`3832cc070ae1716e322105d3b39fb398695e5f031c9d39224cf227a8c2b889f6`.
`perf` and `strace` are on PATH; bpftrace and lldb were not found there or at their
usual /usr/bin names. Tool presence is not an operating qualification.

Local policy observations: Yama ptrace_scope=1, perf_event_paranoid=4,
unprivileged_bpf_disabled=2. This inspection process has CapEff=0, NoNewPrivs=1,
Seccomp=2. These do not prove that a future child trace will fail, but also do not
establish permission. Do not alter policy or infer privileges from a tool's presence.

| Candidate | Boundary and bytes | Independence / attempt / substitution | Offline, privilege, mutation and execution |
| --- | --- | --- | --- |
| GDB hardware execution breakpoint at exact first instruction | Concrete preferred design candidate. Can in principle stop before entry instructions and read registers/object memory. Independent external hashing can measure the read bytes. Full custom decoder/association procedure remains unqualified. | Must independently link the live callable, image, retained B, protected A and committed attempt; a bare breakpoint cannot distinguish equal-byte B substitution or another caller. Requires complete lifecycle/coverage and fail-closed handling. | Offline with debuginfod and auto-load disabled. Hardware support/slots and ptrace permission untested. No text patch with hardware breakpoint, but debug state and scheduling change. Memory inspection must never call inferior functions, pretty-printers or object methods. A later experiment runs native consumer machinery; no source/result execution is required by observation itself. |
| GDB software breakpoint | Same potential register/buffer access at corrected entry PC. | Same association requirements; trap restoration and resume behavior also need qualification. | Offline; same tracing limits. Patches the running code byte, so an unmodified on-disk hash cannot describe the entire observed state. Not selected; patch accounting would be additional work. |
| Direct ptrace supervisor / debugger API | Registers plus bounded process-memory reads can reach the same entry. strace by itself reports syscalls, not this user-space C receipt. | Could externalize decoder/hash and synchronization, but no qualified supervisor artifact exists. GDB/MI alone does not supply semantic qualification. | Offline, ptrace/LSM/seccomp restrictions apply; hardware or software stop required. New native tooling would need separate implementation authorization; none created. No candidate execution intrinsic to reads. |
| eBPF/uprobe or perf uprobe | Would need executable file offset `0x29bff0` for this text mapping, not blindly the VA or a libpython symbol; bounded user-memory reads could capture the vector and bytes. No such probe installed. | Needs correlation, type/object checks, lost-event detection, lifetime coverage and independent userspace hash. Hashing the expected payload in a harness is insufficient. | Current perf/BPF restrictions make unprivileged availability unestablished; elevated permissions likely needed. Uprobes generally instrument running instruction execution. No qualified BPF loader/decoder or bpftrace present. Offline possible in principle. |
| Native in-process instrumentation | A correctly placed native hook could read original entry arguments; a wrapper or LD_PRELOAD interposition on an unrelated exported compiler API cannot substitute. | Same-process trust and hook identity required; must not replace the consumer. No qualified hook exists. | Would require authorized build/patch/injection and freezing the actual altered artifacts. Not performed; no architecture change authorized. Native observer code runs, candidate code need not execute. |
| Python profile/audit/wrapper/monkey-patch | Insufficient for this native-receipt contract. | Cannot independently establish the complete original entry vector, actual control arrival, image/object association and same-attempt measurement merely from event names/caller logs. | Offline possible, usually no special privilege; wrappers/patches change binding. Running a hook is still observer code, and does not create a native receipt. Not used. |

**Selected qualified observer: none.** Preferred candidate for a later qualification
is external GDB with a hardware execution breakpoint at this exact image entry,
non-evaluating bounded memory reads and external hashing. That preference is not a
qualification or authorization to attach it. Installed GDB's own shared libraries,
auto-load scripts and debugger APIs were not treated as closed dependencies.

### Why Python-only observations are insufficient

`sys.setprofile` C-call notifications identify a callable event, not an independent
snapshot of the incoming native argument vector at its first instruction. The installed
`profile.py` dispatch code uses `arg.__name__` for c_call. It does not supply native
source registers, image association or full argument bytes. Caller frame inspection
cannot turn that into actual receiving-entry evidence.

An audit event named `compile` is not proof of this builtin entry: it can also be
emitted through other compilation routes or user audit emission. The executable has
an audit USDT probe, but it is not a dedicated builtin receiving-entry probe. Neither
event naming nor an audit source/filename pair establishes original B identity,
exact six-plus-one arguments, conversion ordering or the retained callable. Exact
build-specific audit placement has not been qualified here; do not silently promote
it to equivalent coverage. Python or native audit hooks alone are insufficient.

Wrappers record intent; monkey-patched observers can replace the expected callable.
Even a wrapper that later calls the real builtin cannot prove that call's actual
original receiving vector using only its own log. **Python-level observer verdict:
INSUFFICIENT**, without weakening the claim.

## Byte-observation and association contract for a future qualification

At a verified stop before the receiver executes conversions, an observer would need:

- actual args pointer, positional count and keyword tuple, decoded without running
  Python methods, repr, conversions, arbitrary pretty-printers or inferior functions;
- actual args[0] object address equal to retained live B, exact native type equal to
  this image's PyBytes_Type (exported VA `0xa2bee0`), and exact length 2;
- bounded direct reads of the bytes object and its two buffer bytes, full equality
  to `23 0a`, and SHA-256 independently calculated over **those observed bytes**:
  `32c4858e22cc2c967b42150fa550562a2c839c2cebcaab91cabdf6f4da020022`;
- independent protected-A association, seals/size and bounded complete read matching
  the incoming B, as required by the existing specification; knowledge of B alone
  does not prove its sealed origin;
- exact filename str `<ns001-h2a2-real-input-v1>`, mode str `exec`, flags exact int 0,
  dont_inherit exact bool true, optimize exact int 0, exactly one keyword named
  `_feature_version` with exact int -1; reject bool-as-int, extra/duplicate keywords,
  subclasses and coercion. Validate native layouts of strings, tuples, longs and
  booleans as well as bytes; decoding them is not implemented here.

For the installed non-Py_TRACE_REFS 64-bit header layout, candidate byte offsets are
ob_type +8, ob_size +16 and ob_sval +32. They follow PyObject_VAR_HEAD plus ob_shash;
they must be associated with the running image before use. The terminating NUL is
not a third payload byte. ob_shash is CPython's cached hash, **not SHA-256**. Addresses
are transient association evidence; exact reference identity cannot be replaced with
equal digest/length. Any unreadable object or incomplete read is refusal/abort.

The required chain is:

`frozen E -> measured process executable/mapped entry -> live builtin m_ml/target -> qualified attachment -> actual args[0] = retained B -> committed dispatch/attempt ID`.

A later supervisor must launch the absolute pinned executable with a frozen bootstrap,
control loader interposition and startup selection, keep process/thread identity
stable against PID reuse, verify executable and actual mapped entry association
(including file offsets/load bias and relevant live bytes), and freeze the observed
callable before arming. Disk hashes alone are not loaded-image evidence. The build is
ET_EXEC, but the method must still compute/verify mappings and must not assume that
all addresses or libraries are unaffected by ASLR.

Registration and durable ATTEMPTED must precede exactly one associated entry. The
observer must maintain lifetime/per-attempt counts, detect early/duplicate/missing
entries and observe completion or a separately qualified observer-stop. It must
recheck retained callable versus builtin binding and native target while the relevant
state is stopped/synchronized; the entry registers alone contain no callable object.
The stop must cover all relevant threads and prevent unobserved mutation during
measurement under the trusted-host assumption. No GDB inferior call is permitted.

Bootstrap compilation/import activity must finish outside the armed attempt interval;
its identity and coverage still require review. A second interpreter, a child or
embedded runtime must not consume the fixture while the observer watches another.
The future harness must independently enforce the specification's source/result
non-execution coverage and canonical witness ordering. A return value or successful
compilation is never the receipt. This review neither launches that bootstrap nor
claims those guards exist.

## Substitution risks and qualification gaps

| Risk | Required narrow treatment; current limitation |
| --- | --- |
| Alternate executable/environment | Absolute path plus prelaunch and actual-process image match; reject PATH/shebang/venv fallback. No live association measured. |
| Replaced executable/shared image or interposition | Hash expected image and associate mapped entry/loader behavior; installed libpython is not this target. Acquisition provenance and live checks remain missing. |
| Rebound builtins.compile | Exact retained object, actual builtins binding, PyCFunction type/m_ml/target and dispatch match; same function address alone insufficient. |
| Symbol mismatch | Freeze image hash and recovered method-table/entry coordinates; reject nearest-export labels, other builds or deeper compiler APIs. |
| Wrong process/function, PID reuse, ASLR | Supervisor-owned process lifetime, actual mappings and entry-PC validation, no address-only correlation. |
| Buffer/object substitution | Native source reference must remain the retained B and match independent A; equal bytes from a different object refuse. |
| Observer unavailable/replaced | Freeze observer/bootstrap identities, verify arming/coverage and fail closed; no profile/audit fallback. Current tracing permission and hardware breakpoint viability untested. |

Independent unresolved requirements are (1) authenticated engine acquisition and
version-matched source/build/interface provenance under the existing E contract,
(2) a reviewed concrete observer/bootstrap/decoder and live-image/callable/attempt
association artifact, and (3) evidence that its attachment mechanism is permitted
and effective in the intended local execution context. Static reverse inspection
reduces boundary uncertainty but does not discharge these requirements. No blanket
"trusted interpreter" assertion substitutes for them.

Residual assumptions even after such qualification would include honest host/kernel,
measurement tools and hashing; correct memory-read/ABI decoding; no hostile native
mutation outside controlled observation; reliable stopped-thread and journal ordering;
and separately reviewed harness non-execution control flow. These are conditional
synthetic-receipt assumptions, not cryptographic attestation or full runtime closure.

Full installation reproducibility, stdlib/package/import closure, complete native
library closure and runtime immutability remain dependency_runtime_lock obligations.
This review only measures candidate receiver/loader identities and describes the
necessary association. It begins none of that separate gate.

## Reproduction anchors and preservation receipt

Read-only inspection used `readlink`, `file`, `sha256sum`, `readelf`, `nm`, `objdump`,
`strings`, `dpkg-query`, bounded text/path searches, a Perl binary pointer scan, and
Git status/blob inspection. The pointer scan read binary data only, not Python source.
Static checks are reproducible from the image coordinates above. Supporting file pins:

| Local evidence file | SHA-256 |
| --- | --- |
| `/usr/lib/python3.12/config-3.12-x86_64-linux-gnu/Makefile` | `8aa2fc9e04721bd6ff24f8aa39013618cb16fb77b0572a5dfcb5e78da73a4de7` |
| `/usr/lib/python3.12/config-3.12-x86_64-linux-gnu/libpython3.12.a` | `6b97cc132cca12eb21f6a5f93ccff060677baf01a1fa567d735c64e0db3cc051` |
| `/usr/include/python3.12/cpython/bytesobject.h` | `5ba5010b9aa79f401196740da7c653590f5f4eec6b4f33e99de5412a969fcc8a` |
| `/usr/include/python3.12/cpython/methodobject.h` | `5beb9f3b68ac72efe403a1b0a3fbbb14a5606a49a2840b9c7e9ff243d82d79b9` |
| `/usr/include/python3.12/methodobject.h` | `059e19bd8d418c8bf1481e301340f989317ba7b56de94729a19aae26fee3da62` |
| `/usr/include/x86_64-linux-gnu/python3.12/pyconfig.h` | `23931f53bc7ee512c6bd3162828747494eaa5e21f23dd63b31170ec1adfbe65e` |
| `/usr/bin/sha256sum` | `4d2db56c867e5324e0084c9e897f6360d37517de77ac96f2bd31494223d69a60` |

These are measured local evidence references, not newly authenticated releases or
separate retained artifacts. Exactly this document is created. Before commit, all
215 pre-existing tracked files were compared byte-for-byte by Git blob identity with
HEAD before, including H2A1, both completed H2A2 slices (code/tests/fixtures/evidence)
and the real-boundary specification. The exact one-file staged diff and whitespace
check must pass. No completed slice is edited or tests rerun. Commit/push identity
and document SHA-256 are reported outside the document to avoid self-reference.

The operation record contains no candidate compile/eval/exec/import invocation,
Python candidate-source execution, runtime harness/client/scientific/E0 invocation,
observer attachment, installation or dependency-runtime work. The allowed -VV
administrative launch is explicitly disclosed above. This is an action-log receipt,
not a system-wide trace asserting that no unrelated process invoked Python.

## Closing qualification record

- candidate CPython installation: `/usr/bin/python3.12`, local CPython 3.12.3, Ubuntu package `3.12.3-1ubuntu0.17`.
- engine descriptor: executable/compiler SHA-256 `e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f`, ELF64 x86-64, SOABI `cpython-312-x86_64-linux-gnu`; candidate pins only, authenticated origin/build and complete E unavailable.
- native receiving entry: builtin_compile first instruction, image VA `0x69bff0`, file offset `0x29bff0`, method definition VA `0xa49ae0`, flags `0x82`; before unpacking/source conversion.
- native boundary confidence: high static identification on exact inspected image; live receipt/association unqualified.
- observer candidates: GDB hardware/software entry breakpoint, direct ptrace/debugger API, perf/eBPF uprobe, native instrumentation; Python hooks insufficient.
- selected observer, if any: none qualified; GDB hardware breakpoint preferred only for prospective qualification.
- Python-level observer verdict: INSUFFICIENT for specified real native receipt.
- byte-observation contract: actual vector/type/length/direct bytes/independent SHA-256, same retained B, independent sealed A equality, and exact six positional plus one keyword values/types.
- engine/observer association: frozen E -> actual process/mapped receiver -> live builtin/target -> qualified attachment -> actual source -> durable dispatch/attempt; specified, not observed.
- substitution risks: alternate engine/image/loader, rebound callable, wrong symbol/process, unstable address, replaced B, missing observer and environment-selected interpreter; fail closed.
- residual assumptions: honest host/kernel/tooling, valid ABI reads, synchronized state, artifact provenance and complete reviewed observer/guard coverage; no hostile-host or full runtime claim.
- qualification verdict: NOT_QUALIFIABLE on current retained evidence, with taxonomy limitation stated in the decision section.
- if PARTIAL, exact missing qualification: not applicable; multiple independent requirements remain unresolved, listed above.
- future implementation readiness: NO under the current qualification record.
- external_trust_root status: unresolved; real compiler input receipt unproven.
- dependency_runtime_lock status: unresolved and not begun.
- H2A1 status: unchanged scoped VERIFIED.
- H2A2 status: sealed handoff VERIFIED; surrogate consumption VERIFIED WITH RESIDUAL ASSUMPTION; both frozen unchanged; real boundary statically located only; all eight full gates unresolved.
- E0 status: HOLD.
- one next bounded action only: separately authorize one document-only engine acquisition/build-provenance evidence review for this exact executable hash; no observer attachment or experiment. Not performed here.
