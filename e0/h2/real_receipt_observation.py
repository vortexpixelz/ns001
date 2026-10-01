"""Offline MI records and paired native observations; never connects to a debugger."""
from dataclasses import dataclass
import re
from .real_receipt_policy import Invalid, digest, DIGEST, FIXTURE, parameters_match, ranked
from .real_receipt_abi import Decoder, Snapshot


@dataclass(frozen=True)
class MIRecord:
    raw: bytes
    token: int | None
    channel: str
    kind: str
    fields: object


class MIParser:
    """Bounded MI2 grammar, preserving async/stream records and duplicate errors."""
    def __init__(self, maximum=8 * 1024 * 1024):
        self.maximum = maximum
        self.total = 0
        self.pending = None
        self.last_token = 0
        self.records = []

    def command(self, raw):
        from .real_receipt_policy import mi_command
        m = re.fullmatch(rb'([1-9][0-9]*)(-[^\n]+)\n', raw)
        if not m or self.pending is not None:
            raise Invalid('one outstanding MI command')
        token = int(m[1])
        if token <= self.last_token or mi_command(token, m[2].decode('ascii')) != raw:
            raise Invalid('monotonic allowlisted command')
        self.last_token = token
        self.pending = token

    def feed(self, raw, channel='stdout'):
        self.total += len(raw)
        if self.total > self.maximum or len(raw) > 65536 or not raw.endswith(b'\n'):
            raise Invalid('MI transcript bound/framing')
        if channel == 'stderr':
            record = MIRecord(raw, None, channel, 'stderr', None)
        elif channel != 'stdout':
            raise Invalid('inferior channel cannot be MI')
        elif raw in (b'(gdb)\n', b'(gdb) \n'):
            record = MIRecord(raw, None, channel, 'prompt', None)
        else:
            try:
                text = raw[:-1].decode('ascii')
            except UnicodeError as exc:
                raise Invalid('MI ASCII') from exc
            m = re.match(r'([0-9]*)([\^*+=~@&])', text)
            if not m:
                raise Invalid('MI record prefix')
            token = int(m[1]) if m[1] else None
            prefix = m[2]
            parser = _Grammar(text[m.end():])
            if prefix in '~@&':
                if token is not None:
                    raise Invalid('stream token')
                fields = parser.string()
                kind = prefix
            else:
                kind = prefix + parser.identifier()
                fields = parser.results(',')
            if parser.i != len(parser.s):
                raise Invalid('MI trailing data')
            if prefix == '^':
                if token is None or token != self.pending:
                    raise Invalid('result token association')
                self.pending = None
                if kind == '^error':
                    # Preserve error and stop. No retry/resume is generated.
                    self.records.append(MIRecord(raw, token, channel, kind, fields))
                    raise Invalid('MI command failed')
            record = MIRecord(raw, token, channel, kind, fields)
        self.records.append(record)
        return record


class _Grammar:
    def __init__(self, s):
        self.s, self.i = s, 0

    def identifier(self):
        m = re.match(r'[A-Za-z_][A-Za-z_0-9-]*', self.s[self.i:])
        if not m:
            raise Invalid('MI identifier')
        self.i += len(m[0])
        return m[0]

    def string(self):
        if self.s[self.i:self.i + 1] != '"':
            raise Invalid('MI C string')
        self.i += 1
        out = bytearray()
        escapes = {'n': 10, 'r': 13, 't': 9, 'b': 8, 'f': 12, 'v': 11,
                   'a': 7, '\\': 92, '"': 34, "'": 39}
        while self.i < len(self.s):
            c = self.s[self.i]
            self.i += 1
            if c == '"':
                return bytes(out)
            if c == '\\':
                if self.i == len(self.s):
                    raise Invalid('MI escape')
                c = self.s[self.i]
                self.i += 1
                if c in escapes:
                    out.append(escapes[c])
                elif c in '01234567':
                    m = re.match(r'[0-7]{0,2}', self.s[self.i:])[0]
                    self.i += len(m)
                    value = int(c + m, 8)
                    if value > 255:
                        raise Invalid('MI octal byte')
                    out.append(value)
                else:
                    raise Invalid('MI unknown escape')
            elif ord(c) < 32:
                raise Invalid('MI control byte')
            else:
                out.append(ord(c))
        raise Invalid('MI unterminated string')

    def value(self, depth=0):
        if depth > 16:
            raise Invalid('MI nesting')
        c = self.s[self.i:self.i + 1]
        if c == '"':
            return self.string()
        if c not in ('{', '['):
            raise Invalid('MI value')
        self.i += 1
        end = '}' if c == '{' else ']'
        if self.s[self.i:self.i + 1] == end:
            self.i += 1
            return {} if c == '{' else []
        is_result = self.s[self.i:self.i + 1] not in ('"', '{', '[')
        if c == '{' and not is_result:
            raise Invalid('MI tuple requires results')
        result = {} if is_result and c == '{' else []
        while True:
            if is_result:
                key = self.identifier()
                if (type(result) is dict and key in result) or self.s[self.i:self.i + 1] != '=':
                    raise Invalid('MI duplicate/result')
                self.i += 1
                value = self.value(depth + 1)
                if type(result) is dict:
                    result[key] = value
                else:
                    result.append({key: value})  # MI result lists preserve repeated names/order.
            else:
                result.append(self.value(depth + 1))
            c = self.s[self.i:self.i + 1]
            self.i += 1
            if c == end:
                return result
            if c != ',':
                raise Invalid('MI delimiter')

    def results(self, delimiter):
        result = {}
        while self.i < len(self.s):
            if self.s[self.i] != delimiter:
                raise Invalid('MI result separator')
            self.i += 1
            key = self.identifier()
            if key in result or self.s[self.i:self.i + 1] != '=':
                raise Invalid('MI duplicate result')
            self.i += 1
            result[key] = self.value()
        return result


