# encoding: utf-8

from __future__ import absolute_import, division, print_function

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
        return cls(None, None, None, None)
