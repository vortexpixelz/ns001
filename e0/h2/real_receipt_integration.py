"""Offline integration of the frozen real-input contract. No target/launch API.

Inputs are retained or synthetic evidence. Parsing and validating them is not live
mechanism qualification, authenticated native provenance, or experiment permission.
"""
from dataclasses import dataclass, replace
import json
import re
from .real_receipt_policy import (Invalid, ENGINE, Q1, READBACKS, SCHEMA, PROFILE,
    PARAMETERS, DIGEST, canonical, parse, digest, keys, ranked, initialization_plan,
    engine_admission, parameters_match, hash_value)
from .real_receipt_observation import MIParser, Stop, Capture, evaluate_capture, derivation_codes
from .real_receipt_abi import Decoder, Snapshot, Read


@dataclass(frozen=True)
class Chunk:
    channel: str
    raw: bytes


class Transcript:
    """Chunked channels with byte offsets, strict token association and stop epochs."""
    def __init__(self, chunks):
        self.chunks = tuple(chunks)
        self.parser = MIParser()
        self.raw = dict.fromkeys(('commands', 'stdout', 'stderr'), b'')
        self.order, self.commands, self.results, self.stops = [], {}, {}, []
        self.streams, self.stop_data = {}, {}
        self.active_stop = None
        self.execution_token = None
        self.execution_running = False
        self.groups, self.threads = {}, {}
        buffers = {'stdout': b'', 'stderr': b''}
        for index, chunk in enumerate(self.chunks):
            if chunk.channel not in self.raw or type(chunk.raw) is not bytes or not chunk.raw:
                raise Invalid('channel/framing')
            if sum(map(len, self.raw.values())) + len(chunk.raw) > 8 * 1024 * 1024:
                raise Invalid('transcript budget')
            offset = len(self.raw[chunk.channel])
            self.raw[chunk.channel] += chunk.raw
            self.order.append(dict(index=index, channel=chunk.channel, offset=offset, length=len(chunk.raw)))
            if chunk.channel == 'commands':
                if buffers['stdout'] or buffers['stderr']:
                    raise Invalid('command amid incomplete output')
                self.parser.command(chunk.raw)
                token = self.parser.pending
                command = chunk.raw[len(str(token)):-1].decode('ascii')
                self.commands[token] = command
                self.streams[token] = b''
                if command in ('-exec-continue', '-exec-step-instruction', '-exec-run'):
                    if self.execution_token is not None:
                        raise Invalid('ambiguous execution command')
                    self.execution_token = token
                    self.execution_running = False
                    self.active_stop = None
                continue
            buffers[chunk.channel] += chunk.raw
            while b'\n' in buffers[chunk.channel]:
                line, buffers[chunk.channel] = buffers[chunk.channel].split(b'\n', 1)
                line += b'\n'
                pending = self.parser.pending
                rec = self.parser.feed(line, chunk.channel)
                if rec.kind in ('~', '&'):
                    if pending is not None:
                        self.streams[pending] += rec.fields
                    elif rec.fields:
                        raise Invalid('unassociated console/log record')
                elif rec.kind == 'stderr':
                    # Never treat stderr as MI, a successful response or a native stop.
                    # Policy diagnostics must have a descriptor-qualified owner below.
                    pass
                elif rec.kind.startswith('^'):
                    def software(v):
                        if type(v) is dict:
                            return (v.get('type') in (b'breakpoint', b'software breakpoint') or
                                    any(software(x) for x in v.values()))
                        if type(v) is list:
                            return any(software(x) for x in v)
                        return False
                    if software(rec.fields):
                        raise Invalid('unexpected software breakpoint evidence')
                    self.results[rec.token] = rec
                    cmd = self.commands[rec.token]
                    if cmd.startswith('-exec-'):
                        if rec.kind != '^running':
                            raise Invalid('execution command did not run')
                        self.execution_running = True
                    elif rec.kind != '^done':
                        raise Invalid('unexpected result class')
                    if cmd.startswith('-break-insert -h *'):
                        bkpt = rec.fields.get('bkpt')
                        if (type(bkpt) is not dict or bkpt.get('type') != b'hw breakpoint' or
                                bkpt.get('enabled') != b'y' or _hex(bkpt.get('addr')) != int(cmd.split('*')[1], 16) or
                                any(k in bkpt for k in ('pending', 'cond', 'ignore', 'commands', 'locations'))):
                            raise Invalid('hardware site/software fallback evidence')
                    if self.active_stop is not None:
                        self._read_response(cmd, rec)
                elif rec.kind == '*running':
                    if self.execution_token is None:
                        raise Invalid('uncommanded running')
                elif rec.kind == '*stopped':
                    if self.execution_token is None:
                        raise Invalid('unassociated/duplicate stop')
                    # Result-before-stop and stop-before-result are both MI orderings;
                    # the outstanding exact execution token supplies the association.
                    execution = self.execution_token
                    self.stops.append((index, execution, rec))
                    self.active_stop = len(self.stops) - 1
                    self.stop_data[self.active_stop] = {'registers': None, 'names': None, 'reads': []}
                    self.execution_token = None
                elif rec.kind == '=thread-group-started':
                    group = rec.fields['id']
                    if group in self.groups or self.groups:
                        raise Invalid('duplicate/multiple inferior')
                    self.groups[group] = _decimal(rec.fields['pid'])
                elif rec.kind == '=thread-created':
                    tid, group = _decimal(rec.fields['id']), rec.fields['group-id']
                    if tid in self.threads or self.threads or group not in self.groups:
                        raise Invalid('duplicate/multiple/unbound thread')
                    self.threads[tid] = group
                elif rec.kind in ('=thread-group-exited', '=thread-exited'):
                    if len(self.stops) != 2 or self.parser.pending is not None:
                        raise Invalid('premature process exit')
                elif rec.kind == 'prompt':
                    pass
                else:
                    raise Invalid('unexpected async/status/stream record')
        if any(buffers.values()) or self.parser.pending is not None or self.execution_token is not None:
            raise Invalid('incomplete transcript')
        if set(self.commands) != set(self.results):
            raise Invalid('missing command response')
        self.names = None

    def _read_response(self, cmd, rec):
        data = self.stop_data[self.active_stop]
        if cmd == '-data-list-register-names':
            if set(rec.fields) != {'register-names'}:
                raise Invalid('unexpected register result fields')
            names = rec.fields.get('register-names')
            if type(names) is not list or any(type(n) is not bytes for n in names):
                raise Invalid('register mapping')
            names = [n.decode('ascii') for n in names]
            required = {'rip', 'rax', 'r12', 'rdi', 'rsi', 'rdx', 'rcx', 'rsp'}
            if not required <= set(names) or len([n for n in names if n]) != len(set(n for n in names if n)) or data['names'] is not None:
                raise Invalid('ambiguous register mapping')
            data['names'] = names
        elif cmd == '-data-list-register-values x':
            if set(rec.fields) != {'register-values'}:
                raise Invalid('unexpected value result fields')
            if data['names'] is None or data['registers'] is not None:
                raise Invalid('register capture ordering/duplicate')
            entries = rec.fields.get('register-values')
            if type(entries) is not list:
                raise Invalid('register values')
            regs = {}
            for entry in entries:
                if type(entry) is not dict or set(entry) != {'number', 'value'}:
                    raise Invalid('register entry')
                number = _decimal(entry['number'])
                if number >= len(data['names']):
                    raise Invalid('register number')
                name = data['names'][number]
                if not name or name in regs:
                    raise Invalid('duplicate/unnamed register')
                regs[name] = _hex(entry['value'])
            if not {'rip', 'rax', 'r12', 'rdi', 'rsi', 'rdx', 'rcx', 'rsp'} <= set(regs):
                raise Invalid('missing native registers')
            data['registers'] = regs
        elif cmd.startswith('-data-read-memory-bytes '):
            if set(rec.fields) != {'memory'}:
                raise Invalid('unexpected memory result fields')
            address, count = cmd.split()[1:]
            address, count = int(address, 16), int(count)
            blocks = rec.fields.get('memory')
            if type(blocks) is not list or len(blocks) != 1:
                raise Invalid('complete memory result')
            block = blocks[0]
            if type(block) is not dict or set(block) != {'begin', 'offset', 'end', 'contents'}:
                raise Invalid('memory shape')
            if _hex(block['begin']) != address or _hex(block['offset']) != 0 or _hex(block['end']) != address + count:
                raise Invalid('memory request association')
            if type(block['contents']) is not bytes or re.fullmatch(rb'[0-9a-fA-F]*', block['contents']) is None:
                raise Invalid('memory hex')
            raw = bytes.fromhex(block['contents'].decode('ascii'))
            if len(raw) != count:
                raise Invalid('partial memory result')
            data['reads'].append(Read(address, count, raw))

    def readbacks(self, descriptor):
        keys(descriptor, 'settings outputs native_reasons stderr')
        if descriptor['settings'] != dict(zip(READBACKS[:26], Q1)) or set(descriptor['outputs']) != set(READBACKS):
            raise Invalid('Q1 descriptor')
        if self.raw['stderr'] != bytes.fromhex(descriptor['stderr']):
            raise Invalid('unexpected stderr/policy diagnostic')
        result = {}
        for show in READBACKS:
            cmd = '-interpreter-exec console ' + json.dumps(show)
            matches = [t for t, c in self.commands.items() if c == cmd]
            if len(matches) != 1:
                raise Invalid('missing/duplicate Q1 readback')
            t = matches[0]
            form = descriptor['outputs'][show]
            if show == 'show auto-load':
                keys(form, 'facilities')
                facilities = form['facilities']
                names = ['gdb-scripts', 'guile-scripts', 'libthread-db', 'local-gdbinit', 'python-scripts']
                if type(facilities) is not list or [f.get('name') for f in facilities] != names:
                    raise Invalid('complete auto-load facility inventory')
                # Each prefix/suffix is independently frozen for this tool's output
                # dialect; every facility is measured, never inferred from aggregate intent.
                raw = self.streams[t]
                cursor = 0
                for facility in facilities:
                    keys(facility, 'name prefix suffix')
                    prefix, suffix = bytes.fromhex(facility['prefix']), bytes.fromhex(facility['suffix'])
                    if not prefix or not suffix or not raw[cursor:].startswith(prefix):
                        raise Invalid('auto-load output association')
                    start = cursor + len(prefix)
                    end = raw.find(suffix, start)
                    if end < 0 or raw[start:end] != b'off':
                        raise Invalid('auto-load facility enabled/unknown')
                    cursor = end + len(suffix)
                if cursor != len(raw):
                    raise Invalid('unaccounted auto-load readback')
                result[show] = 'set auto-load off'
                continue
            keys(form, 'prefix suffix')
            prefix, suffix = bytes.fromhex(form['prefix']), bytes.fromhex(form['suffix'])
            raw = self.streams[t]
            if not prefix or not suffix or not raw.startswith(prefix) or not raw.endswith(suffix):
                raise Invalid('Q1 readback format')
            measured = raw[len(prefix):-len(suffix)].decode('ascii')
            i = READBACKS.index(show)
            expected = (Q1[i].split()[-1] if i != 16 else '') if i < 26 else ('on' if i < 28 else 'off')
            if measured != expected:
                raise Invalid('Q1 measured policy conflict')
            if show in descriptor['settings']:
                result[show] = 'set ' + show.removeprefix('show ') + (' ' + measured if measured else '')
        first_execution = min((t for t, c in self.commands.items() if c.startswith('-exec-')), default=2**31)
        if any(t >= first_execution for t, c in self.commands.items() if c.startswith('-interpreter-exec console "show ')):
            raise Invalid('late policy readback')
        return result

    def snapshot(self, index, custody, roots, reasons):
        try:
            order, token, rec = self.stops[index]
            data = self.stop_data[index]
            regs = data['registers']
            if regs is None or not data['reads']:
                raise Invalid('missing stop capture')
            Snapshot(data['reads'])
            pc = _hex(rec.fields['frame']['addr'])
            tid = _decimal(rec.fields['thread-id'])
            if (pc != regs['rip'] or tid != custody['tid'] or rec.fields.get('stopped-threads') != b'all' or
                    self.groups.get(self.threads.get(tid)) != custody['pid']):
                raise Invalid('stop snapshot association')
            reason = rec.fields['reason'].decode('ascii')
            binding = reasons[index]
            keys(binding, 'command reason pc trap mechanism')
            if (binding['command'] != self.commands[token] or binding['reason'] != reason or
                    binding['pc'] != pc or binding['mechanism'] not in ('x86-debug-execute', 'x86-in-place-single-step') or
                    binding['trap'] != 'SIGTRAP-native-qualified'):
                raise Invalid('native reason qualification')
            kind = ('qualified-hardware-caller' if pc == 0x581feb and binding['mechanism'] == 'x86-debug-execute' else
                    'qualified-in-place-call-receiver' if pc == 0x69bff0 and binding['mechanism'] == 'x86-in-place-single-step' else 'ready')
            return Stop(order, custody['pid'], tid, custody['creation_id'], regs,
                        tuple(data['reads']), roots, kind, token)
        except (KeyError, IndexError, TypeError, UnicodeError) as exc:
            raise Invalid('missing/ambiguous stop') from exc

    def artifacts(self):
        return {'mi.commands': self.raw['commands'], 'mi.stdout': self.raw['stdout'],
                'mi.stderr': self.raw['stderr'], 'order.jsonl': b''.join(canonical(r) for r in self.order)}


