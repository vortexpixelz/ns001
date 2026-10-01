"""Additive real-input evidence store. No dispatch, compiler or observer runner."""
import fcntl
import os
from pathlib import Path, PurePosixPath
from .real_receipt_policy import (Invalid, SCHEMA, PROFILE, PARAMETERS, DIGEST, canonical,
    parse, digest, keys, hash_value, attempt_id, ranked, parameters_match)

FIELDS = {
    'store': 'schema namespace',
    'expectation': 'schema spec_sha256 profile fixture parameters engine bootstrap_sha256 observer_sha256 qualification_sha256 source_policy',
    'request': 'schema expectation_sha256 case_id profile parameters source_channel source_environment cwd_policy',
    'registration': 'schema attempt_id expectation_sha256 request_sha256',
    'event': 'schema attempt_id sequence state primary_code diagnostics previous_sha256 witness_sha256 entered',
    'witness': 'schema attempt_id expectation_sha256 qualification_sha256 observer_sha256 observations violations',
    'recovery': 'schema attempt_id state primary_code diagnostics registration_sha256 request_sha256 witness_sha256 journal_sha256 journal_length valid_prefix_sha256 valid_prefix_length last_valid_sequence entered',
}
OBS = {
    'protected': 'initial valid association seals_exact length sha256',
    'derived': 'exact_bytes from_A retained length sha256',
    'engine': 'images_match live_association build_match interface_sha256',
    'callable': 'object_match native_target_match binding_match',
    'observer': 'artifact_match attachment_match qualified sentinel_active armed',
    'dispatch': 'attempted_event_sha256 persisted',
    'entry': 'native_entry engine_match callable_match after_dispatch armed exact_bytes same_B same_A independent_A_equal vector_valid parameters_match length sha256 positional_count keyword_count keyword_names parameters',
    'guard': 'operation denied',
    'completion': 'linked_to_entry outcome',
    'end': 'entry_count observer_entry_count same_A seals_exact no_reopen observer_complete execution_coverage execution_attempted',
}
NULLABLE = {'length', 'sha256', 'interface_sha256', 'same_A', 'seals_exact', 'parameters', 'keyword_names'}
BOOLS = set(('initial valid association seals_exact exact_bytes from_A retained images_match '
    'live_association build_match object_match native_target_match binding_match artifact_match '
    'attachment_match qualified sentinel_active armed persisted native_entry engine_match callable_match '
    'after_dispatch same_B same_A independent_A_equal vector_valid parameters_match denied linked_to_entry '
    'no_reopen observer_complete execution_coverage execution_attempted').split())
COUNTS = {'length', 'positional_count', 'keyword_count', 'entry_count', 'observer_entry_count'}


def typed_parameters(v):
    keys(v, 'filename mode flags dont_inherit optimize _feature_version')
    for k, x in PARAMETERS.items():
        if type(v[k]) is not type(x):
            raise Invalid('parameter type')
    canonical(v)


