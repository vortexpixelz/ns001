"""Faithful RR1-RR4 retained-history regressions; synthetic evidence only."""
from dataclasses import replace
import re
import unittest
import test_e0_h2_real_receipt_correction as prior
from e0.h2.real_receipt_integration import Chunk, Transcript
from e0.h2.real_receipt_policy import Invalid, mi_command


def before_step(o, command=None, notification=None):
    start = next(i for i, c in enumerate(o.transcript)
                 if c.channel == 'commands' and b'-exec-step-instruction' in c.raw)
    if notification is not None:
        return replace(o, transcript=o.transcript[:start] + (Chunk('stdout', notification),) + o.transcript[start:])
    token = int(o.transcript[start].raw.split(b'-', 1)[0])
    extra = (Chunk('commands', mi_command(token, command)), Chunk('stdout', f'{token}^done\n'.encode()))
    tail = tuple(replace(c, raw=re.sub(rb'^([0-9]+)([-^])',
        lambda m: str(int(m[1])+1).encode()+m[2], c.raw)) for c in o.transcript[start:])
    natives = (o.native_stops[0], {**o.native_stops[1], 'token': o.native_stops[1]['token']+1})
    return replace(o, transcript=o.transcript[:start]+extra+tail, native_stops=natives)


class RereviewCorrectionTests(unittest.TestCase):
    setUp = prior.CorrectionTests.setUp
    tearDown = prior.CorrectionTests.tearDown
    begin = prior.CorrectionTests.begin
    public = prior.CorrectionTests.public
    precondition = prior.CorrectionTests.precondition
    complete = prior.CorrectionTests.complete
    negative = prior.CorrectionTests.negative

    def extra_ready(self, address, number=3):
        extra = (Chunk('commands', mi_command(5000, f'-break-insert -h *0x{address:x}')),
            Chunk('stdout', f'5000^done,bkpt={{number="{number}",type="hw breakpoint",enabled="y",addr="0x{address:x}"}}\n'.encode()))
        self.precondition(replace(self.p, transcript=self.p.transcript+extra))

    def test_RR1_exact_receiver_delete_after_caller(self):
        self.negative(lambda o: before_step(o, '-break-delete 1'))

    def test_RR1_caller_retirement_after_caller(self):
        self.negative(lambda o: before_step(o, '-break-delete 2'))

    def test_RR1_unknown_retirement(self):
        self.negative(lambda o: before_step(o, '-break-delete 99'))

    def test_RR1_exact_extra_wrapper_at_READY(self):
        self.extra_ready(0x4f6102)

    def test_RR1_other_derivation_site_at_READY(self):
        self.extra_ready(0x4f6274)

    def test_RR1_duplicate_receiver_identity(self):
        self.extra_ready(0x69bff0, 1)

    def test_RR1_wrong_initial_derivation_phase(self):
        chunks = self.p.transcript
        index = next(i for i,c in enumerate(chunks) if c.channel == 'commands' and b'-exec-' in c.raw)
        token = int(chunks[index].raw.split(b'-',1)[0])
        extra = (Chunk('commands', mi_command(token, '-break-insert -h *0x4f6274')),
                 Chunk('stdout', f'{token}^done,bkpt={{number="99",type="hw breakpoint",enabled="y",addr="0x4f6274"}}\n'.encode()))
        # Shift all later tokens and their independent native links faithfully.
        tail = tuple(replace(c, raw=re.sub(rb'^([0-9]+)([-^])',
            lambda m:str(int(m[1])+1).encode()+m[2],c.raw)) for c in chunks[index:])
        natives = tuple({**n,'token':n['token']+1} for n in self.p.native_derivation)
        self.precondition(replace(self.p, transcript=chunks[:index]+extra+tail,native_derivation=natives))

    def test_RR2_exact_thread_exit_before_receiver(self):
        self.negative(lambda o: before_step(o, notification=b'=thread-exited,id="401",group-id="i1"\n'))

    def test_RR2_process_exit_before_receiver(self):
        self.negative(lambda o: before_step(o, notification=b'=thread-group-exited,id="i1",exit-code="0"\n'))

    def test_RR2_stale_identity_recreation(self):
        self.negative(lambda o: before_step(o, notification=b'=thread-exited,id="401",group-id="i1"\n=thread-created,id="401",group-id="i1"\n'))

    def test_RR2_unowned_exit(self):
        self.negative(lambda o: before_step(o, notification=b'=thread-exited,id="999",group-id="i1"\n'))

    def test_RR2_terminal_death_after_complete_capture(self):
        terminal = self.complete(lambda o: replace(o, transcript=o.transcript +
            (Chunk('stdout', b'=thread-exited,id="401",group-id="i1"\n=thread-group-exited,id="i1",exit-code="0"\n'),)))
        self.assertEqual(terminal['state'], 'ACCEPTED')
        self.assertTrue(self.public())

    def test_RR3_exact_non_site_contradiction(self):
        self.negative(mutate_memory=lambda m:m.ranges.__setitem__(0x500000,bytearray(b'\xcc')))

    def test_RR3_other_address_contradiction(self):
        self.negative(mutate_memory=lambda m:m.ranges.__setitem__(0x500010,bytearray(b'\xcc\x00')))

    def test_RR3_matching_non_site_read(self):
        terminal = self.complete(mutate_memory=lambda m:m.ranges.__setitem__(0x500010,bytearray(b'\x00\x00')))
        self.assertEqual(terminal['state'], 'ACCEPTED')
        self.assertTrue(self.public())

    def test_RR3_outside_text_is_not_compiler_evidence(self):
        terminal = self.complete(mutate_memory=lambda m:m.ranges.__setitem__(0x710000,bytearray(b'\xcc')))
        self.assertEqual(terminal['state'], 'ACCEPTED')
        self.assertTrue(self.public())

    def test_RR3_overlapping_contradiction(self):
        self.negative(mutate_memory=lambda m:m.ranges.__setitem__(0x581fec,bytearray(b'\xcc')))

    def test_RR3_overflow_rejected(self):
        with self.assertRaises(Invalid):
            mi_command(1, '-data-read-memory-bytes 0xffffffffffffffff 2')

    def test_RR4_exact_seals_fault_before_malformed_MI(self):
        terminal = self.negative(lambda o:replace(o, protected_final={**o.protected_final,'seals':0},
            transcript=o.transcript+(Chunk('stdout',b'not valid MI\n'),)))
        self.assertEqual(terminal['state'], 'ABORTED')
        self.assertEqual(terminal['primary_code'], 'ATTEMPT_INCOMPLETE')
        self.assertIn('OBJECT_SUBSTITUTION',terminal['diagnostics'])

    def test_RR4_execution_fault_before_incomplete_MI(self):
        terminal = self.negative(lambda o:replace(o,guard_operations=('execution',),
            transcript=o.transcript+(Chunk('stdout',b'not valid MI\n'),)))
        self.assertIn('EXECUTION_PROHIBITED',terminal['diagnostics'])

    def test_RR4_both_supported_faults_before_interruption(self):
        terminal = self.negative(lambda o:replace(o,guard_operations=('execution',),
            protected_final={**o.protected_final,'seals':0}, interrupted=True))
        self.assertIn('EXECUTION_PROHIBITED',terminal['diagnostics'])
        self.assertIn('OBJECT_SUBSTITUTION',terminal['diagnostics'])

    def test_RR4_no_fabricated_diagnostic(self):
        terminal = self.negative(lambda o:replace(o,transcript=o.transcript+(Chunk('stdout',b'not valid MI\n'),)))
        self.assertEqual(terminal['diagnostics'],[])

    def test_RR1_complete_temporary_sequence_positive(self):
        self.assertEqual(self.complete()['state'], 'ACCEPTED')
        self.assertTrue(self.public())

    def test_RR1_missing_temporary_retirement(self):
        chunks = self.p.transcript
        index = next(i for i,c in enumerate(chunks) if c.channel == 'commands' and b'-break-delete 3' in c.raw)
        self.precondition(replace(self.p,transcript=chunks[:index]+chunks[index+2:]))

    def test_RR1_missing_temporary_insertion(self):
        chunks = self.p.transcript
        index = next(i for i,c in enumerate(chunks) if c.channel == 'commands' and b'-break-insert -h *0x4f6102' in c.raw)
        self.precondition(replace(self.p,transcript=chunks[:index]+chunks[index+2:]))

    def test_RR4_map_fault_survives_malformed_MI(self):
        terminal = self.negative(lambda o:replace(o,maps=(b'wrong',b'wrong'),
            transcript=o.transcript+(Chunk('stdout',b'not valid MI\n'),)))
        self.assertIn('ENGINE_UNQUALIFIED',terminal['diagnostics'])

    def test_RR1_inventory_readback_extra_active_site(self):
        extra = (Chunk('commands',mi_command(5000,'-break-list')),
            Chunk('stdout',b'5000^done,BreakpointTable={body=[bkpt={number="1",type="hw breakpoint",enabled="y",addr="0x69bff0"},bkpt={number="2",type="hw breakpoint",enabled="y",addr="0x581feb"},bkpt={number="99",type="hw breakpoint",enabled="y",addr="0x4f6102"}]}\n'))
        self.precondition(replace(self.p,transcript=self.p.transcript+extra))

    def test_RR1_unassociated_hardware_result(self):
        extra = (Chunk('commands',mi_command(5000,'-interpreter-exec console "maintenance info breakpoints"')),
            Chunk('stdout',b'5000^done,bkpt={number="99",type="hw breakpoint",enabled="y",addr="0x4f6102"}\n'))
        self.precondition(replace(self.p,transcript=self.p.transcript+extra))