def _decimal(v):
    if type(v) is not bytes or re.fullmatch(rb'[0-9]+', v) is None:
        raise Invalid('decimal native identifier')
    return int(v)


def _hex(v):
    if type(v) is not bytes or re.fullmatch(rb'0x[0-9a-fA-F]+', v) is None or len(v) > 18:
        raise Invalid('bounded native hexadecimal')
    return int(v, 16)


@dataclass(frozen=True)
class Preparation:
    engine: dict
    pins: dict
    artifacts: dict
    custody: dict
    bootstrap: dict
    guard: dict
    q1: dict
    admission: dict
    ready: Stop
    derivation: object
    protected: dict
    a_capture: bytes
    transcript: tuple
    documents: dict


def preparation_codes(p, x, e, namespace):
    """Ordered admission stages, derived from retained records and raw snapshots."""
    from .real_receipt_evidence import forensic_bytes
    try:
        if type(p) is not Preparation:
            return ['EXPECTATION_INVALID']
        expected_protected = {'attempt_id': x, 'identity': p.derivation.a_identity,
            'kind': 'regular-memfd', 'size': 2, 'seals': 15, 'writable_mappings': 0,
            'origin': 'exclusive-fresh-acquisition'}
        if canonical(p.protected) != canonical(expected_protected) or p.a_capture != b'#\n':
            return ['WRONG_PROTECTED_OBJECT']
        faults = derivation_codes(p.derivation, x, p.protected['identity'])
        if faults:
            return faults
        if digest(p.derivation.syscall_capture) != DIGEST:
            return ['INPUT_ALTERED']
        faults = engine_admission(p.engine, p.pins, p.artifacts)
        if faults:
            return faults
        # E and the artifact dossier are independently frozen comparison inputs.
        if (e['bootstrap_sha256'] != p.pins['bootstrap'] or e['observer_sha256'] != p.pins['controller'] or
                e['qualification_sha256'] != p.pins['qualification'] or
                e['engine']['interface_sha256'] != p.pins['decoder'] or e['engine']['abi'] != ENGINE['abi'] or
                e['engine']['images'] != [dict(role=r, sha256=ENGINE['gdb_sha256'] if r == 'observer_native' else ENGINE['sha256'],
                    origin_sha256=p.pins['provenance']) for r in ('compiler', 'executable', 'observer_native')]):
            return ['ENGINE_UNQUALIFIED']
        if p.artifacts['bootstrap'] != canonical(p.bootstrap) or p.artifacts['q1'] != canonical(p.q1):
            return ['OBSERVER_UNQUALIFIED']
        d = Decoder(Snapshot(p.ready.reads))
        b, c, m = p.ready.roots
        try:
            d.callable(c, m)
            d.exact(m, 'module')
            binding, _ = d.dictionary(d.s.number(m + 16))
            if binding.get('compile') != c:
                return ['WRONG_COMPILE_CALLABLE']
        except Invalid:
            return ['WRONG_COMPILE_CALLABLE']
        keys(p.custody, 'namespace controller pid tid creation_id parent_chain credentials channel')
        if (p.custody['namespace'] != namespace or type(p.custody['controller']) is not str or not p.custody['controller'] or
                type(p.custody['creation_id']) is not str or not p.custody['creation_id'] or
                type(p.custody['pid']) is not int or p.custody['pid'] <= 0 or p.custody['tid'] != p.custody['pid'] or
                p.custody['parent_chain'] != ['controller', 'gdb-launcher', 'gdb', 'inferior-launcher', 'cpython'] or
                p.custody['credentials'] != 'ordinary-unchanged' or p.custody['channel'] != 'private-one-use-framed'):
            return ['OBSERVER_UNQUALIFIED']
        bootstrap = dict(profile=PROFILE, source_policy='sealed-bytes-only', parameters=PARAMETERS,
            root_name='_ns001_observer_roots_v1', roots=4, pread_count=3, pread_offset=0,
            retries=0, death_signal='SIGKILL', parent_checks=['before', 'after'],
            shutdown='kill-stopped-no-finalizers', setup_epoch='completed-before-derivation')
        if canonical(p.bootstrap) != canonical(bootstrap):
            return ['OBSERVER_UNQUALIFIED']
        keys(p.guard, 'source_channel environment payload_operations execution_operations coverage')
        if (type(p.guard['environment']) is not dict or type(p.guard['payload_operations']) is not list or
                type(p.guard['execution_operations']) is not list or type(p.guard['coverage']) is not list):
            return ['OBSERVER_UNQUALIFIED']
        policy = dict(source_channel='protected_bytes', environment={}, payload_operations=[], execution_operations=[],
                      coverage=['derivation', 'ready', 'caller', 'receiver', 'kill', 'death'])
        if parse(p.artifacts['guard']) != policy:
            return ['OBSERVER_UNQUALIFIED']
        if p.guard['source_channel'] != 'protected_bytes' or p.guard['environment']:
            return ['SOURCE_REDIRECTION']
        if p.guard['payload_operations']:
            return ['PATHNAME_REOPEN']
        if p.guard['execution_operations']:
            return ['EXECUTION_PROHIBITED']
        if p.guard['coverage'] != ['derivation', 'ready', 'caller', 'receiver', 'kill', 'death']:
            return ['OBSERVER_UNQUALIFIED']
        transcript = Transcript(p.transcript)
        settings = transcript.readbacks(p.q1)
        admission = p.admission
        keys(admission, 'argv environment initial_inventory loader_inventory controls exec syscall step text death task_ids')
        if admission['argv'] != list(initialization_plan()) or admission['environment'] != {'LC_ALL': 'C', 'DEBUGINFOD_URLS': ''} or admission['initial_inventory'] != []:
            return ['OBSERVER_UNQUALIFIED']
        loader = [{'address': 0x2820, 'image': ENGINE['loader_sha256'], 'type': 'software',
                   'insertion': 'denied-before-delegation', 'location': 'shlib-disabled'}]
        if canonical(admission['loader_inventory']) != canonical(loader):
            return ['OBSERVER_UNQUALIFIED']
        controls = [dict(site=site, pc=site, tid=p.custody['tid'], slot=i,
            programming='PTRACE_POKEUSER', trap='SIGTRAP-hardware-before-instruction')
            for i, site in enumerate((0x581feb, 0x69bff0))]
        if canonical(admission['controls']) != canonical(controls) or admission['task_ids'] != [p.custody['tid']]:
            return ['OBSERVER_NOT_ARMED']
        if (admission['exec'] != 'PTRACE_EVENT_EXEC' or admission['syscall'] != ['PTRACE_SYSCALL_ENTRY', 'PTRACE_SYSCALL_EXIT'] or
                admission['step'] != {'from': 0x581feb, 'to': 0x69bff0, 'instruction': 'ffd0',
                    'stack_delta': -8, 'return_pc': 0x581fed, 'receiver_slot': 'armed', 'mode': 'in-place-one-step'} or
                admission['death'] != ['controller-loss-kills-gdb', 'gdb-loss-kills-child', 'parent-checks-match']):
            return ['OBSERVER_NOT_ARMED']
        # Independent channel digests, complete segment bounds and frozen reference
        # dossier associations are supporting measurement evidence, not MI shadow bytes.
        text = admission['text']
        if type(text) is not list or [t.get('role') for t in text] != ['launcher', 'executable', 'loader']:
            return ['ENGINE_UNQUALIFIED']
        references = parse(p.artifacts['qualification'])
        keys(references, 'text_ranges trap_policy')
        if references['trap_policy'] != p.q1['native_reasons']:
            return ['OBSERVER_UNQUALIFIED']
        if len(references['text_ranges']) != len(text):
            return ['ENGINE_UNQUALIFIED']
        for measured, ref in zip(text, references['text_ranges']):
            keys(measured, 'role file_offset length reference_sha256 supervisor_sha256 mi_sha256 writable_executable')
            if (type(measured['file_offset']) is not int or measured['file_offset'] < 0 or
                    type(measured['length']) is not int or not 0 < measured['length'] <= 4 * 1024 * 1024):
                return ['ENGINE_UNQUALIFIED']
            for k in ('reference_sha256', 'supervisor_sha256', 'mi_sha256'):
                hash_value(measured[k])
            if ({k: measured[k] for k in ('role', 'file_offset', 'length', 'reference_sha256')} != ref or
                    measured['supervisor_sha256'] != ref['reference_sha256'] or measured['mi_sha256'] != ref['reference_sha256'] or
                    measured['writable_executable'] is not False):
                return ['ENGINE_UNQUALIFIED']
        if text[1]['file_offset'] != 0x020000 or text[1]['length'] != 0x302fbc - 0x020000 + 1:
            return ['ENGINE_UNQUALIFIED']
        if settings != dict(zip(READBACKS[:26], Q1)):
            return ['OBSERVER_UNQUALIFIED']
        # READY roots/bytes and actual callable association, not a supplied ready flag.
        if (p.ready.pid != p.custody['pid'] or p.ready.tid != p.custody['tid'] or p.ready.custody != p.custody['creation_id'] or
                d.roots(m, x, digest(canonical(e))) != (b, c, m) or b != p.derivation.ready_b):
            return ['OBJECT_SUBSTITUTION']
        if d.bytes(b) != p.derivation.syscall_capture:
            return ['INPUT_ALTERED']
        return []
    except (Invalid, KeyError, TypeError, AttributeError, UnicodeError):
        return ['OBSERVER_UNQUALIFIED']


