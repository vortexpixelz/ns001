# NS-001 H2A2 consumption-boundary implementation re-review v0.1

## Basis and method

HEAD before: `e7b806f5c2b649a8487887f28ecdae88696735b2`, branch
`codex/e0-h2-preparation`; initial working tree clean. HEAD after is the commit
introducing this receipt; its resolved identity is reported after commit.

Independent re-review means a separate assessment in this turn, not an independent
organization or external authenticated witness. Read the corrected implementation,
tests and correction receipt against the prior implementation review and frozen
acceptance specification, specification correction and specification re-review.
No repair or implementation change was made. Administrative data-only Python decoded
JSON/base64/gzip and calculated hashes; no surrogate module, acceptance harness,
compiler/loader/client/scientific/E0 path was imported or executed.

Implementation SHA-256: `65b13fb57c8ea02b8ee868defa9f410d18b1f78703483e3719c4e69056e9d2cb`.
Test SHA-256: `cd272f651af924bb32b610432c587533909ff19743efe343a42b220b54ad5290`.
Both archived tested sources match the current files exactly.

## F1 — CLOSED within retained-custody assumptions

Store initialization distinguishes exclusive creation from reopening. Only successful
creation of a previously absent directory enables creation of lock, store.json and
expectation metadata. A pre-existing empty directory is deliberately refused rather
than treated as fresh. Thus a new empty store initializes legitimately through its
constructor, but a caller cannot bless an existing empty retained root as new.

Reopen opens the retained lock without O_CREAT, validates regular-file metadata and
root/lock identity, compares namespace metadata and expectation bytes with the expected
canonical values, and does not rewrite them. Missing metadata raises STOP; malformed
or conflicting bytes cannot equal the required canonical bytes. Required expectation
linkage is checked at its content-derived pathname. Custody is checked again before
reserve, recovery and normal writes. A caller's supplied namespace or expectation
cannot reconstruct a missing file in an existing retained root.

The 11 retained custody checks cover missing store/expectation/lock, malformed and
conflicting store/expectation, live missing store/expectation, valid reopen and existing
empty root. Ten byte-map observation files show damaged == after; valid reopen also
shows before == after. The eleventh empty-root case is supported by the harness's
explicit no-files assertion and recorded STOP. No metadata repair is hidden in reopen.

This does not detect malicious deletion of the entire directory followed by dishonest
reuse of its namespace: preservation of the root/namespace and no reuse are explicitly
frozen custodian assumptions. Nor is this a hostile-host concurrent-race defense. These
are retained limitations, not a new runtime-lock requirement or an F1 closure claim
outside the frozen custody regime.

## F2 — CLOSED

Recovery first checks that parsed registration is exactly a dict before using its keys.
Canonical null/scalar/list values therefore reach controlled invalid-record handling,
not the former uncontrolled set(null)/set(integer) TypeError. ValueError, TypeError,
KeyError and RecursionError are classified; decoding errors inherit ValueError.
A complete newline-terminated invalid registration sets RECORD_INVALID and clears the
registration object. Torn/empty/missing registration remains ATTEMPT_INCOMPLETE absent
another complete invalid record. Recovery remains ABORTED, never inferred acceptance.
No code, rank or recovery schema was added by this correction.

The retained ten complete malformed cases and three torn/empty/missing cases have the
specified distinct primary codes. The harness checks each result and repeated recovery,
and preserves original bytes. Data-only review independently checked terminal state/code
pairs and raw registration/request/witness/journal hash bindings for all 21 ABORTED
records. Repetition here means idempotent recovery of identical retained inputs; unique
attempt IDs correctly prevent claiming identical whole receipts across new attempts.

## F3 — CLOSED

Attempt.require_writable checks custody and final/interrupted recovery before any
register/event persistence. A retained recovery disposition stops both cached and fresh
writers. The check precedes witness persistence, journal append and cached event update.
Register cannot rewrite request/registration. Dispatch reaches guarded event writes;
invoke checks the same guard before calling receive. Recovery never invokes receive;
repeated matching disposition returns unchanged and conflicting disposition stops.
A stale journal also refuses before append. In-memory witness bookkeeping is not a
resumed durable lifecycle or authorized dispatch.

The 252 recorded STOPs form exactly the Cartesian product of 21 ABORTED attempts,
original/fresh writers, and six operations: PREPARED, ATTEMPTED, ACCEPTED, REFUSED,
register and invoke. No duplicate tuple substitutes for a missing operation. Harness
control flow appends a STOP result only after catching Stop; successful return fails the
test. It compares complete attempt-file snapshots and receiver-entry counts before and
after these probes. Fresh event-writer cases additionally require a terminal diagnostic.

