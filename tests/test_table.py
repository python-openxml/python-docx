# encoding: utf-8

"""Test suite for the docx.table module"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import (
    WD_ALIGN_VERTICAL,
    WD_ROW_HEIGHT,
    WD_TABLE_ALIGNMENT,
    WD_TABLE_DIRECTION,
)
from docx.oxml import parse_xml
from docx.oxml.table import CT_Tc
from docx.parts.document import DocumentPart
from docx.shared import Inches
from docx.table import _Cell, _Column, _Columns, _Row, _Rows, Table
from docx.text.paragraph import Paragraph

from .oxml.unitdata.table import a_gridCol, a_tbl, a_tblGrid, a_tc, a_tr
from .oxml.unitdata.text import a_p
from .unitutil.cxml import element, xml
from .unitutil.file import snippet_seq
from .unitutil.mock import instance_mock, property_mock


class DescribeTable(object):
    def it_can_add_a_row(self, add_row_fixture):
        table, expected_xml = add_row_fixture
        row = table.add_row()
        assert table._tbl.xml == expected_xml
        assert isinstance(row, _Row)
        assert row._tr is table._tbl.tr_lst[-1]
        assert row._parent is table

    def it_can_add_a_column(self, add_column_fixture):
        table, width, expected_xml = add_column_fixture
        column = table.add_column(width)
        assert table._tbl.xml == expected_xml
        assert isinstance(column, _Column)
        assert column._gridCol is table._tbl.tblGrid.gridCol_lst[-1]
        assert column._parent is table

    def it_provides_access_to_a_cell_by_row_and_col_indices(self, table):
        for row_idx in range(2):
            for col_idx in range(2):
                cell = table.cell(row_idx, col_idx)
                assert isinstance(cell, _Cell)
                tr = table._tbl.tr_lst[row_idx]
                tc = tr.tc_lst[col_idx]
                assert tc is cell._tc

    def it_provides_access_to_the_table_rows(self, table):
        rows = table.rows
        assert isinstance(rows, _Rows)

    def it_provides_access_to_the_table_columns(self, table):
        columns = table.columns
        assert isinstance(columns, _Columns)

    def it_provides_access_to_the_cells_in_a_column(self, col_cells_fixture):
        table, column_idx, expected_cells = col_cells_fixture
        column_cells = table.column_cells(column_idx)
        assert column_cells == expected_cells

    def it_provides_access_to_the_cells_in_a_row(self, row_cells_fixture):
        table, row_idx, expected_cells = row_cells_fixture
        row_cells = table.row_cells(row_idx)
        assert row_cells == expected_cells

    def it_knows_its_alignment_setting(self, alignment_get_fixture):
        table, expected_value = alignment_get_fixture
        assert table.alignment == expected_value

    def it_can_change_its_alignment_setting(self, alignment_set_fixture):
        table, new_value, expected_xml = alignment_set_fixture
        table.alignment = new_value
        assert table._tbl.xml == expected_xml

    def it_knows_whether_it_should_autofit(self, autofit_get_fixture):
        table, expected_value = autofit_get_fixture
        assert table.autofit is expected_value

    def it_can_change_its_autofit_setting(self, autofit_set_fixture):
        table, new_value, expected_xml = autofit_set_fixture
        table.autofit = new_value
        assert table._tbl.xml == expected_xml

    def it_knows_it_is_the_table_its_children_belong_to(self, table_fixture):
        table = table_fixture
        assert table.table is table

    def it_knows_its_direction(self, direction_get_fixture):
        table, expected_value = direction_get_fixture
        assert table.table_direction == expected_value

    def it_can_change_its_direction(self, direction_set_fixture):
        table, new_value, expected_xml = direction_set_fixture
        table.table_direction = new_value
        assert table._element.xml == expected_xml

    def it_knows_its_table_style(self, style_get_fixture):
        table, style_id_, style_ = style_get_fixture
        style = table.style
        table.part.get_style.assert_called_once_with(style_id_, WD_STYLE_TYPE.TABLE)
        assert style is style_

    def it_can_change_its_table_style(self, style_set_fixture):
        table, value, expected_xml = style_set_fixture
        table.style = value
        table.part.get_style_id.assert_called_once_with(value, WD_STYLE_TYPE.TABLE)
        assert table._tbl.xml == expected_xml

    def it_provides_access_to_its_cells_to_help(self, cells_fixture):
        table, cell_count, unique_count, matches = cells_fixture
        cells = table._cells
        assert len(cells) == cell_count
        assert len(set(cells)) == unique_count
        for matching_idxs in matches:
            comparator_idx = matching_idxs[0]
            for idx in matching_idxs[1:]:
                assert cells[idx] is cells[comparator_idx]

    def it_knows_its_column_count_to_help(self, column_count_fixture):
        table, expected_value = column_count_fixture
        column_count = table._column_count
        assert column_count == expected_value

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def add_column_fixture(self):
        snippets = snippet_seq("add-row-col")
        tbl = parse_xml(snippets[0])
        table = Table(tbl, None)
        width = Inches(1.5)
        expected_xml = snippets[2]
        return table, width, expected_xml

    @pytest.fixture
    def add_row_fixture(self):
        snippets = snippet_seq("add-row-col")
        tbl = parse_xml(snippets[0])
        table = Table(tbl, None)
        expected_xml = snippets[1]
        return table, expected_xml

    @pytest.fixture(
        params=[
            ("w:tbl/w:tblPr", None),
            ("w:tbl/w:tblPr/w:jc{w:val=center}", WD_TABLE_ALIGNMENT.CENTER),
            ("w:tbl/w:tblPr/w:jc{w:val=right}", WD_TABLE_ALIGNMENT.RIGHT),
            ("w:tbl/w:tblPr/w:jc{w:val=left}", WD_TABLE_ALIGNMENT.LEFT),
        ]
    )
    def alignment_get_fixture(self, request):
        tbl_cxml, expected_value = request.param
        table = Table(element(tbl_cxml), None)
        return table, expected_value

    @pytest.fixture(
        params=[
            (
                "w:tbl/w:tblPr",
                WD_TABLE_ALIGNMENT.LEFT,
                "w:tbl/w:tblPr/w:jc{w:val=left}",
            ),
            (
                "w:tbl/w:tblPr/w:jc{w:val=left}",
                WD_TABLE_ALIGNMENT.RIGHT,
                "w:tbl/w:tblPr/w:jc{w:val=right}",
            ),
            ("w:tbl/w:tblPr/w:jc{w:val=right}", None, "w:tbl/w:tblPr"),
        ]
    )
    def alignment_set_fixture(self, request):
        tbl_cxml, new_value, expected_tbl_cxml = request.param
        table = Table(element(tbl_cxml), None)
        expected_xml = xml(expected_tbl_cxml)
        return table, new_value, expected_xml

    @pytest.fixture(
        params=[
            ("w:tbl/w:tblPr", True),
            ("w:tbl/w:tblPr/w:tblLayout", True),
            ("w:tbl/w:tblPr/w:tblLayout{w:type=autofit}", True),
            ("w:tbl/w:tblPr/w:tblLayout{w:type=fixed}", False),
        ]
    )
    def autofit_get_fixture(self, request):
        tbl_cxml, expected_autofit = request.param
        table = Table(element(tbl_cxml), None)
        return table, expected_autofit

    @pytest.fixture(
        params=[
            ("w:tbl/w:tblPr", True, "w:tbl/w:tblPr/w:tblLayout{w:type=autofit}"),
            ("w:tbl/w:tblPr", False, "w:tbl/w:tblPr/w:tblLayout{w:type=fixed}"),
            ("w:tbl/w:tblPr", None, "w:tbl/w:tblPr/w:tblLayout{w:type=fixed}"),
            (
                "w:tbl/w:tblPr/w:tblLayout{w:type=fixed}",
                True,
                "w:tbl/w:tblPr/w:tblLayout{w:type=autofit}",
            ),
            (
                "w:tbl/w:tblPr/w:tblLayout{w:type=autofit}",
                False,
                "w:tbl/w:tblPr/w:tblLayout{w:type=fixed}",
            ),
        ]
    )
    def autofit_set_fixture(self, request):
        tbl_cxml, new_value, expected_tbl_cxml = request.param
        table = Table(element(tbl_cxml), None)
        expected_xml = xml(expected_tbl_cxml)
        return table, new_value, expected_xml

    @pytest.fixture(
        params=[
            (0, 9, 9, ()),
            (1, 9, 8, ((0, 1),)),
            (2, 9, 8, ((1, 4),)),
            (3, 9, 6, ((0, 1, 3, 4),)),
            (4, 9, 4, ((0, 1), (3, 6), (4, 5, 7, 8))),
        ]
    )
    def cells_fixture(self, request):
        snippet_idx, cell_count, unique_count, matches = request.param
        tbl_xml = snippet_seq("tbl-cells")[snippet_idx]
        table = Table(parse_xml(tbl_xml), None)
        return table, cell_count, unique_count, matches

    @pytest.fixture
    def col_cells_fixture(self, _cells_, _column_count_):
        table = Table(None, None)
        _cells_.return_value = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        _column_count_.return_value = 3
        column_idx = 1
        expected_cells = [1, 4, 7]
        return table, column_idx, expected_cells

    @pytest.fixture
    def column_count_fixture(self):
        tbl_cxml = "w:tbl/w:tblGrid/(w:gridCol,w:gridCol,w:gridCol)"
        expected_value = 3
        table = Table(element(tbl_cxml), None)
        return table, expected_value

    @pytest.fixture(
        params=[
            ("w:tbl/w:tblPr", None),
            ("w:tbl/w:tblPr/w:bidiVisual", WD_TABLE_DIRECTION.RTL),
            ("w:tbl/w:tblPr/w:bidiVisual{w:val=0}", WD_TABLE_DIRECTION.LTR),
            ("w:tbl/w:tblPr/w:bidiVisual{w:val=on}", WD_TABLE_DIRECTION.RTL),
        ]
    )
    def direction_get_fixture(self, request):
        tbl_cxml, expected_value = request.param
        table = Table(element(tbl_cxml), None)
        return table, expected_value

    @pytest.fixture(
        params=[
            ("w:tbl/w:tblPr", WD_TABLE_DIRECTION.RTL, "w:tbl/w:tblPr/w:bidiVisual"),
            (
                "w:tbl/w:tblPr/w:bidiVisual",
                WD_TABLE_DIRECTION.LTR,
                "w:tbl/w:tblPr/w:bidiVisual{w:val=0}",
            ),
            (
                "w:tbl/w:tblPr/w:bidiVisual{w:val=0}",
                WD_TABLE_DIRECTION.RTL,
                "w:tbl/w:tblPr/w:bidiVisual",
            ),
            ("w:tbl/w:tblPr/w:bidiVisual{w:val=1}", None, "w:tbl/w:tblPr"),
        ]
    )
    def direction_set_fixture(self, request):
        tbl_cxml, new_value, expected_cxml = request.param
        table = Table(element(tbl_cxml), None)
        expected_xml = xml(expected_cxml)
        return table, new_value, expected_xml

    @pytest.fixture
    def row_cells_fixture(self, _cells_, _column_count_):
        table = Table(None, None)
        _cells_.return_value = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        _column_count_.return_value = 3
        row_idx = 1
        expected_cells = [3, 4, 5]
        return table, row_idx, expected_cells

    @pytest.fixture
    def style_get_fixture(self, part_prop_):
        style_id = "Barbaz"
        tbl_cxml = "w:tbl/w:tblPr/w:tblStyle{w:val=%s}" % style_id
        table = Table(element(tbl_cxml), None)
        style_ = part_prop_.return_value.get_style.return_value
        return table, style_id, style_

    @pytest.fixture(
        params=[
            ("w:tbl/w:tblPr", "Tbl A", "TblA", "w:tbl/w:tblPr/w:tblStyle{w:val=TblA}"),
            (
                "w:tbl/w:tblPr/w:tblStyle{w:val=TblA}",
                "Tbl B",
                "TblB",
                "w:tbl/w:tblPr/w:tblStyle{w:val=TblB}",
            ),
            ("w:tbl/w:tblPr/w:tblStyle{w:val=TblB}", None, None, "w:tbl/w:tblPr"),
        ]
    )
    def style_set_fixture(self, request, part_prop_):
        tbl_cxml, value, style_id, expected_cxml = request.param
        table = Table(element(tbl_cxml), None)
        part_prop_.return_value.get_style_id.return_value = style_id
        expected_xml = xml(expected_cxml)
        return table, value, expected_xml

    @pytest.fixture
    def table_fixture(self):
        table = Table(None, None)
        return table

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _cells_(self, request):
        return property_mock(request, Table, "_cells")

    @pytest.fixture
    def _column_count_(self, request):
        return property_mock(request, Table, "_column_count")

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def part_prop_(self, request, document_part_):
        return property_mock(request, Table, "part", return_value=document_part_)

    @pytest.fixture
    def table(self):
        tbl = _tbl_bldr(rows=2, cols=2).element
        table = Table(tbl, None)
        return table


class Describe_Cell(object):
    def it_knows_what_text_it_contains(self, text_get_fixture):
        cell, expected_text = text_get_fixture
        text = cell.text
        assert text == expected_text

    def it_can_replace_its_content_with_a_string_of_text(self, text_set_fixture):
        cell, text, expected_xml = text_set_fixture
        cell.text = text
        assert cell._tc.xml == expected_xml

    def it_knows_its_vertical_alignment(self, alignment_get_fixture):
        cell, expected_value = alignment_get_fixture
        vertical_alignment = cell.vertical_alignment
        assert vertical_alignment == expected_value

    def it_can_change_its_vertical_alignment(self, alignment_set_fixture):
        cell, new_value, expected_xml = alignment_set_fixture
        cell.vertical_alignment = new_value
        assert cell._element.xml == expected_xml

    def it_knows_its_width_in_EMU(self, width_get_fixture):
        cell, expected_width = width_get_fixture
        assert cell.width == expected_width

    def it_can_change_its_width(self, width_set_fixture):
        cell, value, expected_xml = width_set_fixture
        cell.width = value
        assert cell.width == value
        assert cell._tc.xml == expected_xml

    def it_provides_access_to_the_paragraphs_it_contains(self, paragraphs_fixture):
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

    def it_can_add_a_paragraph(self, add_paragraph_fixture):
        cell, expected_xml = add_paragraph_fixture
        p = cell.add_paragraph()
        assert cell._tc.xml == expected_xml
        assert isinstance(p, Paragraph)

    def it_can_add_a_table(self, add_table_fixture):
        cell, expected_xml = add_table_fixture
        table = cell.add_table(rows=2, cols=2)
        assert cell._element.xml == expected_xml
        assert isinstance(table, Table)

    def it_can_merge_itself_with_other_cells(self, merge_fixture):
        cell, other_cell, merged_tc_ = merge_fixture
        merged_cell = cell.merge(other_cell)
        cell._tc.merge.assert_called_once_with(other_cell._tc)
        assert isinstance(merged_cell, _Cell)
        assert merged_cell._tc is merged_tc_
        assert merged_cell._parent is cell._parent

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            ("w:tc", "w:tc/w:p"),
            ("w:tc/w:p", "w:tc/(w:p, w:p)"),
            ("w:tc/w:tbl", "w:tc/(w:tbl, w:p)"),
        ]
    )
    def add_paragraph_fixture(self, request):
        tc_cxml, after_tc_cxml = request.param
        cell = _Cell(element(tc_cxml), None)
        expected_xml = xml(after_tc_cxml)
        return cell, expected_xml

    @pytest.fixture
    def add_table_fixture(self, request):
        cell = _Cell(element("w:tc/w:p"), None)
        expected_xml = snippet_seq("new-tbl")[1]
        return cell, expected_xml

    @pytest.fixture(
        params=[
            ("w:tc", None),
            ("w:tc/w:tcPr", None),
            ("w:tc/w:tcPr/w:vAlign{w:val=bottom}", WD_ALIGN_VERTICAL.BOTTOM),
            ("w:tc/w:tcPr/w:vAlign{w:val=top}", WD_ALIGN_VERTICAL.TOP),
        ]
    )
    def alignment_get_fixture(self, request):
        tc_cxml, expected_value = request.param
        cell = _Cell(element(tc_cxml), None)
        return cell, expected_value

    @pytest.fixture(
        params=[
            ("w:tc", WD_ALIGN_VERTICAL.TOP, "w:tc/w:tcPr/w:vAlign{w:val=top}"),
            (
                "w:tc/w:tcPr",
                WD_ALIGN_VERTICAL.CENTER,
                "w:tc/w:tcPr/w:vAlign{w:val=center}",
            ),
            (
                "w:tc/w:tcPr/w:vAlign{w:val=center}",
                WD_ALIGN_VERTICAL.BOTTOM,
                "w:tc/w:tcPr/w:vAlign{w:val=bottom}",
            ),
            ("w:tc/w:tcPr/w:vAlign{w:val=center}", None, "w:tc/w:tcPr"),
            ("w:tc", None, "w:tc/w:tcPr"),
            ("w:tc/w:tcPr", None, "w:tc/w:tcPr"),
        ]
    )
    def alignment_set_fixture(self, request):
        cxml, new_value, expected_cxml = request.param
        cell = _Cell(element(cxml), None)
        expected_xml = xml(expected_cxml)
        return cell, new_value, expected_xml

    @pytest.fixture
    def merge_fixture(self, tc_, tc_2_, parent_, merged_tc_):
        cell, other_cell = _Cell(tc_, parent_), _Cell(tc_2_, parent_)
        tc_.merge.return_value = merged_tc_
        return cell, other_cell, merged_tc_

    @pytest.fixture
    def paragraphs_fixture(self):
        return _Cell(element("w:tc/(w:p, w:p)"), None)

    @pytest.fixture(
        params=[
            ("w:tc", 0),
            ("w:tc/w:tbl", 1),
            ("w:tc/(w:tbl,w:tbl)", 2),
            ("w:tc/(w:p,w:tbl)", 1),
            ("w:tc/(w:tbl,w:tbl,w:p)", 2),
        ]
    )
    def tables_fixture(self, request):
        cell_cxml, expected_count = request.param
        cell = _Cell(element(cell_cxml), None)
        return cell, expected_count

    @pytest.fixture(
        params=[
            ("w:tc", ""),
            ('w:tc/w:p/w:r/w:t"foobar"', "foobar"),
            ('w:tc/(w:p/w:r/w:t"foo",w:p/w:r/w:t"bar")', "foo\nbar"),
            ('w:tc/(w:tcPr,w:p/w:r/w:t"foobar")', "foobar"),
            ('w:tc/w:p/w:r/(w:t"fo",w:tab,w:t"ob",w:br,w:t"ar",w:br)', "fo\tob\nar\n"),
        ]
    )
    def text_get_fixture(self, request):
        tc_cxml, expected_text = request.param
        cell = _Cell(element(tc_cxml), None)
        return cell, expected_text

    @pytest.fixture(
        params=[
            ("w:tc/w:p", "foobar", 'w:tc/w:p/w:r/w:t"foobar"'),
            (
                "w:tc/w:p",
                "fo\tob\rar\n",
                'w:tc/w:p/w:r/(w:t"fo",w:tab,w:t"ob",w:br,w:t"ar",w:br)',
            ),
            (
                "w:tc/(w:tcPr, w:p, w:tbl, w:p)",
                "foobar",
                'w:tc/(w:tcPr, w:p/w:r/w:t"foobar")',
            ),
        ]
    )
    def text_set_fixture(self, request):
        tc_cxml, new_text, expected_cxml = request.param
        cell = _Cell(element(tc_cxml), None)
        expected_xml = xml(expected_cxml)
        return cell, new_text, expected_xml

    @pytest.fixture(
        params=[
            ("w:tc", None),
            ("w:tc/w:tcPr", None),
            ("w:tc/w:tcPr/w:tcW{w:w=25%,w:type=pct}", None),
            ("w:tc/w:tcPr/w:tcW{w:w=1440,w:type=dxa}", 914400),
        ]
    )
    def width_get_fixture(self, request):
        tc_cxml, expected_width = request.param
        cell = _Cell(element(tc_cxml), None)
        return cell, expected_width

    @pytest.fixture(
        params=[
            ("w:tc", Inches(1), "w:tc/w:tcPr/w:tcW{w:w=1440,w:type=dxa}"),
            (
                "w:tc/w:tcPr/w:tcW{w:w=25%,w:type=pct}",
                Inches(2),
                "w:tc/w:tcPr/w:tcW{w:w=2880,w:type=dxa}",
            ),
        ]
    )
    def width_set_fixture(self, request):
        tc_cxml, new_value, expected_cxml = request.param
        cell = _Cell(element(tc_cxml), None)
        expected_xml = xml(expected_cxml)
        return cell, new_value, expected_xml

    # fixture components ---------------------------------------------

    @pytest.fixture
    def merged_tc_(self, request):
        return instance_mock(request, CT_Tc)

    @pytest.fixture
    def parent_(self, request):
        return instance_mock(request, Table)

    @pytest.fixture
    def tc_(self, request):
        return instance_mock(request, CT_Tc)

    @pytest.fixture
    def tc_2_(self, request):
        return instance_mock(request, CT_Tc)


class Describe_Column(object):
    def it_provides_access_to_its_cells(self, cells_fixture):
        column, column_idx, expected_cells = cells_fixture
        cells = column.cells
        column.table.column_cells.assert_called_once_with(column_idx)
        assert cells == expected_cells

    def it_provides_access_to_the_table_it_belongs_to(self, table_fixture):
        column, table_ = table_fixture
        assert column.table is table_

    def it_knows_its_width_in_EMU(self, width_get_fixture):
        column, expected_width = width_get_fixture
        assert column.width == expected_width

    def it_can_change_its_width(self, width_set_fixture):
        column, value, expected_xml = width_set_fixture
        column.width = value
        assert column.width == value
        assert column._gridCol.xml == expected_xml

    def it_knows_its_index_in_table_to_help(self, index_fixture):
        column, expected_idx = index_fixture
        assert column._index == expected_idx

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def cells_fixture(self, _index_, table_prop_, table_):
        column = _Column(None, None)
        _index_.return_value = column_idx = 4
        expected_cells = (3, 2, 1)
        table_.column_cells.return_value = list(expected_cells)
        return column, column_idx, expected_cells

    @pytest.fixture
    def index_fixture(self):
        tbl = element("w:tbl/w:tblGrid/(w:gridCol,w:gridCol,w:gridCol)")
        gridCol, expected_idx = tbl.tblGrid[1], 1
        column = _Column(gridCol, None)
        return column, expected_idx

    @pytest.fixture
    def table_fixture(self, parent_, table_):
        column = _Column(None, parent_)
        parent_.table = table_
        return column, table_

    @pytest.fixture(
        params=[
            ("w:gridCol{w:w=4242}", 2693670),
            ("w:gridCol{w:w=1440}", 914400),
            ("w:gridCol{w:w=2.54cm}", 914400),
            ("w:gridCol{w:w=54mm}", 1944000),
            ("w:gridCol{w:w=12.5pt}", 158750),
            ("w:gridCol", None),
        ]
    )
    def width_get_fixture(self, request):
        gridCol_cxml, expected_width = request.param
        column = _Column(element(gridCol_cxml), None)
        return column, expected_width

    @pytest.fixture(
        params=[
            ("w:gridCol", 914400, "w:gridCol{w:w=1440}"),
            ("w:gridCol{w:w=4242}", 457200, "w:gridCol{w:w=720}"),
            ("w:gridCol{w:w=4242}", None, "w:gridCol"),
            ("w:gridCol", None, "w:gridCol"),
        ]
    )
    def width_set_fixture(self, request):
        gridCol_cxml, new_value, expected_cxml = request.param
        column = _Column(element(gridCol_cxml), None)
        expected_xml = xml(expected_cxml)
        return column, new_value, expected_xml

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _index_(self, request):
        return property_mock(request, _Column, "_index")

    @pytest.fixture
    def parent_(self, request):
        return instance_mock(request, Table)

    @pytest.fixture
    def table_(self, request):
        return instance_mock(request, Table)

    @pytest.fixture
    def table_prop_(self, request, table_):
        return property_mock(request, _Column, "table", return_value=table_)


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

    def it_provides_access_to_the_table_it_belongs_to(self, table_fixture):
        columns, table_ = table_fixture
        assert columns.table is table_

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def columns_fixture(self):
        column_count = 2
        tbl = _tbl_bldr(rows=2, cols=column_count).element
        columns = _Columns(tbl, None)
        return columns, column_count

    @pytest.fixture
    def table_fixture(self, table_):
        columns = _Columns(None, table_)
        table_.table = table_
        return columns, table_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def table_(self, request):
        return instance_mock(request, Table)


class Describe_Row(object):
    def it_knows_its_height(self, height_get_fixture):
        row, expected_height = height_get_fixture
        assert row.height == expected_height

    def it_can_change_its_height(self, height_set_fixture):
        row, value, expected_xml = height_set_fixture
        row.height = value
        assert row._tr.xml == expected_xml

    def it_knows_its_height_rule(self, height_rule_get_fixture):
        row, expected_rule = height_rule_get_fixture
        assert row.height_rule == expected_rule

    def it_can_change_its_height_rule(self, height_rule_set_fixture):
        row, rule, expected_xml = height_rule_set_fixture
        row.height_rule = rule
        assert row._tr.xml == expected_xml

    def it_provides_access_to_its_cells(self, cells_fixture):
        row, row_idx, expected_cells = cells_fixture
        cells = row.cells
        row.table.row_cells.assert_called_once_with(row_idx)
        assert cells == expected_cells

    def it_provides_access_to_the_table_it_belongs_to(self, table_fixture):
        row, table_ = table_fixture
        assert row.table is table_

    def it_knows_its_index_in_table_to_help(self, idx_fixture):
        row, expected_idx = idx_fixture
        assert row._index == expected_idx

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def cells_fixture(self, _index_, table_prop_, table_):
        row = _Row(None, None)
        _index_.return_value = row_idx = 6
        expected_cells = (1, 2, 3)
        table_.row_cells.return_value = list(expected_cells)
        return row, row_idx, expected_cells

    @pytest.fixture(
        params=[
            ("w:tr", None),
            ("w:tr/w:trPr", None),
            ("w:tr/w:trPr/w:trHeight", None),
            ("w:tr/w:trPr/w:trHeight{w:val=0}", 0),
            ("w:tr/w:trPr/w:trHeight{w:val=1440}", 914400),
        ]
    )
    def height_get_fixture(self, request):
        tr_cxml, expected_height = request.param
        row = _Row(element(tr_cxml), None)
        return row, expected_height

    @pytest.fixture(
        params=[
            ("w:tr", Inches(1), "w:tr/w:trPr/w:trHeight{w:val=1440}"),
            ("w:tr/w:trPr", Inches(1), "w:tr/w:trPr/w:trHeight{w:val=1440}"),
            ("w:tr/w:trPr/w:trHeight", Inches(1), "w:tr/w:trPr/w:trHeight{w:val=1440}"),
            (
                "w:tr/w:trPr/w:trHeight{w:val=1440}",
                Inches(2),
                "w:tr/w:trPr/w:trHeight{w:val=2880}",
            ),
            ("w:tr/w:trPr/w:trHeight{w:val=2880}", None, "w:tr/w:trPr/w:trHeight"),
            ("w:tr", None, "w:tr/w:trPr"),
            ("w:tr/w:trPr", None, "w:tr/w:trPr"),
            ("w:tr/w:trPr/w:trHeight", None, "w:tr/w:trPr/w:trHeight"),
        ]
    )
    def height_set_fixture(self, request):
        tr_cxml, new_value, expected_cxml = request.param
        row = _Row(element(tr_cxml), None)
        expected_xml = xml(expected_cxml)
        return row, new_value, expected_xml

    @pytest.fixture(
        params=[
            ("w:tr", None),
            ("w:tr/w:trPr", None),
            ("w:tr/w:trPr/w:trHeight{w:val=0, w:hRule=auto}", WD_ROW_HEIGHT.AUTO),
            (
                "w:tr/w:trPr/w:trHeight{w:val=1440, w:hRule=atLeast}",
                WD_ROW_HEIGHT.AT_LEAST,
            ),
            (
                "w:tr/w:trPr/w:trHeight{w:val=2880, w:hRule=exact}",
                WD_ROW_HEIGHT.EXACTLY,
            ),
        ]
    )
    def height_rule_get_fixture(self, request):
        tr_cxml, expected_rule = request.param
        row = _Row(element(tr_cxml), None)
        return row, expected_rule

    @pytest.fixture(
        params=[
            ("w:tr", WD_ROW_HEIGHT.AUTO, "w:tr/w:trPr/w:trHeight{w:hRule=auto}"),
            (
                "w:tr/w:trPr",
                WD_ROW_HEIGHT.AT_LEAST,
                "w:tr/w:trPr/w:trHeight{w:hRule=atLeast}",
            ),
            (
                "w:tr/w:trPr/w:trHeight",
                WD_ROW_HEIGHT.EXACTLY,
                "w:tr/w:trPr/w:trHeight{w:hRule=exact}",
            ),
            (
                "w:tr/w:trPr/w:trHeight{w:val=1440, w:hRule=exact}",
                WD_ROW_HEIGHT.AUTO,
                "w:tr/w:trPr/w:trHeight{w:val=1440, w:hRule=auto}",
            ),
            (
                "w:tr/w:trPr/w:trHeight{w:val=1440, w:hRule=auto}",
                None,
                "w:tr/w:trPr/w:trHeight{w:val=1440}",
            ),
            ("w:tr", None, "w:tr/w:trPr"),
            ("w:tr/w:trPr", None, "w:tr/w:trPr"),
            ("w:tr/w:trPr/w:trHeight", None, "w:tr/w:trPr/w:trHeight"),
        ]
    )
    def height_rule_set_fixture(self, request):
        tr_cxml, new_rule, expected_cxml = request.param
        row = _Row(element(tr_cxml), None)
        expected_xml = xml(expected_cxml)
        return row, new_rule, expected_xml

    @pytest.fixture
    def idx_fixture(self):
        tbl = element("w:tbl/(w:tr,w:tr,w:tr)")
        tr, expected_idx = tbl[1], 1
        row = _Row(tr, None)
        return row, expected_idx

    @pytest.fixture
    def table_fixture(self, parent_, table_):
        row = _Row(None, parent_)
        parent_.table = table_
        return row, table_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _index_(self, request):
        return property_mock(request, _Row, "_index")

    @pytest.fixture
    def parent_(self, request):
        return instance_mock(request, Table)

    @pytest.fixture
    def table_(self, request):
        return instance_mock(request, Table)

    @pytest.fixture
    def table_prop_(self, request, table_):
        return property_mock(request, _Row, "table", return_value=table_)


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

    def it_provides_sliced_access_to_rows(self, slice_fixture):
        rows, start, end, expected_count = slice_fixture
        slice_of_rows = rows[start:end]
        assert len(slice_of_rows) == expected_count
        tr_lst = rows._tbl.tr_lst
        for idx, row in enumerate(slice_of_rows):
            assert tr_lst.index(row._tr) == start + idx
            assert isinstance(row, _Row)

    def it_raises_on_indexed_access_out_of_range(self, rows_fixture):
        rows, row_count = rows_fixture
        with pytest.raises(IndexError):
            too_low = -1 - row_count
            rows[too_low]
        with pytest.raises(IndexError):
            too_high = row_count
            rows[too_high]

    def it_provides_access_to_the_table_it_belongs_to(self, table_fixture):
        rows, table_ = table_fixture
        assert rows.table is table_

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def rows_fixture(self):
        row_count = 2
        tbl = _tbl_bldr(rows=row_count, cols=2).element
        rows = _Rows(tbl, None)
        return rows, row_count

    @pytest.fixture(
        params=[
            (3, 1, 3, 2),
            (3, 0, -1, 2),
        ]
    )
    def slice_fixture(self, request):
        row_count, start, end, expected_count = request.param
        tbl = _tbl_bldr(rows=row_count, cols=2).element
        rows = _Rows(tbl, None)
        return rows, start, end, expected_count

    @pytest.fixture
    def table_fixture(self, table_):
        rows = _Rows(None, table_)
        table_.table = table_
        return rows, table_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def table_(self, request):
        return instance_mock(request, Table)


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
