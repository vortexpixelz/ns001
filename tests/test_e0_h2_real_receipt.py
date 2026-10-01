"""Offline only: constructed byte snapshots, MI strings, temporary evidence stores.

No GDB, inferior, candidate compile/eval/exec/import, memfd or process-control test.
"""
import copy
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from e0.h2.real_receipt_policy import (Invalid, ENGINE, Q1, READBACKS, PARAMETERS, PROFILE,
    DIGEST, SCHEMA, canonical, parse, digest, ranked, engine_admission,
    initialization_plan, mi_command, validate_q1)
from e0.h2.real_receipt_abi import Decoder, Snapshot, Read, TYPES, TRUE
from e0.h2.real_receipt_observation import (MIParser, Stop, Derivation, Capture,
    evaluate_capture, byte_codes, paired_codes, derivation_codes)
from e0.h2.real_receipt_evidence import (Store, Attempt, validate, witness_codes,
    manifest, verify_manifest, public_accept, journal_prefix)

NS = 'a' * 64
X = NS + ':1'
B, C, M = 0x10000, 0x11000, 0x12000
VECTOR, KW, ROOT, DICT, DK = 0x13000, 0x14000, 0x15000, 0x16000, 0x17000


def expectation():
    return dict(schema=SCHEMA + 'expectation.v1', spec_sha256='b' * 64, profile=PROFILE,
        fixture={'length': 2, 'sha256': DIGEST}, parameters=copy.deepcopy(PARAMETERS),
        engine=dict(implementation='CPython', version='3.12.3', build_sha256='c' * 64,
            abi=ENGINE['abi'], callable='builtins.compile', interface_sha256='d' * 64,
            images=[dict(role=r, sha256=ENGINE['gdb_sha256'] if r == 'observer_native' else ENGINE['sha256'],
                         origin_sha256='e' * 64) for r in ('compiler', 'executable', 'observer_native')]),
        bootstrap_sha256='f' * 64, observer_sha256='1' * 64,
        qualification_sha256='2' * 64, source_policy='sealed-bytes-only')


def request(e):
    return canonical(dict(schema=SCHEMA + 'request.v1', expectation_sha256=digest(canonical(e)),
        case_id='P01', profile=PROFILE, parameters=copy.deepcopy(PARAMETERS),
        source_channel='protected_bytes', source_environment={}, cwd_policy='exclusive-synthetic'))


class Memory:
    def __init__(self):
        self.ranges = {}

    def object(self, p, kind, length):
        data = bytearray(length)
        data[8:16] = TYPES[kind].to_bytes(8, 'little')
        self.ranges[p] = data
        return data

    def word(self, p, offset, value, width=8, signed=False):
        self.ranges[p][offset:offset + width] = value.to_bytes(width, 'little', signed=signed)

    def string(self, p, value, kind=1, compact=True, ascii_=True):
        raw = b''.join(ord(c).to_bytes(kind, 'little') for c in value)
        offset = 40 if ascii_ else 56
        self.object(p, 'str', offset + len(raw) + kind if compact else 64)
        self.word(p, 16, len(value))
        self.word(p, 32, (kind << 2) | (32 if compact else 0) | (64 if ascii_ else 0), 4)
        if compact:
            self.ranges[p][offset:offset + len(raw)] = raw
        else:
            self.word(p, 56, p + 0x80)
            self.ranges[p + 0x80] = bytearray(raw + bytes(kind))

    def integer(self, p, value, kind='int'):
        digits = []
        n = abs(value)
        while n:
            digits.append(n & ((1 << 30) - 1))
            n >>= 30
        self.object(p, kind, 24 + max(4, 4 * len(digits)))
        sign = 1 if value == 0 else 2 if value < 0 else 0
        self.word(p, 16, (len(digits) << 3) | sign)
        for i, d in enumerate(digits):
            self.word(p, 24 + i * 4, d, 4)

    def reads(self):
        return tuple(Read(p, len(v), bytes(v)) for p, v in sorted(self.ranges.items()))


