# NS-001 H2A2 snapshot-handoff acceptance specification v0.1

## Status and normative interpretation

Branch `codex/e0-h2-preparation`; starting HEAD
`740d1feb67c15020d90c91cf6fd572a430ce87be`; initial working tree clean.
This one document resolves the design review's B1–B3 at the acceptance-contract level.
It does not modify the design/review or implement, execute or test the proposed mechanism.
Only this new specification and its requested Git commit/push are authorized.
H2A1 VERIFIED within preserved scope; H2A2 implementation UNSTARTED; all eight substantive
H2 gates unresolved; E0 HOLD. No scientific/client/runtime code was run by this circuit.

Normative inputs: `NS-001_H2A2_RUNTIME_TRUST_ROOT_DESIGN_v0.1.md` and
`NS-001_H2A2_RUNTIME_TRUST_ROOT_DESIGN_REVIEW_v0.1.md` in this directory at starting HEAD;
existing `H2_EVIDENCE_CONTRACT_DRAFT.md` and its eight gate requirements remain unchanged.
MUST/MUST NOT denote proposed future acceptance requirements, not observed controls.

## 1. Allowed claim and exclusions

Strongest allowed successful wording:

> VERIFIED single-file byte identity and immutable handoff within the declared trusted
> test harness: the exact expected bytes were validated against the frozen fixture
> identity and handed to the fixed non-executing consumer. No source execution verified.

This is not proof of execution of those bytes, interpreter/compiler identity, dependency
or runtime closure, process identity, arbitrary-code isolation, client identity, transport
integrity, response correctness, resource accounting, scientific validity, E0 execution,
project authority beyond H2A1, or resolution of any H2 gate. The label applies only after
implementation and independent acceptance evidence, never merely from this specification.
The trusted validator/harness, consumer implementation and host are explicit residual
assumptions; digest equality or a diagnostic receipt cannot authenticate their behavior
against a compromised host. This is not a production package or runtime trust anchor.

## 2. Exact fixture and byte identity

One payload file only, logical path `source.bin`, with exactly three bytes in hexadecimal
`61 62 63` (ASCII `abc`, NO newline). It is inert data, not an executable source program.
Its classification as the source input under test must never lead to interpreting it.

- Byte length: **3**.
- SHA-256: `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`.
- Filename/path IS part of the expected logical identity, in addition to byte identity.
- Case-sensitive exact ASCII spelling; no alternate separators, Unicode aliases, dot
  components, repeated separators, drive/UNC names, NUL, escaping or traversal.
- Line endings, BOMs and every other byte are significant. No trimming, decoding,
  normalization, decompression, re-encoding or text-mode read is permitted for payload.
- Source must be a regular file, not a symlink; aliases/hard links outside the dedicated
  fixture are refused (future acquisition must establish single-link policy or refuse).
- Numeric permissions, owner and mtime are NOT identity fields; regular-file type and
  readability are preconditions. Do not chmod or infer execution rights from permission
  bits. OS permissions alone are not an immutability guarantee. Inaccessible input refuses.

This fixture fixes expected identities independently of observed input. A future caller
cannot replace the expected digest with the observed digest and call that verification.
The three bytes and constants here may be embedded in synthetic tests; no fixture is
created by this document-only circuit. Real NS-001 source is not a permitted substitution.

## 3. Root, exact file set and acquisition interval

The **acquisition root** is a dedicated newly allocated temporary directory outside the
repository, datasets, credential/config and output locations. Its canonical absolute
path R is chosen and pinned by the trusted fixture harness BEFORE validation. It is an
input capability/locator, not a field accepted from the untrusted manifest. The validator
must require the supplied root to designate that bound directory, not another identical
copy. Wrong root is refusal even when its file bytes match.

