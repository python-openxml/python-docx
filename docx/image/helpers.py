# encoding: utf-8

from __future__ import absolute_import, division, print_function


_BIG_ENDIAN = '>'
_LITTLE_ENDIAN = '<'


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
            _LITTLE_ENDIAN if byte_order == _LITTLE_ENDIAN else _BIG_ENDIAN
        )
        self._base_offset = base_offset