def native_memory(x=X, ehash=None):
    ehash = ehash or digest(canonical(expectation()))
    mem = Memory()
    mem.object(B, 'bytes', 35)
    mem.word(B, 16, 2)
    mem.ranges[B][32:34] = b'#\n'
    strings = {0x18000: PARAMETERS['filename'], 0x19000: 'exec', 0x1a000: '_feature_version',
               0x1b000: 'compile', 0x1c000: '_ns001_observer_roots_v1', 0x1d000: x, 0x1e000: ehash}
    for p, value in strings.items():
        mem.string(p, value)
    mem.integer(0x1f000, 0)
    mem.integer(0x20000, -1)
    mem.integer(TRUE, 1, 'bool')
    mem.object(KW, 'tuple', 32)
    mem.word(KW, 16, 1)
    mem.word(KW, 24, 0x1a000)
    mem.object(ROOT, 'tuple', 56)
    mem.word(ROOT, 16, 4)
    for i, p in enumerate((B, C, 0x1d000, 0x1e000)):
        mem.word(ROOT, 24 + 8 * i, p)
    mem.ranges[VECTOR] = bytearray(b''.join(p.to_bytes(8, 'little') for p in
        (B, 0x18000, 0x19000, 0x1f000, TRUE, 0x1f000, 0x20000)))
    mem.object(C, 'cfunction', 56)
    mem.word(C, 16, 0xa49ae0)
    mem.word(C, 24, M)
    mem.word(C, 48, 0x581f90)
    mem.ranges[0xa49ae0] = bytearray(24)
    mem.word(0xa49ae0, 8, 0x69bff0)
    mem.word(0xa49ae0, 16, 0x82, 4)
    mem.object(M, 'module', 24)
    mem.word(M, 16, DICT)
    mem.object(DICT, 'dict', 48)
    mem.word(DICT, 16, 2)
    mem.word(DICT, 24, 11)
    mem.word(DICT, 32, DK)
    mem.ranges[DK] = bytearray(72)
    mem.word(DK, 8, 3, 1)
    mem.word(DK, 9, 3, 1)
    mem.word(DK, 10, 1, 1)
    mem.word(DK, 16, 3)
    mem.word(DK, 24, 2)
    mem.ranges[DK][32:40] = bytes([0, 1, 255, 255, 255, 255, 255, 255])
    for offset, value in ((40, 0x1b000), (48, C), (56, 0x1c000), (64, ROOT)):
        mem.word(DK, offset, value)
    mem.ranges[0x30000] = bytearray((0x581fed).to_bytes(8, 'little'))
    return mem


def q1():
    settings = dict(zip(READBACKS[:26], Q1))
    names = ('before_inferior continuous_policy empty_initial_inventory stopping_on register_control_on '
        'observer_off auto_load_all_off classic_loader_denied_disabled no_unexpected_internal_sites '
        'no_libthread_db native_exec_event ptrace_syscall_events in_place_single_call_step '
        'receiver_stays_armed raw_unmasked_text_equal complete_text_ranges two_effective_slots '
        'kernel_programming_witnessed blocked_gate_restop death_chain_qualified no_software_fallback '
        'no_post_entry_resume').split()
    return settings, dict.fromkeys(names, True)


def capture(x=X, ehash=None, attempted='3' * 64):
    ehash = ehash or digest(canonical(expectation()))
    mem = native_memory(x, ehash)
    regs = dict(rip=0x581feb, rax=0x69bff0, r12=C, rdi=M, rsi=VECTOR, rdx=6, rcx=KW, rsp=0x30008)
    caller = Stop(10, 401, 401, 'retained-pidfd-creation-identity', regs, mem.reads(),
                  (B, C, M), 'qualified-hardware-caller', 20)
    receiver = replace(caller, index=11, registers={**regs, 'rip': 0x69bff0, 'rsp': 0x30000},
                       reason='qualified-in-place-call-receiver', token=21)
    d = Derivation(x, 'retained-A-capability-chain', 7, 0x4f6102,
        (0x4f6102, 0x4f6224, 0x4f6274, 0x4f6299), 17, 7, 3, 0, 2, b'#\n',
        0x99000, B, B, B, 0x88800, 0x88800, 1, 1, 15, 15, 2, 2, True)
    roles = ('controller launcher_gdb launcher_cpython bootstrap mi_parser decoder hash_tool guard '
             'qualification q1 provenance').split()
    artifacts = {r: ('synthetic-metadata:' + r).encode('ascii') for r in roles}
    settings, facts = q1()
    completion = dict.fromkeys(('stopped_at_entry capture_synced final_associations kill_requested '
        'pidfd_death_confirmed debugger_exit_confirmed transcript_drained no_resume '
        'guard_coverage_complete').split(), True)
    return Capture(x, ehash, attempted, attempted, caller, receiver, 21, d, d.a_identity,
        b'#\n', b'#\n', B, C, M, 1, 1, False, completion, copy.deepcopy(ENGINE),
        {r: digest(v) for r, v in artifacts.items()}, artifacts, settings, facts)


