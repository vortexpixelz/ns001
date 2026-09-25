# NS-001 H2A2 runtime trust-root implementation receipt v0.1

## Bounded outcome and preserved basis

Starting branch `codex/e0-h2-preparation`, HEAD
`49382cf1be66b0f083a4456ae4383379cd300cd3`, clean working tree.
Read the frozen acceptance specification, acceptance review and mechanism-selection
receipt in this directory at that commit. The mechanism receipt unambiguously froze
exactly the three paths below. No fallback receipt path was needed.

**PASS: 80 bounded cases, 4 ACCEPT and 76 REFUSE.** All N01–N31 and M01–M15
families and the appended required cases were exercised, with subcases recorded below.
There were no skipped cases, no failing acceptance runs and no repair/retry of a failed
handoff. P1, repeated P1 and both P2 isolation variants produce identical canonical
ACCEPT bytes. These are four observations of one positive acceptance predicate.

The synthetic sealed-object handoff claim is VERIFIED WITH RESIDUAL ASSUMPTION within
the reviewed trusted harness. This is local offline acceptance evidence, not an independent
organization's audit or authenticated runtime proof. The observer is a separate fixed
function and independently measures its own handle; it is not a separate security principal.

## Exact changed paths and source pins

| Path | Purpose / SHA-256 |
| --- | --- |
| `e0/h2/runtime_trust_root.py` | Only handoff implementation, fixed consumer/observer and deterministic evidence; `ad46e8370d04b0fb38fda2aca0fd2417380f4b59e3e7d76b51025e6a0c93f6eb` |
| `tests/test_e0_h2_runtime_trust_root.py` | Only offline synthetic fixture/harness and required tests; `0c85b93d2565eb075c0c840c3fe34815113d85b9dadfdc1b15e076e6eca2db6e` |
| `docs/e0/h2/NS-001_H2A2_RUNTIME_TRUST_ROOT_IMPLEMENTATION_RECEIPT_v0.1.md` | This receipt and retained output; no recursive self-hash |

Implementation and harness were reviewed as source before the acceptance run. Their whole
file hashes K/T were computed outside the candidate and passed as literal command-line
pins. The harness checks both before importing the one new module; it does not accept a
candidate-generated expected pin. The two role bodies also undergo a restricted AST-call
allowlist check. No existing E0 entrypoint or package initializer is imported. This records
review within this circuit, not a claim of independently authenticated loaded-code identity.

## Frozen identities and concrete behavior

- Synthetic file: only `source.bin`, bytes `61 62 63` / ASCII abc, no LF; length 3.
- Payload F: `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`.
- Canonical manifest M: `4a9ebe2c4e275600d9a6c7864bb14c3d5a4c0b6a7c8bbf88193fc48f76affce0`.
- Logical snapshot S: `0ae1c30f2568188390fe05d092609eb122f3bee16c48f41fae9fe3f08e6ba432`.
- Logical root: `ns001-h2a2-fixture-v1`; two acquisition files only, source.bin and manifest.json.
- memfd creation flags: exactly `MFD_ALLOW_SEALING | MFD_CLOEXEC`.
- Required and observed final seals: exactly `F_SEAL_WRITE | F_SEAL_GROW | F_SEAL_SHRINK | F_SEAL_SEAL`.
- Consumer: `ns001.h2a2.identity-consumer.v1` / `consume`, source identity K above.
- Observer: `ns001.h2a2.identity-observer.v1` / `observe`, same whole-module K; separately fixed function.

Descriptor-relative acquisition walks canonical R without symlinks and retains a bound
root handle. Single-link regular-file checks and exact member cardinality precede bounded
reads. Manifest duplicate handling, canonical serialization, path/length/digest and
expected identity are checked before the copy. Before/after acquisition metadata is used
only under the declared exclusive controlled-harness assumption, not as hostile-race proof.

The implementation creates one anonymous memfd, performs one positioned write, checks
copied size/hash, applies Q once, queries Q, and rechecks the sealed bytes. No writable
mapping exists in the positive path. Two F_DUPFD_CLOEXEC handles reference that same live
object; creator and duplicates remain open through the observations. No ordinary-file
fallback, alternate seal set, pathname reopen or source evaluation exists in the roles.
Both independently fstat, query seals, pread from offset zero and compute SHA-256.

The harness observes actual creation, direct duplication edges and the roles' separate
stat/seal/read calls. Each positive run records seven association checkpoints, one consumer
and one observer read, matching live device/inode metadata and zero consumption reopens.
The original handle stays live until completion. Descriptor numbers and device/inode values
are not serialized as stable or cryptographic identities. They corroborate the observed
live reference relationships under the trusted kernel/harness model.

## Actual acceptance command and environment

