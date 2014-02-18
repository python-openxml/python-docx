# encoding: utf-8

"""
Test suite for docx.image.png module
"""

from __future__ import absolute_import, print_function

import pytest

from mock import call

from docx.compat import BytesIO
from docx.image.constants import MIME_TYPE, PNG_CHUNK_TYPE, TAG
from docx.image.exceptions import InvalidImageStreamError
from docx.image.helpers import BIG_ENDIAN, StreamReader
from docx.image.png import (
    _Chunk, _Chunks, _ChunkFactory, _ChunkParser, _IHDRChunk, _pHYsChunk,
    Png, _PngParser
)

from ..unitutil import (
    function_mock, class_mock, initializer_mock, instance_mock, method_mock,
    test_file
)


class DescribePng(object):

    def it_can_construct_from_a_png_stream(self, from_stream_fixture):
        stream_, _PngParser_, Png__init__, cx, cy, horz_dpi, vert_dpi = (
            from_stream_fixture
        )
        png = Png.from_stream(stream_)
        _PngParser_.parse.assert_called_once_with(stream_)
        Png__init__.assert_called_once_with(cx, cy, horz_dpi, vert_dpi)
        assert isinstance(png, Png)

    def it_parses_PNG_headers_to_access_attrs(self, parse_png_fixture):
        (stream_, _parse_chunk_offsets_, _parse_chunks_, chunk_offsets,
         attrs_) = parse_png_fixture
        attrs = Png._parse_png_headers(stream_)
        _parse_chunk_offsets_.assert_called_once_with(stream_)
        _parse_chunks_.assert_called_once_with(stream_, chunk_offsets)
        assert attrs == attrs_

    def it_parses_chunk_offsets_to_help_chunk_parser(
            self, chunk_offset_fixture):
        stream, expected_chunk_offsets = chunk_offset_fixture
        chunk_offsets = Png._parse_chunk_offsets(stream)
        assert chunk_offsets == expected_chunk_offsets

    def it_parses_chunks_to_extract_fields(self, parse_chunks_fixture):
        (stream_, chunk_offsets, _parse_IHDR_, ihdr_offset, _parse_pHYs_,
         phys_offset, expected_attrs) = parse_chunks_fixture
        attrs = Png._parse_chunks(stream_, chunk_offsets)
        _parse_IHDR_.assert_called_once_with(stream_, ihdr_offset)
        if phys_offset is not None:
            _parse_pHYs_.assert_called_once_with(stream_, phys_offset)
        assert attrs == expected_attrs

    def it_raises_on_png_having_no_IHDR_chunk(self, no_IHDR_fixture):
        stream_, chunk_offsets = no_IHDR_fixture
        with pytest.raises(InvalidImageStreamError):
            Png._parse_chunks(stream_, chunk_offsets)

    def it_can_parse_an_IHDR_chunk(self, parse_IHDR_fixture):
        stream, offset, expected_attrs = parse_IHDR_fixture
        attrs = Png._parse_IHDR(stream, offset)
        assert attrs == expected_attrs

    def it_can_parse_an_pHYs_chunk(self, parse_pHYs_fixture):
        stream, offset, expected_attrs = parse_pHYs_fixture
        attrs = Png._parse_pHYs(stream, offset)
        assert attrs == expected_attrs

    def it_knows_its_content_type(self):
        png = Png(None, None, None, None)
        assert png.content_type == MIME_TYPE.PNG

    # def it_knows_its_dpi(self, dpi_fixture):
    #     png, expected_dpi = dpi_fixture
    #     assert png.horz_dpi == expected_dpi
    #     assert png.vert_dpi == expected_dpi

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def attrs(self):
        return dict()

    @pytest.fixture
    def attrs_(self, request):
        return instance_mock(request, dict)

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
    def chunk_offsets(self, request):
        return dict()

    @pytest.fixture(params=[
        (5906, 1, 150), (11811, 1, 300), (5906, 0, 72), (None, 0, 72),
        (666, 0, 72), (2835, 1, 72)
    ])
    def dpi_fixture(self, request):
        px_per_unit, units_specifier, expected_dpi = request.param
        attrs = {
            TAG.HORZ_PX_PER_UNIT: px_per_unit,
            TAG.VERT_PX_PER_UNIT: px_per_unit,
            TAG.UNITS_SPECIFIER:  units_specifier
        }
        png = Png(None, None, None, attrs)
        return png, expected_dpi

    @pytest.fixture
    def from_stream_fixture(
            self, stream_, _PngParser_, png_parser_, Png__init__):
        px_width, px_height, horz_dpi, vert_dpi = 42, 24, 36, 63
        png_parser_.px_width = px_width
        png_parser_.px_height = px_height
        png_parser_.horz_dpi = horz_dpi
        png_parser_.vert_dpi = vert_dpi
        return (
            stream_, _PngParser_, Png__init__, px_width, px_height,
            horz_dpi, vert_dpi
        )

    @pytest.fixture
    def no_IHDR_fixture(self, stream_, chunk_offsets):
        return stream_, chunk_offsets

    @pytest.fixture(params=[(42, 24), (42, None)])
    def parse_chunks_fixture(
            self, request, stream_rdr_, _parse_IHDR_, _parse_pHYs_):
        ihdr_offset, phys_offset = request.param
        chunk_offsets = {'IHDR': ihdr_offset}
        expected_attrs = dict(_parse_IHDR_.return_value)
        if phys_offset is not None:
            chunk_offsets['pHYs'] = phys_offset
            expected_attrs.update(_parse_pHYs_.return_value)
        return (
            stream_rdr_, chunk_offsets, _parse_IHDR_, ihdr_offset,
            _parse_pHYs_, phys_offset, expected_attrs
        )

    @pytest.fixture
    def parse_IHDR_fixture(self):
        bytes_ = b'\x00\x00\x00\x2A\x00\x00\x00\x18'
        stream = BytesIO(bytes_)
        stream_rdr = StreamReader(stream, BIG_ENDIAN)
        offset = 0
        expected_attrs = {TAG.PX_WIDTH: 42, TAG.PX_HEIGHT: 24}
        return stream_rdr, offset, expected_attrs

    @pytest.fixture
    def parse_pHYs_fixture(self):
        bytes_ = b'\x00\x00\x17\x12\x00\x00\x1E\xC2\x01'
        stream = BytesIO(bytes_)
        stream_rdr = StreamReader(stream, BIG_ENDIAN)
        offset = 0
        expected_attrs = {
            TAG.HORZ_PX_PER_UNIT: 5906, TAG.VERT_PX_PER_UNIT: 7874,
            TAG.UNITS_SPECIFIER: 1
        }
        return stream_rdr, offset, expected_attrs

    @pytest.fixture
    def parse_png_fixture(
            self, stream_rdr_, _parse_chunk_offsets_, _parse_chunks_,
            chunk_offsets, attrs_):
        chunk_offsets['IHDR'] = 666
        return (
            stream_rdr_, _parse_chunk_offsets_, _parse_chunks_,
            chunk_offsets, attrs_
        )

    @pytest.fixture
    def _parse_chunk_offsets_(self, request, chunk_offsets):
        return method_mock(
            request, Png, '_parse_chunk_offsets', return_value=chunk_offsets
        )

    @pytest.fixture
    def _parse_chunks_(self, request, attrs_):
        return method_mock(
            request, Png, '_parse_chunks', return_value=attrs_
        )

    @pytest.fixture
    def _parse_IHDR_(self, request):
        return method_mock(
            request, Png, '_parse_IHDR', return_value={
                TAG.PX_WIDTH: 12, TAG.PX_HEIGHT: 34
            }
        )

    @pytest.fixture
    def _parse_pHYs_(self, request):
        return method_mock(
            request, Png, '_parse_pHYs', return_value={
                TAG.HORZ_PX_PER_UNIT: 56, TAG.VERT_PX_PER_UNIT: 78,
                TAG.UNITS_SPECIFIER: 1
            }
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
    def _PngParser_(self, request, png_parser_):
        _PngParser_ = class_mock(request, 'docx.image.png._PngParser')
        _PngParser_.parse.return_value = png_parser_
        return _PngParser_

    @pytest.fixture
    def png_parser_(self, request):
        return instance_mock(request, _PngParser)

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


class Describe_PngParser(object):

    def it_can_parse_the_headers_of_a_PNG_stream(self, parse_fixture):
        stream_, _Chunks_, _PngParser__init_, chunks_ = parse_fixture
        png_parser = _PngParser.parse(stream_)
        _Chunks_.from_stream.assert_called_once_with(stream_)
        _PngParser__init_.assert_called_once_with(chunks_)
        assert isinstance(png_parser, _PngParser)

    def it_knows_the_image_width_and_height(self, dimensions_fixture):
        png_parser, px_width, px_height = dimensions_fixture
        assert png_parser.px_width == px_width
        assert png_parser.px_height == px_height

    def it_knows_the_image_dpi(self, dpi_fixture):
        png_parser, horz_dpi, vert_dpi = dpi_fixture
        assert png_parser.horz_dpi == horz_dpi
        assert png_parser.vert_dpi == vert_dpi

    def it_defaults_image_dpi_to_72(self, no_dpi_fixture):
        png_parser = no_dpi_fixture
        assert png_parser.horz_dpi == 72
        assert png_parser.vert_dpi == 72

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def _Chunks_(self, request, chunks_):
        _Chunks_ = class_mock(request, 'docx.image.png._Chunks')
        _Chunks_.from_stream.return_value = chunks_
        return _Chunks_

    @pytest.fixture
    def chunks_(self, request):
        return instance_mock(request, _Chunks)

    @pytest.fixture
    def dimensions_fixture(self, chunks_):
        px_width, px_height = 12, 34
        chunks_.IHDR.px_width = px_width
        chunks_.IHDR.px_height = px_height
        png_parser = _PngParser(chunks_)
        return png_parser, px_width, px_height

    @pytest.fixture
    def dpi_fixture(self, chunks_):
        horz_px_per_unit, vert_px_per_unit, units_specifier = 1654, 945, 1
        horz_dpi, vert_dpi = 42, 24
        chunks_.pHYs.horz_px_per_unit = horz_px_per_unit
        chunks_.pHYs.vert_px_per_unit = vert_px_per_unit
        chunks_.pHYs.units_specifier = units_specifier
        png_parser = _PngParser(chunks_)
        return png_parser, horz_dpi, vert_dpi

    @pytest.fixture(params=[
        (-1, -1), (0, 1000), (None, 1000), (1, 0), (1, None)
    ])
    def no_dpi_fixture(self, request, chunks_):
        """
        Scenarios are: 1) no pHYs chunk in PNG stream, 2) units specifier
        other than 1; 3) px_per_unit is 0; 4) px_per_unit is None
        """
        units_specifier, px_per_unit = request.param
        if units_specifier == -1:
            chunks_.pHYs = None
        else:
            chunks_.pHYs.horz_px_per_unit = px_per_unit
            chunks_.pHYs.vert_px_per_unit = px_per_unit
            chunks_.pHYs.units_specifier = units_specifier
        png_parser = _PngParser(chunks_)
        return png_parser

    @pytest.fixture
    def parse_fixture(self, stream_, _Chunks_, _PngParser__init_, chunks_):
        return stream_, _Chunks_, _PngParser__init_, chunks_

    @pytest.fixture
    def _PngParser__init_(self, request):
        return initializer_mock(request, _PngParser)

    @pytest.fixture
    def stream_(self, request):
        return instance_mock(request, BytesIO)


class Describe_Chunks(object):

    def it_can_construct_from_a_stream(self, from_stream_fixture):
        stream_, _ChunkParser_, chunk_parser_, _Chunks__init_, chunk_lst = (
            from_stream_fixture
        )
        chunks = _Chunks.from_stream(stream_)
        _ChunkParser_.from_stream.assert_called_once_with(stream_)
        chunk_parser_.iter_chunks.assert_called_once_with()
        _Chunks__init_.assert_called_once_with(chunk_lst)
        assert isinstance(chunks, _Chunks)

    def it_provides_access_to_the_IHDR_chunk(self, IHDR_fixture):
        chunks, IHDR_chunk_ = IHDR_fixture
        assert chunks.IHDR == IHDR_chunk_

    def it_provides_access_to_the_pHYs_chunk(self, pHYs_fixture):
        chunks, expected_chunk = pHYs_fixture
        assert chunks.pHYs == expected_chunk

    def it_raises_if_theres_no_IHDR_chunk(self, no_IHDR_fixture):
        chunks = no_IHDR_fixture
        with pytest.raises(InvalidImageStreamError):
            chunks.IHDR

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def from_stream_fixture(
            self, stream_, _ChunkParser_, chunk_parser_, _Chunks__init_):
        chunk_lst = [1, 2]
        chunk_parser_.iter_chunks.return_value = iter(chunk_lst)
        return (
            stream_, _ChunkParser_, chunk_parser_, _Chunks__init_, chunk_lst
        )

    @pytest.fixture
    def _ChunkParser_(self, request, chunk_parser_):
        _ChunkParser_ = class_mock(request, 'docx.image.png._ChunkParser')
        _ChunkParser_.from_stream.return_value = chunk_parser_
        return _ChunkParser_

    @pytest.fixture
    def chunk_parser_(self, request):
        return instance_mock(request, _ChunkParser)

    @pytest.fixture
    def _Chunks__init_(self, request):
        return initializer_mock(request, _Chunks)

    @pytest.fixture
    def IHDR_fixture(self, IHDR_chunk_, pHYs_chunk_):
        chunks = (IHDR_chunk_, pHYs_chunk_)
        chunks = _Chunks(chunks)
        return chunks, IHDR_chunk_

    @pytest.fixture
    def IHDR_chunk_(self, request):
        return instance_mock(
            request, _IHDRChunk, type_name=PNG_CHUNK_TYPE.IHDR
        )

    @pytest.fixture
    def no_IHDR_fixture(self, pHYs_chunk_):
        chunks = (pHYs_chunk_,)
        chunks = _Chunks(chunks)
        return chunks

    @pytest.fixture
    def pHYs_chunk_(self, request):
        return instance_mock(
            request, _pHYsChunk, type_name=PNG_CHUNK_TYPE.pHYs
        )

    @pytest.fixture(params=[True, False])
    def pHYs_fixture(self, request, IHDR_chunk_, pHYs_chunk_):
        has_pHYs_chunk = request.param
        chunks = [IHDR_chunk_]
        if has_pHYs_chunk:
            chunks.append(pHYs_chunk_)
        expected_chunk = pHYs_chunk_ if has_pHYs_chunk else None
        chunks = _Chunks(chunks)
        return chunks, expected_chunk

    @pytest.fixture
    def stream_(self, request):
        return instance_mock(request, BytesIO)


class Describe_ChunkParser(object):

    def it_can_construct_from_a_stream(self, from_stream_fixture):
        stream_, StreamReader_, stream_rdr_, _ChunkParser__init_ = (
            from_stream_fixture
        )
        chunk_parser = _ChunkParser.from_stream(stream_)
        StreamReader_.assert_called_once_with(stream_, BIG_ENDIAN)
        _ChunkParser__init_.assert_called_once_with(stream_rdr_)
        assert isinstance(chunk_parser, _ChunkParser)

    def it_can_iterate_over_the_chunks_in_its_png_stream(self, iter_fixture):
        # fixture ----------------------
        chunk_parser, _iter_chunk_offsets_, _ChunkFactory_ = iter_fixture[:3]
        stream_rdr_, offsets, chunk_lst = iter_fixture[3:]
        # exercise ---------------------
        chunks = [chunk for chunk in chunk_parser.iter_chunks()]
        # verify -----------------------
        _iter_chunk_offsets_.assert_called_once_with()
        assert _ChunkFactory_.call_args_list == [
            call(PNG_CHUNK_TYPE.IHDR, stream_rdr_, offsets[0]),
            call(PNG_CHUNK_TYPE.pHYs, stream_rdr_, offsets[1]),
        ]
        assert chunks == chunk_lst

    def it_iterates_over_the_chunk_offsets_to_help_parse(
            self, iter_offsets_fixture):
        chunk_parser, expected_chunk_offsets = iter_offsets_fixture
        chunk_offsets = [co for co in chunk_parser._iter_chunk_offsets()]
        assert chunk_offsets == expected_chunk_offsets

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def chunk_(self, request):
        return instance_mock(request, _Chunk)

    @pytest.fixture
    def chunk_2_(self, request):
        return instance_mock(request, _Chunk)

    @pytest.fixture
    def _ChunkFactory_(self, request, chunk_lst_):
        return function_mock(
            request, 'docx.image.png._ChunkFactory',
            side_effect=chunk_lst_
        )

    @pytest.fixture
    def chunk_lst_(self, chunk_, chunk_2_):
        return [chunk_, chunk_2_]

    @pytest.fixture
    def _ChunkParser__init_(self, request):
        return initializer_mock(request, _ChunkParser)

    @pytest.fixture
    def from_stream_fixture(
            self, stream_, StreamReader_, stream_rdr_, _ChunkParser__init_):
        return stream_, StreamReader_, stream_rdr_, _ChunkParser__init_

    @pytest.fixture
    def _iter_chunk_offsets_(self, request):
        chunk_offsets = (
            (PNG_CHUNK_TYPE.IHDR, 2),
            (PNG_CHUNK_TYPE.pHYs, 4),
        )
        return method_mock(
            request, _ChunkParser, '_iter_chunk_offsets',
            return_value=iter(chunk_offsets)
        )

    @pytest.fixture
    def iter_fixture(
            self, _iter_chunk_offsets_, _ChunkFactory_, stream_rdr_, chunk_,
            chunk_2_):
        chunk_parser = _ChunkParser(stream_rdr_)
        offsets = [2, 4, 6]
        chunk_lst = [chunk_, chunk_2_]
        return (
            chunk_parser, _iter_chunk_offsets_, _ChunkFactory_, stream_rdr_,
            offsets, chunk_lst
        )

    @pytest.fixture
    def iter_offsets_fixture(self):
        bytes_ = b'-filler-\x00\x00\x00\x00IHDRxxxx\x00\x00\x00\x00IEND'
        stream_rdr = StreamReader(BytesIO(bytes_), BIG_ENDIAN)
        chunk_parser = _ChunkParser(stream_rdr)
        expected_chunk_offsets = [
            (PNG_CHUNK_TYPE.IHDR, 16),
            (PNG_CHUNK_TYPE.IEND, 28),
        ]
        return chunk_parser, expected_chunk_offsets

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


class Describe_ChunkFactory(object):

    def it_constructs_the_appropriate_Chunk_subclass(self, call_fixture):
        chunk_type, stream_rdr_, offset, chunk_cls_ = call_fixture
        chunk = _ChunkFactory(chunk_type, stream_rdr_, offset)
        chunk_cls_.from_offset.assert_called_once_with(
            chunk_type, stream_rdr_, offset
        )
        assert isinstance(chunk, _Chunk)

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        PNG_CHUNK_TYPE.IHDR,
        PNG_CHUNK_TYPE.pHYs,
        PNG_CHUNK_TYPE.IEND,
    ])
    def call_fixture(
            self, request, _IHDRChunk_, _pHYsChunk_, _Chunk_, stream_rdr_):
        chunk_type = request.param
        chunk_cls_ = {
            PNG_CHUNK_TYPE.IHDR: _IHDRChunk_,
            PNG_CHUNK_TYPE.pHYs: _pHYsChunk_,
            PNG_CHUNK_TYPE.IEND: _Chunk_,
        }[chunk_type]
        offset = 999
        return chunk_type, stream_rdr_, offset, chunk_cls_

    @pytest.fixture
    def _Chunk_(self, request, chunk_):
        _Chunk_ = class_mock(request, 'docx.image.png._Chunk')
        _Chunk_.from_offset.return_value = chunk_
        return _Chunk_

    @pytest.fixture
    def chunk_(self, request):
        return instance_mock(request, _Chunk)

    @pytest.fixture
    def _IHDRChunk_(self, request, ihdr_chunk_):
        _IHDRChunk_ = class_mock(request, 'docx.image.png._IHDRChunk')
        _IHDRChunk_.from_offset.return_value = ihdr_chunk_
        return _IHDRChunk_

    @pytest.fixture
    def ihdr_chunk_(self, request):
        return instance_mock(request, _IHDRChunk)

    @pytest.fixture
    def _pHYsChunk_(self, request, phys_chunk_):
        _pHYsChunk_ = class_mock(request, 'docx.image.png._pHYsChunk')
        _pHYsChunk_.from_offset.return_value = phys_chunk_
        return _pHYsChunk_

    @pytest.fixture
    def phys_chunk_(self, request):
        return instance_mock(request, _pHYsChunk)

    @pytest.fixture
    def stream_rdr_(self, request):
        return instance_mock(request, StreamReader)


