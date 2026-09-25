"""Offline abc-only sealed-memfd handoff. No source execution or E0 integration.

The caller is the reviewed, exclusively owning synthetic harness. Source pins and
observations are externally checked by that harness, not authenticated by this module.
No callbacks, selectable consumers, plugins, path-based consumption or mutable backend.
"""
from dataclasses import dataclass
from hashlib import sha256
import json
import re
import stat
from os import (open as fd_open, close, fstat, stat as fd_stat, listdir, read,
                pread, pwrite, memfd_create, O_RDONLY, O_DIRECTORY, O_NOFOLLOW,
                O_CLOEXEC, O_NONBLOCK, MFD_ALLOW_SEALING, MFD_CLOEXEC)
from fcntl import (fcntl, F_ADD_SEALS, F_GET_SEALS, F_DUPFD_CLOEXEC,
                   F_GETFD, FD_CLOEXEC, F_SEAL_WRITE, F_SEAL_GROW,
                   F_SEAL_SHRINK, F_SEAL_SEAL)

PROFILE = 'ns001.h2a2.sealed-memfd.v1'
F = 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
M = '4a9ebe2c4e275600d9a6c7864bb14c3d5a4c0b6a7c8bbf88193fc48f76affce0'
S = '0ae1c30f2568188390fe05d092609eb122f3bee16c48f41fae9fe3f08e6ba432'
Q = F_SEAL_WRITE | F_SEAL_GROW | F_SEAL_SHRINK | F_SEAL_SEAL
L = ['F_SEAL_GROW', 'F_SEAL_SEAL', 'F_SEAL_SHRINK', 'F_SEAL_WRITE']
FLAGS = MFD_ALLOW_SEALING | MFD_CLOEXEC
CV = 'ns001.h2a2.identity-consumer.v1'
OV = 'ns001.h2a2.identity-observer.v1'


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode('ascii')


class Refusal(Exception):
    """Stable contract code; never include host exception text in evidence."""


def require(condition, code):
    if not condition:
        raise Refusal(code)


def refusal(code):
    return canonical(dict(profile=PROFILE, verdict='REFUSE', code=code,
                          handoff_succeeded=False))


def identity(info):
    return info.st_dev, info.st_ino


def _walk(path):
    require(isinstance(path, str) and path.startswith('/') and path != '/'
            and all(p not in ('', '.', '..') for p in path[1:].split('/'))
            and '\x00' not in path, 'ROOT_MISMATCH')
    fd = fd_open('/', O_RDONLY | O_DIRECTORY | O_NOFOLLOW | O_CLOEXEC)
    try:
        for part in path[1:].split('/'):
            try:
                info = fd_stat(part, dir_fd=fd, follow_symlinks=False)
                require(not stat.S_ISLNK(info.st_mode), 'SYMLINK')
                require(stat.S_ISDIR(info.st_mode), 'ROOT_TYPE')
                nxt = fd_open(part, O_RDONLY | O_DIRECTORY | O_NOFOLLOW | O_CLOEXEC,
                              dir_fd=fd)
            except FileNotFoundError:
                raise Refusal('ROOT_MISSING') from None
            except OSError:
                raise Refusal('IO_ERROR') from None
            close(fd)
            fd = nxt
        return fd
    except BaseException:
        close(fd)
        raise


@dataclass(frozen=True)
class Root:
    path: str
    fd: int
    key: tuple
    exclusive: bool


def bind_root(path):
    """Harness calls before validation; it owns and eventually closes this handle."""
    fd = _walk(path)
    return Root(path, fd, identity(fstat(fd)), True)


@dataclass(frozen=True)
class Pins:
    implementation: str
    harness: str
    observed_implementation: str
    observed_harness: str
    consumer: tuple
    observer: tuple


