# encoding: utf-8

"""
Test suite for the docx.table module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.table import (
    _Cell, _Column, _ColumnCells, _Columns, _Row, _RowCells, _Rows, Table
)
from docx.text import Paragraph

from .oxml.unitdata.table import (
    a_gridCol, a_tbl, a_tblGrid, a_tblPr, a_tblStyle, a_tc, a_tcPr, a_tr
)
from .oxml.unitdata.text import a_p, a_t, an_r


class DescribeTable(object):

    def it_provides_access_to_the_table_rows(self, table):
        rows = table.rows
        assert isinstance(rows, _Rows)

    def it_provides_access_to_the_table_columns(self, table):
        columns = table.columns
        assert isinstance(columns, _Columns)

    def it_provides_access_to_a_cell_by_row_and_col_indices(self, table):
        for row_idx in range(2):
            for col_idx in range(2):
                cell = table.cell(row_idx, col_idx)
                assert isinstance(cell, _Cell)
                tr = table._tbl.tr_lst[row_idx]
                tc = tr.tc_lst[col_idx]
                assert tc is cell._tc

    def it_can_add_a_row(self, add_row_fixture):
        table, expected_xml = add_row_fixture
        row = table.add_row()
        assert table._tbl.xml == expected_xml
        assert isinstance(row, _Row)
        assert row._tr is table._tbl.tr_lst[1]

    def it_can_add_a_column(self, add_column_fixture):
        table, expected_xml = add_column_fixture
        column = table.add_column()
        assert table._tbl.xml == expected_xml
        assert isinstance(column, _Column)
        assert column._gridCol is table._tbl.tblGrid.gridCol_lst[1]

    def it_knows_its_table_style(self, table_style_fixture):
        table, style = table_style_fixture
        assert table.style == style

    def it_can_apply_a_table_style_by_name(self, table_style_set_fixture):
        table, style_name, expected_xml = table_style_set_fixture
        table.style = style_name
        assert table._tbl.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def add_column_fixture(self):
        tbl = _tbl_bldr(2, 1).element
        table = Table(tbl)
        expected_xml = _tbl_bldr(2, 2).xml()
        return table, expected_xml

    @pytest.fixture
    def add_row_fixture(self):
        tbl = _tbl_bldr(rows=1, cols=2).element
        table = Table(tbl)
        expected_xml = _tbl_bldr(rows=2, cols=2).xml()
        return table, expected_xml

    @pytest.fixture
    def table(self):
        tbl = _tbl_bldr(rows=2, cols=2).element
        table = Table(tbl)
        return table

    @pytest.fixture
    def table_style_fixture(self):
        style = 'foobar'
        tbl = (
            a_tbl().with_nsdecls().with_child(
                a_tblPr().with_child(
                    a_tblStyle().with_val(style)))
        ).element
        table = Table(tbl)
        return table, style

    @pytest.fixture
    def table_style_set_fixture(self):
        # table ------------------------
        tbl = a_tbl().with_nsdecls().with_child(a_tblPr()).element
        table = Table(tbl)
        # style_name -------------------
        style_name = 'foobar'
        # expected_xml -----------------
        expected_xml = (
            a_tbl().with_nsdecls().with_child(
                a_tblPr().with_child(
                    a_tblStyle().with_val(style_name)))
        ).xml()
        return table, style_name, expected_xml


class Describe_Cell(object):

    def it_provides_access_to_the_paragraphs_it_contains(
            self, cell_with_paragraphs):
        cell = cell_with_paragraphs
        paragraphs = cell.paragraphs
        assert len(paragraphs) == 2
        for p in paragraphs:
            assert isinstance(p, Paragraph)

    def it_can_replace_its_content_with_a_string_of_text(
            self, cell_text_fixture):
        cell, text, expected_xml = cell_text_fixture
        cell.text = text
        assert cell._tc.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def cell_text_fixture(self):
        # cell -------------------------
        tc = (
            a_tc().with_nsdecls().with_child(
                a_tcPr()).with_child(
                a_p()).with_child(
                a_tbl()).with_child(
                a_p())
        ).element
        cell = _Cell(tc)
        # text -------------------------
        text = 'foobar'
        # expected_xml -----------------
        expected_xml = (
            a_tc().with_nsdecls().with_child(
                a_tcPr()).with_child(
                a_p().with_child(
                    an_r().with_child(
                        a_t().with_text(text))))
        ).xml()
        return cell, text, expected_xml

    @pytest.fixture
    def cell_with_paragraphs(self):
        tc = (
            a_tc().with_nsdecls()
                  .with_child(a_p())
                  .with_child(a_p())
                  .element
        )
        return _Cell(tc)


class Describe_Column(object):

    def it_provides_access_to_the_column_cells(self, column):
        cells = column.cells
        assert isinstance(cells, _ColumnCells)

    def it_knows_its_width_in_EMU(self, width_get_fixture):
        column, expected_width = width_get_fixture
        assert column.width == expected_width

    def it_can_change_its_width(self, width_set_fixture):
        column, value, expected_xml = width_set_fixture
        column.width = value
        assert column.width == value
        assert column._gridCol.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        (4242,     2693670),
        (1440,     914400),
        ('2.54cm', 914400),
        ('54mm',   1944000),
        ('12.5pt', 158750),
        (None,     None),
    ])
    def width_get_fixture(self, request):
        w, expected_width = request.param
        gridCol = self.gridCol_bldr(w).element
        column = _Column(gridCol, None)
        return column, expected_width

    @pytest.fixture(params=[
        (4242, None,   None),
        (None, None,   None),
        (4242, 914400, 1440),
        (None, 914400, 1440),
    ])
    def width_set_fixture(self, request):
        initial_w, value, expected_w = request.param
        gridCol = self.gridCol_bldr(initial_w).element
        column = _Column(gridCol, None)
        expected_xml = self.gridCol_bldr(expected_w).xml()
        return column, value, expected_xml

    # fixture components ---------------------------------------------

    @pytest.fixture
    def column(self):
        return _Column(None, None)

    def gridCol_bldr(self, w=None):
        gridCol_bldr = a_gridCol().with_nsdecls()
        if w is not None:
            gridCol_bldr.with_w(w)
        return gridCol_bldr


class Describe_ColumnCells(object):

    def it_knows_how_many_cells_it_contains(self, cells_fixture):
        cells, cell_count = cells_fixture
        assert len(cells) == cell_count

    def it_can_iterate_over_its__Cell_instances(self, cells_fixture):
        cells, cell_count = cells_fixture
        actual_count = 0
        for cell in cells:
            assert isinstance(cell, _Cell)
            actual_count += 1
        assert actual_count == cell_count

    def it_provides_indexed_access_to_cells(self, cells_fixture):
        cells, cell_count = cells_fixture
        for idx in range(-cell_count, cell_count):
            cell = cells[idx]
            assert isinstance(cell, _Cell)

    def it_raises_on_indexed_access_out_of_range(self, cells_fixture):
        cells, cell_count = cells_fixture
        too_low = -1 - cell_count
        too_high = cell_count
        with pytest.raises(IndexError):
            cells[too_low]
        with pytest.raises(IndexError):
            cells[too_high]

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def cells_fixture(self):
        cell_count = 2
        tbl = _tbl_bldr(rows=cell_count, cols=1).element
        gridCol = tbl.tblGrid.gridCol_lst[0]
        cells = _ColumnCells(tbl, gridCol)
        return cells, cell_count


class Describe_Columns(object):

    def it_knows_how_many_columns_it_contains(self, columns_fixture):
        columns, column_count = columns_fixture
        assert len(columns) == column_count

    def it_can_interate_over_its__Column_instances(self, columns_fixture):
        columns, column_count = columns_fixture
        actual_count = 0
        for column in columns:
            assert isinstance(column, _Column)
            actual_count += 1
        assert actual_count == column_count

    def it_provides_indexed_access_to_columns(self, columns_fixture):
        columns, column_count = columns_fixture
        for idx in range(-column_count, column_count):
            column = columns[idx]
            assert isinstance(column, _Column)

    def it_raises_on_indexed_access_out_of_range(self, columns_fixture):
        columns, column_count = columns_fixture
        too_low = -1 - column_count
        too_high = column_count
        with pytest.raises(IndexError):
            columns[too_low]
        with pytest.raises(IndexError):
            columns[too_high]

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def columns_fixture(self):
        column_count = 2
        tbl = _tbl_bldr(rows=2, cols=column_count).element
        columns = _Columns(tbl)
        return columns, column_count


class Describe_Row(object):

    def it_provides_access_to_the_row_cells(self, cells_access_fixture):
        row = cells_access_fixture
        cells = row.cells
        assert isinstance(cells, _RowCells)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def cells_access_fixture(self):
        tr = a_tr().with_nsdecls().element
        row = _Row(tr)
        return row


class Describe_RowCells(object):

    def it_knows_how_many_cells_it_contains(self, cell_count_fixture):
        cells, cell_count = cell_count_fixture
        assert len(cells) == cell_count

    def it_can_iterate_over_its__Cell_instances(self, cell_count_fixture):
        cells, cell_count = cell_count_fixture
        actual_count = 0
        for cell in cells:
            assert isinstance(cell, _Cell)
            actual_count += 1
        assert actual_count == cell_count

    def it_provides_indexed_access_to_cells(self, cell_count_fixture):
        cells, cell_count = cell_count_fixture
        for idx in range(-cell_count, cell_count):
            cell = cells[idx]
            assert isinstance(cell, _Cell)

    def it_raises_on_indexed_access_out_of_range(self, cell_count_fixture):
        cells, cell_count = cell_count_fixture
        too_low = -1 - cell_count
        too_high = cell_count
        with pytest.raises(IndexError):
            cells[too_low]
        with pytest.raises(IndexError):
            cells[too_high]

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def cell_count_fixture(self):
        cell_count = 2
        tr_bldr = a_tr().with_nsdecls()
        for idx in range(cell_count):
            tr_bldr.with_child(a_tc())
        tr = tr_bldr.element
        cells = _RowCells(tr)
        return cells, cell_count


class Describe_Rows(object):

    def it_knows_how_many_rows_it_contains(self, rows_fixture):
        rows, row_count = rows_fixture
        assert len(rows) == row_count

    def it_can_iterate_over_its__Row_instances(self, rows_fixture):
        rows, row_count = rows_fixture
        actual_count = 0
        for row in rows:
            assert isinstance(row, _Row)
            actual_count += 1
        assert actual_count == row_count

    def it_provides_indexed_access_to_rows(self, rows_fixture):
        rows, row_count = rows_fixture
        for idx in range(-row_count, row_count):
            row = rows[idx]
            assert isinstance(row, _Row)

    def it_raises_on_indexed_access_out_of_range(self, rows_fixture):
        rows, row_count = rows_fixture
        with pytest.raises(IndexError):
            too_low = -1 - row_count
            rows[too_low]
        with pytest.raises(IndexError):
            too_high = row_count
            rows[too_high]

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def rows_fixture(self):
        row_count = 2
        tbl = _tbl_bldr(rows=row_count, cols=2).element
        rows = _Rows(tbl)
        return rows, row_count


# fixtures -----------------------------------------------------------

def _tbl_bldr(rows, cols):
    tblGrid_bldr = a_tblGrid()
    for i in range(cols):
        tblGrid_bldr.with_child(a_gridCol())
    tbl_bldr = a_tbl().with_nsdecls().with_child(tblGrid_bldr)
    for i in range(rows):
        tr_bldr = _tr_bldr(cols)
        tbl_bldr.with_child(tr_bldr)
    return tbl_bldr


def _tc_bldr():
    return a_tc().with_child(a_p())


def _tr_bldr(cols):
    tr_bldr = a_tr()
    for i in range(cols):
        tc_bldr = _tc_bldr()
        tr_bldr.with_child(tc_bldr)
    return tr_bldr
