"""Synthetic abc-only consumption evidence. No payload compilation or execution.

Trusted bootstrap supplies reviewed artifact pins. This is not a Python sandbox,
a runtime lock or a real compiler qualification. No scientific modules are loaded.
"""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

F = 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
M = '4a9ebe2c4e275600d9a6c7864bb14c3d5a4c0b6a7c8bbf88193fc48f76affce0'
S = '0ae1c30f2568188390fe05d092609eb122f3bee16c48f41fae9fe3f08e6ba432'
PROFILE = 'ns001.h2a2.compile-input-surrogate.v1'
ENTRY = 'e0.h2.consumption_boundary.receive'
SPEC = '7757f0d7fb8c8f27d2c7516e68c065ea4313b3fd8f013f6674a1e2c5f81799b6'
PARAMS = dict(filename='<ns001-h2a2-input-v1>', mode='exec', flags=0,
              dont_inherit=True, optimize=0)
Q = fcntl.F_SEAL_WRITE | fcntl.F_SEAL_GROW | fcntl.F_SEAL_SHRINK | fcntl.F_SEAL_SEAL
CODES = ('RECORD_INVALID EXPECTATION_INVALID WRONG_PROTECTED_OBJECT INPUT_IO '
         'INPUT_TYPE INPUT_TRUNCATED INPUT_APPENDED INPUT_ALTERED PROFILE_UNQUALIFIED '
         'WRONG_LOADER SOURCE_REDIRECTION WRONG_ENTRYPOINT OBSERVER_NOT_ARMED '
         'PATHNAME_REOPEN OBJECT_SUBSTITUTION INVOCATION_COUNT OBSERVATION_MISSING '
         'ATTEMPT_INCOMPLETE').split()


class Stop(Exception):
    """No dispatch/retry is permitted after a custody or persistence failure."""


class Refuse(Exception):
    pass


def H(raw):
    return hashlib.sha256(raw).hexdigest()


def C(value):
    def check(v):
        if type(v) is str:
            if any(ord(c) < 32 or ord(c) > 126 for c in v):
                raise ValueError('ASCII printable strings required')
        elif type(v) is dict:
            for k, x in v.items():
                if type(k) is not str:
                    raise ValueError('key type')
                check(k)
                check(x)
        elif type(v) is list:
            for x in v:
                check(x)
        elif v is not None and type(v) not in (bool, int):
            raise ValueError('value type')
    check(value)
    return (json.dumps(value, sort_keys=True, separators=(',', ':'),
                       ensure_ascii=True, allow_nan=False) + '\n').encode('ascii')


def parse(raw):
    def pairs(items):
        result = {}
        for k, v in items:
            if k in result:
                raise ValueError('duplicate key')
            result[k] = v
        return result
    value = json.loads(raw, object_pairs_hook=pairs)
    if C(value) != raw:
        raise ValueError('noncanonical')
    return value


def codes(items):
    if not set(items) <= set(CODES):
        raise ValueError('unknown code')
    return sorted(set(items), key=CODES.index)


def receive(source, filename, mode, flags, dont_inherit, optimize, /):
    if (type(source) is not bytes or source != b'abc' or
            type(filename) is not str or filename != '<ns001-h2a2-input-v1>' or
            type(mode) is not str or mode != 'exec' or type(flags) is not int or flags != 0 or
            type(dont_inherit) is not bool or dont_inherit is not True or
            type(optimize) is not int or optimize != 0):
        raise Refuse('invalid surrogate arguments')
    return ('surrogate_received', 3, F)


RECEIVER = receive
RECEIVER_CODE = receive.__code__


def expectation(consumer, observer, harness):
    return dict(schema='ns001.h2a2.surrogate-expectation.v1', spec_sha256=SPEC,
                consumer_sha256=consumer, observer_sha256=observer, harness_sha256=harness,
                entrypoint=ENTRY, interface='bytes-six-positional.v1', profile=PROFILE,
                input_length=3, input_sha256=F, manifest_sha256=M, root_sha256=S)


def request(e, case='P01'):
    return dict(expectation_sha256=H(C(e)), profile=PROFILE, entrypoint=ENTRY,
                source_channel='protected_bytes', source_environment={},
                cwd_policy='exclusive-synthetic', parameters=PARAMS.copy(), case_id=case)