def validate(v, kind):
    keys(v, FIELDS[kind])
    if v['schema'] != SCHEMA + kind + '.v1':
        raise Invalid('schema')
    canonical(v)
    for k, x in v.items():
        if k.endswith('_sha256') and x is not None:
            hash_value(x)
    if 'attempt_id' in v:
        attempt_id(v['attempt_id'])
    if kind == 'store':
        hash_value(v['namespace'])
    elif kind == 'expectation':
        keys(v['fixture'], 'length sha256')
        if v['fixture'] != {'length': 2, 'sha256': DIGEST} or type(v['fixture']['length']) is not int:
            raise Invalid('fixture')
        if v['profile'] != PROFILE or v['source_policy'] != 'sealed-bytes-only' or not parameters_match(v['parameters']):
            raise Invalid('expectation values')
        engine = v['engine']
        keys(engine, 'implementation version build_sha256 abi images callable interface_sha256')
        if engine['implementation'] != 'CPython' or engine['version'] != '3.12.3' or engine['callable'] != 'builtins.compile':
            raise Invalid('engine descriptor')
        for k in ('build_sha256', 'interface_sha256'):
            hash_value(engine[k])
        if type(engine['abi']) is not str or not engine['abi']:
            raise Invalid('ABI descriptor')
        if type(engine['images']) is not list or [a.get('role') for a in engine['images'] if type(a) is dict] != ['compiler', 'executable', 'observer_native']:
            raise Invalid('role-sorted images')
        for image in engine['images']:
            keys(image, 'role sha256 origin_sha256')
            hash_value(image['sha256'])
            hash_value(image['origin_sha256'])
    elif kind == 'request':
        typed_parameters(v['parameters'])
        import re
        if type(v['case_id']) is not str or re.fullmatch(r'(P01|N0[1-9]|N1[01])(\.[0-9]+)?', v['case_id']) is None:
            raise Invalid('case')
        if type(v['source_environment']) is not dict or any(type(k) is not str or type(x) is not str for k, x in v['source_environment'].items()):
            raise Invalid('source environment')
        if any(type(v[k]) is not str for k in ('profile', 'source_channel', 'cwd_policy')):
            raise Invalid('request strings')
    elif kind == 'event':
        if type(v['sequence']) is not int or v['sequence'] < 0 or type(v['diagnostics']) is not list:
            raise Invalid('event sequence/codes')
        if v['entered'] is not None and type(v['entered']) is not bool:
            raise Invalid('entered')
        state = v['state']
        if state not in ('PREPARED', 'ATTEMPTED', 'ACCEPTED', 'REFUSED'):
            raise Invalid('journal state')
        codes = ranked(([v['primary_code']] if v['primary_code'] else []) + v['diagnostics'])
        if state == 'REFUSED':
            if not codes or v['primary_code'] != codes[0] or v['diagnostics'] != codes[1:] or v['witness_sha256'] is None:
                raise Invalid('refusal precedence/witness')
        elif codes or v['primary_code'] is not None:
            raise Invalid('unexpected fault')
        if state in ('PREPARED', 'ATTEMPTED') and v['witness_sha256'] is not None:
            raise Invalid('premature witness')
        if state == 'PREPARED' and (v['sequence'] != 0 or v['entered'] is not False):
            raise Invalid('prepared')
        if state == 'ATTEMPTED' and (v['sequence'] != 1 or v['entered'] is not None):
            raise Invalid('attempted')
        if state == 'ACCEPTED' and (v['entered'] is not True or v['witness_sha256'] is None):
            raise Invalid('accepted facts')
    elif kind == 'witness':
        if type(v['violations']) is not list or ranked(v['violations']) != v['violations'] or type(v['observations']) is not list:
            raise Invalid('witness collections')
        for i, o in enumerate(v['observations']):
            keys(o, 'index kind data')
            if type(o['index']) is not int or o['index'] != i or o['kind'] not in OBS:
                raise Invalid('observation index/kind')
            keys(o['data'], OBS[o['kind']])
            for k, x in o['data'].items():
                if x is None and k in NULLABLE:
                    continue
                if k in BOOLS and type(x) is not bool:
                    raise Invalid('observation bool')
                if k in COUNTS and (type(x) is not int or x < 0):
                    raise Invalid('observation count')
                if k.endswith('sha256'):
                    hash_value(x)
                if k == 'parameters':
                    typed_parameters(x)
                if k == 'keyword_names' and (type(x) is not list or any(type(s) is not str for s in x)):
                    raise Invalid('keyword names')
            if o['kind'] == 'guard' and o['data']['operation'] not in ('payload_open', 'payload_reopen', 'filesystem_fallback', 'source_redirect', 'execution'):
                raise Invalid('guard operation')
            if o['kind'] == 'completion' and o['data']['outcome'] not in ('code_return', 'exception', 'observer_stop', 'unknown'):
                raise Invalid('completion')
    elif kind == 'recovery':
        if v['state'] != 'ABORTED' or v['primary_code'] not in ('RECORD_INVALID', 'ATTEMPT_INCOMPLETE'):
            raise Invalid('recovery terminal')
        if type(v['diagnostics']) is not list or ranked(v['diagnostics'], True) != v['diagnostics'] or v['primary_code'] in v['diagnostics']:
            raise Invalid('recovery diagnostics')
        for k in ('journal_length', 'valid_prefix_length'):
            if type(v[k]) is not int or v[k] < 0:
                raise Invalid('recovery length')
        if v['valid_prefix_length'] > v['journal_length'] or (v['last_valid_sequence'] is not None and (type(v['last_valid_sequence']) is not int or v['last_valid_sequence'] < 0)):
            raise Invalid('recovery prefix')
        if v['entered'] is not None and type(v['entered']) is not bool:
            raise Invalid('recovery entered')
    return v