The acceptance suite was run once, including its required positive repetition and isolation
variants, using a cleared environment and isolated standard-library Python. No package
installation, network request, external test discovery, client call, scientific source
execution or E0 execution occurred. Python audit hooks reject socket/network and
subprocess/fork/exec operations during the harness. Static role review and controlled
source inspection supply the non-execution boundary; this is not an OS sandbox claim.
The separately authorized Git push occurs only after acceptance/preservation checks.

Diagnostic interpreter: Python 3.12.3, `/usr/bin/python3` bytes SHA-256
`e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f`.
This diagnostic observation does not establish interpreter/kernel identity or lock dependencies.

From the repository root, reproduce offline with these externally pinned values:

```sh
env -i PATH=/usr/bin:/bin LC_ALL=C.UTF-8 /usr/bin/python3 -I -B -S tests/test_e0_h2_runtime_trust_root.py --implementation-sha256 ad46e8370d04b0fb38fda2aca0fd2417380f4b59e3e7d76b51025e6a0c93f6eb --harness-sha256 0c85b93d2565eb075c0c840c3fe34815113d85b9dadfdc1b15e076e6eca2db6e
```

Exit status: 0. Bytecode writes were disabled. Fixtures were allocated only in fresh
`/tmp/ns001-h2a2-*` temporary directories and cleaned up. All memfd/duplicate/root handles
were closed by their owners. No persisted fixture, new evidence directory or runtime
integration was added.

## Kernel enforcement versus synthetic faults

| Tests | Observed result | Claim boundary |
| --- | --- | --- |
| M04 | Real post-seal pwrite denied with EPERM; content, size and Q unchanged | Genuine kernel write denial; harness terminates the deliberately invalid protocol with HANDOFF_MUTATION_ATTEMPT |
| M05-shrink / M05-grow | Real ftruncate to 2 / 4 denied with EPERM; content, size and Q unchanged | Genuine kernel length-change denial; same outer protocol refusal |
| M13 | Real shared writable mapping prevents F_ADD_SEALS with EBUSY | Genuine kernel prerequisite enforcement; unmap only during cleanup, no retry |
| M01 | Real creation without sealing capability refused on initial seal state | No fallback or attempted seal repair |
| M03 subcases | Real reduced seal sets detected before delivery | Synthetic setup, actual queried state; no incomplete object consumed |
| N13, M06–M09 | Equal-byte, separately created sealed objects substituted at fixed boundaries and refused | Synthetic substitution tests using genuine distinct memfds; not kernel attack detection against hostile process state |
| N27 | Faulted retained read returns wrong bytes; HANDOFF_MUTATED | Synthetic corrupted-state branch; real sealed-byte mutation was prevented in M04 |
| N25 socket/device | Synthetic metadata stubs refused | No socket/device created; does not claim real acquisition of those objects |
| A-unreadable, M02/M14 and result/identity omissions | Labelled injected errors/expectations | Validator refusal behavior only |
| M12 | Attempted consumption reopen intercepted before path I/O | Trusted harness guard plus source review, not a production filesystem sandbox |

M11 corrupts completed copied object size before the size recheck, retaining the actual
successful pwrite return count. This exercises MEMFD_COPY_SIZE without lying about a short
write. A genuinely short write is separately refused by M14 with MEMFD_COPY_IO. No copy is
repaired. M04/M05 outer refusal is a harness protocol guard after actual kernel denial;
it is not evidence that the immutable object changed or a general production intrusion detector.

All negative cases compare actual canonical bytes with an independent expected REFUSE
record and assert no ACCEPT. Invocation counts are checked: pre-consumer failures have
zero role reads; M07/N30 allow only the already-completed consumer; result/evidence failures
allow only the calls already reached. Neither role is retried.

## Deterministic evidence and retained outputs

Mechanism profile: `ns001.h2a2.sealed-memfd.v1`. It is the explicitly selected refinement
of the earlier abstract receipt/consumer profile, not a modification of prior evidence.
The canonical ACCEPT record below has SHA-256
`1647d76d543133b722667352b5964d70f335c6cb7eb22930d966bf957243eae5`. P1, P1-repeat, P2-replace and P2-delete match it byte-for-byte.
No timestamps, absolute roots, PIDs, numeric descriptors, inode values or exception messages
appear in canonical records. False handoff_succeeded means no accepted transaction, not
necessarily zero earlier role calls. Record digests are external to their records.

The following fence contains exactly the ACCEPT bytes, excluding fence/newline framing:

