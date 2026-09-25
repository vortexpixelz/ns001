"""Bounded offline acceptance harness; run directly with externally reviewed K/T.

No pytest discovery, project imports, dependencies, live inputs or payload execution.
Fault adapters below belong to this test harness only. They are labelled in inventory.
"""
import argparse
import ast
from contextlib import ExitStack
from dataclasses import replace
import errno
import fcntl
import hashlib
import importlib.util
import inspect
import json
import mmap
import os
from pathlib import Path
import stat
import sys
import tempfile
from unittest.mock import patch

PAYLOAD = b'abc'
F = 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
M = '4a9ebe2c4e275600d9a6c7864bb14c3d5a4c0b6a7c8bbf88193fc48f76affce0'
S = '0ae1c30f2568188390fe05d092609eb122f3bee16c48f41fae9fe3f08e6ba432'
PROFILE = 'ns001.h2a2.sealed-memfd.v1'
L = ['F_SEAL_GROW', 'F_SEAL_SEAL', 'F_SEAL_SHRINK', 'F_SEAL_WRITE']
MANIFEST = (b'{"byte_length":3,"path":"source.bin","schema":"ns001.h2a2.single-file.v1",'
            b'"sha256":"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"}')


def C(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True,
                      allow_nan=False).encode('ascii')


def H(value):
    return hashlib.sha256(value).hexdigest()


def oracle(k, t):
    def role(name):
        return dict(role=name, source_sha256=k, object_type='sealed-memfd',
                    byte_length=3, sha256=F, seals=L, reference_bound=True)
    return C(dict(profile=PROFILE, verdict='ACCEPT', snapshot_sha256=S,
                  manifest_sha256=M, source_sha256=F, byte_length=3,
                  implementation_sha256=k, harness_sha256=t, consumer=role('consumer'),
                  observer=role('observer'), checks=dict(source_validated=True,
                  copy_validated=True, sealed_revalidated=True, creation_witnessed=True,
                  duplication_witnessed=True, same_object=True, no_reopen=True,
                  consumer_calls=1, observer_calls=1)))


def deny_external(event, args):
    if event.startswith(('socket.', 'subprocess.', 'os.exec', 'os.spawn', 'os.posix_spawn')) or event in (
            'os.system', 'os.fork', 'os.forkpty'):
        raise AssertionError('OFFLINE_BOUNDARY: ' + event)


def review_roles(source):
    """Explicit AST allowlist for both fixed role bodies; no payload evaluator."""
    tree = ast.parse(source)
    roles = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)
             and n.name in ('consume', 'observe')}
    assert set(roles) == {'consume', 'observe'}
    allowed = {'fstat', 'fcntl', 'pread', 'sha256', 'len', 'require', 'dict',
               'stat.S_ISREG', 'sha256(data).hexdigest'}
    for node in roles.values():
        assert [a.arg for a in node.args.args] == ['fd']
        for n in ast.walk(node):
            assert not isinstance(n, (ast.Import, ast.ImportFrom, ast.Lambda))
            if isinstance(n, ast.Call):
                assert ast.unparse(n.func) in allowed, ast.unparse(n.func)


