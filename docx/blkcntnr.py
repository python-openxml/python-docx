# encoding: utf-8

"""Block item container, used by body, cell, header, etc.

Block level items are things like paragraph and table, although there are a few other
specialized ones like structured document tags.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from docx.bookmark import _Bookmark
from docx.oxml.table import CT_Tbl
from docx.shared import lazyproperty, Parented
from docx.text.paragraph import Paragraph


class BlockItemContainer(Parented):
    """Base class for proxy objects that can contain block items.

    These containers include _Body, _Cell, header, footer, footnote, endnote, comment,
    and text box objects. Provides the shared functionality to add a block item like
    a paragraph or table.
    """

    def __init__(self, element, parent):
        super(BlockItemContainer, self).__init__(parent)
        self._element = element

    def add_paragraph(self, text="", style=None):
        """
        Return a paragraph newly added to the end of the content in this
        container, having *text* in a single run if present, and having
        paragraph style *style*. If *style* is |None|, no paragraph style is
        applied, which has the same effect as applying the 'Normal' style.
        """
        paragraph = self._add_paragraph()
        if text:
            paragraph.add_run(text)
        if style is not None:
            paragraph.style = style
        return paragraph

    def add_table(self, rows, cols, width):
        """
        Return a table of *width* having *rows* rows and *cols* columns,
        newly appended to the content in this container. *width* is evenly
        distributed between the table columns.
        """
        from .table import Table

        tbl = CT_Tbl.new_tbl(rows, cols, width)
        self._element._insert_tbl(tbl)
        return Table(tbl, self)

    def end_bookmark(self, bookmark):
        """Return `bookmark` after closing it after last block item in container."""
        raise NotImplementedError

    @property
    def paragraphs(self):
        """
        A list containing the paragraphs in this container, in document
        order. Read-only.
        """
        return [Paragraph(p, self) for p in self._element.p_lst]

    def start_bookmark(self, name):
        """Return newly-added |_Bookmark| object identified by `name`.

        The returned bookmark is anchored at the end of this block-item container, for
        example, after the last paragraph in the document when the document body is the
        block-item container.
        """
        if name in self._bookmarks:
            raise KeyError("Document already contains bookmark with name %s" % name)

        return _Bookmark(
            (self._element.add_bookmarkStart(name, self._bookmarks.next_id), None)
        )

    @property
    def tables(self):
        """
        A list containing the tables in this container, in document order.
        Read-only.
        """
        from .table import Table

        return [Table(tbl, self) for tbl in self._element.tbl_lst]

    def _add_paragraph(self):
        """
        Return a paragraph newly added to the end of the content in this
        container.
        """
        return Paragraph(self._element.add_p(), self)

    @lazyproperty
    def _bookmarks(self):
        """Global |Bookmarks| object for overall document."""
        return self.part.bookmarks
