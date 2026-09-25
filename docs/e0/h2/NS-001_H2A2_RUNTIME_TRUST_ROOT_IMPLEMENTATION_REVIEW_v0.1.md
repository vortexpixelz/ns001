# NS-001 H2A2 runtime trust-root implementation review v0.1

## Basis and disposition

Branch `codex/e0-h2-preparation`; reviewed HEAD
`496f21ea7759adbe63826730bb58518f6a0a2dde`; initial working tree clean.
Review subjects, with all source-line references pinned to that commit:

- `e0/h2/runtime_trust_root.py` (implementation, abbreviated I).
- `tests/test_e0_h2_runtime_trust_root.py` (harness, abbreviated T).
- `docs/e0/h2/NS-001_H2A2_RUNTIME_TRUST_ROOT_IMPLEMENTATION_RECEIPT_v0.1.md` (receipt, R).

Comparison authorities are the frozen snapshot-handoff acceptance specification and
handoff-mechanism selection receipt in this directory at the same commit. Their bytes
are unchanged. This is an independent review turn, not an independent organization or
security principal. Only this new review receipt is changed.

**Implementation-slice verdict: PARTIAL.** The normal sealed-object path and the preserved
80-case results support useful bounded evidence, but full frozen-contract conformance is
not established. B1 is an input-identity acceptance defect, B2 is a refusal-code defect,
and B3 is an independent-evidence acceptance/coverage gap. They block endorsing the whole
slice as VERIFIED. None demonstrates a successful write through a correctly sealed memfd.
Do not discard or rewrite the historical passing observations; retain their narrower scope.

## Blocking findings

### B1 — BLOCKING: short acquisition reads can accept an oversized input

I:129–136 checks opened-file metadata against the initial metadata, then returns one
bounded read without checking that the bytes returned cover the file. I:195–200 checks
only the returned payload length/hash and unchanged before/after metadata. A file size
other than three is not itself rejected. I:145–146 similarly bounds the returned manifest
buffer, not the manifest file size recorded during acquisition.

Concrete source counterexample: metadata consistently reports size 4 for source.bin;
the four-byte read returns only the first three bytes, abc. The metadata comparisons
succeed, len(payload) is 3, F matches and acquisition returns abc. The frozen original-file
identity requires exactly three bytes, not just a matching read prefix.

Concrete manifest counterexample: metadata consistently reports manifest size 2048;
the bounded read returns only the exact 150-byte canonical manifest prefix. MANIFEST_SIZE
checks 150 and the canonical/hash checks pass, despite the input file exceeding the frozen
1024-byte acquisition limit and containing unconsumed bytes. The before/after size can
remain unchanged and still satisfy the implementation's stability comparison.

This review reproduced both paths using the unmodified `_acquire` and `_read_member`
functions with in-memory doubles for filesystem operations. There was no real kernel
short-read experiment, fixture file creation or memfd creation. The doubles represent a
short read from a file whose actual metadata is larger; they do not simulate broken sealing.
Observed output:

```text
oversize-source-short-read ACQUISITION_PASSED 616263 metadata_sizes 4 150
oversize-manifest-short-read ACQUISITION_PASSED 616263 metadata_sizes 3 2048
```

Reproduction inputs: Root('/synthetic-review-root', 10, (1,10), True); synthetic root inode
10, source inode 11, manifest inode 12 on device 1. Files are regular, single-link with
constant mtime/ctime. `_walk` returns 10; fd-relative stat/list/open return those objects;
`read(source,4)` returns abc and `read(manifest,1025)` returns the frozen manifest. The
first case reports source/manifest sizes 4/150; the second reports 3/2048. Close is a no-op.
These are review-only I/O doubles, not edits or new test files.

N03 and A-oversize exercise normal full reads, so they do not expose this gap. A later
bounded correction must reject inconsistent/incomplete acquisition and enforce the
actual frozen sizes/limits without repairing a read. Add these two boundary cases;
this is not a request for general fuzzing. No such correction was made here.

### B2 — BLOCKING for exact conformance: short memfd read has the wrong refusal code

I:209–216 maps every size/read-length inequality to MEMFD_COPY_SIZE. With fstat size 3
and pread returning two bytes, `_copy_check` raises MEMFD_COPY_SIZE. The mechanism receipt
section 5 gives MEMFD_COPY_IO first priority for an error/short write **or read**.

An in-memory reproduction of the unmodified function confirmed:

```text
memfd-short-read MEMFD_COPY_SIZE contract_expected MEMFD_COPY_IO
```

This remains a refusal, not false ACCEPT or a sealing bypass. T:461–464 tests short/error
writes only; it does not test the specified short-read branch. A future correction must
distinguish a short read of a correctly sized object from a wrong object size and preserve
the frozen code ordering. No mechanism redesign is needed.

### B3 — BLOCKING for complete acceptance evidence: N31 tests a different omission

The frozen specification requires EVIDENCE_INCOMPLETE when the independent handoff
observation is missing; its section 9 rejects a bare self-reported observation flag.
The mechanism receipt likewise requires independently checked association evidence and
harness-supplied reference binding before acceptance.

