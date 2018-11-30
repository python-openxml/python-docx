# encoding: utf-8

"""
|Header| and |Footer| objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from .blkcntnr import BlockItemContainer
from .shared import ElementProxy, Emu


class _HeaderFooter(ElementProxy):

    __slots__ = ('_type', '__body')

    def __init__(self, element, parent, hf_type):
        super(_HeaderFooter, self).__init__(element, parent)
        self._type = hf_type
        self.__body = None

    def add_paragraph(self, text='', style=None):
        """
        Return a paragraph, populated
        with *text* and having paragraph style *style*. *text* can contain
        tab (``\\t``) characters, which are converted to the appropriate XML
        form for a tab. *text* can also include newline (``\\n``) or carriage
        return (``\\r``) characters, each of which is converted to a line
        break.
        """
        return self._body.add_paragraph(text, style)

    @property
    def paragraphs(self):
        """
            A list of |Paragraph| instances corresponding to the paragraphs in
            this object. Note that paragraphs within revision
            marks such as ``<w:ins>`` or ``<w:del>`` do not appear in this list.
        """
        return self._body.paragraphs

    def add_table(self, rows, cols, style=None):
        """
            Add a table having row and column counts of *rows* and *cols*
            respectively and table style of *style*. *style* may be a paragraph
            style object or a paragraph style name. If *style* is |None|, the
            table inherits the default table style of the document.
        """
        table = self._body.add_table(rows, cols, self._block_width)
        table.style = style
        return table

    @property
    def tables(self):
        """
            A list of |Table| instances corresponding to the tables in
            this object. Note that only tables appearing at the
            top level of the document appear in this list; a table nested inside
            a table cell does not appear. A table within revision marks such as
            ``<w:ins>`` or ``<w:del>`` will also not appear in the list.
        """

        return self._body.tables

    @property
    def _block_width(self):
        """
        Return a |Length| object specifying the width of available "writing"
        space between the margins of the last section of this document.
        """
        section = self._parent
        return Emu(
            section.page_width - section.left_margin - section.right_margin
        )

    @property
    def _body(self):
        if self.__body is None:
            ref = self._parent.sectPr.get_header_reference_of_type(self._type)
            if ref is None:
                return None
            part = self.part.get_related_part(ref.rId)
            if part is not None:
                self.__body = _HeaderFooterBody(part._element, self)

        return self.__body


class Header(_HeaderFooter):

    @property
    def is_linked_to_previous(self):
        """

            :return: True when is linked to previous header otherwise false
        """
        if self._parent is None:
            return True
        return True if self._parent.sectPr.get_header_reference_of_type(self._type) is None else False

    @is_linked_to_previous.setter
    def is_linked_to_previous(self, value):
        """
            - if previous value is True and value is False then need to create new header
            - if previous value is False and value is True then need to remove reference
        """
        if self.is_linked_to_previous is True and value is False:
            rId = self.part.add_header_part()
            self._parent.sectPr.add_header_reference_of_type(rId, self._type)
            self.add_paragraph('')
        elif self.is_linked_to_previous is False and value is True:
            self._parent.sectPr.remove_header_reference(self._type)
            self.__body = None


class Footer(_HeaderFooter):

    @property
    def is_linked_to_previous(self):
        """

        :return: True when is linked otherwise false
        """
        if self._parent is None:
            return True
        return True if self._parent.sectPr.get_footer_reference_of_type(self._type) is None else False

    @is_linked_to_previous.setter
    def is_linked_to_previous(self, value):
        """
            - if previous value is True and value is False then need to create new footer
            - if previous value is False and value is True then need to remove reference
        """
        if self.is_linked_to_previous is True and value is False:
            rId = self.part.add_footer_part(self._type)
            self._parent.sectPr.add_footer_reference_of_type(rId, self._type)
        elif self.is_linked_to_previous is False and value is True:
            self._parent.sectPr.remove_footer_reference(self._type)
            self.__body = None


class _HeaderFooterBody(BlockItemContainer):
    pass
