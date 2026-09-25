# NS-001 H2A2 runtime trust-root correction review v0.1

## Review basis and decision

Preparation branch `codex/e0-h2-preparation`; reviewed HEAD
`378be59be4e2306c19fc0d16bbbd3770731e5e4e`; initial working tree clean.
Reviewed only the implementation, harness and correction receipt named below, using the
frozen acceptance specification, mechanism selection and prior implementation review as
comparison authorities. All line references refer to the reviewed commit.

- I: `e0/h2/runtime_trust_root.py`.
- T: `tests/test_e0_h2_runtime_trust_root.py`.
- R: `docs/e0/h2/NS-001_H2A2_RUNTIME_TRUST_ROOT_CORRECTION_RECEIPT_v0.1.md`.

**Corrected implementation-slice verdict: VERIFIED within the frozen non-executing
synthetic scope, with the explicitly retained residual trust assumptions.** The prior
B1–B3 blockers are closed. No new blocking issue was found in the requested review scope.
This is an independent review turn, not an independent organization or security principal.
It does not close external_trust_root or any other substantive H2 gate.

Method: static code/contract review plus administrative parsing and hashing of committed
evidence. Neither reviewed module was imported or executed. No acceptance suite, memfd,
fixture, live runtime, client, scientific code or E0 was run in this review. Kernel and
repetition findings below refer to the preserved corrected acceptance run and its inspected
test paths, not fresh kernel execution. Historical receipts remain unchanged.

## Findings against the fourteen requested checks

### 1–2. Oversized input and complete-object identity — VERIFIED WITH RESIDUAL ASSUMPTION

I:129–148 validates the opened regular single-link object's identity against the initial
metadata, requires source size exactly 3 or manifest size at most 1024, requires the bounded
read length to equal the opened object's entire observed size, requires a one-byte EOF
probe to return empty, and rechecks that object's metadata. I:208–216 subsequently checks
canonical manifest/hash, full payload length/hash and unchanged membership metadata.

The original counterexamples no longer pass: source size 4 fails FILE_LENGTH before a
prefix read, and manifest size over 1024 fails MANIFEST_SIZE before canonical-prefix
validation. A partial read of a permissible-size file fails IO_ERROR. An appended source
byte at the EOF probe fails FILE_LENGTH. No retry, read-completion loop or trimming can
turn an incomplete read into acceptance. SHA-256 is calculated over the complete accepted
three-byte object, not an arbitrary prefix.

T's N02/N03 cover ordinary truncation/append. B1-large-tail covers larger appended input;
B1-source-prefix and B1-manifest-oversize-prefix prove rejection before the dangerous read;
B1-manifest-trailing-prefix and B1-incomplete-source exercise actual incomplete reads via
bounded adapters. B1-eof-extra-byte schedules a real append before the EOF probe. These
are distinct, relevant boundaries. Unreached prefix adapters in the size-first cases are
correctly labelled as early rejection, not claimed evidence of a performed short read.

This establishes the intended property under the frozen trusted-kernel and exclusive
synthetic-acquisition assumptions. It does not promise immunity to a lying kernel or
uncontrolled concurrent filesystem mutation. Changes after successful snapshot finalization
remain allowed by the frozen P2 isolation contract and do not change the retained bytes.

### 3–4. Memfd read versus size refusal — VERIFIED

I:222–230 first checks returned length against min(observed size, four-byte request).
A two-byte read of an observed three-byte object therefore returns MEMFD_COPY_IO before
size/digest checks. A complete two-byte object returns MEMFD_COPY_SIZE; a complete four-byte
object likewise returns MEMFD_COPY_SIZE. This implements the mechanism receipt section 5
priority for incomplete I/O separately from wrong object size.

Both before-seal and after-seal B2 short-read cases use a real correctly sized memfd with
a deliberately shortened positioned-read request; the preserved result is MEMFD_COPY_IO.
M11-2/M11-4 continue to produce MEMFD_COPY_SIZE. These test adaptations do not imply that
the kernel spontaneously returned short data or that seals were bypassed. No new code or
changed refusal semantics were introduced by the correction.

### 5. Correct N31 omission — VERIFIED

T:442–451 clears only Trace.associations before evidence assembly. It does not remove,
replace or corrupt either role's valid result. T:268–277 independently verifies those
results against the fixed oracle, verifies both calls occurred once, verifies every other
evidence component remains true, and records the exact omission. Trace.evidence maps the
missing independent association component to same_object=None. I:332–339 consequently
returns EVIDENCE_INCOMPLETE. The retained N31 record/hash and observation agree.

The old test's missing observer-result argument is no longer the N31 target. The new test
reaches the real final evidence boundary with intact role results and insufficient
independent evidence. It satisfies the frozen N31 definition.

### 6–7. Evidence finalization and internal staging — VERIFIED WITH RESIDUAL ASSUMPTION

