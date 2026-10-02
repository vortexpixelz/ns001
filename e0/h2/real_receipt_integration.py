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
    def __init__(self, chunks, expected_stops=None):
        self.chunks = tuple(chunks)
        self.parser = MIParser()
        self.raw = dict.fromkeys(('commands', 'stdout', 'stderr'), b'')
        self.order, self.commands, self.results, self.stops = [], {}, {}, []
        self.streams, self.stop_data = {}, {}
        self.record_order = []
        self.running_notification = False
        self.active_stop = None
        self.execution_token = None
        self.execution_running = False
        self.groups, self.threads = {}, {}
        self.seen_groups, self.seen_threads = set(), set()
        self.terminal_exit = False
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
                if self.terminal_exit:
                    raise Invalid('command after terminal death')
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
                self.record_order.append((index, pending, rec))
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
                    if 'bkpt' in rec.fields and not cmd.startswith('-break-insert -h *'):
                        raise Invalid('unassociated hardware insertion result')
                    if cmd.startswith('-break-delete ') and rec.fields:
                        raise Invalid('ambiguous hardware retirement result')
                    if cmd.startswith('-exec-'):
                        if rec.kind != '^running':
                            raise Invalid('execution command did not run')
                        self.execution_running = self.execution_token is not None
                    elif rec.kind != '^done':
                        raise Invalid('unexpected result class')
                    if cmd.startswith('-break-insert -h *'):
                        bkpt = rec.fields.get('bkpt')
                        if (type(bkpt) is not dict or bkpt.get('type') != b'hw breakpoint' or
                                bkpt.get('enabled') != b'y' or _hex(bkpt.get('addr')) != int(cmd.split('*')[1], 16) or
                                any(k in bkpt for k in ('pending', 'cond', 'ignore', 'commands', 'locations'))):
                            raise Invalid('hardware site/software fallback evidence')
                    if cmd.startswith('-data-read-memory-bytes ') and self.active_stop is None:
                        raise Invalid('memory read without stopped custody')
                    if self.active_stop is not None:
                        self._read_response(cmd, rec)
                elif rec.kind == '*running':
                    if (self.execution_token is None or self.running_notification or
                            rec.token not in (None, self.execution_token) or
                            set(rec.fields) != {'thread-id'} or
                            rec.fields['thread-id'] not in (b'all',) + tuple(str(t).encode() for t in self.threads)):
                        raise Invalid('uncommanded/duplicate/unrelated running')
                    self.running_notification = True
                elif rec.kind == '*stopped':
                    if (self.execution_token is None or not self.running_notification or
                            rec.token not in (None, self.execution_token)):
                        raise Invalid('unassociated/duplicate stop')
                    self.running_notification = False
                    self.execution_running = False
                    # Result-before-stop and stop-before-result are both MI orderings;
                    # the outstanding exact execution token supplies the association.
                    execution = self.execution_token
                    self.stops.append((index, execution, rec))
                    self.active_stop = len(self.stops) - 1
                    self.stop_data[self.active_stop] = {'registers': None, 'names': None, 'reads': [],
                        'groups': dict(self.groups), 'threads': dict(self.threads)}
                    self.execution_token = None
                elif rec.kind == '=thread-group-started':
                    group = rec.fields['id']
                    if group in self.seen_groups or self.groups or self.terminal_exit:
                        raise Invalid('duplicate/multiple inferior')
                    self.groups[group] = _decimal(rec.fields['pid'])
                    self.seen_groups.add(group)
                elif rec.kind == '=thread-created':
                    tid, group = _decimal(rec.fields['id']), rec.fields['group-id']
                    if tid in self.seen_threads or self.threads or group not in self.groups or self.terminal_exit:
                        raise Invalid('duplicate/multiple/unbound thread')
                    self.threads[tid] = group
                    self.seen_threads.add(tid)
                elif rec.kind in ('=thread-group-exited', '=thread-exited'):
                    if rec.kind == '=thread-exited':
                        tid, group = _decimal(rec.fields['id']), rec.fields['group-id']
                        if self.threads.get(tid) != group:
                            raise Invalid('exit of unowned thread')
                        del self.threads[tid]
                    else:
                        group = rec.fields['id']
                        if group not in self.groups:
                            raise Invalid('exit of unowned process')
                        del self.groups[group]
                        self.threads = {t: g for t, g in self.threads.items() if g != group}
                    if (expected_stops is None or len(self.stops) != expected_stops or
                            self.parser.pending is not None or self.execution_token is not None or
                            self.active_stop is None or
                            self.stop_data[self.active_stop]['registers'] is None or
                            not self.stop_data[self.active_stop]['reads']):
                        raise Invalid('premature process/thread exit')
                    self.terminal_exit = True
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
        if self.groups != data['groups'] or self.threads != data['threads']:
            raise Invalid('capture after custody loss')
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
        # Complete setup history is reconciled, including notifications before commands.
        policy_end = max(i for i, _, rec in self.record_order
                         if rec.kind == '^done' and rec.token in
                         [t for t, c in self.commands.items() if c.startswith('-interpreter-exec console \"show ')])
        for i, owner, rec in self.record_order:
            if rec.kind in ('=thread-group-started', '=thread-created', '*running', '*stopped') and i <= policy_end:
                raise Invalid('inferior/event before Q1 policy')
            if (rec.kind in ('~', '&') and rec.fields and
                    self.commands.get(owner, '') not in
                    ['-interpreter-exec console ' + json.dumps(show) for show in READBACKS]):
                raise Invalid('unqualified setup diagnostic')
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
                    data['groups'].get(data['threads'].get(tid)) != custody['pid']):
                raise Invalid('stop snapshot association')
            if ('signal-name' in rec.fields and rec.fields['signal-name'] != b'SIGTRAP' or
                    'signal-meaning' in rec.fields or any(k in rec.fields for k in ('exit-code', 'core'))):
                raise Invalid('contradictory stop signal/exit')
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
    text_captures: tuple = ()
    native_derivation: tuple = ()
    native_controls: tuple = ()