def valid_request(raw, e):
    r = parse(raw)
    if type(r) is not dict or set(r) != set(request(e)):
        raise ValueError('request fields')
    for k in ('expectation_sha256', 'profile', 'entrypoint', 'source_channel', 'cwd_policy', 'case_id'):
        if type(r[k]) is not str:
            raise ValueError('request type')
    if r['expectation_sha256'] != H(C(e)) or not re.fullmatch(r'(P01|N(?:0[1-9]|1[0-9]|20))(\.[1-9][0-9]*)?', r['case_id']):
        raise ValueError('expectation/case')
    env = r['source_environment']
    if type(env) is not dict or any(type(v) is not str for v in env.values()):
        raise ValueError('environment')
    p = r['parameters']
    if type(p) is not dict or set(p) != set(PARAMS) or any(type(p[k]) is not type(v) for k, v in PARAMS.items()):
        raise ValueError('parameters')
    return r


def sync_dir(path):
    fd = os.open(path, os.O_DIRECTORY | os.O_RDONLY | os.O_CLOEXEC)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def persist(path, raw, append=False):
    fd = os.open(path, os.O_WRONLY | os.O_CLOEXEC | os.O_CREAT |
                 (os.O_APPEND if append else os.O_EXCL), 0o600)
    try:
        if os.write(fd, raw) != len(raw):
            raise Stop('incomplete evidence write')
        os.fsync(fd)
    finally:
        os.close(fd)
    sync_dir(Path(path).parent)


class Store:
    """Single owner, retained monotonic reservations. No automatic cleanup."""
    def __init__(self, path, namespace, e):
        self.path = Path(path)
        self.lock = None
        try:
            if type(namespace) is not str or re.fullmatch('[0-9a-f]{64}', namespace) is None:
                raise Stop('namespace')
            if (type(e) is not dict or any(not typed(e[k], 'h') for k in
                    ('consumer_sha256', 'observer_sha256', 'harness_sha256')) or
                    e != expectation(e['consumer_sha256'], e['observer_sha256'], e['harness_sha256'])):
                raise Stop('invalid expectation')
            self.namespace, self.e = namespace, parse(C(e))
            self.metadata = C(dict(schema='ns001.h2a2.store.v1', namespace=namespace))
            self.expected_bytes = C(e)
            self.pin = self.path / (H(self.expected_bytes) + '.json')
            try:
                self.path.mkdir()
                fresh = True
            except FileExistsError:
                fresh = False
            if self.path.is_symlink() or not self.path.is_dir():
                raise Stop('invalid store root')
            self.root_key = self._key(self.path.stat())
            # Existing directories, even empty ones, are retained custody roots.
            # Only exclusive creation above authorizes initial metadata writes.
            flags = os.O_RDWR | os.O_CLOEXEC | os.O_NOFOLLOW
            self.lock = os.open(self.path / 'lock', flags | (os.O_CREAT | os.O_EXCL if fresh else 0), 0o600)
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.lock_key = self._key(os.fstat(self.lock))
            if fresh:
                persist(self.path / 'store.json', self.metadata)
                persist(self.pin, self.expected_bytes)
                sync_dir(self.path.parent)
            self.validate_custody()
            self.scan()
        except (OSError, ValueError, TypeError, KeyError, Stop):
            if self.lock is not None:
                os.close(self.lock)
                self.lock = None
            raise Stop('store custody unavailable or conflicting') from None

    @staticmethod
    def _key(info):
        return info.st_dev, info.st_ino

    def validate_custody(self):
        """Recheck retained evidence; never repair it from cached/caller values."""
        try:
            if self.lock is None or self.path.is_symlink() or self._key(self.path.stat()) != self.root_key:
                raise Stop('store unavailable')
            for p in (self.path / 'lock', self.path / 'store.json', self.pin):
                if not stat.S_ISREG(p.lstat().st_mode):
                    raise Stop('custody file type')
            if self._key((self.path / 'lock').stat()) != self.lock_key:
                raise Stop('lock replaced')
            if ((self.path / 'store.json').read_bytes() != self.metadata or
                    self.pin.read_bytes() != self.expected_bytes or C(self.e) != self.expected_bytes):
                raise Stop('custody mismatch')
        except (OSError, ValueError, TypeError):
            raise Stop('store custody unavailable or conflicting') from None

    def close(self):
        if self.lock is not None:
            fcntl.flock(self.lock, fcntl.LOCK_UN)
            os.close(self.lock)
            self.lock = None

    def scan(self):
        ordinals = []
        for p in self.path.iterdir():
            if p.name in ('lock', 'store.json') or re.fullmatch(r'[0-9a-f]{64}\.json', p.name):
                continue
            if not re.fullmatch('[1-9][0-9]*', p.name) or not p.is_dir() or p.is_symlink():
                raise Stop('unrecognized store entry')
            ordinals.append(int(p.name))
        if sorted(ordinals) != list(range(1, max(ordinals, default=0) + 1)):
            raise Stop('reservation gap')
        return sorted(ordinals)

    def reserve(self):
        self.validate_custody()
        ids = self.scan()
        for n in ids:
            self.recover(n)
        n = max(ids, default=0) + 1
        p = self.path / str(n)
        p.mkdir()
        sync_dir(self.path)
        return Attempt(self, n)

    def recover(self, n):
        return recover(self, n)


