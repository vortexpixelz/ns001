# NS-001 H2A2 runtime trust-root correction receipt v0.1

## Authorized bounded result

Starting branch `codex/e0-h2-preparation`, HEAD
`c38a9b2bbb7840af831aed5a1948360301796fec`. This circuit corrects only B1–B3 from
`NS-001_H2A2_RUNTIME_TRUST_ROOT_IMPLEMENTATION_REVIEW_v0.1.md`. It continues the
existing working-tree edits after interruption; no circuit restart or replacement of
those edits occurred. The acceptance specification, mechanism-selection document,
implementation receipt and independent review remain unchanged as historical evidence.

**PASS: all three defects FIXED within the frozen offline synthetic scope.** The complete
bounded suite passed once after correction: **88 cases: 4 positive/isolation ACCEPT and
84 expected REFUSE**. No failing correction acceptance run, skipped required case, repair
of a refused transaction, or retry of a failed handoff occurred. The new cases concern
only the reviewed acquisition and incomplete-read boundaries; N31 was corrected in place.
No broad fuzzing, live integration or scientific execution was performed.

The implementation-slice verdict is VERIFIED WITH RESIDUAL ASSUMPTION for this local
synthetic contract. Full external_trust_root and all eight substantive gates remain
unresolved. Independent review of the correction remains a separate next circuit.

## B1: exact input length, complete read and EOF

Oversized-input defect: **FIXED**.

For source.bin, the opened regular single-link file must have fstat size exactly three.
For manifest.json, the opened file size must not exceed the frozen 1024-byte limit. After
checking identity/stability against the bound initial metadata, acquisition performs its
bounded read and requires the returned length to equal the opened object's full size.
Incomplete acquisition returns IO_ERROR; it is not completed by a retry or accepted as a
matching prefix. An additional one-byte read must return EOF. A trailing source byte
returns FILE_LENGTH; trailing manifest data at that probe returns MANIFEST_NONCANONICAL.
Opened-object metadata is rechecked, followed by the existing directory/member stability
check. Hashing therefore covers the complete accepted source, not merely a prefix.

This is an explicit EOF probe, not a repair loop, second acquisition or pathname reopen.
As before, the trusted harness owns the synthetic acquisition interval; these checks do
not claim protection against an unconstrained malicious filesystem/kernel.

| Case | Expected and actual result |
| --- | --- |
| P1 and P1-repeat | Exact three-byte input ACCEPT |
| N02 | One-byte truncation REFUSE / FILE_LENGTH |
| N03 | One-byte append REFUSE / FILE_LENGTH |
| B1-large-tail | 4096 trailing bytes REFUSE / FILE_LENGTH |
| B1-source-prefix | Four-byte source with short-read adapter REFUSE / FILE_LENGTH before read |
| B1-manifest-oversize-prefix | Oversized manifest with canonical-prefix adapter REFUSE / MANIFEST_SIZE before read |
| B1-manifest-trailing-prefix | Allowed-size manifest with unread trailing byte REFUSE / IO_ERROR |
| B1-incomplete-source | Correct-size source, incomplete two-byte read REFUSE / IO_ERROR |
| B1-eof-extra-byte | Scheduled real append before EOF probe REFUSE / FILE_LENGTH |

The first two prefix adapters are intentionally not reached because their actual size
already refuses. The incomplete-read adapters use real file descriptors but request fewer
bytes; they are synthetic fault scheduling, not evidence of spontaneous kernel failure.
The EOF test appends only to its disposable synthetic fixture.

## B2: frozen memfd read-code distinction

Memfd short-read refusal-code defect: **FIXED**.

Expected code for an incomplete protected-object read: **MEMFD_COPY_IO**. The mechanism
selection receipt section 5 orders error/short write or read before size/read-length
mismatch. A genuinely shorter complete object remains **MEMFD_COPY_SIZE**. No code was
invented, and neither condition can ACCEPT.

`_copy_check` compares returned bytes with the amount obtainable from the observed file
size and the four-byte bounded request. A partial result refuses MEMFD_COPY_IO before the
exact three-byte size/hash checks. Tests B2-short-read-before-seal and
B2-short-read-after-seal independently force a two-byte positioned read of an actual
three-byte memfd and both return MEMFD_COPY_IO. Existing M11-2 and M11-4 still report
MEMFD_COPY_SIZE for complete reads of wrong-size copies. No byte mutation is implied by
an incomplete read. The seal mechanism, exact Q and no-fallback rule are unchanged.

## B3: independent evidence gates final ACCEPT

N31 defect: **FIXED**.

`run` now returns either a canonical REFUSE or internal PendingHandoff measurements.
PendingHandoff is not a verdict, serialized receipt or third top-level outcome; it
contains the successful role measurements without asserting ACCEPT. Only `finalize`
can serialize ACCEPT, after receiving the separately reviewed harness's HandoffEvidence.
It checks completeness, exact boolean observations, actual one-call counts and intact
role results before emitting the existing canonical schema. The outward outcomes remain
only ACCEPT/REFUSE. No callback, dynamic consumer or new runtime mechanism is introduced.

The harness computes this evidence from its own recorded creation/duplication, copy/seal,
role stat/query/read, association and no-reopen observations. It now counts actual role
function entries with a bounded Python profile hook rather than equating reads with
invocations; the previous profile state is restored during cleanup. This is evidence
bookkeeping for B3, not a new runtime-identity claim or a general profiler.

