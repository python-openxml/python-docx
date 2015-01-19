# encoding: utf-8

"""
Style object hierarchy.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..enum.style import WD_STYLE_TYPE
from ..shared import ElementProxy
from ..text.paragraph import ParagraphFormat
from ..text.run import Font


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
    table, and numbering. These properties and methods are inherited by all
    style objects.
    """

    __slots__ = ()

    @property
    def builtin(self):
        """
        Read-only. |True| if this style is a built-in style. |False|
        indicates it is a custom (user-defined) style. Note this value is
        based on the presence of a `customStyle` attribute in the XML, not on
        specific knowledge of which styles are built into Word.
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
    def hidden(self):
        """
        True if display of this style in the style gallery and list of
        recommended styles is suppressed. False otherwise. In order to be
        shown in the style gallery, this value must be |False| and
        :attr:`.quick_style` must be |True|.
        """
        return self._element.semiHidden_val

    @hidden.setter
    def hidden(self, value):
        self._element.semiHidden_val = value

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
    def priority(self):
        """
        The integer sort key governing display sequence of this style in the
        Word UI. |None| indicates no setting is defined, causing Word to use
        the default value of 0. Style name is used as a secondary sort key to
        resolve ordering of styles having the same priority value.
        """
        return self._element.uiPriority_val

    @priority.setter
    def priority(self, value):
        self._element.uiPriority_val = value

    @property
    def style_id(self):
        """
        The unique key name (string) for this style. This value is subject to
        rewriting by Word and should generally not be changed unless you are
        familiar with the internals involved.
        """
        return self._element.styleId

    @style_id.setter
    def style_id(self, value):
        self._element.styleId = value

    @property
    def type(self):
        """
        Member of :ref:`WdStyleType` corresponding to the type of this style,
        e.g. ``WD_STYLE_TYPE.PARAGRAPH``.
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
    A character style. A character style is applied to a |Run| object and
    primarily provides character-level formatting via the |Font| object in
    its :attr:`.font` property.
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

    @base_style.setter
    def base_style(self, style):
        style_id = style.style_id if style is not None else None
        self._element.basedOn_val = style_id

    @property
    def font(self):
        """
        The |Font| object providing access to the character formatting
        properties for this style, such as font name and size.
        """
        return Font(self._element)


class _ParagraphStyle(_CharacterStyle):
    """
    A paragraph style. A paragraph style provides both character formatting
    and paragraph formatting such as indentation and line-spacing.
    """

    __slots__ = ()

    @property
    def paragraph_format(self):
        """
        The |ParagraphFormat| object providing access to the paragraph
        formatting properties for this style such as indentation.
        """
        return ParagraphFormat(self._element)


class _TableStyle(_ParagraphStyle):
    """
    A table style. A table style provides character and paragraph formatting
    for its contents as well as special table formatting properties.
    """

    __slots__ = ()


class _NumberingStyle(BaseStyle):
    """
    A numbering style. Not yet implemented.
    """

    __slots__ = ()
