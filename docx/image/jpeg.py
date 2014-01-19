# encoding: utf-8

from __future__ import absolute_import, division, print_function

from .image import Image


class Jpeg(Image):
    """
    Base class for JFIF and EXIF subclasses.
    """


class Exif(Jpeg):
    """
    Image header parser for Exif image format
    """


class Jfif(Jpeg):
    """
    Image header parser for JFIF image format
    """
