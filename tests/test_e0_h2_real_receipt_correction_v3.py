"""Bounded receiver-thread scope regressions; synthetic evidence/local stores only."""
from dataclasses import replace
import unittest
import test_e0_h2_real_receipt_correction as prior
from test_e0_h2_real_receipt_correction_v2 import before_step
from real_receipt_fixtures import observation
from test_e0_h2_real_receipt import X
from e0.h2.real_receipt_integration import Chunk, text_maps
from e0.h2.real_receipt_policy import mi_command


def scoped(p, address, thread=None, groups=None):
    marker = f'addr="0x{address:x}"'.encode()
    suffix = (f',thread="{thread}"'.encode() if thread is not None else b'')
    suffix += (b',thread-groups=[' + b','.join(b'"'+g.encode()+b'"' for g in groups) + b']'
               if groups is not None else b'')
    chunks, changed = [], 0
    for c in p.transcript:
        if c.channel == 'stdout' and b'bkpt=' in c.raw and marker in c.raw:
            c = replace(c, raw=c.raw.replace(marker, marker+suffix))
            changed += 1
        chunks.append(c)
    assert changed == 1
    return replace(p, transcript=tuple(chunks))


def stop_threads(o, caller=None, receiver=None, native=False):
    chunks, index = [], 0
    natives = list(o.native_stops)
    for c in o.transcript:
        if c.channel == 'stdout' and b'*stopped,' in c.raw:
            thread = (caller, receiver)[index]
            if thread is not None:
                c = replace(c, raw=c.raw.replace(b'thread-id="401"', f'thread-id="{thread}"'.encode()))
                if native:
                    natives[index] = {**natives[index], 'tid':thread}
            index += 1
        chunks.append(c)
    assert index == 2
    return replace(o, transcript=tuple(chunks), native_stops=tuple(natives))


def retid_chunks(chunks, tid):
    return tuple(replace(c,raw=c.raw.replace(b'=thread-created,id="401"',f'=thread-created,id="{tid}"'.encode()).replace(
        b'thread-id="401"',f'thread-id="{tid}"'.encode()).replace(b'pid="401"',f'pid="{tid}"'.encode())) for c in chunks)


def retid_preparation(p, tid):
    admission = {**p.admission, 'task_ids':[tid],
                 'controls':[{**c,'tid':tid} for c in p.admission['controls']]}
    return replace(p,custody={**p.custody,'pid':tid,'tid':tid},admission=admission,ready=replace(p.ready,pid=tid,tid=tid),
        transcript=retid_chunks(p.transcript,tid),
        native_derivation=tuple({**n,'pid':tid,'tid':tid} for n in p.native_derivation),
        native_controls=tuple({**n,'pid':tid,'tid':tid} for n in p.native_controls),
        text_captures=tuple(replace(c,mapping={**c.mapping,'pid':tid,'tid':tid}) for c in p.text_captures))


def retid_observation(o, tid):
    captures = tuple(replace(c,mapping={**c.mapping,'pid':tid,'tid':tid}) for c in o.text_captures)
    return replace(o,transcript=retid_chunks(o.transcript,tid),
        native_stops=tuple({**n,'pid':tid,'tid':tid} for n in o.native_stops),text_captures=captures,
        maps=tuple(text_maps(captures,epoch) for epoch in ('caller','receiver')))


class ThreadScopeTests(unittest.TestCase):
    setUp = prior.CorrectionTests.setUp
    tearDown = prior.CorrectionTests.tearDown
    begin = prior.CorrectionTests.begin
    public = prior.CorrectionTests.public
    precondition = prior.CorrectionTests.precondition
    complete = prior.CorrectionTests.complete
    negative = prior.CorrectionTests.negative

    def test_exact_rereview_receiver_monitor_scope_999(self):
        self.precondition(scoped(self.p,0x69bff0,999))
        self.assertEqual(self.a.recover()['primary_code'],'OBSERVER_UNQUALIFIED')

    def test_caller_monitor_wrong_scope(self):
        self.precondition(scoped(self.p,0x581feb,999))

    def test_caller_stop_wrong_TID(self):
        self.negative(lambda o:stop_threads(o,caller=999))

    def test_receiver_stop_wrong_TID(self):
        self.negative(lambda o:stop_threads(o,receiver=999))

    def test_both_stops_match_each_other_but_not_admitted_TID(self):
        self.negative(lambda o:stop_threads(o,caller=999,receiver=999,native=True))

    def test_receiver_native_TID_cannot_replace_MI_mismatch(self):
        self.negative(lambda o:stop_threads(o,receiver=999,native=True))

    def test_other_created_live_thread_cannot_supply_receiver(self):
        self.negative(lambda o:before_step(stop_threads(o,receiver=999,native=True),
            notification=b'=thread-created,id="999",group-id="i1"\n'))

    def test_correct_unrestricted_baseline(self):
        self.assertEqual(self.complete()['state'],'ACCEPTED')
        self.assertTrue(self.public())

    def test_correct_explicit_selected_scope(self):
        self.p = scoped(scoped(self.p,0x69bff0,self.p.custody['tid']),0x581feb,self.p.custody['tid'])
        self.assertEqual(self.complete()['state'],'ACCEPTED')
        self.assertTrue(self.public())

    def test_wrong_process_group_scope(self):
        self.precondition(scoped(self.p,0x69bff0,groups=['i2']))

    def test_inventory_cannot_change_receiver_scope(self):
        extra=(Chunk('commands',mi_command(5000,'-break-list')),
            Chunk('stdout',b'5000^done,BreakpointTable={body=[bkpt={number="1",type="hw breakpoint",enabled="y",addr="0x69bff0",thread="999"},bkpt={number="2",type="hw breakpoint",enabled="y",addr="0x581feb"}]}\n'))
        self.precondition(replace(self.p,transcript=self.p.transcript+extra))

    def test_exit_before_receiver_fails_closed(self):
        self.negative(lambda o:before_step(o,notification=b'=thread-exited,id="401",group-id="i1"\n'))

    def test_terminal_death_after_capture_remains_permitted(self):
        terminal=self.complete(lambda o:replace(o,transcript=o.transcript+
            (Chunk('stdout',b'=thread-exited,id="401",group-id="i1"\n=thread-group-exited,id="i1",exit-code="0"\n'),)))
        self.assertEqual(terminal['state'],'ACCEPTED')
        self.assertTrue(self.public())

    def test_generic_selected_TID_707_positive(self):
        self.p=retid_preparation(self.p,707)
        self.p=scoped(self.p,0x69bff0,707)
        tried=self.begin()
        self.a.finish(None,retid_observation(observation(self.p,X,self.e,tried),707))
        self.assertEqual(self.a.recover()['state'],'ACCEPTED')
        self.assertTrue(self.public())

    def test_generic_selected_TID_707_rejects_old_401_scope(self):
        self.precondition(scoped(retid_preparation(self.p,707),0x69bff0,401))
