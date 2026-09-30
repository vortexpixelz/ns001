# NS-001 H2A2 post-surrogate next scope v0.1

## Decision and authority

HEAD before: `d5cdc7ce090e3316e1af9dd03eb9ac774aae8e66`.
Branch: `codex/e0-h2-preparation`; initial working tree clean.
**Next-boundary verdict: READY_FOR_REAL_BOUNDARY_SPEC.** One isolated document-only
specification can be designed next for protected bytes reaching an identified real CPython
compiler input entry. A complete dependency_runtime_lock primitive is not a logical
prerequisite for that conditional, input-receipt-only claim. Actual engine association and
observer qualification are necessary inputs; neither has been established by this review.
Readiness here is for a specification, not implementation, compilation, gate closure or E0.

This review accepts the established slices and residual assumptions as supplied by the user
and the preserved independent re-review; it does not modify, rerun or re-review them:

1. Verified synthetic bytes → sealed same-object handoff: independently VERIFIED.
2. Protected bytes → immutable byte-preserving derivative → qualified non-executing
   surrogate receiving boundary: independently VERIFIED WITH RESIDUAL ASSUMPTION.

No full solution, new acceptance schema, implementation, fixture or experiment is created.
No candidate source was compiled, evaluated, executed or imported. No scientific/client/E0
path, network research, installation, runtime probe or dependency-lock work was performed.
The only network operation authorized here is the requested receipt-only Git push.

## Read-only evidence and its limits

Repository sources below are pinned by HEAD before. They were read as text:

- `preregistrations/e0/NS-001_E0_GETDATA_AMENDMENT_DRAFT.md`, structural controls: H1 source-file consistency is not loaded-code provenance; future H2 needs source-only bootstrap or externally verified read-only runtime, without bytecode substitution. The draft remains non-operative.
- `preregistrations/e0/NS-001_E0_INTERFACE_DECISION_DRAFT.md`: prospective GetData choice, not a selected client or production bootstrap.
- `e0/hardening.py`, module header, `_verify_running_source`, `LiveGetDataAdapter`: mock scaffold with no executable entrypoint; associated-file hashes do not prove compilation origin; live adapter refuses.
- `Dockerfile`, ENTRYPOINT; `run_experiment.py`, imports and `run`; `ns001_tau_check.py`, imports and retrieval: existing feasibility route starts Python with a script pathname, imports NumPy/scientific code, and can reach network retrieval. It is not an approved E0 launch route.
- `docs/e0/h2/NS-001_H2A2_READINESS_SCOPE_REVIEW_v0.1.md`, gate table; `NS-001_H2A2_RUNTIME_TRUST_ROOT_DESIGN_v0.1.md`, identity and gate maps; `NS-001_H2A2_EXTERNAL_TRUST_ROOT_NEXT_SCOPE_v0.1.md`, consumption/runtime-lock distinction: whole-gate obligations remain broader than input receipt.
- `NS-001_H2A2_CONSUMPTION_BOUNDARY_IMPLEMENTATION_REREVIEW_v0.1.md`, disposition only: inherited completed-slice status, not a new implementation assessment. SHA-256 `b29c4f0409d07f0b49743c1401f193e43c7fac5f263625766811435f95ef1fcc`.

Supplemental local interface text, not an authenticated engine release or a measured runtime:

- `/usr/lib/python3.12/importlib/_bootstrap_external.py`, lines 989–995 and 1054–1149; SHA-256 `97c6211750d63067712ad2cd74d50be33337f1fb1cd2c769022ced9b401edd92`.
- `/usr/include/python3.12/compile.h`, SHA-256 `1f10c818b29007e6a4446505a1140dd77ca6618ad81e87b502f4b274406`.
- `/usr/include/python3.12/cpython/compile.h`, flag/type declarations; `/usr/include/python3.12/cpython/pythonrun.h`, separate compile and run declarations.
- `/usr/include/python3.12/cpython/sysmodule.h`, audit-hook declarations; SHA-256 `d4936db24692cccadb19c11accda260787f95e5658f88cfc752d9a49344ee051`.

