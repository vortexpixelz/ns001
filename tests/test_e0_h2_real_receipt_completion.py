"""Bounded integrated tests using synthetic/retained evidence only."""
import copy
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from e0.h2.real_receipt_policy import Invalid, Q1, canonical, parse, digest, mi_command
from e0.h2.real_receipt_evidence import Store, Attempt, public_accept
from e0.h2.real_receipt_integration import (Transcript, Chunk, preparation_codes, compare_repetition,
    verify_package, package_recovery, _all_files, _package)
from real_receipt_fixtures import preparation, observation, freeze
from test_e0_h2_real_receipt import NS, X, request, B, TYPES


class IntegratedTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
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

    def complete(self, mutate=None):
        tried = self.begin()
        o = observation(self.p, X, self.e, tried)
        self.a.finish(None, mutate(o) if mutate else o)
        return o

    def test_positive_complete_package(self):
        self.complete()
        self.assertEqual(self.a.events()[-1]['state'], 'ACCEPTED')
        self.assertTrue(verify_package(self.a, True))
        self.assertTrue(public_accept(self.a, self.a.raw('package-manifest.json'),
            self.a.raw('package-manifest.sha256'), _all_files(self.a), set()))

    def test_required_durable_order(self):
        import e0.h2.real_receipt_evidence as evidence
        original, seen = evidence.retain, []
        def retained(path, raw):
            seen.append(path.name)
            return original(path, raw)
        tried = self.begin()
        with patch.object(evidence, 'retain', side_effect=retained):
            self.a.finish(None, observation(self.p, X, self.e, tried))
        for before, after in (('completion.json', 'capture-manifest.json'), ('capture-manifest.json', 'witness.json'),
                              ('witness.json', 'package-started'), ('package-started', 'package-manifest.json'),
                              ('package-manifest.json', 'package-manifest.sha256')):
            self.assertLess(seen.index(before), seen.index(after))

    def test_no_prepared_bypass(self):
        self.a.prepare()
        self.assertEqual(self.a.events()[-1]['state'], 'REFUSED')
        self.assertEqual(self.a.events()[-1]['primary_code'], 'EXPECTATION_INVALID')
        with self.assertRaises(Invalid):
            self.a.attempted()

    def test_direct_event_cannot_bypass_preparation(self):
        with self.assertRaises(Invalid):
            self.a.event('PREPARED', entered=False)

    def test_observer_cannot_backfill_attempted(self):
        self.a.prepare(self.p)
        before = self.a.raw('events.jsonl')
        with self.assertRaises(Invalid):
            self.a.finish(None, observation(self.p, X, self.e, '3' * 64))
        self.assertEqual(before, self.a.raw('events.jsonl'))

    def test_wrong_engine_precondition_refused(self):
        p = replace(self.p, engine={**self.p.engine, 'sha256': '3' * 64})
        self.a.prepare(p)
        self.assertEqual([e['state'] for e in self.a.events()], ['REFUSED'])
        self.assertEqual(self.a.events()[0]['primary_code'], 'ENGINE_UNQUALIFIED')
        self.assertTrue(verify_package(self.a))
        self.assertFalse(verify_package(self.a, True))

    def test_wrong_callable_preparation(self):
        reads = list(self.p.ready.reads)
        for i, r in enumerate(reads):
            if r.address == 0x11000:
                b = bytearray(r.data)
                b[48:56] = (0x581f91).to_bytes(8, 'little')
                reads[i] = replace(r, data=bytes(b))
        self.a.prepare(replace(self.p, ready=replace(self.p.ready, reads=tuple(reads))))
        self.assertEqual(self.a.events()[-1]['state'], 'REFUSED')
        self.assertEqual(self.a.events()[-1]['primary_code'], 'WRONG_COMPILE_CALLABLE')

    def test_wrong_custody(self):
        self.a.prepare(replace(self.p, custody={**self.p.custody, 'namespace': '9' * 64}))
        self.assertEqual(self.a.events()[-1]['primary_code'], 'OBSERVER_UNQUALIFIED')

    def test_bootstrap_conflict(self):
        self.a.prepare(replace(self.p, bootstrap={**self.p.bootstrap, 'retries': 1}))
        self.assertEqual(self.a.events()[-1]['state'], 'REFUSED')

    def test_missing_artifact_pin(self):
        pins = dict(self.p.pins)
        del pins['launcher_gdb']
        self.a.prepare(replace(self.p, pins=pins))
        self.assertEqual(self.a.events()[-1]['primary_code'], 'ENGINE_UNQUALIFIED')

    def test_guard_conflict(self):
        self.a.prepare(replace(self.p, guard={**self.p.guard, 'execution_operations': ['exec']}))
        self.assertEqual(self.a.events()[-1]['state'], 'REFUSED')
        self.assertEqual(self.a.events()[-1]['primary_code'], 'EXECUTION_PROHIBITED')

    def test_policy_actual_readback_off_to_on(self):
        chunks = tuple(replace(c, raw=c.raw.replace(b'show may-write-memory : off', b'show may-write-memory : on')) for c in self.p.transcript)
        self.a.prepare(replace(self.p, transcript=chunks))
        self.assertEqual(self.a.events()[-1]['primary_code'], 'OBSERVER_UNQUALIFIED')

    def test_individual_autoload_facility_must_be_off(self):
        chunks = tuple(replace(c, raw=c.raw.replace(b'auto-load python-scripts : off', b'auto-load python-scripts : on')) for c in self.p.transcript)
        self.a.prepare(replace(self.p, transcript=chunks))
        self.assertEqual(self.a.events()[-1]['primary_code'], 'OBSERVER_UNQUALIFIED')

    def test_unknown_software_inventory(self):
        adm = {**self.p.admission, 'loader_inventory': self.p.admission['loader_inventory'] + [{'type': 'software'}]}
        self.a.prepare(replace(self.p, admission=adm))
        self.assertEqual(self.a.events()[-1]['primary_code'], 'OBSERVER_UNQUALIFIED')

    def test_unmasked_capture_mismatch(self):
        adm = copy.deepcopy(self.p.admission)
        adm['text'][1]['supervisor_sha256'] = '9' * 64
        self.a.prepare(replace(self.p, admission=adm))
        self.assertEqual(self.a.events()[-1]['primary_code'], 'ENGINE_UNQUALIFIED')

    def test_hardware_ineffective(self):
        adm = copy.deepcopy(self.p.admission)
        adm['controls'][0]['programming'] = 'debug-register-mirror-only'
        self.a.prepare(replace(self.p, admission=adm))
        self.assertEqual(self.a.events()[-1]['primary_code'], 'OBSERVER_NOT_ARMED')

    def test_wrong_dispatch_attempt(self):
        self.complete(lambda o: replace(o, dispatch={**o.dispatch, 'attempt_id': NS + ':9'}))
        self.assertEqual(parse(self.a.raw('recovery.json'))['primary_code'], 'RECORD_INVALID')
        self.assertFalse(verify_package(self.a, True))

    def test_wrong_dispatch_event_link(self):
        self.complete(lambda o: replace(o, dispatch={**o.dispatch, 'attempted_sha256': '9' * 64}))
        self.assertEqual(self.a.events()[-1]['state'], 'REFUSED')
        self.assertEqual(self.a.events()[-1]['primary_code'], 'OBSERVATION_MISSING')

    def test_interrupt_with_raw_preservation(self):
        o = self.complete(lambda o: replace(o, interrupted=True))
        self.assertEqual(parse(self.a.raw('recovery.json'))['state'], 'ABORTED')
        self.assertEqual((self.a.path / 'observer/mi.stdout').read_bytes(), b''.join(c.raw for c in o.transcript if c.channel == 'stdout'))

    def test_guard_execution_invalidates(self):
        self.complete(lambda o: replace(o, guard_operations=('execution',)))
        terminal = self.a.events()[-1]
        self.assertEqual(terminal['state'], 'REFUSED')
        self.assertIn('EXECUTION_PROHIBITED', [terminal['primary_code']] + terminal['diagnostics'])

    def test_guard_refusal_precedence(self):
        self.complete(lambda o: replace(o, guard_operations=('payload_reopen', 'execution')))
        self.assertEqual(self.a.events()[-1]['primary_code'], 'PATHNAME_REOPEN')

    def test_transcript_wrong_pid_aborts(self):
        self.complete(lambda o: replace(o, transcript=tuple(replace(c, raw=c.raw.replace(b'pid="401"', b'pid="402"')) for c in o.transcript)))
        self.assertEqual(parse(self.a.raw('recovery.json'))['state'], 'ABORTED')

    def test_missing_native_trap_never_becomes_receipt(self):
        self.complete(lambda o: replace(o, native_stops=()))
        self.assertEqual(parse(self.a.raw('recovery.json'))['state'], 'ABORTED')

    def test_conflicting_native_trap_never_becomes_receipt(self):
        def mutate(o):
            records = list(o.native_stops)
            records[1] = {**records[1], 'tid': 999}
            return replace(o, native_stops=tuple(records))
        self.complete(mutate)
        self.assertEqual(parse(self.a.raw('recovery.json'))['state'], 'ABORTED')

    def test_missing_native_stop_aborts(self):
        self.complete(lambda o: replace(o, transcript=tuple(replace(c, raw=c.raw.split(b'*stopped')[0])
            if b'frame={addr="0x69bff0"}' in c.raw else c for c in o.transcript)))
        self.assertEqual(parse(self.a.raw('recovery.json'))['state'], 'ABORTED')

    def test_mutated_native_bytes_refused(self):
        tried = self.begin()
        def mutate(mem):
            mem.ranges[B][32] = 32
        self.a.finish(None, observation(self.p, X, self.e, tried, mutate_memory=mutate))
        self.assertEqual(self.a.events()[-1]['primary_code'], 'INPUT_ALTERED')

    def test_actual_nonbytes_refused(self):
        tried = self.begin()
        def mutate(mem):
            mem.word(B, 8, TYPES['str'])
        self.a.finish(None, observation(self.p, X, self.e, tried, mutate_memory=mutate))
        self.assertEqual(self.a.events()[-1]['primary_code'], 'INPUT_TYPE')

    def test_actual_argument_substitution(self):
        tried = self.begin()
        self.a.finish(None, observation(self.p, X, self.e, tried, mutate_memory=lambda m: m.string(0x18000, '<wrong>')))
        self.assertEqual(self.a.events()[-1]['primary_code'], 'WRONG_ENTRYPOINT')

    def test_observed_keyword_not_replaced_by_expected_name(self):
        tried = self.begin()
        self.a.finish(None, observation(self.p, X, self.e, tried, mutate_memory=lambda m: m.string(0x1a000, '_wrong_keyword')))
        w = parse(self.a.raw('witness.json'))
        self.assertEqual(w['observations'][6]['data']['keyword_names'], ['_wrong_keyword'])
        self.assertEqual(self.a.events()[-1]['primary_code'], 'WRONG_ENTRYPOINT')

    def test_unsupported_string_not_coerced(self):
        tried = self.begin()
        self.a.finish(None, observation(self.p, X, self.e, tried, mutate_memory=lambda m: m.string(0x18000, '\n')))
        w = parse(self.a.raw('witness.json'))
        self.assertIsNone(w['observations'][6]['data']['parameters'])
        self.assertEqual(self.a.events()[-1]['primary_code'], 'WRONG_ENTRYPOINT')

    def test_missing_required_artifact_blocks_public_accept(self):
        self.complete()
        before = self.a.raw('events.jsonl')
        (self.a.path / 'observer/B.entry.bin').unlink()
        self.assertFalse(verify_package(self.a, True))
        self.assertEqual(self.a.recover()['state'], 'ACCEPTED')
        self.assertEqual(self.a.raw('events.jsonl'), before)

    def test_package_sidecar_mismatch(self):
        self.complete()
        (self.a.path / 'package-manifest.sha256').write_bytes(b'9' * 64 + b'\n')
        self.assertFalse(verify_package(self.a, True))

    def test_reopened_terminal_cannot_start_packaging(self):
        self.complete()
        reopened = Attempt(self.store, 1)
        with self.assertRaises(Invalid):
            _package(reopened)

    def test_bad_typed_guard_cannot_be_absence(self):
        self.a.prepare(replace(self.p, guard={**self.p.guard, 'execution_operations': None}))
        self.assertEqual(self.a.events()[-1]['primary_code'], 'OBSERVER_UNQUALIFIED')

    def test_repetition_positive_distinct_originals_retained(self):
        self.complete()
        before = self.a.raw('events.jsonl')
        e2, p2 = preparation(NS + ':2')
        self.assertEqual(canonical(e2), canonical(self.e))
        freeze(self.store, e2, p2)
        b = self.store.reserve(e2, request(e2))
        b.prepare(p2)
        tried = b.attempted()
        b.finish(None, observation(p2, b.x, e2, tried))
        self.assertTrue(compare_repetition(self.a, b))
        self.assertEqual(before, self.a.raw('events.jsonl'))
        self.assertFalse(compare_repetition(self.a, self.a))

    def test_repetition_negative_case_id_not_normalized(self):
        self.complete()
        e2, p2 = preparation(NS + ':2')
        raw = parse(request(e2))
        raw['case_id'] = 'N01'
        b = self.store.reserve(e2, canonical(raw))
        b.prepare(p2)
        tried = b.attempted()
        b.finish(None, observation(p2, b.x, e2, tried))
        self.assertTrue(verify_package(b, True))
        self.assertFalse(compare_repetition(self.a, b))

    def test_repetition_negative_changed_capture(self):
        self.complete()
        e2, p2 = preparation(NS + ':2')
        b = self.store.reserve(e2, request(e2))
        b.prepare(p2)
        tried = b.attempted()
        b.finish(None, observation(p2, b.x, e2, tried))
        (b.path / 'observer/A.entry.bin').write_bytes(b' \n')
        self.assertFalse(compare_repetition(self.a, b))


class ReservedRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.tmp.name) / 'store', NS, create=True)
        self.e, self.p = preparation(X)
        freeze(self.store, self.e, self.p)
        self.a = self.store.reserve_only(self.e)

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def test_reserved_only_absence_preserved_idempotent_abort(self):
        reservation = (self.store.root / 'reservations/1').read_bytes()
        self.assertFalse(self.a.path.exists())
        result = package_recovery(self.a)
        self.assertEqual(result['state'], 'ABORTED')
        for k in ('registration_sha256', 'request_sha256', 'witness_sha256', 'journal_sha256'):
            self.assertIsNone(result[k])
        self.assertFalse((self.a.path / 'request.json').exists())
        self.assertFalse((self.a.path / 'registration.json').exists())
        self.assertEqual(reservation, (self.store.root / 'reservations/1').read_bytes())
        before = self.a.raw('recovery.json')
        self.assertEqual(result, package_recovery(self.a))
        self.assertEqual(before, self.a.raw('recovery.json'))
        self.assertTrue(verify_package(self.a))
        self.assertFalse(verify_package(self.a, True))
        with self.assertRaises(Invalid):
            self.a.register(request(self.e))
        b = self.store.reserve_only(self.e)
        self.assertEqual(b.x, NS + ':2')

    def test_partial_request_retained(self):
        self.a.path.mkdir()
        (self.a.path / 'request.json').write_bytes(b'{"schema"')
        self.assertEqual(self.a.recover()['primary_code'], 'ATTEMPT_INCOMPLETE')
        self.assertEqual(self.a.raw('request.json'), b'{"schema"')

    def test_complete_invalid_request(self):
        self.a.path.mkdir()
        (self.a.path / 'request.json').write_bytes(b'{}\n')
        self.assertEqual(self.a.recover()['primary_code'], 'RECORD_INVALID')

    def test_reservation_torn_record_retained(self):
        path = self.store.root / 'reservations/1'
        path.write_bytes(b'{')
        self.assertEqual(self.a.recover()['state'], 'ABORTED')
        self.assertEqual(path.read_bytes(), b'{')
        with self.assertRaises(Invalid):
            self.store.reserve_only(self.e)

    def test_missing_reservation_stops(self):
        (self.store.root / 'reservations/1').unlink()
        with self.assertRaises(Invalid):
            self.a.recover()

    def test_conflicting_recovery_stops(self):
        self.a.recover()
        before = self.a.raw('recovery.json')
        (self.a.path / 'events.jsonl').write_bytes(b'{}\n')
        with self.assertRaises(Invalid):
            self.a.recover()
        self.assertEqual(before, self.a.raw('recovery.json'))


class TranscriptIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.e, self.p = preparation(X)
        self.o = observation(self.p, X, self.e, '3' * 64)

    def test_fragmented_stdout_preserved(self):
        fragmented = []
        for c in self.o.transcript:
            if c.channel == 'stdout':
                fragmented += [Chunk('stdout', c.raw[:1]), Chunk('stdout', c.raw[1:])]
            else:
                fragmented.append(c)
        t = Transcript(fragmented)
        self.assertEqual(t.raw['stdout'], b''.join(c.raw for c in self.o.transcript if c.channel == 'stdout'))
        self.assertEqual(len(t.stops), 2)

    def test_result_and_stop_orderings(self):
        chunks = list(self.o.transcript)
        for i in range(len(chunks) - 1):
            if b'^running' in chunks[i].raw and b'*stopped' in chunks[i + 1].raw:
                chunks[i], chunks[i + 1] = chunks[i + 1], chunks[i]
        self.assertEqual(len(Transcript(chunks).stops), 2)

    def test_missing_result(self):
        chunks = [c for c in self.o.transcript if c.raw != b'100^running\n']
        with self.assertRaises(Invalid):
            Transcript(chunks)

    def test_duplicate_result(self):
        chunks = list(self.o.transcript)
        chunks.insert(3, Chunk('stdout', b'100^running\n'))
        with self.assertRaises(Invalid):
            Transcript(chunks)

    def test_ambiguous_stop(self):
        chunks = tuple(replace(c, raw=c.raw.replace(b'reason="end-stepping-range"', b'reason="signal-received"')) for c in self.o.transcript)
        t = Transcript(chunks)
        with self.assertRaises(Invalid):
            t.snapshot(1, self.p.custody, self.p.ready.roots, self.p.q1['native_reasons'])

    def test_partial_memory_result(self):
        chunks = tuple(replace(c, raw=c.raw.replace(b'contents="0100000000000000"', b'contents="01"')) for c in self.o.transcript)
        # Direct malformed response independent of fixture object contents.
        p = [Chunk('commands', mi_command(1, '-exec-continue')), Chunk('stdout', b'1^running\n*stopped,reason="breakpoint-hit",thread-id="401",stopped-threads="all",frame={addr="0x581feb"}\n'),
             Chunk('commands', mi_command(2, '-data-read-memory-bytes 0x10000 2')),
             Chunk('stdout', b'2^done,memory=[{begin="0x10000",offset="0x0",end="0x10002",contents="23"}]\n')]
        with self.assertRaises(Invalid):
            Transcript(p)

    def test_software_breakpoint_evidence(self):
        chunks = [Chunk('commands', mi_command(1, '-break-insert -h *0x69bff0')),
            Chunk('stdout', b'1^done,bkpt={type="breakpoint",enabled="y",addr="0x69bff0"}\n')]
        with self.assertRaises(Invalid):
            Transcript(chunks)

    def test_named_result_list_preserves_order(self):
        from e0.h2.real_receipt_observation import MIParser
        p = MIParser()
        p.command(mi_command(1, '-break-list'))
        record = p.feed(b'1^done,BreakpointTable={body=[bkpt={type="hw breakpoint"},bkpt={type="hw breakpoint"}]}\n')
        self.assertEqual(len(record.fields['BreakpointTable']['body']), 2)

    def test_software_inventory_evidence_denied(self):
        with self.assertRaises(Invalid):
            Transcript([Chunk('commands', mi_command(1, '-break-list')),
                Chunk('stdout', b'1^done,BreakpointTable={body=[bkpt={type="breakpoint"}]}\n')])

    def test_raw_stderr_separated(self):
        t = Transcript(self.o.transcript + (Chunk('stderr', b'100^done\n'),))
        self.assertEqual(t.raw['stderr'], b'100^done\n')
        self.assertNotIn(b'100^done', t.raw['stdout'])

    def test_unexpected_q1_stderr(self):
        t = Transcript(self.p.transcript + (Chunk('stderr', b'software fallback\n'),))
        with self.assertRaises(Invalid):
            t.readbacks(self.p.q1)

    def test_wrong_token(self):
        chunks = tuple(replace(c, raw=c.raw.replace(b'100^running', b'999^running')) for c in self.o.transcript)
        with self.assertRaises(Invalid):
            Transcript(chunks)

    def test_raw_truncation(self):
        chunks = self.o.transcript[:-1] + (replace(self.o.transcript[-1], raw=self.o.transcript[-1].raw[:-1]),)
        with self.assertRaises(Invalid):
            Transcript(chunks)


