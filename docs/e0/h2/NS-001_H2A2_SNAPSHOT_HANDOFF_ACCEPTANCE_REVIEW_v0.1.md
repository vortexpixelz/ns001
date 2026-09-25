# NS-001 H2A2 snapshot-handoff acceptance review v0.1

## Review basis and decision

Reviewed preparation branch `codex/e0-h2-preparation` at
`d2d92334f6fc1cdc3a038461a4e38784fa5c1cc8`. The reviewed object is
`docs/e0/h2/NS-001_H2A2_SNAPSHOT_HANDOFF_ACCEPTANCE_SPEC_v0.1.md`
at that commit. Section references below refer to that pinned specification.
This is an independent reading of the contract, not an implementation or a demonstration
of its proposed protections. Only this review receipt is added.

**Implementation-ready: PARTIAL.** One substantive decision remains: select and approve
one concrete acquisition-to-immutable-handoff binding mechanism, including its independent
observation/checkpoint profile. The abstract contract is otherwise implementable without
inventing substantive input or outcome semantics. This review does not select that mechanism
or authorize implementation. Additional coverage noted below tests already specified behavior.

## Findings

### Claim and ownership — VERIFIED

Sections 1–2, 7 and 12 limit success to exact single-file byte validation and protected
handoff to the fixed non-executing identity consumer. Running validator/consumer test code
is distinguished from executing the payload. Source execution, identified runtime/process,
dependency identity, client traffic and execution uniqueness are explicitly excluded.
The proposed slice does not establish the full external_trust_root gate or take ownership
of the other seven substantive H2 gates. All eight remain unresolved.

### Object identity — VERIFIED

Sections 3–5 fix the ASCII path `source.bin`, exact three bytes `61 62 63`, byte length,
SHA-256, and no normalization, decoding or newline changes. Path spelling is part of
identity; links and multiple hard links are forbidden. File type and readability are
required; owner, mode and time are not identity inputs. Source identity is distinct from
snapshot descriptor identity and from the physical acquisition directory.

Administrative text/hash verification in this review reproduced the frozen constants:

| Object | SHA-256 |
| --- | --- |
| Payload F | `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` |
| Canonical manifest M | `4a9ebe2c4e275600d9a6c7864bb14c3d5a4c0b6a7c8bbf88193fc48f76affce0` |
| Canonical descriptor S | `0ae1c30f2568188390fe05d092609eb122f3bee16c48f41fae9fe3f08e6ba432` |

This checked document constants, not runtime controls.

### Manifest — VERIFIED

Section 4 defines one four-field object, exact values/types, canonical compact sorted ASCII
JSON, no extra whitespace/BOM/newline, and duplicate-aware parsing before dictionary creation.
Duplicate path keys precede other duplicate keys; arrays/path lists are schema failures.
Unknown/missing fields, wrong versions, absolute/traversal paths, alternate path spellings,
length/digest mismatch and noncanonical serialization have assigned refusal codes. Invalid
paths never become OS-call operands. The 1024-byte limit and overflow read are bounded.
For this fixed schema and ASCII fixture, serialization does not depend on unspecified
Unicode or general-purpose number canonicalization choices.

### Snapshot and root — VERIFIED WITH RESIDUAL ASSUMPTION

Sections 3 and 5 specify exactly two direct acquisition files, no nested/hidden/special
extras, logical root `ns001-h2a2-fixture-v1`, and a snapshot containing only retained payload,
canonical manifest and logical root identity. Physical temporary paths are excluded from
canonical evidence. Another directory with identical contents is not the bound R.
The abstract membership/identity contract is deterministic. Its stable physical-root
binding and controlled acquisition assumption still need realization in the single mechanism
decision below; a path string or content digest alone does not prove that binding.

### Immutable handoff — PARTIAL; B1 BLOCKING before implementation

Section 6 requires the same immutable object instance/capability associated with the successful
validation event, independently observed through consumer completion. Equal-byte object
replacement is forbidden. Consequently a sealed buffer, immutable copy, content-addressed
object and read-only descriptor are not interchangeable acceptance mechanisms merely because
they return the same digest. Copy timing changes which object was validated; content addressing
does not prevent replacement; a read-only descriptor may retain mutable backing storage.

**B1, the single missing decision:** approve one concrete binding profile that specifies
stable root/acquisition binding, snapshot finalization, the protected object/capability and
its lifetime, independent association observation, and deterministic substitution/mutation
checkpoints. These are parts of the same acquisition-to-consumption trust boundary, not
permission to add runtime identity, a loader or live integration.

The selected profile must explain how N13 and N26–N27 operate on that actual primitive.
For N27, distinguish a real mutation attempt prevented by protection from the synthetic
changed-content refusal branch. Do not report a synthetic HANDOFF_MUTATED result as proof
of actual immutability or silently equate a prevented write with a changed snapshot.
The specification already demands this distinction; the profile must bind the concrete
observation and test adapter before implementation. No mechanism is chosen here.

### Consumer — VERIFIED WITH RESIDUAL ASSUMPTION