class Attempt:
    def __init__(self, store, ordinal):
        self.store, self.ordinal = store, ordinal
        self.path = store.path / str(ordinal)
        self.id = store.namespace + ':' + str(ordinal)
        self.events = []

    def require_writable(self):
        self.store.validate_custody()
        recovery = self.path / 'recovery.json'
        if recovery.exists() or recovery.is_symlink() or any(self.path.glob('recovery*.partial')):
            raise Stop('recovered or interrupted-recovery attempt is terminal')
        raw = read_optional(self.path / 'events.jsonl') or b''
        if raw != b''.join(C(event) for event in self.events):
            raise Stop('stale or interrupted attempt writer')
        if self.events and self.events[-1]['state'] in ('ACCEPTED', 'REFUSED'):
            raise Stop('terminal attempt')

    def register(self, raw):
        self.require_writable()
        persist(self.path / 'request.json', raw)
        persist(self.path / 'registration.json', C(dict(schema='ns001.h2a2.registration.v1',
                attempt_id=self.id, expectation_sha256=H(C(self.store.e)), request_sha256=H(raw))))

    def event(self, state, witness=None, reasons=(), entered=None):
        self.require_writable()
        reasons = codes(reasons)
        if self.events and self.events[-1]['state'] in ('ACCEPTED', 'REFUSED'):
            raise Stop('terminal attempt')
        previous = self.events[-1]['state'] if self.events else None
        if state not in {None: ('PREPARED', 'REFUSED'), 'PREPARED': ('ATTEMPTED', 'REFUSED'),
                         'ATTEMPTED': ('ACCEPTED', 'REFUSED')}[previous]:
            raise Stop('transition')
        wh = None
        if state in ('ACCEPTED', 'REFUSED'):
            if witness is None:
                raise Stop('witness missing')
            persist(self.path / 'witness.json', C(witness))
            wh = H(C(witness))
        value = dict(schema='ns001.h2a2.consumption-event.v1', attempt_id=self.id,
                     sequence=len(self.events), state=state, primary_code=reasons[0] if reasons else None,
                     diagnostics=reasons[1:], previous_sha256=H(C(self.events[-1])) if self.events else None,
                     witness_sha256=wh, entered=entered)
        persist(self.path / 'events.jsonl', C(value), append=True)
        self.events.append(value)
        return H(C(value))


# Recovery refuses malformed complete records and never invokes a receiver.
EVENT_KEYS = set('schema attempt_id sequence state primary_code diagnostics previous_sha256 witness_sha256 entered'.split())


def read_optional(path):
    return path.read_bytes() if path.exists() else None


