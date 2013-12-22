# encoding: utf-8

"""
The |Table| object and related proxy classes.
"""

from __future__ import absolute_import, print_function, unicode_literals

from .shared import lazyproperty


class Table(object):
    """
    Proxy class for a WordprocessingML ``<w:tbl>`` element.
    """
    def __init__(self, tbl):
        super(Table, self).__init__()
        self._tbl = tbl

    def add_column(self):
        """
        Return a |_Column| instance, newly added rightmost to the table.
        """
        tblGrid = self._tbl.tblGrid
        gridCol = tblGrid.add_gridCol()
        for tr in self._tbl.tr_lst:
            tr.add_tc()
        return _Column(gridCol, self._tbl)

    def add_row(self):
        """
        Return a |_Row| instance, newly added bottom-most to the table.
        """
        tbl = self._tbl
        tr = tbl.add_tr()
        for gridCol in tbl.tblGrid.gridCol_lst:
            tr.add_tc()
        return _Row(tr)

    def cell(self, row_idx, col_idx):
        """
        Return |_Cell| instance correponding to table cell at *row_idx*,
        *col_idx* intersection, where (0, 0) is the top, left-most cell.
        """
        row = self.rows[row_idx]
        return row.cells[col_idx]

    @lazyproperty
    def columns(self):
        return _ColumnCollection(self._tbl)

    @lazyproperty
    def rows(self):
        return _RowCollection(self._tbl)


class _Cell(object):
    """
    Table cell
    """
    def __init__(self, tc):
        super(_Cell, self).__init__()
        self._tc = tc


class _Column(object):
    """
    Table column
    """
    def __init__(self, gridCol, tbl):
        super(_Column, self).__init__()
        self._gridCol = gridCol
        self._tbl = tbl

    @lazyproperty
    def cells(self):
        """
        |_ColumnCellCollection| instance containing sequence of |_Cell|
        instances corresponding to cells in this column.
        """
        return _ColumnCellCollection(self._tbl, self._gridCol)


class _ColumnCellCollection(object):
    """
    Sequence of |_Cell| instances corresponding to the cells in a table
    column.
    """
    def __init__(self, tbl, gridCol):
        super(_ColumnCellCollection, self).__init__()
        self._tbl = tbl
        self._gridCol = gridCol


class _ColumnCollection(object):
    """
    Sequence of |_Column| instances corresponding to the columns in a table.
    """
    def __init__(self, tbl):
        super(_ColumnCollection, self).__init__()
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
        return _Column(gridCol, self._tbl)

    def __iter__(self):
        return (_Column(gridCol, self._tbl) for gridCol in self._gridCol_lst)

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


class _Row(object):
    """
    Table row
    """
    def __init__(self, tr):
        super(_Row, self).__init__()
        self._tr = tr

    @lazyproperty
    def cells(self):
        """
        Sequence of |_Cell| instances corresponding to the cells in this row.
        """
        return _RowCellCollection(self._tr)


class _RowCellCollection(object):
    """
    Sequence of |_Cell| instances corresponding to the cells in a table row.
    """
    def __init__(self, tr):
        super(_RowCellCollection, self).__init__()
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
        return _Cell(tc)

    def __iter__(self):
        return (_Cell(tc) for tc in self._tr.tc_lst)

    def __len__(self):
        return len(self._tr.tc_lst)


class _RowCollection(object):
    """
    Sequence of |_Row| instances corresponding to the rows in a table.
    """
    def __init__(self, tbl):
        super(_RowCollection, self).__init__()
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
        return _Row(tr)

    def __iter__(self):
        return (_Row(tr) for tr in self._tbl.tr_lst)

    def __len__(self):
        return len(self._tbl.tr_lst)