class Describe_Chunk(object):

    def it_can_construct_from_a_stream_and_offset(self):
        chunk_type = 'fOOB'
        chunk = _Chunk.from_offset(chunk_type, None, None)
        assert isinstance(chunk, _Chunk)
        assert chunk.type_name == chunk_type


class Describe_IHDRChunk(object):

    def it_can_construct_from_a_stream_and_offset(self, from_offset_fixture):
        stream_rdr, offset, px_width, px_height = from_offset_fixture
        ihdr_chunk = _IHDRChunk.from_offset(None, stream_rdr, offset)
        assert isinstance(ihdr_chunk, _IHDRChunk)
        assert ihdr_chunk.px_width == px_width
        assert ihdr_chunk.px_height == px_height

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def from_offset_fixture(self):
        bytes_ = b'\x00\x00\x00\x2A\x00\x00\x00\x18'
        stream_rdr = StreamReader(BytesIO(bytes_), BIG_ENDIAN)
        offset, px_width, px_height = 0, 42, 24
        return stream_rdr, offset, px_width, px_height


class Describe_pHYsChunk(object):

    def it_can_construct_from_a_stream_and_offset(self, from_offset_fixture):
        stream_rdr, offset = from_offset_fixture[:2]
        horz_px_per_unit, vert_px_per_unit = from_offset_fixture[2:4]
        units_specifier = from_offset_fixture[4]
        pHYs_chunk = _pHYsChunk.from_offset(None, stream_rdr, offset)
        assert isinstance(pHYs_chunk, _pHYsChunk)
        assert pHYs_chunk.horz_px_per_unit == horz_px_per_unit
        assert pHYs_chunk.vert_px_per_unit == vert_px_per_unit
        assert pHYs_chunk.units_specifier == units_specifier

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def from_offset_fixture(self):
        bytes_ = b'\x00\x00\x00\x2A\x00\x00\x00\x18\x01'
        stream_rdr = StreamReader(BytesIO(bytes_), BIG_ENDIAN)
        offset, horz_px_per_unit, vert_px_per_unit, units_specifier = (
            0, 42, 24, 1
        )
        return (
            stream_rdr, offset, horz_px_per_unit, vert_px_per_unit,
            units_specifier
        )
