# NS-001 H2A2 consumption-boundary specification re-review v0.1

## Basis and decision

Reviewed HEAD: `1292401b269be9f64cff5141293aac65f3f103ad` on
`codex/e0-h2-preparation`. After the reported shutdown, inspection confirmed that HEAD,
a clean working tree, and no existing partial receipt or later receipt commit. This
finishes the interrupted review without replacing completed work.

Reviewed only the consumption-boundary acceptance specification (S) and specification
correction receipt (C), against the prior acceptance review (R), all in `docs/e0/h2/`
at the reviewed commit. This is a separate review turn, not an independent organization.
**Implementation-ready: YES for the offline non-executing surrogate contract.** No remaining
B1–B4 blocker was identified. This is document acceptance, not implementation verification
or permission to execute the next circuit.

S SHA-256: `7757f0d7fb8c8f27d2c7516e68c065ea4313b3fd8f013f6674a1e2c5f81799b6`.
R SHA-256: `85ed8e3ce501cad05e1400137c8d9e2ed1a470cc8f29ae2ccf748a5db725ea01`.
These match C's preserved identities. C accurately limits its findings to contract repair.

## B1–B4 findings

**B1 — CLOSED at contract level.** S sections 5 and 8 require exclusive durable reservation
before preparation, retained registration/request identities, and synchronized ATTEMPTED
before dispatch. ACCEPTED/REFUSED are immutable terminal states. Interrupted nonterminal
reservations become distinct ABORTED dispositions; recovery neither retries consumption
nor infers acceptance. Attempt ID, raw journal and maximal valid-prefix hashes/lengths,
and registration/request/witness hashes bind recovery to the correct retained attempt.
Empty reservations and torn tails remain visible. Restart either reproduces the same
recovery record or stops on conflict. Completeness is conditional on the stated honest
storage/synchronization and preserved namespace/store assumptions, not resistance to
malicious deletion or rollback. The former missing prefix field and pre-PREPARED gap are
addressed.

**B2 — CLOSED at contract level.** S section 7 separates initial object admission from
post-binding substitution, candidate-request validation from evidence-record validation,
and normal completion from recovery. Normal failures choose the smallest applicable rank;
secondary diagnostics cannot change that primary. Recovery deterministically distinguishes
complete invalid evidence from interrupted writes. The eighteen codes have bounded reachable
cases in section 9; precondition failures do not acquire an invented invocation-count fault.
The prior counterexamples now resolve to OBJECT_SUBSTITUTION for later A replacement,
EXPECTATION_INVALID for a missing candidate expectation, and ABORTED/ATTEMPT_INCOMPLETE for
a torn tail without complete invalid evidence. No runtime-lock proof is required by those
surrogate refusal tests.

**B3 — CLOSED at contract level.** S section 4 fixes receiver artifact, exact callable and
six-argument interface, live code/reference association and permitted bootstrap under an
explicit trusted-process assumption. It separates harness startup from payload selection.
Python executable, stdlib, package, import and full environment closure are explicitly not
surrogate acceptance requirements. Actual compiler image/build/callable and native-entry
observation remain unproven, and the real profile always refuses. Concrete future artifact
pins are required test inputs, not a remaining substantive behavioral decision. No hidden
runtime-lock gate is needed for this conditional synthetic claim.

**B4 — CLOSED at contract level.** S section 6 specifies actual receiving-entry observation,
separate observer state, independently computed incoming length/digest, live retained A→B
association, actual typed parameters, dispatch ordering and matching return evidence.
The lifetime sentinel covers premature entry. A separate canonical witness carries the same
attempt/expectation identity; the terminal event binds its entire hash. No-reopen/fallback
coverage is explicit for the reviewed fixed program and denying test guard. It is not a
hostile-process syscall sandbox. The consumer's output cannot populate independent witness
facts. In-process role independence is adequate only under the expressly retained trusted
harness/interpreter/kernel assumptions; it proves neither real compiler receipt nor runtime
correctness. The previously missing witness schema and attachment binding are supplied.

## Preservation and disposition

Administrative text/hash/Git checks only; no Python, compiler, loader, runtime, client,
acceptance harness or E0 path was invoked. Before commit, all 206 pre-existing tracked files
were compared byte-for-byte with reviewed HEAD and remained unchanged, including S, C, R,
H2A1 and the completed first H2A2 implementation/tests. Only this new receipt changed.
No stronger claim, additional requirement or another gate is introduced.

- B1 verdict: CLOSED at document-contract level, with declared custody/storage assumptions.
- B2 verdict: CLOSED at document-contract level; one deterministic primary code per failed disposition.
- B3 verdict: CLOSED at document-contract level; surrogate qualification is distinct from real-engine and runtime-lock qualification.
- B4 verdict: CLOSED at document-contract level; independently retained actual-entry witness within trusted in-process scope.
- blocking issues: NONE identified within B1–B4.
- implementation-ready: YES for the specified offline non-executing surrogate; separate implementation authorization required.
- external_trust_root status: full gate unresolved; actual compiler consumption unproven.
- H2A1 status: VERIFIED for scoped prospective custody/publication auditability; unchanged.
- H2A2 status: first sealed-handoff slice independently VERIFIED; corrected downstream surrogate contract re-reviewed only; all eight full H2 gates unresolved.
- E0 status: HOLD.
- one next bounded action only: obtain explicit authorization for one offline synthetic non-executing surrogate implementation/acceptance circuit under the corrected contract.
