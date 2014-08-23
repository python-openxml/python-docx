# encoding: utf-8

"""
The |Table| object and related proxy classes.
"""

from __future__ import absolute_import, print_function, unicode_literals

from .blkcntnr import BlockItemContainer
from .shared import lazyproperty, Parented, write_only_property



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

    def cell(self, row_idx, col_idx, visual_grid=True):
        """
        Return |_Cell| instance correponding to table cell at *row_idx*,
        *col_idx* intersection, where (0, 0) is the top, left-most cell.
        """
        row = self.rows[row_idx]
        row.cells.visual_grid = visual_grid
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


class _Cell(BlockItemContainer):
    """
    Table cell
    """
    def __init__(self, tc, parent):
        super(_Cell, self).__init__(tc, parent)
        self._tc = tc

    def _get_parent(self, instance_type):
        """
        Return a reference to the parent object of type `instance_type`, or
        *None* if no match.
        """
        parent = self._parent
        while parent is not None:
            if isinstance(parent, instance_type):
                return parent
            parent = parent._parent
        return None
        
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
    
    @property
    def column_index(self):
        """
        The column index of the cell. Read-only.
        """
        if self._parent is None: 
            return 0
        elif isinstance(self._parent, _RowCells):
            return self._parent._tr.tc_lst.index(self._tc)
        elif isinstance(self._parent, _ColumnCells):
            return self._parent._col_idx
        else:
            msg = ('Could not get column index: unexpected cell parent '
                    'type (%s).')
            raise ValueError(msg % type(self._parent).__name__)
        raise ValueError('Could not find the column index.')
    
    def merge(self, cell):
        """
        Merge the rectangular area delimited by the current cell and another
        cell passed as the argument.
        """
        def _horizontal_merge(tr, merge_start_idx, merge_stop_idx):
            tr.tc_lst[merge_start_idx].hmerge = 'restart'
            for tc in tr.tc_lst[merge_start_idx+1:merge_stop_idx+1]:
                tc.hmerge = 'continue'

        def _vertical_merge(column, merge_start_idx, merge_stop_idx):
            column.cells[merge_start_idx]._tc.vmerge = 'restart'
            for index in range(merge_start_idx + 1, merge_stop_idx + 1):
                column.cells[index]._tc.vmerge = 'continue'

        def _twoways_merge(table, topleft_coord, bottomright_coord):
            for row_idx in range(topleft_coord[0], bottomright_coord[0] + 1):
                tr = table.rows[row_idx]._tr
                _horizontal_merge(tr, topleft_coord[1], bottomright_coord[1])
            col = table.columns[topleft_coord[1]]
            _vertical_merge(col, topleft_coord[0], bottomright_coord[0])

        # Verify the cells to be merged are from the same table.
        orig_table = self._get_parent(Table)
        dest_table = cell._get_parent(Table)
        if (orig_table is None) or (dest_table is None):
            raise ValueError('Cannot merge cells without a Table parent.')
        if orig_table._tbl is not dest_table._tbl:
            raise ValueError('Cannot merge cells from different tables.')
        table = orig_table
        # Get the cells coordinates and reorganize them.
        orig_row_idx = min(self.row_index, cell.row_index)
        orig_col_idx = min(self.column_index, cell.column_index)
        dest_row_idx = max(self.row_index, cell.row_index)
        dest_col_idx = max(self.column_index, cell.column_index)
        orig_coord = (orig_row_idx, orig_col_idx)
        dest_coord = (dest_row_idx, dest_col_idx)
        # Process the merge.
        if (orig_row_idx == dest_row_idx) and (orig_col_idx != dest_col_idx):
            tr = table.rows[orig_row_idx]._tr
            _horizontal_merge(tr, orig_col_idx, dest_col_idx)
        elif (orig_row_idx != dest_row_idx) and (orig_col_idx == dest_col_idx):
            col = table.columns[orig_col_idx]
            _vertical_merge(col, orig_row_idx, dest_row_idx)
        elif (orig_row_idx != dest_row_idx) and (orig_col_idx != dest_col_idx):
            _twoways_merge(table, orig_coord, dest_coord)
        else: # orig_coord == dest_coord:
            return

    @property
    def paragraphs(self):
        """
        List of paragraphs in the cell. A table cell is required to contain
        at least one block-level element and end with a paragraph. By
        default, a new cell contains a single paragraph. Read-only.
        """
        return super(_Cell, self).paragraphs

    @property
    def row_index(self):
        """
        The row index of the cell. Read-only.
        """
        if self._parent is None:
            return 0
        if isinstance(self._parent, _RowCells):
            parent_row = self._get_parent(_Row)
            parent_rows = self._get_parent(_Rows)
            if parent_row is None or parent_rows is None:
                return 0
            return parent_rows._tbl.tr_lst.index(parent_row._tr)
        elif isinstance(self._parent, _ColumnCells):
            for i, cell in enumerate(self._parent):
                if self._tc is cell._tc: 
                    return i
        else:
            msg = 'Cannot get row index: unexpected cell parent type (%s).'
            raise ValueError(msg % type(self._parent).__name__)
        raise ValueError('Could not find the row index.')

    @property
    def tables(self):
        """
        List of tables in the cell, in the order they appear. Read-only.
        """
        return super(_Cell, self).tables

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
    # The visual grid property defines how the merged cells are accounted in 
    # the rows and columns' length. It also restricts access to certain merged
    # cells to protect against unintended modification.
    visual_grid = True
    
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
        if self.visual_grid:
            if tc.hmerge == 'continue' or tc.vmerge == 'continue': 
                raise ValueError('Merged cell access is restricted.')
        return _Cell(tc, self)

    def __iter__(self):
        for tr in self._tr_lst:
            tc = tr.tc_lst[self._col_idx]
            if self.visual_grid:
                if tc.hmerge == 'continue' or tc.vmerge == 'continue': 
                    continue
            yield _Cell(tc, self)

    def __len__(self):
        if self.visual_grid:
            cell_lst = []
            for cell in self: 
                cell_lst.append(cell)
            return len(cell_lst)
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
    # See the equivalent static property description in _ColumnCells.
    visual_grid = True
    
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
        if self.visual_grid:
            if tc.hmerge == 'continue' or tc.vmerge == 'continue':
                raise ValueError('Merged cell access is restricted.')        
        return _Cell(tc, self)

    def __iter__(self):
        for tc in self._tr.tc_lst:
            if self.visual_grid:
                if tc.hmerge == 'continue' or tc.vmerge == 'continue': 
                    continue
            yield _Cell(tc, self)

    def __len__(self):
        if self.visual_grid:
            cell_lst = []
            for cell in self: 
                cell_lst.append(cell)
            return len(cell_lst)
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
