"""Bounded CPython 3.12.3 LP64 decoding of supplied offline snapshots only."""
from dataclasses import dataclass
from .real_receipt_policy import Invalid, PARAMETERS

TYPES = dict(bytes=0xa2bee0, tuple=0xa42c40, str=0xa472c0, int=0xa3bf20,
             bool=0xa2a3a0, cfunction=0xa3fb20, module=0xa3ff00, dict=0xa3d840)
TRUE = 0xa2a360


@dataclass(frozen=True)
class Read:
    address: int
    requested: int
    data: bytes


class Snapshot:
    """Disjoint addressed captures; missing/truncated bytes are never manufactured."""
    def __init__(self, reads):
        self.reads = tuple(reads)
        intervals = []
        for r in self.reads:
            self.range(r.address, r.requested)
            if type(r.data) is not bytes or len(r.data) != r.requested:
                raise Invalid('partial observation')
            intervals.append((r.address, r.address + r.requested))
        intervals.sort()
        if any(a[1] > b[0] for a, b in zip(intervals, intervals[1:])):
            raise Invalid('overlapping observation')
        self.total = 0

    @staticmethod
    def range(address, count):
        if (type(address) is not int or type(count) is not int or
                address <= 0 or count < 0 or count > 65536 or address + count > 2**64):
            raise Invalid('bounded address range')

    def read(self, address, count):
        self.range(address, count)
        self.total += count
        if self.total > 8 * 1024 * 1024:
            raise Invalid('snapshot read budget')
        for r in self.reads:
            if r.address <= address and address + count <= r.address + len(r.data):
                start = address - r.address
                return r.data[start:start + count]
        raise Invalid('missing addressed bytes')

    def number(self, address, width=8, signed=False):
        return int.from_bytes(self.read(address, width), 'little', signed=signed)