Evidence strength is bounded: an original writer from a closed store can stop at the
custody check, and fresh invocation witnesses are unarmed. Thus 252 is a count of rejected
operations, not 252 independent armed-dispatch experiments. The reviewed unconditional
pre-invocation recovery guard supplies the causal terminality argument; fresh event
writers rule out reliance solely on stale cached state. No bypass in the supported
lifecycle API was identified. Direct malicious calls to raw filesystem helpers or the
receiver are outside the frozen trusted-program assumption.

## Regression, evidence and determinism

Decoded the correction receipt's 315-file archive, without using temporary-run files:

- Gzip SHA-256: `83be4887fa03c5065ece59c31ea3d8f53f02f8ba4e5772ef05f611bb88d14522`.
- JSON SHA-256: `5f0865ad1f3ab604c6cf05e2dd9a894796e36e6d64e7e9b035e5538dd284c793`.
- Raw terminal records, cross-checked with their recorded hashes: 2 ACCEPTED,
  27 REFUSED and 21 ABORTED.
- Independently recounted canonical complete record round trips: 207. Deliberately
  malformed raw registration is not normalized or counted as schema-valid evidence.
- Custody result inventory: 11; post-ABORT tuple inventory: 252, all STOP.

Both positive witness hashes bind to their terminal records and same attempt IDs.
Actual entry records carry length 3, SHA-256 of abc, same-A/same-B and independent-A
comparison, typed parameter match and hook/dispatch facts. Dispatch hashes bind the
persisted ATTEMPTED events. Removing only attempt ID and derived dispatch hash yields
equal positive semantic observations. Canonical serialization round-trips exactly;
whole records from different attempt IDs deliberately differ.

Review of the unchanged bounded test paths confirms equal-byte B substitution uses a
new object and checks identity, unrelated A substitution checks protected association,
missing witness cannot be supplied by a valid return, and denied pathname/fallback
requests do not read the altered decoy. Rank-ordered primary refusal logic is unchanged.
The correction diff changes custody/writer guards and registration classification,
not the receiver, qualification, observer, derivative binding or witness schemas.
B3/B4 therefore remain materially unchanged within their existing residual assumptions.

The prior 420-file evidence archive still decodes with gzip SHA-256
`079bcc12809e0abe7597448d9a6a99f5b1b825646071f52b97ade140393fe78a`.
Historical receipts remain byte-identical. Retained records and test control flow
corroborate the correction receipt's counts; receipt prose alone was not accepted.
This read-only review does not claim a fresh acceptance-suite execution, authenticate
past process exit status independently, or prove real power-loss behavior.

## Preservation and verdict

Before creating this receipt, all 212 tracked files compared byte-for-byte with HEAD
before. Before commit, only this new receipt is changed. Corrected implementation,
tests, correction receipt, frozen contracts, prior review, H2A1, first H2A2 slice and
scientific artifacts are unchanged. No runtime-lock work or live execution occurred.

The strongest permissible positive claim remains:

> Within the frozen synthetic offline surrogate scope, exact protected bytes were bound to and independently witnessed at the qualified surrogate receiving boundary.

- F1: CLOSED.
- F2: CLOSED.
- F3: CLOSED.
- custody regression: PASS within retained-custody assumptions.
- registration classification: PASS; complete-invalid distinct from torn/missing.
- ABORTED terminality: PASS for supported lifecycle and dispatch paths.
- positive tests: 2 corroborated from retained evidence.
- refusal tests: 27 corroborated.
- recovery tests: 21 corroborated.
- custody tests: 11 corroborated with the evidence qualifications above.
- post-ABORT rejection: 252 corroborated operations, not independent armed-dispatch trials.
- determinism: PASS for canonical encoding, semantic repeat and idempotent recovery.
- preserved evidence: PASS; historical evidence unchanged.
- blocking issues: NONE identified in F1–F3 or their bounded regression scope.
- implementation-slice verdict: VERIFIED WITH RESIDUAL ASSUMPTION.
- residual assumptions: frozen trusted host/interpreter/harness/observer, kernel,
  filesystem synchronization and preserved custody namespace/store; no hostile-host proof.
- external_trust_root status: full gate unresolved; actual compiler consumption unproven.
- H2A1 status: unchanged VERIFIED for scoped prospective custody/publication auditability.
- H2A2 status: first sealed-handoff slice unchanged independently VERIFIED; corrected
  consumption surrogate independently re-reviewed within the stated assumptions;
  all eight full H2 gates unresolved.
- E0 status: HOLD; no execution or readiness claim.
- next bounded action: a document-only scope review of the immediately adjacent
  external_trust_root boundary, retaining the runtime-lock interface and real-engine
  deferral; not performed and requiring separate authorization.
