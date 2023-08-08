import itertools
import sys
import struct
from io import open, BytesIO, SEEK_CUR, SEEK_END  # noqa

PY2 = sys.version_info[0] == 2

# Kaitai Struct runtime version, in the format defined by PEP 440.
# Used by our setup.cfg to set the version number in
# packaging/distribution metadata.
# Also used in Python code generated by older ksc versions (0.7 through 0.9)
# to check that the imported runtime is compatible with the generated code.
# Since ksc 0.10, the compatibility check instead uses the API_VERSION constant,
# so that the version string does not need to be parsed at runtime
# (see https://github.com/kaitai-io/kaitai_struct/issues/804).
__version__ = '0.10'

# Kaitai Struct runtime API version, as a tuple of ints.
# Used in generated Python code (since ksc 0.10) to check that the imported
# runtime is compatible with the generated code.
API_VERSION = (0, 10)

# pylint: disable=invalid-name,missing-docstring,too-many-public-methods
# pylint: disable=useless-object-inheritance,super-with-arguments,consider-using-f-string


class KaitaiStruct(object):
    def __init__(self, stream):
        self._io = stream

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def close(self):
        self._io.close()

    @classmethod
    def from_file(cls, filename):
        f = open(filename, 'rb')
        try:
            return cls(KaitaiStream(f))
        except Exception:
            # close file descriptor, then reraise the exception
            f.close()
            raise

    @classmethod
    def from_bytes(cls, buf):
        return cls(KaitaiStream(BytesIO(buf)))

    @classmethod
    def from_io(cls, io):
        return cls(KaitaiStream(io))


