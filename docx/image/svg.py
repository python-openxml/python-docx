from __future__ import absolute_import, division, print_function

from willow.image import Image

from .constants import MIME_TYPE
from .image import BaseImageHeader


class Svg(BaseImageHeader):
    """
    Image header parser for SVG images. Handles both big and little endian
    byte ordering.
    """
    @property
    def content_type(self):
        """
        Return the MIME type of this SVG image, unconditionally the string
        ``image/svg``.
        """
        return MIME_TYPE.SVG

    @property
    def default_ext(self):
        """
        Default filename extension, always 'svg' for SVG images.
        """
        return 'svg'

    @classmethod
    def from_stream(cls, stream):
        """
        Return a |Svg| instance containing the properties of the SVG image
        in *stream*.
        """
        px_width, px_height = Image.open(stream).get_size()
        horz_dpi, vert_dpi = 96, 96

        return cls(px_width, px_height, horz_dpi, vert_dpi)
