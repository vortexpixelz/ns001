# DRAFT — NS-001 H2 declaration contract

**Contract phase:** `DRAFT_H2A0_DECLARATIONS_ONLY` (`contract_phase`).
**Execution status:** invariantly **HOLD** (`overall_status`). The draft phase
is lifecycle metadata and grants no authorization.

**Authority:** This document and its Python module are not evidence
verification, a gate decision, an amendment, an execution package, a readiness
decision, E0 authorization, or permission to use credentials or a network.

## Pure H2A0 scope

H2A0 fixes JSON declaration shapes, expected values, declaration ordering,
within-submission identity-reuse rules, and the names of later-H2 verifier roles.
It cannot authenticate a declaration's category, origin, authority, custody,
verifier, rule result, resolution, or external identity. It does not inspect Git,
the filesystem, credentials, retained evidence stores, audit bundles, or remote
services.

The module can report only that one declaration submission covers the required
schema slots. Schema coverage does not mean evidence was verified, a rule
passed, a substantive gate was resolved, or execution was authorized. All eight
substantive H2 gates remain unresolved after every successful H2A0 call.

## Expected anchor declarations

The contract carries four expected values:

- expected H1 checkpoint commit:
  `6e33cb9ca7019e50e2f247ade9ae8c9a7b40d3ff`
- expected scientific base commit:
  `0393315223df8ed90f20f0c821508cc98bea08d1`
- expected frozen preregistration SHA-256:
  `a2a8523c065d4d41155aa29d367c888d49ab3032f6075b8cebbd2475ff1efd78`
- expected H1 audit bundle SHA-256:
  `a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f`

These are declarations, not observations. H2A0 checks that the submitted
contract contains these exact expected strings. It does not verify current Git
HEAD, ancestry, preregistration bytes, sidecar bytes, or audit-bundle bytes. A
later `external_anchor_verifier` must obtain independently anchored observations,
compare them with these expected declarations, and retain its inputs and result.

The contract hash is computed from deterministic UTF-8 JSON with sorted object
keys and no insignificant whitespace. It is carried by a gate declaration
submission and is not inserted into the contract itself, avoiding
self-reference. This hash identifies the declaration contract only; it does not
authenticate the expected anchors or any evidence.

## Evidence declarations and later verifier ownership

Every record contains declared category, subject, origin, authority, custody,
verifier, resolution, identity metadata, and rule results. H2A0 validates their
exact schema and types only. In particular, `declared_passed: true` is a claim,
not proof, and a record labelled `authoritative_primary` is not thereby
authoritative.

Later H2 must authenticate each declaration as follows:

| Declaration | H2A0 treatment | Required later-H2 verifier |
| --- | --- | --- |
| expected anchors | exact expected strings | `external_anchor_verifier` |
| `authoritative_primary` category and authority/content declarations | unauthenticated labels | `later_h2.authority_and_content_verifier` |
| retained origin, custody, and byte identity | unauthenticated metadata | `later_h2.origin_custody_and_retained_bytes_verifier` |
| `synthetic_test` category and claimed behavior | unauthenticated labels/results | `later_h2.synthetic_execution_verifier` |
| `reported_not_reproduced` attribution | unauthenticated report metadata | `later_h2.report_attribution_verifier` |
| unresolved claims and declared resolution | unauthenticated state | `later_h2.claim_resolution_verifier` |
| declared verifier identity/independence | unauthenticated identity | the applicable later verifier plus independent review |
| each `declared_passed` rule result | unauthenticated boolean | the requirement's category verifier named in the contract |

The contract records the fully qualified later-verifier role for every required
category. Those verifier roles are future responsibilities; H2A0 implements
none of them. The draft-only `external_anchor_verifier` is a later-H2
responsibility, not a category-verifier identifier emitted by this contract.

## Supplied-byte consistency and identity reuse

An identity declaration contains an algorithm, artifact name, declared expected
SHA-256, declared observed SHA-256, and declared byte count. Metadata validation
does not claim that these values match any bytes.

The optional pure supplied-byte consistency function accepts exact bytes
directly and can recompute their SHA-256 and length against one immutable
identity declaration. Success establishes only that those caller-supplied bytes
match the declared digest and length. It does not establish that the bytes came
from the declared origin, were retained, were executed, are authoritative, or
support a rule result.

Within one gate declaration submission, the canonical declared byte identity is
the tuple `(algorithm, declared_observed_sha256, declared_byte_count)`. Reuse of
that tuple across distinct requirement slots is forbidden, even when free-form
`evidence_id` values or artifact names differ. Consequently, one declared byte
identity cannot occupy authoritative, provenance, synthetic, or reported-only
slots in the same gate. A later retained-bytes verifier must determine whether
different declarations actually refer to identical bytes and apply the same
no-reuse rule to its observations.

## Eight unresolved substantive gates

The declaration contract fixes required slots and later-verifier rules for:

1. `external_trust_root`
2. `client_source`
3. `response_contract`
4. `transport_accounting`
5. `dependency_runtime_lock`
6. `maximum_partition_memory`
7. `amendment_freeze`
8. `final_manifest_package_audit`

A submission must bind the exact declaration-contract hash and contain each
required declaration once, in contract order, with the required declared
category and complete ordered rule-ID declarations. Missing, extra, unknown,
duplicated, or out-of-order slots are structural refusals. Repeated free-form
IDs and repeated canonical declared byte identities are separate structural
refusals. Declared rule booleans and declared resolution values never change the
substantive state: every gate remains unresolved and overall status remains
`HOLD`.

Validated contracts are created only by `validate_evidence_contract()`.
The exported evidence declaration constructors validate exact scalar types and
nested domain types. Supported list/tuple inputs for rule and requirement
collections are defensively reconstructed into tuples with immutable elements.
Validated values and normally constructed declarations retain no caller-owned
mutable aliases. `to_json_value()` explicitly returns a fresh mutable JSON
copy; changing that copy cannot change the validated contract.

Successful `GateDeclarationSubmissionCoverage` and `SuppliedBytesIdentityCheck`
objects are factory-only: use `validate_gate_declaration_submission()` and
`check_supplied_bytes_against_identity_declaration()`, respectively. Direct
construction (including dataclass replacement) refuses, so an ordinary caller
cannot fabricate a successful result without invoking the relevant checks.
The coverage result's `overall_status` property is the exact literal `HOLD`;
`evidence_verified` and `substantive_gate_resolved` are always false.

These guarantees cover ordinary supported API use. Reflection, private-member
tampering, and deliberate Python object-model subversion are outside this H2A0
boundary. No broader Python security boundary is claimed.

## H2A0 capability boundary

`e0/h2/evidence_contract.py` only parses, canonicalizes, hashes supplied values,
validates declaration schemas, reconstructs immutable declarations, checks
within-submission declared identity reuse, and optionally compares bytes passed
directly by its caller with declared hash/length metadata.

It has no credential lookup, environment-secret lookup, transport, network,
subprocess, dynamic-import, filesystem-write, production adapter,
amendment-freeze writer, final-manifest generator, package builder, readiness
transition, E0 authorization, or E0 execution path. Ordinary Python source
loading is not itself treated as a violation; the regression test installs
capability blockers before executing already-read module source bytes. With
standard-library dependencies already loaded, direct application file reads
(including credential files), filesystem writes, and `input()` are blocked.
Inert read/write/prompt probes verify these blockers without accessing any
credential file or accepting input.

H2A1 and later work must implement and independently review the external
verifiers and real evidence. This draft does not begin that work. Even if later
work eventually resolves every H2 gate, E0 still requires separate explicit
authorization.
