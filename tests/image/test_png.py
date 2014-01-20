# encoding: utf-8

"""
Test suite for docx.image.png module
"""

from __future__ import absolute_import, print_function

import pytest

from docx.compat import BytesIO
from docx.image.exceptions import InvalidImageStreamError
from docx.image.helpers import BIG_ENDIAN, StreamReader
from docx.image.png import Png

from ..unitutil import (
    initializer_mock, class_mock, instance_mock, method_mock, test_file
)


class DescribePng(object):

    def it_can_construct_from_a_png_stream(self, from_stream_fixture):
        # fixture ----------------------
        (stream_, blob_, filename_, StreamReader_, _parse_png_headers_,
         stream_rdr_, Png__init__, cx, cy, attrs, png_) = from_stream_fixture
        # exercise ---------------------
        png = Png.from_stream(stream_, blob_, filename_)
        # verify -----------------------
        StreamReader_.assert_called_once_with(stream_, '>')
        _parse_png_headers_.assert_called_once_with(stream_rdr_)
        Png__init__.assert_called_once_with(blob_, filename_, cx, cy, attrs)
        assert isinstance(png, Png)

    def it_parses_PNG_headers_to_access_attrs(self, parse_png_fixture):
        (stream_, _parse_chunk_offsets_, _parse_chunks_, chunk_offsets_,
         attrs_) = parse_png_fixture
        attrs = Png._parse_png_headers(stream_)
        _parse_chunk_offsets_.assert_called_once_with(stream_)
        _parse_chunks_.assert_called_once_with(stream_, chunk_offsets_)
        assert attrs == attrs_

    def it_raises_on_png_having_no_IHDR_chunk(self, no_IHDR_fixture):
        stream_ = no_IHDR_fixture
        with pytest.raises(InvalidImageStreamError):
            Png._parse_png_headers(stream_)

    def it_parses_chunk_offsets_to_help_chunk_parser(
            self, chunk_offset_fixture):
        stream, expected_chunk_offsets = chunk_offset_fixture
        chunk_offsets = Png._parse_chunk_offsets(stream)
        assert chunk_offsets == expected_chunk_offsets

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def attrs(self):
        return dict()

    @pytest.fixture
    def attrs_(self, request):
        return instance_mock(request, dict)

    @pytest.fixture
    def blob_(self, request):
        return instance_mock(request, bytes)

    @pytest.fixture(params=[
        ('150-dpi.png', {
            'IHDR': 16, 'pHYs': 41, 'iCCP': 62, 'cHRM': 2713, 'IDAT': 2757,
            'IEND': 146888}),
        ('300-dpi.png', {
            'IHDR': 16, 'pHYs': 41, 'tEXt': 62, 'IDAT': 99, 'IEND': 39917}),
    ])
    def chunk_offset_fixture(self, request):
        filename, expected_chunk_offsets = request.param
        path = test_file(filename)
        with open(path, 'rb') as f:
            blob = f.read()
        stream = BytesIO(blob)
        stream_rdr = StreamReader(stream, BIG_ENDIAN)
        return stream_rdr, expected_chunk_offsets

    @pytest.fixture
    def chunk_offsets_(self, request):
        return dict()

    @pytest.fixture
    def filename_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def from_stream_fixture(
            self, stream_, blob_, filename_, StreamReader_,
            _parse_png_headers_, stream_rdr_, Png__init__, attrs, png_):
        cx, cy = 42, 24
        attrs.update({'px_width': cx, 'px_height': cy})
        return (
            stream_, blob_, filename_, StreamReader_, _parse_png_headers_,
            stream_rdr_, Png__init__, cx, cy, attrs, png_
        )

    @pytest.fixture
    def no_IHDR_fixture(
            self, stream_, _parse_chunk_offsets_, _parse_chunks_):
        return stream_

    @pytest.fixture
    def parse_png_fixture(
            self, stream_rdr_, _parse_chunk_offsets_, _parse_chunks_,
            chunk_offsets_, attrs_):
        chunk_offsets_['IHDR'] = 666
        return (
            stream_rdr_, _parse_chunk_offsets_, _parse_chunks_,
            chunk_offsets_, attrs_
        )

    @pytest.fixture
    def _parse_chunk_offsets_(self, request, chunk_offsets_):
        return method_mock(
            request, Png, '_parse_chunk_offsets', return_value=chunk_offsets_
        )

    @pytest.fixture
    def _parse_chunks_(self, request, attrs_):
        return method_mock(
            request, Png, '_parse_chunks', return_value=attrs_
        )

    @pytest.fixture
    def _parse_png_headers_(self, request, attrs):
        return method_mock(
            request, Png, '_parse_png_headers', return_value=attrs
        )

    @pytest.fixture
    def Png__init__(self, request):
        return initializer_mock(request, Png)

    @pytest.fixture
    def png_(self, request):
        return instance_mock(request, Png)

    @pytest.fixture
    def StreamReader_(self, request, stream_rdr_):
        return class_mock(
            request, 'docx.image.png.StreamReader', return_value=stream_rdr_
        )

    @pytest.fixture
    def stream_(self, request):
        return instance_mock(request, BytesIO)

    @pytest.fixture
    def stream_rdr_(self, request):
        return instance_mock(request, StreamReader)
