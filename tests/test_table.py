# encoding: utf-8

"""
Test suite for the docx.table module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.shared import Inches
from docx.table import (
    _Cell, _Column, _ColumnCells, _Columns, _Row, _RowCells, _Rows, Table
)
from docx.text import Paragraph

from .oxml.unitdata.table import a_gridCol, a_tbl, a_tblGrid, a_tc, a_tr
from .oxml.unitdata.text import a_p
from .unitutil.cxml import element, xml


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

    def it_knows_its_table_style(self, table_style_get_fixture):
        table, style = table_style_get_fixture
        assert table.style == style

    def it_can_apply_a_table_style_by_name(self, table_style_set_fixture):
        table, style_name, expected_xml = table_style_set_fixture
        table.style = style_name
        assert table._tbl.xml == expected_xml

    def it_knows_whether_it_should_autofit(self, autofit_get_fixture):
        table, expected_value = autofit_get_fixture
        assert table.autofit is expected_value

    def it_can_change_its_autofit_setting(self, autofit_set_fixture):
        table, new_value, expected_xml = autofit_set_fixture
        table.autofit = new_value
        assert table._tbl.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def add_column_fixture(self):
        tbl = _tbl_bldr(2, 1).element
        table = Table(tbl, None)
        expected_xml = _tbl_bldr(2, 2).xml()
        return table, expected_xml

    @pytest.fixture
    def add_row_fixture(self):
        tbl = _tbl_bldr(rows=1, cols=2).element
        table = Table(tbl, None)
        expected_xml = _tbl_bldr(rows=2, cols=2).xml()
        return table, expected_xml

    @pytest.fixture(params=[
        ('w:tbl/w:tblPr',                             True),
        ('w:tbl/w:tblPr/w:tblLayout',                 True),
        ('w:tbl/w:tblPr/w:tblLayout{w:type=autofit}', True),
        ('w:tbl/w:tblPr/w:tblLayout{w:type=fixed}',   False),
    ])
    def autofit_get_fixture(self, request):
        tbl_cxml, expected_autofit = request.param
        table = Table(element(tbl_cxml), None)
        return table, expected_autofit

    @pytest.fixture(params=[
        ('w:tbl/w:tblPr', True,
         'w:tbl/w:tblPr/w:tblLayout{w:type=autofit}'),
        ('w:tbl/w:tblPr', False,
         'w:tbl/w:tblPr/w:tblLayout{w:type=fixed}'),
        ('w:tbl/w:tblPr', None,
         'w:tbl/w:tblPr/w:tblLayout{w:type=fixed}'),
        ('w:tbl/w:tblPr/w:tblLayout{w:type=fixed}', True,
         'w:tbl/w:tblPr/w:tblLayout{w:type=autofit}'),
        ('w:tbl/w:tblPr/w:tblLayout{w:type=autofit}', False,
         'w:tbl/w:tblPr/w:tblLayout{w:type=fixed}'),
    ])
    def autofit_set_fixture(self, request):
        tbl_cxml, new_value, expected_tbl_cxml = request.param
        table = Table(element(tbl_cxml), None)
        expected_xml = xml(expected_tbl_cxml)
        return table, new_value, expected_xml

    @pytest.fixture(params=[
        ('w:tbl/w:tblPr', None),
        ('w:tbl/w:tblPr/w:tblStyle{w:val=foobar}', 'foobar'),
    ])
    def table_style_get_fixture(self, request):
        tbl_cxml, expected_style = request.param
        table = Table(element(tbl_cxml), None)
        return table, expected_style

    @pytest.fixture(params=[
        ('w:tbl/w:tblPr', 'foobar',
         'w:tbl/w:tblPr/w:tblStyle{w:val=foobar}'),
        ('w:tbl/w:tblPr/w:tblStyle{w:val=foobar}', 'barfoo',
         'w:tbl/w:tblPr/w:tblStyle{w:val=barfoo}'),
        ('w:tbl/w:tblPr/w:tblStyle{w:val=foobar}', None,
         'w:tbl/w:tblPr'),
        ('w:tbl/w:tblPr', None,
         'w:tbl/w:tblPr'),
    ])
    def table_style_set_fixture(self, request):
        tbl_cxml, new_style, expected_cxml = request.param
        table = Table(element(tbl_cxml), None)
        expected_xml = xml(expected_cxml)
        return table, new_style, expected_xml

    # fixture components ---------------------------------------------

    @pytest.fixture
    def table(self):
        tbl = _tbl_bldr(rows=2, cols=2).element
        table = Table(tbl, None)
        return table


class Describe_Cell(object):

    def it_can_add_a_paragraph(self, add_paragraph_fixture):
        cell, expected_xml = add_paragraph_fixture
        p = cell.add_paragraph()
        assert cell._tc.xml == expected_xml
        assert isinstance(p, Paragraph)

    def it_can_add_a_table(self, add_table_fixture):
        cell, expected_xml = add_table_fixture
        table = cell.add_table(rows=0, cols=0)
        assert cell._tc.xml == expected_xml
        assert isinstance(table, Table)

    def it_provides_access_to_the_paragraphs_it_contains(
            self, paragraphs_fixture):
        cell = paragraphs_fixture
        paragraphs = cell.paragraphs
        assert len(paragraphs) == 2
        count = 0
        for idx, paragraph in enumerate(paragraphs):
            assert isinstance(paragraph, Paragraph)
            assert paragraph is paragraphs[idx]
            count += 1
        assert count == 2

    def it_provides_access_to_the_tables_it_contains(self, tables_fixture):
        # test len(), iterable, and indexed access
        cell, expected_count = tables_fixture
        tables = cell.tables
        assert len(tables) == expected_count
        count = 0
        for idx, table in enumerate(tables):
            assert isinstance(table, Table)
            assert tables[idx] is table
            count += 1
        assert count == expected_count

    def it_can_replace_its_content_with_a_string_of_text(
            self, text_set_fixture):
        cell, text, expected_xml = text_set_fixture
        cell.text = text
        assert cell._tc.xml == expected_xml

    def it_knows_its_width_in_EMU(self, width_get_fixture):
        cell, expected_width = width_get_fixture
        assert cell.width == expected_width

    def it_can_change_its_width(self, width_set_fixture):
        cell, value, expected_xml = width_set_fixture
        cell.width = value
        assert cell.width == value
        assert cell._tc.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('w:tc',       'w:tc/w:p'),
        ('w:tc/w:p',   'w:tc/(w:p, w:p)'),
        ('w:tc/w:tbl', 'w:tc/(w:tbl, w:p)'),
    ])
    def add_paragraph_fixture(self, request):
        tc_cxml, after_tc_cxml = request.param
        cell = _Cell(element(tc_cxml), None)
        expected_xml = xml(after_tc_cxml)
        return cell, expected_xml

    @pytest.fixture(params=[
        ('w:tc',     'w:tc/(w:tbl'),
        ('w:tc/w:p', 'w:tc/(w:p, w:tbl'),
    ])
    def add_table_fixture(self, request):
        tc_cxml, after_tc_cxml = request.param
        # the table has some overhead elements, also a blank para after since
        # it's in a cell.
        after_tc_cxml += (
            '/(w:tblPr/w:tblW{w:type=auto,w:w=0},w:tblGrid),w:p)'
        )
        cell = _Cell(element(tc_cxml), None)
        expected_xml = xml(after_tc_cxml)
        return cell, expected_xml

    @pytest.fixture
    def paragraphs_fixture(self):
        return _Cell(element('w:tc/(w:p, w:p)'), None)

    @pytest.fixture(params=[
        ('w:tc',                   0),
        ('w:tc/w:tbl',             1),
        ('w:tc/(w:tbl,w:tbl)',     2),
        ('w:tc/(w:p,w:tbl)',       1),
        ('w:tc/(w:tbl,w:tbl,w:p)', 2),
    ])
    def tables_fixture(self, request):
        cell_cxml, expected_count = request.param
        cell = _Cell(element(cell_cxml), None)
        return cell, expected_count

    @pytest.fixture(params=[
        ('w:tc/w:p', 'foobar',
         'w:tc/w:p/w:r/w:t"foobar"'),
        ('w:tc/w:p', 'fo\tob\rar\n',
         'w:tc/w:p/w:r/(w:t"fo",w:tab,w:t"ob",w:br,w:t"ar",w:br)'),
        ('w:tc/(w:tcPr, w:p, w:tbl, w:p)', 'foobar',
         'w:tc/(w:tcPr, w:p/w:r/w:t"foobar")'),
    ])
    def text_set_fixture(self, request):
        tc_cxml, new_text, expected_cxml = request.param
        cell = _Cell(element(tc_cxml), None)
        expected_xml = xml(expected_cxml)
        return cell, new_text, expected_xml

    @pytest.fixture(params=[
        ('w:tc',                                   None),
        ('w:tc/w:tcPr',                            None),
        ('w:tc/w:tcPr/w:tcW{w:w=25%,w:type=pct}',  None),
        ('w:tc/w:tcPr/w:tcW{w:w=1440,w:type=dxa}', 914400),
    ])
    def width_get_fixture(self, request):
        tc_cxml, expected_width = request.param
        cell = _Cell(element(tc_cxml), None)
        return cell, expected_width

    @pytest.fixture(params=[
        ('w:tc', Inches(1),
         'w:tc/w:tcPr/w:tcW{w:w=1440,w:type=dxa}'),
        ('w:tc/w:tcPr/w:tcW{w:w=25%,w:type=pct}', Inches(2),
         'w:tc/w:tcPr/w:tcW{w:w=2880,w:type=dxa}'),
    ])
    def width_set_fixture(self, request):
        tc_cxml, new_value, expected_cxml = request.param
        cell = _Cell(element(tc_cxml), None)
        expected_xml = xml(expected_cxml)
        return cell, new_value, expected_xml


class Describe_Column(object):

    def it_provides_access_to_the_column_cells(self):
        column = _Column(None, None, None)
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
        ('w:gridCol{w:w=4242}',   2693670),
        ('w:gridCol{w:w=1440}',    914400),
        ('w:gridCol{w:w=2.54cm}',  914400),
        ('w:gridCol{w:w=54mm}',   1944000),
        ('w:gridCol{w:w=12.5pt}',  158750),
        ('w:gridCol',                None),
    ])
    def width_get_fixture(self, request):
        gridCol_cxml, expected_width = request.param
        column = _Column(element(gridCol_cxml), None, None)
        return column, expected_width

    @pytest.fixture(params=[
        ('w:gridCol',           914400, 'w:gridCol{w:w=1440}'),
        ('w:gridCol{w:w=4242}', 457200, 'w:gridCol{w:w=720}'),
        ('w:gridCol{w:w=4242}',   None, 'w:gridCol'),
        ('w:gridCol',             None, 'w:gridCol'),
    ])
    def width_set_fixture(self, request):
        gridCol_cxml, new_value, expected_cxml = request.param
        column = _Column(element(gridCol_cxml), None, None)
        expected_xml = xml(expected_cxml)
        return column, new_value, expected_xml


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
        cells = _ColumnCells(tbl, gridCol, None)
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
        columns = _Columns(tbl, None)
        return columns, column_count


class Describe_Row(object):

    def it_provides_access_to_the_row_cells(self):
        row = _Row(element('w:tr'), None)
        cells = row.cells
        assert isinstance(cells, _RowCells)


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
        cells = _RowCells(element('w:tr/(w:tc, w:tc)'), None)
        cell_count = 2
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
        rows = _Rows(tbl, None)
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