def witness_codes(w, x, e, attempted):
    try:
        validate(w, 'witness')
        if (w['attempt_id'] != x or w['expectation_sha256'] != digest(canonical(e)) or
                w['qualification_sha256'] != e['qualification_sha256'] or w['observer_sha256'] != e['observer_sha256']):
            return ['RECORD_INVALID']
    except (ValueError, TypeError, KeyError):
        return ['RECORD_INVALID']
    faults = list(w['violations'])
    obs = w['observations']
    nonguards = [o for o in obs if o['kind'] != 'guard']
    order = [o['kind'] for o in nonguards]
    positive_order = ['protected', 'derived', 'engine', 'callable', 'observer', 'dispatch', 'entry', 'protected', 'completion', 'end']
    precondition = attempted is None and bool(w['violations'])
    if (not precondition and order != positive_order or
            precondition and order != positive_order[:len(order)]):
        faults.append('OBSERVATION_MISSING')
    for o in obs:
        kind, d = o['kind'], o['data']
        if kind in ('protected', 'derived', 'entry'):
            if d['length'] is None or d['sha256'] is None:
                faults.append('OBSERVATION_MISSING')
            elif d['length'] < 2:
                faults.append('INPUT_TRUNCATED')
            elif d['length'] > 2:
                faults.append('INPUT_APPENDED')
            elif d['sha256'] != DIGEST:
                faults.append('INPUT_ALTERED')
        if kind == 'protected':
            if not all(d[k] is True for k in ('valid', 'association', 'seals_exact')):
                faults.append('WRONG_PROTECTED_OBJECT' if d['initial'] else 'OBJECT_SUBSTITUTION')
        elif kind == 'derived' and not all(d[k] is True for k in ('exact_bytes', 'from_A', 'retained')):
            faults.append('INPUT_IO')
        elif kind == 'engine' and (not all(d[k] is True for k in ('images_match', 'live_association', 'build_match')) or d['interface_sha256'] != e['engine']['interface_sha256']):
            faults.append('ENGINE_UNQUALIFIED')
        elif kind == 'callable' and not all(d.values()):
            faults.append('WRONG_COMPILE_CALLABLE')
        elif kind == 'observer':
            if not all(d[k] is True for k in ('artifact_match', 'attachment_match', 'qualified')):
                faults.append('OBSERVER_UNQUALIFIED')
            if d['sentinel_active'] is not True or d['armed'] is not True:
                faults.append('OBSERVER_NOT_ARMED')
        elif kind == 'dispatch' and (d['persisted'] is not True or d['attempted_event_sha256'] != attempted):
            faults.append('OBSERVATION_MISSING')
        elif kind == 'entry':
            for names, code in (
                (('native_entry', 'after_dispatch', 'independent_A_equal'), 'OBSERVATION_MISSING'),
                (('engine_match',), 'ENGINE_UNQUALIFIED'), (('callable_match',), 'WRONG_COMPILE_CALLABLE'),
                (('armed',), 'OBSERVER_NOT_ARMED'), (('same_B', 'same_A'), 'OBJECT_SUBSTITUTION'),
                (('exact_bytes',), 'INPUT_ALTERED'), (('vector_valid', 'parameters_match'), 'WRONG_ENTRYPOINT')):
                if any(d[k] is not True for k in names):
                    faults.append(code)
            if d['positional_count'] != 6 or d['keyword_count'] != 1 or d['keyword_names'] != ['_feature_version'] or not parameters_match(d['parameters']):
                faults.append('WRONG_ENTRYPOINT')
        elif kind == 'guard':
            faults.append('EXECUTION_PROHIBITED' if d['operation'] == 'execution' else
                          'SOURCE_REDIRECTION' if d['operation'] == 'source_redirect' else 'PATHNAME_REOPEN')
        elif kind == 'completion' and (d['linked_to_entry'] is not True or d['outcome'] != 'observer_stop'):
            faults.append('OBSERVATION_MISSING')
        elif kind == 'end':
            if d['entry_count'] != 1 or d['observer_entry_count'] != 1:
                faults.append('INVOCATION_COUNT')
            if d['same_A'] is not True or d['seals_exact'] is not True:
                faults.append('OBJECT_SUBSTITUTION')
            if any(d[k] is not True for k in ('no_reopen', 'observer_complete', 'execution_coverage')):
                faults.append('OBSERVATION_MISSING')
            if d['execution_attempted']:
                faults.append('EXECUTION_PROHIBITED')
    if len(nonguards) == 10 and (nonguards[0]['data'].get('initial') is not True or nonguards[7]['data'].get('initial') is not False):
        faults.append('OBSERVATION_MISSING')
    if sum(o['kind'] == 'entry' for o in obs) > 1:
        faults.append('INVOCATION_COUNT')
    return ranked(faults)


