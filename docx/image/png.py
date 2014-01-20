# encoding: utf-8

from __future__ import absolute_import, division, print_function

from .constants import MIME_TYPE, TAG
from .exceptions import InvalidImageStreamError
from .helpers import StreamReader
from .image import Image


_CHUNK_TYPE_IHDR = 'IHDR'
_CHUNK_TYPE_pHYs = 'pHYs'
_CHUNK_TYPE_IEND = 'IEND'


class Png(Image):
    """
    Image header parser for PNG images
    """
    def __init__(self, blob, filename, cx, cy, attrs):
        super(Png, self).__init__(blob, filename, cx, cy, attrs)

    @property
    def content_type(self):
        """
        MIME content type for this image, unconditionally `image/png` for
        PNG images.
        """
        return MIME_TYPE.PNG

    @classmethod
    def from_stream(cls, stream, blob, filename):
        """
        Return a |Png| instance having header properties parsed from image in
        *stream*.
        """
        stream_rdr = StreamReader(stream, '>')
        attrs = cls._parse_png_headers(stream_rdr)
        cx, cy = attrs.pop('px_width'), attrs.pop('px_height')
        return Png(blob, filename, cx, cy, attrs)

    @property
    def horz_dpi(self):
        """
        Integer dots per inch for the width of this image. Defaults to 72
        when not present in the file, as is often the case.
        """
        units_specifier = self._attrs.get(TAG.UNITS_SPECIFIER)
        horz_px_per_unit = self._attrs.get(TAG.HORZ_PX_PER_UNIT)

        if units_specifier == 1 and horz_px_per_unit is not None:
            horz_dpi = int(round(horz_px_per_unit * 0.0254))
        else:
            horz_dpi = 72

        return horz_dpi

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
