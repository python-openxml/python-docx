# encoding: utf-8

from __future__ import absolute_import, division, print_function

from .constants import MIME_TYPE, TAG
from .exceptions import InvalidImageStreamError
from .helpers import BIG_ENDIAN, StreamReader
from .image import BaseImageHeader


_CHUNK_TYPE_IHDR = 'IHDR'
_CHUNK_TYPE_pHYs = 'pHYs'
_CHUNK_TYPE_IEND = 'IEND'


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

    @property
    def horz_dpi(self):
        """
        Integer dots per inch for the width of this image. Defaults to 72
        when not present in the file, as is often the case.
        """
        units_specifier = self._attrs.get(TAG.UNITS_SPECIFIER)
        horz_px_per_unit = self._attrs.get(TAG.HORZ_PX_PER_UNIT)
        return self._dpi(units_specifier, horz_px_per_unit)

    @property
    def vert_dpi(self):
        """
        Integer dots per inch for the height of this image. Defaults to 72
        when not present in the file, as is often the case.
        """
        units_specifier = self._attrs.get(TAG.UNITS_SPECIFIER)
        vert_px_per_unit = self._attrs.get(TAG.VERT_PX_PER_UNIT)
        return self._dpi(units_specifier, vert_px_per_unit)

    @staticmethod
    def _dpi(units_specifier, px_per_unit):
        """
        Return dots per inch value calculated from *units_specifier* and
        *px_per_unit*.
        """
        if units_specifier == 1 and px_per_unit is not None:
            return int(round(px_per_unit * 0.0254))
        return 72

    @classmethod
    def _parse_png_headers(cls, stream):
        """
        Return a dict of field, value pairs parsed from the PNG chunks in
        *stream*.
        """
        chunk_offsets = cls._parse_chunk_offsets(stream)
        attrs = cls._parse_chunks(stream, chunk_offsets)
        return attrs

    @classmethod
    def _parse_chunk_offsets(cls, stream):
        """
        Return a dict of chunk_type, offset(s) parsed from the chunks in
        *stream*. The offsets for a chunk type that may appear more than once
        are returned as a list regardless of their actual number in *stream*.
        """
        chunk_offsets = {}
        for chunk_type, offset in cls._iter_chunk_offsets(stream):
            # this would need to be more sophisticated if we needed any of
            # the chunks that can appear multiple times
            chunk_offsets[chunk_type] = offset
        return chunk_offsets

    @staticmethod
    def _iter_chunk_offsets(stream):
        """
        Generate a (chunk_type, chunk_offset) 2-tuple for each of the chunks
        in the PNG image stream. Iteration stops after the IEND chunk is
        returned.
        """
        chunk_offset = 8
        while True:
            chunk_data_len = stream.read_long(chunk_offset)
            chunk_type = stream.read_str(4, chunk_offset, 4)
            data_offset = chunk_offset + 8
            yield chunk_type, data_offset
            if chunk_type == _CHUNK_TYPE_IEND:
                break
            # incr offset for chunk len long, chunk type, chunk data, and CRC
            chunk_offset += (4 + 4 + chunk_data_len + 4)

    @classmethod
    def _parse_chunks(cls, stream, chunk_offsets):
        """
        Return a dict of field, value pairs parsed from selected chunks in
        the PNG image in *stream*, using *chunk_offsets* to locate the
        desired chunks.
        """
        attrs = {}

        # IHDR chunk -------------------
        if _CHUNK_TYPE_IHDR not in chunk_offsets:
            # IHDR chunk is mandatory, invalid if not present
            raise InvalidImageStreamError('no IHDR chunk in PNG image')
        ihdr_offset = chunk_offsets[_CHUNK_TYPE_IHDR]
        ihdr_attrs = cls._parse_IHDR(stream, ihdr_offset)
        attrs.update(ihdr_attrs)

        # pHYs chunk -------------------
        if _CHUNK_TYPE_pHYs in chunk_offsets:
            phys_offset = chunk_offsets[_CHUNK_TYPE_pHYs]
            phys_attrs = cls._parse_pHYs(stream, phys_offset)
            attrs.update(phys_attrs)

        return attrs

    @classmethod
    def _parse_IHDR(cls, stream, offset):
        """
        Return a dict containing values for TAG.PX_WIDTH and TAG.PX_HEIGHT
        extracted from the IHDR chunk in *stream* at *offset*.
        """
        return {
            TAG.PX_WIDTH:  stream.read_long(offset),
            TAG.PX_HEIGHT: stream.read_long(offset, 4)
        }

    @classmethod
    def _parse_pHYs(cls, stream, offset):
        """
        Return a dict containing values for TAG.HORZ_PX_PER_UNIT,
        TAG.VERT_PX_PER_UNIT, and TAG.UNITS_SPECIFIER parsed from the pHYs
        chunk at *offset* in *stream*.
        """
        return {
            TAG.HORZ_PX_PER_UNIT: stream.read_long(offset),
            TAG.VERT_PX_PER_UNIT: stream.read_long(offset, 4),
            TAG.UNITS_SPECIFIER:  stream.read_byte(offset, 8)
        }


class _PngParser(object):
    """
    Parses a PNG image stream to extract the image properties found in its
    chunks.
    """
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
        raise NotImplementedError

    @property
    def px_height(self):
        """
        The number of stacked rows of pixels in the image.
        """
        raise NotImplementedError

    @property
    def horz_dpi(self):
        """
        Integer dots per inch for the width of this image. Defaults to 72
        when not present in the file, as is often the case.
        """
        raise NotImplementedError

    @property
    def vert_dpi(self):
        """
        Integer dots per inch for the height of this image. Defaults to 72
        when not present in the file, as is often the case.
        """
        raise NotImplementedError


class _Chunks(object):
    """
    Collection of the chunks parsed from a PNG image stream
    """
    @classmethod
    def from_stream(cls, stream):
        """
        Return a |_Chunks| instance containing the PNG chunks in *stream*.
        """
        chunk_parser = _ChunkParser.from_stream(stream)
        chunk_lst = [chunk for chunk in chunk_parser.iter_chunks()]
        return cls(chunk_lst)


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
            if chunk_type == 'IEND':
                break
            # incr offset for chunk len long, chunk type, chunk data, and CRC
            chunk_offset += (4 + 4 + chunk_data_len + 4)


def _ChunkFactory(chunk_type, stream_rdr, offset):
    """
    Return a |_Chunk| subclass instance appropriate to *chunk_type* parsed
    from *stream_rdr* at *offset*.
    """
    raise NotImplementedError


class _Chunk(object):
    """
    Base class for specific chunk types. Also serves as the default chunk
    type.
    """