**Exact N31 omission:** withhold the independent same-object association observations
from Trace while preserving both consumer and observer results, creation and duplication
observations, copy/seal observations, no-reopen result and one call to each role. The test
asserts both role results still equal the independent oracle and every other evidence
component remains present. `same_object` is absent (None), so `finalize` emits exactly
EVIDENCE_INCOMPLETE. No ACCEPT bytes are constructed before that evidence check.

N31 actual canonical record SHA-256:
`182eb6b3f5c8349268cc51bce415fc383dac66aef8cded31870c8f54c7ee106c`.
This replaces the old test's removal of an observer-result argument. It does not remove
a role result and call that independent evidence loss. The old test and its limits remain
preserved in Git and the historical receipts.

Evidence remains supplied by the trusted reviewed harness; this is not an authentication
protocol against arbitrary callers forging evidence objects, compromised Python or a
malicious kernel. No new stronger claim is made.

## Complete bounded acceptance and source pins

The modified implementation/harness were inspected before running, then their whole-file
hashes were computed externally and supplied as literal pins. The harness checks those
pins before importing the new module. The successful command, run from the repository root:

```sh
env -i PATH=/usr/bin:/bin LC_ALL=C.UTF-8 /usr/bin/python3 -I -B -S tests/test_e0_h2_runtime_trust_root.py --implementation-sha256 d15ddd0b3d689592398987e62ce3135ee8a61e48ccd48cfa511d4870ac0b0023 --harness-sha256 67150d764cfde33e1d72837cf3ec518c3469a7f617ec19808d30c0762434b647
```

Exit status 0. All N01–N31 families, all M01–M15 families, prior appended required tests,
and the eight added short-read/size/EOF subcases passed. The four positive cases are P1,
P1-repeat, P2-replace and P2-delete; all share one positive predicate. No extra dependency,
fixture directory, external test discovery or network request was used. Bytecode writes
were disabled. Temporary synthetic files and descriptors were cleaned up by the harness.
Audit hooks continue to reject network/socket/subprocess/fork/exec operations during tests.
No E0 entrypoint, live client or scientific source was loaded/executed.

| Changed file | SHA-256 / purpose |
| --- | --- |
| `e0/h2/runtime_trust_root.py` | `d15ddd0b3d689592398987e62ce3135ee8a61e48ccd48cfa511d4870ac0b0023`; only B1 acquisition completeness, B2 refusal ordering, B3 evidence finalization |
| `tests/test_e0_h2_runtime_trust_root.py` | `67150d764cfde33e1d72837cf3ec518c3469a7f617ec19808d30c0762434b647`; corrected B3 observation target/counting, eight B1/B2 cases, existing bounded matrix retained |
| `docs/e0/h2/NS-001_H2A2_RUNTIME_TRUST_ROOT_CORRECTION_RECEIPT_v0.1.md` | This new correction receipt; no recursive self-hash |

## Kernel enforcement, same object and determinism

Kernel-enforcement verdict: **PASS**. M04 actual pwrite and M05 actual shrink/grow attempts
are denied with EPERM, with length/hash/Q unchanged. M13 actual writable shared mapping
causes F_ADD_SEALS to fail with EBUSY. Those kernel results are separate from the harness's
outer HANDOFF_MUTATION_ATTEMPT refusal and from injected errors, missing-seal state,
short-read adapters and equal-byte distinct-object substitutions. No synthetic result is
presented as kernel enforcement.

Same-object verdict: **PASS within the trusted harness**. One creator memfd is retained;
C/O are direct duplicated handles. Live device/inode corroboration and seven association
checkpoints remain, alongside separate consumer/observer reads and queries. N13/M06–M09
still refuse equal-byte distinct-object substitutions. Numeric descriptors and inode data
are not stable or cryptographic identities and are excluded from canonical output.

Determinism verdict: **PASS**. Four equal positive/isolation runs produce identical ACCEPT
bytes with SHA-256 `6b5bc733835004aeb9ea6ce3994f028f9c815f2556a11fb34a9fa4724ca5adce`. The schema has no timestamps,
nonces, PIDs, descriptor numbers or temporary paths. The new hash differs from the prior
implementation's receipt because the content includes the intentionally changed K/T source
pins; byte equality is required across equal runs of these corrected sources, not across
different implementation/harness identities.

Exact canonical ACCEPT bytes, excluding fence/newline framing:

```json
{"byte_length":3,"checks":{"consumer_calls":1,"copy_validated":true,"creation_witnessed":true,"duplication_witnessed":true,"no_reopen":true,"observer_calls":1,"same_object":true,"sealed_revalidated":true,"source_validated":true},"consumer":{"byte_length":3,"object_type":"sealed-memfd","reference_bound":true,"role":"consumer","seals":["F_SEAL_GROW","F_SEAL_SEAL","F_SEAL_SHRINK","F_SEAL_WRITE"],"sha256":"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","source_sha256":"d15ddd0b3d689592398987e62ce3135ee8a61e48ccd48cfa511d4870ac0b0023"},"harness_sha256":"67150d764cfde33e1d72837cf3ec518c3469a7f617ec19808d30c0762434b647","implementation_sha256":"d15ddd0b3d689592398987e62ce3135ee8a61e48ccd48cfa511d4870ac0b0023","manifest_sha256":"4a9ebe2c4e275600d9a6c7864bb14c3d5a4c0b6a7c8bbf88193fc48f76affce0","observer":{"byte_length":3,"object_type":"sealed-memfd","reference_bound":true,"role":"observer","seals":["F_SEAL_GROW","F_SEAL_SEAL","F_SEAL_SHRINK","F_SEAL_WRITE"],"sha256":"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","source_sha256":"d15ddd0b3d689592398987e62ce3135ee8a61e48ccd48cfa511d4870ac0b0023"},"profile":"ns001.h2a2.sealed-memfd.v1","snapshot_sha256":"0ae1c30f2568188390fe05d092609eb122f3bee16c48f41fae9fe3f08e6ba432","source_sha256":"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","verdict":"ACCEPT"}
```