def witness(x, e, tried):
    # These are synthetic stage facts, with no verdict field or consumer result.
    stages = [
        ('protected', dict(initial=True, valid=True, association=True, seals_exact=True, length=2, sha256=DIGEST)),
        ('derived', dict(exact_bytes=True, from_A=True, retained=True, length=2, sha256=DIGEST)),
        ('engine', dict(images_match=True, live_association=True, build_match=True, interface_sha256=e['engine']['interface_sha256'])),
        ('callable', dict(object_match=True, native_target_match=True, binding_match=True)),
        ('observer', dict(artifact_match=True, attachment_match=True, qualified=True, sentinel_active=True, armed=True)),
        ('dispatch', dict(attempted_event_sha256=tried, persisted=True)),
        ('entry', dict(native_entry=True, engine_match=True, callable_match=True, after_dispatch=True,
            armed=True, exact_bytes=True, same_B=True, same_A=True, independent_A_equal=True,
            vector_valid=True, parameters_match=True, length=2, sha256=DIGEST,
            positional_count=6, keyword_count=1, keyword_names=['_feature_version'], parameters=copy.deepcopy(PARAMETERS))),
        ('protected', dict(initial=False, valid=True, association=True, seals_exact=True, length=2, sha256=DIGEST)),
        ('completion', dict(linked_to_entry=True, outcome='observer_stop')),
        ('end', dict(entry_count=1, observer_entry_count=1, same_A=True, seals_exact=True,
            no_reopen=True, observer_complete=True, execution_coverage=True, execution_attempted=False))]
    return dict(schema=SCHEMA + 'witness.v1', attempt_id=x, expectation_sha256=digest(canonical(e)),
        qualification_sha256=e['qualification_sha256'], observer_sha256=e['observer_sha256'],
        observations=[dict(index=i, kind=k, data=d) for i, (k, d) in enumerate(stages)], violations=[])


