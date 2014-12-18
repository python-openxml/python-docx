# encoding: utf-8

"""
The |Table| object and related proxy classes.
"""

from __future__ import absolute_import, print_function, unicode_literals

from .blkcntnr import BlockItemContainer
from .oxml.simpletypes import ST_Merge
from .shared import lazyproperty, Parented


class Table(Parented):
    """
    Proxy class for a WordprocessingML ``<w:tbl>`` element.
    """
    def __init__(self, tbl, parent):
        super(Table, self).__init__(parent)
        self._tbl = tbl

    def add_column(self):
        """
        Return a |_Column| instance, newly added rightmost to the table.
        """
        tblGrid = self._tbl.tblGrid
        gridCol = tblGrid.add_gridCol()
        for tr in self._tbl.tr_lst:
            tr.add_tc()
        return _Column(gridCol, self)

    def add_row(self):
        """
        Return a |_Row| instance, newly added bottom-most to the table.
        """
        tbl = self._tbl
        tr = tbl.add_tr()
        for gridCol in tbl.tblGrid.gridCol_lst:
            tr.add_tc()
        return _Row(tr, self)

    @property
    def alignment(self):
        """
        Read/write. A member of :ref:`WdRowAlignment` or None, specifying the
        positioning of this table between the page margins. |None| if no
        setting is specified, causing the effective value to be inherited
        from the style hierarchy.
        """
        return self._tblPr.alignment

    @alignment.setter
    def alignment(self, value):
        self._tblPr.alignment = value

    @property
    def autofit(self):
        """
        |True| if column widths can be automatically adjusted to improve the
        fit of cell contents. |False| if table layout is fixed. Column widths
        are adjusted in either case if total column width exceeds page width.
        Read/write boolean.
        """
        return self._tblPr.autofit

    @autofit.setter
    def autofit(self, value):
        self._tblPr.autofit = value

    def cell(self, row_idx, col_idx):
        """
        Return |_Cell| instance correponding to table cell at *row_idx*,
        *col_idx* intersection, where (0, 0) is the top, left-most cell.
        """
        cell_idx = col_idx + (row_idx * self._column_count)
        return self._cells[cell_idx]

    def column_cells(self, column_idx):
        """
        Sequence of cells in the column at *column_idx* in this table.
        """
        cells = self._cells
        idxs = range(column_idx, len(cells), self._column_count)
        return [cells[idx] for idx in idxs]

    @lazyproperty
    def columns(self):
        """
        |_Columns| instance containing the sequence of columns in this table.
        """
        return _Columns(self._tbl, self)

    def row_cells(self, row_idx):
        """
        Sequence of cells in the row at *row_idx* in this table.
        """
        column_count = self._column_count
        start = row_idx * column_count
        end = start + column_count
        return self._cells[start:end]

    @lazyproperty
    def rows(self):
        """
        |_Rows| instance containing the sequence of rows in this table.
        """
        return _Rows(self._tbl, self)

    @property
    def style(self):
        """
        String name of style to be applied to this table, e.g.
        'LightShading-Accent1'. Name is derived by removing spaces from the
        table style name displayed in the Word UI.
        """
        return self._tblPr.style

    @style.setter
    def style(self, value):
        self._tblPr.style = value

    @property
    def table(self):
        """
        Provide child objects with reference to the |Table| object they
        belong to, without them having to know their direct parent is
        a |Table| object. This is the terminus of a series of `parent._table`
        calls from an arbitrary child through its ancestors.
        """
        return self

    @property
    def _cells(self):
        """
        A sequence of |_Cell| objects, one for each cell of the layout grid.
        If the table contains a span, one or more |_Cell| object references
        are repeated.
        """
        col_count = self._column_count
        cells = []
        for tc in self._tbl.iter_tcs():
            for grid_span_idx in range(tc.grid_span):
                if tc.vMerge == ST_Merge.CONTINUE:
                    cells.append(cells[-col_count])
                elif grid_span_idx > 0:
                    cells.append(cells[-1])
                else:
                    cells.append(_Cell(tc, self))
        return cells

    @property
    def _column_count(self):
        """
        The number of grid columns in this table.
        """
        return self._tbl.col_count

    @property
    def _tblPr(self):
        return self._tbl.tblPr


