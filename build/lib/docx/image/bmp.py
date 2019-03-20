# encoding: utf-8

from __future__ import absolute_import, division, print_function

from .constants import MIME_TYPE
from .helpers import LITTLE_ENDIAN, StreamReader
from .image import BaseImageHeader


class Bmp(BaseImageHeader):
    """
    Image header parser for BMP images
    """
    @classmethod
    def from_stream(cls, stream):
        """
        Return |Bmp| instance having header properties parsed from the BMP
        image in *stream*.
        """
        stream_rdr = StreamReader(stream, LITTLE_ENDIAN)

        px_width = stream_rdr.read_long(0x12)
        px_height = stream_rdr.read_long(0x16)

        horz_px_per_meter = stream_rdr.read_long(0x26)
        vert_px_per_meter = stream_rdr.read_long(0x2A)

        horz_dpi = cls._dpi(horz_px_per_meter)
        vert_dpi = cls._dpi(vert_px_per_meter)

        return cls(px_width, px_height, horz_dpi, vert_dpi)

    @property
    def content_type(self):
        """
        MIME content type for this image, unconditionally `image/bmp` for
        BMP images.
        """
        return MIME_TYPE.BMP

    @property
    def default_ext(self):
        """
        Default filename extension, always 'bmp' for BMP images.
        """
        return 'bmp'

    @staticmethod
    def _dpi(px_per_meter):
        """
        Return the integer pixels per inch from *px_per_meter*, defaulting to
        96 if *px_per_meter* is zero.
        """
        if px_per_meter == 0:
            return 96
        return int(round(px_per_meter * 0.0254))
