# encoding: utf-8

from __future__ import absolute_import, division, print_function

from .image import BaseImageHeader


class Bmp(BaseImageHeader):
    """
    Image header parser for BMP images
    """
    @classmethod
    def from_stream(cls, stream):
        """
        Return |Bmp| instance having header properties parsed from BMP image
        in *stream*.
        """
        return cls(None, None, None, None)
