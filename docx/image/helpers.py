# encoding: utf-8

from __future__ import absolute_import, division, print_function


class StreamReader(object):
    """
    Wraps a file-like object to provide access to structured data from a
    binary file. Byte-order is configurable. *base_offset* is added to any
    base value provided to calculate actual location for reads.
    """
