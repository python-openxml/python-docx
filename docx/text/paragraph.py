# encoding: utf-8

"""
Paragraph-related proxy types.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..enum.style import WD_STYLE_TYPE
from .parfmt import ParagraphFormat
from .run import Run
from ..shared import Parented
from ..runcntnr import RunItemContainer
from .hyperlink import Hyperlink
from ..oxml.ns import qn

class Paragraph(RunItemContainer):
    """
    Proxy object wrapping ``<w:p>`` element.
    """
    def __init__(self, p, parent):
        super(Paragraph, self).__init__(p, parent)
        self._p = self._element = p

    def add_run(self, text=None, style=None):
        return super(Paragraph, self).add_paragraph(text, style)

    @property
    def alignment(self):
        """
        A member of the :ref:`WdParagraphAlignment` enumeration specifying
        the justification setting for this paragraph. A value of |None|
        indicates the paragraph has no directly-applied alignment value and
        will inherit its alignment value from its style hierarchy. Assigning
        |None| to this property removes any directly-applied alignment value.
        """
        return self._p.alignment

    @alignment.setter
    def alignment(self, value):
        self._p.alignment = value

    def clear(self):
        """
        Return this same paragraph after removing all its content.
        Paragraph-level formatting, such as style, is preserved.
        """
        self._p.clear_content()
        return self

    def insert_paragraph_before(self, text=None, style=None):
        """
        Return a newly created paragraph, inserted directly before this
        paragraph. If *text* is supplied, the new paragraph contains that
        text in a single run. If *style* is provided, that style is assigned
        to the new paragraph.
        """
        paragraph = self._insert_paragraph_before()
        if text:
            paragraph.add_run(text)
        if style is not None:
            paragraph.style = style
        return paragraph

    @property
    def paragraph_format(self):
        """
        The |ParagraphFormat| object providing access to the formatting
        properties for this paragraph, such as line spacing and indentation.
        """
        return ParagraphFormat(self._element)

    @property
    def runs(self):
        return super(Paragraph, self).runs
    
    @property
    def inline_items(self):
        return [self._get_inline_item_class(t.tag)(t, self) for t in self._p.inline_items]

    @property
    def style(self):
        """
        Read/Write. |_ParagraphStyle| object representing the style assigned
        to this paragraph. If no explicit style is assigned to this
        paragraph, its value is the default paragraph style for the document.
        A paragraph style name can be assigned in lieu of a paragraph style
        object. Assigning |None| removes any applied style, making its
        effective value the default paragraph style for the document.
        """
        style_id = self._p.style
        return self.part.get_style(style_id, WD_STYLE_TYPE.PARAGRAPH)

    @style.setter
    def style(self, style_or_name):
        style_id = self.part.get_style_id(
            style_or_name, WD_STYLE_TYPE.PARAGRAPH
        )
        self._p.style = style_id

    @property
    def text(self):
        """
        String formed by concatenating the text of each run in the paragraph.
        Tabs and line breaks in the XML are mapped to ``\\t`` and ``\\n``
        characters respectively.

        Assigning text to this property causes all existing paragraph content
        to be replaced with a single run containing the assigned text.
        A ``\\t`` character in the text is mapped to a ``<w:tab/>`` element
        and each ``\\n`` or ``\\r`` character is mapped to a line break.
        Paragraph-level formatting, such as style, is preserved. All
        run-level formatting, such as bold or italic, is removed.
        """
        text = ''
        for inline in self.inline_items:
            text += inline.text
        return text

    @text.setter
    def text(self, text):
        self.clear()
        self.add_run(text)

    def _insert_paragraph_before(self):
        """
        Return a newly created paragraph, inserted directly before this
        paragraph.
        """
        p = self._p.add_p_before()
        return Paragraph(p, self._parent)

    def _get_inline_item_class(self, tag):
        if tag == qn('w:r'):
            return Run

        if tag == qn('w:hyperlink'):
            return Hyperlink