I:303–326 introduces internal measurement/evidence containers, not additional public
verdicts. Successful `run` returns PendingHandoff without an ACCEPT field or serialized
receipt. The failure path still returns REFUSE. The harness constructs evidence from its
separate creation, duplication, copy/seal, role-operation, association and no-reopen
observations before calling `finalize` (T:179–203, 263–278).

I:329–357 checks the exact container types, every required true observation, integer call
counts of one, and exact role-result structure/values before canonical serialization.
Source AST inspection found the only construction of verdict=ACCEPT in `finalize`, after
those checks. A missing required observation cannot produce ACCEPT through this reviewed
path. The outward receipt schema remains the frozen mechanism profile's ACCEPT/REFUSE;
PendingHandoff is an internal staging value, not a third accepted outcome.

Closing handles after all live observations but before serialization does not change the
claim: evidence describes the completed observed handoff, not a permanently retained live
object. The kernel protects the payload through both role completions and final association
checks. Pending dictionaries are measurement records, not the protected payload itself;
finalization rechecks their expected contents.

This is an evidence gate inside a trusted reviewed harness, not an unforgeable capability,
anti-replay service, sandbox or cryptographic authentication protocol. An arbitrary caller
that fabricates containers or a compromised Python process is outside the explicitly frozen
trust model. No stronger universal claim about preventing arbitrary Python serialization
is implied. The staging changes correct B3 without expanding the scientific/runtime claim.

### 8–9. Four positive cases and eighty-four refusals — VERIFIED for the bounded matrix

P1 creates the exact synthetic fixture and genuinely traverses acquisition, copy/seal,
both independent observations and evidence finalization. P1-repeat uses a fresh root.
P2-replace and P2-delete modify only the original source pathname after `_finalize` returns;
the same protected memfd must still be observed. All four compare actual canonical bytes
with a separately encoded oracle and independently check actual descriptor relationships
and role operations. They are not four aliases for an unexecuted expected record.

For every negative, T:287–290 compares actual canonical bytes against an independently
constructed REFUSE with an explicit expected code, rejects any ACCEPT substring and checks
call counts. The committed aggregate has exactly 84 such cases, with N01–N31 and M01–M15
families present. Review of setup/adapter placement found no substitute expected-output
assertion masquerading as a boundary test in the corrected matrix.

| Negative groups | Actual boundary exercised and limitation |
| --- | --- |
| Fixture/path/manifest/root N cases and appended A cases | Mutated synthetic input or explicitly labelled metadata/I/O stub reaches the relevant validator guard; stubs do not establish OS behavior |
| N13 and M06–M09 | Separate equal-byte sealed memfds replace live references at fixed checkpoints; association guards refuse without relying on a hash difference |
| N26/N27, N30 and M15 | Deliberate seal-query/read/result/identity faults exercise protection/result guards; not actual seal-breaking claims |
| N31 | Independent association evidence is withheld while role results remain intact; finalization refuses |
| M01–M03, M10–M11, M14 | Creation/seal/copy and syscall failure boundaries; wrong size and short I/O remain distinct |
| M04–M05, M13 | Genuine kernel mutation/sealing denials; outer protocol refusal remains a harness action |
| M12 | Test-only consumption-reopen guard; no claim of a production syscall sandbox |
| New B1/B2 cases | Exact-size, EOF and incomplete-read boundaries described above; no broad fuzzing |

The harness now counts actual function-entry events using the two fixed code objects
(T:103–111), rather than treating successful reads as invocation counts. Separate read
observations remain. Profile state and fault patches are restored per case; fixtures and
trace state are fresh. The assertion-based harness requires the recorded non-optimized
invocation, as specified; this is a trusted test harness, not adversarial isolation.

### 10. Kernel evidence — VERIFIED WITH RESIDUAL ASSUMPTION

The inspected M04/M05 paths call actual os.pwrite/os.ftruncate and require EPERM plus
unchanged bytes, length and Q. M13 creates a real writable shared mapping and requires
EBUSY from the actual seal syscall. None of these errno outcomes is injected by the fault
adapter used for M02. The aggregate records the expected genuine denials. Cleanup does not
retry failed sealing. The subsequent outer HANDOFF_MUTATION_ATTEMPT is correctly described
as the harness's protocol refusal, not kernel-generated application evidence.

This review confirms the preserved result and the real-syscall test construction. It does
not rerun or independently authenticate the host/kernel that produced the historical run.
The trusted-kernel residual assumption is unchanged.

### 11. Same-object evidence — VERIFIED WITH RESIDUAL ASSUMPTION

I:360–385 duplicates both handles directly from retained A, checks device/inode association,
seals and type at the boundaries, invokes each fixed role separately and performs the final
live checks. Trace independently witnesses one creation, two direct duplicate edges, seven
association checkpoints, and separate stat/query/read observations from C and O. `evidence`
requires those relationships before finalization. Equal hashes alone cannot satisfy that
observed chain; the distinct-object substitutions would fail it even with identical bytes.