Exact aggregate stdout follows, including its one final LF but excluding fence framing.
SHA-256: `43670acec3144ca5a9ff5fc95f81f42fbacfa7fccd80f77357df7835058c123e`.
It retains all 88 outcomes, canonical-record hashes, role invocation counts, fault labels
and observations. Expected codes are explicit in the pinned harness and compared before
inclusion. REFUSE bytes reconstruct exactly from the fixed profile, verdict REFUSE,
recorded code and handoff_succeeded=false using sorted compact ASCII JSON. No local cache
or uncommitted output file is needed to recover this evidence.

```json
{"accept_sha256":"6b5bc733835004aeb9ea6ce3994f028f9c815f2556a11fb34a9fa4724ca5adce","all_passed":true,"canonical_accept":"{\"byte_length\":3,\"checks\":{\"consumer_calls\":1,\"copy_validated\":true,\"creation_witnessed\":true,\"duplication_witnessed\":true,\"no_reopen\":true,\"observer_calls\":1,\"same_object\":true,\"sealed_revalidated\":true,\"source_validated\":true},\"consumer\":{\"byte_length\":3,\"object_type\":\"sealed-memfd\",\"reference_bound\":true,\"role\":\"consumer\",\"seals\":[\"F_SEAL_GROW\",\"F_SEAL_SEAL\",\"F_SEAL_SHRINK\",\"F_SEAL_WRITE\"],\"sha256\":\"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad\",\"source_sha256\":\"d15ddd0b3d689592398987e62ce3135ee8a61e48ccd48cfa511d4870ac0b0023\"},\"harness_sha256\":\"67150d764cfde33e1d72837cf3ec518c3469a7f617ec19808d30c0762434b647\",\"implementation_sha256\":\"d15ddd0b3d689592398987e62ce3135ee8a61e48ccd48cfa511d4870ac0b0023\",\"manifest_sha256\":\"4a9ebe2c4e275600d9a6c7864bb14c3d5a4c0b6a7c8bbf88193fc48f76affce0\",\"observer\":{\"byte_length\":3,\"object_type\":\"sealed-memfd\",\"reference_bound\":true,\"role\":\"observer\",\"seals\":[\"F_SEAL_GROW\",\"F_SEAL_SEAL\",\"F_SEAL_SHRINK\",\"F_SEAL_WRITE\"],\"sha256\":\"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad\",\"source_sha256\":\"d15ddd0b3d689592398987e62ce3135ee8a61e48ccd48cfa511d4870ac0b0023\"},\"profile\":\"ns001.h2a2.sealed-memfd.v1\",\"snapshot_sha256\":\"0ae1c30f2568188390fe05d092609eb122f3bee16c48f41fae9fe3f08e6ba432\",\"source_sha256\":\"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad\",\"verdict\":\"ACCEPT\"}","cases":[{"case":"P1","code":null,"consumer_calls":1,"kind":"fixture","observations":[{"association_checks":7,"creation":true,"direct_duplicates":2,"independent_role_reads":2,"no_reopen":true}],"observer_calls":1,"record_sha256":"6b5bc733835004aeb9ea6ce3994f028f9c815f2556a11fb34a9fa4724ca5adce","verdict":"ACCEPT"},{"case":"P1-repeat","code":null,"consumer_calls":1,"kind":"fixture","observations":[{"association_checks":7,"creation":true,"direct_duplicates":2,"independent_role_reads":2,"no_reopen":true}],"observer_calls":1,"record_sha256":"6b5bc733835004aeb9ea6ce3994f028f9c815f2556a11fb34a9fa4724ca5adce","verdict":"ACCEPT"},{"case":"P2-replace","code":null,"consumer_calls":1,"kind":"fixture","observations":[{"association_checks":7,"creation":true,"direct_duplicates":2,"independent_role_reads":2,"no_reopen":true}],"observer_calls":1,"record_sha256":"6b5bc733835004aeb9ea6ce3994f028f9c815f2556a11fb34a9fa4724ca5adce","verdict":"ACCEPT"},{"case":"P2-delete","code":null,"consumer_calls":1,"kind":"fixture","observations":[{"association_checks":7,"creation":true,"direct_duplicates":2,"independent_role_reads":2,"no_reopen":true}],"observer_calls":1,"record_sha256":"6b5bc733835004aeb9ea6ce3994f028f9c815f2556a11fb34a9fa4724ca5adce","verdict":"ACCEPT"},{"case":"N01","code":"FILE_DIGEST","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"b5a550009d44778beba65a9eabc3d24bb2ccea001f46b13a45d9d73c1a52facb","verdict":"REFUSE"},{"case":"N02","code":"FILE_LENGTH","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"b3debbafbd47925f463427f5f4fd60281f16b4ac2c526cb94200691a0e313364","verdict":"REFUSE"},{"case":"N03","code":"FILE_LENGTH","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"b3debbafbd47925f463427f5f4fd60281f16b4ac2c526cb94200691a0e313364","verdict":"REFUSE"},{"case":"N04","code":"FILE_MISSING","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"cc73bb8fce98b05f5443801f0e0fc28303ef6b6d869a697816232a08c85ca4fa","verdict":"REFUSE"},{"case":"N05","code":"FILE_MISSING","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"cc73bb8fce98b05f5443801f0e0fc28303ef6b6d869a697816232a08c85ca4fa","verdict":"REFUSE"},{"case":"N06","code":"EXTRA_FILE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"78d63b7b75bd66e14ccdd20909e7aa2b3ca5c191f3a7a0789a1a4ca4781592fa","verdict":"REFUSE"},{"case":"N07","code":"SYMLINK","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"95cf9194c940778bc391aa301c55ae13c5a1a8e24e6dfdff35cff426ecc66eed","verdict":"REFUSE"},{"case":"N08","code":"MANIFEST_DIGEST","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"d033f8a1dfc55576954d6763d40df3b11b1ed508c759b1c615071aa77e6faf9c","verdict":"REFUSE"},{"case":"N09","code":"MANIFEST_LENGTH","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"20892c44265afb8913d6ea4d99ceee5a78101057c5d73af479cfacaf3ca84fa6","verdict":"REFUSE"},{"case":"N10","code":"DUPLICATE_KEY","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"d4f57637818893005523dcd5c44633c65d6f6c47e8309f73c91ff4bf4c612cbb","verdict":"REFUSE"},{"case":"N11","code":"MANIFEST_FIELD_MISSING","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"8a50325cc312e1398a84447e3a87aaacfeda2d344985a98f366146b91eb02625","verdict":"REFUSE"},{"case":"N12","code":"ROOT_MISMATCH","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"23cecab9a8d1ee25262f763fc08eedc0cfeef81aa18322525a90f833d334eec6","verdict":"REFUSE"},{"case":"N13","code":"HANDOFF_SUBSTITUTED","consumer_calls":0,"kind":"synthetic substitution / real distinct memfd","observations":[{"equal_byte_distinct_memfd":true,"substitution":"consumer"}],"observer_calls":0,"record_sha256":"0984e17ef80778a6e381c8f11716e10408963e70d28547887b7d4ea4771d9a54","verdict":"REFUSE"},{"case":"N14-policy-0","code":"CONSUMER_IDENTITY","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"75e2cb4a28b7564ecb12557530a93edef1129adcf441bd2fac57c8bb12629453","verdict":"REFUSE"},{"case":"N14-policy-1","code":"CONSUMER_IDENTITY","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"75e2cb4a28b7564ecb12557530a93edef1129adcf441bd2fac57c8bb12629453","verdict":"REFUSE"},{"case":"N14-policy-2","code":"CONSUMER_IDENTITY","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"75e2cb4a28b7564ecb12557530a93edef1129adcf441bd2fac57c8bb12629453","verdict":"REFUSE"},{"case":"N14-delivery","code":"CONSUMER_IDENTITY","consumer_calls":0,"kind":"synthetic identity substitution","observations":[],"observer_calls":0,"record_sha256":"75e2cb4a28b7564ecb12557530a93edef1129adcf441bd2fac57c8bb12629453","verdict":"REFUSE"},{"case":"N15","code":"MANIFEST_MISSING","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"e4ede83d67bc57906b469d8fc7d4196d4f5499518fb0c6c0351ff2dead83204a","verdict":"REFUSE"},{"case":"N16","code":"MANIFEST_MALFORMED","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"69a1a5cf3960113efc4d20e8b598c9c1c9471a735e5d6cc59123947168a05cee","verdict":"REFUSE"},{"case":"N17","code":"MANIFEST_FIELD_UNKNOWN","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"80fbb160b197077537ecf78997e5bcd27f85ad590182a933d055531349fc0bff","verdict":"REFUSE"},{"case":"N18","code":"MANIFEST_VERSION","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"13c6d6e82a6d994bf8a0d6cdef1fd491b89d979794064ffc8ada0e28eadac3ea","verdict":"REFUSE"},{"case":"N19","code":"PATH_TRAVERSAL","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"02b05d977335bde7f210e1b8dbb4893cd198dcdd99497d69ea40ebb8c5f83dc2","verdict":"REFUSE"},{"case":"N20","code":"PATH_ABSOLUTE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"6b0ccbd382c5d3fea81f696613c3da1c7953bb1c1a694b9f60d311dffb4cc5e9","verdict":"REFUSE"},{"case":"N21","code":"DUPLICATE_PATH","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"64afd2b02349378e33b4f39d007daeafffd828384e08e45a67c9879cf35d3a5c","verdict":"REFUSE"},{"case":"N22-0","code":"EXPECTED_IDENTITY","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"1ec55c9cc0fe9d6daa18be4d78199ba097035b8f57fe3260eb82e2c8e862d3fc","verdict":"REFUSE"},{"case":"N22-1","code":"EXPECTED_IDENTITY","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"1ec55c9cc0fe9d6daa18be4d78199ba097035b8f57fe3260eb82e2c8e862d3fc","verdict":"REFUSE"},{"case":"N22-2","code":"EXPECTED_IDENTITY","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"1ec55c9cc0fe9d6daa18be4d78199ba097035b8f57fe3260eb82e2c8e862d3fc","verdict":"REFUSE"},{"case":"N22-3","code":"EXPECTED_IDENTITY","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"1ec55c9cc0fe9d6daa18be4d78199ba097035b8f57fe3260eb82e2c8e862d3fc","verdict":"REFUSE"},{"case":"N23","code":"ROOT_MISSING","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"61638fc1cfc65fd9ee4b2793a98f1ece37ed985d658846b1dac830d2f0177a44","verdict":"REFUSE"},{"case":"N24-.hidden","code":"EXTRA_FILE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"78d63b7b75bd66e14ccdd20909e7aa2b3ca5c191f3a7a0789a1a4ca4781592fa","verdict":"REFUSE"},{"case":"N24-source.pyc","code":"EXTRA_FILE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"78d63b7b75bd66e14ccdd20909e7aa2b3ca5c191f3a7a0789a1a4ca4781592fa","verdict":"REFUSE"},{"case":"N25-directory","code":"ENTRY_TYPE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"8aba8dcf54ea7fe6a76ea80961f53b7a438db4788cc0a96f63923b7434d3680c","verdict":"REFUSE"},{"case":"N25-fifo","code":"ENTRY_TYPE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"8aba8dcf54ea7fe6a76ea80961f53b7a438db4788cc0a96f63923b7434d3680c","verdict":"REFUSE"},{"case":"N25-socket","code":"ENTRY_TYPE","consumer_calls":0,"kind":"synthetic metadata stub; no socket/device created","observations":[],"observer_calls":0,"record_sha256":"8aba8dcf54ea7fe6a76ea80961f53b7a438db4788cc0a96f63923b7434d3680c","verdict":"REFUSE"},{"case":"N25-device","code":"ENTRY_TYPE","consumer_calls":0,"kind":"synthetic metadata stub; no socket/device created","observations":[],"observer_calls":0,"record_sha256":"8aba8dcf54ea7fe6a76ea80961f53b7a438db4788cc0a96f63923b7434d3680c","verdict":"REFUSE"},{"case":"N26","code":"HANDOFF_UNPROTECTED","consumer_calls":0,"kind":"synthetic seal-query fault","observations":[],"observer_calls":0,"record_sha256":"fab07a5bac44ed4b87a22bb4d50b13ee9e1a6d543723493d48d8aec4e6368963","verdict":"REFUSE"},{"case":"N27","code":"HANDOFF_MUTATED","consumer_calls":0,"kind":"synthetic read fault; real mutation denial separately M04","observations":[],"observer_calls":0,"record_sha256":"8f7b6f7288a8d4128e7c360c9d544051cbc1d7599875b4c2a51e6a9c306c8f9b","verdict":"REFUSE"},{"case":"N28","code":"MANIFEST_NONCANONICAL","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"b968fdaf7251e3af8cd71319d794bd69b4859f566f547ba08931f7816cea92a9","verdict":"REFUSE"},{"case":"N29","code":"FILE_PATH","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"df652cecb2fccf4408784fd6a8c818803480e81d22c061a761830d532a9fbe2b","verdict":"REFUSE"},{"case":"N30-False","code":"CONSUMER_RESULT","consumer_calls":1,"kind":"synthetic result fault","observations":[],"observer_calls":0,"record_sha256":"b8fcf83a7e7726fd24deb564e88966b6dc0970591a425c4fdb1042d3468a63b3","verdict":"REFUSE"},{"case":"N30-True","code":"CONSUMER_RESULT","consumer_calls":1,"kind":"synthetic result fault","observations":[],"observer_calls":0,"record_sha256":"b8fcf83a7e7726fd24deb564e88966b6dc0970591a425c4fdb1042d3468a63b3","verdict":"REFUSE"},{"case":"N31","code":"EVIDENCE_INCOMPLETE","consumer_calls":1,"kind":"withheld independent association evidence; both role results intact","observations":[{"no_accept_before_finalization":true,"omitted":"independent association observations","role_results_preserved":true}],"observer_calls":1,"record_sha256":"182eb6b3f5c8349268cc51bce415fc383dac66aef8cded31870c8f54c7ee106c","verdict":"REFUSE"},{"case":"M01","code":"MEMFD_CAPABILITY","consumer_calls":0,"kind":"real kernel initial seal state","observations":[],"observer_calls":0,"record_sha256":"7af84361ac98ea2bf5556f2b33a419d4e9f2b79f5b0759681b781fb8230f3b5b","verdict":"REFUSE"},{"case":"M02","code":"MEMFD_SEAL_APPLY","consumer_calls":0,"kind":"synthetic syscall error","observations":[],"observer_calls":0,"record_sha256":"bd8afbe4f7a7a18dac7bc49d1033aaded7d97ea910ae45b9337a7b4a82b9936f","verdict":"REFUSE"},{"case":"M03-F_SEAL_GROW","code":"MEMFD_SEAL_SET","consumer_calls":0,"kind":"real reduced seal set / synthetic setup","observations":[],"observer_calls":0,"record_sha256":"a70c5d0da2b8a4c6a7dda1ff1e3c394c71a213013f0b3f8301c130e5732b1e91","verdict":"REFUSE"},{"case":"M03-F_SEAL_SEAL","code":"MEMFD_SEAL_SET","consumer_calls":0,"kind":"real reduced seal set / synthetic setup","observations":[],"observer_calls":0,"record_sha256":"a70c5d0da2b8a4c6a7dda1ff1e3c394c71a213013f0b3f8301c130e5732b1e91","verdict":"REFUSE"},{"case":"M03-F_SEAL_SHRINK","code":"MEMFD_SEAL_SET","consumer_calls":0,"kind":"real reduced seal set / synthetic setup","observations":[],"observer_calls":0,"record_sha256":"a70c5d0da2b8a4c6a7dda1ff1e3c394c71a213013f0b3f8301c130e5732b1e91","verdict":"REFUSE"},{"case":"M03-F_SEAL_WRITE","code":"MEMFD_SEAL_SET","consumer_calls":0,"kind":"real reduced seal set / synthetic setup","observations":[],"observer_calls":0,"record_sha256":"a70c5d0da2b8a4c6a7dda1ff1e3c394c71a213013f0b3f8301c130e5732b1e91","verdict":"REFUSE"},{"case":"M04","code":"HANDOFF_MUTATION_ATTEMPT","consumer_calls":0,"kind":"kernel enforcement + harness protocol refusal","observations":[{"errno":"EPERM","operation":"write","unchanged":true}],"observer_calls":0,"record_sha256":"ad158975a6cb58f292112680111c1c0752fd63477cbe5952109e7836e280dfc6","verdict":"REFUSE"},{"case":"M05-shrink","code":"HANDOFF_MUTATION_ATTEMPT","consumer_calls":0,"kind":"kernel enforcement + harness protocol refusal","observations":[{"errno":"EPERM","operation":"shrink","unchanged":true}],"observer_calls":0,"record_sha256":"ad158975a6cb58f292112680111c1c0752fd63477cbe5952109e7836e280dfc6","verdict":"REFUSE"},{"case":"M05-grow","code":"HANDOFF_MUTATION_ATTEMPT","consumer_calls":0,"kind":"kernel enforcement + harness protocol refusal","observations":[{"errno":"EPERM","operation":"grow","unchanged":true}],"observer_calls":0,"record_sha256":"ad158975a6cb58f292112680111c1c0752fd63477cbe5952109e7836e280dfc6","verdict":"REFUSE"},{"case":"M06","code":"HANDOFF_SUBSTITUTED","consumer_calls":0,"kind":"synthetic substitution / real distinct sealed memfd","observations":[{"equal_byte_distinct_memfd":true,"substitution":"anchor"}],"observer_calls":0,"record_sha256":"0984e17ef80778a6e381c8f11716e10408963e70d28547887b7d4ea4771d9a54","verdict":"REFUSE"},{"case":"M07","code":"HANDOFF_SUBSTITUTED","consumer_calls":1,"kind":"synthetic substitution / real distinct sealed memfd","observations":[{"equal_byte_distinct_memfd":true,"substitution":"after-consumer"}],"observer_calls":0,"record_sha256":"0984e17ef80778a6e381c8f11716e10408963e70d28547887b7d4ea4771d9a54","verdict":"REFUSE"},{"case":"M08","code":"HANDOFF_SUBSTITUTED","consumer_calls":0,"kind":"synthetic substitution / real distinct sealed memfd","observations":[{"equal_byte_distinct_memfd":true,"substitution":"consumer"}],"observer_calls":0,"record_sha256":"0984e17ef80778a6e381c8f11716e10408963e70d28547887b7d4ea4771d9a54","verdict":"REFUSE"},{"case":"M09","code":"HANDOFF_SUBSTITUTED","consumer_calls":0,"kind":"synthetic substitution / real distinct sealed memfd","observations":[{"equal_byte_distinct_memfd":true,"substitution":"observer"}],"observer_calls":0,"record_sha256":"0984e17ef80778a6e381c8f11716e10408963e70d28547887b7d4ea4771d9a54","verdict":"REFUSE"},{"case":"M10","code":"MEMFD_COPY_DIGEST","consumer_calls":0,"kind":"synthetic copy fault","observations":[],"observer_calls":0,"record_sha256":"f117687571e5b0b32bffa357a04edf077fd9d071c4ded7644679cd590db243cf","verdict":"REFUSE"},{"case":"M11-2","code":"MEMFD_COPY_SIZE","consumer_calls":0,"kind":"synthetic post-copy size corruption before sealing","observations":[],"observer_calls":0,"record_sha256":"640e70a34b2db5003d19edcf694cfbc3b70351ddd6c221adcbdd88f27aa0a700","verdict":"REFUSE"},{"case":"M11-4","code":"MEMFD_COPY_SIZE","consumer_calls":0,"kind":"synthetic post-copy size corruption before sealing","observations":[],"observer_calls":0,"record_sha256":"640e70a34b2db5003d19edcf694cfbc3b70351ddd6c221adcbdd88f27aa0a700","verdict":"REFUSE"},{"case":"M12","code":"HANDOFF_REOPEN","consumer_calls":0,"kind":"harness reopen guard; no reopen performed","observations":[],"observer_calls":0,"record_sha256":"52fd0c95ba80e9ff59f46ead5ab49cdff67fa5407f01b7fc931b8ad15e2aeb5a","verdict":"REFUSE"},{"case":"M13","code":"MEMFD_SEAL_APPLY","consumer_calls":0,"kind":"kernel enforcement: genuine writable mapping","observations":[{"errno":"EBUSY","operation":"F_ADD_SEALS"}],"observer_calls":0,"record_sha256":"bd8afbe4f7a7a18dac7bc49d1033aaded7d97ea910ae45b9337a7b4a82b9936f","verdict":"REFUSE"},{"case":"M14-short","code":"MEMFD_COPY_IO","consumer_calls":0,"kind":"synthetic short write","observations":[],"observer_calls":0,"record_sha256":"3e5b00ba4f391ce7368101b7a24f74e8b8358e2c47d55ac05932d4d5cbabde0a","verdict":"REFUSE"},{"case":"M14-error","code":"MEMFD_COPY_IO","consumer_calls":0,"kind":"synthetic syscall error","observations":[],"observer_calls":0,"record_sha256":"3e5b00ba4f391ce7368101b7a24f74e8b8358e2c47d55ac05932d4d5cbabde0a","verdict":"REFUSE"},{"case":"M15-identity","code":"OBSERVER_IDENTITY","consumer_calls":0,"kind":"synthetic identity expectation","observations":[],"observer_calls":0,"record_sha256":"57b44c6025479d916ff44ae5546df807ea0ed5d5aa22a1461e31254dbadac4ca","verdict":"REFUSE"},{"case":"M15-result","code":"OBSERVER_RESULT","consumer_calls":1,"kind":"synthetic result fault","observations":[],"observer_calls":1,"record_sha256":"341465a2b7558b7131eb8179da3cc8ffff8ed80b144f03a1ba6822cd099275e8","verdict":"REFUSE"},{"case":"A-root-symlink","code":"SYMLINK","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"95cf9194c940778bc391aa301c55ae13c5a1a8e24e6dfdff35cff426ecc66eed","verdict":"REFUSE"},{"case":"A-root-type","code":"ROOT_TYPE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"7459f9131a4c7b1e1618027ec2060ab3646a99c84016ee7b298145f6fbcec234","verdict":"REFUSE"},{"case":"A-hardlink","code":"FILE_ALIAS","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"414d17fe8d5e143f0e3ec56f981563ad77804853e3f5e4acb423ec49d238c1c4","verdict":"REFUSE"},{"case":"A-unreadable","code":"IO_ERROR","consumer_calls":0,"kind":"synthetic permission error unit case","observations":[],"observer_calls":0,"record_sha256":"cba6f1e0ee38904c45bc1aab97f329afd13a93b4265dcf35f1f3e970c3cacadb","verdict":"REFUSE"},{"case":"A-oversize","code":"MANIFEST_SIZE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"3f559c55dd5c6e38880da3b8be14db0f258d026ee4967965b6b1c60cc8330892","verdict":"REFUSE"},{"case":"A-type-bool","code":"SCHEMA_TYPE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"79be71d467886de3bbe5e6db4163ebfb517c3d3941edafe8ded62f1fb815e31f","verdict":"REFUSE"},{"case":"A-type-float","code":"SCHEMA_TYPE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"79be71d467886de3bbe5e6db4163ebfb517c3d3941edafe8ded62f1fb815e31f","verdict":"REFUSE"},{"case":"A-type-path-list","code":"SCHEMA_TYPE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"79be71d467886de3bbe5e6db4163ebfb517c3d3941edafe8ded62f1fb815e31f","verdict":"REFUSE"},{"case":"A-type-array","code":"SCHEMA_TYPE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"79be71d467886de3bbe5e6db4163ebfb517c3d3941edafe8ded62f1fb815e31f","verdict":"REFUSE"},{"case":"A-duplicate-precedence","code":"DUPLICATE_PATH","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"64afd2b02349378e33b4f39d007daeafffd828384e08e45a67c9879cf35d3a5c","verdict":"REFUSE"},{"case":"A-exclusive-boundary","code":"ROOT_UNSTABLE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"b75918fcc645ec8c300a0b1d688082c6bff5efeb3d0ef7791b40813a0575bc02","verdict":"REFUSE"},{"case":"A-acquisition-change","code":"ROOT_UNSTABLE","consumer_calls":0,"kind":"scheduled real fixture change","observations":[],"observer_calls":0,"record_sha256":"b75918fcc645ec8c300a0b1d688082c6bff5efeb3d0ef7791b40813a0575bc02","verdict":"REFUSE"},{"case":"B1-large-tail","code":"FILE_LENGTH","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"b3debbafbd47925f463427f5f4fd60281f16b4ac2c526cb94200691a0e313364","verdict":"REFUSE"},{"case":"B1-source-prefix","code":"FILE_LENGTH","consumer_calls":0,"kind":"oversized file with short-read adapter; rejected by size before read","observations":[],"observer_calls":0,"record_sha256":"b3debbafbd47925f463427f5f4fd60281f16b4ac2c526cb94200691a0e313364","verdict":"REFUSE"},{"case":"B1-manifest-oversize-prefix","code":"MANIFEST_SIZE","consumer_calls":0,"kind":"oversized manifest with short-read adapter; rejected by size before read","observations":[],"observer_calls":0,"record_sha256":"3f559c55dd5c6e38880da3b8be14db0f258d026ee4967965b6b1c60cc8330892","verdict":"REFUSE"},{"case":"B1-manifest-trailing-prefix","code":"IO_ERROR","consumer_calls":0,"kind":"actual short read of incomplete manifest prefix","observations":[],"observer_calls":0,"record_sha256":"cba6f1e0ee38904c45bc1aab97f329afd13a93b4265dcf35f1f3e970c3cacadb","verdict":"REFUSE"},{"case":"B1-incomplete-source","code":"IO_ERROR","consumer_calls":0,"kind":"actual short acquisition read of exact-size file","observations":[],"observer_calls":0,"record_sha256":"cba6f1e0ee38904c45bc1aab97f329afd13a93b4265dcf35f1f3e970c3cacadb","verdict":"REFUSE"},{"case":"B1-eof-extra-byte","code":"FILE_LENGTH","consumer_calls":0,"kind":"scheduled real append immediately before EOF probe","observations":[],"observer_calls":0,"record_sha256":"b3debbafbd47925f463427f5f4fd60281f16b4ac2c526cb94200691a0e313364","verdict":"REFUSE"},{"case":"B2-short-read-before-seal","code":"MEMFD_COPY_IO","consumer_calls":0,"kind":"short-read adapter on actual correctly-sized memfd; no mutation","observations":[],"observer_calls":0,"record_sha256":"3e5b00ba4f391ce7368101b7a24f74e8b8358e2c47d55ac05932d4d5cbabde0a","verdict":"REFUSE"},{"case":"B2-short-read-after-seal","code":"MEMFD_COPY_IO","consumer_calls":0,"kind":"short-read adapter on actual correctly-sized memfd; no mutation","observations":[],"observer_calls":0,"record_sha256":"3e5b00ba4f391ce7368101b7a24f74e8b8358e2c47d55ac05932d4d5cbabde0a","verdict":"REFUSE"}],"deterministic":true,"harness_sha256":"67150d764cfde33e1d72837cf3ec518c3469a7f617ec19808d30c0762434b647","implementation_sha256":"d15ddd0b3d689592398987e62ce3135ee8a61e48ccd48cfa511d4870ac0b0023","negative":84,"offline_guard":true,"positive":4,"total":88}
```