The loader source explicitly calls `compile(data, path, 'exec', dont_inherit=True,
optimize=_optimize)` from `source_to_code`. Its `get_code` can instead select cached bytecode,
and `exec_module` separately invokes execution. The headers distinguish compiler interfaces
from run interfaces and show that an audit-hook API exists. They do NOT prove where a compile
audit event occurs, which argument object it exposes, or its coverage/ordering. Version-matched
native implementation and authoritative interface evidence are still required by a future
specification. No online source or candidate engine was fetched or invoked to fill that gap.

## Answers to the twelve scope questions

### 1–2. Actual candidate interface and the surrogate-to-real gap

No production E0 source-consuming API has yet been selected/implemented by the inspected
drafts. The concrete candidate for the next specification is the **bytes source argument at
entry to the real `builtins.compile` callable in a specifically identified CPython build**,
with explicit filename/mode/flags/inheritance/optimization arguments. The existing six-argument
surrogate models this interface shape; it does not provide evidence that a native compiler
received anything. This recommendation does not select a production E0 launcher.

`SourceLoader.source_to_code` is a concrete documented-in-source adapter to that compiler;
using `get_code`, ordinary import or `exec_module` introduces wider source selection/cache or
execution semantics. The direct bytes compiler entry is therefore the smaller boundary to
specify. C `Py_CompileString*` APIs are possible downstream interfaces but use a different
buffer/parameter contract and cannot silently replace the bytes-object boundary.

The established surrogate ends at a Python function call observed through that function's
frame/code reference. The real builtin's native entry, engine association, input conversion,
and observer semantics are unproven. There is no surrogate frame/code-object proof that
transfers automatically to a native builtin. A wrapper's frame only proves wrapper receipt.

### 3. Narrow permissible claim

A future successfully qualified and accepted circuit could state:

> Within the specified offline synthetic scope and declared trusted-host/observer assumptions,
> the identified CPython compiler callable received the exact protected byte derivative as
> its source argument at the qualified input entry, bound to this attempt.

Here “consumed” means received at that entry, not every byte parsed, compilation succeeded,
generated code corresponded correctly, or generated code executed. Native decoding/parser
transformations are beyond this exact original-byte entry claim. This is meaningful because
it replaces a stand-in receiver with evidence at a real source-processing component, closing
one source-substitution gap. It proves no scientific result, production client identity,
compiled-code provenance, runtime integrity, full external_trust_root or E0 readiness.

### 4–5. Minimal engine identity versus runtime-lock obligations

Minimum narrow-claim identity must include the selected CPython implementation/version/build
and ABI/configuration relevant to the input and observer interfaces; retained authenticated
origin and exact digests of the executable and compiler-bearing image (including libpython
where applicable); the actual process/loaded-image association at the observed call; identity
and association of the native compile callable; and pinned observer/bootstrap artifacts and
qualification evidence. A file found on PATH, version string, module name, self-reported hash,
or hash of a file unrelated to the loaded mapping cannot establish that association.

Native code that implements/interposes on the selected entry or witness cannot be left
unidentified while claiming that entry was identified. The future specification must state
how association is measured and which host/loader/measurement honesty assumptions remain.
It must not substitute “the interpreter is trusted” for all actual engine association facts.
These are bounded consumer-identity requirements for this edge, even though some identity
artifacts may later be reused by dependency_runtime_lock. They are not evidence of complete
runtime closure, immutable execution throughout, or reproducible installation.

The separate gate owns complete transitive stdlib/package/native/plugin/loader dependency
closure, all artifact hashes and platform variants, immutable runtime, reproducible network-
blocked installation, and proof that later imports/execution resolve only to that closure.
Build-tool and environment closure needed for those stronger guarantees remains there too.
No production packages need be installed or scientifically exercised to design input receipt.
An influential component either needs narrow qualification or an explicit residual trust
assumption; silently omitting it is not a legitimate way to isolate the scope.