def recover(store, n):
    store.validate_custody()
    p, aid = store.path / str(n), store.namespace + ':' + str(n)
    raw = {name: read_optional(p / name) for name in ('registration.json', 'request.json', 'witness.json', 'events.jsonl')}
    journal = raw['events.jsonl'] or b''
    prefix = b''
    events = []
    invalid = False
    registration = None
    if raw['registration.json']:
        try:
            registration = parse(raw['registration.json'])
            if type(registration) is not dict or set(registration) != set('schema attempt_id expectation_sha256 request_sha256'.split()) or registration != dict(
                    schema='ns001.h2a2.registration.v1', attempt_id=aid,
                    expectation_sha256=H(C(store.e)), request_sha256=H(raw['request.json'] or b'')):
                raise ValueError('registration')
        except (ValueError, TypeError, KeyError, RecursionError):
            invalid = raw['registration.json'].endswith(b'\n')
            registration = None
    witness = None
    if raw['witness.json']:
        try:
            witness = parse(raw['witness.json'])
            validate_witness(witness, aid, store.e)
        except (ValueError, KeyError, TypeError):
            invalid |= raw['witness.json'].endswith(b'\n')
            witness = None
    previous = None
    for line in journal.splitlines(keepends=True):
        if not line.endswith(b'\n'):
            break
        try:
            ev = parse(line)
            if set(ev) != EVENT_KEYS or ev['schema'] != 'ns001.h2a2.consumption-event.v1' or ev['attempt_id'] != aid:
                raise ValueError('event schema')
            if type(ev['sequence']) is not int or ev['sequence'] != len(events) or ev['previous_sha256'] != (H(C(events[-1])) if events else None):
                raise ValueError('event link')
            allowed = {None: ('PREPARED', 'REFUSED'), 'PREPARED': ('ATTEMPTED', 'REFUSED'),
                       'ATTEMPTED': ('ACCEPTED', 'REFUSED')}.get(previous, ())
            if ev['state'] not in allowed or ev['entered'] is not None and type(ev['entered']) is not bool:
                raise ValueError('state')
            reasons = ([ev['primary_code']] if ev['primary_code'] else []) + ev['diagnostics']
            if reasons != codes(reasons):
                raise ValueError('codes')
            if ev['state'] in ('PREPARED', 'ATTEMPTED'):
                if reasons or ev['witness_sha256'] is not None or ev['entered'] is not (False if ev['state'] == 'PREPARED' else None):
                    raise ValueError('nonterminal')
            else:
                if witness is None or ev['witness_sha256'] != H(raw['witness.json']):
                    raise ValueError('witness binding')
                observed = witness_codes(witness, attempted=previous == 'ATTEMPTED')
                if previous == 'ATTEMPTED' and not dispatch_bound(witness, events[-1]):
                    observed = codes(observed + ['OBSERVATION_MISSING'])
                if ev['state'] == 'ACCEPTED':
                    if reasons or observed or ev['entered'] is not True:
                        raise ValueError('unproved ACCEPT')
                elif not reasons or reasons[0] == 'ATTEMPT_INCOMPLETE' or reasons != observed:
                    raise ValueError('refusal')
            events.append(ev)
            prefix += line
            previous = ev['state']
        except (ValueError, KeyError, TypeError):
            invalid = True
            break
    if not invalid and registration is not None and len(prefix) == len(journal) and events and events[-1]['state'] in ('ACCEPTED', 'REFUSED'):
        if (p / 'recovery.json').exists():
            raise Stop('terminal recovery conflict')
        return events[-1]
    supported = witness['violations'] if witness else []
    primary = 'RECORD_INVALID' if invalid else 'ATTEMPT_INCOMPLETE'
    entries = [x for x in witness['observations'] if x['kind'] == 'entry'] if witness else None
    result = dict(schema='ns001.h2a2.consumption-recovery.v1', attempt_id=aid, state='ABORTED',
                  primary_code=primary, diagnostics=[x for x in codes(supported) if x != primary],
                  registration_sha256=H(raw['registration.json']) if raw['registration.json'] is not None else None,
                  request_sha256=H(raw['request.json']) if raw['request.json'] is not None else None,
                  witness_sha256=H(raw['witness.json']) if raw['witness.json'] is not None else None,
                  journal_sha256=H(journal) if raw['events.jsonl'] is not None else None,
                  journal_length=len(journal), valid_prefix_sha256=H(prefix), valid_prefix_length=len(prefix),
                  last_valid_sequence=events[-1]['sequence'] if events else None,
                  entered=bool(entries) if entries is not None else None)
    expected = C(result)
    final = p / 'recovery.json'
    if final.exists():
        if final.read_bytes() != expected:
            raise Stop('recovery conflict')
        return result
    for partial in p.glob('recovery*.partial'):
        if not expected.startswith(partial.read_bytes()):
            raise Stop('invalid recovery prefix')
    serial = 1
    while (p / ('recovery' + str(serial) + '.partial')).exists():
        serial += 1
    tmp = p / ('recovery' + str(serial) + '.partial')
    persist(tmp, expected)
    os.rename(tmp, final)
    sync_dir(p)
    return result