class OfflineReceiptTests(unittest.TestCase):
    def setUp(self):
        self.e = expectation()
        self.cap = capture()

    def verdict(self, cap):
        return evaluate_capture(cap, X, digest(canonical(self.e)), '3' * 64)

    def test_positive_decoded_receipt(self):
        self.assertEqual(self.verdict(self.cap), ('ACCEPT', []))

    def test_positive_witness(self):
        self.assertEqual(witness_codes(witness(X, self.e, '3' * 64), X, self.e, '3' * 64), [])

    def test_expected_fixture_without_capture_never_satisfies_receipt(self):
        self.assertIn('OBSERVATION_MISSING', byte_codes(None, 2, DIGEST, B, B, b'#\n', b'#\n', b'#\n', X, X))

    def test_wrong_compile_target(self):
        c = replace(self.cap.caller, registers={**self.cap.caller.registers, 'rax': 0x69bff1})
        self.assertIn('WRONG_COMPILE_CALLABLE', self.verdict(replace(self.cap, caller=c))[1])

    def test_wrong_receiver_pc(self):
        c = replace(self.cap.receiver, registers={**self.cap.receiver.registers, 'rip': 0x69bff1})
        self.assertIn('ENGINE_UNQUALIFIED', self.verdict(replace(self.cap, receiver=c))[1])

    def test_wrong_source_identity(self):
        self.assertIn('OBJECT_SUBSTITUTION', self.verdict(replace(self.cap, b=B + 8))[1])

    def test_actual_wrong_source_type(self):
        mem = native_memory()
        mem.word(B, 8, TYPES['str'])
        cap = replace(self.cap, caller=replace(self.cap.caller, reads=mem.reads()),
                      receiver=replace(self.cap.receiver, reads=mem.reads()))
        self.assertEqual(self.verdict(cap)[1][0], 'INPUT_TYPE')

    def test_actual_wrong_positional_count(self):
        cap = replace(self.cap,
            caller=replace(self.cap.caller, registers={**self.cap.caller.registers, 'rdx': 5}),
            receiver=replace(self.cap.receiver, registers={**self.cap.receiver.registers, 'rdx': 5}))
        self.assertEqual(self.verdict(cap)[1][0], 'WRONG_ENTRYPOINT')

    def test_actual_wrong_keyword(self):
        mem = native_memory()
        mem.string(0x1a000, '_wrong_feature_version')
        cap = replace(self.cap, caller=replace(self.cap.caller, reads=mem.reads()),
                      receiver=replace(self.cap.receiver, reads=mem.reads()))
        self.assertEqual(self.verdict(cap)[1][0], 'WRONG_ENTRYPOINT')

    def test_missing_caller(self):
        self.assertIn('OBSERVATION_MISSING', self.verdict(replace(self.cap, caller=None))[1])

    def test_missing_receiver(self):
        self.assertIn('OBSERVATION_MISSING', self.verdict(replace(self.cap, receiver=None))[1])

    def test_reverse_stops(self):
        self.assertIn('OBSERVATION_MISSING', self.verdict(replace(self.cap, receiver=replace(self.cap.receiver, index=9)))[1])

    def test_duplicate_receiver(self):
        self.assertIn('INVOCATION_COUNT', self.verdict(replace(self.cap, entry_count=2, observer_entry_count=2))[1])

    def test_wrong_pid(self):
        self.assertIn('OBSERVATION_MISSING', self.verdict(replace(self.cap, receiver=replace(self.cap.receiver, pid=402)))[1])

    def test_wrong_tid(self):
        self.assertIn('OBSERVATION_MISSING', self.verdict(replace(self.cap, receiver=replace(self.cap.receiver, tid=402)))[1])

    def test_wrong_attempt(self):
        self.assertEqual(self.verdict(replace(self.cap, attempt=NS + ':2')), ('REFUSE', ['RECORD_INVALID']))

    def test_wrong_attempted_link(self):
        self.assertIn('OBSERVATION_MISSING', self.verdict(replace(self.cap, attempted_sha256='9' * 64))[1])

    def test_wrong_release_link(self):
        self.assertIn('OBSERVATION_MISSING', self.verdict(replace(self.cap, released_attempted_sha256='9' * 64))[1])

    def test_observer_interruption(self):
        self.assertEqual(self.verdict(replace(self.cap, interruption=True)), ('ABORT', ['ATTEMPT_INCOMPLETE']))

    def test_unconfirmed_death(self):
        self.assertEqual(self.verdict(replace(self.cap, completion={**self.cap.completion, 'pidfd_death_confirmed': False}))[0], 'ABORT')

    def test_partial_memory(self):
        reads = tuple(replace(r, data=r.data[:-1]) if r.address == B else r for r in self.cap.receiver.reads)
        self.assertIn('OBSERVATION_MISSING', self.verdict(replace(self.cap, receiver=replace(self.cap.receiver, reads=reads)))[1])

    def test_stack_return(self):
        reads = tuple(replace(r, data=(0x581fee).to_bytes(8, 'little')) if r.address == 0x30000 else r for r in self.cap.receiver.reads)
        self.assertIn('OBSERVATION_MISSING', self.verdict(replace(self.cap, receiver=replace(self.cap.receiver, reads=reads)))[1])

    def test_derivation_resize_move_allowed(self):
        self.assertNotEqual(self.cap.derivation.original_buffer, self.cap.derivation.return_b)
        self.assertEqual(derivation_codes(self.cap.derivation, X, self.cap.a_identity), [])

    def test_derivation_missing_resize(self):
        self.assertEqual(derivation_codes(replace(self.cap.derivation, post_resize_b=0), X, self.cap.a_identity), ['OBJECT_SUBSTITUTION'])

    def test_derivation_short_io(self):
        self.assertEqual(derivation_codes(replace(self.cap.derivation, result=1), X, self.cap.a_identity), ['INPUT_IO'])

    def test_derivation_retry(self):
        self.assertEqual(derivation_codes(replace(self.cap.derivation, syscall_entries=2), X, self.cap.a_identity), ['INPUT_IO'])

    def test_derivation_wrong_a(self):
        self.assertEqual(derivation_codes(self.cap.derivation, X, 'other'), ['WRONG_PROTECTED_OBJECT'])

    def test_independent_a_equality(self):
        self.assertIn('OBSERVATION_MISSING', self.verdict(replace(self.cap, a_capture=b' \n'))[1])

    def test_positive_q1(self):
        self.assertEqual(validate_q1(*q1()), [])
        self.assertEqual(initialization_plan()[:4], ('/usr/bin/gdb', '--nx', '--nh', '--interpreter=mi2'))
        self.assertEqual(len(Q1), 26)

    def test_q1_permission_change(self):
        s, f = q1()
        s['show may-write-memory'] = 'set may-write-memory on'
        self.assertEqual(validate_q1(s, f), ['OBSERVER_UNQUALIFIED'])

    def test_q1_software_fallback(self):
        s, f = q1()
        f['no_software_fallback'] = False
        self.assertEqual(validate_q1(s, f), ['OBSERVER_NOT_ARMED'])

    def test_q1_mi_view_not_unmasked_proof(self):
        s, f = q1()
        f['raw_unmasked_text_equal'] = False
        self.assertEqual(validate_q1(s, f), ['OBSERVER_NOT_ARMED'])

    def test_engine_admission(self):
        self.assertEqual(engine_admission(self.cap.engine, self.cap.pins, self.cap.artifacts), [])

    def test_engine_artifact_hash(self):
        pins = {**self.cap.pins, 'bootstrap': '4' * 64}
        self.assertEqual(engine_admission(self.cap.engine, pins, self.cap.artifacts), ['ENGINE_UNQUALIFIED'])

    def test_engine_missing_role(self):
        pins = dict(self.cap.pins)
        del pins['guard']
        self.assertEqual(engine_admission(self.cap.engine, pins, self.cap.artifacts), ['ENGINE_UNQUALIFIED'])

    def test_deterministic_canonical(self):
        w = witness(X, self.e, '3' * 64)
        self.assertEqual(canonical(w), canonical(dict(reversed(list(w.items())))))
        self.assertEqual(parse(canonical(w)), w)
        self.assertEqual(digest(b'#\n'), DIGEST)

    def test_refusal_precedence(self):
        self.assertEqual(ranked(['OBJECT_SUBSTITUTION', 'PATHNAME_REOPEN', 'OBJECT_SUBSTITUTION']), ['PATHNAME_REOPEN', 'OBJECT_SUBSTITUTION'])

    def test_recovery_only_code(self):
        with self.assertRaises(Invalid):
            ranked(['ATTEMPT_INCOMPLETE'])

    def test_witness_unknown_field(self):
        w = witness(X, self.e, '3' * 64)
        w['result'] = 'ACCEPT'
        self.assertEqual(witness_codes(w, X, self.e, '3' * 64), ['RECORD_INVALID'])

    def test_witness_execution_precedence(self):
        w = witness(X, self.e, '3' * 64)
        w['violations'] = ['PATHNAME_REOPEN', 'EXECUTION_PROHIBITED']
        self.assertEqual(witness_codes(w, X, self.e, '3' * 64), ['PATHNAME_REOPEN', 'EXECUTION_PROHIBITED'])

    def test_witness_parameters_exact_types(self):
        w = witness(X, self.e, '3' * 64)
        w['observations'][6]['data']['parameters']['flags'] = False
        self.assertEqual(witness_codes(w, X, self.e, '3' * 64), ['RECORD_INVALID'])

    def test_witness_unknown_count_not_zero(self):
        w = witness(X, self.e, '3' * 64)
        w['observations'][-1]['data']['entry_count'] = None
        self.assertEqual(witness_codes(w, X, self.e, '3' * 64), ['RECORD_INVALID'])


