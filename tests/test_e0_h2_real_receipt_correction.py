"""R1-R9 independent-review counterexamples, synthetic data and local stores only.

No debugger or candidate operation. A prohibited-operation string is evidence data.
"""
import copy
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest
from e0.h2.real_receipt_policy import Invalid, canonical, parse, digest, mi_command
from e0.h2.real_receipt_evidence import Store, manifest, public_accept
from e0.h2.real_receipt_integration import (Chunk, Transcript, _all_files, verify_package,
    compare_repetition, text_maps)
from real_receipt_fixtures import preparation, observation, freeze
from test_e0_h2_real_receipt import NS, X, request, DK, B


class CorrectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='ns001-correction-')
        self.store = Store(Path(self.tmp.name) / 'store', NS, create=True)
        self.e, self.p = preparation(X)
        freeze(self.store, self.e, self.p)
        self.a = self.store.reserve(self.e, request(self.e))

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def begin(self, p=None):
        self.a.prepare(self.p if p is None else p)
        return self.a.attempted()

    def public(self, a=None):
        a = a or self.a
        return public_accept(a, a.raw('package-manifest.json'), a.raw('package-manifest.sha256'), _all_files(a), set())

    def precondition(self, p):
        self.a.prepare(p)
        self.assertEqual(self.a.events()[-1]['state'], 'REFUSED')
        self.assertFalse(self.public())
        with self.assertRaises(Invalid):
            self.a.attempted()

    def complete(self, change=None, mutate_memory=None):
        tried = self.begin()
        o = observation(self.p, X, self.e, tried, mutate_memory=mutate_memory)
        self.a.finish(None, change(o) if change else o)
        return self.a.recover()

    def negative(self, change=None, mutate_memory=None):
        terminal = self.complete(change, mutate_memory)
        self.assertIn(terminal['state'], ('REFUSED', 'ABORTED'))
        self.assertFalse(self.public())
        return terminal

    def test_positive_raw_path_and_public_replay(self):
        terminal = self.complete()
        self.assertEqual(terminal['state'], 'ACCEPTED')
        self.assertTrue(self.public())
        self.assertTrue(verify_package(self.a, True))
        # Full binary captures do not enlarge or use the MI/JSON parser budget.
        self.assertLess(len((self.a.path / 'observer/mi.stdout').read_bytes()), 8 * 1024 * 1024)
        self.assertEqual(len((self.a.path / 'observer/text.receiver.executable.bin').read_bytes()), 3026877)

    def test_R1_inferior_before_policy(self):
        c = Chunk('stdout', b'=thread-group-started,id="i1",pid="401"\n=thread-created,id="401",group-id="i1"\n')
        self.precondition(replace(self.p, transcript=(c,) + self.p.transcript))

    def test_R1_premature_receiver_in_setup(self):
        extra = (Chunk('commands', mi_command(5000, '-exec-continue')),
            Chunk('stdout', b'5000^running\n*running,thread-id="all"\n*stopped,reason="breakpoint-hit",thread-id="401",stopped-threads="all",frame={addr="0x69bff0"}\n'))
        self.precondition(replace(self.p, transcript=self.p.transcript + extra))

    def test_R1_unexpected_software_diagnostic(self):
        extra = (Chunk('commands', mi_command(5000, '-interpreter-exec console "maintenance info breakpoints"')),
            Chunk('stdout', b'~"UNEXPECTED software breakpoint inserted at 0x581feb\\n"\n5000^done\n'))
        self.precondition(replace(self.p, transcript=self.p.transcript + extra))

    def test_R1_arbitrary_unqualified_log_also_blocks(self):
        extra = (Chunk('commands', mi_command(5000, '-interpreter-exec console "maintenance info breakpoints"')),
            Chunk('stdout', b'&"unclassified backend event\\n"\n5000^done\n'))
        self.precondition(replace(self.p, transcript=self.p.transcript + extra))

    def test_R1_missing_native_setup_measurement(self):
        self.precondition(replace(self.p, native_derivation=self.p.native_derivation[:-1]))

    def test_R2_malformed_register_names_tuple(self):
        self.negative(lambda o: replace(o, transcript=tuple(replace(c, raw=c.raw.replace(
            b'register-names=[', b'register-names={').replace(b'"rsp"]', b'"rsp"}')) for c in o.transcript)))

    def test_R2_unrelated_async_token(self):
        self.negative(lambda o: replace(o, transcript=tuple(replace(c, raw=c.raw.replace(
            b'*stopped,', b'999*stopped,')) for c in o.transcript)))

    def test_R2_duplicate_running_wrong_thread(self):
        self.negative(lambda o: replace(o, transcript=tuple(replace(c, raw=c.raw.replace(
            b'*running,thread-id="all"\n', b'*running,thread-id="all"\n*running,thread-id="999"\n')) for c in o.transcript)))

    def test_R2_contradictory_signal(self):
        self.negative(lambda o: replace(o, transcript=tuple(replace(c, raw=c.raw.replace(
            b'stopped-threads="all",frame=', b'stopped-threads="all",signal-name="SIGSEGV",frame=')) for c in o.transcript)))

    def test_R2_malformed_frame_remains_rejected(self):
        def change(o):
            return replace(o, transcript=tuple(replace(c, raw=c.raw.replace(b'frame={addr=', b'frame=[addr=').replace(
                b'frame=[addr="0x581feb"}', b'frame=[addr="0x581feb"]').replace(
                b'frame=[addr="0x69bff0"}', b'frame=[addr="0x69bff0"]')) for c in o.transcript))
        self.negative(change)

    def test_R2_matching_async_tokens_are_valid(self):
        def change(o):
            token = None
            chunks = []
            for c in o.transcript:
                if c.channel == 'commands' and b'-exec-' in c.raw:
                    token = c.raw.split(b'-', 1)[0]
                raw = c.raw.replace(b'*stopped,', token + b'*stopped,') if token else c.raw
                chunks.append(replace(c, raw=raw))
            return replace(o, transcript=tuple(chunks))
        self.assertEqual(self.complete(change)['state'], 'ACCEPTED')
        self.assertTrue(self.public())

    def swapped(self, p, role='hash_tool'):
        artifacts = {**p.artifacts, role: b'unfrozen-replacement-' + role.encode()}
        return replace(p, artifacts=artifacts, pins={**p.pins, role: digest(artifacts[role])})

    def test_R3_hash_tool_replacement_after_freeze(self):
        self.precondition(self.swapped(self.p))

    def test_R3_every_unanchored_tool_role(self):
        # No Attempt mutation: independently compare the frozen dossier for each role.
        from e0.h2.real_receipt_integration import frozen_role_codes
        for role in self.p.pins:
            with self.subTest(role=role):
                self.assertEqual(frozen_role_codes(self.store, self.swapped(self.p, role), self.e), ['ENGINE_UNQUALIFIED'])

    def test_R3_repetition_changed_tool_false(self):
        self.complete()
        e, p = preparation(NS + ':2')
        self.assertEqual(e, self.e)
        freeze(self.store, e, p)
        a = self.store.reserve(e, request(e))
        a.prepare(self.swapped(p))
        self.assertEqual(a.events()[-1]['state'], 'REFUSED')
        self.assertFalse(compare_repetition(self.a, a))

    def test_R4_null_original_buffer(self):
        self.precondition(replace(self.p, derivation=replace(self.p.derivation, original_buffer=0)))

    def test_R4_negative_fd_and_syscall_fd(self):
        self.precondition(replace(self.p, derivation=replace(self.p.derivation, fd=-1, syscall_fd=-1)))

    def test_R4_null_return_pcs(self):
        self.precondition(replace(self.p, derivation=replace(self.p.derivation, return_pc_in=0, return_pc_out=0)))

    def test_R4_self_consistent_unmeasured_derivation(self):
        self.precondition(replace(self.p, derivation=replace(self.p.derivation, fd=8, syscall_fd=8)))

    def test_R4_invalid_return_mapping(self):
        self.precondition(replace(self.p, derivation=replace(self.p.derivation, return_pc_in=0x88800, return_pc_out=0x88800)))

    def test_R4_supplied_labels_without_raw_measurement(self):
        self.precondition(replace(self.p, text_captures=()))

    def test_R4_missing_stop_text(self):
        self.negative(lambda o: replace(o, text_captures=()))

    def test_R4_absent_actual_CALL_bytes(self):
        self.negative(mutate_memory=lambda m: m.ranges.pop(0x581feb))

    def test_R4_changed_actual_CALL_bytes(self):
        self.negative(mutate_memory=lambda m: m.ranges.__setitem__(0x581feb, bytearray.fromhex('ffd1')))

    def test_R4_binary_text_mutation_with_unmodified_digest(self):
        captures = list(self.p.text_captures)
        captures[2] = replace(captures[2], raw=b'x' + captures[2].raw[1:])
        self.precondition(replace(self.p, text_captures=tuple(captures)))

    def test_R4_stop_map_handle_substitution(self):
        def change(o):
            cs = tuple(replace(c, mapping={**c.mapping, 'handle': 'other-file'}) for c in o.text_captures)
            return replace(o, text_captures=cs, maps=tuple(text_maps(cs, epoch) for epoch in ('caller', 'receiver')))
        self.negative(change)

    def test_R5_256_slots_one_byte_indices(self):
        def mutate(mem):
            old = mem.ranges[DK]
            header = bytearray(old[:32])
            header[8:10] = bytes([8, 8])
            header[16:24] = (168).to_bytes(8, 'little')
            mem.ranges[DK] = header + bytes([0, 1]) + bytes([255] * 254) + old[40:72]
        self.negative(mutate_memory=mutate)

    def test_R5_no_empty_index_READY(self):
        reads = list(self.p.ready.reads)
        for i, r in enumerate(reads):
            if r.address == DK:
                raw = bytearray(r.data)
                raw[34:40] = bytes([254] * 6)
                reads[i] = replace(r, data=bytes(raw))
        self.precondition(replace(self.p, ready=replace(self.p.ready, reads=tuple(reads))))

    def test_R6_replaced_lock_two_writers_cannot_pass(self):
        path = self.store.root / 'lock'
        path.unlink()
        path.write_bytes(b'')
        with self.assertRaises(Invalid):
            self.store.check()
        with self.assertRaises(Invalid):
            Store(self.store.root)

    def test_R6_ordinary_second_writer_denied(self):
        with self.assertRaises(Invalid):
            Store(self.store.root)
        self.store.check()

    def test_R7_post_ATTEMPTED_exec_assertion(self):
        tried = self.begin()
        self.p.guard['execution_operations'].append('exec')
        self.a.finish(None, observation(self.p, X, self.e, tried))
        terminal = self.a.recover()
        self.assertNotEqual(terminal['state'], 'ACCEPTED')
        self.assertIn('EXECUTION_PROHIBITED', [terminal['primary_code']] + terminal['diagnostics'])
        self.assertEqual(self.a._preparation.guard['execution_operations'], [])
        self.assertFalse(self.public())

    def test_R7_completion_integer_ones(self):
        self.negative(lambda o: replace(o, completion=dict.fromkeys(o.completion, 1)))

    def test_R7_each_completion_bool_exact(self):
        from e0.h2.real_receipt_observation import evaluate_capture
        from test_e0_h2_real_receipt import capture
        cap = capture()
        for k in cap.completion:
            with self.subTest(k=k):
                self.assertEqual(evaluate_capture(replace(cap, completion={**cap.completion, k: 1}),
                    X, cap.expectation_sha256, cap.attempted_sha256)[0], 'ABORT')

    def rehash(self):
        files = _all_files(self.a)
        capfiles = {n: raw for n, raw in files.items() if n.startswith('qualification/') or n.startswith('1/observer/')}
        h = digest(canonical(self.e))
        (self.a.path / 'capture-manifest.json').write_bytes(canonical(manifest('capture', X, h, capfiles)))
        files = _all_files(self.a)
        raw = canonical(manifest('package', X, h, files))
        (self.a.path / 'package-manifest.json').write_bytes(raw)
        (self.a.path / 'package-manifest.sha256').write_bytes((digest(raw) + '\n').encode())

    def test_R8_rehashed_missing_original_evidence(self):
        self.complete()
        before = self.a.raw('events.jsonl')
        for name in ('capture.json', 'observer/native-stops.json'):
            (self.a.path / name).unlink()
        self.rehash()
        self.assertFalse(self.public())
        self.assertEqual(self.a.recover()['state'], 'ACCEPTED')
        self.assertEqual(before, self.a.raw('events.jsonl'))

    def test_R8_rehashed_missing_binary_text(self):
        self.complete()
        (self.a.path / 'observer/text.receiver.executable.bin').unlink()
        self.rehash()
        self.assertFalse(self.public())

    def test_R8_rehashed_contradictory_original_capture(self):
        self.complete()
        raw = parse(self.a.raw('capture.json'))
        raw['native_stops'][1]['pc'] = 0
        (self.a.path / 'capture.json').write_bytes(canonical(raw))
        self.rehash()
        self.assertFalse(self.public())

    def test_R9_guard_execution_plus_incomplete_death(self):
        terminal = self.negative(lambda o: replace(o, guard_operations=('execution',),
            completion={**o.completion, 'pidfd_death_confirmed': False}))
        self.assertEqual(terminal['state'], 'ABORTED')
        self.assertIn('EXECUTION_PROHIBITED', terminal['diagnostics'])
        self.assertEqual(self.a.recover(), terminal)

    def test_R9_wrong_mode_and_wrong_seals_ranked_refusal(self):
        r = parse(request(self.e))
        r['parameters']['mode'] = 'eval'
        # Replace synthetic request and exact corresponding registration link before preparation.
        (self.a.path / 'request.json').write_bytes(canonical(r))
        reg = parse(self.a.raw('registration.json'))
        reg['request_sha256'] = digest(canonical(r))
        (self.a.path / 'registration.json').write_bytes(canonical(reg))
        self.a.prepare(replace(self.p, protected={**self.p.protected, 'seals': 0}))
        terminal = self.a.recover()
        self.assertEqual(terminal['state'], 'REFUSED')
        self.assertEqual(terminal['primary_code'], 'WRONG_PROTECTED_OBJECT')
        self.assertIn('WRONG_ENTRYPOINT', terminal['diagnostics'])
        self.assertFalse(self.public())

    def test_R9_guard_fault_before_MI_parse_failure(self):
        terminal = self.negative(lambda o: replace(o, guard_operations=('execution',),
            transcript=o.transcript + (Chunk('stdout', b'bad-mi\n'),)))
        self.assertIn('EXECUTION_PROHIBITED', terminal['diagnostics'])

    def test_R9_execution_fault_before_interruption(self):
        terminal = self.negative(lambda o: replace(o, guard_operations=('execution',), interrupted=True))
        self.assertIn('EXECUTION_PROHIBITED', terminal['diagnostics'])


    def test_R1_native_controls_required(self):
        self.precondition(replace(self.p, native_controls=()))

    def test_R1_failed_kernel_slot_programming(self):
        controls = list(self.p.native_controls)
        controls[1] = {**controls[1], 'result': -1}
        self.precondition(replace(self.p, native_controls=tuple(controls)))

    def test_R1_unqualified_control_trap(self):
        controls = list(self.p.native_controls)
        controls[2] = {**controls[2], 'siginfo_code': 2}
        self.precondition(replace(self.p, native_controls=tuple(controls)))

    def test_R5_valid_256_slots_two_byte_indices(self):
        from e0.h2.real_receipt_abi import Decoder, Snapshot
        from test_e0_h2_real_receipt import native_memory, DICT, C
        mem = native_memory()
        old = mem.ranges[DK]
        header = bytearray(old[:32])
        header[8:10] = bytes([8, 9])
        header[16:24] = (168).to_bytes(8, 'little')
        mem.ranges[DK] = header + bytes([0, 0, 1, 0]) + bytes([255] * 508) + old[40:72]
        self.assertEqual(Decoder(Snapshot(mem.reads())).dictionary(DICT)[0]['compile'], C)

    def test_R7_internal_snapshot_change_blocks(self):
        tried = self.begin()
        self.a._preparation.guard['execution_operations'].append('exec')
        self.a.finish(None, observation(self.p, X, self.e, tried))
        self.assertNotEqual(self.a.recover()['state'], 'ACCEPTED')
        self.assertFalse(self.public())

    def test_R8_rehashed_conflicting_map_file(self):
        self.complete()
        (self.a.path / 'observer/maps.stop1').write_bytes(canonical([]))
        self.rehash()
        self.assertFalse(self.public())

    def test_R8_rehashed_conflicting_setup_transcript(self):
        self.complete()
        (self.a.path / 'observer/setup.mi.stdout').write_bytes(b'')
        self.rehash()
        self.assertFalse(self.public())

    def test_R9_multiple_precondition_stages_keep_guard_diagnostics(self):
        p = replace(self.p, protected={**self.p.protected, 'seals': 0},
            guard={**self.p.guard, 'execution_operations': ['exec']})
        self.precondition(p)
        terminal = self.a.recover()
        self.assertEqual(terminal['primary_code'], 'WRONG_PROTECTED_OBJECT')
        self.assertIn('EXECUTION_PROHIBITED', terminal['diagnostics'])

    def test_R9_incomplete_keeps_non_guard_fault(self):
        terminal = self.negative(lambda o: replace(o, protected_final={**o.protected_final, 'seals': 0},
            completion={**o.completion, 'pidfd_death_confirmed': False}))
        self.assertIn('OBJECT_SUBSTITUTION', terminal['diagnostics'])

    def test_R1_receiver_monitor_cannot_be_missing(self):
        chunks = tuple(c for c in self.p.transcript if b'-break-insert -h *0x69bff0' not in c.raw and
                       not c.raw.startswith(b'30^done'))
        self.precondition(replace(self.p, transcript=chunks))

    def test_R1_receiver_monitor_cannot_be_retired(self):
        chunks = self.p.transcript + (Chunk('commands', mi_command(5000, '-break-delete 1')),
                                     Chunk('stdout', b'5000^done\n'))
        self.precondition(replace(self.p, transcript=chunks))

    def test_R1_native_control_exact_integer_result(self):
        controls = list(self.p.native_controls)
        controls[1] = {**controls[1], 'result': False}
        self.precondition(replace(self.p, native_controls=tuple(controls)))