OBS_FIELDS = {
    'protected': dict(valid='b', initial='b', association='b', seals_exact='b', length='?i', sha256='?h'),
    'derived': dict(type='s', length='?i', sha256='?h', from_retained_A='b', reference_retained='b'),
    'qualification': dict(profile_allowed='b', capability_qualified='b', consumer_sha256='?h', artifact_match='b',
                          callable_match='b', entrypoint='?s', parameters_match='b', source_selection_valid='b'),
    'armed': dict(sentinel_active='b', entry_hook_active='b', guard_active='b', consumer_bound='b'),
    'dispatch': dict(attempted_event_sha256='h', persisted='b'),
    'entry': dict(consumer_match='b', entrypoint='s', source_type='s', length='?i', sha256='?h',
                  same_B='b', same_A='b', independent_A_equal='?b', parameters_match='b', parameters='?p',
                  after_dispatch='b', hook_armed='b'),
    'guard': dict(operation='s', denied='b'),
    'return': dict(matches_entry='b', result='s'),
    'end': dict(entry_count='i', observer_entry_count='i', same_A='?b', seals_exact='?b', no_reopen='b',
                guard_coverage='b', outcome='s')}


def typed(value, kind):
    if kind.startswith('?'):
        return value is None or typed(value, kind[1:])
    if kind == 'p':
        return type(value) is dict and set(value) == set(PARAMS) and all(type(value[k]) is type(v) for k, v in PARAMS.items())
    if kind == 'h':
        return type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None
    return (type(value) is {'b': bool, 's': str, 'i': int}[kind]
            and (kind != 'i' or value >= 0))


def validate_witness(w, aid, e):
    if type(w) is not dict or set(w) != set('schema attempt_id expectation_sha256 consumer_sha256 observer_sha256 harness_sha256 entrypoint observations violations'.split()):
        raise ValueError('witness schema')
    if w['schema'] != 'ns001.h2a2.consumption-witness.v1' or w['attempt_id'] != aid or w['expectation_sha256'] != H(C(e)):
        raise ValueError('witness identity')
    if any(w[k] != e[k] for k in ('consumer_sha256', 'observer_sha256', 'harness_sha256')):
        raise ValueError('witness pins')
    if w['entrypoint'] is not None and type(w['entrypoint']) is not str:
        raise ValueError('witness entrypoint')
    if type(w['observations']) is not list or type(w['violations']) is not list or w['violations'] != codes(w['violations']):
        raise ValueError('witness lists')
    for i, o in enumerate(w['observations']):
        if type(o) is not dict or set(o) != {'index', 'kind', 'data'} or type(o['index']) is not int or o['index'] != i or o['kind'] not in OBS_FIELDS:
            raise ValueError('observation')
        d, shape = o['data'], OBS_FIELDS[o['kind']]
        if type(d) is not dict or set(d) != set(shape) or any(not typed(d[k], t) for k, t in shape.items()):
            raise ValueError('observation data')
        allowed = {'type': ('bytes', 'nonbytes'), 'source_type': ('bytes', 'nonbytes'),
                   'operation': ('payload_open', 'payload_reopen', 'filesystem_fallback', 'source_redirect'),
                   'result': ('fixed_tuple', 'other', 'aborted'), 'outcome': ('returned', 'precondition_refused', 'aborted')}
        if any(k in d and d[k] not in values for k, values in allowed.items()):
            raise ValueError('observation enum')


