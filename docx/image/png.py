# encoding: utf-8

from __future__ import absolute_import, division, print_function

from .constants import MIME_TYPE, PNG_CHUNK_TYPE
from .exceptions import InvalidImageStreamError
from .helpers import BIG_ENDIAN, StreamReader
from .image import BaseImageHeader


class Png(BaseImageHeader):
    """
    Image header parser for PNG images
    """

    @property
    def content_type(self):
        """
        MIME content type for this image, unconditionally `image/png` for
        PNG images.
        """
        return MIME_TYPE.PNG

    @property
    def default_ext(self):
        """
        Default filename extension, always 'png' for PNG images.
        """
        return "png"

    @classmethod
    def from_stream(cls, stream):
        """
        Return a |Png| instance having header properties parsed from image in
        *stream*.
        """
        parser = _PngParser.parse(stream)

        px_width = parser.px_width
        px_height = parser.px_height
        horz_dpi = parser.horz_dpi
        vert_dpi = parser.vert_dpi

        return cls(px_width, px_height, horz_dpi, vert_dpi)


class _PngParser(object):
    """
    Parses a PNG image stream to extract the image properties found in its
    chunks.
    """

    def __init__(self, chunks):
        super(_PngParser, self).__init__()
        self._chunks = chunks

    @classmethod
    def parse(cls, stream):
        """
        Return a |_PngParser| instance containing the header properties
        parsed from the PNG image in *stream*.
        """
        chunks = _Chunks.from_stream(stream)
        return cls(chunks)

    @property
    def px_width(self):
        """
        The number of pixels in each row of the image.
        """
        IHDR = self._chunks.IHDR
        return IHDR.px_width

    @property
    def px_height(self):
        """
        The number of stacked rows of pixels in the image.
        """
        IHDR = self._chunks.IHDR
        return IHDR.px_height

    @property
    def horz_dpi(self):
        """
        Integer dots per inch for the width of this image. Defaults to 72
        when not present in the file, as is often the case.
        """
        pHYs = self._chunks.pHYs
        if pHYs is None:
            return 72
        return self._dpi(pHYs.units_specifier, pHYs.horz_px_per_unit)

    @property
    def vert_dpi(self):
        """
        Integer dots per inch for the height of this image. Defaults to 72
        when not present in the file, as is often the case.
        """
        pHYs = self._chunks.pHYs
        if pHYs is None:
            return 72
        return self._dpi(pHYs.units_specifier, pHYs.vert_px_per_unit)

    @staticmethod
    def _dpi(units_specifier, px_per_unit):
        """
        Return dots per inch value calculated from *units_specifier* and
        *px_per_unit*.
        """
        if units_specifier == 1 and px_per_unit:
            return int(round(px_per_unit * 0.0254))
        return 72


class _Chunks(object):
    """
    Collection of the chunks parsed from a PNG image stream
    """

    def __init__(self, chunk_iterable):
        super(_Chunks, self).__init__()
        self._chunks = list(chunk_iterable)

    @classmethod
    def from_stream(cls, stream):
        """
        Return a |_Chunks| instance containing the PNG chunks in *stream*.
        """
        chunk_parser = _ChunkParser.from_stream(stream)
        chunks = [chunk for chunk in chunk_parser.iter_chunks()]
        return cls(chunks)

    @property
    def IHDR(self):
        """
        IHDR chunk in PNG image
        """
        match = lambda chunk: chunk.type_name == PNG_CHUNK_TYPE.IHDR  # noqa
        IHDR = self._find_first(match)
        if IHDR is None:
            raise InvalidImageStreamError("no IHDR chunk in PNG image")
        return IHDR

    @property
    def pHYs(self):
        """
        pHYs chunk in PNG image, or |None| if not present
        """
        match = lambda chunk: chunk.type_name == PNG_CHUNK_TYPE.pHYs  # noqa
        return self._find_first(match)

    def _find_first(self, match):
        """
        Return first chunk in stream order returning True for function
        *match*.
        """
        for chunk in self._chunks:
            if match(chunk):
                return chunk
        return None