class _Cell(BlockItemContainer):
    """
    Table cell
    """
    def __init__(self, tc, parent):
        super(_Cell, self).__init__(tc, parent)
        self._tc = tc

    def add_paragraph(self, text='', style=None):
        """
        Return a paragraph newly added to the end of the content in this
        cell. If present, *text* is added to the paragraph in a single run.
        If specified, the paragraph style *style* is applied. If *style* is
        not specified or is |None|, the result is as though the 'Normal'
        style was applied. Note that the formatting of text in a cell can be
        influenced by the table style. *text* can contain tab (``\\t``)
        characters, which are converted to the appropriate XML form for
        a tab. *text* can also include newline (``\\n``) or carriage return
        (``\\r``) characters, each of which is converted to a line break.
        """
        return super(_Cell, self).add_paragraph(text, style)

    def add_table(self, rows, cols):
        """
        Return a table newly added to this cell after any existing cell
        content, having *rows* rows and *cols* columns. An empty paragraph is
        added after the table because Word requires a paragraph element as
        the last element in every cell.
        """
        new_table = super(_Cell, self).add_table(rows, cols)
        self.add_paragraph()
        return new_table

    def merge(self, other_cell):
        """
        Return a merged cell created by spanning the rectangular region
        having this cell and *other_cell* as diagonal corners. Raises
        |InvalidSpanError| if the cells do not define a rectangular region.
        """
        tc, tc_2 = self._tc, other_cell._tc
        merged_tc = tc.merge(tc_2)
        return _Cell(merged_tc, self._parent)

    @property
    def paragraphs(self):
        """
        List of paragraphs in the cell. A table cell is required to contain
        at least one block-level element and end with a paragraph. By
        default, a new cell contains a single paragraph. Read-only
        """
        return super(_Cell, self).paragraphs

    @property
    def tables(self):
        """
        List of tables in the cell, in the order they appear. Read-only.
        """
        return super(_Cell, self).tables

    @property
    def text(self):
        """
        The entire contents of this cell as a string of text. Assigning
        a string to this property replaces all existing content with a single
        paragraph containing the assigned text in a single run.
        """
        return '\n'.join(p.text for p in self.paragraphs)

    @text.setter
    def text(self, text):
        """
        Write-only. Set entire contents of cell to the string *text*. Any
        existing content or revisions are replaced.
        """
        tc = self._tc
        tc.clear_content()
        p = tc.add_p()
        r = p.add_r()
        r.text = text

    @property
    def width(self):
        """
        The width of this cell in EMU, or |None| if no explicit width is set.
        """
        return self._tc.width

    @width.setter
    def width(self, value):
        self._tc.width = value


class _Column(Parented):
    """
    Table column
    """
    def __init__(self, gridCol, parent):
        super(_Column, self).__init__(parent)
        self._gridCol = gridCol

    @property
    def cells(self):
        """
        Sequence of |_Cell| instances corresponding to cells in this column.
        """
        return tuple(self.table.column_cells(self._index))

    @property
    def table(self):
        """
        Reference to the |Table| object this column belongs to.
        """
        return self._parent.table

    @property
    def width(self):
        """
        The width of this column in EMU, or |None| if no explicit width is
        set.
        """
        return self._gridCol.w

    @width.setter
    def width(self, value):
        self._gridCol.w = value

    @property
    def _index(self):
        """
        Index of this column in its table, starting from zero.
        """
        return self._gridCol.gridCol_idx


class _Columns(Parented):
    """
    Sequence of |_Column| instances corresponding to the columns in a table.
    Supports ``len()``, iteration and indexed access.
    """
    def __init__(self, tbl, parent):
        super(_Columns, self).__init__(parent)
        self._tbl = tbl

    def __getitem__(self, idx):
        """
        Provide indexed access, e.g. 'columns[0]'
        """
        try:
            gridCol = self._gridCol_lst[idx]
        except IndexError:
            msg = "column index [%d] is out of range" % idx
            raise IndexError(msg)
        return _Column(gridCol, self)

    def __iter__(self):
        for gridCol in self._gridCol_lst:
            yield _Column(gridCol, self)

    def __len__(self):
        return len(self._gridCol_lst)

    @property
    def table(self):
        """
        Reference to the |Table| object this column collection belongs to.
        """
        return self._parent.table

    @property
    def _gridCol_lst(self):
        """
        Sequence containing ``<w:gridCol>`` elements for this table, each
        representing a table column.
        """
        tblGrid = self._tbl.tblGrid
        return tblGrid.gridCol_lst


class _Row(Parented):
    """
    Table row
    """
    def __init__(self, tr, parent):
        super(_Row, self).__init__(parent)
        self._tr = tr

    @property
    def cells(self):
        """
        Sequence of |_Cell| instances corresponding to cells in this row.
        """
        return tuple(self.table.row_cells(self._index))

    @property
    def table(self):
        """
        Reference to the |Table| object this row belongs to.
        """
        return self._parent.table

    @property
    def _index(self):
        """
        Index of this row in its table, starting from zero.
        """
        return self._tr.tr_idx


class _Rows(Parented):
    """
    Sequence of |_Row| instances corresponding to the rows in a table.
    Supports ``len()``, iteration and indexed access.
    """
    def __init__(self, tbl, parent):
        super(_Rows, self).__init__(parent)
        self._tbl = tbl

    def __getitem__(self, idx):
        """
        Provide indexed access, (e.g. 'rows[0]')
        """
        try:
            tr = self._tbl.tr_lst[idx]
        except IndexError:
            msg = "row index [%d] out of range" % idx
            raise IndexError(msg)
        return _Row(tr, self)

    def __iter__(self):
        return (_Row(tr, self) for tr in self._tbl.tr_lst)

    def __len__(self):
        return len(self._tbl.tr_lst)

    @property
    def table(self):
        """
        Reference to the |Table| object this row collection belongs to.
        """
        return self._parent.table