def witness_codes(w, attempted):
    reasons = list(w['violations'])
    obs = w['observations']
    ends = [o['data'] for o in obs if o['kind'] == 'end']
    if len(ends) != 1 or not obs or obs[-1]['kind'] != 'end':
        reasons.append('OBSERVATION_MISSING')
    for o in obs:
        d, k = o['data'], o['kind']
        if k == 'guard':
            reasons.append('SOURCE_REDIRECTION' if d['operation'] == 'source_redirect' else 'PATHNAME_REOPEN')
        if k == 'entry':
            if not d['hook_armed'] or not d['after_dispatch']:
                reasons.append('OBSERVER_NOT_ARMED')
            if not d['consumer_match']:
                reasons.append('WRONG_LOADER')
            if not d['parameters_match'] or d['parameters'] != PARAMS:
                reasons.append('WRONG_ENTRYPOINT')
            if not d['same_B'] or not d['same_A']:
                reasons.append('OBJECT_SUBSTITUTION')
            if d['independent_A_equal'] is not True:
                reasons.append('OBSERVATION_MISSING')
    if attempted and ends:
        end = ends[0]
        if end['entry_count'] != 1:
            reasons.append('INVOCATION_COUNT')
        if end['entry_count'] != end['observer_entry_count']:
            reasons.append('OBSERVATION_MISSING')
        if not end['same_A']:
            reasons.append('OBJECT_SUBSTITUTION')
    # ACCEPT requires all positive observations, not merely absence of reported faults.
    if attempted and not reasons:
        expected = ['protected', 'derived', 'qualification', 'armed', 'dispatch', 'entry', 'protected', 'return', 'end']
        if [x['kind'] for x in obs] != expected:
            reasons.append('OBSERVATION_MISSING')
        else:
            p, b, q, a, dispatch, entry, p2, ret, end = [o['data'] for o in obs]
            truth = [p['valid'], p['initial'], p['association'], p['seals_exact'], b['from_retained_A'],
                     b['reference_retained'], q['profile_allowed'], q['capability_qualified'], q['artifact_match'],
                     q['callable_match'], q['parameters_match'], q['source_selection_valid'], *a.values(),
                     dispatch['persisted'], entry['same_B'], entry['same_A'], entry['independent_A_equal'],
                     p2['valid'], p2['association'], p2['seals_exact'], ret['matches_entry'], end['same_A'],
                     end['seals_exact'], end['no_reopen'], end['guard_coverage']]
            exact = all(d['length'] == 3 and d['sha256'] == F for d in (p, b, entry, p2))
            if (not all(v is True for v in truth) or not exact or p2['initial'] or b['type'] != 'bytes'
                    or entry['source_type'] != 'bytes' or ret['result'] != 'fixed_tuple' or end['outcome'] != 'returned'):
                reasons.append('OBSERVATION_MISSING')
    return codes(reasons)


class Protected:
    """Live capability from witnessed creation; only the trusted harness constructs it."""
    def __init__(self, payload):
        if payload != b'abc' or type(payload) is not bytes:
            raise Refuse('WRONG_PROTECTED_OBJECT')
        self.fd = os.memfd_create('ns001-h2a2-handoff', os.MFD_ALLOW_SEALING | os.MFD_CLOEXEC)
        self.key = None
        try:
            s = os.fstat(self.fd)
            if not stat.S_ISREG(s.st_mode) or s.st_size != 0 or fcntl.fcntl(self.fd, fcntl.F_GET_SEALS) != 0:
                raise Refuse('WRONG_PROTECTED_OBJECT')
            if os.pwrite(self.fd, payload, 0) != 3 or os.pread(self.fd, 4, 0) != payload:
                raise Refuse('WRONG_PROTECTED_OBJECT')
            fcntl.fcntl(self.fd, fcntl.F_ADD_SEALS, Q)
            self.key = (s.st_dev, s.st_ino)
            if not self.measure(self.fd, True)[0]['valid']:
                raise Refuse('WRONG_PROTECTED_OBJECT')
        except BaseException:
            os.close(self.fd)
            raise

    def measure(self, fd, initial=False):
        d = dict(valid=False, initial=initial, association=False, seals_exact=False, length=None, sha256=None)
        raw = None
        try:
            info = os.fstat(fd)
            raw = os.pread(fd, 4, 0)
            d.update(association=(info.st_dev, info.st_ino) == self.key,
                     seals_exact=fcntl.fcntl(fd, fcntl.F_GET_SEALS) == Q,
                     length=len(raw), sha256=H(raw))
            d['valid'] = (d['association'] and d['seals_exact'] and info.st_size == len(raw) == 3
                          and raw == b'abc' and stat.S_ISREG(info.st_mode)
                          and bool(fcntl.fcntl(fd, fcntl.F_GETFD) & fcntl.FD_CLOEXEC))
        except OSError:
            pass
        return d, raw

    def close(self):
        os.close(self.fd)