R has no symlink components and must be a directory; its trailing slash convention is
one canonical absolute form without trailing slash (except filesystem root, which is
forbidden). No lexical normalization is used to silently accept another path. Root
creation/physical path is host-specific and explicitly excluded from deterministic output.
Logical root identity is fixed `ns001-h2a2-fixture-v1`. It does not claim a globally unique
filesystem/process identity. A review-approved binding primitive must connect R to the
actual acquired directory object; a mutable pathname string alone is not that primitive.

Initial direct-member set MUST equal exactly `{manifest.json, source.bin}`. Both must
be regular, readable, non-symlink, single-link files. No other material is allowed:
no hidden files, extra regular files, nested directories/files, empty subdirectories,
symlinks (including dangling links), devices, sockets, FIFOs or other special entries.
Do not follow links, traverse unexpected directories, open device/FIFO/socket entries or
read unexpected file contents. Directories are significant: only R itself is allowed.
Manifest is the one permitted metadata file; its bytes are not payload source bytes.

The trusted synthetic harness controls mutation scheduling. During acquisition it must
maintain exclusive ownership of the fixture directory or use a reviewed equivalent
stable observation mechanism; evidence of change or inability to establish that boundary
refuses. A before/after directory scan alone is not proof against an unconstrained attacker.
This first slice makes no concurrent hostile-filesystem guarantee outside that assumption.
No arbitrary path scanning, credentials, live input or network observation is permitted.

## 4. Manifest: exact schema and bytes

Exactly one JSON object, four fields, no array of paths and no optional fields:

| Key | Required exact domain/value |
| --- | --- |
| schema | string `ns001.h2a2.single-file.v1` |
| path | string `source.bin` |
| byte_length | integer 3; booleans, floats, exponent and negative forms prohibited |
| sha256 | lowercase 64-hex string `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` |

No source commit/tree is included: the claim is the frozen synthetic file, not Git
source provenance. No paths to runtimes, clients, interpreters or configuration exist.
Canonical serialization C: UTF-8 restricted to ASCII here, lexicographically sorted keys,
compact JSON separators `,` and `:`, no whitespace/BOM/final newline, no unnecessary escape
forms, and decimal integer representation. Canonical input bytes must match C(parsed value)
exactly after duplicate-aware parse and semantic checks; a parser must not erase duplicates
before testing them. Source bytes themselves are never parsed as JSON.

The exact manifest bytes (the fence delimiters and following newline are NOT part of it):

```json
{"byte_length":3,"path":"source.bin","schema":"ns001.h2a2.single-file.v1","sha256":"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"}
```

Manifest SHA-256 M = `4a9ebe2c4e275600d9a6c7864bb14c3d5a4c0b6a7c8bbf88193fc48f76affce0`.
Only these canonical bytes are accepted. Missing keys, unknown fields, wrong version,
wrong field types/values, duplicate keys and alternate serialization refuse. Duplicate
`path` key is specifically DUPLICATE_PATH; other duplicate keys are DUPLICATE_KEY.
Arrays/extra entries or a path list refuse SCHEMA_TYPE: duplicate-path lists are not a
supported representation. Traversal or absolute-path values refuse before canonical-byte
comparison; any other path differing from `source.bin` refuses FILE_PATH.
Manifest reading is bounded at 1024 bytes plus one overflow-detection byte; overflow refuses
MANIFEST_SIZE. No repair, best effort, inferred defaults or manifest regeneration.

## 5. Snapshot: minimal in-memory value, not a directory/archive

The **snapshot** is a protected immutable logical value containing only:

1. the retained three payload bytes;
2. the retained exact canonical manifest bytes;
3. the fixed logical root ID.

Parsed file identity, manifest digest and snapshot identity are derivable, not additional
mutable authority. No filesystem path, archive, timestamp, source commit, process ID,
plugin, executable or extra content belongs to this snapshot. Physical root contents
are acquisition inputs; the snapshot is their minimal accepted byte representation.
Payload cardinality is one; acquisition file cardinality is two including metadata.

The snapshot descriptor D has this exact canonical form:

