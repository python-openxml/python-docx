"""Test suite for docx.image.helpers module."""

import io

import pytest

from docx.image.exceptions import UnexpectedEndOfFileError
from docx.image.helpers import BIG_ENDIAN, LITTLE_ENDIAN, StreamReader


class DescribeStreamReader:
    def it_can_read_a_string_of_specified_len_at_offset(self, read_str_fixture):
        stream_rdr, expected_string = read_str_fixture
        s = stream_rdr.read_str(6, 2)
        assert s == "foobar"

    def it_raises_on_unexpected_EOF(self, read_str_fixture):
        stream_rdr = read_str_fixture[0]
        with pytest.raises(UnexpectedEndOfFileError):
            stream_rdr.read_str(9, 2)

    def it_can_read_a_long(self, read_long_fixture):
        stream_rdr, offset, expected_int = read_long_fixture
        long_ = stream_rdr.read_long(offset)
        assert long_ == expected_int

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            (BIG_ENDIAN, b"\xBE\x00\x00\x00\x2A\xEF", 1, 42),
            (LITTLE_ENDIAN, b"\xBE\xEF\x2A\x00\x00\x00", 2, 42),
        ]
    )
    def read_long_fixture(self, request):
        byte_order, bytes_, offset, expected_int = request.param
        stream = io.BytesIO(bytes_)
        stream_rdr = StreamReader(stream, byte_order)
        return stream_rdr, offset, expected_int

    @pytest.fixture
    def read_str_fixture(self):
        stream = io.BytesIO(b"\x01\x02foobar\x03\x04")
        stream_rdr = StreamReader(stream, BIG_ENDIAN)
        expected_string = "foobar"
        return stream_rdr, expected_string