class Monitor:
    """Lifetime sentinel; separate state from receiver and per-attempt witness."""
    def __init__(self):
        self.witness = None
        self.entries = 0
        self.fn = self.profile

    def install(self):
        if sys.getprofile() is not None:
            raise Stop('profiler occupied')
        sys.setprofile(self.fn)

    def close(self):
        if sys.getprofile() is not self.fn:
            raise Stop('profiler replaced')
        sys.setprofile(None)

    def profile(self, frame, event, arg):
        if frame.f_code is not RECEIVER_CODE:
            return
        if event == 'call':
            self.entries += 1
            if self.witness is None:
                raise Stop('unregistered receiver entry')
            self.witness.entry(frame)
        elif event == 'return' and self.witness is not None:
            self.witness.returned(frame, arg)


class Witness:
    def __init__(self, attempt, monitor):
        self.attempt, self.monitor = attempt, monitor
        e = attempt.store.e
        self.record = dict(schema='ns001.h2a2.consumption-witness.v1', attempt_id=attempt.id,
                           expectation_sha256=H(C(e)), consumer_sha256=e['consumer_sha256'],
                           observer_sha256=e['observer_sha256'], harness_sha256=e['harness_sha256'],
                           entrypoint=None, observations=[], violations=[])
        self.protected = None
        self.a = None
        self.b = None
        self.read_buffer = None
        self.armed = False
        self.guard_active = False
        self.dispatch = None
        self.frame = None
        self.start_count = monitor.entries
        self.calls = 0
        self.guarded = False
        monitor.witness = self

    def add(self, kind, data):
        self.record['observations'].append(dict(index=len(self.record['observations']), kind=kind, data=data))

    def fail(self, code):
        self.record['violations'] = codes(self.record['violations'] + [code])

    def guard(self, operation):
        if operation not in ('payload_open', 'payload_reopen', 'filesystem_fallback', 'source_redirect'):
            raise Stop('unqualified operation')
        self.guarded = True
        self.add('guard', dict(operation=operation, denied=True))
        self.fail('SOURCE_REDIRECTION' if operation == 'source_redirect' else 'PATHNAME_REOPEN')
        # A request is recorded and refused; no open or fallback is performed.
        return False

    def entry(self, frame):
        self.frame = frame
        self.calls += int(self.armed)
        args = frame.f_locals
        src = args['source']
        p = {k: args[k] for k in PARAMS}
        if not typed(p, 'p') or any(type(v) is str and any(ord(c) < 32 or ord(c) > 126 for c in v) for v in p.values()):
            p = None
        if self.protected is not None:
            facts, independent = self.protected.measure(self.a)
        else:
            facts, independent = dict(valid=False, initial=False, association=False, seals_exact=False, length=None, sha256=None), None
        self.record['entrypoint'] = ENTRY
        self.add('entry', dict(consumer_match=frame.f_code is RECEIVER_CODE and receive is RECEIVER,
                              entrypoint=ENTRY, source_type='bytes' if type(src) is bytes else 'nonbytes',
                              length=len(src) if type(src) is bytes else None,
                              sha256=H(src) if type(src) is bytes else None,
                              same_B=src is self.b, same_A=facts['association'],
                              independent_A_equal=(src == independent) if independent is not None else None,
                              parameters_match=p == PARAMS, parameters=p, after_dispatch=self.dispatch is not None,
                              hook_armed=self.armed))
        self.add('protected', facts)

    def returned(self, frame, value):
        result = 'fixed_tuple' if type(value) is tuple and value == ('surrogate_received', 3, F) else ('aborted' if value is None else 'other')
        self.add('return', dict(matches_entry=frame is self.frame, result=result))

    def end(self, outcome):
        facts = self.protected.measure(self.a)[0] if self.protected is not None else None
        self.add('end', dict(entry_count=self.monitor.entries - self.start_count,
                            observer_entry_count=self.calls, same_A=facts['association'] if facts else None,
                            seals_exact=facts['seals_exact'] if facts else None, no_reopen=not self.guarded,
                            guard_coverage=self.guard_active, outcome=outcome))