class KaitaiStream(object):
    def __init__(self, io):
        self._io = io
        self.align_to_byte()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def close(self):
        self._io.close()

    # region Stream positioning

    def is_eof(self):
        if self.bits_left > 0:
            return False

        io = self._io
        t = io.read(1)
        if t == b'':
            return True

        io.seek(-1, SEEK_CUR)
        return False

    def seek(self, n):
        self._io.seek(n)

    def pos(self):
        return self._io.tell()

    def size(self):
        # Python has no internal File object API function to get
        # current file / StringIO size, thus we use the following
        # trick.
        io = self._io
        # Remember our current position
        cur_pos = io.tell()
        # Seek to the end of the stream and remember the full length
        full_size = io.seek(0, SEEK_END)
        # Seek back to the current position
        io.seek(cur_pos)
        return full_size

    # endregion

    # region Structs for numeric types

    packer_s1 = struct.Struct('b')
    packer_s2be = struct.Struct('>h')
    packer_s4be = struct.Struct('>i')
    packer_s8be = struct.Struct('>q')
    packer_s2le = struct.Struct('<h')
    packer_s4le = struct.Struct('<i')
    packer_s8le = struct.Struct('<q')

    packer_u1 = struct.Struct('B')
    packer_u2be = struct.Struct('>H')
    packer_u4be = struct.Struct('>I')
    packer_u8be = struct.Struct('>Q')
    packer_u2le = struct.Struct('<H')
    packer_u4le = struct.Struct('<I')
    packer_u8le = struct.Struct('<Q')

    packer_f4be = struct.Struct('>f')
    packer_f8be = struct.Struct('>d')
    packer_f4le = struct.Struct('<f')
    packer_f8le = struct.Struct('<d')

    # endregion

    # region Integer numbers

    # region Signed

    def read_s1(self):
        return KaitaiStream.packer_s1.unpack(self.read_bytes(1))[0]

    # region Big-endian

    def read_s2be(self):
        return KaitaiStream.packer_s2be.unpack(self.read_bytes(2))[0]

    def read_s4be(self):
        return KaitaiStream.packer_s4be.unpack(self.read_bytes(4))[0]

    def read_s8be(self):
        return KaitaiStream.packer_s8be.unpack(self.read_bytes(8))[0]

    # endregion

    # region Little-endian

    def read_s2le(self):
        return KaitaiStream.packer_s2le.unpack(self.read_bytes(2))[0]

    def read_s4le(self):
        return KaitaiStream.packer_s4le.unpack(self.read_bytes(4))[0]

    def read_s8le(self):
        return KaitaiStream.packer_s8le.unpack(self.read_bytes(8))[0]

    # endregion

    # endregion

    # region Unsigned

    def read_u1(self):
        return KaitaiStream.packer_u1.unpack(self.read_bytes(1))[0]

    # region Big-endian

    def read_u2be(self):
        return KaitaiStream.packer_u2be.unpack(self.read_bytes(2))[0]

    def read_u4be(self):
        return KaitaiStream.packer_u4be.unpack(self.read_bytes(4))[0]

    def read_u8be(self):
        return KaitaiStream.packer_u8be.unpack(self.read_bytes(8))[0]

    # endregion

    # region Little-endian

    def read_u2le(self):
        return KaitaiStream.packer_u2le.unpack(self.read_bytes(2))[0]

    def read_u4le(self):
        return KaitaiStream.packer_u4le.unpack(self.read_bytes(4))[0]

    def read_u8le(self):
        return KaitaiStream.packer_u8le.unpack(self.read_bytes(8))[0]

    # endregion

    # endregion

    # endregion

    # region Floating point numbers

    # region Big-endian

    def read_f4be(self):
        return KaitaiStream.packer_f4be.unpack(self.read_bytes(4))[0]

    def read_f8be(self):
        return KaitaiStream.packer_f8be.unpack(self.read_bytes(8))[0]

    # endregion

    # region Little-endian

    def read_f4le(self):
        return KaitaiStream.packer_f4le.unpack(self.read_bytes(4))[0]

    def read_f8le(self):
        return KaitaiStream.packer_f8le.unpack(self.read_bytes(8))[0]

    # endregion

    # endregion

    # region Unaligned bit values

    def align_to_byte(self):
        self.bits_left = 0
        self.bits = 0

    def read_bits_int_be(self, n):
        res = 0

        bits_needed = n - self.bits_left
        self.bits_left = -bits_needed % 8

        if bits_needed > 0:
            # 1 bit  => 1 byte
            # 8 bits => 1 byte
            # 9 bits => 2 bytes
            bytes_needed = ((bits_needed - 1) // 8) + 1  # `ceil(bits_needed / 8)`
            buf = self.read_bytes(bytes_needed)
            if PY2:
                buf = bytearray(buf)
            for byte in buf:
                res = res << 8 | byte

            new_bits = res
            res = res >> self.bits_left | self.bits << bits_needed
            self.bits = new_bits  # will be masked at the end of the function
        else:
            res = self.bits >> -bits_needed  # shift unneeded bits out

        mask = (1 << self.bits_left) - 1  # `bits_left` is in range 0..7
        self.bits &= mask

        return res

    # Unused since Kaitai Struct Compiler v0.9+ - compatibility with
    # older versions.
    def read_bits_int(self, n):
        return self.read_bits_int_be(n)

    def read_bits_int_le(self, n):
        res = 0
        bits_needed = n - self.bits_left

        if bits_needed > 0:
            # 1 bit  => 1 byte
            # 8 bits => 1 byte
            # 9 bits => 2 bytes
            bytes_needed = ((bits_needed - 1) // 8) + 1  # `ceil(bits_needed / 8)`
            buf = self.read_bytes(bytes_needed)
            if PY2:
                buf = bytearray(buf)
            for i, byte in enumerate(buf):
                res |= byte << (i * 8)

            new_bits = res >> bits_needed
            res = res << self.bits_left | self.bits
            self.bits = new_bits
        else:
            res = self.bits
            self.bits >>= n

        self.bits_left = -bits_needed % 8

        mask = (1 << n) - 1  # no problem with this in Python (arbitrary precision integers)
        res &= mask
        return res

    # endregion

    # region Byte arrays

    def read_bytes(self, n):
        if n < 0:
            raise ValueError(
                "requested invalid %d amount of bytes" %
                (n,)
            )

        is_satisfiable = True
        # When a large number of bytes is requested, try to check first
        # that there is indeed enough data left in the stream.
        # This avoids reading large amounts of data only to notice afterwards
        # that it's not long enough. For smaller amounts of data, it's faster to
        # first read the data unconditionally and check the length afterwards.
        if (
            n >= 8*1024*1024  # = 8 MiB
            # in Python 2, there is a common error ['file' object has no
            # attribute 'seekable'], so we need to make sure that seekable() exists
            and callable(getattr(self._io, 'seekable', None))
            and self._io.seekable()
        ):
            num_bytes_available = self.size() - self.pos()
            is_satisfiable = (n <= num_bytes_available)

        if is_satisfiable:
            r = self._io.read(n)
            num_bytes_available = len(r)
            is_satisfiable = (n <= num_bytes_available)

        if not is_satisfiable:
            # noinspection PyUnboundLocalVariable
            raise EOFError(
                "requested %d bytes, but only %d bytes available" %
                (n, num_bytes_available)
            )

        # noinspection PyUnboundLocalVariable
        return r

    def read_bytes_full(self):
        return self._io.read()

    def read_bytes_term(self, term, include_term, consume_term, eos_error):
        r = b''
        while True:
            c = self._io.read(1)
            if c == b'':
                if eos_error:
                    raise Exception(
                        "end of stream reached, but no terminator %d found" %
                        (term,)
                    )

                return r

            if ord(c) == term:
                if include_term:
                    r += c
                if not consume_term:
                    self._io.seek(-1, SEEK_CUR)
                return r

            r += c

    def ensure_fixed_contents(self, expected):
        actual = self._io.read(len(expected))
        if actual != expected:
            raise Exception(
                "unexpected fixed contents: got %r, was waiting for %r" %
                (actual, expected)
            )
        return actual

    @staticmethod
    def bytes_strip_right(data, pad_byte):
        return data.rstrip(KaitaiStream.byte_from_int(pad_byte))

    @staticmethod
    def bytes_terminate(data, term, include_term):
        new_data, term_byte, _ = data.partition(KaitaiStream.byte_from_int(term))
        if include_term:
            new_data += term_byte
        return new_data

    # endregion

    # region Byte array processing

    @staticmethod
    def process_xor_one(data, key):
        if PY2:
            return bytes(bytearray(v ^ key for v in bytearray(data)))

        return bytes(v ^ key for v in data)

    @staticmethod
    def process_xor_many(data, key):
        if PY2:
            return bytes(bytearray(a ^ b for a, b in zip(bytearray(data), itertools.cycle(bytearray(key)))))

        return bytes(a ^ b for a, b in zip(data, itertools.cycle(key)))

    @staticmethod
    def process_rotate_left(data, amount, group_size):
        if group_size != 1:
            raise Exception(
                "unable to rotate group of %d bytes yet" %
                (group_size,)
            )

        anti_amount = -amount % (group_size * 8)

        r = bytearray(data)
        for i, byte in enumerate(r):
            r[i] = (byte << amount) & 0xff | (byte >> anti_amount)
        return bytes(r)

    # endregion

    # region Misc runtime operations

    @staticmethod
    def int_from_byte(v):
        return ord(v) if PY2 else v

    @staticmethod
    def byte_from_int(i):
        return chr(i) if PY2 else bytes((i,))

    @staticmethod
    def byte_array_index(data, i):
        return KaitaiStream.int_from_byte(data[i])

    @staticmethod
    def byte_array_min(b):
        return KaitaiStream.int_from_byte(min(b))

    @staticmethod
    def byte_array_max(b):
        return KaitaiStream.int_from_byte(max(b))

    @staticmethod
    def resolve_enum(enum_obj, value):
        """Resolves value using enum: if the value is not found in the map,
        we'll just use literal value per se. Works around problem with Python
        enums throwing an exception when encountering unknown value.
        """
        try:
            return enum_obj(value)
        except ValueError:
            return value

    # endregion


class KaitaiStructError(Exception):
    """Common ancestor for all error originating from Kaitai Struct usage.
    Stores KSY source path, pointing to an element supposedly guilty of
    an error.
    """
    def __init__(self, msg, src_path):
        super(KaitaiStructError, self).__init__("%s: %s" % (src_path, msg))
        self.src_path = src_path


class UndecidedEndiannessError(KaitaiStructError):
    """Error that occurs when default endianness should be decided with
    switch, but nothing matches (although using endianness expression
    implies that there should be some positive result).
    """
    def __init__(self, src_path):
        super(UndecidedEndiannessError, self).__init__("unable to decide on endianness for a type", src_path)


class ValidationFailedError(KaitaiStructError):
    """Common ancestor for all validation failures. Stores pointer to
    KaitaiStream IO object which was involved in an error.
    """
    def __init__(self, msg, io, src_path):
        super(ValidationFailedError, self).__init__("at pos %d: validation failed: %s" % (io.pos(), msg), src_path)
        self.io = io


class ValidationNotEqualError(ValidationFailedError):
    """Signals validation failure: we required "actual" value to be equal to
    "expected", but it turned out that it's not.
    """
    def __init__(self, expected, actual, io, src_path):
        super(ValidationNotEqualError, self).__init__("not equal, expected %s, but got %s" % (repr(expected), repr(actual)), io, src_path)
        self.expected = expected
        self.actual = actual


class ValidationLessThanError(ValidationFailedError):
    """Signals validation failure: we required "actual" value to be
    greater than or equal to "min", but it turned out that it's not.
    """
    def __init__(self, min_bound, actual, io, src_path):
        super(ValidationLessThanError, self).__init__("not in range, min %s, but got %s" % (repr(min_bound), repr(actual)), io, src_path)
        self.min = min_bound
        self.actual = actual


class ValidationGreaterThanError(ValidationFailedError):
    """Signals validation failure: we required "actual" value to be
    less than or equal to "max", but it turned out that it's not.
    """
    def __init__(self, max_bound, actual, io, src_path):
        super(ValidationGreaterThanError, self).__init__("not in range, max %s, but got %s" % (repr(max_bound), repr(actual)), io, src_path)
        self.max = max_bound
        self.actual = actual


class ValidationNotAnyOfError(ValidationFailedError):
    """Signals validation failure: we required "actual" value to be
    from the list, but it turned out that it's not.
    """
    def __init__(self, actual, io, src_path):
        super(ValidationNotAnyOfError, self).__init__("not any of the list, got %s" % (repr(actual)), io, src_path)
        self.actual = actual


class ValidationExprError(ValidationFailedError):
    """Signals validation failure: we required "actual" value to match
    the expression, but it turned out that it doesn't.
    """
    def __init__(self, actual, io, src_path):
        super(ValidationExprError, self).__init__("not matching the expression, got %s" % (repr(actual)), io, src_path)
        self.actual = actual