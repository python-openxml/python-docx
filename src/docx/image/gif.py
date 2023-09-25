# encoding: utf-8

from __future__ import absolute_import, division, print_function

from struct import Struct

from .constants import MIME_TYPE
from .image import BaseImageHeader


class Gif(BaseImageHeader):
    """
    Image header parser for GIF images. Note that the GIF format does not
    support resolution (DPI) information. Both horizontal and vertical DPI
    default to 72.
    """

    @classmethod
    def from_stream(cls, stream):
        """
        Return |Gif| instance having header properties parsed from GIF image
        in *stream*.
        """
        px_width, px_height = cls._dimensions_from_stream(stream)
        return cls(px_width, px_height, 72, 72)

    @property
    def content_type(self):
        """
        MIME content type for this image, unconditionally `image/gif` for
        GIF images.
        """
        return MIME_TYPE.GIF

    @property
    def default_ext(self):
        """
        Default filename extension, always 'gif' for GIF images.
        """
        return "gif"

    @classmethod
    def _dimensions_from_stream(cls, stream):
        stream.seek(6)
        bytes_ = stream.read(4)
        struct = Struct("<HH")
        px_width, px_height = struct.unpack(bytes_)
        return px_width, px_height
