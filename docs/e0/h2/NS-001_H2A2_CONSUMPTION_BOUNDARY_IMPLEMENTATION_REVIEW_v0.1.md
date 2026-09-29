# NS-001 H2A2 consumption-boundary implementation review v0.1

## Basis and decision

HEAD before: `bb777737fcbfbbd2fd240174893a966826255bc0`.
Branch: `codex/e0-h2-preparation`; initial working tree clean.
Independent review turn: no implementation changes, repair, acceptance rerun or next slice.
**Implementation-slice verdict: PARTIAL.** The retained bounded runs support the surrogate
receiving-boundary result, but recovery/lifecycle enforcement does not fully implement the
frozen contract. Three blocking findings below prevent whole-slice verification.

Reviewed implementation scope only:

- `e0/h2/consumption_boundary.py` (I).
- `tests/test_e0_h2_consumption_boundary.py` (T).
- `docs/e0/h2/NS-001_H2A2_CONSUMPTION_BOUNDARY_IMPLEMENTATION_RECEIPT_v0.1.md` (R), including its embedded evidence as data.

Normative comparison: consumption-boundary ACCEPTANCE_SPEC, SPEC_CORRECTION and
SPEC_REREVIEW v0.1 in this directory. The specification hash is
`7757f0d7fb8c8f27d2c7516e68c065ea4313b3fd8f013f6674a1e2c5f81799b6`.
I and T match the archived final source bytes exactly, respectively:
`a8e6688dc6e72b9c1ee95eee4f95a74256ca1be231be07202dfe29343c7fa91b` and
`6736cdef976fb53ef7a581152133dc2ecd83a12d094848d4ab2751e1bd7d32cf`.
Other tracked files were compared for preservation only, not substantively reviewed.

Method: source/control-flow inspection and independent standard-library data decoding,
SHA-256, JSON serialization, record/link/count checks. Neither I, T nor archived code was
imported or executed. No acceptance harness, surrogate receiver, scientific module, real
compiler/runtime/client path or E0 was invoked. Administrative Python handled data only.
Git push is the separately authorized repository transport, not test/client traffic.

## Blocking findings

### F1 — existing-store custody loss is silently reconstructed (B1)

I:164–174 writes missing `store.json` and the expected-descriptor file from caller inputs,
without distinguishing a fresh empty store from an existing store containing reservations.
Reopen an existing retained store whose descriptor is absent: the constructor recreates it
before recovery, and existing attempts are evaluated against the caller's E. A missing
namespace record is likewise recreated. No custody stop or missing-E recovery fact survives.
This is a static control-flow counterexample, not an executed deletion experiment.

Specification sections 5 and 10 require lost/conflicting custody to stop, and unavailable E
to remain a refusal/recovery fact rather than current-host auto-approval. This finding does
not demand adversarial rollback detection or stronger filesystem assumptions: it concerns
an observable missing file in a nonempty store. Tests only reopen a complete store and do
not cover this path. New-store initialization itself is legitimate; unconditional recovery
of missing custody inputs in a nonempty store is the defect.

### F2 — complete invalid registration can escape ABORTED classification (B1/B2)

I:258–266 parses registration, calls `set(registration)`, and catches only ValueError.
A complete canonical registration containing `null\n` or `1\n` passes generic canonical
parsing, then raises TypeError at `set(registration)`. No ABORTED/RECORD_INVALID record is
produced. The frozen contract requires complete structurally invalid retained records to
receive that deterministic disposition. The process fails closed with respect to dispatch,
but an uncaught exception does not satisfy the specified retained recovery classification.

This conclusion follows directly from the source and Python builtin type semantics; the
implementation was not executed. The retained N18 cases corrupt witness IDs, so their
success does not cover malformed registration root types.

### F3 — ABORTED does not close the live Attempt event writer (B1)

I:219–238 enforces only the object's in-memory ACCEPTED/REFUSED states. Recovery writes a
separate ABORTED record (I:319–343), but neither marks the existing Attempt object terminal
nor makes `Attempt.event` check that record. For the same process's controlled PREPARED
interruption (as used in T), after recovery returns ABORTED, the retained Attempt object
still permits `event('ATTEMPTED')`; the ordinary invocation path can subsequently dispatch.
Similarly an empty recovered reservation's original Attempt can append PREPARED. This
changes the journal after recovery and defeats ABORTED-as-terminal at the writer boundary.

The supplied harness does return immediately from these interruption cases, so none of the
37 retained cases demonstrates resumed consumption. A later recovery would detect a
conflict, but only after the forbidden append/possible dispatch. This is a latent lifecycle
enforcement gap, not evidence that the preserved run consumed again or that restart itself
silently promoted an incomplete chain. The frozen contract prohibits resumption after ABORTED.

No repairs or counterexample executions were performed.

## Scope, identity and receiving witness