```json
{"file":{"byte_length":3,"path":"source.bin","schema":"ns001.h2a2.single-file.v1","sha256":"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"},"manifest_sha256":"4a9ebe2c4e275600d9a6c7864bb14c3d5a4c0b6a7c8bbf88193fc48f76affce0","root_id":"ns001-h2a2-fixture-v1","schema":"ns001.h2a2.snapshot.v1"}
```

Snapshot identity S = SHA-256(C(D)) = `0ae1c30f2568188390fe05d092609eb122f3bee16c48f41fae9fe3f08e6ba432`.
“Snapshot root/hash” means S, not R, not a Git tree, not a Merkle root and not a security
trust root. Root identity in receipts is the logical root ID plus S. D includes the full
file identity and M; consequently it binds metadata and the payload's expected hash/length.
The independently frozen expected F, M and S are constants of this specification. Wrong
external expected values must be refused, not adopted as replacements for the constants.

## 6. Validation order and immutable handoff

Logical stages, in this order: policy/consumer binding; root binding; directory safety and
membership; manifest parsing/semantics/canonical bytes; source acquisition/identity;
snapshot finalization; protected handoff; consumer identity confirmation/result; final
receipt. On first failed stage, stop. Never invoke consumer on pre-handoff refusal.

The validator must retain the acquired immutable payload/manifest value, calculate identity
from those same retained bytes, and bind it to a single successful validation event. That
exact bound object instance/capability is delivered to the fixed consumer. No pathname is
reopened for consumption; no path A→path B substitution, lazily read file, mutable caller
buffer alias, substituted object (even with equal bytes) or switched consumer is allowed.
The binding between validation event and delivered object must be observed by the trusted
harness, independently of consumer self-report. The object token is private ephemeral
state, never a serialized memory address/nonce that would break deterministic receipt bytes.

Acceptable realizations are a sealed/immutable buffer or an equivalent reviewed protected
object. A read-only FD is NOT sufficient if another writer can change its backing file.
An immutable copy or content-addressed object is acceptable only with proof that the
backing bytes cannot change, the verified object is the consumed object and the consumer
cannot reopen by name. A name containing a hash does not establish immutability.
No concrete OS/API/loader mechanism is selected here; failure to meet these requirements
is REFUSE, not permission to claim an equivalent implementation without review.

Phase-specific mutation rule (no original-or-refuse ambiguity):

- Before/during acquisition: wrong bytes or unsafe/unstable input MUST REFUSE.
- After successful immutable snapshot finalization: deterministic deletion/replacement
  of the original source pathname alone MUST NOT be reread; correct retained snapshot
  consumption still ACCEPTS. This is a positive isolation test, not current-directory
  integrity. No claim about later backing-root membership is made.
- Mutation/substitution of the retained handoff object or its bound association at any
  pre-consumer handoff checkpoint MUST REFUSE. This differs from changing the obsolete
  backing pathname. Consumer substitution at that checkpoint also MUST REFUSE.

Mutation must be induced at fixed test checkpoints, not sleeps/timing races. If a required
protection cannot be demonstrated, REFUSE HANDOFF_UNPROTECTED. No mutation is allowed to
become consumer input. Snapshot protection lasts until the consumer has completed.

## 7. Fixed non-executing consumer

Semantic consumer version/entrypoint ID: `ns001.h2a2.identity-consumer.v1` / `consume`.
It is fixed by the trusted test harness before validation, not chosen by the manifest,
source file or a run-time caller callback. Its sole allowed action is to receive the
bound immutable snapshot, recompute byte count/F/M/S from its content, compare them to
the frozen constants, return the deterministic identity tuple, and stop. It may not
interpret/decode the payload, evaluate/compile/execute source, spawn a process, invoke
a compiler/interpreter on input, open a pathname, import a plugin, access network or
credentials, or mutate input. Implementation code necessarily runs in a test engine;
this is NOT execution of input bytes and makes no engine-identity assurance claim.