def prepare(attempt, witness, protected, supplied_fd, raw_request, consumer_pin):
    """Preparation stops at its first measured failure. No receiver dispatch here."""
    try:
        try:
            r = valid_request(raw_request, attempt.store.e)
        except (ValueError, TypeError):
            raise Refuse('EXPECTATION_INVALID') from None
        witness.protected, witness.a = protected, supplied_fd
        facts, _ = protected.measure(supplied_fd, initial=True)
        witness.add('protected', facts)
        if not facts['valid']:
            raise Refuse('WRONG_PROTECTED_OBJECT')
        before = os.fstat(supplied_fd).st_size
        try:
            b = os.pread(supplied_fd, 4, 0)
        except OSError:
            raise Refuse('INPUT_IO') from None
        if type(b) is bytes and len(b) < min(before, 4):
            raise Refuse('INPUT_IO')
        witness.read_buffer = b
        return r, b
    except Refuse as exc:
        witness.fail(str(exc))
        return None, None


def bind_derivative(w, b):
    w.add('derived', dict(type='bytes' if type(b) is bytes else 'nonbytes', length=len(b) if type(b) is bytes else None,
                          sha256=H(b) if type(b) is bytes else None,
                          from_retained_A=b is w.read_buffer, reference_retained=type(b) is bytes))
    failure = ('INPUT_TYPE' if type(b) is not bytes else 'INPUT_TRUNCATED' if len(b) < 3 else
               'INPUT_APPENDED' if len(b) > 3 else 'INPUT_ALTERED' if b != b'abc' else None)
    if failure:
        w.fail(failure)
        return False
    if not w.protected.measure(w.a)[0]['valid']:
        w.fail('OBJECT_SUBSTITUTION')
        return False
    w.b = b
    return True


def qualify(w, r, observed_pin, selected=RECEIVER):
    e = w.attempt.store.e
    d = dict(profile_allowed=r['profile'] == PROFILE, capability_qualified=True,
             consumer_sha256=observed_pin, artifact_match=observed_pin == e['consumer_sha256'],
             callable_match=selected is RECEIVER and selected.__code__ is RECEIVER_CODE and receive is RECEIVER,
             entrypoint=r['entrypoint'], parameters_match=r['parameters'] == PARAMS and r['entrypoint'] == ENTRY,
             source_selection_valid=r['source_channel'] == 'protected_bytes' and r['source_environment'] == {} and r['cwd_policy'] == 'exclusive-synthetic')
    w.add('qualification', d)
    failure = ('PROFILE_UNQUALIFIED' if not d['profile_allowed'] else 'WRONG_LOADER' if not d['artifact_match'] or not d['callable_match'] else
               'SOURCE_REDIRECTION' if not d['source_selection_valid'] else 'WRONG_ENTRYPOINT' if not d['parameters_match'] else None)
    if failure:
        w.fail(failure)
        return False
    w.armed = w.guard_active = True
    w.add('armed', dict(sentinel_active=sys.getprofile() is w.monitor.fn, entry_hook_active=True,
                        guard_active=True, consumer_bound=selected is RECEIVER))
    if sys.getprofile() is not w.monitor.fn:
        w.fail('OBSERVER_NOT_ARMED')
        return False
    return True


def dispatch(attempt, w):
    attempt.event('PREPARED', entered=False)
    w.dispatch = attempt.event('ATTEMPTED')
    w.add('dispatch', dict(attempted_event_sha256=w.dispatch, persisted=True))


def dispatch_bound(witness, event):
    values = [o['data'] for o in witness['observations'] if o['kind'] == 'dispatch']
    return (len(values) == 1 and values[0]['persisted'] is True
            and values[0]['attempted_event_sha256'] == H(C(event)))


def invoke(w, source):
    """Fixed dispatch only; never accepts an alternate callable or source path."""
    w.attempt.require_writable()
    if receive is not RECEIVER or receive.__code__ is not RECEIVER_CODE:
        w.fail('WRONG_LOADER')
        return
    if not w.armed or sys.getprofile() is not w.monitor.fn or w.dispatch is None:
        w.fail('OBSERVER_NOT_ARMED')
        return
    receive(source, '<ns001-h2a2-input-v1>', 'exec', 0, True, 0)


def finish(attempt, w, attempted):
    w.end('returned' if attempted else 'precondition_refused')
    validate_witness(w.record, attempt.id, attempt.store.e)
    reasons = witness_codes(w.record, attempted)
    if attempted and not dispatch_bound(w.record, attempt.events[-1]):
        reasons = codes(reasons + ['OBSERVATION_MISSING'])
    w.record['violations'] = reasons
    event = attempt.event('REFUSED' if reasons else 'ACCEPTED', w.record, reasons,
                          entered=w.monitor.entries > w.start_count)
    return attempt.events[-1]