@dataclass(frozen=True)
class Observation:
    transcript: tuple
    dispatch: dict
    completion: dict
    a_capture: bytes
    protected_final: dict
    maps: tuple
    guard_operations: tuple = ()
    interrupted: bool = False
    native_stops: tuple = ()


def decode_observation(p, observation, x, e, attempted):
    """Build Capture solely from transcript-derived stops and protected admission."""
    if type(observation) is not Observation:
        raise Invalid('observation interface')
    if observation.interrupted:
        return None, None, ['ATTEMPT_INCOMPLETE']
    keys(observation.dispatch, 'attempt_id expectation_sha256 attempted_sha256 frame_count gate')
    dispatch = observation.dispatch
    if dispatch['attempt_id'] != x or dispatch['expectation_sha256'] != digest(canonical(e)):
        return None, None, ['RECORD_INVALID']
    faults = []
    if dispatch['attempted_sha256'] != attempted or dispatch['frame_count'] != 1 or dispatch['gate'] != 'released-once-after-fsync':
        faults.append('OBSERVATION_MISSING')
    transcript = Transcript(observation.transcript)
    if transcript.raw['stderr'] != bytes.fromhex(p.q1['stderr']) or any(transcript.streams.values()):
        raise Invalid('unexpected observer policy/debug diagnostic')
    if len(transcript.stops) != 2:
        raise Invalid('missing/duplicate native pair')
    reasons = p.q1['native_reasons']
    caller = transcript.snapshot(0, p.custody, p.ready.roots, reasons)
    receiver = transcript.snapshot(1, p.custody, p.ready.roots, reasons)
    if len(observation.native_stops) != 2:
        raise Invalid('missing native trap captures')
    for stop, native, qualifier in zip((caller, receiver), observation.native_stops, reasons):
        keys(native, 'token pid tid pc signal mechanism trap register_read source')
        if (native['token'] != stop.token or native['pid'] != stop.pid or native['tid'] != stop.tid or
                native['pc'] != stop.registers['rip'] or native['signal'] != 'SIGTRAP' or
                native['mechanism'] != qualifier['mechanism'] or native['trap'] != qualifier['trap'] or
                native['register_read'] != 'PTRACE_GETREGSET' or native['source'] != 'independent-native-stop-capture'):
            raise Invalid('native trap/MI association')
    if transcript.commands[caller.token] != '-exec-continue' or transcript.commands[receiver.token] != '-exec-step-instruction':
        raise Invalid('exact CALL transition')
    if any(c.startswith('-exec-') for t, c in transcript.commands.items() if t > receiver.token):
        raise Invalid('post-receiver resume')
    if observation.protected_final != p.protected:
        faults.append('OBJECT_SUBSTITUTION')
    if len(observation.maps) != 2 or any(m != canonical(p.admission['text']) for m in observation.maps):
        faults.append('ENGINE_UNQUALIFIED')
    for op in observation.guard_operations:
        faults.append('EXECUTION_PROHIBITED' if op == 'execution' else
                      'SOURCE_REDIRECTION' if op == 'source_redirect' else 'PATHNAME_REOPEN')
    b, c, m = p.ready.roots
    facts = dict.fromkeys(('before_inferior continuous_policy empty_initial_inventory stopping_on register_control_on observer_off '
        'auto_load_all_off classic_loader_denied_disabled no_unexpected_internal_sites no_libthread_db native_exec_event '
        'ptrace_syscall_events in_place_single_call_step receiver_stays_armed raw_unmasked_text_equal complete_text_ranges '
        'two_effective_slots kernel_programming_witnessed blocked_gate_restop death_chain_qualified no_software_fallback '
        'no_post_entry_resume').split(), True)
    # These derived predicates are formed only after validated preparation/transcript,
    # never accepted as bypass flags in the integrated admission interface.
    cap = Capture(x, digest(canonical(e)), attempted, dispatch['attempted_sha256'], caller, receiver,
        receiver.token, p.derivation, p.protected['identity'], observation.a_capture,
        Decoder(Snapshot(p.ready.reads)).bytes(b), b, c, m, 1, 1, False,
        observation.completion, p.engine, p.pins, p.artifacts, dict(zip(READBACKS[:26], Q1)), facts)
    decision, measured = evaluate_capture(cap, x, digest(canonical(e)), attempted)
    if decision == 'ABORT':
        return cap, transcript, ['ATTEMPT_INCOMPLETE']
    return cap, transcript, ranked(faults + measured)