Consumer identity C_ID consists of the fixed version, entrypoint and SHA-256 C_SRC of
its exact future implementation source artifact. That artifact must be reviewed and
pinned separately before acceptance runs; expected C_SRC must not be read from snapshot
or chosen by the candidate at run time. No implementation exists now, so no source hash
is fabricated. If consumer shares the proposed module with validator, C_SRC hashes that
entire exact module; no ambiguous source-span hashing. Dynamic dispatch/plugin selection
is forbidden. Wrong/missing expected or observed consumer identity refuses.

The internal consumer result is exactly a four-key object: byte_length (integer 3),
sha256 (F), manifest_sha256 (M), snapshot_sha256 (S). No other keys or values are allowed.
It is not an outcome/receipt and contains no ACCEPT label.

The reviewed consumer source hash is a required externally pinned test parameter, not an
additional manifest field. The fixed semantic contract is fully defined here; concrete
consumer bytes and protection mechanism remain pre-acceptance implementation obligations.
No receipt may use a placeholder, zero digest or hash of this prose as C_SRC.

## 8. Outcomes, refusal codes and precedence

Exactly two top-level results: ACCEPT or REFUSE. No warning-success, partial success,
auto-repair or retries. REFUSE never embeds a success/ACCEPT consumer receipt. A consumer
result is internal and cannot itself assert ACCEPT; only the validator may finalize ACCEPT
after all checks. If final evidence cannot be produced, there is no successful outcome;
crash/non-delivery is an unsuccessful test, never inferred ACCEPT.

Stable reason codes below; within a phase choose the first applicable listed code.
Entry names are inspected in bytewise lexicographic order; do not depend on filesystem
iteration order. Tests below contain one intentional defect unless specified otherwise.

| Phase | Codes in priority order and triggering condition |
| --- | --- |
| Policy | EXPECTED_IDENTITY (external expected F/length/M/S differs from this frozen spec); CONSUMER_IDENTITY (missing/mismatched pinned version/entrypoint/C_SRC or consumer selection) |
| Root | ROOT_MISMATCH (supplied root not bound R); ROOT_MISSING (bound R absent); ROOT_TYPE (R not directory); SYMLINK (root/ancestor link); ROOT_UNSTABLE (bound directory cannot be stably observed); IO_ERROR (unreadable root) |
| Members | SYMLINK (any direct link); ENTRY_TYPE (device/socket/FIFO/other nonregular member including nested/empty directory); FILE_ALIAS (hard-link policy failure); FILE_MISSING (source.bin absent); MANIFEST_MISSING (manifest.json absent); EXTRA_FILE (any other regular member, including hidden/.pyc files); IO_ERROR (metadata/acquisition failure) |
| Manifest syntax | MANIFEST_SIZE; MANIFEST_MALFORMED (invalid UTF-8/JSON); DUPLICATE_PATH (duplicate path key); DUPLICATE_KEY (other duplicate key); SCHEMA_TYPE (not one object or field wrong type); MANIFEST_FIELD_MISSING; MANIFEST_FIELD_UNKNOWN; MANIFEST_VERSION |
| Manifest values | PATH_ABSOLUTE (leading slash, drive or UNC form); PATH_TRAVERSAL (dot/dot-dot component or separator escape); FILE_PATH (other wrong spelling); MANIFEST_LENGTH; MANIFEST_DIGEST; MANIFEST_NONCANONICAL (otherwise correct fields, non-C bytes); MANIFEST_HASH (canonical bytes do not match frozen M) |
| Source | IO_ERROR; FILE_LENGTH (not 3, bounded read maximum four bytes); FILE_DIGEST (3 bytes but SHA-256 not F) |
| Snapshot / handoff | SNAPSHOT_IDENTITY (computed D/S mismatch); HANDOFF_UNPROTECTED (no proven immutable association); HANDOFF_SUBSTITUTED (object/event association differs, including equal-byte replacement); HANDOFF_MUTATED (retained identity/content changed); CONSUMER_IDENTITY (consumer changed before delivery) |
| Consumer / result | CONSUMER_RESULT (exception, missing result, wrong tuple/count or nondeterministic/extra fields); EVIDENCE_INCOMPLETE (required independent handoff observation missing) |

