# encoding: utf-8

from __future__ import absolute_import, division, print_function

from .image import Image


class Tiff(Image):
    """
    Image header parser for TIFF images. Handles both big and little endian
    byte ordering.
    """