class _ChunkParser(object):
    """
    Extracts chunks from a PNG image stream
    """

    def __init__(self, stream_rdr):
        super(_ChunkParser, self).__init__()
        self._stream_rdr = stream_rdr

    @classmethod
    def from_stream(cls, stream):
        """
        Return a |_ChunkParser| instance that can extract the chunks from the
        PNG image in *stream*.
        """
        stream_rdr = StreamReader(stream, BIG_ENDIAN)
        return cls(stream_rdr)

    def iter_chunks(self):
        """
        Generate a |_Chunk| subclass instance for each chunk in this parser's
        PNG stream, in the order encountered in the stream.
        """
        for chunk_type, offset in self._iter_chunk_offsets():
            chunk = _ChunkFactory(chunk_type, self._stream_rdr, offset)
            yield chunk

    def _iter_chunk_offsets(self):
        """
        Generate a (chunk_type, chunk_offset) 2-tuple for each of the chunks
        in the PNG image stream. Iteration stops after the IEND chunk is
        returned.
        """
        chunk_offset = 8
        while True:
            chunk_data_len = self._stream_rdr.read_long(chunk_offset)
            chunk_type = self._stream_rdr.read_str(4, chunk_offset, 4)
            data_offset = chunk_offset + 8
            yield chunk_type, data_offset
            if chunk_type == "IEND":
                break
            # incr offset for chunk len long, chunk type, chunk data, and CRC
            chunk_offset += 4 + 4 + chunk_data_len + 4


def _ChunkFactory(chunk_type, stream_rdr, offset):
    """
    Return a |_Chunk| subclass instance appropriate to *chunk_type* parsed
    from *stream_rdr* at *offset*.
    """
    chunk_cls_map = {
        PNG_CHUNK_TYPE.IHDR: _IHDRChunk,
        PNG_CHUNK_TYPE.pHYs: _pHYsChunk,
    }
    chunk_cls = chunk_cls_map.get(chunk_type, _Chunk)
    return chunk_cls.from_offset(chunk_type, stream_rdr, offset)


class _Chunk(object):
    """
    Base class for specific chunk types. Also serves as the default chunk
    type.
    """

    def __init__(self, chunk_type):
        super(_Chunk, self).__init__()
        self._chunk_type = chunk_type

    @classmethod
    def from_offset(cls, chunk_type, stream_rdr, offset):
        """
        Return a default _Chunk instance that only knows its chunk type.
        """
        return cls(chunk_type)

    @property
    def type_name(self):
        """
        The chunk type name, e.g. 'IHDR', 'pHYs', etc.
        """
        return self._chunk_type


class _IHDRChunk(_Chunk):
    """
    IHDR chunk, contains the image dimensions
    """

    def __init__(self, chunk_type, px_width, px_height):
        super(_IHDRChunk, self).__init__(chunk_type)
        self._px_width = px_width
        self._px_height = px_height

    @classmethod
    def from_offset(cls, chunk_type, stream_rdr, offset):
        """
        Return an _IHDRChunk instance containing the image dimensions
        extracted from the IHDR chunk in *stream* at *offset*.
        """
        px_width = stream_rdr.read_long(offset)
        px_height = stream_rdr.read_long(offset, 4)
        return cls(chunk_type, px_width, px_height)

    @property
    def px_width(self):
        return self._px_width

    @property
    def px_height(self):
        return self._px_height


class _pHYsChunk(_Chunk):
    """
    pYHs chunk, contains the image dpi information
    """

    def __init__(self, chunk_type, horz_px_per_unit, vert_px_per_unit, units_specifier):
        super(_pHYsChunk, self).__init__(chunk_type)
        self._horz_px_per_unit = horz_px_per_unit
        self._vert_px_per_unit = vert_px_per_unit
        self._units_specifier = units_specifier

    @classmethod
    def from_offset(cls, chunk_type, stream_rdr, offset):
        """
        Return a _pHYsChunk instance containing the image resolution
        extracted from the pHYs chunk in *stream* at *offset*.
        """
        horz_px_per_unit = stream_rdr.read_long(offset)
        vert_px_per_unit = stream_rdr.read_long(offset, 4)
        units_specifier = stream_rdr.read_byte(offset, 8)
        return cls(chunk_type, horz_px_per_unit, vert_px_per_unit, units_specifier)

    @property
    def horz_px_per_unit(self):
        return self._horz_px_per_unit

    @property
    def vert_px_per_unit(self):
        return self._vert_px_per_unit

    @property
    def units_specifier(self):
        return self._units_specifier
