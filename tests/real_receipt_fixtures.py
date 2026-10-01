"""Synthetic evidence constructors; never a process, observer, or candidate runner."""
import copy
from dataclasses import replace
import json
from pathlib import Path
from e0.h2.real_receipt_policy import ENGINE, Q1, READBACKS, PARAMETERS, PROFILE, canonical, digest, mi_command, initialization_plan, parse
from e0.h2.real_receipt_integration import Chunk, Preparation, Observation, qualification_material, TextCapture, text_maps
from test_e0_h2_real_receipt import expectation, native_memory, capture, B, C, M


def _mi(value):
    if type(value) is str:
        return json.dumps(value)
    if type(value) is dict:
        return '{' + ','.join(k + '=' + _mi(v) for k, v in value.items()) + '}'
    if type(value) is list:
        return '[' + ','.join(_mi(v) for v in value) + ']'
    raise TypeError(value)


def preparation(x):
    cap = capture(x=x)
    bootstrap = dict(profile=PROFILE, source_policy='sealed-bytes-only', parameters=copy.deepcopy(PARAMETERS),
        root_name='_ns001_observer_roots_v1', roots=4, pread_count=3, pread_offset=0,
        retries=0, death_signal='SIGKILL', parent_checks=['before', 'after'],
        shutdown='kill-stopped-no-finalizers', setup_epoch='completed-before-derivation')
    guard = dict(source_channel='protected_bytes', environment={}, payload_operations=[], execution_operations=[],
                 coverage=['derivation', 'ready', 'caller', 'receiver', 'kill', 'death'])
    native_reasons = [dict(command='-exec-continue', reason='breakpoint-hit', pc=0x581feb,
        trap='SIGTRAP-native-qualified', mechanism='x86-debug-execute'),
        dict(command='-exec-step-instruction', reason='end-stepping-range', pc=0x69bff0,
        trap='SIGTRAP-native-qualified', mechanism='x86-in-place-single-step')]
    # These outputs are an explicitly synthetic, frozen readback dialect. The
    # integrated parser compares actual stream bytes, not fabricated ^done values.
    q1 = dict(settings=dict(zip(READBACKS[:26], Q1)),
        outputs={s: {'prefix': (s + ' : ').encode().hex(), 'suffix': b'\n'.hex()}
                 for s in READBACKS}, native_reasons=native_reasons, stderr='')
    q1['outputs']['show auto-load'] = {'facilities': [dict(name=n,
        prefix=('auto-load ' + n + ' : ').encode().hex(), suffix=b'\n'.hex())
        for n in ('gdb-scripts', 'guile-scripts', 'libthread-db', 'local-gdbinit', 'python-scripts')]}
    # Complete bounded synthetic code ranges, with the actual fixed site bytes.
    code = bytearray(0x302fbc - 0x020000 + 1)
    code[0x581feb - 0x420000:0x581feb - 0x420000 + 2] = bytes.fromhex('ffd0')
    code[0x69bff0 - 0x420000:0x69bff0 - 0x420000 + 4] = bytes.fromhex('f30f1efa')
    raw_text = {'launcher': b'ABCDE', 'executable': bytes(code), 'loader': b'FGHIJ'}
    ranges = [dict(role=r, file_offset=0x020000 if r == 'executable' else 0,
        length=len(raw_text[r]), address=0x420000 if r == 'executable' else 0x800000 if r == 'launcher' else 0x900000,
        load_bias=0, image_sha256=ENGINE['sha256'] if r == 'executable' else
            ENGINE['loader_sha256'] if r == 'loader' else digest(raw_text[r]),
        reference_sha256=digest(raw_text[r])) for r in ('launcher', 'executable', 'loader')]
    setup_path = [dict(command='-exec-continue', reason=reason, pc=pc,
        trap='SIGTRAP-native-qualified', mechanism='x86-debug-execute') for pc, reason in
        ((0x4f6102, 'breakpoint-hit'), (0x4f621f, 'syscall-entry'), (0x4f6224, 'syscall-return'),
         (0x4f6224, 'breakpoint-hit'), (0x4f6274, 'breakpoint-hit'), (0x4f6299, 'breakpoint-hit'),
         (0x581feb, 'breakpoint-hit'))]
    qual = dict(text_ranges=ranges, trap_policy=native_reasons, setup_path=setup_path)
    artifacts = dict(cap.artifacts)
    artifacts.update(bootstrap=canonical(bootstrap), guard=canonical(guard), q1=canonical(q1))
    qual['tool_roles'] = {r: digest(raw) for r, raw in artifacts.items() if r != 'qualification'}
    artifacts['qualification'] = canonical(qual)
    pins = {r: digest(raw) for r, raw in artifacts.items()}
    e = expectation()
    e.update(bootstrap_sha256=pins['bootstrap'], observer_sha256=pins['controller'], qualification_sha256=pins['qualification'])
    e['engine']['interface_sha256'] = pins['decoder']
    e['engine']['images'] = [dict(role=r, sha256=ENGINE['gdb_sha256'] if r == 'observer_native' else ENGINE['sha256'],
        origin_sha256=pins['provenance']) for r in ('compiler', 'executable', 'observer_native')]
    names = ('INPUT_BOUNDARY_SPEC', 'ENGINE_PROVENANCE_REVIEW', 'NATIVE_OBSERVER_DESIGN', 'RECEIPT_EXPERIMENT_DESIGN', 'GDB_Q1_REVIEW')
    directory = Path(__file__).resolve().parents[1] / 'docs/e0/h2'
    docs = {digest(raw): raw for name in names for raw in
            [(directory / ('NS-001_H2A2_REAL_CPYTHON_' + name + '_v0.1.md')).read_bytes()]}
    docs.update({digest(raw): raw for raw in raw_text.values()})
    build = canonical(ENGINE)
    e['engine']['build_sha256'] = digest(build)
    docs[digest(build)] = build
    spec = (directory / 'NS-001_H2A2_REAL_CPYTHON_INPUT_BOUNDARY_SPEC_v0.1.md').read_bytes()
    e['spec_sha256'] = digest(spec)
    mem = native_memory(x, digest(canonical(e)))
    ready = replace(cap.caller, reads=mem.reads(), reason='ready')
    custody = dict(namespace=x.split(':')[0], controller='synthetic-controller-custody', pid=401, tid=401,
        creation_id='retained-pidfd-creation-identity', parent_chain=['controller', 'gdb-launcher', 'gdb', 'inferior-launcher', 'cpython'],
        credentials='ordinary-unchanged', channel='private-one-use-framed')
    admission = dict(argv=list(initialization_plan()), environment={'LC_ALL': 'C', 'DEBUGINFOD_URLS': ''}, initial_inventory=[],
        loader_inventory=[dict(address=0x2820, image=ENGINE['loader_sha256'], type='software', insertion='denied-before-delegation', location='shlib-disabled')],
        controls=[dict(site=s, pc=s, tid=401, slot=i, programming='PTRACE_POKEUSER', trap='SIGTRAP-hardware-before-instruction')
                  for i, s in enumerate((0x581feb, 0x69bff0))], exec='PTRACE_EVENT_EXEC',
        syscall=['PTRACE_SYSCALL_ENTRY', 'PTRACE_SYSCALL_EXIT'],
        step=dict(**{'from': 0x581feb, 'to': 0x69bff0}, instruction='ffd0', stack_delta=-8,
                  return_pc=0x581fed, receiver_slot='armed', mode='in-place-one-step'),
        text=[dict(**{k: r[k] for k in ('role', 'file_offset', 'length', 'reference_sha256')}, supervisor_sha256=r['reference_sha256'], mi_sha256=r['reference_sha256'], writable_executable=False) for r in ranges],
        death=['controller-loss-kills-gdb', 'gdb-loss-kills-child', 'parent-checks-match'], task_ids=[401])
    transcript = []
    for i, show in enumerate(READBACKS, 1):
        value = (Q1[i - 1].split()[-1] if i != 17 else '') if i <= 26 else ('on' if i <= 28 else 'off')
        output = (''.join('auto-load ' + f['name'] + ' : off\n' for f in q1['outputs'][show]['facilities'])
                  if show == 'show auto-load' else show + ' : ' + value + '\n')
        transcript += [Chunk('commands', mi_command(i, '-interpreter-exec console ' + json.dumps(show))),
            Chunk('stdout', ('~' + _mi(output) + '\n').encode()),
            Chunk('stdout', f'{i}^done\n'.encode())]
    text_captures = make_text_captures(ranges, raw_text, ('launcher', 'post-exec', 'ready'))
    # Raw setup stops and independent native records must both cover every link.
    transcript += [Chunk('commands', mi_command(30, '-break-insert -h *0x69bff0')),
        Chunk('stdout', b'30^done,bkpt={number="1",type="hw breakpoint",enabled="y",addr="0x69bff0"}\n')]
    transcript.append(Chunk('stdout', b'=thread-group-started,id="i1",pid="401"\n=thread-created,id="401",group-id="i1"\n'))
    raw_stops = []
    base = dict(cap.caller.registers)
    from e0.h2.real_receipt_abi import Read
    d = cap.derivation
    stack, rbp = 0x31000, 0x32038
    measurements = [
        ({**base, 'rip': 0x4f6102, 'rdi': d.fd, 'rsi': 3, 'rdx': 0, 'rsp': stack},
            (Read(stack, 8, d.return_pc_in.to_bytes(8, 'little')),)),
        ({**base, 'rip': 0x4f621f, 'rax': 17, 'rdi': d.fd, 'rsi': d.original_buffer, 'rdx': 3, 'r10': 0, 'rbp': rbp},
            (Read(d.original_buffer, 2, d.syscall_capture), Read(rbp - 0x38, 8, (d.original_buffer - 32).to_bytes(8, 'little')))),
        ({**base, 'rip': 0x4f6224, 'rax': 2, 'rdi': d.fd, 'rsi': d.original_buffer, 'rdx': 3, 'r10': 0},
            (Read(d.original_buffer, 2, d.syscall_capture),)),
        ({**base, 'rip': 0x4f6224, 'rax': 2}, (Read(d.original_buffer, 2, d.syscall_capture),)),
        ({**base, 'rip': 0x4f6274, 'rbp': rbp}, (Read(rbp - 0x38, 8, B.to_bytes(8, 'little')),
            next(r for r in ready.reads if r.address == B))),
        ({**base, 'rip': 0x4f6299, 'rax': B, 'rsp': stack},
            (Read(stack, 8, d.return_pc_out.to_bytes(8, 'little')), next(r for r in ready.reads if r.address == B))),
        (ready.registers, ready.reads),
    ]
    token = 31
    for binding, (regs, reads) in zip(setup_path, measurements):
        raw_stops.append(dict(token=token, pid=401, tid=401, pc=regs['rip'], signal='SIGTRAP',
            mechanism=binding['mechanism'], trap=binding['trap'], registers=regs,
            reads=[dict(address=r.address, requested=r.requested, hex=r.data.hex()) for r in reads],
            source='independent-native-stop-capture'))
        token = append_stop(transcript, token, binding['command'], binding['reason'], regs, reads)
    transcript += [Chunk('commands', mi_command(token, '-break-insert -h *0x581feb')),
        Chunk('stdout', (f'{token}^done,bkpt={{number="2",type="hw breakpoint",enabled="y",addr="0x581feb"}}\n').encode())]
    common = dict(pid=401, tid=401, source='independent-native-control-capture')
    native_controls = [dict(**common, event='exec', wait_status=(4 << 16) | (5 << 8) | 0x7f)]
    for i, pc in enumerate((0x581feb, 0x69bff0)):
        native_controls += [dict(**common, event='program', request='PTRACE_POKEUSER', slot=i, address=pc,
            dr7_enable=1 << (2 * i), rw_len=0, result=0),
            dict(**common, event='hardware-stop', slot=i, wait_status=(5 << 8) | 0x7f,
                siginfo_code=4, dr6=1 << i, register_read='PTRACE_GETREGSET', rip=pc)]
    native_controls.append(dict(**common, event='closed-gate-restop', wait_status=(5 << 8) | 0x7f,
        register_read='PTRACE_GETREGSET', rip=ready.registers['rip'], gate_frames_received=0))
    protected = dict(attempt_id=x, identity=cap.derivation.a_identity, kind='regular-memfd', size=2,
                     seals=15, writable_mappings=0, origin='exclusive-fresh-acquisition')
    return e, Preparation(copy.deepcopy(ENGINE), pins, artifacts, custody, bootstrap, guard, q1,
        admission, ready, cap.derivation, protected, b'#\n', tuple(transcript), docs, text_captures, tuple(raw_stops), tuple(native_controls))