def synchronize_dir(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def retain(path, raw):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        with os.fdopen(fd, 'wb') as f:
            if f.write(raw) != len(raw):
                raise Invalid('short write')
            f.flush()
            os.fsync(f.fileno())
        synchronize_dir(path.parent)
        if path.read_bytes() != raw:
            raise Invalid('durable readback')
    except BaseException:
        # Never delete a partial write or retry it.
        raise


def forensic_bytes(value):
    """Supporting capture encoding is separate from the frozen witness schema."""
    from dataclasses import is_dataclass, asdict
    def convert(v):
        if is_dataclass(v):
            return convert(asdict(v))
        if type(v) is bytes:
            return {'hex': v.hex(), 'length': len(v)}
        if type(v) is tuple:
            return [convert(x) for x in v]
        if type(v) is dict:
            return {k: convert(x) for k, x in v.items()}
        if type(v) is list:
            return [convert(x) for x in v]
        return v
    return canonical(convert(value))


def journal_prefix(raw, x):
    events, prefix, invalid, previous = [], b'', False, None
    for line in raw.splitlines(keepends=True):
        if not line.endswith(b'\n'):
            break  # Torn tail is not a complete invalid record.
        try:
            v = validate(parse(line), 'event')
            if v['attempt_id'] != x or v['sequence'] != len(events) or v['previous_sha256'] != previous:
                raise Invalid('journal association')
            states = [a['state'] for a in events]
            allowed = ('PREPARED', 'REFUSED') if not states else (
                ('ATTEMPTED', 'REFUSED') if states == ['PREPARED'] else
                ('ACCEPTED', 'REFUSED') if states == ['PREPARED', 'ATTEMPTED'] else ())
            if v['state'] not in allowed:
                raise Invalid('terminal/order')
            events.append(v)
            prefix += line
            previous = digest(line)
        except (ValueError, TypeError, KeyError):
            invalid = True
            break
    return events, prefix, invalid


class Store:
    """Separate namespace; exclusive retained custody, monotonic reservations.

    There is intentionally no recovery-to-dispatch or child control method.
    """
    def __init__(self, root, namespace=None, create=False):
        self.root = Path(root)
        self.closed = False
        self.failed = False
        if create:
            hash_value(namespace)
            self.root.mkdir(mode=0o700)
            retain(self.root / 'store.json', canonical(dict(schema=SCHEMA + 'store.v1', namespace=namespace)))
            retain(self.root / 'custody', canonical({'namespace': namespace, 'kind': 'exclusive-controller'}))
            retain(self.root / 'lock', b'')
            retain(self.root / 'reservation-journal.jsonl', b'')
            (self.root / 'reservations').mkdir(mode=0o700)
            synchronize_dir(self.root)
        if self.root.is_symlink():
            raise Invalid('store symlink')
        metadata = validate(parse((self.root / 'store.json').read_bytes()), 'store')
        self.namespace = metadata['namespace']
        if namespace is not None and namespace != self.namespace:
            raise Invalid('namespace conflict')
        if parse((self.root / 'custody').read_bytes()) != {'namespace': self.namespace, 'kind': 'exclusive-controller'}:
            raise Invalid('custody missing/conflict')
        self.lock = os.open(self.root / 'lock', os.O_RDWR | os.O_NOFOLLOW)
        try:
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            os.close(self.lock)
            raise Invalid('exclusive custody unavailable')

    def close(self):
        if not self.closed:
            os.close(self.lock)
            self.closed = True

    def check(self):
        if self.closed or self.failed:
            raise Invalid('stale writer')
        try:
            valid = (validate(parse((self.root / 'store.json').read_bytes()), 'store')['namespace'] == self.namespace and
                parse((self.root / 'custody').read_bytes()) == {'namespace': self.namespace, 'kind': 'exclusive-controller'})
        except (OSError, ValueError, KeyError, TypeError):
            valid = False
        if not valid:
            raise Invalid('lost custody')

    def freeze(self, e, material):
        """Retain frozen comparison bytes before any reservation/registration."""
        self.check()
        validate(e, 'expectation')
        expected = {e[k] for k in ('spec_sha256', 'bootstrap_sha256', 'observer_sha256', 'qualification_sha256')}
        expected |= {e['engine'][k] for k in ('build_sha256', 'interface_sha256')}
        expected |= {image['origin_sha256'] for image in e['engine']['images']}
        if not expected <= set(material):
            raise Invalid('missing frozen qualification material')
        q = self.root / 'qualification'
        if not q.exists():
            q.mkdir(mode=0o700)
            synchronize_dir(self.root)
        for h, raw in sorted(material.items()):
            hash_value(h)
            if digest(raw) != h or not raw:
                raise Invalid('artifact pin mismatch')
            path = q / h
            if path.exists():
                if path.is_symlink() or path.read_bytes() != raw:
                    raise Invalid('frozen artifact conflict')
            else:
                retain(path, raw)

    def reserve_only(self, e):
        self.check()
        validate(e, 'expectation')
        pins = {e[k] for k in ('spec_sha256', 'bootstrap_sha256', 'observer_sha256', 'qualification_sha256')}
        pins |= {e['engine'][k] for k in ('build_sha256', 'interface_sha256')}
        pins |= {image['origin_sha256'] for image in e['engine']['images']}
        for h in pins:
            path = self.root / 'qualification' / h
            if path.is_symlink() or not path.is_file() or digest(path.read_bytes()) != h:
                raise Invalid('qualification must precede reservation')
        names = [p.name for p in (self.root / 'reservations').iterdir()]
        if any(not s.isdecimal() or int(s) < 1 or str(int(s)) != s for s in names):
            raise Invalid('reservation custody')
        ledger = (self.root / 'reservation-journal.jsonl').read_bytes()
        lines = ledger.splitlines(keepends=True)
        for i, line in enumerate(lines):
            if parse(line) != {'attempt_id': f'{self.namespace}:{i + 1}'}:
                raise Invalid('reservation journal conflict')
        if set(names) != {str(i + 1) for i in range(len(lines))}:
            raise Invalid('reservation custody missing/partial')
        for name in names:
            if (self.root / 'reservations' / name).read_bytes() != canonical({'attempt_id': f'{self.namespace}:{name}'}):
                raise Invalid('reservation bytes conflict')
        n = max(map(int, names), default=0) + 1
        x = f'{self.namespace}:{n}'
        eraw = canonical(e)
        ep = self.root / 'expectation.json'
        if ep.exists():
            if ep.read_bytes() != eraw:
                raise Invalid('frozen expectation conflict')
        else:
            if names:
                raise Invalid('missing expectation custody')
            retain(ep, eraw)
        reservation = canonical({'attempt_id': x})
        try:
            retain(self.root / 'reservations' / str(n), reservation)
            fd = os.open(self.root / 'reservation-journal.jsonl', os.O_WRONLY | os.O_APPEND | os.O_NOFOLLOW)
            with os.fdopen(fd, 'ab') as f:
                if f.write(reservation) != len(reservation):
                    raise Invalid('reservation short write')
                f.flush()
                os.fsync(f.fileno())
            synchronize_dir(self.root)
        except BaseException:
            self.failed = True
            raise
        return Attempt(self, n)

    def reserve(self, e, request_raw):
        attempt = self.reserve_only(e)
        attempt.register(request_raw)
        return attempt


class Attempt:
    def __init__(self, store, ordinal):
        if type(ordinal) is not int or ordinal < 1:
            raise Invalid('ordinal')
        self.store = store
        self.path = store.root / str(ordinal)
        self.x = f'{store.namespace}:{ordinal}'
        self._preparation = None
        self._validated_terminal = None
        self._attempted_hash = None
        self._packaging_authority = None

    def reservation(self):
        raw = (self.store.root / 'reservations' / self.path.name).read_bytes()
        if parse(raw) != {'attempt_id': self.x}:
            raise Invalid('reservation conflict')
        return raw

    def register(self, raw):
        self.store.check()
        self.reservation()
        if self.raw('recovery.json') is not None:
            raise Invalid('reserved attempt already terminal')
        if not self.path.exists():
            self.path.mkdir(mode=0o700)
            synchronize_dir(self.store.root)
        e_raw = (self.store.root / 'expectation.json').read_bytes()
        retain(self.path / 'request.json', raw)
        retain(self.path / 'registration.json', canonical(dict(schema=SCHEMA + 'registration.v1',
            attempt_id=self.x, expectation_sha256=digest(e_raw), request_sha256=digest(raw))))

    def raw(self, name):
        p = self.path / name
        if p.is_symlink():
            raise Invalid('retained symlink')
        return p.read_bytes() if p.exists() else None

    def events(self):
        raw = self.raw('events.jsonl') or b''
        events, prefix, invalid = journal_prefix(raw, self.x)
        if invalid or prefix != raw:
            raise Invalid('invalid/torn journal')
        return events

    def active(self):
        self.store.check()
        self.reservation()
        regraw, reqraw = self.raw('registration.json'), self.raw('request.json')
        if regraw is None or reqraw is None:
            raise Invalid('registration custody missing')
        reg = validate(parse(regraw), 'registration')
        if reg['attempt_id'] != self.x or reg['request_sha256'] != digest(reqraw) or reg['expectation_sha256'] != digest((self.store.root / 'expectation.json').read_bytes()):
            raise Invalid('registration association')
        if self.raw('recovery.json') is not None:
            raise Invalid('recovery terminal or interrupted recovery')
        events = self.events()
        if events and events[-1]['state'] in ('ACCEPTED', 'REFUSED'):
            raise Invalid('immutable terminal')
        return events

    def event(self, state, faults=(), entered=None, witness=None):
        events = self.active()
        states = [e['state'] for e in events]
        allowed = ('PREPARED', 'REFUSED') if not states else (
            ('ATTEMPTED', 'REFUSED') if states == ['PREPARED'] else
            ('ACCEPTED', 'REFUSED') if states == ['PREPARED', 'ATTEMPTED'] else ())
        if state not in allowed:
            raise Invalid('transition')
        if state in ('PREPARED', 'ATTEMPTED') and self._preparation is None:
            raise Invalid('validated admission required')
        if state in ('ACCEPTED', 'REFUSED') and self._validated_terminal != witness:
            raise Invalid('validated observation required')
        faults = ranked(faults)
        if state in ('ACCEPTED', 'REFUSED'):
            wraw = self.raw('witness.json')
            if wraw is None or digest(wraw) != witness:
                raise Invalid('durable witness required')
            w = validate(parse(wraw), 'witness')
            e = validate(parse((self.store.root / 'expectation.json').read_bytes()), 'expectation')
            tried = digest(canonical(events[-1])) if events and events[-1]['state'] == 'ATTEMPTED' else None
            wfaults = witness_codes(w, self.x, e, tried)
            if state == 'ACCEPTED' and (wfaults or self.raw('capture.json') is None):
                raise Invalid('incomplete receipt')
            if not set(wfaults) <= set(faults):
                raise Invalid('unsupported omission of faults')
        previous = digest(canonical(events[-1])) if events else None
        v = dict(schema=SCHEMA + 'event.v1', attempt_id=self.x, sequence=len(events),
                 state=state, primary_code=faults[0] if faults else None, diagnostics=faults[1:],
                 previous_sha256=previous, witness_sha256=witness, entered=entered)
        validate(v, 'event')
        raw = canonical(v)
        try:
            fd = os.open(self.path / 'events.jsonl', os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_NOFOLLOW, 0o600)
            with os.fdopen(fd, 'ab') as f:
                if f.write(raw) != len(raw):
                    raise Invalid('journal short write')
                f.flush()
                os.fsync(f.fileno())
            synchronize_dir(self.path)
            synchronize_dir(self.store.root)
            if self.events()[-1] != v:
                raise Invalid('journal durable readback')
        except BaseException:
            self.store.failed = True
            raise
        if state in ('ACCEPTED', 'REFUSED'):
            self._packaging_authority = digest(raw)
        return digest(raw)

    def prepare(self, preparation=None):
        self.active()
        from .real_receipt_integration import (preparation_codes, measured_witness, retain_preparation,
                                              _capture_manifest, _package)
        e = validate(parse((self.store.root / 'expectation.json').read_bytes()), 'expectation')
        faults = []
        try:
            r = validate(parse(self.raw('request.json')), 'request')
            if r['expectation_sha256'] != digest(canonical(e)):
                faults = ['EXPECTATION_INVALID']
            elif r['profile'] != PROFILE:
                faults = ['PROFILE_UNQUALIFIED']
            elif r['source_channel'] != 'protected_bytes' or r['source_environment'] or r['cwd_policy'] != 'exclusive-synthetic':
                faults = ['SOURCE_REDIRECTION']
            elif not parameters_match(r['parameters']):
                faults = ['WRONG_ENTRYPOINT']
        except (ValueError, TypeError, KeyError):
            faults = ['EXPECTATION_INVALID']
        if not faults:
            faults = preparation_codes(preparation, self.x, e, self.store.namespace)
        retain_preparation(self, preparation)
        if faults:
            w = measured_witness(preparation, None, self.x, e, None, faults, precondition=True)
            validate(w, 'witness')
            _capture_manifest(self)
            retain(self.path / 'witness.json', canonical(w))
            self._validated_terminal = digest(canonical(w))
            terminal = self.event('REFUSED', faults, False, self._validated_terminal)
            _package(self)
            return terminal
        self._preparation = preparation
        return self.event('PREPARED', entered=False)

    def attempted(self):
        from .real_receipt_integration import preparation_codes
        e = validate(parse((self.store.root / 'expectation.json').read_bytes()), 'expectation')
        if preparation_codes(self._preparation, self.x, e, self.store.namespace):
            raise Invalid('admission changed')
        self._attempted_hash = self.event('ATTEMPTED')
        return self._attempted_hash

    def finish(self, witness, capture):
        """Integrate raw transcript and measurements; never backfill ATTEMPTED."""
        from .real_receipt_integration import finish_observation
        events = self.active()
        e = validate(parse((self.store.root / 'expectation.json').read_bytes()), 'expectation')
        attempted = digest(canonical(events[-1])) if events and events[-1]['state'] == 'ATTEMPTED' else None
        if attempted is None or attempted != self._attempted_hash or self._preparation is None:
            raise Invalid('no live durable dispatch authority')
        return finish_observation(self, self._preparation, capture, e, attempted, witness)

    def recover(self):
        self.store.check()
        reservation = (self.store.root / 'reservations' / self.path.name)
        if reservation.is_symlink() or not reservation.is_file():
            raise Invalid('missing reservation custody')
        reserved_raw = reservation.read_bytes()
        reservation_invalid = False
        if reserved_raw.endswith(b'\n'):
            try:
                self.reservation()
            except (Invalid, ValueError):
                reservation_invalid = True
        if not self.path.exists():
            self.path.mkdir(mode=0o700)
            synchronize_dir(self.store.root)
        names = ('registration.json', 'request.json', 'witness.json', 'events.jsonl')
        raw = {name: self.raw(name) for name in names}
        events, prefix, invalid = journal_prefix(raw['events.jsonl'] or b'', self.x)
        invalid = invalid or reservation_invalid
        e_raw = (self.store.root / 'expectation.json').read_bytes()
        capture_raw = self.raw('capture.json')
        if capture_raw is not None and capture_raw.endswith(b'\n'):
            try:
                supporting = parse(capture_raw)
                if type(supporting) is dict and type(supporting.get('dispatch')) is dict:
                    dispatch = supporting['dispatch']
                    if dispatch.get('attempt_id') != self.x or dispatch.get('expectation_sha256') != digest(e_raw):
                        invalid = True
            except Invalid:
                invalid = True
        for name, kind in (('registration.json', 'registration'), ('request.json', 'request'), ('witness.json', 'witness')):
            if raw[name] is not None and raw[name].endswith(b'\n'):
                try:
                    v = validate(parse(raw[name]), kind)
                    if kind in ('registration', 'witness') and (v['attempt_id'] != self.x or v['expectation_sha256'] != digest(e_raw)):
                        raise Invalid('cross-attempt record')
                    if kind == 'registration' and v['request_sha256'] != digest(raw['request.json'] or b''):
                        raise Invalid('request link')
                except (ValueError, KeyError, TypeError):
                    invalid = True
        if events and events[-1]['state'] in ('ACCEPTED', 'REFUSED') and prefix == raw['events.jsonl'] and not invalid:
            if raw['witness.json'] is not None and digest(raw['witness.json']) == events[-1]['witness_sha256']:
                w = parse(raw['witness.json'])
                e = validate(parse(e_raw), 'expectation')
                tried = digest(canonical(events[-2])) if len(events) > 1 and events[-2]['state'] == 'ATTEMPTED' else None
                faults = witness_codes(w, self.x, e, tried)
                terminal = events[-1]
                if (terminal['state'] == 'ACCEPTED' and not faults or terminal['state'] == 'REFUSED' and
                        set(faults) <= set([terminal['primary_code']] + terminal['diagnostics'])):
                    return terminal  # Preserve terminal despite incomplete packaging.
                invalid = True
        v = dict(schema=SCHEMA + 'recovery.v1', attempt_id=self.x, state='ABORTED',
                 primary_code='RECORD_INVALID' if invalid else 'ATTEMPT_INCOMPLETE', diagnostics=[],
                 registration_sha256=digest(raw['registration.json']) if raw['registration.json'] is not None else None,
                 request_sha256=digest(raw['request.json']) if raw['request.json'] is not None else None,
                 witness_sha256=digest(raw['witness.json']) if raw['witness.json'] is not None else None,
                 journal_sha256=digest(raw['events.jsonl']) if raw['events.jsonl'] is not None else None,
                 journal_length=len(raw['events.jsonl'] or b''), valid_prefix_sha256=digest(prefix),
                 valid_prefix_length=len(prefix), last_valid_sequence=events[-1]['sequence'] if events else None,
                 entered=events[-1]['entered'] if events else None)
        validate(v, 'recovery')
        old = self.raw('recovery.json')
        if old is not None:
            if old != canonical(v):
                raise Invalid('recovery conflict/partial write retained')
        else:
            retain(self.path / 'recovery.json', canonical(v))
            self._packaging_authority = digest(canonical(v))
        return v


def manifest(kind, x, ehash, files):
    attempt_id(x)
    hash_value(ehash)
    if kind not in ('capture', 'package'):
        raise Invalid('manifest kind')
    entries = []
    for path, raw in sorted(files.items()):
        p = PurePosixPath(path)
        if (type(path) is not str or not path or p.is_absolute() or '..' in p.parts or
                str(p) != path or p.name in ('capture-manifest.json', 'package-manifest.json', 'package-manifest.sha256') and
                (p.name != 'capture-manifest.json' or kind == 'capture')):
            raise Invalid('manifest path/self-reference')
        entries.append(dict(path=path, length=len(raw), sha256=digest(raw)))
    return dict(schema=f'ns001.h2a2.real-receipt.{kind}-manifest.v1', attempt_id=x,
                expectation_sha256=ehash, entries=entries)


def verify_manifest(raw, files, kind, x, ehash):
    return raw == canonical(manifest(kind, x, ehash, files))


def public_accept(attempt, package_raw, sidecar, files, required_paths):
    """Frozen minimum inventory plus caller additions; no incomplete public ACCEPT."""
    from .real_receipt_integration import verify_package, _all_files
    try:
        return (package_raw == attempt.raw('package-manifest.json') and
                sidecar == attempt.raw('package-manifest.sha256') and files == _all_files(attempt) and
                set(required_paths) <= set(files) and verify_package(attempt, require_accept=True))
    except (Invalid, OSError, TypeError, KeyError):
        return False