Duplicate detection precedes constructing a dictionary; if multiple duplicate kinds occur,
DUPLICATE_PATH takes precedence. Unknown/missing keys are reported before per-value checks
once field types are valid. Invalid path strings are never used in an OS call.
Wrong file length cannot be “fixed” by trimming; wrong digest cannot be repaired by
replacing the expected value. A refused stage has no later side effects or consumption.

## 9. Deterministic evidence contract

Use C for all records: sorted keys, compact ASCII JSON, no BOM/trailing newline. Every
listed key is mandatory, all unlisted keys forbidden. Hex digests lowercase 64 characters.
No timestamp, clock, random nonce, PID, absolute temp path, exception text or platform
metadata occurs in canonical output. Diagnostic operational metadata, if ever needed,
must not be silently added; requires another contract. No secret content is reported.

Define H_ID = SHA-256(C({"consumer": C_ID, "schema":
"ns001.h2a2.handoff.v1", "snapshot_sha256": S})). This is a deterministic content-binding
identity, NOT proof of unique execution. Internal object association is separately
observed; identical reruns intentionally have identical receipts.

ACCEPT record exact keys/types:

| Key | Value |
| --- | --- |
| spec | `ns001.h2a2.snapshot-handoff.v0.1` |
| verdict | `ACCEPT` |
| root_id | `ns001-h2a2-fixture-v1` |
| snapshot_sha256 | S |
| path | `source.bin` |
| byte_length | integer 3 |
| sha256 | F |
| manifest_sha256 | M |
| consumer | object with only `version`, `entrypoint`, `source_sha256`; fixed values and pinned C_SRC |
| handoff_sha256 | H_ID |
| consumer_calls | integer 1 |
| handoff_observed | boolean true, from trusted harness, never input assertion |

REFUSE record exact keys: `spec` (same ID), `verdict` (`REFUSE`), `code` (one tabled code),
`handoff_succeeded` (false). No snapshot payload, consumer ACCEPT result or arbitrary
expected/observed text is emitted. Expected identities are the safe frozen constants
above; a code identifies the failed comparison. Optional observed fields are deliberately
omitted to avoid untrusted data leaks, unstable messages and schema ambiguity.
“handoff_succeeded:false” means no fully accepted handoff/result claim; after-consumer
failure may have invoked the consumer, but must not claim successful validation/handoff.

A record's evidence digest is SHA-256 of its canonical bytes, kept separately by the
retaining receipt/inventory (not recursively inside the record). An independent harness
retains fixture/mutation ID, expected result/code, actual canonical record, record digest,
consumer invocation count and before/after object-association checks. Tests must verify
those observations independently of consumer-returned identity. Refusal before delivery
requires zero consumer calls. A result-stage refusal may have one call, never two.
No bare self-reported handoff_observed flag is sufficient evidence.

## 10. Exact positive and isolation tests

Positive P1: R contains only source.bin with bytes 61 62 63 and manifest.json with the
exact canonical bytes above; pinned constants, bound R, approved immutable mechanism
and fixed reviewed C_ID. Acquire/verify exactly once, finalize S, deliver the same bound
immutable value exactly once, and get exactly matching identity tuple. Outcome ACCEPT;
record equals the canonical ACCEPT template with that pinned C_SRC/H_ID, byte for byte.
The test harness's oracle uses frozen constants, not observed candidate output.

Minimum evidence: exact fixture/manifest bytes, constants, approved consumer source hash,
reviewed mechanism/test source identity, independent received-object association and
byte equality, invocation count 1, actual/expected canonical receipt and receipt digest.
Repeat P1 in fresh equivalent roots twice: identical receipt bytes/digest required.