def measured_witness(p, cap, x, e, attempted, faults, precondition=False):
    """Exact frozen witness keys; data comes from decoded observations/comparisons."""
    observations = []
    def add(kind, data):
        observations.append(dict(index=len(observations), kind=kind, data=data))
    if type(p) is Preparation and type(p.a_capture) is bytes:
        add('protected', dict(initial=True, valid='WRONG_PROTECTED_OBJECT' not in faults,
            association='WRONG_PROTECTED_OBJECT' not in faults, seals_exact=p.protected.get('seals') == 15,
            length=p.protected.get('size') if type(p.protected.get('size')) is int and p.protected['size'] >= 0 else None,
            sha256=digest(p.a_capture)))
    if not precondition and cap is not None:
        add('derived', dict(exact_bytes=p.derivation.syscall_capture == b'#\n', from_A='INPUT_IO' not in faults,
            retained=cap.b == p.derivation.ready_b, length=len(p.derivation.syscall_capture), sha256=digest(p.derivation.syscall_capture)))
        add('engine', dict(images_match='ENGINE_UNQUALIFIED' not in faults, live_association='ENGINE_UNQUALIFIED' not in faults,
            build_match=cap.engine == ENGINE, interface_sha256=e['engine']['interface_sha256']))
        add('callable', dict(object_match='WRONG_COMPILE_CALLABLE' not in faults,
            native_target_match='WRONG_COMPILE_CALLABLE' not in faults, binding_match='WRONG_COMPILE_CALLABLE' not in faults))
        add('observer', dict(artifact_match='OBSERVER_UNQUALIFIED' not in faults, attachment_match='OBSERVER_UNQUALIFIED' not in faults,
            qualified='OBSERVER_UNQUALIFIED' not in faults, sentinel_active=True, armed='OBSERVER_NOT_ARMED' not in faults))
        add('dispatch', dict(attempted_event_sha256=attempted, persisted='OBSERVATION_MISSING' not in faults))
        params, raw, exact, length = None, None, False, None
        d = Decoder(Snapshot(cap.receiver.reads))
        kwnames = cap.receiver.registers['rcx']
        d.exact(kwnames, 'tuple')
        keyword_count = d.s.number(kwnames + 16, signed=True)
        if not 0 <= keyword_count <= 4:
            raise Invalid('unavailable bounded keyword count')
        keyword_names = None
        try:
            keyword_names = [d.unicode(ptr) for ptr in d.tuple(kwnames, 4)]
            canonical(keyword_names)
        except Invalid:
            keyword_names = None
        try:
            source = d.s.number(cap.receiver.registers['rsi'])
            d.exact(source, 'bytes')
            exact = True
            length = d.s.number(source + 16, signed=True)
            if 0 <= length <= 3:
                raw = d.bytes(source)
            _, params, _ = d.arguments(cap.receiver.registers, cap.b)
            canonical(params)
        except Invalid:
            params = None
        add('entry', dict(native_entry=cap.receiver.registers['rip'] == 0x69bff0,
            engine_match='ENGINE_UNQUALIFIED' not in faults, callable_match='WRONG_COMPILE_CALLABLE' not in faults,
            after_dispatch='OBSERVATION_MISSING' not in faults, armed='OBSERVER_NOT_ARMED' not in faults,
            exact_bytes=exact and raw == b'#\n', same_B='OBJECT_SUBSTITUTION' not in faults,
            same_A='OBJECT_SUBSTITUTION' not in faults, independent_A_equal=raw is not None and raw == cap.a_capture,
            vector_valid=params is not None, parameters_match=parameters_match(params), length=length if length is not None and length >= 0 else None,
            sha256=digest(raw) if raw is not None else None, positional_count=cap.receiver.registers['rdx'],
            keyword_count=keyword_count, keyword_names=keyword_names, parameters=params))
        add('protected', dict(initial=False, valid='OBJECT_SUBSTITUTION' not in faults,
            association='OBJECT_SUBSTITUTION' not in faults, seals_exact=p.protected['seals'] == 15,
            length=len(cap.a_capture), sha256=digest(cap.a_capture)))
        add('completion', dict(linked_to_entry=True, outcome='observer_stop'))
        add('end', dict(entry_count=cap.entry_count, observer_entry_count=cap.observer_entry_count,
            same_A='OBJECT_SUBSTITUTION' not in faults, seals_exact=p.protected['seals'] == 15,
            no_reopen='PATHNAME_REOPEN' not in faults, observer_complete=True, execution_coverage=True,
            execution_attempted='EXECUTION_PROHIBITED' in faults))
    return dict(schema=SCHEMA + 'witness.v1', attempt_id=x, expectation_sha256=digest(canonical(e)),
        qualification_sha256=e['qualification_sha256'], observer_sha256=e['observer_sha256'],
        observations=observations, violations=ranked(faults))