@dataclass(frozen=True)
class Stop:
    index: int
    pid: int
    tid: int
    custody: str
    registers: dict
    reads: tuple
    roots: tuple
    reason: str
    token: int


@dataclass(frozen=True)
class Derivation:
    attempt: str
    a_identity: str
    fd: int
    wrapper: int
    sites: tuple
    syscall_number: int
    syscall_fd: int
    count: int
    offset: int
    result: int
    syscall_capture: bytes
    original_buffer: int
    post_resize_b: int
    return_b: int
    ready_b: int
    return_pc_in: int
    return_pc_out: int
    syscall_entries: int
    syscall_exits: int
    seals_before: int
    seals_after: int
    size_before: int
    size_after: int
    uninterrupted: bool


def derivation_codes(d, x, a):
    if d.attempt != x:
        return ['RECORD_INVALID']
    if d.a_identity != a or d.seals_before != 15 or d.seals_after != 15 or d.size_before != 2 or d.size_after != 2:
        return ['WRONG_PROTECTED_OBJECT']
    if (d.wrapper != 0x4f6102 or d.sites != (0x4f6102, 0x4f6224, 0x4f6274, 0x4f6299)
            or d.syscall_number != 17 or d.syscall_fd != d.fd or d.count != 3 or d.offset != 0
            or d.result != 2 or d.syscall_entries != 1 or d.syscall_exits != 1
            or d.uninterrupted is not True or d.return_pc_in != d.return_pc_out
            or any(type(v) is not int or not 0 < v < 2**64 for v in
                   (d.original_buffer, d.return_pc_in, d.return_pc_out))
            or type(d.fd) is not int or not 0 <= d.fd < 2**31
            or type(d.syscall_fd) is not int
            or type(d.syscall_capture) is not bytes or len(d.syscall_capture) != 2):
        return ['INPUT_IO']
    if not d.post_resize_b or not (d.post_resize_b == d.return_b == d.ready_b):
        return ['OBJECT_SUBSTITUTION']
    return []


def paired_codes(caller, receiver, x, e, b, c, m, step_token):
    if caller is None or receiver is None:
        return ['OBSERVATION_MISSING']
    r, s = caller.registers, receiver.registers
    if (caller.index >= receiver.index or caller.pid != receiver.pid or caller.tid != receiver.tid
            or caller.custody != receiver.custody or not caller.custody
            or caller.reason != 'qualified-hardware-caller'
            or receiver.reason != 'qualified-in-place-call-receiver'
            or receiver.token != step_token or step_token <= caller.token):
        return ['OBSERVATION_MISSING']
    try:
        if s['rip'] != 0x69bff0 or r['rip'] != 0x581feb:
            return ['ENGINE_UNQUALIFIED']
        if r['rax'] != 0x69bff0 or r['r12'] != c or s['r12'] != c:
            return ['WRONG_COMPILE_CALLABLE']
        if r['rdx'] != 6 or s['rdx'] != 6:
            return ['WRONG_ENTRYPOINT']
        if (s['rsp'] != r['rsp'] - 8 or any(r[k] != s[k] for k in ('rdi', 'rsi', 'rdx', 'rcx'))
                or r['rdi'] != m):
            return ['OBSERVATION_MISSING']
        if caller.roots != (b, c, m) or receiver.roots != caller.roots:
            return ['OBJECT_SUBSTITUTION']
        a, z = Decoder(Snapshot(caller.reads)), Decoder(Snapshot(receiver.reads))
        if z.s.number(s['rsp']) != 0x581fed:
            return ['OBSERVATION_MISSING']
        if a.roots(m, x, e) != caller.roots or z.roots(m, x, e) != receiver.roots:
            return ['OBJECT_SUBSTITUTION']
        av, ap, ab = a.arguments(r, b)
        zv, zp, zb = z.arguments(s, b)
        if av != zv or ab != zb:
            return ['OBJECT_SUBSTITUTION']
        if not parameters_match(ap) or not parameters_match(zp):
            return ['WRONG_ENTRYPOINT']
    except Invalid as exc:
        if str(exc) in ('sole keyword', 'six positional objects', 'True singleton',
                        'exact type str', 'exact type int', 'exact type bool'):
            return ['WRONG_ENTRYPOINT']
        return ['OBSERVATION_MISSING']
    except (KeyError, TypeError, OverflowError):
        return ['OBSERVATION_MISSING']
    return []


