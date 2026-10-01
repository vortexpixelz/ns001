"""Frozen real-receipt policy. Pure plans/comparators; no process control API."""
import hashlib
import json
import re

PROFILE = 'ns001.h2a2.real-cpython-input-receipt.v1'
FIXTURE = b'#\n'
DIGEST = '32c4858e22cc2c967b42150fa550562a2c839c2cebcaab91cabdf6f4da020022'
PARAMETERS = dict(filename='<ns001-h2a2-real-input-v1>', mode='exec', flags=0,
                  dont_inherit=True, optimize=0, _feature_version=-1)
CODES = ('RECORD_INVALID EXPECTATION_INVALID WRONG_PROTECTED_OBJECT INPUT_IO '
         'INPUT_TYPE INPUT_TRUNCATED INPUT_APPENDED INPUT_ALTERED PROFILE_UNQUALIFIED '
         'ENGINE_UNQUALIFIED WRONG_COMPILE_CALLABLE SOURCE_REDIRECTION WRONG_ENTRYPOINT '
         'OBSERVER_UNQUALIFIED OBSERVER_NOT_ARMED PATHNAME_REOPEN OBJECT_SUBSTITUTION '
         'INVOCATION_COUNT OBSERVATION_MISSING EXECUTION_PROHIBITED ATTEMPT_INCOMPLETE').split()
SCHEMA = 'ns001.h2a2.real-input.'


class Invalid(ValueError):
    """Unavailable/invalid evidence; never a positive fact."""


def digest(raw):
    if type(raw) is not bytes:
        raise Invalid('bytes required')
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    def check(v):
        if type(v) is str:
            if any(not 32 <= ord(c) <= 126 for c in v):
                raise Invalid('printable ASCII required')
        elif type(v) is dict:
            for k, x in v.items():
                if type(k) is not str:
                    raise Invalid('string key required')
                check(k)
                check(x)
        elif type(v) is list:
            for x in v:
                check(x)
        elif v is not None and type(v) not in (int, bool):
            raise Invalid('unsupported canonical type')
    check(value)
    return (json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True,
                       allow_nan=False) + '\n').encode('ascii')


def parse(raw):
    if type(raw) is not bytes or len(raw) > 8 * 1024 * 1024:
        raise Invalid('record bound')
    def pairs(items):
        d = {}
        for k, v in items:
            if k in d:
                raise Invalid('duplicate key')
            d[k] = v
        return d
    try:
        v = json.loads(raw, object_pairs_hook=pairs)
        if canonical(v) != raw:
            raise Invalid('noncanonical bytes')
        return v
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        raise Invalid('invalid canonical record') from exc


def keys(v, names):
    if type(v) is not dict or set(v) != set(names.split()):
        raise Invalid('exact key set required')


def hash_value(v):
    if type(v) is not str or re.fullmatch('[0-9a-f]{64}', v) is None:
        raise Invalid('hash required')


def attempt_id(v):
    if type(v) is not str or re.fullmatch('[0-9a-f]{64}:[1-9][0-9]*', v) is None:
        raise Invalid('attempt ID required')


def ranked(items, recovery=False):
    if any(type(x) is not str or x not in CODES for x in items):
        raise Invalid('unknown refusal')
    if not recovery and 'ATTEMPT_INCOMPLETE' in items:
        raise Invalid('recovery-only code')
    return sorted(set(items), key=CODES.index)


def parameters_match(v):
    return (type(v) is dict and set(v) == set(PARAMETERS) and
            all(type(v[k]) is type(x) and v[k] == x for k, x in PARAMETERS.items()))


# Exact section 6 Q1 initialization, prior to any file/inferior.
Q1 = tuple(('set ' + s) for s in (
    'auto-load off', 'debuginfod enabled off', 'may-insert-breakpoints off',
    'may-write-memory off', 'may-insert-tracepoints off', 'may-insert-fast-tracepoints off',
    'may-call-functions off', 'libthread-db-search-path /dev/null', 'startup-with-shell off',
    'non-stop off', 'displaced-stepping off', 'breakpoint auto-hw off', 'breakpoint pending off',
    'auto-solib-add off', 'stop-on-solib-events 0', 'sysroot /', 'solib-search-path',
    'breakpoint always-inserted on', 'trust-readonly-sections off', 'code-cache off',
    'stack-cache off', 'pagination off', 'debug breakpoint 1', 'debug infrun 1',
    'debug linux-nat 1', 'debug target 1'))
READBACKS = tuple(s.replace('set ', 'show ', 1).removesuffix(' ' + s.split()[-1])
                  for s in Q1 if s != 'set solib-search-path')
# Multiword settings need their complete setting name, without the supplied value.
READBACKS = READBACKS[:16] + ('show solib-search-path',) + READBACKS[16:]
READBACKS += ('show may-stop', 'show may-write-registers', 'show observer')
SITES = (0x69bff0, 0x581feb, 0x4f6102, 0x4f6224, 0x4f6274, 0x4f6299)


def initialization_plan():
    return ('/usr/bin/gdb', '--nx', '--nh', '--interpreter=mi2') + tuple(
        item for command in Q1 for item in ('-iex', command))