**Scope PASS.** Fixed payload is inert `abc`; negative candidates are short/long/altered or
mutable inert bytes. `receive` has six positional-only arguments, no defaults/callbacks,
and only exact type/value checks and a fixed tuple return. No supplied source is evaluated,
executed, imported or compiled. `mode='exec'` is metadata. T's pre-arm bootstrap loads the
reviewed implementation/support; its AST inspection parses implementation source, not payload.
The armed audit hook denies compile/exec, network and process-launch events. This is not a
proof of bootstrap authenticity or of all historical host activity.

**B3 PASS within trusted bootstrap.** T verifies external implementation/harness pins before
loading, and records the shared consumer/observer artifact separately from the harness.
Live receiver/function code references are retained and compared by qualification, invocation
and profiling. Fixed entrypoint/interface/parameter policy and request environment/channel/cwd
checks enforce the surrogate route. The loaded test alias is associated with the reviewed
artifact-relative receiver name by the explicitly trusted bootstrap. Wrong and rebound
callables are exercised. No executable hash, package closure or dependency_runtime_lock
requirement is introduced. The real/unknown profiles refuse; real-engine qualification is
unproven. Artifact checking here means the pinned bootstrap/run, not a standalone guarantee
for arbitrary callers passing unchecked hashes into low-level helpers.

**B4 PASS for retained bounded attempts.** Monitor.profile observes the retained receiver
code's call frame before its body. Witness.entry measures actual source type/length/SHA-256,
compares the retained B reference, separately measures/reads A and compares actual bytes,
checks parameters and records dispatch/arming. Return linkage uses the observed frame.
The positive sequence is protected, derived, qualification, armed, dispatch, entry,
protected, return, end. Successful dispatch references the synchronized ATTEMPTED event;
terminal records hash the separate same-attempt witness. A/B remain live and kernel seals
are checked. Volatile references/FD/inode values are used live, not serialized as identities.

**Witness independence VERIFIED WITH RESIDUAL ASSUMPTION.** The fixed receiver cannot create
a witness through its six data arguments or returned tuple. Measurement and stored state
are in separate observer/supervisor functions. Missing entry evidence despite fixed return
refuses. This is independence within the frozen honest harness/interpreter/profiling/process
assumption, not isolation from arbitrary hostile Python, a compromised observer or kernel.

The guard actually records and denies the test adapter's reopen/fallback request before I/O;
it does not call an uncontrolled path to demonstrate denial. The altered decoy is created
by the harness but not consumed. Fixed post-sealing delivery has no pathname source fallback.
This is exactly the bounded trusted-program assumption, not general syscall interception.

## Refusals and retained attempt inventory

**B2 PARTIAL overall because of F2; normal-path precedence PASS.** CODES supplies the frozen
rank; deduplication/rank sorting yields one primary and remaining ordered diagnostics.
Preparation stops at the first failed phase. Post-binding substitution is not relabelled
initial-object failure. The combined case has PATHNAME_REOPEN primary and
OBJECT_SUBSTITUTION diagnostic. Recovery classifications are separate from normal REFUSED.
Fault adapters change actual candidate/request/reference/observation state before evaluation;
they are not merely assertions of desired refusal codes.

Decoded R's archive strictly as data: 420 files, uncompressed JSON 453969 bytes, SHA-256
`ad3248f21e1e925fe4007b51183b00fc42f61c3526e27875a09343544a9a4c0c`;
gzip SHA-256 `079bcc12809e0abe7597448d9a6a99f5b1b825646071f52b97ade140393fe78a`.
Final summary hash matches
`7b461fdf0d64d2b42edbb9f919543165f545887caf9ce25a0f5b110151b165de`.
Counts were recomputed from the final store's actual terminal journals/recovery records,
not accepted from summary fields or receipt prose:

| Ordinals | Retained outcome / exercised condition |
| --- | --- |
| 1–2 | 2 ACCEPTED, separate P01 IDs |
| 3–8 | Wrong initial A; short derivative read; truncated/appended/altered/mutable candidates |
| 9–11 | Post-admission A; changed B; equal-byte different B |
| 12–15 | Denied reopen; wrong/rebound receiver; premature entry |
| 16–20 | Missing entry; wrong dispatch hash; denied fallback; zero/two invocations |
| 21 | Combined reopen plus object substitution |
| 22–26 | Wrong parameter; PYTHONPATH/PYTHONHOME; stdin; wrong cwd policy |
| 27–29 | Missing candidate expectation; real and unknown profiles |
| 30–34 | ABORTED: registration/PREPARED/ATTEMPTED/torn-journal/empty reservation |
| 35–36 | ABORTED/RECORD_INVALID: wrong-ID and cross-attempt witness |
| 37 | ABORTED: interrupted recovery write and reopening |

Final inventory: **2 ACCEPTED + 27 REFUSED + 8 ABORTED = 37**. Each summary terminal digest
matches its actual retained disposition. Normal terminal witness hashes/attempt IDs and
journal predecessor hashes match. Recovery raw registration/request/witness/journal hashes,
journal lengths and prefix digest bindings match retained bytes. Wrong-ID evidence is kept
raw, not normalized into valid witness evidence. Case 37 retains the actual 37-byte partial.