def observation(p, x, e, attempted, mutate_memory=None, mutate_regs=None):
    mem = native_memory(x, digest(canonical(e)))
    if mutate_memory:
        mutate_memory(mem)
    base = dict(rip=0x581feb, rax=0x69bff0, r12=C, rdi=M, rsi=0x13000, rdx=6, rcx=0x14000, rsp=0x30008)
    chunks, token = [Chunk('stdout', b'=thread-group-started,id="i1",pid="401"\n=thread-created,id="401",group-id="i1"\n')], 100
    native_stops = []
    for index, (command, reason, regs) in enumerate((('-exec-continue', 'breakpoint-hit', base),
            ('-exec-step-instruction', 'end-stepping-range', {**base, 'rip': 0x69bff0, 'rsp': 0x30000}))):
        if mutate_regs:
            regs = mutate_regs(index, dict(regs))
        native_stops.append(dict(token=token, pid=401, tid=401, pc=regs['rip'], signal='SIGTRAP',
            mechanism=p.q1['native_reasons'][index]['mechanism'], trap=p.q1['native_reasons'][index]['trap'],
            register_read='PTRACE_GETREGSET', source='independent-native-stop-capture'))
        chunks.append(Chunk('commands', mi_command(token, command)))
        chunks.append(Chunk('stdout', f'{token}^running\n'.encode()))
        chunks.append(Chunk('stdout', ('*running,thread-id="all"\n*stopped,reason=' + _mi(reason) +
            ',thread-id="401",stopped-threads="all",frame=' + _mi({'addr': hex(regs['rip'])}) + '\n').encode()))
        token += 1
        names = list(regs)
        chunks += [Chunk('commands', mi_command(token, '-data-list-register-names')),
            Chunk('stdout', (f'{token}^done,register-names=' + _mi(names) + '\n').encode())]
        token += 1
        chunks += [Chunk('commands', mi_command(token, '-data-list-register-values x')),
            Chunk('stdout', (f'{token}^done,register-values=' + _mi([dict(number=str(i), value=hex(regs[n])) for i, n in enumerate(names)]) + '\n').encode())]
        token += 1
        for read in mem.reads():
            chunks += [Chunk('commands', mi_command(token, f'-data-read-memory-bytes 0x{read.address:x} {read.requested}')),
                Chunk('stdout', (f'{token}^done,memory=' + _mi([dict(begin=hex(read.address), offset='0x0',
                    end=hex(read.address + read.requested), contents=read.data.hex())]) + '\n').encode())]
            token += 1
    return Observation(tuple(chunks), dict(attempt_id=x, expectation_sha256=digest(canonical(e)), attempted_sha256=attempted,
        frame_count=1, gate='released-once-after-fsync'), copy.deepcopy(capture().completion), b'#\n',
        copy.deepcopy(p.protected), tuple(text_maps(make_text_captures(
            parse(p.artifacts['qualification'])['text_ranges'],
            {c.role: c.raw for c in p.text_captures}, ('caller', 'receiver')), epoch) for epoch in ('caller', 'receiver')),
        native_stops=tuple(native_stops), text_captures=make_text_captures(
            parse(p.artifacts['qualification'])['text_ranges'],
            {c.role: c.raw for c in p.text_captures}, ('caller', 'receiver')))