class Decoder:
    def __init__(self, snapshot, bias=0):
        if bias != 0 or type(bias) is not int:
            raise Invalid('frozen ET_EXEC bias')
        self.s = snapshot

    def exact(self, p, kind):
        if self.s.number(p + 8) != TYPES[kind]:
            raise Invalid('exact type ' + kind)

    def vector(self, p, count=7):
        if type(count) is not int or not 0 <= count <= 7:
            raise Invalid('vector bound')
        raw = self.s.read(p, count * 8)
        result = tuple(int.from_bytes(raw[i:i + 8], 'little') for i in range(0, len(raw), 8))
        if any(x == 0 for x in result):
            raise Invalid('null object')
        return result

    def tuple(self, p, maximum=4):
        self.exact(p, 'tuple')
        n = self.s.number(p + 16, signed=True)
        if type(maximum) is not int or not 0 <= n <= maximum <= 4:
            raise Invalid('tuple bound')
        return self.vector(p + 24, n)

    def bytes(self, p, maximum=3):
        self.exact(p, 'bytes')
        n = self.s.number(p + 16, signed=True)
        if type(maximum) is not int or not 0 <= n <= maximum <= 3:
            raise Invalid('bytes bound')
        raw = self.s.read(p + 32, n)
        if self.s.read(p + 32 + n, 1) != b'\0':
            raise Invalid('bytes terminator')
        return raw

    def unicode(self, p):
        self.exact(p, 'str')
        n = self.s.number(p + 16, signed=True)
        state = self.s.number(p + 32, 4)
        kind, compact, ascii_ = (state >> 2) & 7, bool(state & 32), bool(state & 64)
        # CPython 3.12 has no ready bit. Interned bits 0..1 and static bit 7 exist.
        if not 0 <= n <= 4096 or kind not in (1, 2, 4) or state & ~255:
            raise Invalid('Unicode layout')
        if ascii_ and (not compact or kind != 1):
            raise Invalid('ASCII layout')
        data = p + (40 if ascii_ else 56) if compact else self.s.number(p + 56)
        raw = self.s.read(data, n * kind)
        if self.s.read(data + n * kind, kind) != bytes(kind):
            raise Invalid('Unicode terminator')
        scalars = [int.from_bytes(raw[i:i + kind], 'little') for i in range(0, len(raw), kind)]
        if any(x > 0x10ffff or 0xd800 <= x <= 0xdfff or (ascii_ and x > 127) for x in scalars):
            raise Invalid('Unicode scalar')
        return ''.join(chr(x) for x in scalars)

    def long(self, p, kind='int'):
        self.exact(p, kind)
        tag = self.s.number(p + 16)
        n, sign = tag >> 3, tag & 3
        if n > 4 or sign == 3 or ((n == 0) != (sign == 1)):
            raise Invalid('long tag')
        raw = self.s.read(p + 24, n * 4)
        digits = [int.from_bytes(raw[i:i + 4], 'little') for i in range(0, len(raw), 4)]
        if any(x >= 2**30 for x in digits) or (digits and digits[-1] == 0):
            raise Invalid('long normalization')
        value = sum(x << (30 * i) for i, x in enumerate(digits))
        return -value if sign == 2 else value

    def boolean(self, p):
        if p != TRUE or self.long(p, 'bool') != 1:
            raise Invalid('True singleton')
        return True

    def callable(self, c, m):
        self.exact(c, 'cfunction')
        ml = self.s.number(c + 16)
        if (ml != 0xa49ae0 or self.s.number(c + 24) != m or
                self.s.number(c + 48) != 0x581f90 or self.s.number(ml + 8) != 0x69bff0 or
                self.s.number(ml + 16, 4) != 0x82):
            raise Invalid('compile callable association')
        return c

    def dictionary(self, p):
        self.exact(p, 'dict')
        header = self.s.read(p + 16, 32)
        used, version, k, values = [int.from_bytes(header[i:i + 8], 'little')
                                   for i in range(0, 32, 8)]
        if used > 4096:
            raise Invalid('dict used')
        logsize = self.s.number(k + 8, 1)
        logbytes = self.s.number(k + 9, 1)
        kind = self.s.number(k + 10, 1)
        n = self.s.number(k + 24, signed=True)
        usable = self.s.number(k + 16, signed=True)
        if (logsize > 12 or logbytes > 16 or kind not in (0, 1, 2) or
                not 0 <= n <= 4096 or not 0 <= usable <= 4096 or
                n + usable > (2 * (1 << logsize)) // 3 or used > n or
                bool(values) != (kind == 2)):
            raise Invalid('dict layout')
        slots, indexbytes = 1 << logsize, 1 << logbytes
        width = indexbytes // slots
        if width not in (1, 2, 4, 8) or width * slots != indexbytes:
            raise Invalid('dict index width')
        indices = self.s.read(k + 32, indexbytes)
        active_indices = []
        for i in range(0, len(indices), width):
            x = int.from_bytes(indices[i:i + width], 'little', signed=True)
            if not -2 <= x < n:
                raise Invalid('dict index range')
            if x >= 0:
                active_indices.append(x)
        if len(set(active_indices)) != len(active_indices):
            raise Invalid('duplicate dict index')
        entries = k + 32 + indexbytes
        stride = 24 if kind == 0 else 16
        result = {}
        for i in range(n):
            key = self.s.number(entries + i * stride + (8 if kind == 0 else 0))
            value = self.s.number(values + i * 8) if values else self.s.number(entries + i * stride + stride - 8)
            if key == 0 or value == 0:
                if value != 0 or (not values and i in active_indices):
                    raise Invalid('deleted dict entry')
                continue
            if i not in active_indices:
                raise Invalid('unindexed dict entry')
            text = self.unicode(key)
            if text in result:
                raise Invalid('duplicate dict key')
            result[text] = value
        if len(result) != used or self.s.read(p + 16, 32) != header:
            raise Invalid('dict count/stability')
        return result, version

    def roots(self, m, x, e):
        self.exact(m, 'module')
        d = self.s.number(m + 16)
        bindings, version = self.dictionary(d)
        try:
            b, c, xp, ep = self.tuple(bindings['_ns001_observer_roots_v1'])
        except (KeyError, ValueError) as exc:
            raise Invalid('four roots required') from exc
        if self.unicode(xp) != x or self.unicode(ep) != e or bindings.get('compile') != c:
            raise Invalid('root/binding association')
        self.callable(c, m)
        if self.dictionary(d) != (bindings, version):
            raise Invalid('root stability')
        return b, c, m

    def arguments(self, regs, expected_b):
        if regs['rdx'] != 6:
            raise Invalid('six positional objects')
        names = self.tuple(regs['rcx'], 1)
        if len(names) != 1 or self.unicode(names[0]) != '_feature_version':
            raise Invalid('sole keyword')
        vector = self.vector(regs['rsi'])
        b, filename, mode, flags, inherit, optimize, feature = vector
        if b != expected_b:
            raise Invalid('B substitution')
        actual = dict(filename=self.unicode(filename), mode=self.unicode(mode),
                      flags=self.long(flags), dont_inherit=self.boolean(inherit),
                      optimize=self.long(optimize), _feature_version=self.long(feature))
        return vector, actual, self.bytes(b)
