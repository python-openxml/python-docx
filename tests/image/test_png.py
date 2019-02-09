# encoding: utf-8

"""Unit test suite for docx.image.png module"""

from __future__ import absolute_import, print_function

import pytest

from docx.compat import BytesIO
from docx.image.constants import MIME_TYPE, PNG_CHUNK_TYPE
from docx.image.exceptions import InvalidImageStreamError
from docx.image.helpers import BIG_ENDIAN, StreamReader
from docx.image.png import (
    _Chunk, _Chunks, _ChunkFactory, _ChunkParser, _IHDRChunk, _pHYsChunk,
    Png, _PngParser
)

from ..unitutil.mock import (
    ANY,
    call,
    class_mock,
    function_mock,
    initializer_mock,
    instance_mock,
    method_mock,
)


class DescribePng(object):

    def it_can_construct_from_a_png_stream(
            self, stream_, _PngParser_, png_parser_, Png__init__
    ):
        px_width, px_height, horz_dpi, vert_dpi = 42, 24, 36, 63
        png_parser_.px_width = px_width
        png_parser_.px_height = px_height
        png_parser_.horz_dpi = horz_dpi
        png_parser_.vert_dpi = vert_dpi

        png = Png.from_stream(stream_)

        _PngParser_.parse.assert_called_once_with(stream_)
        Png__init__.assert_called_once_with(
            ANY, px_width, px_height, horz_dpi, vert_dpi
        )
        assert isinstance(png, Png)

    def it_knows_its_content_type(self):
        png = Png(None, None, None, None)
        assert png.content_type == MIME_TYPE.PNG

    def it_knows_its_default_ext(self):
        png = Png(None, None, None, None)
        assert png.default_ext == 'png'

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def Png__init__(self, request):
        return initializer_mock(request, Png)

    @pytest.fixture
    def _PngParser_(self, request, png_parser_):
        _PngParser_ = class_mock(request, 'docx.image.png._PngParser')
        _PngParser_.parse.return_value = png_parser_
        return _PngParser_

    @pytest.fixture
    def png_parser_(self, request):
        return instance_mock(request, _PngParser)

    @pytest.fixture
    def stream_(self, request):
        return instance_mock(request, BytesIO)


class Describe_PngParser(object):

    def it_can_parse_the_headers_of_a_PNG_stream(
        self, stream_, _Chunks_, _PngParser__init_, chunks_
    ):
        png_parser = _PngParser.parse(stream_)

        _Chunks_.from_stream.assert_called_once_with(stream_)
        _PngParser__init_.assert_called_once_with(ANY, chunks_)
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
    def _PngParser__init_(self, request):
        return initializer_mock(request, _PngParser)

    @pytest.fixture
    def stream_(self, request):
        return instance_mock(request, BytesIO)


class Describe_Chunks(object):

    def it_can_construct_from_a_stream(
        self, stream_, _ChunkParser_, chunk_parser_, _Chunks__init_
    ):
        chunk_lst = [1, 2]
        chunk_parser_.iter_chunks.return_value = iter(chunk_lst)

        chunks = _Chunks.from_stream(stream_)

        _ChunkParser_.from_stream.assert_called_once_with(stream_)
        chunk_parser_.iter_chunks.assert_called_once_with()
        _Chunks__init_.assert_called_once_with(ANY, chunk_lst)
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

    def it_can_construct_from_a_stream(
        self, stream_, StreamReader_, stream_rdr_, _ChunkParser__init_
    ):
        chunk_parser = _ChunkParser.from_stream(stream_)

        StreamReader_.assert_called_once_with(stream_, BIG_ENDIAN)
        _ChunkParser__init_.assert_called_once_with(ANY, stream_rdr_)
        assert isinstance(chunk_parser, _ChunkParser)

    def it_can_iterate_over_the_chunks_in_its_png_stream(
        self, _iter_chunk_offsets_, _ChunkFactory_, stream_rdr_, chunk_, chunk_2_
    ):
        offsets = [2, 4, 6]
        chunk_lst = [chunk_, chunk_2_]
        chunk_parser = _ChunkParser(stream_rdr_)

        chunks = [chunk for chunk in chunk_parser.iter_chunks()]

        _iter_chunk_offsets_.assert_called_once_with(chunk_parser)
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