```json
{"byte_length":3,"checks":{"consumer_calls":1,"copy_validated":true,"creation_witnessed":true,"duplication_witnessed":true,"no_reopen":true,"observer_calls":1,"same_object":true,"sealed_revalidated":true,"source_validated":true},"consumer":{"byte_length":3,"object_type":"sealed-memfd","reference_bound":true,"role":"consumer","seals":["F_SEAL_GROW","F_SEAL_SEAL","F_SEAL_SHRINK","F_SEAL_WRITE"],"sha256":"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","source_sha256":"ad46e8370d04b0fb38fda2aca0fd2417380f4b59e3e7d76b51025e6a0c93f6eb"},"harness_sha256":"0c85b93d2565eb075c0c840c3fe34815113d85b9dadfdc1b15e076e6eca2db6e","implementation_sha256":"ad46e8370d04b0fb38fda2aca0fd2417380f4b59e3e7d76b51025e6a0c93f6eb","manifest_sha256":"4a9ebe2c4e275600d9a6c7864bb14c3d5a4c0b6a7c8bbf88193fc48f76affce0","observer":{"byte_length":3,"object_type":"sealed-memfd","reference_bound":true,"role":"observer","seals":["F_SEAL_GROW","F_SEAL_SEAL","F_SEAL_SHRINK","F_SEAL_WRITE"],"sha256":"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","source_sha256":"ad46e8370d04b0fb38fda2aca0fd2417380f4b59e3e7d76b51025e6a0c93f6eb"},"profile":"ns001.h2a2.sealed-memfd.v1","snapshot_sha256":"0ae1c30f2568188390fe05d092609eb122f3bee16c48f41fae9fe3f08e6ba432","source_sha256":"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","verdict":"ACCEPT"}
```

The exact aggregate stdout from the successful run is preserved below (one JSON line plus
one final LF, excluding fence framing). SHA-256 including that final LF:
`9a3e067bd06393d110899e4114560b8c0d6bda8ac5a023246cd54fa748bd1313`. Its case inventory retains actual outcomes, actual
record hashes, call counts, fault classes and kernel/association observations. Expected
codes are independently frozen in the committed harness and compared before inclusion.
Every REFUSE record is exactly C({"profile":"ns001.h2a2.sealed-memfd.v1", "verdict":"REFUSE",
"code":the recorded code, "handoff_succeeded":false}), so its original canonical bytes
are reconstructible and checkable against the per-case hash. No temporary output path
or cache is needed to recover this evidence.

