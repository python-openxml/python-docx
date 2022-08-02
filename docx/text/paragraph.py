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
from .hyperlink import Hyperlink
from ..runcntnr import RunItemContainer
from docx.oxml.ns import qn


class Paragraph(RunItemContainer):
    """
    Proxy object wrapping ``<w:p>`` element.
    """
    def __init__(self, p, parent):
        super(Paragraph, self).__init__(p, parent)
        self._p = p

    def add_hyperlink(self, text=None, style=None, anchor=None, hyperlink_url=None,
                      relationship_id=None, document=None):
        if hyperlink_url is not None and document is None:
            raise ValueError("Need document object to add hyperlink URL.")
        if hyperlink_url is not None and relationship_id is not None:
            raise ValueError("Only one of `hyperlink_url` and `relationship_id` can be set at once.")
        
        _hyperlink = self._element.add_hyperlink()

        hyperlink = Hyperlink(_hyperlink, self)
        run = hyperlink.add_run(text, style)
        if anchor is not None:
            hyperlink.anchor = anchor
        if relationship_id is not None:
            hyperlink.relationship_id = relationship_id
        if hyperlink_url is not None and document is not None:
            if style is None:
                _hyperlink_style = Hyperlink.add_hyperlink_styles(document)
                run.style = "Hyperlink"
            else:
                run.style = style
            rel = document.add_hyperlink_relationship(hyperlink_url)
            hyperlink.relationship_id = rel.rId
        return hyperlink

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
    def hyperlinks(self):
        """
        Sequence of |Hyperlink| instances. Corresponds to the ``<w:hyperlink>`` elements
        in this paragraph.
        """
        return [Hyperlink(_h, self) for _h in self._element.hyperlink_lst]

    @property
    def paragraph_format(self):
        """
        The |ParagraphFormat| object providing access to the formatting
        properties for this paragraph, such as line spacing and indentation.
        """
        return ParagraphFormat(self._element)

    @property
    def runs(self):
        """
        Sequence of |Run| instances. Correponds to the ``<w:r>`` elements
        in this paragraph, and ``<w:r>`` elements in ``<w:hyperlink>`` elements
        in this paragraph.

        |Run| instances are returned in document order.
        """
        ret_list = []
        for child in self._element[:]:
            if child.tag == qn('w:r'):
                ret_list.append(Run(child, self))
            if child.tag == qn('w:hyperlink'):
                _hyperlink = Hyperlink(child, self)
                for sub_run_elem in _hyperlink._element.r_lst:
                    ret_list.append(Run(sub_run_elem, _hyperlink))
        return ret_list

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

    def _insert_paragraph_before(self):
        """
        Return a newly created paragraph, inserted directly before this
        paragraph.
        """
        p = self._p.add_p_before()
        return Paragraph(p, self._parent)
