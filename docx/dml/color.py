# encoding: utf-8

"""
DrawingML objects related to color, ColorFormat being the most prominent.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..enum.dml import MSO_COLOR_TYPE
from ..oxml.simpletypes import ST_HexColorAuto
from ..shared import ElementProxy


class ColorFormat(ElementProxy):
    """
    Provides access to color settings such as RGB color, theme color, and
    luminance adjustments.
    """

    __slots__ = ()

    def __init__(self, rPr_parent):
        super(ColorFormat, self).__init__(rPr_parent)

    @property
    def type(self):
        """
        Read-only. A member of :ref:`MsoColorType`, one of RGB, THEME, or
        AUTO, corresponding to the way this color is defined. Its value is
        |None| if no color is applied at this level, which causes the
        effective color to be inherited from the style hierarchy.
        """
        rPr = self._element.rPr
        if rPr is None:
            return None
        color = rPr.color
        if color is None:
            return None
        if color.themeColor is not None:
            return MSO_COLOR_TYPE.THEME
        if color.val == ST_HexColorAuto.AUTO:
            return MSO_COLOR_TYPE.AUTO
        return MSO_COLOR_TYPE.RGB