## Claim ceiling, preservation and gate status

The only supported claim, with the declared residual assumptions, remains:

> The exact expected single-file bytes were validated, copied into a sealed immutable
> handoff object, and the same protected object was independently observed by the fixed
> non-executing consumer and observer.

No source execution, interpreter/runtime/process/dependency identity, client/transport
integrity, response/scientific correctness, E0 execution or full H2 gate resolution is
established. Residual assumptions remain the trusted Linux kernel and descriptor semantics,
Python/loading, hashing, reviewed harness and exclusive synthetic acquisition/descriptor
control. The observer is logically separate in the same trusted process. No runtime or
dependency lock is established, and evidence objects do not authenticate themselves.

Before commit, all **198 pre-existing tracked files outside the two authorized source/test
paths** were compared byte-for-byte to starting HEAD and are unchanged. This includes all
prior receipts, H2A1 artifacts, preregistration, scientific code/artifacts, E0 entrypoints,
clients and workflows. Only the two approved code/test files and this new receipt changed.
No credential/config, dataset/result or publication mutation occurred. Implementation and
tests were offline; the expressly requested Git push is a later preservation operation.

| H2 gate | Status |
| --- | --- |
| external_trust_root | UNRESOLVED; corrected offline synthetic handoff evidence slice passes with residual assumptions only |
| client_source | UNRESOLVED; untouched |
| response_contract | UNRESOLVED; untouched |
| transport_accounting | UNRESOLVED; untouched |
| dependency_runtime_lock | UNRESOLVED; no lock established |
| maximum_partition_memory | UNRESOLVED; untouched |
| amendment_freeze | UNRESOLVED; untouched |
| final_manifest_package_audit | UNRESOLVED; untouched |

