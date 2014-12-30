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
    def builtin(self):
        """
        Boolean indicating whether this style is a built-in style. False
        indicates it is a custom (user-defined) style.
        """
        return not self._element.customStyle

    def delete(self):
        """
        Remove this style definition from the document. Note that calling
        this method does not remove or change the style applied to any
        document content. Content items having the deleted style will be
        rendered using the default style, as is any content with a style not
        defined in the document.
        """
        self._element.delete()
        self._element = None

    @property
    def name(self):
        """
        The UI name of this style.
        """
        name = self._element.name_val
        if name is not None:
            return self._translate_special_case_names(name)
        return name

    @name.setter
    def name(self, value):
        self._element.name_val = value

    @property
    def style_id(self):
        """
        The unique key name (string) for this style.
        """
        return self._element.styleId

    @style_id.setter
    def style_id(self, value):
        self._element.styleId = value

    @property
    def type(self):
        """
        Member of :ref:`WdStyleType` corresponding to the type of this style,
        e.g. ``WD_STYLE_TYPE.PARAGRAPH`.
        """
        type = self._element.type
        if type is None:
            return WD_STYLE_TYPE.PARAGRAPH
        return type

    @staticmethod
    def _translate_special_case_names(name):
        """
        Translate special-case style names to their English UI counterparts.
        Some style names are stored differently than they appear in the UI,
        with a leading lowercase letter, perhaps for legacy reasons.
        """
        return {
            'caption':   'Caption',
            'heading 1': 'Heading 1',
            'heading 2': 'Heading 2',
            'heading 3': 'Heading 3',
            'heading 4': 'Heading 4',
            'heading 5': 'Heading 5',
            'heading 6': 'Heading 6',
            'heading 7': 'Heading 7',
            'heading 8': 'Heading 8',
            'heading 9': 'Heading 9',
        }.get(name, name)


class _CharacterStyle(BaseStyle):
    """
    A character style.
    """

    __slots__ = ()

    @property
    def base_style(self):
        """
        Style object this style inherits from or |None| if this style is
        not based on another style.
        """
        base_style = self._element.base_style
        if base_style is None:
            return None
        return StyleFactory(base_style)


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
