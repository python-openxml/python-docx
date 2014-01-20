# encoding: utf-8

"""
Test suite for docx.image.helpers module
"""

from __future__ import absolute_import, print_function

import pytest

from docx.compat import BytesIO
from docx.image.exceptions import UnexpectedEndOfFileError
from docx.image.helpers import BIG_ENDIAN, StreamReader


class DescribeStreamReader(object):

    def it_can_read_a_string_of_specified_len_at_offset(
            self, read_str_fixture):
        stream_rdr, expected_string = read_str_fixture
        s = stream_rdr.read_str(6, 2)
        assert s == 'foobar'

    def it_raises_on_unexpected_EOF(self, read_str_fixture):
        stream_rdr = read_str_fixture[0]
        with pytest.raises(UnexpectedEndOfFileError):
            stream_rdr.read_str(9, 2)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def read_str_fixture(self):
        stream = BytesIO(b'\x01\x02foobar\x03\x04')
        stream_rdr = StreamReader(stream, BIG_ENDIAN)
        expected_string = 'foobar'
        return stream_rdr, expected_string
