# encoding: utf-8

from __future__ import absolute_import, division, print_function

from .image import Image


class Gif(Image):
    """
    Image header parser for GIF images. Note that the GIF format does not
    support resolution (DPI) information. Both horizontal and vertical DPI
    default to 72.
    """