def byte_codes(raw, observed_length, observed_digest, b, retained_b, a_capture,
               derived_capture, ready_capture, attempt, expected_attempt, exact_type=True):
    faults = []
    if attempt != expected_attempt:
        faults.append('RECORD_INVALID')
    if not exact_type:
        faults.append('INPUT_TYPE')
    elif type(observed_length) is not int or observed_length < 0:
        faults.append('OBSERVATION_MISSING')
    elif observed_length < 2:
        faults.append('INPUT_TRUNCATED')
    elif observed_length > 2:
        faults.append('INPUT_APPENDED')
    elif type(raw) is not bytes or len(raw) != observed_length:
        faults.append('OBSERVATION_MISSING')
    elif digest(raw) != observed_digest:
        faults.append('OBSERVATION_MISSING')
    elif raw != FIXTURE or observed_digest != DIGEST:
        faults.append('INPUT_ALTERED')
    if b != retained_b or not b:
        faults.append('OBJECT_SUBSTITUTION')
    if any(type(v) is not bytes or v != raw for v in (a_capture, derived_capture, ready_capture)):
        faults.append('OBSERVATION_MISSING')
    return ranked(faults)


@dataclass(frozen=True)
class Capture:
    """Forensic input boundary; synthetic instances are not genuine native evidence."""
    attempt: str
    expectation_sha256: str
    attempted_sha256: str
    released_attempted_sha256: str
    caller: Stop | None
    receiver: Stop | None
    step_token: int
    derivation: Derivation
    a_identity: str
    a_capture: bytes
    b_ready: bytes
    b: int
    c: int
    m: int
    entry_count: int
    observer_entry_count: int
    interruption: bool
    completion: dict
    engine: dict
    pins: dict
    artifacts: dict
    q1_settings: dict
    q1_facts: dict


def evaluate_capture(capture, x, ehash, attempted):
    """Return normal ranked faults or ABORT for interrupted capture.

    This validates offline data; it cannot establish the provenance of a live
    ptrace stop, raw unmasked read, or the supplied admission facts.
    """
    from .real_receipt_policy import engine_admission, validate_q1
    if capture.interruption is not False:
        return 'ABORT', ['ATTEMPT_INCOMPLETE']
    if capture.attempt != x or capture.expectation_sha256 != ehash:
        return 'REFUSE', ['RECORD_INVALID']
    faults = []
    if capture.attempted_sha256 != attempted or capture.released_attempted_sha256 != attempted:
        faults.append('OBSERVATION_MISSING')
    faults += engine_admission(capture.engine, capture.pins, capture.artifacts)
    faults += validate_q1(capture.q1_settings, capture.q1_facts)
    faults += derivation_codes(capture.derivation, x, capture.a_identity)
    faults += paired_codes(capture.caller, capture.receiver, x, ehash, capture.b,
                           capture.c, capture.m, capture.step_token)
    if capture.derivation.ready_b != capture.b:
        faults.append('OBJECT_SUBSTITUTION')
    if (type(capture.entry_count) is not int or type(capture.observer_entry_count) is not int or
            capture.entry_count != 1 or capture.observer_entry_count != 1):
        faults.append('INVOCATION_COUNT')
    expected_completion = {'stopped_at_entry': True, 'capture_synced': True,
                           'final_associations': True, 'kill_requested': True,
                           'pidfd_death_confirmed': True, 'debugger_exit_confirmed': True,
                           'transcript_drained': True, 'no_resume': True,
                           'guard_coverage_complete': True}
    if (type(capture.completion) is not dict or capture.completion != expected_completion or
                any(type(v) is not bool for v in capture.completion.values())):
        return 'ABORT', ranked(faults + ['ATTEMPT_INCOMPLETE'], recovery=True)
    if capture.receiver is not None:
        try:
            decoder = Decoder(Snapshot(capture.receiver.reads))
            source = decoder.s.number(capture.receiver.registers['rsi'])
            if source != capture.b:
                faults.append('OBJECT_SUBSTITUTION')
            if decoder.s.number(source + 8) != 0xa2bee0:
                faults.append('INPUT_TYPE')
            else:
                length = decoder.s.number(source + 16, signed=True)
                if length < 0:
                    faults.append('OBSERVATION_MISSING')
                elif length != 2:
                    faults.append('INPUT_TRUNCATED' if length < 2 else 'INPUT_APPENDED')
                else:
                    raw = decoder.bytes(source)
                    faults += byte_codes(raw, length, digest(raw), source, capture.b,
                        capture.a_capture, capture.derivation.syscall_capture,
                        capture.b_ready, x, capture.attempt)
        except (Invalid, KeyError, TypeError):
            faults.append('OBSERVATION_MISSING')
    faults = ranked(faults)
    return ('REFUSE' if faults else 'ACCEPT'), faults