I:279–303 creates reference_bound=true and the checks/call-count fields from the candidate's
successful control flow. `_receipt` receives pins and two role-result dictionaries, but no
separate harness observation. T:219–224 receives a canonical ACCEPT from `run` first, then
checks the external Trace with assertions. Those assertions are valuable and prevent a
failed positive test from entering the final successful aggregate report. They do not
convert missing independent evidence into the required canonical EVIDENCE_INCOMPLETE.

T:382–385 (N31) instead substitutes None for the observer-result dictionary passed to
`_receipt`, after both actual roles and trace observations have run. This checks a missing
role-result argument, not loss of creation/duplication/association observations in Trace.
Therefore N31's passing result is not evidence that the stipulated independent-observation
omission is correctly handled.

Specific untested boundary: preserve both role results but omit the external association
observation. Candidate record construction is unaffected; subsequent `Trace.positive()`
assertions fail rather than producing the required stable refusal. This follows directly
from the data flow; no implementation was modified to run an adversarial variant here.

The future correction must make the independent evidence check a condition of final
acceptance and exercise that actual omission while keeping role results intact. It must
not merely rename a role result as independent evidence. This finding does not assert
that the preserved successful runs lacked observations: their Trace records do contain
creation, duplication and association evidence.

## Remaining review findings and verified scope

| Area | Classification | Evidence and limit |
| --- | --- | --- |
| Implementation boundary | VERIFIED | I imports standard data/descriptor primitives; no client/scientific imports, eval/exec, compiler, subprocess or network calls. Payload is hashed, never parsed as scientific input. Only manifest JSON is parsed. No source pathname open occurs after acquisition. |
| Memfd/sealing | VERIFIED WITH RESIDUAL ASSUMPTION | I:23–25, 219–234, 341–358 selects sealing-enabled creation, copies/re-hashes bytes, applies all four seals in one call, queries exact Q and re-hashes after sealing. No mapping or mutable-file fallback exists in the positive path. Trust in the kernel is retained. |
| Same-object delivery | VERIFIED WITH RESIDUAL ASSUMPTION for the preserved positive path | I:306–330 duplicates A directly for C/O and retains all references. I:237–246 checks live device/inode equality, Q, type and CLOEXEC; each role independently reads its handle. T:99–178 independently corroborates duplication and live relationships. Equal-byte distinct memfds in N13/M06–M09 are rejected by identity, not just hashes. Evidence finalization remains subject to B3. |
| Consumer/observer | VERIFIED WITH RESIDUAL ASSUMPTION | I:253–272 contains separate stat/query/read/hash bodies; neither calls the other or shares its result/buffer. They read without changing the common offset and do not mutate the object. Fixed callable identity checks occur before role use. This is logical same-process independence, not mutual isolation against compromised Python/globals. |
| Canonical determinism | VERIFIED for the preserved positive/isolation runs | Independent oracle T:43–54, comparison T:222 and repetition T:501 establish identical expected bytes. The four saved hashes match; schema emits no clock/random ID/PID/FD/inode/temp path. No fresh suite or kernel rerun was performed in this review. |
| Claim boundary | VERIFIED | R explicitly denies execution, runtime/dependency/process/client/transport/scientific/E0 and full-gate claims. B1 prevents endorsing the general exact-original-file claim across all allowed read outcomes; the four demonstrated positive cases are narrower valid observations. |
| Residual assumptions | VERIFIED as explicit limitations | Kernel/descriptor semantics, Python/harness/loading, hash library, exclusive acquisition and controlled descriptor table are stated. K/T content hashes and the recorded interpreter hash are not loaded-runtime or dependency-lock proof. |

### Harness strengths and limitations — PARTIAL

F/M/S, fixture bytes, output profile and the canonical expected records are separately
encoded in T; refusal strings are explicit expected values and compared byte-for-byte,
not taken from candidate output. Real positive observations are independently checked,
not accepted merely because the candidate sets a flag. Same-object substitutions change
live references to distinct equal-byte memfds and reach the association guard. N27 is
explicitly a read-result fault, not an impossible claimed mutation through seals.

Some protocol values (Q, role version constants) are read from I in the harness. Static
comparison confirms the current values match the frozen contract. Separate output oracles
and missing-seal subcases provide useful checks, but sharing those values is not an
independent derivation of all policy constants. No current wrong constant was found.

The `Trace.calls` counters at T:121–127 count completed role pread operations, not function
entries. An exception before a read is not counted as an invocation. The current fixed
successful bodies each perform exactly one read, and static call sites are single-use;
the preserved counts are consistent for tested paths. The stronger general claim that
invocations are directly observed is PARTIAL. Actual entry counts and pre-read exception
cases would be needed to substantiate that claim without equating reads with calls.

Each case allocates fresh fixture state and uses ExitStack to restore patches. Positive
repetition explicitly compares canonical bytes. No accidental dependence on an earlier
fixture or descriptor number was found. This is source/evidence review, not an exhaustive
concurrency or arbitrary-host attack assessment. Assertion-based checks depend on the
recorded non-optimized invocation; they are not secure against disabling assertions.

