# encoding: utf-8

from __future__ import absolute_import, division, print_function

import xml.etree.ElementTree as ET

from .constants import MIME_TYPE
from .image import BaseImageHeader


class Svg(BaseImageHeader):
    """
    Image header parser for SVG images.
    """

    @classmethod
    def from_stream(cls, stream):
        """
        Return |Svg| instance having header properties parsed from SVG image
        in *stream*.
        """
        px_width, px_height = cls._dimensions_from_stream(stream)
        return cls(px_width, px_height, 72, 72)

    @property
    def content_type(self):
        """
        MIME content type for this image, unconditionally `image/svg+xml` for
        SVG images.
        """
        return MIME_TYPE.SVG

    @property
    def default_ext(self):
        """
        Default filename extension, always 'svg' for SVG images.
        """
        return "svg"

    @classmethod
    def _dimensions_from_stream(cls, stream):
        stream.seek(0)
        data = stream.read()
        root = ET.fromstring(data)
        # FIXME: The width could be expressed as '4cm'
        # See https://www.w3.org/TR/SVG11/struct.html#NewDocument
        width = int(root.attrib["width"])
        height = int(root.attrib["height"])
        return width, height
