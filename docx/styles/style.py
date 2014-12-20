# encoding: utf-8

"""
Style object hierarchy.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..enum.style import WD_STYLE_TYPE
from ..shared import ElementProxy


def StyleFactory(style_elm):
    """
    Return a style object of the appropriate |BaseStyle| subclass, according
    to the type of *style_elm*.
    """
    style_cls = {
        WD_STYLE_TYPE.PARAGRAPH: _ParagraphStyle,
        WD_STYLE_TYPE.CHARACTER: _CharacterStyle,
        WD_STYLE_TYPE.TABLE:     _TableStyle,
        WD_STYLE_TYPE.LIST:      _NumberingStyle
    }[style_elm.type]

    return style_cls(style_elm)


class BaseStyle(ElementProxy):
    """
    Base class for the various types of style object, paragraph, character,
    table, and numbering.
    """

    __slots__ = ()

    @property
    def style_id(self):
        """
        The unique key name (string) for this style.
        """
        return self._element.styleId

    @style_id.setter
    def style_id(self, value):
        self._element.styleId = value


class _CharacterStyle(BaseStyle):
    """
    A character style.
    """

    __slots__ = ()


class _ParagraphStyle(_CharacterStyle):
    """
    A paragraph style.
    """

    __slots__ = ()


class _TableStyle(_ParagraphStyle):
    """
    A table style.
    """

    __slots__ = ()


class _NumberingStyle(BaseStyle):
    """
    A numbering style.
    """

    __slots__ = ()
