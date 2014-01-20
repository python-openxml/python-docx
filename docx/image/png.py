# encoding: utf-8

from __future__ import absolute_import, division, print_function

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
        raise NotImplementedError