def _policy(pins, expected):
    require(expected == (F, 3, M, S), 'EXPECTED_IDENTITY')
    require(re.fullmatch('[0-9a-f]{64}', pins.implementation) is not None
            and pins.implementation != '0' * 64
            and pins.observed_implementation == pins.implementation
            and pins.consumer == (CV, 'consume', pins.implementation)
            and consume is _FIXED_CONSUMER, 'CONSUMER_IDENTITY')
    require(pins.observer == (OV, 'observe', pins.implementation)
            and observe is _FIXED_OBSERVER, 'OBSERVER_IDENTITY')
    require(re.fullmatch('[0-9a-f]{64}', pins.harness) is not None
            and pins.harness != '0' * 64
            and pins.observed_harness == pins.harness, 'EVIDENCE_INCOMPLETE')


def _members(fd):
    names = sorted(listdir(fd), key=lambda n: n.encode('utf-8', 'surrogateescape'))
    entries = [(n, fd_stat(n, dir_fd=fd, follow_symlinks=False)) for n in names]
    require(not any(stat.S_ISLNK(s.st_mode) for _, s in entries), 'SYMLINK')
    require(all(stat.S_ISREG(s.st_mode) for _, s in entries), 'ENTRY_TYPE')
    require(all(s.st_nlink == 1 for _, s in entries), 'FILE_ALIAS')
    require('source.bin' in names, 'FILE_MISSING')
    require('manifest.json' in names, 'MANIFEST_MISSING')
    require(names == ['manifest.json', 'source.bin'], 'EXTRA_FILE')
    return {n: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
            for n, s in entries}