def qualification_material(p):
    material = {digest(raw): raw for raw in p.artifacts.values()}
    for h, raw in p.documents.items():
        if digest(raw) != h:
            raise Invalid('document identity')
        material[h] = raw
    return material


def _retain_observer(attempt, files):
    from .real_receipt_evidence import retain, synchronize_dir
    path = attempt.path / 'observer'
    if not path.exists():
        path.mkdir(mode=0o700)
        synchronize_dir(attempt.path)
    for name, raw in files.items():
        if '/' in name or name in ('.', '..'):
            raise Invalid('observer artifact path')
        retain(path / name, raw)


def retain_preparation(attempt, p):
    from .real_receipt_evidence import forensic_bytes
    files = {'admission.json': forensic_bytes(p)}
    if type(p) is Preparation:
        # Invalid transcripts still retain original bytes and actual chunk order.
        raws, order = dict.fromkeys(('commands', 'stdout', 'stderr'), b''), []
        for i, chunk in enumerate(p.transcript):
            if type(chunk) is not Chunk or chunk.channel not in raws:
                continue
            order.append(dict(index=i, channel=chunk.channel, offset=len(raws[chunk.channel]), length=len(chunk.raw)))
            raws[chunk.channel] += chunk.raw
        files.update({'setup.mi.commands': raws['commands'], 'setup.mi.stdout': raws['stdout'],
            'setup.mi.stderr': raws['stderr'], 'setup.order.jsonl': b''.join(canonical(o) for o in order),
            'derivation.json': forensic_bytes(p.derivation), 'B.derived.bin': p.derivation.syscall_capture})
        if type(p.admission) is dict and 'text' in p.admission:
            files['maps.before'] = canonical(p.admission['text'])
        try:
            files['B.ready.bin'] = Decoder(Snapshot(p.ready.reads)).bytes(p.ready.roots[0])
        except (Invalid, KeyError, AttributeError, TypeError):
            pass  # Preserve only actually measured bytes; no placeholder capture.
    try:
        _retain_observer(attempt, files)
    except BaseException:
        attempt.store.failed = True
        raise