# Avoid rerunning IntegratedTests merely to share its fixture setup.
class CutTests(unittest.TestCase):
    setUp = IntegratedTests.setUp
    tearDown = IntegratedTests.tearDown
    begin = IntegratedTests.begin


def _cut_test(name):
    def test(self):
        import e0.h2.real_receipt_evidence as evidence
        original = evidence.retain
        tried = self.begin()
        def cut(path, raw):
            if path.name == name:
                # Exactly one bounded halfway write; no repair or retry.
                path.write_bytes(raw[:max(1, len(raw) // 2)])
                raise OSError('synthetic interrupted write')
            return original(path, raw)
        with patch.object(evidence, 'retain', side_effect=cut):
            with self.assertRaises(OSError):
                self.a.finish(None, observation(self.p, X, self.e, tried))
        before = self.a.raw('events.jsonl')
        terminal = self.a.recover()
        if name in ('package-manifest.json', 'package-manifest.sha256'):
            self.assertEqual(terminal['state'], 'ACCEPTED')
            self.assertEqual(self.a.raw('events.jsonl'), before)
            self.assertFalse(verify_package(self.a, True))
            with self.assertRaises(Invalid):
                _package(self.a)
        else:
            self.assertEqual(terminal['state'], 'ABORTED')
        self.assertFalse(verify_package(self.a, True))
    return test


for _name in ('stop1.json', 'capture-manifest.json', 'witness.json', 'package-manifest.json', 'package-manifest.sha256'):
    setattr(CutTests, 'test_halfway_cut_' + _name.replace('.', '_'), _cut_test(_name))


class RecordCutTests(unittest.TestCase):
    setUp = IntegratedTests.setUp
    tearDown = IntegratedTests.tearDown
    begin = IntegratedTests.begin
    complete = IntegratedTests.complete

    def test_halfway_registration_cut(self):
        raw = self.a.raw('registration.json')
        torn = raw[:len(raw) // 2]
        (self.a.path / 'registration.json').write_bytes(torn)
        self.assertEqual(self.a.recover()['state'], 'ABORTED')
        self.assertEqual(self.a.raw('registration.json'), torn)

    def test_halfway_reservation_cut(self):
        path = self.store.root / 'reservations/1'
        raw = path.read_bytes()
        path.write_bytes(raw[:len(raw) // 2])
        self.assertEqual(self.a.recover()['state'], 'ABORTED')
        self.assertEqual(path.read_bytes(), raw[:len(raw) // 2])
        with self.assertRaises(Invalid):
            self.a.attempted()

    def test_halfway_prepared_cut(self):
        self.a.prepare(self.p)
        raw = self.a.raw('events.jsonl')
        torn = raw[:len(raw) // 2]
        (self.a.path / 'events.jsonl').write_bytes(torn)
        self.assertEqual(self.a.recover()['valid_prefix_length'], 0)
        self.assertEqual(self.a.raw('events.jsonl'), torn)

    def test_halfway_attempted_cut(self):
        self.begin()
        first, attempted = self.a.raw('events.jsonl').splitlines(keepends=True)
        torn = first + attempted[:len(attempted) // 2]
        (self.a.path / 'events.jsonl').write_bytes(torn)
        result = self.a.recover()
        self.assertEqual(result['state'], 'ABORTED')
        self.assertEqual(result['valid_prefix_length'], len(first))
        self.assertEqual(self.a.raw('events.jsonl'), torn)

    def test_halfway_terminal_cut(self):
        self.complete()
        first, second, terminal = self.a.raw('events.jsonl').splitlines(keepends=True)
        torn = first + second + terminal[:len(terminal) // 2]
        (self.a.path / 'events.jsonl').write_bytes(torn)
        self.assertEqual(self.a.recover()['state'], 'ABORTED')
        self.assertEqual(self.a.raw('events.jsonl'), torn)

    def test_halfway_recovery_cut(self):
        self.a.recover()
        raw = self.a.raw('recovery.json')
        torn = raw[:len(raw) // 2]
        (self.a.path / 'recovery.json').write_bytes(torn)
        with self.assertRaises(Invalid):
            self.a.recover()
        self.assertEqual(self.a.raw('recovery.json'), torn)
        with self.assertRaises(Invalid):
            self.a.prepare(self.p)
