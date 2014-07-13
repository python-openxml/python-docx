# encoding: utf-8

"""
The |Table| object and related proxy classes.
"""

from __future__ import absolute_import, print_function, unicode_literals

from .shared import lazyproperty, Parented, write_only_property
from .text import Paragraph


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
        return _Column(gridCol, self._tbl, self)

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
        row = self.rows[row_idx]
        return row.cells[col_idx]

    @lazyproperty
    def columns(self):
        """
        |_Columns| instance containing the sequence of rows in this table.
        """
        return _Columns(self._tbl, self)

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
    def _tblPr(self):
        return self._tbl.tblPr


class _Cell(Parented):
    """
    Table cell
    """
    def __init__(self, tc, parent):
        super(_Cell, self).__init__(parent)
        self._tc = tc

    @property
    def paragraphs(self):
        """
        List of paragraphs in the cell. A table cell is required to contain
        at least one block-level element. By default this is a single
        paragraph.
        """
        return [Paragraph(p, self) for p in self._tc.p_lst]

    @write_only_property
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
    def __init__(self, gridCol, tbl, parent):
        super(_Column, self).__init__(parent)
        self._gridCol = gridCol
        self._tbl = tbl

    @lazyproperty
    def cells(self):
        """
        Sequence of |_Cell| instances corresponding to cells in this column.
        Supports ``len()``, iteration and indexed access.
        """
        return _ColumnCells(self._tbl, self._gridCol, self)

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


class _ColumnCells(Parented):
    """
    Sequence of |_Cell| instances corresponding to the cells in a table
    column.
    """
    def __init__(self, tbl, gridCol, parent):
        super(_ColumnCells, self).__init__(parent)
        self._tbl = tbl
        self._gridCol = gridCol

    def __getitem__(self, idx):
        """
        Provide indexed access, (e.g. 'cells[0]')
        """
        try:
            tr = self._tr_lst[idx]
        except IndexError:
            msg = "cell index [%d] is out of range" % idx
            raise IndexError(msg)
        tc = tr.tc_lst[self._col_idx]
        return _Cell(tc, self)

    def __iter__(self):
        for tr in self._tr_lst:
            tc = tr.tc_lst[self._col_idx]
            yield _Cell(tc, self)

    def __len__(self):
        return len(self._tr_lst)

    @property
    def _col_idx(self):
        gridCol_lst = self._tbl.tblGrid.gridCol_lst
        return gridCol_lst.index(self._gridCol)

    @property
    def _tr_lst(self):
        return self._tbl.tr_lst


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
        return _Column(gridCol, self._tbl, self)

    def __iter__(self):
        for gridCol in self._gridCol_lst:
            yield _Column(gridCol, self._tbl, self)

    def __len__(self):
        return len(self._gridCol_lst)

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

    @lazyproperty
    def cells(self):
        """
        Sequence of |_Cell| instances corresponding to cells in this row.
        Supports ``len()``, iteration and indexed access.
        """
        return _RowCells(self._tr, self)


class _RowCells(Parented):
    """
    Sequence of |_Cell| instances corresponding to the cells in a table row.
    """
    def __init__(self, tr, parent):
        super(_RowCells, self).__init__(parent)
        self._tr = tr

    def __getitem__(self, idx):
        """
        Provide indexed access, (e.g. 'cells[0]')
        """
        try:
            tc = self._tr.tc_lst[idx]
        except IndexError:
            msg = "cell index [%d] is out of range" % idx
            raise IndexError(msg)
        return _Cell(tc, self)

    def __iter__(self):
        return (_Cell(tc, self) for tc in self._tr.tc_lst)

    def __len__(self):
        return len(self._tr.tc_lst)


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