def _engine_mutation(key):
    def test(self):
        e = copy.deepcopy(self.cap.engine)
        v = e[key]
        e[key] = v + 1 if type(v) is int else {} if type(v) is dict else [] if type(v) is list else '<wrong>'
        self.assertEqual(engine_admission(e, self.cap.pins, self.cap.artifacts), ['ENGINE_UNQUALIFIED'])
    return test


for _key in ENGINE:
    setattr(OfflineReceiptTests, 'test_engine_mismatch_' + _key, _engine_mutation(_key))


def _byte_mutation(raw, code):
    def test(self):
        faults = byte_codes(raw, len(raw), digest(raw), B, B, raw, raw, raw, X, X)
        self.assertEqual(faults, [code])
    return test


for _name, _raw, _code in (('truncated', b'#', 'INPUT_TRUNCATED'),
        ('appended', b'#\n\n', 'INPUT_APPENDED'), ('altered', b' \n', 'INPUT_ALTERED')):
    setattr(OfflineReceiptTests, 'test_bytes_' + _name, _byte_mutation(_raw, _code))


def _actual_argument_mutation(index, value):
    def test(self):
        mem = native_memory()
        if index in (1, 2):
            mem.string(0x18000 if index == 1 else 0x19000, value)
        elif index == 4:
            mem.word(TRUE, 16, 1)
        else:
            p = 0x21000
            mem.integer(p, value)
            mem.word(VECTOR, index * 8, p)
        cap = replace(self.cap, caller=replace(self.cap.caller, reads=mem.reads()),
                      receiver=replace(self.cap.receiver, reads=mem.reads()))
        self.assertEqual(self.verdict(cap)[0], 'REFUSE')
        self.assertEqual(self.verdict(cap)[1][0], 'WRONG_ENTRYPOINT')
    return test


for _i, _value in ((1, '<wrong>'), (2, 'eval'), (3, 1), (4, False), (5, -1), (6, 0)):
    setattr(OfflineReceiptTests, 'test_actual_wrong_argument_' + str(_i), _actual_argument_mutation(_i, _value))


def _q1_missing_fact(name):
    def test(self):
        s, f = q1()
        f[name] = False
        self.assertEqual(validate_q1(s, f), ['OBSERVER_NOT_ARMED'])
    return test


for _fact in q1()[1]:
    setattr(OfflineReceiptTests, 'test_q1_failed_' + _fact, _q1_missing_fact(_fact))


