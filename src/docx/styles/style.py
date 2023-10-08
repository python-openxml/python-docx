"""Style object hierarchy."""

from __future__ import annotations

from typing import Type

from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.styles import CT_Style
from docx.shared import ElementProxy
from docx.styles import BabelFish
from docx.text.font import Font
from docx.text.parfmt import ParagraphFormat


def StyleFactory(style_elm: CT_Style) -> BaseStyle:
    """Return `Style` object of appropriate |BaseStyle| subclass for `style_elm`."""
    style_cls: Type[BaseStyle] = {
        WD_STYLE_TYPE.PARAGRAPH: ParagraphStyle,
        WD_STYLE_TYPE.CHARACTER: CharacterStyle,
        WD_STYLE_TYPE.TABLE: _TableStyle,
        WD_STYLE_TYPE.LIST: _NumberingStyle,
    }[style_elm.type]

    return style_cls(style_elm)


class BaseStyle(ElementProxy):
    """Base class for the various types of style object, paragraph, character, table,
    and numbering.

    These properties and methods are inherited by all style objects.
    """

    def __init__(self, style_elm: CT_Style):
        super().__init__(style_elm)
        self._style_elm = style_elm

    @property
    def builtin(self):
        """Read-only.

        |True| if this style is a built-in style. |False| indicates it is a custom
        (user-defined) style. Note this value is based on the presence of a
        `customStyle` attribute in the XML, not on specific knowledge of which styles
        are built into Word.
        """
        return not self._element.customStyle

    def delete(self):
        """Remove this style definition from the document.

        Note that calling this method does not remove or change the style applied to any
        document content. Content items having the deleted style will be rendered using
        the default style, as is any content with a style not defined in the document.
        """
        self._element.delete()
        self._element = None

    @property
    def hidden(self):
        """|True| if display of this style in the style gallery and list of recommended
        styles is suppressed.

        |False| otherwise. In order to be shown in the style gallery, this value must be
        |False| and :attr:`.quick_style` must be |True|.
        """
        return self._element.semiHidden_val

    @hidden.setter
    def hidden(self, value):
        self._element.semiHidden_val = value

    @property
    def locked(self):
        """Read/write Boolean.

        |True| if this style is locked. A locked style does not appear in the styles
        panel or the style gallery and cannot be applied to document content. This
        behavior is only active when formatting protection is turned on for the document
        (via the Developer menu).
        """
        return self._element.locked_val

    @locked.setter
    def locked(self, value):
        self._element.locked_val = value

    @property
    def name(self):
        """The UI name of this style."""
        name = self._element.name_val
        if name is None:
            return None
        return BabelFish.internal2ui(name)

    @name.setter
    def name(self, value):
        self._element.name_val = value

    @property
    def priority(self):
        """The integer sort key governing display sequence of this style in the Word UI.

        |None| indicates no setting is defined, causing Word to use the default value of
        0. Style name is used as a secondary sort key to resolve ordering of styles
        having the same priority value.
        """
        return self._element.uiPriority_val

    @priority.setter
    def priority(self, value):
        self._element.uiPriority_val = value

    @property
    def quick_style(self):
        """|True| if this style should be displayed in the style gallery when
        :attr:`.hidden` is |False|.

        Read/write Boolean.
        """
        return self._element.qFormat_val

    @quick_style.setter
    def quick_style(self, value):
        self._element.qFormat_val = value

    @property
    def style_id(self) -> str:
        """The unique key name (string) for this style.

        This value is subject to rewriting by Word and should generally not be changed
        unless you are familiar with the internals involved.
        """
        return self._style_elm.styleId

    @style_id.setter
    def style_id(self, value):
        self._element.styleId = value

    @property
    def type(self):
        """Member of :ref:`WdStyleType` corresponding to the type of this style, e.g.
        ``WD_STYLE_TYPE.PARAGRAPH``."""
        type = self._style_elm.type
        if type is None:
            return WD_STYLE_TYPE.PARAGRAPH
        return type

    @property
    def unhide_when_used(self):
        """|True| if an application should make this style visible the next time it is
        applied to content.

        False otherwise. Note that |docx| does not automatically unhide a style having
        |True| for this attribute when it is applied to content.
        """
        return self._element.unhideWhenUsed_val

    @unhide_when_used.setter
    def unhide_when_used(self, value):
        self._element.unhideWhenUsed_val = value


class CharacterStyle(BaseStyle):
    """A character style.

    A character style is applied to a |Run| object and primarily provides character-
    level formatting via the |Font| object in its :attr:`.font` property.
    """

    @property
    def base_style(self):
        """Style object this style inherits from or |None| if this style is not based on
        another style."""
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
        """The |Font| object providing access to the character formatting properties for
        this style, such as font name and size."""
        return Font(self._element)


# -- just in case someone uses the old name in an extension function --
_CharacterStyle = CharacterStyle


class ParagraphStyle(CharacterStyle):
    """A paragraph style.

    A paragraph style provides both character formatting and paragraph formatting such
    as indentation and line-spacing.
    """

    def __repr__(self):
        return "_ParagraphStyle('%s') id: %s" % (self.name, id(self))

    @property
    def next_paragraph_style(self):
        """|_ParagraphStyle| object representing the style to be applied automatically
        to a new paragraph inserted after a paragraph of this style.

        Returns self if no next paragraph style is defined. Assigning |None| or `self`
        removes the setting such that new paragraphs are created using this same style.
        """
        next_style_elm = self._element.next_style
        if next_style_elm is None:
            return self
        if next_style_elm.type != WD_STYLE_TYPE.PARAGRAPH:
            return self
        return StyleFactory(next_style_elm)

    @next_paragraph_style.setter
    def next_paragraph_style(self, style):
        if style is None or style.style_id == self.style_id:
            self._element._remove_next()
        else:
            self._element.get_or_add_next().val = style.style_id

    @property
    def paragraph_format(self):
        """The |ParagraphFormat| object providing access to the paragraph formatting
        properties for this style such as indentation."""
        return ParagraphFormat(self._element)


# -- just in case someone uses the old name in an extension function --
_ParagraphStyle = ParagraphStyle


class _TableStyle(ParagraphStyle):
    """A table style.

    A table style provides character and paragraph formatting for its contents as well
    as special table formatting properties.
    """

    def __repr__(self):
        return "_TableStyle('%s') id: %s" % (self.name, id(self))


class _NumberingStyle(BaseStyle):
    """A numbering style.

    Not yet implemented.
    """