def _all_files(attempt):
    """Attempt-local package view; snapshots prevent later reservations changing it."""
    from pathlib import Path
    root, ordinal = attempt.store.root, attempt.path.name
    files = {}
    for base in (root / 'qualification', root / ordinal):
        for p in sorted(base.rglob('*')):
            if p.is_symlink():
                raise Invalid('package symlink')
            if p.is_file() and p.name not in ('package-manifest.json', 'package-manifest.sha256'):
                files[p.relative_to(root).as_posix()] = p.read_bytes()
    # Immutable per-attempt snapshots identify shared store state at this attempt.
    for p in (attempt.path / 'store-snapshot').iterdir():
        if p.is_file():
            files[f'{ordinal}/store-snapshot/{p.name}'] = p.read_bytes()
    files['expectation.json'] = (root / 'expectation.json').read_bytes()
    files[f'reservations/{ordinal}'] = (root / 'reservations' / ordinal).read_bytes()
    return files


def _capture_manifest(attempt):
    from .real_receipt_evidence import retain, manifest
    q = attempt.store.root / 'qualification'
    files = {p.relative_to(attempt.store.root).as_posix(): p.read_bytes() for p in q.iterdir() if p.is_file()}
    files.update({p.relative_to(attempt.store.root).as_posix(): p.read_bytes()
                  for p in (attempt.path / 'observer').iterdir() if p.is_file()})
    raw = canonical(manifest('capture', attempt.x,
        digest((attempt.store.root / 'expectation.json').read_bytes()), files))
    path = attempt.path / 'capture-manifest.json'
    if path.exists():
        if path.is_symlink() or path.read_bytes() != raw:
            raise Invalid('capture manifest conflict/partial write')
    else:
        retain(path, raw)