class ABITests(unittest.TestCase):
    def test_full_argument_vector_and_roots(self):
        mem = native_memory()
        d = Decoder(Snapshot(mem.reads()))
        self.assertEqual(d.roots(M, X, digest(canonical(expectation()))), (B, C, M))
        v, p, b = d.arguments(capture().receiver.registers, B)
        self.assertEqual(len(v), 7)
        self.assertEqual(p, PARAMETERS)
        self.assertEqual(b, b'#\n')

    def test_unicode_layouts(self):
        for kind, text, compact in ((1, 'é', True), (2, 'Ω', True), (4, '😀', True), (2, 'Ω', False)):
            mem = Memory()
            mem.string(0x40000, text, kind, compact, False)
            self.assertEqual(Decoder(Snapshot(mem.reads())).unicode(0x40000), text)

    def test_long_normalization(self):
        for n in (0, -1, 1, 2**62 + 123):
            mem = Memory()
            mem.integer(0x40000, n)
            self.assertEqual(Decoder(Snapshot(mem.reads())).long(0x40000), n)

    def test_bool_not_exact_int(self):
        d = Decoder(Snapshot(native_memory().reads()))
        with self.assertRaises(Invalid):
            d.long(TRUE)
        self.assertIs(d.boolean(TRUE), True)

    def test_read_missing_range(self):
        with self.assertRaises(Invalid):
            Snapshot([]).read(1, 2)

    def test_overflow(self):
        with self.assertRaises(Invalid):
            Snapshot.range(2**64 - 1, 2)

    def test_negative_length(self):
        mem = native_memory()
        mem.word(B, 16, -1, signed=True)
        with self.assertRaises(Invalid):
            Decoder(Snapshot(mem.reads())).bytes(B)

    def test_wrong_type(self):
        mem = native_memory()
        mem.word(B, 8, TYPES['str'])
        with self.assertRaises(Invalid):
            Decoder(Snapshot(mem.reads())).bytes(B)

    def test_missing_payload_not_padded(self):
        mem = native_memory()
        mem.ranges[B] = mem.ranges[B][:33]
        with self.assertRaises(Invalid):
            Decoder(Snapshot(mem.reads())).bytes(B)

    def test_bytes_terminator(self):
        mem = native_memory()
        mem.ranges[B][34] = 1
        with self.assertRaises(Invalid):
            Decoder(Snapshot(mem.reads())).bytes(B)

    def test_tuple_oversize(self):
        mem = native_memory()
        mem.word(ROOT, 16, 5)
        with self.assertRaises(Invalid):
            Decoder(Snapshot(mem.reads())).tuple(ROOT)

    def test_unicode_oversize(self):
        mem = native_memory()
        mem.word(0x18000, 16, 4097)
        with self.assertRaises(Invalid):
            Decoder(Snapshot(mem.reads())).unicode(0x18000)

    def test_unicode_surrogate(self):
        mem = Memory()
        mem.string(0x40000, '\ud800', 2, True, False)
        with self.assertRaises(Invalid):
            Decoder(Snapshot(mem.reads())).unicode(0x40000)

    def test_long_invalid_sign(self):
        mem = native_memory()
        mem.word(0x20000, 16, 11)
        with self.assertRaises(Invalid):
            Decoder(Snapshot(mem.reads())).long(0x20000)

    def test_long_invalid_digit(self):
        mem = native_memory()
        mem.word(0x20000, 24, 2**30, 4)
        with self.assertRaises(Invalid):
            Decoder(Snapshot(mem.reads())).long(0x20000)

    def test_dict_duplicate_index(self):
        mem = native_memory()
        mem.ranges[DK][33] = 0
        with self.assertRaises(Invalid):
            Decoder(Snapshot(mem.reads())).dictionary(DICT)

    def test_dict_wrong_used(self):
        mem = native_memory()
        mem.word(DICT, 16, 1)
        with self.assertRaises(Invalid):
            Decoder(Snapshot(mem.reads())).dictionary(DICT)

    def test_split_dictionary(self):
        mem = native_memory()
        mem.word(DICT, 40, 0x22000)
        mem.word(DK, 10, 2, 1)
        mem.ranges[0x22000] = bytearray(C.to_bytes(8, 'little') + ROOT.to_bytes(8, 'little'))
        self.assertEqual(Decoder(Snapshot(mem.reads())).dictionary(DICT)[0]['compile'], C)

    def test_general_dictionary(self):
        mem = native_memory()
        mem.word(DK, 10, 0, 1)
        mem.ranges[DK] = mem.ranges[DK][:40] + bytearray(48)
        for offset, value in ((48, 0x1b000), (56, C), (72, 0x1c000), (80, ROOT)):
            mem.word(DK, offset, value)
        self.assertEqual(Decoder(Snapshot(mem.reads())).dictionary(DICT)[0]['compile'], C)