- oversized-input defect: FIXED.
- exact-length/EOF verification method: opened-file size + complete bounded read + explicit one-byte EOF probe + metadata stability, without retry/repair.
- memfd short-read refusal-code defect: FIXED.
- expected refusal code: MEMFD_COPY_IO for incomplete read; MEMFD_COPY_SIZE for genuinely wrong complete-object size.
- N31 defect: FIXED; independently observed association evidence withheld with both role results intact.
- total positive tests: 4.
- total negative/refusal tests: 84.
- kernel-enforcement verdict: PASS, genuine EPERM/EBUSY distinguished from synthetic faults.
- same-object verdict: PASS within declared trusted harness.
- determinism verdict: PASS across equal corrected-source runs.
- claim-boundary verdict: preserved; non-executing synthetic handoff only.
- files changed: exactly the three paths listed above.
- residual assumptions: trusted kernel/descriptors, Python/loading/hashing and reviewed exclusive harness; no runtime/dependency lock or adversarial-host authentication.
- external_trust_root slice status: corrected bounded evidence accepted with residual assumptions; full gate unresolved.
- all eight H2 gate statuses: UNRESOLVED.
- H2A1 status: VERIFIED for scoped prospective custody/publication auditability; unchanged.
- H2A2 status: first offline synthetic slice corrected and acceptance-passed; no live integration or whole-gate closure.
- E0 status: HOLD.
- one next bounded action only: independent read-only review of the three corrections and their preserved acceptance evidence; no next implementation or E0 execution.