def _package(attempt):
    """One-shot explicit packaging; no repair/re-dispatch after any partial write."""
    from .real_receipt_evidence import retain, synchronize_dir, manifest
    attempt.store.check()
    terminal = attempt.raw('recovery.json')
    if terminal is None:
        events = attempt.events()
        terminal = canonical(events[-1]) if events and events[-1]['state'] in ('ACCEPTED', 'REFUSED') else None
    if terminal is None or attempt._packaging_authority != digest(terminal):
        raise Invalid('no fresh terminal-write packaging authority')
    attempt._packaging_authority = None  # Consume before any write; no retry after failure.
    if (attempt.path / 'package-started').exists():
        raise Invalid('packaging already attempted; retained incomplete state')
    retain(attempt.path / 'package-started', canonical({'attempt_id': attempt.x}))
    snap = attempt.path / 'store-snapshot'
    snap.mkdir(mode=0o700)
    synchronize_dir(attempt.path)
    for name in ('store.json', 'custody', 'lock', 'reservation-journal.jsonl'):
        retain(snap / name, (attempt.store.root / name).read_bytes())
    files = _all_files(attempt)
    raw = canonical(manifest('package', attempt.x,
        digest((attempt.store.root / 'expectation.json').read_bytes()), files))
    retain(attempt.path / 'package-manifest.json', raw)
    retain(attempt.path / 'package-manifest.sha256', (digest(raw) + '\n').encode('ascii'))
    if not verify_package(attempt):
        raise Invalid('package completeness/hash verification failed')
    return raw


def verify_package(attempt, require_accept=False):
    """Read-only verification; it neither fills files nor rewrites valid terminals."""
    from .real_receipt_evidence import verify_manifest, validate
    try:
        files = _all_files(attempt)
        e = validate(parse((attempt.store.root / 'expectation.json').read_bytes()), 'expectation')
        h = digest(canonical(e))
        raw = attempt.raw('package-manifest.json')
        if raw is None or attempt.raw('package-manifest.sha256') != (digest(raw) + '\n').encode('ascii'):
            return False
        if not verify_manifest(raw, files, 'package', attempt.x, h):
            return False
        ordinal = attempt.path.name
        capraw = attempt.raw('capture-manifest.json')
        captured = {n: b for n, b in files.items() if n.startswith('qualification/') or n.startswith(f'{ordinal}/observer/')}
        if capraw is None or not verify_manifest(capraw, captured, 'capture', attempt.x, h):
            return False
        for n, b in files.items():
            if n.startswith('qualification/') and digest(b) != n.split('/')[-1]:
                return False
        mandatory = {f'qualification/{e[k]}' for k in ('spec_sha256', 'bootstrap_sha256', 'observer_sha256', 'qualification_sha256')}
        mandatory |= {f'{ordinal}/store-snapshot/{n}' for n in ('store.json', 'custody', 'lock', 'reservation-journal.jsonl')}
        mandatory |= {f'reservations/{ordinal}', 'expectation.json'}
        if not mandatory <= set(files):
            return False
        snapshot = parse(files[f'{ordinal}/store-snapshot/store.json'])
        if snapshot != {'schema': SCHEMA + 'store.v1', 'namespace': attempt.store.namespace}:
            return False
        if parse(files[f'{ordinal}/store-snapshot/custody']) != {'namespace': attempt.store.namespace, 'kind': 'exclusive-controller'}:
            return False
        if not require_accept:
            return True
        events = attempt.events()
        if not events or events[-1]['state'] != 'ACCEPTED' or attempt.raw('recovery.json') is not None:
            return False
        reg = validate(parse(attempt.raw('registration.json')), 'registration')
        req = validate(parse(attempt.raw('request.json')), 'request')
        if (reg['attempt_id'] != attempt.x or reg['expectation_sha256'] != h or
                reg['request_sha256'] != digest(attempt.raw('request.json')) or req['expectation_sha256'] != h or
                req['profile'] != PROFILE or not parameters_match(req['parameters']) or
                req['source_channel'] != 'protected_bytes' or req['source_environment'] or req['cwd_policy'] != 'exclusive-synthetic'):
            return False
        required = ('mi.commands mi.stdout mi.stderr order.jsonl admission.json maps.before maps.stop1 maps.stop2 '
            'derivation.json stop1.json stop2.json arguments.json B.derived.bin B.ready.bin B.entry.bin A.entry.bin '
            'completion.json setup.mi.commands setup.mi.stdout setup.mi.stderr setup.order.jsonl').split()
        if not {f'{ordinal}/observer/{n}' for n in required} <= set(files):
            return False
        for name in ('B.derived.bin', 'B.ready.bin', 'B.entry.bin', 'A.entry.bin'):
            if files[f'{ordinal}/observer/{name}'] != b'#\n':
                return False
        if digest(attempt.raw('witness.json')) != events[-1]['witness_sha256']:
            return False
        w = validate(parse(attempt.raw('witness.json')), 'witness')
        from .real_receipt_evidence import witness_codes
        if witness_codes(w, attempt.x, e, digest(canonical(events[-2]))):
            return False
        return True
    except (Invalid, ValueError, KeyError, TypeError, OSError):
        return False