class MITests(unittest.TestCase):
    def test_tokened_result_and_async(self):
        p = MIParser()
        p.command(mi_command(1, '-break-list'))
        self.assertEqual(p.feed(b'*stopped,reason="breakpoint-hit",frame={addr="0x69bff0"}\n').kind, '*stopped')
        self.assertEqual(p.feed(b'1^done,bkpt={number="1",type="hw breakpoint"}\n').fields['bkpt']['type'], b'hw breakpoint')
        self.assertIsNone(p.pending)

    def test_stream_c_escape(self):
        self.assertEqual(MIParser().feed(b'~"line\\n\\101"\n').fields, b'line\nA')

    def test_array_grammar(self):
        p = MIParser()
        p.command(mi_command(1, '-data-list-register-values x'))
        self.assertEqual(len(p.feed(b'1^done,register-values=[{number="0",value="0x1"}]\n').fields['register-values']), 1)

    def test_error_preserved_and_fail_closed(self):
        p = MIParser()
        p.command(mi_command(1, '-break-list'))
        with self.assertRaises(Invalid):
            p.feed(b'1^error,msg="failure"\n')
        self.assertEqual(p.records[-1].kind, '^error')

    def test_result_wrong_token(self):
        p = MIParser()
        p.command(mi_command(1, '-break-list'))
        with self.assertRaises(Invalid):
            p.feed(b'2^done\n')

    def test_two_outstanding_denied(self):
        p = MIParser()
        p.command(mi_command(1, '-break-list'))
        with self.assertRaises(Invalid):
            p.command(mi_command(2, '-break-list'))

    def test_duplicate_field(self):
        with self.assertRaises(Invalid):
            MIParser().feed(b'*stopped,reason="a",reason="b"\n')

    def test_inferior_cannot_inject(self):
        with self.assertRaises(Invalid):
            MIParser().feed(b'1^done\n', 'inferior')

    def test_transcript_overflow(self):
        with self.assertRaises(Invalid):
            MIParser(2).feed(b'(gdb)\n')


def _denied_command(command):
    def test(self):
        with self.assertRaises(Invalid):
            mi_command(1, command)
    return test


