# encoding: utf-8

"""Block item container, used by body, cell, header, etc.

Block level items are things like paragraph and table, although there are a few other
specialized ones like structured document tags.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from docx.oxml.table import CT_Tbl
from docx.shared import Parented
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

    def add_paragraph(self, text='', style=None):
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

    def add_table_from_df(self, df, width, header):
        """
        Return a table with the data from the dataframe along with the column headings
        """
        idx_shift = 1 if header else 0
        tbl = self.add_table(
            rows=df.shape[0] + idx_shift, cols=df.shape[1], width=width
        )

        if header:
            # Add the column headings
            for j in range(df.shape[1]):
                tbl.cell(0, j).text = df.columns[j]

        # Add the body of the data frame
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                cell = df.iat[i, j]
                tbl.cell(i + idx_shift, j).text = str(cell)

        return tbl

    @property
    def paragraphs(self):
        """
        A list containing the paragraphs in this container, in document
        order. Read-only.
        """
        return [Paragraph(p, self) for p in self._element.p_lst]

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