Numeric FD slots and inode/device metadata are ephemeral corroboration under the trusted
kernel, not stable cryptographic identities. No separate-process independence or authenticated
runtime identity is inferred. The claims remain limited to this fixed synthetic handoff.

### 12–13. Determinism and correction-receipt accuracy — VERIFIED in the stated scope

Read the committed aggregate from R, not a temporary cache. Verified both whole-source
pins, the aggregate bytes/hash, all 88 reconstructed canonical record hashes, the four
positive hashes and the full case-family inventory. All positive hashes equal
`6b5bc733835004aeb9ea6ce3994f028f9c815f2556a11fb34a9fa4724ca5adce`.
The harness additionally compares actual receipt bytes with the independent oracle per
positive and with the first positive after all cases. The serializer/schema contains no
clock, randomness, descriptor number, PID, inode or temporary path. This supports actual
byte identity in the preserved equal runs, not a fresh rerun in this review.

Reviewed source and output pins:

- Implementation K: `d15ddd0b3d689592398987e62ce3135ee8a61e48ccd48cfa511d4870ac0b0023`.
- Harness T: `67150d764cfde33e1d72837cf3ec518c3469a7f617ec19808d30c0762434b647`.
- Aggregate stdout including final LF: `43670acec3144ca5a9ff5fc95f81f42fbacfa7fccd80f77357df7835058c123e`.
- N31 canonical REFUSE: `182eb6b3f5c8349268cc51bce415fc383dac66aef8cded31870c8f54c7ee106c`.

R accurately describes the three corrections, 4/84 counts, preserved original tests,
synthetic/kernel distinction, exact N31 omission, source-pin change and remaining gates.
Its new ACCEPT hash need not equal the old implementation's hash because K/T changed.
Hash verification establishes preservation and consistency; it does not independently
prove an exhaustive historical run log or execution authenticity, neither of which is
claimed by the bounded receipt.

### 14. Claim ceiling — VERIFIED; stronger claims UNSUPPORTED

The only supported statement remains: the exact expected synthetic single-file bytes were
validated, copied into a sealed immutable handoff object, and the same protected object
was independently observed by the fixed non-executing consumer and observer, within the
trusted harness. No payload execution, scientific interpretation or live integration is
introduced. Interpreter/runtime/process/dependency identity, client/transport integrity,
response/scientific correctness, E0 execution and full-gate resolution remain UNSUPPORTED.
Kernel/descriptor semantics, Python/loading/harness and hashing, exclusive acquisition and
controlled descriptor state remain explicit residual assumptions. There is no runtime or
dependency lock. No prior historical limitation is silently promoted to VERIFIED.

## Preservation and closing disposition

Only this new review receipt is authorized to change. The review consisted of text/AST
inspection and administrative evidence hashing/parsing; no reviewed code, fixture, memfd,
client, live runtime or E0 was executed. Prior artifacts and implementation/test bytes are
preserved. Pre-commit preservation: PASS; all 201 pre-existing tracked files are
byte-identical to reviewed HEAD, including implementation/tests, H2A1 and scientific
artifacts. Only this new receipt appears in Git status.

- oversized-input verdict: VERIFIED WITH RESIDUAL ASSUMPTION; B1 closed within controlled acquisition.
- short-read-code verdict: VERIFIED; MEMFD_COPY_IO for incomplete reads, MEMFD_COPY_SIZE for complete wrong-size objects.
- N31 verdict: VERIFIED; actual independent association omission with intact valid role results.
- evidence-finalization verdict: VERIFIED WITH RESIDUAL ASSUMPTION; reviewed path emits ACCEPT only after independent evidence checks.
- test-harness verdict: VERIFIED for the frozen bounded matrix; four positives and 84 expected refusals, with explicit synthetic limitations.
- kernel-enforcement verdict: VERIFIED WITH RESIDUAL ASSUMPTION from inspected real-syscall tests and preserved EPERM/EBUSY evidence; not rerun here.
- same-object verdict: VERIFIED WITH RESIDUAL ASSUMPTION; direct live duplication/association evidence, not hash equality alone.
- determinism verdict: VERIFIED for the preserved repeated equal runs.
- receipt-accuracy verdict: VERIFIED within its stated local evidence scope and residual assumptions.
- blocking issues: NONE identified in the requested corrected-slice review; prior B1–B3 closed.
- corrected implementation-slice verdict: VERIFIED within the frozen synthetic claim and stated residual assumptions.
- external_trust_root slice status: corrected bounded evidence verified; full external_trust_root and all eight substantive H2 gates remain unresolved.
- H2A1 status: VERIFIED for scoped prospective custody/publication auditability; unchanged, not re-audited here.
- H2A2 status: first corrected offline synthetic slice independently reviewed; no live integration or whole-gate closure.
- E0 status: HOLD.
- one next bounded action only: one document-only scope review of the next remaining external_trust_root boundary, with no implementation or E0 execution.
