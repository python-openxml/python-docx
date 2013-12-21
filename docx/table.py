# encoding: utf-8

"""
The |Table| object and related proxy classes.
"""


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
        return _Column(gridCol)

    def add_row(self):
        """
        Return a |_Row| instance, newly added bottom-most to the table.
        """
        tbl = self._tbl
        tr = tbl.add_tr()
        for gridCol in tbl.tblGrid.gridCol_lst:
            tr.add_tc()
        return _Row(tr)


class _Column(object):
    """
    Table column
    """
    def __init__(self, gridCol):
        super(_Column, self).__init__()
        self._gridCol = gridCol


class _Row(object):
    """
    Table row
    """
    def __init__(self, tr):
        super(_Row, self).__init__()
        self._tr = tr