Isolation P2: after successful snapshot finalization, replace original source file with
three wrong bytes at a deterministic checkpoint. Original retained snapshot is delivered;
P1's exact ACCEPT receipt remains unchanged. Repeat with deletion of original source.
This does not permit handoff-object mutation or assert current root integrity. It proves
only no source pathname reread after validation under the controlled harness boundary.

## 11. Required bounded negative matrix

For each row, verdict is REFUSE and no consumer/outer record may indicate ACCEPT.
Unless the row explicitly targets post-validation state, mutate only the named input
before acquisition. Retain the expected code and zero consumer calls for all pre-delivery
refusals. No exhaustive fuzzing is required.

| ID | Mutation from P1 | Required code |
| --- | --- | --- |
| N01 | source bytes `abd` (change final byte) | FILE_DIGEST |
| N02 | source bytes `ab` (truncate one byte) | FILE_LENGTH |
| N03 | source bytes `abcd` (append one byte) | FILE_LENGTH |
| N04 | rename source.bin to other.bin | FILE_MISSING (precedes extra-file) |
| N05 | remove source.bin initially | FILE_MISSING |
| N06 | add unexpected regular file extra.bin | EXTRA_FILE |
| N07 | replace source.bin with symlink, target not followed | SYMLINK |
| N08 | manifest sha256 first hex digit changed to another valid lowercase hex digit | MANIFEST_DIGEST |
| N09 | manifest byte_length integer 4 | MANIFEST_LENGTH |
| N10 | duplicate schema key in raw JSON, even equal values | DUPLICATE_KEY |
| N11 | remove sha256 manifest key | MANIFEST_FIELD_MISSING |
| N12 | supply different existing root containing identical fixture bytes | ROOT_MISMATCH |
| N13 | after validation, replace bound snapshot object with another equal-byte object | HANDOFF_SUBSTITUTED |
| N14 | wrong consumer version/entrypoint/source identity before validation or delivery | CONSUMER_IDENTITY |
| N15 | remove manifest.json | MANIFEST_MISSING |
| N16 | manifest raw bytes `{` | MANIFEST_MALFORMED |
| N17 | add unknown key x with string value | MANIFEST_FIELD_UNKNOWN |
| N18 | set schema to ns001.h2a2.single-file.v2 | MANIFEST_VERSION |
| N19 | manifest path ../source.bin | PATH_TRAVERSAL |
| N20 | manifest path /source.bin | PATH_ABSOLUTE |
| N21 | duplicate path key even with same value | DUPLICATE_PATH |
| N22 | change externally expected F, length, M or S (one per subcase) | EXPECTED_IDENTITY |
| N23 | bound R does not exist | ROOT_MISSING |
| N24 | add .hidden or source.pyc regular file (separate subcases) | EXTRA_FILE |
| N25 | add nested directory, socket, FIFO or special entry (safe synthetic metadata stub if host cannot create safely) | ENTRY_TYPE |
| N26 | present mutable/unprotected snapshot backing at handoff | HANDOFF_UNPROTECTED |
| N27 | inject changed retained content at protected-boundary checkpoint without changing event association | HANDOFF_MUTATED; if protection prevents injection, prove attempted mutation was refused, then use a test double only for refusal-branch coverage and label it synthetic |
| N28 | correct manifest values with an added final newline | MANIFEST_NONCANONICAL |
| N29 | manifest path other.bin | FILE_PATH |
| N30 | missing or wrong fixed-consumer result | CONSUMER_RESULT (one call allowed, no ACCEPT) |
| N31 | omit independent handoff observation | EVIDENCE_INCOMPLETE |

N25 stubs prove validator dispatch/refusal logic only, not real OS acquisition protection;
actual supported regular/link/root acquisition requires separate concrete acceptance.
N27 must not weaken immutable protection just to allow a mutation; any simulated breach
is marked fault injection and cannot stand in for a real protection test. Failure of a
required genuine-path test remains a gap, not a reason to relabel a stub as integration.
Tests not applicable to a claimed primitive must yield an explicit acceptance gap, never
silent success. Root symlink, non-directory root, unsupported aliases, unreadability and
oversize manifest require refusal-code unit cases as part of the same bounded matrix.