def preparation_codes(p, x, e, namespace):
    """Gather independently supported stage faults, then apply frozen precedence.

    A damaged earlier stage never causes later supplied negative evidence to vanish;
    missing measurements fail their own stage without inventing replacement inputs.
    """
    if type(p) is not Preparation:
        return ['EXPECTATION_INVALID']
    stages = (_protected_codes, _derivation_codes, _engine_codes, _callable_codes,
              _custody_codes, _guard_codes, _observer_codes)
    return ranked([code for stage in stages for code in stage(p, x, e, namespace)] +
                  supported_guard_faults(p, None))


def _protected_codes(p, x, e, namespace):
    try:
        expected_protected = {'attempt_id': x, 'identity': p.derivation.a_identity,
            'kind': 'regular-memfd', 'size': 2, 'seals': 15, 'writable_mappings': 0,
            'origin': 'exclusive-fresh-acquisition'}
        if canonical(p.protected) != canonical(expected_protected) or p.a_capture != b'#\n':
            return ['WRONG_PROTECTED_OBJECT']
        return []
    except (Invalid, KeyError, TypeError, AttributeError, UnicodeError):
        return ['WRONG_PROTECTED_OBJECT']


def _derivation_codes(p, x, e, namespace):
    try:
        faults = derivation_codes(p.derivation, x, p.protected['identity'])
        if faults:
            return faults
        if digest(p.derivation.syscall_capture) != DIGEST:
            return ['INPUT_ALTERED']
        return []
    except (Invalid, KeyError, TypeError, AttributeError, UnicodeError):
        return ['INPUT_IO']


def _engine_codes(p, x, e, namespace):
    try:
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
        return []
    except (Invalid, KeyError, TypeError, AttributeError, UnicodeError):
        return ['ENGINE_UNQUALIFIED']


def _callable_codes(p, x, e, namespace):
    try:
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
        return []
    except (Invalid, KeyError, TypeError, AttributeError, UnicodeError):
        return ['WRONG_COMPILE_CALLABLE']


def _custody_codes(p, x, e, namespace):
    try:
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
        return []
    except (Invalid, KeyError, TypeError, AttributeError, UnicodeError):
        return ['OBSERVER_UNQUALIFIED']


def _guard_codes(p, x, e, namespace):
    try:
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
        return []
    except (Invalid, KeyError, TypeError, AttributeError, UnicodeError):
        return ['OBSERVER_UNQUALIFIED']