### Kernel versus synthetic evidence — VERIFIED WITH RESIDUAL ASSUMPTION

T:406–421 performs genuine pwrite/ftruncate attempts, checks EPERM and unchanged bytes,
size and Q, then the harness raises HANDOFF_MUTATION_ATTEMPT to terminate the deliberate
protocol violation. T:447–460 holds a real shared writable mapping, checks EBUSY when
applying seals, and closes the mapping during cleanup. R describes these distinctions
correctly; it does not present the harness-generated outer refusal as kernel detection
of a malicious process. These facts are supported by retained results and inspected test
code; this review did not repeat those kernel operations.

M02, N26/N27, result/identity faults, N25 socket/device metadata and A-unreadable are labelled
synthetic. M12 is a test-only reopen guard. M11 is post-copy size corruption with the actual
write return preserved, and M14 separately covers failed/short writes. None is substituted
for the recorded real EPERM/EBUSY checks. N31's inaccurate coverage implication is B3.

## Receipt accuracy and administrative verification

R's source hashes match the current reviewed implementation and harness:

- I: `ad46e8370d04b0fb38fda2aca0fd2417380f4b59e3e7d76b51025e6a0c93f6eb`.
- T: `0c85b93d2565eb075c0c840c3fe34815113d85b9dadfdc1b15e076e6eca2db6e`.
- Preserved canonical ACCEPT: `1647d76d543133b722667352b5964d70f335c6cb7eb22930d966bf957243eae5`.
- Preserved aggregate stdout including final LF: `9a3e067bd06393d110899e4114560b8c0d6bda8ac5a023246cd54fa748bd1313`.

Parsed the embedded report and reconstructed all 80 canonical record bytes/hashes.
All hashes match; 4 ACCEPT, 76 REFUSE and the expected family inventory are internally
consistent. This verifies preservation, not cryptographic authenticity of execution or
completeness of the test matrix. The report was read from committed R, not /tmp caches.

Receipt-accuracy verdict: PARTIAL. Its 80-case count, positive determinism, tested kernel
results, synthetic labels, source pins and unchanged gate boundaries are supported.
The implication that this passing matrix establishes the complete frozen slice is
UNSUPPORTED because of B1–B3. Its invocation language must be read as successful read
counts for the demonstrated paths, not a separately instrumented entry-count guarantee.
The historical receipt is preserved unchanged, with these qualifications added here.

## Preservation and closing disposition

This review used source inspection, administrative parsing/hashing, and three bounded
in-memory reproductions of acquisition/copy behavior. All filesystem/memfd primitives in
those reproductions were replaced by local doubles; no fixture or protected object was
created, no acceptance suite rerun, and no live/client/scientific/E0 execution occurred.
Implementation and test bytes were not changed. Pre-commit preservation check: PASS; all
199 pre-existing tracked files are byte-identical to reviewed HEAD, including scientific
artifacts and H2A1. Git status contains only this new review receipt.

- implementation-boundary verdict: VERIFIED; non-executing synthetic scope retained.
- sealing verdict: VERIFIED WITH RESIDUAL ASSUMPTION; preserved kernel checks supported, not rerun here.
- same-object verdict: VERIFIED WITH RESIDUAL ASSUMPTION for demonstrated delivery; final evidence conformance PARTIAL under B3.
- consumer/observer verdict: VERIFIED WITH RESIDUAL ASSUMPTION; separate reads, same trusted process.
- acceptance-contract verdict: PARTIAL; B1–B3 block complete conformance.
- test-harness verdict: PARTIAL; useful independent oracles but missing short-read boundaries and incorrect N31 omission target.
- kernel-vs-synthetic verdict: VERIFIED; recorded genuine denials are not replaced by synthetic faults.
- determinism verdict: VERIFIED for preserved four positive/isolation records; no hidden dynamic identifiers in canonical schema.
- claim-boundary verdict: VERIFIED as limited scope; general exact-input claim not fully established due to B1.
- receipt-accuracy verdict: PARTIAL; historical results intact, completeness implication unsupported.
- residual assumptions: trusted kernel/descriptors, Python/loading/harness and hashing, controlled fixture/descriptor state; no runtime/dependency lock.
- blocking issues: B1 incomplete acquisition can pass; B2 short memfd read code mismatch; B3 independent-evidence omission is not the tested/finalized boundary.
- implementation-slice verdict: PARTIAL.
- external_trust_root slice status: demonstrated sealed-handoff evidence retained; full slice conformance not accepted pending corrections; full gate and all other seven substantive H2 gates remain unresolved.
- H2A1 status: VERIFIED for scoped prospective custody/publication auditability; unchanged, not re-audited here.
- H2A2 status: first slice implemented and historically tested; independent review PARTIAL; no further integration.
- E0 status: HOLD.
- one next bounded action only: authorize one offline correction/acceptance circuit for B1–B3 and the associated evidence/call-count tests, preserving historical receipts and the existing claim ceiling.