Thus a full lock is not required before designing this narrow specification. If later work
seeks an unconditional claim against a compromised interpreter/loader/host, the current
trust assumptions no longer suffice; completing a dependency lock alone would not prove
observer honesty against that adversary either. That stronger objective is not chosen here.

### 6. Independent actual-entry observation

Feasible in principle without scientific-source execution: a separately qualified observation
at the real native receiving boundary can measure the actual argument bytes and associate
entry, engine and attempt. It must be independent of caller intent and compiler output.
This is a scope feasibility judgment, not a measured observer qualification.

A Python wrapper log or a reported return/code object is insufficient. Neither an ordinary
C-call notification alone nor an event named `compile` should be assumed to expose the exact
original argument. An engine-originated audit event is only a candidate if retained native
source and interface evidence establish its location, actual argument representation,
conversion history, coverage and refusal behavior. A hook that receives transformed data
cannot certify original B reference identity without an independently established link.
A forgeable same-named event is not authenticated native entry merely because its label
matches. Qualified native-entry instrumentation is another possible observation family;
this receipt does not select, implement or validate a hook/instrumentation design.

The next specification can resolve that local observer choice using version-matched primary
evidence and explicit fail-closed qualification requirements. No missing fact currently forces
a choice of full dependency-runtime closure instead of the compiler-entry boundary. If that
specification cannot qualify an observer, it must remain unaccepted rather than infer receipt.

### 7–9. Inert input and compilation versus execution/authorization

A separately specified tiny comment-only or empty ASCII source can exercise the real bytes
compiler interface without importing or executing scientific source. Such a fixture is a
future new profile, not a replacement for the frozen `abc` fixture. It must have its own
explicit byte identity. `abc` is inert data in the completed surrogate, but if interpreted as
Python it is a name expression; the frozen receipt does not authorize that reinterpretation.

Calling real `compile` normally performs compilation (or fails while attempting it) and
may return a code object; it does not itself execute that code object's statements. The
`'exec'` mode names the compilation grammar, not an instruction to call `exec`. Compilation
still executes compiler/observer machinery, may emit audit events, and has resource/failure
behavior. “No scientific execution” must not be described as “no runtime activity.”

It is possible in principle to refuse/abort at a qualified entry observation before later
compiler work, but that depends on the selected native hook's proven placement. It would
establish entry receipt only, not parsing or successful compilation. This review does not
claim that the available local audit interface provides such a boundary. The next scope
should budget explicitly for real compilation of inert input if the call proceeds; it must
not promise a compilation-free normal invocation or misuse SyntaxError as entry proof.

Actual compilation is **outside this document-only authorization and the frozen non-executing
surrogate circuit**. No such invocation is performed now. It is not inherently beyond the
conceptual external_trust_root input-receipt claim: a separately authorized synthetic circuit
may compile while claiming only witnessed input receipt and leaving output/execution unproven.
That future authorization must explicitly allow inert compilation and prohibit evaluation,
execution/import of generated or scientific code. Selecting this scope grants no such authority.

### 10. Evidence distinguishing intent from actual receipt

Intent evidence says a wrapper selected B or planned a call. Actual receipt evidence must
bind protected A and retained B, independent byte length/SHA-256 and equality/reference facts
at the qualified real entry, actual arguments and call count, the actual engine/callable
association, observer identity and source-supported observation semantics, and the same
reserved attempt after committed dispatch. Missing/mismatched/cross-attempt observations
must not be replaced by output success. The frozen earlier receipts supply upstream claims,
not fresh live A/B capabilities or real-engine entry evidence for a new attempt.

These are evidence categories for the next scope, not a new protocol/schema or acceptance
matrix. Runtime honesty and storage/custody assumptions must remain explicit in any result.

### 11. Relevant substitution channels