def freeze(store, e, p):
    store.freeze(e, qualification_material(p))


def make_text_captures(ranges, raw_text, epochs):
    return tuple(TextCapture(epoch, r['role'], dict(start=r['address'], end=r['address'] + r['length'],
        file_offset=r['file_offset'], device=1, inode=1 + i, handle='synthetic-open-' + r['role'],
        load_bias=r['load_bias'], pid=401, tid=401, source='independent-supervisor-unmasked-read',
        image_sha256=r['image_sha256']), raw_text[r['role']])
        for epoch in epochs for i, r in enumerate(ranges)
        if r['role'] in (('launcher', 'loader') if epoch == 'launcher' else ('executable', 'loader')))


def append_stop(chunks, token, command, reason, regs, reads):
    chunks += [Chunk('commands', mi_command(token, command)),
        Chunk('stdout', f'{token}^running\n'.encode()),
        Chunk('stdout', ('*running,thread-id="all"\n*stopped,reason=' + _mi(reason) +
            ',thread-id="401",stopped-threads="all",frame=' + _mi({'addr': hex(regs['rip'])}) + '\n').encode())]
    token += 1
    names = list(regs)
    chunks += [Chunk('commands', mi_command(token, '-data-list-register-names')),
        Chunk('stdout', (f'{token}^done,register-names=' + _mi(names) + '\n').encode())]
    token += 1
    chunks += [Chunk('commands', mi_command(token, '-data-list-register-values x')),
        Chunk('stdout', (f'{token}^done,register-values=' + _mi([dict(number=str(i), value=hex(regs[n])) for i, n in enumerate(names)]) + '\n').encode())]
    token += 1
    for read in reads:
        chunks += [Chunk('commands', mi_command(token, f'-data-read-memory-bytes 0x{read.address:x} {read.requested}')),
            Chunk('stdout', (f'{token}^done,memory=' + _mi([dict(begin=hex(read.address), offset='0x0',
                end=hex(read.address + read.requested), contents=read.data.hex())]) + '\n').encode())]
        token += 1
    return token
