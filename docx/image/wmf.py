# encoding: utf-8

from __future__ import absolute_import, division, print_function

from .constants import MIME_TYPE
from .helpers import LITTLE_ENDIAN, StreamReader
from .image import BaseImageHeader


class Wmf(BaseImageHeader):
    """
    Image header parser for WMF images
    """
    @classmethod
    def from_stream(cls, stream):
        """
        Return |Wmf| instance having header properties parsed from the WMF
        image in *stream*.
        """
        stream_rdr = StreamReader(stream, LITTLE_ENDIAN)

        # read Aldus Placeable Metafiles header fields
        inch = stream_rdr.read_long(14)
        x0 = stream_rdr.read_short(6)
        y0 = stream_rdr.read_short(8)
        x1 = stream_rdr.read_short(10)
        y1 = stream_rdr.read_short(12)
        
        horz_dpi = cls._dpi()
        vert_dpi = cls._dpi()

        inch_width = (x1 - x0) / inch
        inch_height = (y1 - y0) / inch

        px_width = inch_width * horz_dpi
        px_height = inch_height * vert_dpi

        return cls(px_width, px_height, horz_dpi, vert_dpi)

    @property
    def content_type(self):
        """
        MIME content type for this image, unconditionally `image/wmf` for
        WMF images.
        """
        return MIME_TYPE.WMF

    @property
    def default_ext(self):
        """
        Default filename extension, always 'wmf' for WMF images.
        """
        return 'wmf'

    @staticmethod
    def _dpi():
        """
        Defaulting to 96 pixels per inch
        """
        return 96
