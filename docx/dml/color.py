# encoding: utf-8

"""
DrawingML objects related to color, ColorFormat being the most prominent.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..shared import ElementProxy


class ColorFormat(ElementProxy):
    """
    Provides access to color settings such as RGB color, theme color, and
    luminance adjustments.
    """

    __slots__ = ()

    def __init__(self, rPr_parent):
        super(ColorFormat, self).__init__(rPr_parent)
