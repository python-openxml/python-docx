# encoding: utf-8

from __future__ import absolute_import, division, print_function

from .exceptions import InvalidImageStreamError
from .helpers import StreamReader
from .image import Image


class Png(Image):
    """
    Image header parser for PNG images
    """
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

    @classmethod
    def _parse_png_headers(cls, stream):
        """
        Return a dict of field, value pairs parsed from the PNG chunks in
        *stream*.
        """
        chunk_offsets = cls._parse_chunk_offsets(stream)
        # IHDR chunk is mandatory, invalid if not present
        if 'IHDR' not in chunk_offsets:
            raise InvalidImageStreamError('no IHDR chunk in PNG image')
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
            if chunk_type == 'IEND':
                break
            # incr offset for chunk len long, chunk type, chunk data, and CRC
            chunk_offset += (4 + 4 + chunk_data_len + 4)

    @classmethod
    def _parse_chunks(cls, stream, chunk_offsets):
        """
        Return a dict of field, value pairs parsed from the chunks in
        *stream* having offsets in *chunk_offsets*.
        """
        raise NotImplementedError