def _read_member(fd, name, count, before):
    item = fd_open(name, O_RDONLY | O_NOFOLLOW | O_CLOEXEC | O_NONBLOCK, dir_fd=fd)
    try:
        s = fstat(item)
        require(stat.S_ISREG(s.st_mode) and s.st_nlink == 1, 'ROOT_UNSTABLE')
        require((s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
                == before[name], 'ROOT_UNSTABLE')
        return read(item, count)
    finally:
        close(item)


class _Pairs(list):
    pass


def _manifest(raw):
    require(len(raw) <= 1024, 'MANIFEST_SIZE')
    try:
        def reject_constant(_):
            raise ValueError
        parsed = json.loads(raw.decode('utf-8'), object_pairs_hook=_Pairs,
                            parse_constant=reject_constant)
    except (ValueError, UnicodeError, RecursionError):
        raise Refusal('MANIFEST_MALFORMED') from None
    duplicates = []
    def scan(value):
        if isinstance(value, _Pairs):
            seen = set()
            for k, v in value:
                if k in seen:
                    duplicates.append(k)
                seen.add(k)
                scan(v)
        elif isinstance(value, list):
            for v in value:
                scan(v)
    scan(parsed)
    require('path' not in duplicates, 'DUPLICATE_PATH')
    require(not duplicates, 'DUPLICATE_KEY')
    require(isinstance(parsed, _Pairs), 'SCHEMA_TYPE')
    value = dict(parsed)
    types = {'schema': str, 'path': str, 'byte_length': int, 'sha256': str}
    require(all(type(v) is types[k] for k, v in value.items() if k in types), 'SCHEMA_TYPE')
    require(set(types) <= set(value), 'MANIFEST_FIELD_MISSING')
    require(set(value) == set(types), 'MANIFEST_FIELD_UNKNOWN')
    require(value['schema'] == 'ns001.h2a2.single-file.v1', 'MANIFEST_VERSION')
    path = value['path']
    require(not (path.startswith(('/', '\\\\')) or re.match('^[A-Za-z]:', path)), 'PATH_ABSOLUTE')
    require(not (any(c in ('.', '..') for c in path.replace('\\', '/').split('/'))
                 or '\\' in path), 'PATH_TRAVERSAL')
    require(path == 'source.bin', 'FILE_PATH')
    require(value['byte_length'] == 3, 'MANIFEST_LENGTH')
    require(value['sha256'] == F, 'MANIFEST_DIGEST')
    require(raw == canonical(value), 'MANIFEST_NONCANONICAL')
    require(sha256(raw).hexdigest() == M, 'MANIFEST_HASH')
    return value


def _acquire(root, supplied):
    require(supplied == root.path, 'ROOT_MISMATCH')
    check = _walk(root.path)
    try:
        require(identity(fstat(check)) == root.key == identity(fstat(root.fd)), 'ROOT_MISMATCH')
        require(root.exclusive, 'ROOT_UNSTABLE')
        before = _members(check)
        manifest = _read_member(check, 'manifest.json', 1025, before)
        value = _manifest(manifest)
        payload = _read_member(check, 'source.bin', 4, before)
        require(len(payload) == 3, 'FILE_LENGTH')
        require(sha256(payload).hexdigest() == F, 'FILE_DIGEST')
        require(_members(check) == before, 'ROOT_UNSTABLE')
        descriptor = dict(file=value, manifest_sha256=sha256(manifest).hexdigest(),
                          root_id='ns001-h2a2-fixture-v1', schema='ns001.h2a2.snapshot.v1')
        require(sha256(canonical(descriptor)).hexdigest() == S, 'SNAPSHOT_IDENTITY')
        return payload
    finally:
        close(check)


def _copy_check(fd):
    try:
        size = fstat(fd).st_size
        data = pread(fd, 4, 0)
    except OSError:
        raise Refusal('MEMFD_COPY_IO') from None
    require(size == len(data) == 3, 'MEMFD_COPY_SIZE')
    require(sha256(data).hexdigest() == F, 'MEMFD_COPY_DIGEST')


def _seal(fd):
    try:
        require(fcntl(fd, F_ADD_SEALS, Q) == 0, 'MEMFD_SEAL_APPLY')
    except OSError:
        raise Refusal('MEMFD_SEAL_APPLY') from None
    try:
        require(fcntl(fd, F_GET_SEALS) == Q, 'MEMFD_SEAL_SET')
    except OSError:
        raise Refusal('MEMFD_SEAL_SET') from None


def _finalize(fd):
    _copy_check(fd)
    _seal(fd)
    _copy_check(fd)
    return identity(fstat(fd))


def _boundary(handles, key):
    try:
        facts = [fstat(fd) for fd in handles]
        require(all(identity(s) == key for s in facts), 'HANDOFF_SUBSTITUTED')
        require(all(fcntl(fd, F_GET_SEALS) == Q for fd in handles), 'HANDOFF_UNPROTECTED')
        require(all(stat.S_ISREG(s.st_mode) for s in facts)
                and all(fcntl(fd, F_GETFD) & FD_CLOEXEC for fd in handles), 'MEMFD_HANDLE')
        data = pread(handles[0], 4, 0)
        require(all(s.st_size == 3 for s in facts) and len(data) == 3
                and sha256(data).hexdigest() == F, 'HANDOFF_MUTATED')
    except OSError:
        raise Refusal('HANDOFF_UNPROTECTED') from None


# Deliberate independent role measurements: neither delegates to the other or
# shares a byte buffer/digest result. Only the standard hash implementation is shared.
def consume(fd):
    info = fstat(fd)
    seals = fcntl(fd, F_GET_SEALS)
    data = pread(fd, 4, 0)
    digest = sha256(data).hexdigest()
    require(stat.S_ISREG(info.st_mode) and info.st_size == len(data) == 3
            and digest == F and seals == Q, 'CONSUMER_RESULT')
    return dict(byte_length=len(data), sha256=digest, seal_mask=seals,
                st_dev=info.st_dev, st_ino=info.st_ino, regular_file=True)


def observe(fd):
    info = fstat(fd)
    seals = fcntl(fd, F_GET_SEALS)
    data = pread(fd, 4, 0)
    digest = sha256(data).hexdigest()
    require(stat.S_ISREG(info.st_mode) and info.st_size == len(data) == 3
            and digest == F and seals == Q, 'OBSERVER_RESULT')
    return dict(byte_length=len(data), sha256=digest, seal_mask=seals,
                st_dev=info.st_dev, st_ino=info.st_ino, regular_file=True)


_FIXED_CONSUMER = consume
_FIXED_OBSERVER = observe


def _result(value, key, role, pin):
    code = 'CONSUMER_RESULT' if role == 'consumer' else 'OBSERVER_RESULT'
    expected = dict(byte_length=3, sha256=F, seal_mask=Q, st_dev=key[0],
                    st_ino=key[1], regular_file=True)
    require(type(value) is dict and value == expected
            and all(type(value[k]) is type(v) for k, v in expected.items()), code)
    return dict(role=role, source_sha256=pin, object_type='sealed-memfd',
                byte_length=3, sha256=F, seals=L.copy(), reference_bound=True)


def _receipt(pins, consumer, observer):
    require(consumer is not None and observer is not None, 'EVIDENCE_INCOMPLETE')
    # Content tuple required by the abstract contract, with M/S retained by validator.
    content = dict(byte_length=consumer['byte_length'], sha256=consumer['sha256'],
                   manifest_sha256=M, snapshot_sha256=S)
    require(content == dict(byte_length=3, sha256=F, manifest_sha256=M, snapshot_sha256=S),
            'EVIDENCE_INCOMPLETE')
    return canonical(dict(profile=PROFILE, verdict='ACCEPT', snapshot_sha256=S,
                          manifest_sha256=M, source_sha256=F, byte_length=3,
                          implementation_sha256=pins.implementation, harness_sha256=pins.harness,
                          consumer=consumer, observer=observer,
                          checks=dict(source_validated=True, copy_validated=True,
                                      sealed_revalidated=True, creation_witnessed=True,
                                      duplication_witnessed=True, same_object=True,
                                      no_reopen=True, consumer_calls=1, observer_calls=1)))


def _handoff(a, key, pins):
    c = o = None
    try:
        _boundary((a,), key)
        c = fcntl(a, F_DUPFD_CLOEXEC, 0)
        _boundary((a, c), key)
        o = fcntl(a, F_DUPFD_CLOEXEC, 0)
        handles = (a, c, o)
        _boundary(handles, key)
        require(consume is _FIXED_CONSUMER, 'CONSUMER_IDENTITY')
        try:
            cr = consume(c)
        except OSError:
            raise Refusal('CONSUMER_RESULT') from None
        _boundary(handles, key)
        consumer = _result(cr, key, 'consumer', pins.implementation)
        _boundary(handles, key)
        require(observe is _FIXED_OBSERVER, 'OBSERVER_IDENTITY')
        try:
            ob = observe(o)
        except OSError:
            raise Refusal('OBSERVER_RESULT') from None
        _boundary(handles, key)
        observer = _result(ob, key, 'observer', pins.implementation)
        _boundary(handles, key)
        return _receipt(pins, consumer, observer)
    except OSError:
        raise Refusal('MEMFD_HANDLE') from None
    finally:
        if o is not None:
            close(o)
        if c is not None:
            close(c)


def _protected(payload, pins):
    try:
        a = memfd_create('ns001-h2a2-handoff', FLAGS)
    except OSError:
        raise Refusal('MEMFD_CREATE') from None
    try:
        facts = fstat(a)
        require(stat.S_ISREG(facts.st_mode) and facts.st_size == 0
                and fcntl(a, F_GETFD) & FD_CLOEXEC
                and fcntl(a, F_GET_SEALS) == 0, 'MEMFD_CAPABILITY')
        try:
            require(pwrite(a, payload, 0) == 3, 'MEMFD_COPY_IO')
        except OSError:
            raise Refusal('MEMFD_COPY_IO') from None
        key = _finalize(a)
        return _handoff(a, key, pins)
    finally:
        close(a)


def run(root, supplied, pins, expected=(F, 3, M, S)):
    """One attempt; no fallback or repair. Harness independently validates evidence.

    root is a live prebound capability from bind_root, never a manifest parameter.
    Pins contain hashes checked before import by the external trusted test harness.
    """
    try:
        _policy(pins, expected)
        payload = _acquire(root, supplied)
        return _protected(payload, pins)
    except Refusal as exc:
        return refusal(str(exc))
    except OSError:
        return refusal('IO_ERROR')