Section 7 fixes version, entrypoint, permitted count/hash/compare behavior and forbidden
pathname reopening, evaluation, subprocess, network, plugin and mutation behavior.
C_SRC must pin the whole future implementation module before acceptance runs and cannot
be supplied by the snapshot. Its absence before code exists is not a second design choice.
The trusted harness must actually bind that reviewed consumer and observe its calls;
a source hash or returned tuple alone is not proof of loaded/runtime identity. This
residual harness assumption is explicit and does not support a runtime/process claim.

### ACCEPT/REFUSE — VERIFIED

Sections 6, 8–10 define one final ACCEPT predicate; P2 reaches that same predicate using
the retained object after the obsolete pathname changes. It is not a second permissive
acceptance rule. Final evidence must exist before success. Refusal is terminal, without
retry or repair; post-consumer refusal may have one invocation but no accepted result.

Phase order and first applicable code within each phase resolve overlaps. Code priority
applies across member defects; lexicographic entry inspection does not override that stated
priority. Duplicate-path precedence and missing-before-extra behavior are explicit.
MANIFEST_HASH and SNAPSHOT_IDENTITY are defensive consistency guards: after exact canonical
constants have passed they are not independently reachable ordinary-input mutations.
Their presence does not require inventing a second accepted representation or forcing a
normal fixture to reach an impossible state. Crash/non-delivery is an unsuccessful test,
not an additional canonical outcome or inferred ACCEPT.

### Test matrix — PARTIAL coverage, without another substantive design decision

P1 fixes positive byte equality, single delivery, oracle values and repeatable receipts;
P2 fixes post-finalization pathname replacement/deletion isolation. N01–N31 cover the
requested wrong/altered/missing/extra source, wrong manifest/expected identity, object
substitution, mutable backing, consumer replacement/result and missing evidence boundaries.
The appended required root/link/alias/unreadability/oversize cases are part of the matrix;
N01–N31 alone are not its full required coverage. N25 metadata stubs cannot prove OS safety.

Genuine missing explicit cases are schema-type rejection (for example a boolean length or
path-list value -> SCHEMA_TYPE), combined duplicate path/other key precedence -> DUPLICATE_PATH,
and an acquisition instability checkpoint -> ROOT_UNSTABLE. These exercise stated contract
boundaries; none requires a new outcome or policy. Include these bounded cases when a future
implementation is authorized. Also check invocation counts and canonical record bytes for
all existing cases as section 9 already requires. General fuzzing is unnecessary here.
Mechanism-dependent genuine-path coverage remains contingent on B1; it is not marked passed.

### Evidence — VERIFIED WITH RESIDUAL ASSUMPTION for format; PARTIAL for protection proof

Section 9 fixes canonical ACCEPT/REFUSE fields, external record hashes and a deterministic
handoff content identity. It excludes clocks, physical paths and ephemeral object tokens.
A refusal's false handoff_succeeded denotes no fully accepted result, not necessarily zero
consumer calls; the separate observation establishes the count.

Validated bytes -> protected handoff -> fixed consumer observation is supportable only
with the separately retained harness association/count observations and the approved B1
profile. Neither equal hashes, H_ID nor handoff_observed=true alone proves that chain.
Identical reruns deliberately have identical receipts: freshness, unique execution and
cryptographic execution attestation are not claimed. Trust in host, harness, hashing and
the concrete protection mechanism remains a residual assumption, not silently VERIFIED.

## Preservation and review limits

No implementation, payload/consumer execution, runtime/client operation, E0 execution,
network experiment or scientific test was performed. Operations were document inspection,
administrative hashing and Git preservation. No runtime implementation was imported.
Before commit, every existing tracked file was compared byte-for-byte to the base commit;
only this new receipt was present as a change. This includes all H2A1 evidence, the reviewed
specification, frozen scientific artifacts and earlier receipts. Commit scope is this receipt
alone; Git bookkeeping and the requested branch push are the only preservation mutations.

## Closing disposition

- claim-boundary verdict: VERIFIED; byte validation and non-executing handoff only.
- object-identity verdict: VERIFIED.
- manifest verdict: VERIFIED.
- snapshot/root verdict: VERIFIED WITH RESIDUAL ASSUMPTION; concrete binding pending B1.
- immutable-handoff verdict: PARTIAL; B1 blocks implementation.
- consumer verdict: VERIFIED WITH RESIDUAL ASSUMPTION; fixed trusted harness and pinned future source.
- ACCEPT/REFUSE verdict: VERIFIED at the specified abstract contract boundary.
- test-matrix verdict: PARTIAL; listed coverage additions and concrete B1 mapping required.
- evidence-contract verdict: deterministic format VERIFIED; protection proof PARTIAL pending B1.
- blocking issues: B1 only; no additional substantive behavior decision identified.
- implementation-ready: PARTIAL.
- if PARTIAL, exact single missing decision: select and approve one concrete acquisition-to-immutable-handoff binding and independent observation profile, including its N13/N26/N27 checkpoints.
- H2A1 status: VERIFIED for scoped prospective custody/publication auditability; unchanged.
- H2A2 status: implementation UNSTARTED; all eight substantive H2 gates unresolved.
- E0 status: HOLD.
- one next bounded action only: one document-only binding-mechanism selection receipt resolving B1 and recording its concrete acceptance observations; no implementation.