def _observer_codes(p, x, e, namespace):
    try:
        b, c, m = p.ready.roots
        d = Decoder(Snapshot(p.ready.reads))
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
        keys(references, 'text_ranges trap_policy tool_roles setup_path')
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
            if ({k: measured[k] for k in ('role', 'file_offset', 'length', 'reference_sha256')} != {k: ref[k] for k in ('role', 'file_offset', 'length', 'reference_sha256')} or
                    measured['supervisor_sha256'] != ref['reference_sha256'] or measured['mi_sha256'] != ref['reference_sha256'] or
                    measured['writable_executable'] is not False):
                return ['ENGINE_UNQUALIFIED']
        if text[1]['file_offset'] != 0x020000 or text[1]['length'] != 0x302fbc - 0x020000 + 1:
            return ['ENGINE_UNQUALIFIED']
        validate_setup(p, transcript, references)
        validate_controls(p)
        validate_text(p, p.text_captures, ('launcher', 'post-exec', 'ready'))
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
    text_captures: tuple = ()


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
    transcript = Transcript(observation.transcript, expected_stops=2)
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
    if len(observation.maps) != 2 or any(m != text_maps(observation.text_captures, epoch)
            for m, epoch in zip(observation.maps, ('caller', 'receiver'))):
        faults.append('ENGINE_UNQUALIFIED')
    validate_text(p, observation.text_captures, ('caller', 'receiver'))
    reconcile_mi_text(transcript, observation.text_captures, ('caller', 'receiver'))
    for stop in (caller, receiver):
        code = Snapshot(stop.reads)
        if code.read(ENGINE['caller'], 2) != bytes.fromhex(ENGINE['caller_hex']) or code.read(ENGINE['receiver'], 4) != bytes.fromhex(ENGINE['receiver_hex']):
            raise Invalid('missing/changed actual CALL/entry bytes')
    for op in observation.guard_operations:
        faults.append('EXECUTION_PROHIBITED' if op == 'execution' else
                      'SOURCE_REDIRECTION' if op == 'source_redirect' else 'PATHNAME_REOPEN')
    b, c, m = p.ready.roots
    setup = Transcript(p.transcript)
    settings = setup.readbacks(p.q1)
    references = parse(p.artifacts['qualification'])
    setup_facts = validate_setup(p, setup, references)
    hardware_facts = validate_hardware_history(setup, transcript, references, p.custody)
    controls = validate_controls(p)
    facts = {
        'before_inferior': not any(i <= setup_facts['policy_end'] and r.kind in
            ('=thread-group-started', '=thread-created') for i, _, r in setup.record_order),
        'continuous_policy': settings == p.q1['settings'],
        'empty_initial_inventory': p.admission['initial_inventory'] == [],
        'stopping_on': setup_facts['readback_values']['show may-stop'] == b'on',
        'register_control_on': setup_facts['readback_values']['show may-write-registers'] == b'on',
        'observer_off': setup_facts['readback_values']['show observer'] == b'off',
        'auto_load_all_off': settings.get('show auto-load') == 'set auto-load off',
        'classic_loader_denied_disabled': all(o['insertion'] == 'denied-before-delegation' and
            o['location'] == 'shlib-disabled' for o in p.admission['loader_inventory']),
        'no_unexpected_internal_sites': not any(stream for token, stream in setup.streams.items()
            if not setup.commands[token].startswith('-interpreter-exec console "show ')),
        'no_libthread_db': p.q1['outputs']['show auto-load']['facilities'][2]['name'] == 'libthread-db'
            and settings['show libthread-db-search-path'] == 'set libthread-db-search-path /dev/null',
        'native_exec_event': controls['exec'],
        'ptrace_syscall_events': setup_facts['syscalls'] == (1, 1),
        'in_place_single_call_step': transcript.commands[receiver.token] == '-exec-step-instruction'
            and receiver.registers['rsp'] == caller.registers['rsp'] - 8,
        'receiver_stays_armed': hardware_facts['monitor_armed'],
        'raw_unmasked_text_equal': validate_text(p, observation.text_captures, ('caller', 'receiver')),
        'complete_text_ranges': validate_text(p, p.text_captures, ('launcher', 'post-exec', 'ready')),
        'two_effective_slots': controls['slots'] == [0, 1] and
            hardware_facts['active_count'] == 2,
        'kernel_programming_witnessed': controls['writes'] == [0, 1],
        'blocked_gate_restop': controls['restop'] and setup_facts['ready'] and dispatch['gate'] == 'released-once-after-fsync',
        'death_chain_qualified': p.admission['death'] == ['controller-loss-kills-gdb', 'gdb-loss-kills-child', 'parent-checks-match'],
        'no_software_fallback': controls['hardware_traps'] == [0, 1],
        'no_post_entry_resume': not any(c.startswith('-exec-') for t, c in transcript.commands.items() if t > receiver.token),
    }
    entry_count = setup_facts['receiver_hits'] + sum(_hex(r.fields['frame']['addr']) == ENGINE['receiver']
        for _, _, r in transcript.stops)
    sentinel_count = setup_facts['receiver_hits'] + sum(n['pc'] == ENGINE['receiver'] for n in observation.native_stops)
    cap = Capture(x, digest(canonical(e)), attempted, dispatch['attempted_sha256'], caller, receiver,
        receiver.token, p.derivation, p.protected['identity'], observation.a_capture,
        Decoder(Snapshot(p.ready.reads)).bytes(b), b, c, m, entry_count, sentinel_count, False,
        observation.completion, p.engine, p.pins, p.artifacts, settings, facts)
    decision, measured = evaluate_capture(cap, x, digest(canonical(e)), attempted)
    if decision == 'ABORT':
        return cap, transcript, ranked(faults + measured, recovery=True)
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
            qualified='OBSERVER_UNQUALIFIED' not in faults, sentinel_active=cap.q1_facts['receiver_stays_armed'], armed='OBSERVER_NOT_ARMED' not in faults))
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
            files['maps.before'] = text_maps(p.text_captures, 'ready')
        try:
            files['B.ready.bin'] = Decoder(Snapshot(p.ready.reads)).bytes(p.ready.roots[0])
        except (Invalid, KeyError, AttributeError, TypeError):
            pass  # Preserve only actually measured bytes; no placeholder capture.
    if type(p) is Preparation:
        files.update(text_files(p.text_captures))
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
    for name in ('store.json', 'custody', 'lock', 'lock-identity.json', 'reservation-journal.jsonl'):
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
        mandatory |= {f'{ordinal}/store-snapshot/{n}' for n in ('store.json', 'custody', 'lock', 'lock-identity.json', 'reservation-journal.jsonl')}
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
        if f'{ordinal}/capture.json' not in files:
            return False
        required = ('native-stops.json mi.commands mi.stdout mi.stderr order.jsonl admission.json maps.before maps.stop1 maps.stop2 '
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
        # Reparse the original captures and independently reproduce terminal facts.
        p, o = retained_inputs(attempt, files)
        if preparation_codes(p, attempt.x, e, attempt.store.namespace) or frozen_role_codes(attempt.store, p, e):
            return False
        tried = digest(canonical(events[-2]))
        cap, transcript, faults = decode_observation(p, o, attempt.x, e, tried)
        if cap is None or faults or canonical(measured_witness(p, cap, attempt.x, e, tried, [])) != attempt.raw('witness.json'):
            return False
        from .real_receipt_evidence import forensic_bytes
        if files[f'{ordinal}/observer/native-stops.json'] != forensic_bytes(o.native_stops):
            return False
        if files[f'{ordinal}/observer/derivation.json'] != forensic_bytes(p.derivation):
            return False
        if files[f'{ordinal}/observer/stop1.json'] != forensic_bytes(cap.caller) or files[f'{ordinal}/observer/stop2.json'] != forensic_bytes(cap.receiver):
            return False
        for name, raw in transcript.artifacts().items():
            if files[f'{ordinal}/observer/{name}'] != raw:
                return False
        if files[f'{ordinal}/observer/completion.json'] != canonical(o.completion):
            return False
        if files[f'{ordinal}/observer/maps.before'] != text_maps(p.text_captures, 'ready'):
            return False
        for i, raw in enumerate(o.maps, 1):
            if files[f'{ordinal}/observer/maps.stop{i}'] != raw:
                return False
        setup = Transcript(p.transcript)
        for name, raw in setup.artifacts().items():
            if files[f'{ordinal}/observer/setup.{name}'] != raw:
                return False
        d = Decoder(Snapshot(cap.receiver.reads))
        source = d.s.number(cap.receiver.registers['rsi'])
        _, parameters, _ = d.arguments(cap.receiver.registers, cap.b)
        if files[f'{ordinal}/observer/arguments.json'] != canonical({'parameters': parameters, 'source': source}):
            return False
        if parse(files[f'{ordinal}/supported-faults.json']):
            return False
        if f'{ordinal}/observed-faults.json' in files and parse(files[f'{ordinal}/observed-faults.json']):
            return False
        for name, raw in text_files(p.text_captures + o.text_captures).items():
            if files[f'{ordinal}/observer/{name}'] != raw:
                return False
        return True
    except (Invalid, ValueError, KeyError, TypeError, OSError, AttributeError):
        return False


def finish_observation(attempt, p, observation, e, attempted, supplied_witness=None):
    from .real_receipt_evidence import retain, forensic_bytes, validate, witness_codes
    if observation is None:
        raise Invalid('raw observation required')
    # Retain independent supported faults before any later decode can erase them.
    known = supported_predecode_faults(p, observation, attempt.x, e, attempted)
    if (forensic_bytes(attempt._preparation_input) != attempt._preparation_bytes or
            forensic_bytes(p) != attempt._preparation_bytes):
        known += supported_guard_faults(attempt._preparation_input, None) + ['RECORD_INVALID']
        _retain_observer(attempt, {'admission-later.json': forensic_bytes(attempt._preparation_input)})
    known = ranked(known)
    retain(attempt.path / 'supported-faults.json', canonical(known))
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
    if type(observation) is Observation:
        rawfiles.update(text_files(observation.text_captures))
    _retain_observer(attempt, rawfiles)
    try:
        cap, transcript, faults = decode_observation(p, observation, attempt.x, e, attempted)
    except (Invalid, KeyError, TypeError, ValueError):
        attempt.recover()
        _capture_manifest(attempt)
        _package(attempt)
        return attempt.raw('recovery.json')
    faults = ranked(faults + known, recovery=True)
    if cap is None or 'ATTEMPT_INCOMPLETE' in faults:
        retain(attempt.path / 'observed-faults.json', canonical([f for f in faults if f != 'ATTEMPT_INCOMPLETE']))
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
        roles = parse((a.store.root / 'qualification' / e['qualification_sha256']).read_bytes())['tool_roles']
        return canonical([e, request, reg, events, witness, roles]), captures
    try:
        return semantic(left) == semantic(right)
    except (Invalid, OSError, KeyError, TypeError):
        return False


@dataclass(frozen=True)
class TextCapture:
    """Independent binary read plus its stopped-child/file-handle map association.

    Raw supervisor bytes stay outside MI/JSON bounds. The MI site reads must agree
    with these bytes. No read primitive is executed by this offline interface.
    """
    epoch: str
    role: str
    mapping: dict
    raw: bytes

    @property
    def filename(self):
        if self.epoch not in ('launcher', 'post-exec', 'ready', 'caller', 'receiver') or self.role not in ('launcher', 'executable', 'loader'):
            raise Invalid('text artifact role/epoch')
        return f'text.{self.epoch}.{self.role}.bin'


def text_files(captures):
    files = {}
    for c in captures:
        if type(c) is not TextCapture or c.filename in files or type(c.raw) is not bytes or not 0 < len(c.raw) <= 4 * 1024 * 1024:
            raise Invalid('bounded binary text artifact')
        files[c.filename] = c.raw
    return files


def text_maps(captures, epoch):
    return canonical([dict(role=c.role, **c.mapping) for c in captures if c.epoch == epoch])


def validate_text(p, captures, epochs):
    refs = parse(p.artifacts['qualification'])['text_ranges']
    expected = [(epoch, r['role']) for epoch in epochs for r in refs
                if r['role'] in (('launcher', 'loader') if epoch == 'launcher' else ('executable', 'loader'))]
    if [(c.epoch, c.role) for c in captures] != expected:
        raise Invalid('missing/duplicate text epoch/range')
    for c in captures:
        ref = next(r for r in refs if r['role'] == c.role)
        m = c.mapping
        keys(m, 'start end file_offset device inode handle load_bias pid tid source image_sha256')
        if (any(type(m[k]) is not int or m[k] < 0 for k in ('start', 'end', 'file_offset', 'device', 'inode', 'load_bias', 'pid', 'tid')) or
                m['source'] != 'independent-supervisor-unmasked-read' or not m['inode'] or not m['handle'] or
                m['pid'] != p.custody['pid'] or m['tid'] != p.custody['tid'] or
                not 0 < m['start'] < m['end'] <= 2**64 or
                m['file_offset'] + ref['length'] > 2**64 or
                m['start'] != ref['address'] or m['end'] != m['start'] + ref['length'] or
                m['file_offset'] != ref['file_offset'] or m['image_sha256'] != ref['image_sha256'] or
                m['load_bias'] != ref['load_bias'] or
                type(c.raw) is not bytes or len(c.raw) != ref['length'] or
                len(c.raw) > 4 * 1024 * 1024 or digest(c.raw) != ref['reference_sha256'] or
                p.documents.get(ref['reference_sha256']) != c.raw):
            raise Invalid('raw text/map/reference association')
        if c.role == 'executable':
            for pc, raw in ((ENGINE['caller'], bytes.fromhex(ENGINE['caller_hex'])),
                            (ENGINE['receiver'], bytes.fromhex(ENGINE['receiver_hex']))):
                off = pc - m['start']
                if off < 0 or c.raw[off:off + len(raw)] != raw:
                    raise Invalid('raw CALL/entry text')
    for c in captures:
        prior = next((b for b in p.text_captures if b.role == c.role), None)
        if prior is not None and c.mapping != prior.mapping:
            raise Invalid('post-admission backing map change')
    # Same open reference and map identity across all stopped epochs of each image.
    for role in ('launcher', 'executable', 'loader'):
        maps = [canonical(c.mapping) for c in captures if c.role == role]
        if maps and any(m != maps[0] for m in maps):
            raise Invalid('text backing handle/map changed')
    return True


def frozen_role_codes(store, p, e):
    try:
        q = store.root / 'qualification' / e['qualification_sha256']
        roles = parse(q.read_bytes())['tool_roles']
        if roles != {r: h for r, h in p.pins.items() if r != 'qualification'}:
            return ['ENGINE_UNQUALIFIED']
        if p.pins['qualification'] != e['qualification_sha256']:
            return ['ENGINE_UNQUALIFIED']
        for r, h in p.pins.items():
            path = store.root / 'qualification' / h
            if path.is_symlink() or path.read_bytes() != p.artifacts[r]:
                return ['ENGINE_UNQUALIFIED']
        return []
    except (Invalid, OSError, KeyError, TypeError, AttributeError):
        return ['ENGINE_UNQUALIFIED']


def supported_guard_faults(p, observation):
    faults = []
    if type(p) is Preparation and type(p.guard) is dict:
        if p.guard.get('execution_operations'):
            faults.append('EXECUTION_PROHIBITED')
        if p.guard.get('payload_operations'):
            faults.append('PATHNAME_REOPEN')
        if p.guard.get('source_channel') != 'protected_bytes' or p.guard.get('environment'):
            faults.append('SOURCE_REDIRECTION')
    if type(observation) is Observation:
        if type(observation.guard_operations) is not tuple:
            return ranked(faults + ['OBSERVATION_MISSING'])
        for op in observation.guard_operations:
            faults.append('EXECUTION_PROHIBITED' if op == 'execution' else
                          'SOURCE_REDIRECTION' if op == 'source_redirect' else 'PATHNAME_REOPEN')
    return ranked(faults)


def supported_predecode_faults(p, observation, x, e, attempted):
    """Persist independent observed facts before the MI parser can fail."""
    faults = supported_guard_faults(p, observation)
    if type(p) is Preparation and type(observation) is Observation:
        if observation.protected_final != p.protected:
            faults.append('OBJECT_SUBSTITUTION')
        if type(observation.dispatch) is dict:
            d = observation.dispatch
            if all(k in d for k in ('attempt_id', 'expectation_sha256')) and (
                    d['attempt_id'] != x or d['expectation_sha256'] != digest(canonical(e))):
                faults.append('RECORD_INVALID')
            if all(k in d for k in ('attempted_sha256', 'frame_count', 'gate')) and (
                    d['attempted_sha256'] != attempted or d['frame_count'] != 1 or d['gate'] != 'released-once-after-fsync'):
                faults.append('OBSERVATION_MISSING')
        if type(observation.a_capture) is bytes and observation.a_capture != p.a_capture:
            faults.append('OBSERVATION_MISSING')
        try:
            if type(observation.maps) is tuple and type(observation.text_captures) is tuple:
                if len(observation.maps) != 2 or any(m != text_maps(observation.text_captures, epoch)
                        for m, epoch in zip(observation.maps, ('caller', 'receiver'))):
                    faults.append('ENGINE_UNQUALIFIED')
        except (Invalid, AttributeError, TypeError, ValueError):
            # Malformed ancillary data supplies no association fact; it must not
            # prevent already supported guard/object faults from being persisted.
            pass
    return ranked(faults)


def reconcile_mi_text(transcript, captures, epochs):
    """Compare every actual addressed MI text intersection to retained binary bytes.

    Object reads outside executable mappings remain object evidence. No absent MI
    byte is supplied from a reference. Snapshot also rejects ambiguous overlaps.
    """
    for index, data in transcript.stop_data.items():
        epoch = epochs[index]
        for read in data['reads']:
            Snapshot.range(read.address, read.requested)
            for capture in captures:
                if capture.epoch != epoch or capture.role != 'executable':
                    continue
                start, end = capture.mapping['start'], capture.mapping['end']
                if not 0 < start < end <= 2**64:
                    raise Invalid('text range overflow')
                lo, hi = max(start, read.address), min(end, read.address + read.requested)
                if lo < hi and read.data[lo-read.address:hi-read.address] != capture.raw[lo-start:hi-start]:
                    raise Invalid('MI/supervisor text disagreement')
    return True


def validate_hardware_history(setup, observation, references, custody):
    """Replay successful retained control results across setup and receipt phases.

    Temporary sites follow the frozen sequential phases, including the return
    site spanning syscall stops. Receiver retirement is never reversible.
    """
    # Retain scope with each active site: dropping it would allow contradictory
    # MI thread restrictions to be replaced by admitted/native expected values.
    first = setup.stop_data.get(0, {})
    group = first.get('threads', {}).get(custody['tid'])
    if group is None or first.get('groups', {}).get(group) != custody['pid']:
        raise Invalid('hardware scope without admitted process/thread custody')

    def site(bkpt):
        address = _hex(bkpt.get('addr'))
        thread = _decimal(bkpt['thread']) if 'thread' in bkpt else None
        groups = bkpt.get('thread-groups')
        if (thread is not None and thread != custody['tid'] or
                groups is not None and groups != [group] or 'task' in bkpt):
            raise Invalid('hardware scope excludes admitted receipt thread/process')
        return address, thread, tuple(groups) if groups is not None else None

    def addresses():
        return {value[0] for value in active.values()}

    active, used = {}, set()
    receiver_id = None
    count = 0
    path = references['setup_path']
    # The return site spans the entry/exit syscall catchpoints. READY is a
    # blocked-gate restop; its caller site is installed only after that capture.
    temporary = (0x4f6102, 0x4f6224, 0x4f6224, 0x4f6224, 0x4f6274, 0x4f6299, None)
    for transcript, observing in ((setup, False), (observation, True)):
        if transcript is None:
            continue
        for _, _, rec in transcript.record_order:
            if rec.kind.startswith('^'):
                cmd = transcript.commands[rec.token]
                if cmd.startswith('-break-insert -h *'):
                    bkpt = rec.fields['bkpt']
                    number, scoped_site = _decimal(bkpt['number']), site(bkpt)
                    address = scoped_site[0]
                    if not number or number in used or address in addresses():
                        raise Invalid('duplicate/reused hardware identity/site')
                    if observing:
                        raise Invalid('hardware insertion after READY')
                    if address == ENGINE['receiver']:
                        if receiver_id is not None or count:
                            raise Invalid('late/replaced receiver monitor')
                        receiver_id = number
                    elif address == ENGINE['caller']:
                        if count != len(path) or len(active) != 1:
                            raise Invalid('caller before derivation retirement')
                    elif count >= len(temporary) or address != temporary[count]:
                        raise Invalid('hardware site outside frozen derivation phase')
                    active[number] = scoped_site
                    used.add(number)
                    if len(active) > 2:
                        raise Invalid('hardware slot budget')
                elif cmd.startswith('-break-delete '):
                    number = int(cmd.split()[1])
                    if number not in active or number == receiver_id or observing:
                        raise Invalid('receipt monitor/unknown hardware retirement')
                    del active[number]
                elif cmd == '-break-list':
                    table = rec.fields.get('BreakpointTable', {})
                    body = table.get('body')
                    if type(body) is not list:
                        raise Invalid('missing hardware inventory')
                    measured = {}
                    for entry in body:
                        b = entry.get('bkpt', entry)
                        if b.get('type') != b'hw breakpoint' or b.get('enabled') != b'y':
                            raise Invalid('unexpected inventory site')
                        n = _decimal(b.get('number'))
                        if n in measured:
                            raise Invalid('duplicate inventory')
                        measured[n] = site(b)
                    if measured != active:
                        raise Invalid('hardware inventory disagreement')
                elif cmd.startswith('-exec-'):
                    if not observing and count >= len(path):
                        raise Invalid('execution beyond frozen setup path')
                    if receiver_id not in active:
                        raise Invalid('unarmed receiver during execution')
                    permitted = ({ENGINE['receiver'], ENGINE['caller']} if observing else
                        {ENGINE['receiver']} | ({temporary[count]} if temporary[count] is not None else set()))
                    if addresses() != permitted:
                        raise Invalid('incomplete/unretired phase hardware inventory')
            elif rec.kind == '*stopped' and not observing:
                count += 1
        if addresses() != {ENGINE['receiver'], ENGINE['caller']}:
            raise Invalid('READY/receipt hardware inventory')
    return dict(monitor_armed=receiver_id in active and
        active[receiver_id][1] in (None, custody['tid']) and
        active[receiver_id][2] in (None, (group,)), active_count=len(active))


def validate_setup(p, transcript, references):
    """Reconcile every setup stop with the independently frozen native path.

    Native syscall/wrapper values are decoded from addressed raw reads/registers;
    the caller's Derivation descriptor cannot supply missing measurements.
    """
    path = references['setup_path']
    hardware = validate_hardware_history(transcript, None, references, p.custody)
    reconcile_mi_text(transcript, p.text_captures, ('post-exec',) * 6 + ('ready',))
    if len(path) != 7 or len(transcript.stops) != len(path) or len(p.native_derivation) != len(path):
        raise Invalid('incomplete/unexpected setup stop history')
    if transcript.groups != {b'i1': p.custody['pid']} or transcript.threads != {p.custody['tid']: b'i1'}:
        raise Invalid('setup sole inferior/thread custody')
    # The receiver monitor is installed before the first setup continuation and
    # retained through READY; a final descriptor cannot backfill lifetime coverage.
    first_exec = min(t for t, c in transcript.commands.items() if c.startswith('-exec-'))
    receiver_inserts = [t for t, c in transcript.commands.items() if c == '-break-insert -h *0x69bff0']
    caller_inserts = [t for t, c in transcript.commands.items() if c == '-break-insert -h *0x581feb']
    if len(receiver_inserts) != 1 or receiver_inserts[0] >= first_exec or len(caller_inserts) != 1:
        raise Invalid('missing lifetime receiver/ready caller instrumentation')
    monitor = transcript.results[receiver_inserts[0]].fields.get('bkpt', {})
    monitor_id = _decimal(monitor.get('number'))
    if any(c == f'-break-delete {monitor_id}' for c in transcript.commands.values()):
        raise Invalid('lifetime receiver monitor retired')
    if caller_inserts[0] <= transcript.stops[-1][1]:
        raise Invalid('caller armed outside READY admission phase')
    snapshots = []
    for i, (binding, native) in enumerate(zip(path, p.native_derivation)):
        stop = transcript.snapshot(i, p.custody, p.ready.roots, path)
        if stop.registers['rip'] != binding['pc'] or native != dict(token=stop.token, pid=stop.pid,
                tid=stop.tid, pc=stop.registers['rip'], signal='SIGTRAP', mechanism=binding['mechanism'],
                trap=binding['trap'], registers=stop.registers, reads=[dict(address=r.address,
                requested=r.requested, hex=r.data.hex()) for r in stop.reads],
                source='independent-native-stop-capture'):
            raise Invalid('setup native/MI association')
        snapshots.append(stop)
    pcs = tuple(s.registers['rip'] for s in snapshots)
    if pcs != (0x4f6102, 0x4f621f, 0x4f6224, 0x4f6224, 0x4f6274, 0x4f6299, p.ready.registers['rip']):
        raise Invalid('unqualified derivation control path')
    wrapper, entry, exit_, returned, resized, ret, ready = snapshots
    w, a, z, r, b, v = [s.registers for s in snapshots[:6]]
    d = p.derivation
    wm, zm, bm, vm = [Snapshot(s.reads) for s in (wrapper, exit_, resized, ret)]
    from .real_receipt_observation import Derivation
    measured = Derivation(d.attempt, d.a_identity, w['rdi'], w['rip'],
        (w['rip'], r['rip'], b['rip'], v['rip']), a['rax'], a['rdi'], a['rdx'], a['r10'],
        z['rax'], zm.read(a['rsi'], 2), a['rsi'], bm.number(b['rbp'] - 0x38), v['rax'],
        ready.roots[0], wm.number(w['rsp']), vm.number(v['rsp']),
        sum(q['reason'] == 'syscall-entry' for q in path), sum(q['reason'] == 'syscall-return' for q in path),
        d.seals_before, d.seals_after, d.size_before, d.size_after,
        all(s.pid == wrapper.pid and s.tid == wrapper.tid for s in snapshots))
    from .real_receipt_evidence import forensic_bytes
    em = Snapshot(entry.reads)
    if (a['rsi'] != em.number(a['rbp'] - 0x38) + 32 or
            Decoder(Snapshot(resized.reads)).bytes(measured.post_resize_b) != measured.syscall_capture or
            Decoder(Snapshot(ret.reads)).bytes(measured.return_b) != measured.syscall_capture):
        raise Invalid('raw original buffer/resize bytes association')
    if (forensic_bytes(measured) != forensic_bytes(d) or derivation_codes(measured, d.attempt, p.protected['identity']) or
            w['rsi'] != 3 or w['rdx'] != 0 or r['rax'] != 2 or
            any(z[k] != a[k] for k in ('rdi', 'rsi', 'rdx', 'r10')) or
            not 0x420000 <= measured.return_pc_in <= 0x702fbc):
        raise Invalid('raw pread/call/resize/return chain')
    if ready.registers != p.ready.registers or ready.reads != p.ready.reads:
        raise Invalid('READY capture not associated with setup')
    policy_tokens = [t for t, c in transcript.commands.items() if c.startswith('-interpreter-exec console "show ')]
    policy_end = max(i for i, _, rec in transcript.record_order if rec.kind == '^done' and rec.token in policy_tokens)
    values = {}
    for show in ('show may-stop', 'show may-write-registers', 'show observer'):
        token = next(t for t, cmd in transcript.commands.items() if cmd == '-interpreter-exec console ' + json.dumps(show))
        form = p.q1['outputs'][show]
        values[show] = transcript.streams[token][len(bytes.fromhex(form['prefix'])):-len(bytes.fromhex(form['suffix']))]
    return dict(policy_end=policy_end, readback_values=values, ready=pcs[-1] == p.ready.registers['rip'], monitor_armed=hardware['monitor_armed'],
        receiver_hits=sum(pc == ENGINE['receiver'] for pc in pcs), syscalls=(measured.syscall_entries, measured.syscall_exits))


def retained_inputs(attempt, files):
    """Decode only the known supporting evidence interface; no dynamic constructors.

    Binary links resolve to retained artifacts with exact byte lengths/hashes.
    This is read-only replay, never evidence reconstruction or missing-file repair.
    """
    prefix = attempt.path.name + '/observer/'
    def decode(v):
        if type(v) is dict:
            if set(v) == {'hex', 'length'}:
                raw = bytes.fromhex(v['hex'])
                if len(raw) != v['length']:
                    raise Invalid('supporting hex length')
                return raw
            if set(v) == {'qualification_artifact', 'length'}:
                raw = files['qualification/' + v['qualification_artifact']]
                if digest(raw) != v['qualification_artifact'] or len(raw) != v['length']:
                    raise Invalid('binary qualification link')
                return raw
            if set(v) == {'artifact', 'length', 'sha256'}:
                if '/' in v['artifact']:
                    raise Invalid('binary capture link path')
                raw = files[prefix + v['artifact']]
                if len(raw) != v['length'] or digest(raw) != v['sha256']:
                    raise Invalid('binary capture link')
                return raw
            return {k: decode(x) for k, x in v.items()}
        if type(v) is list:
            return [decode(x) for x in v]
        return v
    def chunks(v):
        return tuple(Chunk(**c) for c in v)
    def texts(v):
        return tuple(TextCapture(**c) for c in v)
    def stop(v):
        v['reads'] = tuple(Read(**r) for r in v['reads'])
        v['roots'] = tuple(v['roots'])
        return Stop(**v)
    from .real_receipt_observation import Derivation
    p = decode(parse(files[prefix + 'admission.json']))
    p['transcript'] = chunks(p['transcript'])
    p['text_captures'] = texts(p['text_captures'])
    p['native_derivation'] = tuple(p['native_derivation'])
    p['native_controls'] = tuple(p['native_controls'])
    p['ready'] = stop(p['ready'])
    p['derivation']['sites'] = tuple(p['derivation']['sites'])
    p['derivation'] = Derivation(**p['derivation'])
    o = decode(parse(files[attempt.path.name + '/capture.json']))
    o['transcript'] = chunks(o['transcript'])
    o['text_captures'] = texts(o['text_captures'])
    o['maps'] = tuple(o['maps'])
    o['guard_operations'] = tuple(o['guard_operations'])
    o['native_stops'] = tuple(o['native_stops'])
    return Preparation(**p), Observation(**o)


def validate_controls(p):
    """Independent native launcher control records; descriptors alone do not qualify.

    These captures remain conditional on their collector/host provenance. Offline
    validation checks actual wait, programming results and native register values.
    """
    records = p.native_controls
    if type(records) is not tuple or len(records) != 6:
        raise Invalid('missing native control capture')
    exec_, write0, hit0, write1, hit1, restop = records
    common = dict(pid=p.custody['pid'], tid=p.custody['tid'],
                  source='independent-native-control-capture')
    if canonical(exec_) != canonical(dict(**common, event='exec', wait_status=(4 << 16) | (5 << 8) | 0x7f)):
        raise Invalid('native exec-event status')
    for i, (write, hit) in enumerate(((write0, hit0), (write1, hit1))):
        pc = p.admission['controls'][i]['site']
        if canonical(write) != canonical(dict(**common, event='program', request='PTRACE_POKEUSER', slot=i, address=pc,
                         dr7_enable=1 << (2 * i), rw_len=0, result=0)):
            raise Invalid('native hardware programming result')
        if canonical(hit) != canonical(dict(**common, event='hardware-stop', slot=i, wait_status=(5 << 8) | 0x7f,
                       siginfo_code=4, dr6=1 << i, register_read='PTRACE_GETREGSET', rip=pc)):
            raise Invalid('native effective execute-slot trap')
    if canonical(restop) != canonical(dict(**common, event='closed-gate-restop', wait_status=(5 << 8) | 0x7f,
                      register_read='PTRACE_GETREGSET', rip=p.ready.registers['rip'],
                      gate_frames_received=0)):
        raise Invalid('closed-gate native restop')
    return dict(exec=exec_['wait_status'] >> 16 == 4,
                writes=[r['slot'] for r in (write0, write1) if r['result'] == 0],
                slots=[r['slot'] for r in (hit0, hit1)],
                hardware_traps=[r['slot'] for r in (hit0, hit1) if r['siginfo_code'] == 4],
                restop=restop['gate_frames_received'] == 0)