for _i, _command in enumerate(('-break-insert *0x69bff0', '-break-insert -h *0x69bff1',
        '-break-insert -h -f *0x69bff0', '-exec-next-instruction', '-exec-finish',
        '-data-evaluate-expression "compile"', '-data-write-memory-bytes 0x10000 00',
        '-target-detach', '-interpreter-exec console "set may-write-memory on"')):
    setattr(MITests, 'test_denied_command_' + str(_i), _denied_command(_command))


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.tmp.name) / 'store', NS, create=True)
        from real_receipt_fixtures import preparation, freeze
        self.e, self.prep = preparation(X)
        freeze(self.store, self.e, self.prep)
        self.a = self.store.reserve(self.e, request(self.e))

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def observation(self, tried):
        from real_receipt_fixtures import observation
        return observation(self.prep, X, self.e, tried)

    def finish_positive(self):
        self.a.prepare(self.prep)
        tried = self.a.attempted()
        self.a.finish(witness(X, self.e, tried), self.observation(tried))

    def test_positive_durable_chain(self):
        self.finish_positive()
        self.assertEqual([e['state'] for e in self.a.events()], ['PREPARED', 'ATTEMPTED', 'ACCEPTED'])
        before = self.a.raw('events.jsonl')
        self.assertEqual(self.a.recover()['state'], 'ACCEPTED')
        self.assertEqual(self.a.raw('events.jsonl'), before)

    def test_witness_alone_no_accept(self):
        self.a.prepare(self.prep)
        tried = self.a.attempted()
        with self.assertRaises(Invalid):
            self.a.finish(witness(X, self.e, tried), None)

    def test_terminal_no_resume(self):
        self.finish_positive()
        with self.assertRaises(Invalid):
            self.a.attempted()

    def test_aborted_terminality_and_idempotence(self):
        self.a.prepare(self.prep)
        self.a.attempted()
        v = self.a.recover()
        self.assertEqual(v['state'], 'ABORTED')
        self.assertEqual(v, self.a.recover())
        with self.assertRaises(Invalid):
            self.a.prepare(self.prep)

    def test_observer_loss_aborts(self):
        self.a.prepare(self.prep)
        tried = self.a.attempted()
        self.assertEqual(self.a.finish(witness(X, self.e, tried), replace(self.observation(tried), interrupted=True))['state'], 'ABORTED')

    def test_torn_tail_retained(self):
        self.a.prepare(self.prep)
        raw = self.a.raw('events.jsonl') + b'{"schema"'
        (self.a.path / 'events.jsonl').write_bytes(raw)
        r = self.a.recover()
        self.assertEqual(r['primary_code'], 'ATTEMPT_INCOMPLETE')
        self.assertEqual(self.a.raw('events.jsonl'), raw)
        self.assertLess(r['valid_prefix_length'], r['journal_length'])

    def test_complete_invalid_record(self):
        (self.a.path / 'events.jsonl').write_bytes(b'{}\n')
        self.assertEqual(self.a.recover()['primary_code'], 'RECORD_INVALID')

    def test_cross_attempt_registration(self):
        v = parse(self.a.raw('registration.json'))
        v['attempt_id'] = NS + ':2'
        (self.a.path / 'registration.json').write_bytes(canonical(v))
        self.assertEqual(self.a.recover()['primary_code'], 'RECORD_INVALID')

    def test_recovery_conflict_preserves(self):
        self.a.recover()
        before = self.a.raw('recovery.json')
        (self.a.path / 'events.jsonl').write_bytes(b'bad\n')
        with self.assertRaises(Invalid):
            self.a.recover()
        self.assertEqual(self.a.raw('recovery.json'), before)

    def test_partial_recovery_preserves(self):
        (self.a.path / 'recovery.json').write_bytes(b'{')
        with self.assertRaises(Invalid):
            self.a.recover()
        self.assertEqual(self.a.raw('recovery.json'), b'{')

    def test_stale_writer(self):
        self.store.close()
        with self.assertRaises(Invalid):
            self.a.prepare(self.prep)

    def test_missing_custody_never_recreated(self):
        (self.store.root / 'custody').unlink()
        with self.assertRaises(Invalid):
            self.a.prepare(self.prep)
        self.assertFalse((self.store.root / 'custody').exists())

    def test_exclusive_store(self):
        with self.assertRaises(Invalid):
            Store(self.store.root)

    def test_monotonic_reservation_after_abort(self):
        self.a.recover()
        b = self.store.reserve(self.e, request(self.e))
        self.assertEqual(b.x, NS + ':2')

    def test_missing_reservation_cannot_reuse_id(self):
        (self.store.root / 'reservations' / '1').unlink()
        with self.assertRaises(Invalid):
            self.store.reserve(self.e, request(self.e))

    def test_custody_replacement(self):
        (self.store.root / 'custody').write_bytes(canonical({'namespace': 'b' * 64, 'kind': 'exclusive-controller'}))
        with self.assertRaises(Invalid):
            self.a.prepare(self.prep)

    def test_fsync_failure_no_attempted_release(self):
        self.a.prepare(self.prep)
        with patch('e0.h2.real_receipt_evidence.os.fsync', side_effect=OSError('synthetic fsync failure')):
            with self.assertRaises(OSError):
                self.a.attempted()
        # No dispatch capability exists. Interrupted write is retained as-is.
        self.assertIsNotNone(self.a.raw('events.jsonl'))
        with self.assertRaises(Invalid):
            self.a.attempted()

    def test_incomplete_package_never_public_accept(self):
        self.finish_positive()
        files = {'1/events.jsonl': self.a.raw('events.jsonl')}
        raw = canonical(manifest('package', X, digest(canonical(self.e)), files))
        self.assertFalse(public_accept(self.a, raw, (digest(raw) + '\n').encode(), files, {'1/witness.json'}))
        self.assertEqual(self.a.recover()['state'], 'ACCEPTED')


class SerializationTests(unittest.TestCase):
    def test_noncanonical_rejected(self):
        for raw in (b'{"a": 1}\n', b'{"a":1,"a":1}\n', b'{}', b'\xef\xbb\xbf{}\n', b'{"a":1.0}\n'):
            with self.assertRaises(Invalid):
                parse(raw)

    def test_control_string_rejected(self):
        with self.assertRaises(Invalid):
            canonical({'a': '\n'})

    def test_manifest_determinism(self):
        files = {'qualification/q1': b'policy', '1/observer/B.entry.bin': b'#\n'}
        raw = canonical(manifest('capture', X, 'b' * 64, files))
        self.assertTrue(verify_manifest(raw, dict(reversed(list(files.items()))), 'capture', X, 'b' * 64))
        self.assertFalse(verify_manifest(raw, {**files, '1/observer/B.entry.bin': b'bad'}, 'capture', X, 'b' * 64))

    def test_manifest_self_reference_and_traversal(self):
        for path in ('../bad', '/bad', '1/package-manifest.json', 'a//b', '1/capture-manifest.json'):
            with self.assertRaises(Invalid):
                manifest('capture', X, 'b' * 64, {path: b'bad'})


if __name__ == '__main__':
    unittest.main()