Relevant channels include executable PATH/symlink replacement; loaded libpython or native
interposition/loader search; rebinding/shadowing of `compile` or an adapter; buffer/reference
substitution and implicit text/encoding conversion; altered filename/mode/flags/optimization
or inherited compiler flags; script/stdin/module source selection; payload pathname reopen;
source-loader cache/stale pyc or prebuilt code/AST alternatives; startup site/customization,
PYTHONPATH/PYTHONHOME/cwd/import hooks; and disabled, replaced, spoofed or cross-attempt
observer evidence. A direct bytes call can exclude many source-selection routes from that
specific delivery path, but does not prove their absence throughout the interpreter.

Compiler-input policy and bootstrap/native identity must account for channels affecting
this boundary. Imported scientific modules, later callbacks/plugins and global runtime
closure remain unproven and out of scope. Guarding a declared path is not a sandbox claim.

### 12. One isolated next circuit

One next circuit is a **document-only real-CPython bytes-input boundary specification**,
limited to engine identity/association, qualified receiving-entry evidence and inert-input
compilation-versus-execution limits. It must retain scope assumptions, source-supported
observer qualification and refusal on missing facts. It must not design a full runtime lock,
select/import a scientific client, implement a launcher or run acceptance. Obtaining/retaining
any missing external primary material requires appropriate separate authorization; no network
research is implicitly granted by this receipt. The specification itself is not written here.

## Preservation and closing disposition

Pre-commit byte comparison against HEAD before confirmed all 213 pre-existing tracked files unchanged,
including both frozen slices, their implementation/tests/contracts/receipts, H2A1 and scientific
artifacts. Only this new receipt is eligible to change or be committed/pushed. No other file is
repaired or reclassified. Administrative text/hash/Git/data operations are distinct from any
candidate-source compiler/runtime invocation. HEAD after is the receipt-only commit reported
in the final response; no self-containing commit hash is embedded here.

- established boundary: both frozen synthetic slices accepted as supplied; sealed handoff VERIFIED, qualified surrogate receipt VERIFIED WITH RESIDUAL ASSUMPTION.
- next adjacent boundary: protected immutable bytes → identified real CPython compiler receiving entry, conditional and synthetic only.
- actual candidate Python interface: real `builtins.compile` bytes source input; no production E0 entrypoint selected.
- surrogate-to-real gap: native engine/callable association, real argument representation and qualified native-entry observation.
- narrow permissible claim: same-attempt witnessed exact-byte receipt at identified compiler input; no output or execution claim.
- minimum engine identity: retained exact executable/compiler-bearing image/build/interface and live association, native callable, observer/bootstrap identity with explicit trust assumptions.
- runtime-lock obligations: complete transitive immutable dependency/native/stdlib/platform closure and reproducible offline installation remain separate and unproven.
- independent observation feasibility: feasible in principle without scientific execution; native observer semantics/qualification not yet established.
- inert real-boundary feasibility: yes prospectively with a separately specified inert fixture and explicit authorization; no probe performed.
- compilation/execution distinction: normal compile invokes compiler machinery without executing generated statements; inert compilation needs separate authorization and does not itself require a full runtime lock.
- substitution channels: engine/native-loader/callable, buffer/conversion/flags, path/cache/import/startup/environment and observer/attempt substitution.
- next-boundary verdict: READY_FOR_REAL_BOUNDARY_SPEC; not ready for implementation or invocation on this receipt.
- external_trust_root status: unresolved; no actual compiler receipt established here.
- dependency_runtime_lock status: unresolved and unstarted by this circuit; not a full-gate prerequisite to the narrow specification.
- H2A1 status: unchanged VERIFIED for scoped prospective custody/publication auditability.
- H2A2 status: completed slices frozen and unchanged; next real boundary unproven; all eight full H2 gates unresolved.
- E0 status: HOLD.
- one next bounded action only: separately authorize one document-only real-CPython input-boundary specification within the limits above; not performed.