def finish_observation(attempt, p, observation, e, attempted, supplied_witness=None):
    from .real_receipt_evidence import retain, forensic_bytes, validate, witness_codes
    if observation is None:
        raise Invalid('raw observation required')
    # Preserve the whole submitted object, including incomplete/interrupted inputs.
    retain(attempt.path / 'capture.json', forensic_bytes(observation))
    raws, order = dict.fromkeys(('commands', 'stdout', 'stderr'), b''), []
    if type(observation) is Observation:
        for i, chunk in enumerate(observation.transcript):
            if type(chunk) is Chunk and chunk.channel in raws:
                order.append(dict(index=i, channel=chunk.channel, offset=len(raws[chunk.channel]), length=len(chunk.raw)))
                raws[chunk.channel] += chunk.raw
    rawfiles = {'mi.commands': raws['commands'], 'mi.stdout': raws['stdout'], 'mi.stderr': raws['stderr'],
                'order.jsonl': b''.join(canonical(o) for o in order)}
    _retain_observer(attempt, rawfiles)
    try:
        cap, transcript, faults = decode_observation(p, observation, attempt.x, e, attempted)
    except (Invalid, KeyError, TypeError, ValueError):
        attempt.recover()
        _capture_manifest(attempt)
        _package(attempt)
        return attempt.raw('recovery.json')
    if cap is None or 'ATTEMPT_INCOMPLETE' in faults:
        result = attempt.recover()
        _capture_manifest(attempt)
        _package(attempt)
        return result
    b, c, m = p.ready.roots
    d = Decoder(Snapshot(cap.receiver.reads))
    source = d.s.number(cap.receiver.registers['rsi'])
    try:
        raw = d.bytes(source)
    except Invalid:
        raw = None
    try:
        _, params, _ = d.arguments(cap.receiver.registers, b)
        canonical(params)
    except Invalid:
        params = None
    files = {'stop1.json': forensic_bytes(cap.caller), 'stop2.json': forensic_bytes(cap.receiver),
        'arguments.json': canonical({'parameters': params, 'source': source}),
        'maps.stop1': observation.maps[0], 'maps.stop2': observation.maps[1],
        'A.entry.bin': observation.a_capture, 'completion.json': canonical(observation.completion),
        'native-stops.json': forensic_bytes(observation.native_stops)}
    if raw is not None:
        files['B.entry.bin'] = raw
    _retain_observer(attempt, files)
    _capture_manifest(attempt)  # Raw capture/death -> capture manifest -> witness -> terminal.
    try:
        w = measured_witness(p, cap, attempt.x, e, attempted, faults)
    except (Invalid, KeyError, TypeError):
        result = attempt.recover()
        _package(attempt)
        return result
    if supplied_witness is not None and canonical(supplied_witness) != canonical(w):
        faults = ranked(['RECORD_INVALID'] + faults)
        w['violations'] = faults
    faults = ranked(faults + witness_codes(w, attempt.x, e, attempted))
    w['violations'] = faults
    validate(w, 'witness')
    retain(attempt.path / 'witness.json', canonical(w))
    attempt._validated_terminal = digest(canonical(w))
    entered = w['observations'][6]['data']['native_entry']
    terminal = attempt.event('REFUSED' if faults else 'ACCEPTED', faults, entered, attempt._validated_terminal)
    _package(attempt)
    return terminal


def package_recovery(attempt):
    """Explicit recovery packaging; never dispatches or repairs terminal packages."""
    result = attempt.recover()
    if result['state'] != 'ABORTED':
        return result
    if attempt.raw('package-manifest.json') is not None or (attempt.path / 'package-started').exists():
        return result
    if not (attempt.path / 'observer').exists():
        _retain_observer(attempt, {'recovery-reservation.bin': (attempt.store.root / 'reservations' / attempt.path.name).read_bytes()})
    _capture_manifest(attempt)
    _package(attempt)
    return result


def compare_repetition(left, right):
    """Compare canonical positives, stripping only verified ID-derived links.

    Raw forensic PIDs/addresses/timing are not canonical semantic records. Their
    originals stay in independently verified packages; none is rewritten.
    """
    from .real_receipt_evidence import validate
    if left.x == right.x or not verify_package(left, True) or not verify_package(right, True):
        return False
    def semantic(a):
        e = parse((a.store.root / 'expectation.json').read_bytes())
        request = validate(parse(a.raw('request.json')), 'request')
        reg = validate(parse(a.raw('registration.json')), 'registration')
        if reg['attempt_id'] != a.x or reg['request_sha256'] != digest(a.raw('request.json')) or reg['expectation_sha256'] != digest(canonical(e)):
            raise Invalid('repetition registration links')
        reg = {k: v for k, v in reg.items() if k != 'attempt_id'}
        events = [{k: v for k, v in event.items() if k not in ('attempt_id', 'previous_sha256', 'witness_sha256')}
                  for event in a.events()]
        witness = validate(parse(a.raw('witness.json')), 'witness')
        if witness['attempt_id'] != a.x:
            raise Invalid('repetition witness identity')
        witness = {k: v for k, v in witness.items() if k != 'attempt_id'}
        # Only this exact causal hash is ID-derived; other hashes are retained.
        for o in witness['observations']:
            if o['kind'] == 'dispatch':
                o['data'] = {k: v for k, v in o['data'].items() if k != 'attempted_event_sha256'}
        captures = [(a.path / 'observer' / n).read_bytes() for n in
                    ('B.derived.bin', 'B.ready.bin', 'B.entry.bin', 'A.entry.bin')]
        return canonical([e, request, reg, events, witness]), captures
    try:
        return semantic(left) == semantic(right)
    except (Invalid, OSError, KeyError, TypeError):
        return False