## 12. Determinism and non-claims

Same frozen constants + same logical fixture bytes + same approved consumer source +
same contract and test checkpoint sequence MUST yield identical verdict and canonical
receipt bytes, irrespective of temporary physical root location or wall time. REFUSE
priority above prevents arbitrary choice of reason. Host I/O failures are different
observed conditions, not identical inputs; they map to stable refusal codes without
nondeterministic message text. No retry disguises a failure.

No ACCEPT is possible without frozen C_SRC and independently checked handoff association.
S and H_ID bind content and semantic roles, not execution uniqueness or process identity.
A copied old ACCEPT record cannot serve as a fresh independent test: the reviewing harness
must observe that test's calls/association. This does not implement an execution receipt
system or cryptographic attestation service.

## 13. Future implementation boundary and authorization threshold

Proposed add-only allowlist (NOT created/authorized by this circuit):

- `e0/h2/runtime_trust_root.py`: validator and fixed non-executing consume entrypoint
  in one new module; entire module is consumer source artifact for C_SRC.
- `tests/test_e0_h2_runtime_trust_root.py`: embedded abc/manifest fixture constants,
  independent positive/isolation oracles and bounded negative matrix. No tracked fixture
  directory or external dependencies necessary merely for representing these inputs.
- `docs/e0/h2/NS-001_H2A2_RUNTIME_TRUST_ROOT_IMPLEMENTATION_RECEIPT_v0.1.md`: preserved
  source identities, reviewed mechanism assumptions, exact acceptance outputs and gaps.

No generalized source loader, executable callback, manifest package builder, production
integration or filesystem-wide scanner. Fixture files only in fresh approved external
temporary roots during a later expressly authorized test. No implementation file now.

Forbidden paths/objects: all `docs/e0/h2/H2A1_*`, `docs/e0/h2/NS-001_H2A1_*`,
`docs/e0/h2/evidence/**`, all prior H2A2 receipts; `e0/h2/evidence_contract.py`,
`e0/h2/external_anchor_verifier.py` and their tests; `e0/hardening.py` and its tests;
`preregistrations/e0/**` including the frozen preregistration and sidecar;
`ns001_tau_check.py`, `run_experiment.py`, `EXPERIMENT.md`, `protocols/**`,
`docs/e1-openai/**`, `Dockerfile`, `requirements.txt`, `Makefile`, `README.md`,
`.github/workflows/**`, `.gitignore`, `.dockerignore`; retained/published H1 archives,
release/tag/assets/settings/attestations; live-client code, credential stores, .env and
home configuration, datasets, scientific outputs/results and existing run directories.
All other writes are forbidden except Git bookkeeping for explicitly allowed preservation.

Before implementation authorization: independently accept this exact claim, byte fixture,
manifest schema, root binding/file-set policy, snapshot/protection semantics, consumer
semantic identity, code priority, positive/negative matrix and canonical evidence contract;
select/review one realizable primitive and test-engine assumptions; authorize only the
three proposed paths. No fabricated future implementation hash is a prerequisite to
writing code, but concrete reviewed C_SRC and implementation source identity must be fixed
BEFORE any acceptance run or PASS claim. Candidate code cannot approve its own identity.

Implementation readiness: **PARTIAL**. Behavioral specification is now concrete; independent
acceptance and implementation-specific root/object binding selection remain required.
No implementation/consumer hash is available or approved yet. This specification's existence
is neither a test pass nor implementation authorization. If the chosen environment cannot
provide the binding, STOP rather than broaden scope or weaken the claim.

## 14. H2 relation and preservation