```json
{"accept_sha256":"1647d76d543133b722667352b5964d70f335c6cb7eb22930d966bf957243eae5","all_passed":true,"canonical_accept":"{\"byte_length\":3,\"checks\":{\"consumer_calls\":1,\"copy_validated\":true,\"creation_witnessed\":true,\"duplication_witnessed\":true,\"no_reopen\":true,\"observer_calls\":1,\"same_object\":true,\"sealed_revalidated\":true,\"source_validated\":true},\"consumer\":{\"byte_length\":3,\"object_type\":\"sealed-memfd\",\"reference_bound\":true,\"role\":\"consumer\",\"seals\":[\"F_SEAL_GROW\",\"F_SEAL_SEAL\",\"F_SEAL_SHRINK\",\"F_SEAL_WRITE\"],\"sha256\":\"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad\",\"source_sha256\":\"ad46e8370d04b0fb38fda2aca0fd2417380f4b59e3e7d76b51025e6a0c93f6eb\"},\"harness_sha256\":\"0c85b93d2565eb075c0c840c3fe34815113d85b9dadfdc1b15e076e6eca2db6e\",\"implementation_sha256\":\"ad46e8370d04b0fb38fda2aca0fd2417380f4b59e3e7d76b51025e6a0c93f6eb\",\"manifest_sha256\":\"4a9ebe2c4e275600d9a6c7864bb14c3d5a4c0b6a7c8bbf88193fc48f76affce0\",\"observer\":{\"byte_length\":3,\"object_type\":\"sealed-memfd\",\"reference_bound\":true,\"role\":\"observer\",\"seals\":[\"F_SEAL_GROW\",\"F_SEAL_SEAL\",\"F_SEAL_SHRINK\",\"F_SEAL_WRITE\"],\"sha256\":\"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad\",\"source_sha256\":\"ad46e8370d04b0fb38fda2aca0fd2417380f4b59e3e7d76b51025e6a0c93f6eb\"},\"profile\":\"ns001.h2a2.sealed-memfd.v1\",\"snapshot_sha256\":\"0ae1c30f2568188390fe05d092609eb122f3bee16c48f41fae9fe3f08e6ba432\",\"source_sha256\":\"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad\",\"verdict\":\"ACCEPT\"}","cases":[{"case":"P1","code":null,"consumer_calls":1,"kind":"fixture","observations":[{"association_checks":7,"creation":true,"direct_duplicates":2,"independent_role_reads":2,"no_reopen":true}],"observer_calls":1,"record_sha256":"1647d76d543133b722667352b5964d70f335c6cb7eb22930d966bf957243eae5","verdict":"ACCEPT"},{"case":"P1-repeat","code":null,"consumer_calls":1,"kind":"fixture","observations":[{"association_checks":7,"creation":true,"direct_duplicates":2,"independent_role_reads":2,"no_reopen":true}],"observer_calls":1,"record_sha256":"1647d76d543133b722667352b5964d70f335c6cb7eb22930d966bf957243eae5","verdict":"ACCEPT"},{"case":"P2-replace","code":null,"consumer_calls":1,"kind":"fixture","observations":[{"association_checks":7,"creation":true,"direct_duplicates":2,"independent_role_reads":2,"no_reopen":true}],"observer_calls":1,"record_sha256":"1647d76d543133b722667352b5964d70f335c6cb7eb22930d966bf957243eae5","verdict":"ACCEPT"},{"case":"P2-delete","code":null,"consumer_calls":1,"kind":"fixture","observations":[{"association_checks":7,"creation":true,"direct_duplicates":2,"independent_role_reads":2,"no_reopen":true}],"observer_calls":1,"record_sha256":"1647d76d543133b722667352b5964d70f335c6cb7eb22930d966bf957243eae5","verdict":"ACCEPT"},{"case":"N01","code":"FILE_DIGEST","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"b5a550009d44778beba65a9eabc3d24bb2ccea001f46b13a45d9d73c1a52facb","verdict":"REFUSE"},{"case":"N02","code":"FILE_LENGTH","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"b3debbafbd47925f463427f5f4fd60281f16b4ac2c526cb94200691a0e313364","verdict":"REFUSE"},{"case":"N03","code":"FILE_LENGTH","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"b3debbafbd47925f463427f5f4fd60281f16b4ac2c526cb94200691a0e313364","verdict":"REFUSE"},{"case":"N04","code":"FILE_MISSING","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"cc73bb8fce98b05f5443801f0e0fc28303ef6b6d869a697816232a08c85ca4fa","verdict":"REFUSE"},{"case":"N05","code":"FILE_MISSING","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"cc73bb8fce98b05f5443801f0e0fc28303ef6b6d869a697816232a08c85ca4fa","verdict":"REFUSE"},{"case":"N06","code":"EXTRA_FILE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"78d63b7b75bd66e14ccdd20909e7aa2b3ca5c191f3a7a0789a1a4ca4781592fa","verdict":"REFUSE"},{"case":"N07","code":"SYMLINK","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"95cf9194c940778bc391aa301c55ae13c5a1a8e24e6dfdff35cff426ecc66eed","verdict":"REFUSE"},{"case":"N08","code":"MANIFEST_DIGEST","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"d033f8a1dfc55576954d6763d40df3b11b1ed508c759b1c615071aa77e6faf9c","verdict":"REFUSE"},{"case":"N09","code":"MANIFEST_LENGTH","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"20892c44265afb8913d6ea4d99ceee5a78101057c5d73af479cfacaf3ca84fa6","verdict":"REFUSE"},{"case":"N10","code":"DUPLICATE_KEY","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"d4f57637818893005523dcd5c44633c65d6f6c47e8309f73c91ff4bf4c612cbb","verdict":"REFUSE"},{"case":"N11","code":"MANIFEST_FIELD_MISSING","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"8a50325cc312e1398a84447e3a87aaacfeda2d344985a98f366146b91eb02625","verdict":"REFUSE"},{"case":"N12","code":"ROOT_MISMATCH","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"23cecab9a8d1ee25262f763fc08eedc0cfeef81aa18322525a90f833d334eec6","verdict":"REFUSE"},{"case":"N13","code":"HANDOFF_SUBSTITUTED","consumer_calls":0,"kind":"synthetic substitution / real distinct memfd","observations":[{"equal_byte_distinct_memfd":true,"substitution":"consumer"}],"observer_calls":0,"record_sha256":"0984e17ef80778a6e381c8f11716e10408963e70d28547887b7d4ea4771d9a54","verdict":"REFUSE"},{"case":"N14-policy-0","code":"CONSUMER_IDENTITY","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"75e2cb4a28b7564ecb12557530a93edef1129adcf441bd2fac57c8bb12629453","verdict":"REFUSE"},{"case":"N14-policy-1","code":"CONSUMER_IDENTITY","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"75e2cb4a28b7564ecb12557530a93edef1129adcf441bd2fac57c8bb12629453","verdict":"REFUSE"},{"case":"N14-policy-2","code":"CONSUMER_IDENTITY","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"75e2cb4a28b7564ecb12557530a93edef1129adcf441bd2fac57c8bb12629453","verdict":"REFUSE"},{"case":"N14-delivery","code":"CONSUMER_IDENTITY","consumer_calls":0,"kind":"synthetic identity substitution","observations":[],"observer_calls":0,"record_sha256":"75e2cb4a28b7564ecb12557530a93edef1129adcf441bd2fac57c8bb12629453","verdict":"REFUSE"},{"case":"N15","code":"MANIFEST_MISSING","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"e4ede83d67bc57906b469d8fc7d4196d4f5499518fb0c6c0351ff2dead83204a","verdict":"REFUSE"},{"case":"N16","code":"MANIFEST_MALFORMED","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"69a1a5cf3960113efc4d20e8b598c9c1c9471a735e5d6cc59123947168a05cee","verdict":"REFUSE"},{"case":"N17","code":"MANIFEST_FIELD_UNKNOWN","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"80fbb160b197077537ecf78997e5bcd27f85ad590182a933d055531349fc0bff","verdict":"REFUSE"},{"case":"N18","code":"MANIFEST_VERSION","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"13c6d6e82a6d994bf8a0d6cdef1fd491b89d979794064ffc8ada0e28eadac3ea","verdict":"REFUSE"},{"case":"N19","code":"PATH_TRAVERSAL","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"02b05d977335bde7f210e1b8dbb4893cd198dcdd99497d69ea40ebb8c5f83dc2","verdict":"REFUSE"},{"case":"N20","code":"PATH_ABSOLUTE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"6b0ccbd382c5d3fea81f696613c3da1c7953bb1c1a694b9f60d311dffb4cc5e9","verdict":"REFUSE"},{"case":"N21","code":"DUPLICATE_PATH","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"64afd2b02349378e33b4f39d007daeafffd828384e08e45a67c9879cf35d3a5c","verdict":"REFUSE"},{"case":"N22-0","code":"EXPECTED_IDENTITY","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"1ec55c9cc0fe9d6daa18be4d78199ba097035b8f57fe3260eb82e2c8e862d3fc","verdict":"REFUSE"},{"case":"N22-1","code":"EXPECTED_IDENTITY","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"1ec55c9cc0fe9d6daa18be4d78199ba097035b8f57fe3260eb82e2c8e862d3fc","verdict":"REFUSE"},{"case":"N22-2","code":"EXPECTED_IDENTITY","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"1ec55c9cc0fe9d6daa18be4d78199ba097035b8f57fe3260eb82e2c8e862d3fc","verdict":"REFUSE"},{"case":"N22-3","code":"EXPECTED_IDENTITY","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"1ec55c9cc0fe9d6daa18be4d78199ba097035b8f57fe3260eb82e2c8e862d3fc","verdict":"REFUSE"},{"case":"N23","code":"ROOT_MISSING","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"61638fc1cfc65fd9ee4b2793a98f1ece37ed985d658846b1dac830d2f0177a44","verdict":"REFUSE"},{"case":"N24-.hidden","code":"EXTRA_FILE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"78d63b7b75bd66e14ccdd20909e7aa2b3ca5c191f3a7a0789a1a4ca4781592fa","verdict":"REFUSE"},{"case":"N24-source.pyc","code":"EXTRA_FILE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"78d63b7b75bd66e14ccdd20909e7aa2b3ca5c191f3a7a0789a1a4ca4781592fa","verdict":"REFUSE"},{"case":"N25-directory","code":"ENTRY_TYPE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"8aba8dcf54ea7fe6a76ea80961f53b7a438db4788cc0a96f63923b7434d3680c","verdict":"REFUSE"},{"case":"N25-fifo","code":"ENTRY_TYPE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"8aba8dcf54ea7fe6a76ea80961f53b7a438db4788cc0a96f63923b7434d3680c","verdict":"REFUSE"},{"case":"N25-socket","code":"ENTRY_TYPE","consumer_calls":0,"kind":"synthetic metadata stub; no socket/device created","observations":[],"observer_calls":0,"record_sha256":"8aba8dcf54ea7fe6a76ea80961f53b7a438db4788cc0a96f63923b7434d3680c","verdict":"REFUSE"},{"case":"N25-device","code":"ENTRY_TYPE","consumer_calls":0,"kind":"synthetic metadata stub; no socket/device created","observations":[],"observer_calls":0,"record_sha256":"8aba8dcf54ea7fe6a76ea80961f53b7a438db4788cc0a96f63923b7434d3680c","verdict":"REFUSE"},{"case":"N26","code":"HANDOFF_UNPROTECTED","consumer_calls":0,"kind":"synthetic seal-query fault","observations":[],"observer_calls":0,"record_sha256":"fab07a5bac44ed4b87a22bb4d50b13ee9e1a6d543723493d48d8aec4e6368963","verdict":"REFUSE"},{"case":"N27","code":"HANDOFF_MUTATED","consumer_calls":0,"kind":"synthetic read fault; real mutation denial separately M04","observations":[],"observer_calls":0,"record_sha256":"8f7b6f7288a8d4128e7c360c9d544051cbc1d7599875b4c2a51e6a9c306c8f9b","verdict":"REFUSE"},{"case":"N28","code":"MANIFEST_NONCANONICAL","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"b968fdaf7251e3af8cd71319d794bd69b4859f566f547ba08931f7816cea92a9","verdict":"REFUSE"},{"case":"N29","code":"FILE_PATH","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"df652cecb2fccf4408784fd6a8c818803480e81d22c061a761830d532a9fbe2b","verdict":"REFUSE"},{"case":"N30-False","code":"CONSUMER_RESULT","consumer_calls":1,"kind":"synthetic result fault","observations":[],"observer_calls":0,"record_sha256":"b8fcf83a7e7726fd24deb564e88966b6dc0970591a425c4fdb1042d3468a63b3","verdict":"REFUSE"},{"case":"N30-True","code":"CONSUMER_RESULT","consumer_calls":1,"kind":"synthetic result fault","observations":[],"observer_calls":0,"record_sha256":"b8fcf83a7e7726fd24deb564e88966b6dc0970591a425c4fdb1042d3468a63b3","verdict":"REFUSE"},{"case":"N31","code":"EVIDENCE_INCOMPLETE","consumer_calls":1,"kind":"synthetic observation omission","observations":[],"observer_calls":1,"record_sha256":"182eb6b3f5c8349268cc51bce415fc383dac66aef8cded31870c8f54c7ee106c","verdict":"REFUSE"},{"case":"M01","code":"MEMFD_CAPABILITY","consumer_calls":0,"kind":"real kernel initial seal state","observations":[],"observer_calls":0,"record_sha256":"7af84361ac98ea2bf5556f2b33a419d4e9f2b79f5b0759681b781fb8230f3b5b","verdict":"REFUSE"},{"case":"M02","code":"MEMFD_SEAL_APPLY","consumer_calls":0,"kind":"synthetic syscall error","observations":[],"observer_calls":0,"record_sha256":"bd8afbe4f7a7a18dac7bc49d1033aaded7d97ea910ae45b9337a7b4a82b9936f","verdict":"REFUSE"},{"case":"M03-F_SEAL_GROW","code":"MEMFD_SEAL_SET","consumer_calls":0,"kind":"real reduced seal set / synthetic setup","observations":[],"observer_calls":0,"record_sha256":"a70c5d0da2b8a4c6a7dda1ff1e3c394c71a213013f0b3f8301c130e5732b1e91","verdict":"REFUSE"},{"case":"M03-F_SEAL_SEAL","code":"MEMFD_SEAL_SET","consumer_calls":0,"kind":"real reduced seal set / synthetic setup","observations":[],"observer_calls":0,"record_sha256":"a70c5d0da2b8a4c6a7dda1ff1e3c394c71a213013f0b3f8301c130e5732b1e91","verdict":"REFUSE"},{"case":"M03-F_SEAL_SHRINK","code":"MEMFD_SEAL_SET","consumer_calls":0,"kind":"real reduced seal set / synthetic setup","observations":[],"observer_calls":0,"record_sha256":"a70c5d0da2b8a4c6a7dda1ff1e3c394c71a213013f0b3f8301c130e5732b1e91","verdict":"REFUSE"},{"case":"M03-F_SEAL_WRITE","code":"MEMFD_SEAL_SET","consumer_calls":0,"kind":"real reduced seal set / synthetic setup","observations":[],"observer_calls":0,"record_sha256":"a70c5d0da2b8a4c6a7dda1ff1e3c394c71a213013f0b3f8301c130e5732b1e91","verdict":"REFUSE"},{"case":"M04","code":"HANDOFF_MUTATION_ATTEMPT","consumer_calls":0,"kind":"kernel enforcement + harness protocol refusal","observations":[{"errno":"EPERM","operation":"write","unchanged":true}],"observer_calls":0,"record_sha256":"ad158975a6cb58f292112680111c1c0752fd63477cbe5952109e7836e280dfc6","verdict":"REFUSE"},{"case":"M05-shrink","code":"HANDOFF_MUTATION_ATTEMPT","consumer_calls":0,"kind":"kernel enforcement + harness protocol refusal","observations":[{"errno":"EPERM","operation":"shrink","unchanged":true}],"observer_calls":0,"record_sha256":"ad158975a6cb58f292112680111c1c0752fd63477cbe5952109e7836e280dfc6","verdict":"REFUSE"},{"case":"M05-grow","code":"HANDOFF_MUTATION_ATTEMPT","consumer_calls":0,"kind":"kernel enforcement + harness protocol refusal","observations":[{"errno":"EPERM","operation":"grow","unchanged":true}],"observer_calls":0,"record_sha256":"ad158975a6cb58f292112680111c1c0752fd63477cbe5952109e7836e280dfc6","verdict":"REFUSE"},{"case":"M06","code":"HANDOFF_SUBSTITUTED","consumer_calls":0,"kind":"synthetic substitution / real distinct sealed memfd","observations":[{"equal_byte_distinct_memfd":true,"substitution":"anchor"}],"observer_calls":0,"record_sha256":"0984e17ef80778a6e381c8f11716e10408963e70d28547887b7d4ea4771d9a54","verdict":"REFUSE"},{"case":"M07","code":"HANDOFF_SUBSTITUTED","consumer_calls":1,"kind":"synthetic substitution / real distinct sealed memfd","observations":[{"equal_byte_distinct_memfd":true,"substitution":"after-consumer"}],"observer_calls":0,"record_sha256":"0984e17ef80778a6e381c8f11716e10408963e70d28547887b7d4ea4771d9a54","verdict":"REFUSE"},{"case":"M08","code":"HANDOFF_SUBSTITUTED","consumer_calls":0,"kind":"synthetic substitution / real distinct sealed memfd","observations":[{"equal_byte_distinct_memfd":true,"substitution":"consumer"}],"observer_calls":0,"record_sha256":"0984e17ef80778a6e381c8f11716e10408963e70d28547887b7d4ea4771d9a54","verdict":"REFUSE"},{"case":"M09","code":"HANDOFF_SUBSTITUTED","consumer_calls":0,"kind":"synthetic substitution / real distinct sealed memfd","observations":[{"equal_byte_distinct_memfd":true,"substitution":"observer"}],"observer_calls":0,"record_sha256":"0984e17ef80778a6e381c8f11716e10408963e70d28547887b7d4ea4771d9a54","verdict":"REFUSE"},{"case":"M10","code":"MEMFD_COPY_DIGEST","consumer_calls":0,"kind":"synthetic copy fault","observations":[],"observer_calls":0,"record_sha256":"f117687571e5b0b32bffa357a04edf077fd9d071c4ded7644679cd590db243cf","verdict":"REFUSE"},{"case":"M11-2","code":"MEMFD_COPY_SIZE","consumer_calls":0,"kind":"synthetic post-copy size corruption before sealing","observations":[],"observer_calls":0,"record_sha256":"640e70a34b2db5003d19edcf694cfbc3b70351ddd6c221adcbdd88f27aa0a700","verdict":"REFUSE"},{"case":"M11-4","code":"MEMFD_COPY_SIZE","consumer_calls":0,"kind":"synthetic post-copy size corruption before sealing","observations":[],"observer_calls":0,"record_sha256":"640e70a34b2db5003d19edcf694cfbc3b70351ddd6c221adcbdd88f27aa0a700","verdict":"REFUSE"},{"case":"M12","code":"HANDOFF_REOPEN","consumer_calls":0,"kind":"harness reopen guard; no reopen performed","observations":[],"observer_calls":0,"record_sha256":"52fd0c95ba80e9ff59f46ead5ab49cdff67fa5407f01b7fc931b8ad15e2aeb5a","verdict":"REFUSE"},{"case":"M13","code":"MEMFD_SEAL_APPLY","consumer_calls":0,"kind":"kernel enforcement: genuine writable mapping","observations":[{"errno":"EBUSY","operation":"F_ADD_SEALS"}],"observer_calls":0,"record_sha256":"bd8afbe4f7a7a18dac7bc49d1033aaded7d97ea910ae45b9337a7b4a82b9936f","verdict":"REFUSE"},{"case":"M14-short","code":"MEMFD_COPY_IO","consumer_calls":0,"kind":"synthetic short write","observations":[],"observer_calls":0,"record_sha256":"3e5b00ba4f391ce7368101b7a24f74e8b8358e2c47d55ac05932d4d5cbabde0a","verdict":"REFUSE"},{"case":"M14-error","code":"MEMFD_COPY_IO","consumer_calls":0,"kind":"synthetic syscall error","observations":[],"observer_calls":0,"record_sha256":"3e5b00ba4f391ce7368101b7a24f74e8b8358e2c47d55ac05932d4d5cbabde0a","verdict":"REFUSE"},{"case":"M15-identity","code":"OBSERVER_IDENTITY","consumer_calls":0,"kind":"synthetic identity expectation","observations":[],"observer_calls":0,"record_sha256":"57b44c6025479d916ff44ae5546df807ea0ed5d5aa22a1461e31254dbadac4ca","verdict":"REFUSE"},{"case":"M15-result","code":"OBSERVER_RESULT","consumer_calls":1,"kind":"synthetic result fault","observations":[],"observer_calls":1,"record_sha256":"341465a2b7558b7131eb8179da3cc8ffff8ed80b144f03a1ba6822cd099275e8","verdict":"REFUSE"},{"case":"A-root-symlink","code":"SYMLINK","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"95cf9194c940778bc391aa301c55ae13c5a1a8e24e6dfdff35cff426ecc66eed","verdict":"REFUSE"},{"case":"A-root-type","code":"ROOT_TYPE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"7459f9131a4c7b1e1618027ec2060ab3646a99c84016ee7b298145f6fbcec234","verdict":"REFUSE"},{"case":"A-hardlink","code":"FILE_ALIAS","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"414d17fe8d5e143f0e3ec56f981563ad77804853e3f5e4acb423ec49d238c1c4","verdict":"REFUSE"},{"case":"A-unreadable","code":"IO_ERROR","consumer_calls":0,"kind":"synthetic permission error unit case","observations":[],"observer_calls":0,"record_sha256":"cba6f1e0ee38904c45bc1aab97f329afd13a93b4265dcf35f1f3e970c3cacadb","verdict":"REFUSE"},{"case":"A-oversize","code":"MANIFEST_SIZE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"3f559c55dd5c6e38880da3b8be14db0f258d026ee4967965b6b1c60cc8330892","verdict":"REFUSE"},{"case":"A-type-bool","code":"SCHEMA_TYPE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"79be71d467886de3bbe5e6db4163ebfb517c3d3941edafe8ded62f1fb815e31f","verdict":"REFUSE"},{"case":"A-type-float","code":"SCHEMA_TYPE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"79be71d467886de3bbe5e6db4163ebfb517c3d3941edafe8ded62f1fb815e31f","verdict":"REFUSE"},{"case":"A-type-path-list","code":"SCHEMA_TYPE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"79be71d467886de3bbe5e6db4163ebfb517c3d3941edafe8ded62f1fb815e31f","verdict":"REFUSE"},{"case":"A-type-array","code":"SCHEMA_TYPE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"79be71d467886de3bbe5e6db4163ebfb517c3d3941edafe8ded62f1fb815e31f","verdict":"REFUSE"},{"case":"A-duplicate-precedence","code":"DUPLICATE_PATH","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"64afd2b02349378e33b4f39d007daeafffd828384e08e45a67c9879cf35d3a5c","verdict":"REFUSE"},{"case":"A-exclusive-boundary","code":"ROOT_UNSTABLE","consumer_calls":0,"kind":"fixture","observations":[],"observer_calls":0,"record_sha256":"b75918fcc645ec8c300a0b1d688082c6bff5efeb3d0ef7791b40813a0575bc02","verdict":"REFUSE"},{"case":"A-acquisition-change","code":"ROOT_UNSTABLE","consumer_calls":0,"kind":"scheduled real fixture change","observations":[],"observer_calls":0,"record_sha256":"b75918fcc645ec8c300a0b1d688082c6bff5efeb3d0ef7791b40813a0575bc02","verdict":"REFUSE"}],"deterministic":true,"harness_sha256":"0c85b93d2565eb075c0c840c3fe34815113d85b9dadfdc1b15e076e6eca2db6e","implementation_sha256":"ad46e8370d04b0fb38fda2aca0fd2417380f4b59e3e7d76b51025e6a0c93f6eb","negative":76,"offline_guard":true,"positive":4,"total":80}
```

