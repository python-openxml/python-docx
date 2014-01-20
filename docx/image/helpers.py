# encoding: utf-8

from __future__ import absolute_import, division, print_function

from struct import Struct

from .exceptions import UnexpectedEndOfFileError


BIG_ENDIAN = '>'
LITTLE_ENDIAN = '<'


class StreamReader(object):
    """
    Wraps a file-like object to provide access to structured data from a
    binary file. Byte-order is configurable. *base_offset* is added to any
    base value provided to calculate actual location for reads.
    """
    def __init__(self, stream, byte_order, base_offset=0):
        super(StreamReader, self).__init__()
        self._stream = stream
        self._byte_order = (
            LITTLE_ENDIAN if byte_order == LITTLE_ENDIAN else BIG_ENDIAN
        )
        self._base_offset = base_offset

    def read_str(self, char_count, base, offset=0):
        """
        Return a string containing the *char_count* bytes at the file
        position determined by self._base_offset + *base* + *offset*.
        """
        def str_struct(char_count):
            format_ = '%ds' % char_count
            return Struct(format_)
        struct = str_struct(char_count)
        chars = self._unpack_item(struct, base, offset)
        unicode_str = chars.decode('UTF-8')
        return unicode_str

    def seek(self, base, offset=0):
        location = self._base_offset + base + offset
        self._stream.seek(location)

    def _read_bytes(self, byte_count, base, offset):
        self.seek(base, offset)
        bytes_ = self._stream.read(byte_count)
        if len(bytes_) < byte_count:
            raise UnexpectedEndOfFileError
        return bytes_

    def _unpack_item(self, struct, base, offset):
        bytes_ = self._read_bytes(struct.size, base, offset)
        return struct.unpack(bytes_)[0]