This slice could provide narrowly scoped synthetic evidence for verified-byte retention
and hash-to-handoff substitution refusal within external_trust_root. It cannot alone prove
exact_verified_bytes_executed because input is never executed; nor does ignoring/rejecting
an adjacent .pyc prove arbitrary runtime import safety. Authoritative primary evidence,
retained provenance and independent gate review remain separate contract slots.
Dependency_runtime_lock is only an interface/trusted-engine assumption here. client_source,
response_contract, transport_accounting, maximum_partition_memory, amendment_freeze and
final_manifest_package_audit are outside this slice. All eight gates stay unresolved.

This circuit consists only of text inspection, specification writing, administrative hash
calculation/blob comparison and requested Git preservation. Computing fixture/manifest
constants is not executing a fixture, proposed runtime, client or scientific code. No
acceptance tests, implementation, interpreter invocation on payload or live calls occurred.
Before commit, compare all pre-existing tracked files with starting HEAD, require this
one new file only, verify frozen preregistration digest/sidecar, and stage only this file.

Observed preservation check: PASS. All 193 prior tracked files are byte-identical
to starting HEAD, including all H2A1/H2A2 records and tracked scientific artifacts.
Frozen preregistration and sidecar match the expected digest. Only this specification
is new. No proposed runtime, client, fixture or scientific execution occurred.

## Closing contract

- Allowed claim: byte-exact single-file validation and immutable handoff to the fixed non-executing consumer within trusted harness; not source execution.
- Prohibited claims: executed source, runtime/interpreter/dependency/process/client/transport/response/resource/scientific/E0 proof or any whole H2 gate pass.
- Snapshot definition: minimal immutable in-memory logical value containing payload bytes, canonical manifest bytes and fixed root ID; descriptor S binds content, not execution.
- Manifest definition: one canonical four-key ASCII JSON object; exact path, length, SHA-256 and schema; no optional/unknown/duplicate fields.
- Root/file-set rule: independently bound canonical temporary R; exactly source.bin and manifest.json, both regular single-link files; no other entries, links, directories or special objects.
- Immutable-handoff rule: same protected retained object bound to successful validation; no reopen, mutable alias, substitute object or consumer switch; backing-path change after snapshot has no effect.
- Fixed-consumer definition: identity-consumer.v1 consume, reviewed whole-module source SHA-256 pinned before tests; count/hash/compare immutable bytes and return identity tuple only.
- ACCEPT criteria: all ordered checks, fixed identity and independent same-object observation pass; exactly one fixed consumer call and exact canonical receipt.
- REFUSE criteria: first applicable stable code; no best effort, retry, repair or ACCEPT record; pre-delivery refusals invoke no consumer.
- Required positive test: exact abc bytes/manifest/root and reviewed consumer/protection; twice identical ACCEPT bytes; original-path replacement/deletion isolation case also fixed.
- Required negative tests: N01–N31 and specified root/type/I/O/size cases with stable codes, controlled checkpoints and explicit synthetic-versus-real-path limitations.
- Deterministic evidence contract: canonical sorted compact ASCII JSON without time/path/PID/random fields; externally retained receipt digest, content-binding H_ID and independent observer evidence.
- Future implementation paths: three proposed new module/test/implementation-receipt paths only, separately authorized; none created now.
- Forbidden paths: all prior H2A1/H2A2/frozen/scientific/runtime/client/workflow/publication/credential/data material and all unlisted writes.
- H2 gate relationship: narrow synthetic external_trust_root evidence only; dependency/runtime interface deferred; all eight gates unresolved.
- Implementation-ready: **PARTIAL**; requires independent specification acceptance, concrete binding-primitive review and separate implementation authorization; actual consumer source pin required before acceptance runs.
- H2A1 status: **VERIFIED within preserved scope**, unchanged.
- H2A2 status: **acceptance specification recorded; implementation UNSTARTED**.
- E0 status: **HOLD**; Gate 1 PARTIAL, unchanged.
- One next bounded action only: obtain independent read-only acceptance review of this exact specification and binding-primitive prerequisites. Not performed here.