def mi_command(token, command):
    if type(token) is not int or not 1 <= token <= 2**31 - 1:
        raise Invalid('MI token')
    if command in ('-exec-step-instruction', '-exec-continue', '-exec-run', '-break-list',
                   '-data-list-register-names', '-data-list-register-values x'):
        pass
    elif command.startswith('-interpreter-exec console '):
        try:
            cli = json.loads(command[len('-interpreter-exec console '):])
        except ValueError as exc:
            raise Invalid('CLI literal') from exc
        if cli not in READBACKS + ('catch exec', 'catch syscall 17',
                                   'maintenance info breakpoints'):
            raise Invalid('CLI denied')
    elif command.startswith('-break-insert -h *'):
        if command not in tuple(f'-break-insert -h *0x{s:x}' for s in SITES):
            raise Invalid('numeric hardware site required')
    elif re.fullmatch(r'-break-delete [1-9][0-9]*', command):
        pass
    elif re.fullmatch(r'-data-read-memory-bytes 0x[0-9a-f]+ [1-9][0-9]*', command):
        address, count = command.split()[-2:]
        if int(count) > 65536 or int(address, 16) + int(count) > 2**64:
            raise Invalid('memory range')
    else:
        raise Invalid('command denied')
    return f'{token}{command}\n'.encode('ascii')


def command_plan(launcher_path):
    """Construct the future initialization/readback/exec/derivation plan only.

    Site handovers, continuing and the paired CALL depend on captured stops;
    this is a vocabulary/phase plan, never an unattended runnable command file.
    """
    if (type(launcher_path) is not str or not launcher_path.startswith('/') or
            any(ord(c) < 32 or ord(c) > 126 for c in launcher_path)):
        raise Invalid('qualified launcher path')
    return dict(startup=list(initialization_plan()),
        environment={'LC_ALL': 'C', 'DEBUGINFOD_URLS': ''},
        readbacks=[mi_command(i + 1, '-interpreter-exec console ' + json.dumps(s)).decode('ascii').rstrip('\n')
                   for i, s in enumerate(READBACKS)],
        launcher_command='-file-exec-and-symbols ' + json.dumps(launcher_path),
        exec_observation='-interpreter-exec console "catch exec"',
        syscall_observation='-interpreter-exec console "catch syscall 17"',
        receiver_site='-break-insert -h *0x69bff0', caller_site='-break-insert -h *0x581feb',
        derivation_sites=[f'-break-insert -h *0x{s:x}' for s in SITES[2:]],
        paired_step='-exec-step-instruction', single_step_count=1,
        hardware_slot_budget=2, software_fallback=False,
        execution_release_requires='durable-ATTEMPTED-and-admission',
        post_entry='remain-stopped-capture-sync-supervisor-kill-confirm-death')


def validate_q1(settings, facts):
    """Already-decoded readbacks plus independently captured admission facts.

    Fact booleans are synthetic/trusted-capture inputs, never measured here.
    Runtime qualification must separately establish their provenance.
    """
    expected = dict(zip(READBACKS[:26], Q1))
    if settings != expected:
        return ['OBSERVER_UNQUALIFIED']
    required = ('before_inferior', 'continuous_policy', 'empty_initial_inventory',
                'stopping_on', 'register_control_on', 'observer_off', 'auto_load_all_off',
                'classic_loader_denied_disabled', 'no_unexpected_internal_sites',
                'no_libthread_db', 'native_exec_event', 'ptrace_syscall_events',
                'in_place_single_call_step', 'receiver_stays_armed',
                'raw_unmasked_text_equal', 'complete_text_ranges', 'two_effective_slots',
                'kernel_programming_witnessed', 'blocked_gate_restop',
                'death_chain_qualified', 'no_software_fallback', 'no_post_entry_resume')
    if set(facts) != set(required) or any(facts[k] is not True for k in required):
        return ['OBSERVER_NOT_ARMED']
    return []


ENGINE = dict(path='/usr/bin/python3.12',
    sha256='e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f',
    package='python3.12-minimal:amd64', version='3.12.3-1ubuntu0.17',
    source='python3.12', source_version='3.12.3-1ubuntu0.17', size=8020928,
    build_id='337d65cf00021797985cc9f77c0cc334a9fbeb38',
    abi='ELF64-LE-x86_64-SystemV-LP64-ET_EXEC-nondebug', bias=0,
    receiver=0x69bff0, receiver_offset=0x29bff0, receiver_hex='f30f1efa',
    caller=0x581feb, caller_hex='ffd0', return_pc=0x581fed,
    method=0xa49ae0, method_flags=0x82, vectorcall=0x581f90,
    compiler_image='executable', needed=['libm.so.6', 'libz.so.1', 'libexpat.so.1', 'libc.so.6'],
    gdb_path='/usr/bin/gdb', gdb_package='gdb:amd64', gdb_version='15.1-1ubuntu1~24.04.1',
    gdb_sha256='3832cc070ae1716e322105d3b39fb398695e5f031c9d39224cf227a8c2b889f6',
    loader_path='/lib64/ld-linux-x86-64.so.2',
    loader_sha256='c20a2dc8917c755f02b94049356320fe1f62ac7d9f8994731f807d9df39302da',
    loader_rendezvous_offset=0x2820,
    packages={k: '3.12.3-1ubuntu0.17' for k in (
        'python3.12', 'libpython3.12-stdlib:amd64', 'libpython3.12t64:amd64')})


def engine_admission(observed, pins, artifacts):
    # Strict type comparison prevents True masquerading as integer one.
    if canonical(observed) != canonical(ENGINE):
        return ['ENGINE_UNQUALIFIED']
    roles = {'controller', 'launcher_gdb', 'launcher_cpython', 'bootstrap', 'mi_parser',
             'decoder', 'hash_tool', 'guard', 'qualification', 'q1', 'provenance'}
    if type(pins) is not dict or set(pins) != roles or set(artifacts) != roles:
        return ['ENGINE_UNQUALIFIED']
    try:
        for role in roles:
            hash_value(pins[role])
            if not artifacts[role] or digest(artifacts[role]) != pins[role]:
                return ['ENGINE_UNQUALIFIED']
    except (ValueError, TypeError):
        return ['ENGINE_UNQUALIFIED']
    return []