**Substitution defense PASS for the requested bounded cases.** The table covers every listed
family. Wrong witness binding becomes ABORTED/RECORD_INVALID, whereas wrong dispatch or
missing observation becomes normal OBSERVATION_MISSING. These counts do not imply that
every possible schema corruption, custody loss or resumption is covered.

## Determinism and restart

**Determinism PASS for canonical data and frozen repeat criterion.** I's canonical serializer
rejects non-printable/non-ASCII strings and unsupported types; parsing rejects duplicate keys
and noncanonical byte encodings. Independent reserialization of the final store's complete
JSON/JSONL lines reproduced **174** byte-identical records. Torn tails and `.partial` are
intentionally excluded from this complete-record count and separately bound by raw hashes.
Canonical encoding is not schema/semantic validity: wrong-ID witness records also serialize
canonically. The check is meaningful encoding evidence, not a universal validity proof.

The two positive witnesses compare equal after removing only attempt_id and its derived
ATTEMPTED-event hash. IDs and full terminal bytes remain distinct. No timestamps, process
IDs, FD/inode numbers or temporary paths appear as volatile canonical identity fields.
Expected hashes/namespace are frozen custody inputs. The tests compare actual records,
although the summary's positive_count is a literal 2; this review independently counted it.

**Recovery behavior PARTIAL.** The retained examples and inspected harness demonstrate
reopening, terminal preservation, raw-tail retention, prefix completion and repeated recovery
without rewriting originals. The interrupted write test performs an actual partial write
and controlled exception, not a power loss. Existing recovery-byte equality returns the
same disposition; conflicting bytes and invalid partial prefixes stop by code inspection.
Those latter conflict branches are not independently exercised by the retained tests.
F1–F3 prevent a universal lifecycle/recovery PASS. No completed retained attempt is shown
to have been silently promoted from incomplete evidence by the supplied run.

## Receipt accuracy and claim boundary

R accurately reports final pins, archive encoding/hashes/file count, 37-case inventory,
174 round trips, positive semantic equality, bounded substitution outcomes and the 37-byte
recovery partial. Archived initial-run summary/source pins corroborate its 2/25/7 inventory;
initial and final source identities are separate. Code supports its described receiver,
observer, sync ordering, guarded source selection and absence of payload execution paths.

R's broad recovery/implementation PASS must be qualified by F1–F3: the retained matrix passes,
but it does not establish full contract correctness. Statements about original process exit
0, absence of any omitted failed development run, and the reported historical SyntaxWarning
are historical assertions, not independently authenticated by retained records alone. This
review does not turn them into independently observed process history. Prior preservation
claims are corroborated by the implementation commit's three-file scope; present preservation
is independently checked below. No archival data is treated as cryptographic witness honesty.

**Receipt accuracy PARTIAL:** concrete retained outcomes verified; general implementation
PASS is too broad given the findings. **Claim-boundary compliance PASS:** R explicitly keeps
the real engine, runtime/dependency integrity, full external_trust_root and E0 unresolved.
The strongest supported positive-result wording remains:

> Within the frozen synthetic offline surrogate scope, exact protected bytes were bound to and independently witnessed at the qualified surrogate receiving boundary.

That describes the retained positive attempts under the frozen trust assumptions; it does
not override the PARTIAL implementation verdict. No actual Python compiler consumption,
successful source compilation, runtime/dependency integrity or E0 readiness is established.

## Verdicts and preservation

- implementation correctness: PARTIAL; three blocking lifecycle/recovery findings.
- B1: PARTIAL (F1–F3); retained ordering/normal terminal examples pass.
- B2: PARTIAL (F2); normal refusal precedence and exercised cases pass.
- B3: PASS within frozen trusted-bootstrap assumptions.
- B4: PASS for bounded receiving-entry witness.
- witness independence: VERIFIED WITH RESIDUAL ASSUMPTION.
- substitution defense: PASS for the frozen bounded cases.
- recovery behavior: PARTIAL.
- determinism: PASS for frozen encoding/repeat rules.
- receipt accuracy: PARTIAL, as qualified above.
- claim-boundary compliance: PASS.
- blocking issues: F1, F2, F3; none repaired.
- implementation-slice verdict: PARTIAL.
- external_trust_root status: unresolved; real compiler boundary unproven.
- H2A1 status: unchanged, inherited VERIFIED for scoped prospective custody/publication auditability; not re-reviewed here.
- H2A2 status: first slice unchanged, inherited independently VERIFIED; consumption slice PARTIAL; all eight full gates unresolved.
- E0 status: HOLD; no execution authorized or performed.
- next bounded action: obtain explicit authorization for a repair-only circuit addressing F1–F3 and bounded regression evidence; not performed.

Before commit, all 210 previously tracked files compared byte-for-byte equal to HEAD before;
Git status showed only this new review receipt as changed. This covers I, T, R, H2A1 and the first
H2A2 slice. No runtime/compiler/client/scientific/E0 path was executed during this review;
no dependency_runtime_lock work began. Commit/push scope is this receipt alone. HEAD after
is the commit introducing this receipt; the final response records its resolved identity
and observed push result without embedding a self-referential commit hash.
