# encoding: utf-8

"""
Test suite for docx.image.tiff module
"""

from __future__ import absolute_import, print_function

import pytest

from docx.compat import BytesIO
from docx.image.helpers import BIG_ENDIAN, LITTLE_ENDIAN, StreamReader
from docx.image.tiff import (
    _IfdEntries, _IfdEntry, _IfdParser, Tiff, _TiffParser
)

from ..unitutil import (
    initializer_mock, class_mock, instance_mock, method_mock
)


class DescribeTiff(object):

    def it_can_construct_from_a_tiff_stream(self, from_stream_fixture):
        (stream_, blob_, filename_, _TiffParser_, Tiff__init_, px_width,
         px_height, horz_dpi, vert_dpi) = from_stream_fixture
        tiff = Tiff.from_stream(stream_, blob_, filename_)
        _TiffParser_.parse.assert_called_once_with(stream_)
        Tiff__init_.assert_called_once_with(
            blob_, filename_, px_width, px_height, horz_dpi, vert_dpi
        )
        assert isinstance(tiff, Tiff)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def blob_(self, request):
        return instance_mock(request, bytes)

    @pytest.fixture
    def filename_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def from_stream_fixture(
            self, stream_, blob_, filename_, _TiffParser_, tiff_parser_,
            Tiff__init_):
        px_width, px_height = 111, 222
        horz_dpi, vert_dpi = 333, 444
        tiff_parser_.px_width = px_width
        tiff_parser_.px_height = px_height
        tiff_parser_.horz_dpi = horz_dpi
        tiff_parser_.vert_dpi = vert_dpi
        return (
            stream_, blob_, filename_, _TiffParser_, Tiff__init_, px_width,
            px_height, horz_dpi, vert_dpi
        )

    @pytest.fixture
    def Tiff__init_(self, request):
        return initializer_mock(request, Tiff)

    @pytest.fixture
    def _TiffParser_(self, request, tiff_parser_):
        _TiffParser_ = class_mock(request, 'docx.image.tiff._TiffParser')
        _TiffParser_.parse.return_value = tiff_parser_
        return _TiffParser_

    @pytest.fixture
    def tiff_parser_(self, request):
        return instance_mock(request, _TiffParser)

    @pytest.fixture
    def stream_(self, request):
        return instance_mock(request, BytesIO)


class Describe_TiffParser(object):

    def it_can_parse_the_properties_from_a_tiff_stream(
            self, from_stream_fixture):
        (stream_, _make_stream_reader_, _IfdEntries_, ifd0_offset_,
         stream_rdr_, _TiffParser__init_, ifd_entries_) = from_stream_fixture
        tiff_parser = _TiffParser.parse(stream_)
        _make_stream_reader_.assert_called_once_with(stream_)
        _IfdEntries_.from_stream.assert_called_once_with(
            stream_rdr_, ifd0_offset_
        )
        _TiffParser__init_.assert_called_once_with(ifd_entries_)
        assert isinstance(tiff_parser, _TiffParser)

    def it_makes_a_stream_reader_to_help_parse(self, mk_stream_rdr_fixture):
        stream, StreamReader_, endian, stream_rdr_ = mk_stream_rdr_fixture
        stream_rdr = _TiffParser._make_stream_reader(stream)
        StreamReader_.assert_called_once_with(stream, endian)
        assert stream_rdr is stream_rdr_

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def from_stream_fixture(
            self, stream_, _make_stream_reader_, _IfdEntries_, ifd0_offset_,
            stream_rdr_, _TiffParser__init_, ifd_entries_):
        return (
            stream_, _make_stream_reader_, _IfdEntries_, ifd0_offset_,
            stream_rdr_, _TiffParser__init_, ifd_entries_
        )

    @pytest.fixture
    def _IfdEntries_(self, request, ifd_entries_):
        _IfdEntries_ = class_mock(request, 'docx.image.tiff._IfdEntries')
        _IfdEntries_.from_stream.return_value = ifd_entries_
        return _IfdEntries_

    @pytest.fixture
    def ifd_entries_(self, request):
        return instance_mock(request, _IfdEntries)

    @pytest.fixture
    def ifd0_offset_(self, request):
        return instance_mock(request, int)

    @pytest.fixture
    def _make_stream_reader_(self, request, stream_rdr_):
        return method_mock(
            request, _TiffParser, '_make_stream_reader',
            return_value=stream_rdr_
        )

    @pytest.fixture(params=[
        (b'MM\x00*', BIG_ENDIAN),
        (b'II*\x00', LITTLE_ENDIAN),
    ])
    def mk_stream_rdr_fixture(self, request, StreamReader_, stream_rdr_):
        bytes_, endian = request.param
        stream = BytesIO(bytes_)
        return stream, StreamReader_, endian, stream_rdr_

    @pytest.fixture
    def stream_(self, request):
        return instance_mock(request, BytesIO)

    @pytest.fixture
    def StreamReader_(self, request, stream_rdr_):
        return class_mock(
            request, 'docx.image.tiff.StreamReader', return_value=stream_rdr_
        )

    @pytest.fixture
    def stream_rdr_(self, request, ifd0_offset_):
        stream_rdr_ = instance_mock(request, StreamReader)
        stream_rdr_.read_long.return_value = ifd0_offset_
        return stream_rdr_

    @pytest.fixture
    def _TiffParser__init_(self, request):
        return initializer_mock(request, _TiffParser)


class Describe_IfdEntries(object):

    def it_can_construct_from_a_stream_and_offset(self, from_stream_fixture):
        stream_, offset_, _IfdParser_, _IfdEntries__init_, entries_ = (
            from_stream_fixture
        )
        ifd_entries = _IfdEntries.from_stream(stream_, offset_)
        _IfdParser_.assert_called_once_with(stream_, offset_)
        _IfdEntries__init_.assert_called_once_with(entries_)
        assert isinstance(ifd_entries, _IfdEntries)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def from_stream_fixture(
            self, stream_, offset_, _IfdParser_, ifd_parser_,
            _IfdEntries__init_, ifd_entry_, ifd_entry_2_):
        ifd_parser_.iter_entries.return_value = [ifd_entry_, ifd_entry_2_]
        entries_ = {1: 42, 2: 24}
        return stream_, offset_, _IfdParser_, _IfdEntries__init_, entries_

    @pytest.fixture
    def ifd_entry_(self, request):
        return instance_mock(request, _IfdEntry, tag=1, value=42)

    @pytest.fixture
    def ifd_entry_2_(self, request):
        return instance_mock(request, _IfdEntry, tag=2, value=24)

    @pytest.fixture
    def _IfdEntries__init_(self, request):
        return initializer_mock(request, _IfdEntries)

    @pytest.fixture
    def _IfdParser_(self, request, ifd_parser_):
        return class_mock(
            request, 'docx.image.tiff._IfdParser', return_value=ifd_parser_
        )

    @pytest.fixture
    def ifd_parser_(self, request):
        return instance_mock(request, _IfdParser)

    @pytest.fixture
    def offset_(self, request):
        return instance_mock(request, int)

    @pytest.fixture
    def stream_(self, request):
        return instance_mock(request, BytesIO)
