"""Direct bounded acceptance, no discovery or scientific imports. Pins precede bootstrap.

Run with external reviewed source hashes, an exclusive new retained store, and
custodian-assigned namespace. Payload is always inert abc; test adapters are explicit.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch


def h(raw):
    return hashlib.sha256(raw).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--implementation-sha256', required=True)
    p.add_argument('--harness-sha256', required=True)
    p.add_argument('--store', required=True)
    p.add_argument('--namespace', required=True)
    args = p.parse_args()
    if sys.flags.optimize:
        raise SystemExit('assertions must be enabled')
    repo = Path(__file__).resolve().parents[1]
    implementation = repo / 'e0/h2/consumption_boundary.py'
    assert h(implementation.read_bytes()) == args.implementation_sha256
    assert h(Path(__file__).read_bytes()) == args.harness_sha256
    legacy = repo / 'e0/h2/runtime_trust_root.py'
    assert h(legacy.read_bytes()) == 'd15ddd0b3d689592398987e62ce3135ee8a61e48ccd48cfa511d4870ac0b0023'
    assert h((repo / 'docs/e0/h2/NS-001_H2A2_CONSUMPTION_BOUNDARY_ACCEPTANCE_SPEC_v0.1.md').read_bytes()) == '7757f0d7fb8c8f27d2c7516e68c065ea4313b3fd8f013f6674a1e2c5f81799b6'
    # Inspect only our implementation source, never the synthetic supplied bytes.
    tree = ast.parse(implementation.read_bytes())
    receiver = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'receive')
    assert len(receiver.args.posonlyargs) == 6 and not receiver.args.args and not receiver.args.defaults
    assert not any(isinstance(n, (ast.Import, ast.ImportFrom, ast.Lambda)) for n in ast.walk(receiver))
    assert all(isinstance(n.func, ast.Name) and n.func.id in ('type', 'Refuse')
               for n in ast.walk(receiver) if isinstance(n, ast.Call))
    forbidden = {'eval', 'exec', 'compile', '__import__'}
    assert not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in forbidden for n in ast.walk(tree))
    m = load(implementation, 'ns001_consumption_acceptance')
    old = load(legacy, 'ns001_prior_handoff_support')
    root = Path(args.store).resolve()
    assert not root.exists(), 'use a new custody namespace/store; never overwrite evidence'
    root.mkdir()
    # Warm stdlib filesystem support before arming; no source supplied to compiler/loader.
    list(root.glob('unused*'))
    def offline(event, values):
        if event.startswith(('socket.', 'subprocess.', 'os.exec', 'os.spawn', 'os.posix_spawn')) or event in (
                'os.system', 'os.fork', 'os.forkpty', 'compile', 'exec'):
            raise AssertionError('forbidden runtime operation: ' + event)
    sys.addaudithook(offline)
    e = m.expectation(args.implementation_sha256, args.implementation_sha256, args.harness_sha256)
    monitor = m.Monitor()
    monitor.install()
    store = m.Store(root / 'store', args.namespace, e)
    results = []
    positive = []
    retained = []
    terminal_checks = []
    custody_checks = []

    def snapshot(directory):
        return {p.relative_to(directory).as_posix(): p.read_bytes().hex()
                for p in sorted(directory.rglob('*')) if p.is_file()}

    def stopped(operation):
        try:
            operation()
        except m.Stop as exc:
            return str(exc)
        raise AssertionError('operation did not stop')

    def check_aborted(a):
        before = snapshot(a.path)
        calls = monitor.entries
        # Test a fresh writer as well as the original live object. The fresh
        # writer must consult the retained disposition, not a cached flag.
        for writer_name, writer in (('original', a), ('fresh', m.Attempt(store, a.ordinal))):
            for state in ('PREPARED', 'ATTEMPTED', 'ACCEPTED', 'REFUSED'):
                message = stopped(lambda state=state: writer.event(state, witness={}, entered=False))
                if writer_name == 'fresh':
                    assert 'terminal' in message
                terminal_checks.append(dict(attempt_id=a.id, writer=writer_name, operation=state, result='STOP'))
            stopped(lambda: writer.register(m.C(m.request(e))))
            w = m.Witness(writer, monitor)
            stopped(lambda: m.invoke(w, b'abc'))
            terminal_checks.extend([dict(attempt_id=a.id, writer=writer_name, operation=op, result='STOP')
                                    for op in ('register', 'invoke')])
        assert monitor.entries == calls, 'ABORTED receiver resumed'
        assert snapshot(a.path) == before, 'ABORTED evidence changed'

    def acquisition(a):
        # Fresh exact frozen acquisition fixture, outside repository. No payload source import.
        fixture = root / ('fixture-' + str(a.ordinal))
        fixture.mkdir()
        manifest = dict(schema='ns001.h2a2.single-file.v1', path='source.bin', byte_length=3, sha256=m.F)
        (fixture / 'manifest.json').write_bytes(old.canonical(manifest))
        (fixture / 'source.bin').write_bytes(b'abc')
        bound = old.bind_root(str(fixture))
        try:
            payload = old._acquire(bound, str(fixture))
        finally:
            os.close(bound.fd)
        obj = m.Protected(payload)
        retained.append(obj)
        return obj

    def record(a, result, expected, note):
        assert result['state'] == expected[0], (note, result)
        assert result['primary_code'] == expected[1], (note, result)
        record = dict(case=note, attempt_id=a.id, state=result['state'], code=result['primary_code'],
                      terminal_sha256=m.H(m.C(result)))
        results.append(record)
        if result['state'] == 'ABORTED':
            check_aborted(a)
        return result

    def run(case, expected, variant='', request_change=None):
        a = store.reserve()
        w = m.Witness(a, monitor)
        r = m.request(e, case)
        if request_change:
            request_change(r)
        raw = m.C(r)
        a.register(raw)
        if variant == 'registration':
            return a, record(a, store.recover(a.ordinal), expected, case + '-' + variant)
        obj = acquisition(a)
        if variant in ('reopen', 'fallback', 'combined'):
            # An actual altered decoy exists, but the guard must never open it.
            (root / ('fixture-' + str(a.ordinal)) / 'source.bin').write_bytes(b'xyz')
        supplied = obj.fd
        if variant == 'initial-object':
            other = acquisition_object()
            supplied = other.fd
        if variant == 'short-read':
            real = m.os.pread
            def short(fd, count, offset):
                # Only the derivative request is shortened: initial measure finishes first.
                short.calls += 1
                return real(fd, 2 if short.calls == 2 else count, offset)
            short.calls = 0
            with patch.object(m.os, 'pread', short):
                parsed, b = m.prepare(a, w, obj, supplied, raw, args.implementation_sha256)
        else:
            parsed, b = m.prepare(a, w, obj, supplied, raw, args.implementation_sha256)
        attempted = False
        if parsed is not None:
            b = {'short': b'ab', 'long': b'abcd', 'alter': b'xyz', 'mutable': bytearray(b'abc')}.get(variant, b)
            if m.bind_derivative(w, b):
                selected = (lambda *ignored: None) if variant == 'wrong-consumer' else m.RECEIVER
                if variant == 'early':
                    try:
                        m.receive(w.b, *m.PARAMS.values())
                    except m.Refuse:
                        pass
                    w.fail('OBSERVER_NOT_ARMED')
                elif m.qualify(w, parsed, args.implementation_sha256, selected):
                    if variant == 'prepared':
                        a.event('PREPARED', entered=False)
                        return a, record(a, store.recover(a.ordinal), expected, case + '-' + variant)
                    m.dispatch(a, w)
                    attempted = True
                    if variant == 'attempted':
                        return a, record(a, store.recover(a.ordinal), expected, case + '-' + variant)
                    src = w.b
                    if variant in ('replace-a', 'combined'):
                        w.a = acquisition_object().fd
                    if variant in ('replace-b', 'equal-b'):
                        src = bytes(bytearray(b'xyz' if variant == 'replace-b' else b'abc'))
                        assert src is not w.b
                    if variant in ('reopen', 'fallback', 'combined'):
                        assert w.guard('filesystem_fallback' if variant == 'fallback' else 'payload_reopen') is False
                    count = 0 if variant == 'zero' else 2 if variant == 'two' else 1
                    for _ in range(count):
                        try:
                            if variant == 'rebound-consumer':
                                with patch.object(m, 'receive', lambda *ignored: None):
                                    m.invoke(w, src)
                            else:
                                m.invoke(w, src)
                        except m.Refuse:
                            pass
                    if variant == 'wrong-dispatch':
                        for observation in w.record['observations']:
                            if observation['kind'] == 'dispatch':
                                observation['data']['attempted_event_sha256'] = '0' * 64
                    if variant == 'missing':
                        assert any(x['kind'] == 'return' and x['data']['result'] == 'fixed_tuple' for x in w.record['observations'])
                        w.record['observations'] = [x for x in w.record['observations'] if x['kind'] != 'entry']
                        for i, o in enumerate(w.record['observations']):
                            o['index'] = i
                    if variant in ('wrong-id', 'torn'):
                        w.end('returned')
                        if variant == 'wrong-id':
                            w.record['attempt_id'] = '0' * 64 + ':999'
                        m.persist(a.path / 'witness.json', m.C(w.record))
                        if variant == 'torn':
                            m.persist(a.path / 'events.jsonl', b'{"attempt_id":', append=True)
                        return a, record(a, store.recover(a.ordinal), expected, case + '-' + variant)
        result = m.finish(a, w, attempted)
        if variant == 'combined':
            assert 'OBJECT_SUBSTITUTION' in result['diagnostics']
        record(a, result, expected, case + ('-' + variant if variant else ''))
        assert store.recover(a.ordinal) == result, 'valid terminal changed on recovery'
        if case == 'P01':
            positive.append((a, w.record, result))
        return a, result

    def acquisition_object():
        # Explicit equal-byte unrelated object for identity-substitution tests only.
        obj = m.Protected(b'abc')
        retained.append(obj)
        return obj

    try:
        run('P01', ('ACCEPTED', None))
        run('P01', ('ACCEPTED', None))
        cases = [('N01', 'initial-object', 'WRONG_PROTECTED_OBJECT'),
                 ('N02', 'short-read', 'INPUT_IO'), ('N03', 'short', 'INPUT_TRUNCATED'),
                 ('N04', 'long', 'INPUT_APPENDED'), ('N05', 'alter', 'INPUT_ALTERED'),
                 ('N06', 'mutable', 'INPUT_TYPE'), ('N07', 'replace-a', 'OBJECT_SUBSTITUTION'),
                 ('N08', 'replace-b', 'OBJECT_SUBSTITUTION'), ('N08', 'equal-b', 'OBJECT_SUBSTITUTION'),
                 ('N09', 'reopen', 'PATHNAME_REOPEN'), ('N10', 'wrong-consumer', 'WRONG_LOADER'),
                 ('N10', 'rebound-consumer', 'WRONG_LOADER'),
                 ('N13', 'early', 'OBSERVER_NOT_ARMED'), ('N14', 'missing', 'OBSERVATION_MISSING'),
                 ('N14', 'wrong-dispatch', 'OBSERVATION_MISSING'),
                 ('N16', 'fallback', 'PATHNAME_REOPEN'), ('N17', 'zero', 'INVOCATION_COUNT'),
                 ('N17', 'two', 'INVOCATION_COUNT'), ('N09', 'combined', 'PATHNAME_REOPEN')]
        for case, variant, code in cases:
            run(case, ('REFUSED', code), variant)
        run('N11', ('REFUSED', 'WRONG_ENTRYPOINT'), request_change=lambda r: r['parameters'].update(filename='wrong'))
        for key in ('PYTHONPATH', 'PYTHONHOME'):
            run('N12', ('REFUSED', 'SOURCE_REDIRECTION'), request_change=lambda r, k=key: r['source_environment'].update({k: 'untrusted'}))
        run('N12', ('REFUSED', 'SOURCE_REDIRECTION'), request_change=lambda r: r.update(source_channel='stdin'))
        run('N12', ('REFUSED', 'SOURCE_REDIRECTION'), request_change=lambda r: r.update(cwd_policy='wrong'))
        run('N19', ('REFUSED', 'EXPECTATION_INVALID'), request_change=lambda r: r.pop('expectation_sha256'))
        run('N20', ('REFUSED', 'PROFILE_UNQUALIFIED'), request_change=lambda r: r.update(profile='ns001.h2a2.compile-input-real.v1'))
        run('N20', ('REFUSED', 'PROFILE_UNQUALIFIED'), request_change=lambda r: r.update(profile='unknown'))
        for variant in ('registration', 'prepared', 'attempted', 'torn'):
            a, result = run('N15', ('ABORTED', 'ATTEMPT_INCOMPLETE'), variant)
            assert store.recover(a.ordinal) == result
        a = store.reserve()
        result = store.recover(a.ordinal)
        record(a, result, ('ABORTED', 'ATTEMPT_INCOMPLETE'), 'N15-reservation')
        assert store.recover(a.ordinal) == result
        run('N18', ('ABORTED', 'RECORD_INVALID'), 'wrong-id')
        # Exact witness swap across real distinct positive attempts; preserve originals.
        a = store.reserve()
        a.register(m.C(m.request(e, 'N14')))
        m.persist(a.path / 'witness.json', m.C(positive[0][1]))
        record(a, store.recover(a.ordinal), ('ABORTED', 'RECORD_INVALID'), 'N14-swapped-witness')
        # Interrupt a genuine recovery write. Keep its raw prefix, then reopen
        # the store and finish recovery without resuming receiver consumption.
        a = store.reserve()
        a.register(m.C(m.request(e, 'N15')))
        actual_persist = m.persist
        def interrupt_recovery(path, raw, append=False):
            if Path(path).name == 'recovery1.partial':
                actual_persist(path, raw[:37], append)
                raise OSError('controlled recovery write interruption')
            return actual_persist(path, raw, append)
        try:
            with patch.object(m, 'persist', interrupt_recovery):
                store.recover(a.ordinal)
        except OSError:
            pass
        else:
            raise AssertionError('recovery interruption was not exercised')
        prefix = (a.path / 'recovery1.partial').read_bytes()
        assert len(prefix) == 37 and not (a.path / 'recovery.json').exists()
        store.close()
        store = m.Store(root / 'store', args.namespace, e)
        result = store.recover(a.ordinal)
        record(a, result, ('ABORTED', 'ATTEMPT_INCOMPLETE'), 'N15-recovery-write-restart')
        assert store.recover(a.ordinal) == result
        assert (a.path / 'recovery1.partial').read_bytes() == prefix
        # Reopening/recovering must preserve every previously valid terminal byte.
        for directory in store.path.iterdir():
            if not directory.is_dir():
                continue
            before = {p.name: p.read_bytes() for p in directory.iterdir()}
            store.recover(int(directory.name))
            assert before == {p.name: p.read_bytes() for p in directory.iterdir()}
        # F2: new isolated malformed registrations; originals are not rewritten.
        registration_cases = [
            ('null', b'null\n', 'RECORD_INVALID'), ('number', b'1\n', 'RECORD_INVALID'),
            ('boolean', b'true\n', 'RECORD_INVALID'), ('string', b'"wrong"\n', 'RECORD_INVALID'),
            ('array', b'[]\n', 'RECORD_INVALID'), ('nested-array', b'[[1]]\n', 'RECORD_INVALID'),
            ('object', b'{}\n', 'RECORD_INVALID'), ('syntax', b'{bad}\n', 'RECORD_INVALID'),
            ('duplicate', b'{"schema":1,"schema":2}\n', 'RECORD_INVALID'),
            ('unicode', b'\xff\n', 'RECORD_INVALID'),
            ('torn', b'{"schema":', 'ATTEMPT_INCOMPLETE'),
            ('empty', b'', 'ATTEMPT_INCOMPLETE'), ('missing', None, 'ATTEMPT_INCOMPLETE')]
        for label, raw, expected_code in registration_cases:
            a = store.reserve()
            m.persist(a.path / 'request.json', m.C(m.request(e, 'N18')))
            if raw is not None:
                m.persist(a.path / 'registration.json', raw)
            prior = snapshot(a.path)
            result = store.recover(a.ordinal)
            record(a, result, ('ABORTED', expected_code), 'F2-' + label)
            assert store.recover(a.ordinal) == result
            assert all(snapshot(a.path)[k] == v for k, v in prior.items())

        # F1: damage only new custody fixtures. Keep before/after byte maps.
        custody_cases = ('missing-store', 'missing-pin', 'missing-lock', 'malformed-store',
                         'malformed-pin', 'conflicting-store', 'conflicting-pin', 'valid',
                         'live-missing-store', 'live-missing-pin')
        for label in custody_cases:
            path = root / ('custody-' + label)
            ns = h((args.namespace + ':' + label).encode('ascii'))
            side = m.Store(path, ns, e)
            side_attempt = side.reserve()
            side_attempt.register(m.C(m.request(e)))
            before = snapshot(path)
            if not label.startswith('live-'):
                side.close()
            target = path / ('store.json' if label.endswith('store') else 'lock' if label.endswith('lock') else m.H(m.C(e)) + '.json')
            if 'missing' in label:
                target.unlink()
            elif label == 'malformed-store' or label == 'malformed-pin':
                target.write_bytes(b'null\n')
            elif label == 'conflicting-store':
                target.write_bytes(m.C(dict(schema='ns001.h2a2.store.v1', namespace='0' * 64)))
            elif label == 'conflicting-pin':
                altered = dict(e, input_sha256='0' * 64)
                target.write_bytes(m.C(altered))
            damaged = snapshot(path)
            if label == 'valid':
                reopened = m.Store(path, ns, e)
                reopened.close()
                assert snapshot(path) == before
                outcomes = ['UNCHANGED']
            elif label.startswith('live-'):
                outcomes = [stopped(side.reserve), stopped(lambda: side.recover(side_attempt.ordinal)),
                            stopped(lambda: side_attempt.event('PREPARED', entered=False))]
                side.close()
            else:
                outcomes = [stopped(lambda: m.Store(path, ns, e))]
            assert snapshot(path) == damaged, 'custody metadata silently repaired'
            custody_checks.append(dict(case=label, result='UNCHANGED' if label == 'valid' else 'STOP',
                                       outcomes=outcomes))
            m.persist(root / ('custody-' + label + '-observations.json'),
                      m.C(dict(before=before, damaged=damaged, after=snapshot(path))))
        empty = root / 'custody-existing-empty'
        empty.mkdir()
        stopped(lambda: m.Store(empty, h((args.namespace + ':empty').encode()), e))
        assert not list(empty.iterdir())
        custody_checks.append(dict(case='existing-empty', result='STOP', outcomes=['no files recreated']))

        # Serialized data round trip uses actual files; no fabricated observed records.
        total = 0
        for directory in store.path.iterdir():
            if not directory.is_dir():
                continue
            for path in directory.iterdir():
                if path.suffix not in ('.json', '.jsonl'):
                    continue
                for line in path.read_bytes().splitlines(keepends=True):
                    if line.endswith(b'\n'):
                        try:
                            parsed = m.parse(line)
                        except (ValueError, UnicodeError):
                            # F2 deliberately retains invalid raw JSON. It is
                            # classified and hashed by recovery, not normalized.
                            assert path.name == 'registration.json'
                        else:
                            assert m.C(parsed) == line
                            total += 1
        x, y = positive[0][1], positive[1][1]
        def semantic(w):
            w = json.loads(json.dumps(w))
            w.pop('attempt_id')
            for o in w['observations']:
                if o['kind'] == 'dispatch':
                    o['data'].pop('attempted_event_sha256')
            return w
        assert semantic(x) == semantic(y)
        assert positive[0][0].id != positive[1][0].id
        assert m.C(positive[0][2]) != m.C(positive[1][2])
        summary = dict(schema='ns001.h2a2.consumption-acceptance.v1', cases=results,
                       positive_count=sum(x['state'] == 'ACCEPTED' for x in results),
                       refusal_count=sum(x['state'] == 'REFUSED' for x in results),
                       recovery_count=sum(x['state'] == 'ABORTED' for x in results),
                       roundtrip_records=total, semantic_repeat_equal=True,
                       implementation_sha256=args.implementation_sha256, harness_sha256=args.harness_sha256)
        summary.update(custody_checks=custody_checks, terminal_checks=terminal_checks)
        m.persist(root / 'acceptance.json', m.C(summary))
        print(m.C(summary).decode(), end='')
    finally:
        monitor.witness = None
        monitor.close()
        for obj in retained:
            obj.close()
        store.close()


if __name__ == '__main__':
    main()