class Trace:
    """External observations; never infer creation/duplication from a candidate flag."""
    def __init__(self, m):
        self.m = m
        self.anchor = None
        self.key = None
        self.duplicates = []
        self.calls = {'consumer': 0, 'observer': 0}
        self.role_events = {'consumer': [], 'observer': []}
        self.associations = []
        self.seals = []
        self.open_after_validation = []
        self.finalized = False
        self.source_validated = False
        self.closed = []
        self.proof = []

    def install(self, stack):
        m = self.m
        originals = {n: getattr(m, n) for n in ('memfd_create', 'fcntl', 'pread',
                     'fstat', 'fd_open', 'close', '_boundary', '_finalize', '_acquire')}
        def create(name, flags):
            fd = originals['memfd_create'](name, flags)
            assert self.anchor is None, 'second production memfd'
            self.anchor = fd
            self.key = (os.fstat(fd).st_dev, os.fstat(fd).st_ino)
            self.creation_flags = flags
            return fd
        def fc(fd, op, *args):
            caller = inspect.currentframe().f_back.f_code.co_name
            try:
                result = originals['fcntl'](fd, op, *args)
            except OSError as e:
                if op == m.F_ADD_SEALS:
                    self.proof.append(dict(operation='F_ADD_SEALS', errno=errno.errorcode[e.errno]))
                raise
            if op == m.F_DUPFD_CLOEXEC:
                self.duplicates.append((fd, result))
            if op == m.F_GET_SEALS:
                self.seals.append(result)
            if caller in ('consume', 'observe'):
                self.role_events['consumer' if caller == 'consume' else 'observer'].append(('seal', fd, result))
            return result
        def pr(fd, count, offset):
            caller = inspect.currentframe().f_back.f_code.co_name
            result = originals['pread'](fd, count, offset)
            if caller in ('consume', 'observe'):
                role = 'consumer' if caller == 'consume' else 'observer'
                self.calls[role] += 1
                self.role_events[role].append(('read', fd, count, offset, result))
            return result
        def fs(fd):
            caller = inspect.currentframe().f_back.f_code.co_name
            result = originals['fstat'](fd)
            if caller in ('consume', 'observe'):
                self.role_events['consumer' if caller == 'consume' else 'observer'].append(
                    ('stat', fd, result.st_dev, result.st_ino, result.st_size))
            return result
        def op(*args, **kwargs):
            if self.source_validated:
                self.open_after_validation.append(str(args[0]))
                raise m.Refusal('HANDOFF_REOPEN')
            return originals['fd_open'](*args, **kwargs)
        def cl(fd):
            self.closed.append(fd)
            return originals['close'](fd)
        def boundary(handles, key):
            facts = [(os.fstat(fd).st_dev, os.fstat(fd).st_ino) for fd in handles]
            self.associations.append(all(x == self.key for x in facts) and key == self.key)
            return originals['_boundary'](handles, key)
        def acquired(root, supplied):
            payload = originals['_acquire'](root, supplied)
            self.source_validated = True
            return payload
        def finalized(fd):
            key = originals['_finalize'](fd)
            self.finalized = True
            return key
        for name, fn in [('memfd_create', create), ('fcntl', fc), ('pread', pr),
                         ('fstat', fs), ('fd_open', op), ('close', cl),
                         ('_boundary', boundary), ('_finalize', finalized), ('_acquire', acquired)]:
            stack.enter_context(patch.object(m, name, fn))

    def positive(self):
        m = self.m
        assert self.creation_flags == os.MFD_ALLOW_SEALING | os.MFD_CLOEXEC
        assert len(self.duplicates) == 2
        assert all(a == self.anchor for a, _ in self.duplicates)
        assert len({self.anchor, *(b for _, b in self.duplicates)}) == 3
        assert self.calls == {'consumer': 1, 'observer': 1}
        assert len(self.associations) >= 7 and all(self.associations)
        assert not self.open_after_validation
        for role, (_, fd) in zip(('consumer', 'observer'), self.duplicates):
            events = self.role_events[role]
            assert events == [('stat', fd, *self.key, 3), ('seal', fd, m.Q),
                              ('read', fd, 4, 0, PAYLOAD)], events
        assert self.anchor in self.closed
        assert all(fd in self.closed for _, fd in self.duplicates)
        self.proof.append(dict(creation=True, direct_duplicates=2,
                               association_checks=len(self.associations),
                               independent_role_reads=2, no_reopen=True))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--implementation-sha256', required=True)
    parser.add_argument('--harness-sha256', required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    impl = repo / 'e0/h2/runtime_trust_root.py'
    raw = impl.read_bytes()
    k, t = args.implementation_sha256, args.harness_sha256
    assert H(raw) == k and H(Path(__file__).read_bytes()) == t, 'unreviewed source bytes'
    assert H(MANIFEST) == M and H(PAYLOAD) == F
    review_roles(raw.decode())
    sys.dont_write_bytecode = True
    sys.addaudithook(deny_external)
    spec = importlib.util.spec_from_file_location('ns001_synthetic_handoff', impl)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    pins = m.Pins(k, t, k, t, (m.CV, 'consume', k), (m.OV, 'observe', k))
    inventory = []
    positives = []

    def case(case_id, code=None, setup=None, fault=None, counts=(0, 0), kind='fixture'):
        with tempfile.TemporaryDirectory(prefix='ns001-h2a2-', dir='/tmp') as temp:
            root_path = Path(temp) / 'fixture'
            root_path.mkdir()
            (root_path / 'source.bin').write_bytes(PAYLOAD)
            (root_path / 'manifest.json').write_bytes(MANIFEST)
            root = m.bind_root(str(root_path))
            options = dict(root=root, supplied=str(root_path), pins=pins, expected=(F, 3, M, S))
            trace = Trace(m)
            try:
                with ExitStack() as stack:
                    if setup:
                        setup(root_path, options, stack)
                    trace.install(stack)
                    if fault:
                        fault(root_path, options, trace, stack)
                    record = m.run(**options)
                actual = json.loads(record)
                if code is None:
                    assert record == oracle(k, t), (case_id, actual)
                    trace.positive()
                    positives.append(record)
                else:
                    expected = C(dict(profile=PROFILE, verdict='REFUSE', code=code, handoff_succeeded=False))
                    assert record == expected, (case_id, actual, code)
                    assert b'ACCEPT' not in record
                    assert tuple(trace.calls.values()) == counts, (case_id, trace.calls)
                inventory.append(dict(case=case_id, kind=kind, verdict=actual['verdict'],
                    code=actual.get('code'), record_sha256=H(record), consumer_calls=trace.calls['consumer'],
                    observer_calls=trace.calls['observer'], observations=trace.proof))
            finally:
                os.close(root.fd)

    def write_source(data):
        return lambda p, o, s: (p / 'source.bin').write_bytes(data)
    def raw_manifest(data):
        return lambda p, o, s: (p / 'manifest.json').write_bytes(data)
    def manifest(**updates):
        v = json.loads(MANIFEST)
        v.update(updates)
        return raw_manifest(C(v))
    def remove(name):
        return lambda p, o, s: (p / name).unlink()
    def after_final(action):
        def fault(p, o, tr, st):
            original = m._finalize
            def wrapped(fd):
                key = original(fd)
                action(p, o, tr, st, fd)
                return key
            st.enter_context(patch.object(m, '_finalize', wrapped))
        return fault
    def replacement_fd(st):
        fd = os.memfd_create('negative-substitute', os.MFD_ALLOW_SEALING | os.MFD_CLOEXEC)
        os.pwrite(fd, PAYLOAD, 0)
        fcntl.fcntl(fd, fcntl.F_ADD_SEALS, m.Q)
        st.callback(os.close, fd)
        return fd
    def substitute(where):
        def fault(p, o, tr, st):
            other = replacement_fd(st)
            if where == 'anchor':
                original = m._handoff
                st.enter_context(patch.object(m, '_handoff', lambda a, key, pins: original(other, key, pins)))
            elif where in ('consumer', 'observer'):
                original = m.fcntl
                number = 1 if where == 'consumer' else 2
                def altered(fd, op, *args):
                    result = original(fd, op, *args)
                    if op == m.F_DUPFD_CLOEXEC and len(tr.duplicates) == number:
                        os.dup2(other, result, inheritable=False)
                    return result
                st.enter_context(patch.object(m, 'fcntl', altered))
            else:
                original = m._result
                def altered(value, key, role, pin):
                    result = original(value, key, role, pin)
                    if role == 'consumer':
                        os.dup2(other, tr.duplicates[1][1], inheritable=False)
                    return result
                st.enter_context(patch.object(m, '_result', altered))
            tr.proof.append(dict(equal_byte_distinct_memfd=True, substitution=where))
        return fault
    def wrong_result(role, missing=False):
        def fault(p, o, tr, st):
            original = m._result
            def changed(value, key, name, pin):
                if name == role:
                    value = None if missing else dict(value, sha256='0' * 64)
                return original(value, key, name, pin)
            st.enter_context(patch.object(m, '_result', changed))
        return fault

    case('P1')
    case('P1-repeat')
    case('P2-replace', fault=after_final(lambda p, o, tr, st, fd: (p / 'source.bin').write_bytes(b'abd')))
    case('P2-delete', fault=after_final(lambda p, o, tr, st, fd: (p / 'source.bin').unlink()))
    for name, data, code in [('N01', b'abd', 'FILE_DIGEST'), ('N02', b'ab', 'FILE_LENGTH'),
                             ('N03', b'abcd', 'FILE_LENGTH')]:
        case(name, code, setup=write_source(data))
    case('N04', 'FILE_MISSING', setup=lambda p, o, s: (p / 'source.bin').rename(p / 'other.bin'))
    case('N05', 'FILE_MISSING', setup=remove('source.bin'))
    case('N06', 'EXTRA_FILE', setup=lambda p, o, s: (p / 'extra.bin').write_bytes(b''))
    def symlink(p, o, st):
        (p / 'source.bin').unlink()
        (p / 'source.bin').symlink_to('manifest.json')
    case('N07', 'SYMLINK', setup=symlink)
    case('N08', 'MANIFEST_DIGEST', setup=manifest(sha256='c' + F[1:]))
    case('N09', 'MANIFEST_LENGTH', setup=manifest(byte_length=4))
    case('N10', 'DUPLICATE_KEY', setup=raw_manifest(MANIFEST[:-1] + b',"schema":"x"}'))
    v = json.loads(MANIFEST); del v['sha256']
    case('N11', 'MANIFEST_FIELD_MISSING', setup=raw_manifest(C(v)))
    def wrong_root(p, o, st):
        other = p.parent / 'other'; other.mkdir()
        (other / 'source.bin').write_bytes(PAYLOAD)
        (other / 'manifest.json').write_bytes(MANIFEST)
        o['supplied'] = str(other)
    case('N12', 'ROOT_MISMATCH', setup=wrong_root)
    case('N13', 'HANDOFF_SUBSTITUTED', fault=substitute('consumer'), kind='synthetic substitution / real distinct memfd')
    for index, value in enumerate(('wrong-version', 'wrong-entrypoint', '0' * 64)):
        def wrong_consumer(p, o, st, index=index, value=value):
            cid = list(pins.consumer); cid[index] = value
            o['pins'] = replace(pins, consumer=tuple(cid))
        case('N14-policy-' + str(index), 'CONSUMER_IDENTITY', setup=wrong_consumer)
    def switch_consumer(p, o, tr, st, fd):
        st.enter_context(patch.object(m, 'consume', lambda fd: None))
    case('N14-delivery', 'CONSUMER_IDENTITY', fault=after_final(switch_consumer), kind='synthetic identity substitution')
    case('N15', 'MANIFEST_MISSING', setup=remove('manifest.json'))
    case('N16', 'MANIFEST_MALFORMED', setup=raw_manifest(b'{'))
    case('N17', 'MANIFEST_FIELD_UNKNOWN', setup=manifest(x='x'))
    case('N18', 'MANIFEST_VERSION', setup=manifest(schema='ns001.h2a2.single-file.v2'))
    case('N19', 'PATH_TRAVERSAL', setup=manifest(path='../source.bin'))
    case('N20', 'PATH_ABSOLUTE', setup=manifest(path='/source.bin'))
    case('N21', 'DUPLICATE_PATH', setup=raw_manifest(MANIFEST[:-1] + b',"path":"source.bin"}'))
    for i in range(4):
        def wrong_expected(p, o, st, i=i):
            values = list(o['expected']); values[i] = 4 if i == 1 else '0' * 64
            o['expected'] = tuple(values)
        case('N22-' + str(i), 'EXPECTED_IDENTITY', setup=wrong_expected)
    def missing_root(p, o, st):
        for f in p.iterdir(): f.unlink()
        p.rmdir()
    case('N23', 'ROOT_MISSING', setup=missing_root)
    for name in ('.hidden', 'source.pyc'):
        case('N24-' + name, 'EXTRA_FILE', setup=lambda p, o, st, name=name: (p / name).write_bytes(b''))
    case('N25-directory', 'ENTRY_TYPE', setup=lambda p, o, st: (p / 'nested').mkdir())
    case('N25-fifo', 'ENTRY_TYPE', setup=lambda p, o, st: os.mkfifo(p / 'fifo'))
    for name, mode in [('socket', stat.S_IFSOCK), ('device', stat.S_IFCHR)]:
        def metadata(p, o, tr, st, mode=mode):
            (p / 'special').write_bytes(b'')
            original = m.fd_stat
            def changed(path, **kw):
                value = original(path, **kw)
                if path == 'special':
                    fields = list(value); fields[0] = mode | 0o600
                    return os.stat_result(fields)
                return value
            st.enter_context(patch.object(m, 'fd_stat', changed))
        case('N25-' + name, 'ENTRY_TYPE', fault=metadata, kind='synthetic metadata stub; no socket/device created')
    def unprotected(p, o, tr, st):
        original = m.fcntl
        def changed(fd, op, *args):
            if tr.finalized and op == m.F_GET_SEALS:
                return m.Q & ~m.F_SEAL_WRITE
            return original(fd, op, *args)
        st.enter_context(patch.object(m, 'fcntl', changed))
    case('N26', 'HANDOFF_UNPROTECTED', fault=unprotected, kind='synthetic seal-query fault')
    def changed_retained(p, o, tr, st):
        original = m.pread
        def changed(fd, count, offset):
            if tr.finalized: return b'abd'
            return original(fd, count, offset)
        st.enter_context(patch.object(m, 'pread', changed))
    case('N27', 'HANDOFF_MUTATED', fault=changed_retained, kind='synthetic read fault; real mutation denial separately M04')
    case('N28', 'MANIFEST_NONCANONICAL', setup=raw_manifest(MANIFEST + b'\n'))
    case('N29', 'FILE_PATH', setup=manifest(path='other.bin'))
    for missing in (False, True):
        case('N30-' + str(missing), 'CONSUMER_RESULT', fault=wrong_result('consumer', missing),
             counts=(1, 0), kind='synthetic result fault')
    def no_evidence(p, o, tr, st):
        original = m._receipt
        st.enter_context(patch.object(m, '_receipt', lambda pin, c, ob: original(pin, c, None)))
    case('N31', 'EVIDENCE_INCOMPLETE', fault=no_evidence, counts=(1, 1), kind='synthetic observation omission')

    def no_sealing(p, o, tr, st):
        original = m.memfd_create
        st.enter_context(patch.object(m, 'memfd_create', lambda n, flags: original(n, os.MFD_CLOEXEC)))
    case('M01', 'MEMFD_CAPABILITY', fault=no_sealing, kind='real kernel initial seal state')
    def seal_fault(p, o, tr, st):
        original = m.fcntl
        def fail(fd, op, *args):
            if op == m.F_ADD_SEALS: raise OSError(errno.EPERM, 'injected')
            return original(fd, op, *args)
        st.enter_context(patch.object(m, 'fcntl', fail))
    case('M02', 'MEMFD_SEAL_APPLY', fault=seal_fault, kind='synthetic syscall error')
    for name in L:
        def missing_seal(p, o, tr, st, name=name):
            original = m.fcntl
            def altered(fd, op, *args):
                if op == m.F_ADD_SEALS: args = (m.Q & ~getattr(m, name),)
                return original(fd, op, *args)
            st.enter_context(patch.object(m, 'fcntl', altered))
        case('M03-' + name, 'MEMFD_SEAL_SET', fault=missing_seal, kind='real reduced seal set / synthetic setup')
    def denied(operation):
        def action(p, o, tr, st, fd):
            try:
                if operation == 'write': os.pwrite(fd, b'z', 0)
                else: os.ftruncate(fd, 2 if operation == 'shrink' else 4)
            except OSError as e:
                assert e.errno == errno.EPERM, e
            else: raise AssertionError('kernel permitted sealed mutation')
            assert os.pread(fd, 4, 0) == PAYLOAD and os.fstat(fd).st_size == 3
            assert fcntl.fcntl(fd, fcntl.F_GET_SEALS) == m.Q
            tr.proof.append(dict(operation=operation, errno='EPERM', unchanged=True))
            raise m.Refusal('HANDOFF_MUTATION_ATTEMPT')
        return after_final(action)
    case('M04', 'HANDOFF_MUTATION_ATTEMPT', fault=denied('write'), kind='kernel enforcement + harness protocol refusal')
    case('M05-shrink', 'HANDOFF_MUTATION_ATTEMPT', fault=denied('shrink'), kind='kernel enforcement + harness protocol refusal')
    case('M05-grow', 'HANDOFF_MUTATION_ATTEMPT', fault=denied('grow'), kind='kernel enforcement + harness protocol refusal')
    for cid, where, counts in [('M06', 'anchor', (0, 0)), ('M07', 'after-consumer', (1, 0)),
                                ('M08', 'consumer', (0, 0)), ('M09', 'observer', (0, 0))]:
        case(cid, 'HANDOFF_SUBSTITUTED', fault=substitute(where), counts=counts,
             kind='synthetic substitution / real distinct sealed memfd')
    def copy_data(data, report=None):
        def fault(p, o, tr, st):
            original = m.pwrite
            def changed(fd, value, offset):
                n = original(fd, data, offset)
                return n if report is None else report
            st.enter_context(patch.object(m, 'pwrite', changed))
        return fault
    case('M10', 'MEMFD_COPY_DIGEST', fault=copy_data(b'abd'), kind='synthetic copy fault')
    for size in (2, 4):
        def bad_copy_size(p, o, tr, st, size=size):
            original = m.pwrite
            def changed(fd, data, offset):
                result = original(fd, data, offset)
                os.ftruncate(fd, size)  # corrupt completed copy before size recheck
                return result  # do not falsify syscall's actual return count
            st.enter_context(patch.object(m, 'pwrite', changed))
        case('M11-' + str(size), 'MEMFD_COPY_SIZE', fault=bad_copy_size,
             kind='synthetic post-copy size corruption before sealing')
    case('M12', 'HANDOFF_REOPEN', fault=after_final(lambda p, o, tr, st, fd:
         m.fd_open(str(p / 'source.bin'), os.O_RDONLY)), kind='harness reopen guard; no reopen performed')
    def mapping(p, o, tr, st):
        original = m.fcntl
        def blocked(fd, op, *args):
            if op == m.F_ADD_SEALS:
                mm = mmap.mmap(fd, 3, flags=mmap.MAP_SHARED, prot=mmap.PROT_READ | mmap.PROT_WRITE)
                st.callback(mm.close)
                try: original(fd, op, *args)
                except OSError as e:
                    assert e.errno == errno.EBUSY, e
                    raise
                else: raise AssertionError('write sealing succeeded with writable mapping')
            return original(fd, op, *args)
        st.enter_context(patch.object(m, 'fcntl', blocked))
    case('M13', 'MEMFD_SEAL_APPLY', fault=mapping, kind='kernel enforcement: genuine writable mapping')
    case('M14-short', 'MEMFD_COPY_IO', fault=copy_data(b'ab'), kind='synthetic short write')
    def copy_error(p, o, tr, st):
        st.enter_context(patch.object(m, 'pwrite', side_effect=OSError(errno.EIO, 'injected')))
    case('M14-error', 'MEMFD_COPY_IO', fault=copy_error, kind='synthetic syscall error')
    case('M15-identity', 'OBSERVER_IDENTITY', setup=lambda p, o, st:
         o.update(pins=replace(pins, observer=('wrong', 'observe', k))), kind='synthetic identity expectation')
    case('M15-result', 'OBSERVER_RESULT', fault=wrong_result('observer'), counts=(1, 1), kind='synthetic result fault')

    def root_symlink(p, o, st):
        moved = p.parent / 'moved'; p.rename(moved); p.symlink_to(moved, target_is_directory=True)
    case('A-root-symlink', 'SYMLINK', setup=root_symlink)
    def root_file(p, o, st):
        p.rename(p.parent / 'moved'); p.write_bytes(b'')
    case('A-root-type', 'ROOT_TYPE', setup=root_file)
    case('A-hardlink', 'FILE_ALIAS', setup=lambda p, o, st: os.link(p / 'source.bin', p.parent / 'alias'))
    def unreadable(p, o, tr, st):
        original = m.fd_open
        def fail(path, *a, **kw):
            if path == 'source.bin': raise PermissionError(errno.EACCES, 'injected unreadable file')
            return original(path, *a, **kw)
        st.enter_context(patch.object(m, 'fd_open', fail))
    case('A-unreadable', 'IO_ERROR', fault=unreadable, kind='synthetic permission error unit case')
    case('A-oversize', 'MANIFEST_SIZE', setup=raw_manifest(b' ' * 1025))
    for label, value in [('bool', True), ('float', 3.0)]:
        case('A-type-' + label, 'SCHEMA_TYPE', setup=manifest(byte_length=value))
    case('A-type-path-list', 'SCHEMA_TYPE', setup=manifest(path=['source.bin']))
    case('A-type-array', 'SCHEMA_TYPE', setup=raw_manifest(b'[]'))
    case('A-duplicate-precedence', 'DUPLICATE_PATH', setup=raw_manifest(
        MANIFEST[:-1] + b',"schema":"x","path":"source.bin"}'))
    case('A-exclusive-boundary', 'ROOT_UNSTABLE', setup=lambda p, o, st: o.update(root=replace(o['root'], exclusive=False)))
    def unstable(p, o, tr, st):
        original = m._members
        calls = 0
        def changed(fd):
            nonlocal calls
            calls += 1
            if calls == 2: (p / 'source.bin').write_bytes(b'abd')
            return original(fd)
        st.enter_context(patch.object(m, '_members', changed))
    case('A-acquisition-change', 'ROOT_UNSTABLE', fault=unstable, kind='scheduled real fixture change')
    assert all(v == positives[0] for v in positives)
    assert {f'N{i:02}' for i in range(1, 32)} <= {v['case'].split('-')[0] for v in inventory}
    assert {f'M{i:02}' for i in range(1, 16)} <= {v['case'].split('-')[0] for v in inventory}
    result = dict(implementation_sha256=k, harness_sha256=t, total=len(inventory),
                  positive=sum(v['verdict'] == 'ACCEPT' for v in inventory),
                  negative=sum(v['verdict'] == 'REFUSE' for v in inventory),
                  all_passed=True, deterministic=True, offline_guard=True,
                  canonical_accept=positives[0].decode(), accept_sha256=H(positives[0]),
                  cases=inventory)
    print(C(result).decode())


if __name__ == '__main__':
    main()