## Allowed claim, limits and gate disposition

The maximum supported claim, within the trusted synthetic harness, is:

> The exact expected single-file bytes were validated, copied into a sealed immutable
> handoff object, and the same protected object was independently observed by the fixed
> non-executing consumer and observer.

Prohibited inferences: execution of source bytes; authenticated interpreter/compiler,
dependency/runtime or process identity; client identity; transport integrity; response or
scientific correctness; E0 execution; full external_trust_root resolution; any other H2
gate resolution. Linux kernel/sealing behavior, reviewed harness, correct source loading,
standard hash implementation and exclusive synthetic acquisition/descriptor control remain
residual assumptions. Same-process logical observer independence is not protection from a
compromised host. Deterministic evidence is not fresh cryptographic execution attestation.

| Gate | Status after this circuit |
| --- | --- |
| external_trust_root | UNRESOLVED; this offline synthetic byte-to-sealed-handoff evidence slice accepted with residual assumptions; exact_verified_bytes_executed not established |
| client_source | UNRESOLVED; untouched |
| response_contract | UNRESOLVED; untouched |
| transport_accounting | UNRESOLVED; untouched |
| dependency_runtime_lock | UNRESOLVED; separate work; diagnostic interpreter hash is not closure |
| maximum_partition_memory | UNRESOLVED; untouched |
| amendment_freeze | UNRESOLVED; untouched |
| final_manifest_package_audit | UNRESOLVED; untouched |

## Preservation and stopping point

Before commit, all 196 pre-existing tracked files were compared byte-for-byte with starting
HEAD and were unchanged. This includes H2A1, all frozen contracts, preregistration,
scientific code/artifacts, existing E0 paths, client code and workflows. Only the three
frozen new paths are changed. Existing bytecode caches were not used to load the new
module and no bytecode was written. No credentials/configuration, datasets/results,
publication object or live infrastructure was accessed or modified by this circuit.

H2A1: VERIFIED for scoped prospective custody/publication auditability, unchanged.
H2A2: first offline synthetic handoff implementation/acceptance slice completed; no live
integration and no whole-gate closure. E0: HOLD.

One next bounded action only: independently review these three committed implementation,
harness and receipt files against the frozen contracts; no scope expansion or E0 execution.
