# pyright: reportPrivateUsage=false

"""Test suite for the docx.oxml.text module."""

from __future__ import annotations

from typing import cast

import pytest

from docx.exceptions import InvalidSpanError
from docx.oxml.parser import parse_xml
from docx.oxml.table import CT_Row, CT_Tbl, CT_Tc
from docx.oxml.text.paragraph import CT_P

from ..unitutil.cxml import element, xml
from ..unitutil.file import snippet_seq
from ..unitutil.mock import FixtureRequest, Mock, call, instance_mock, method_mock, property_mock


class DescribeCT_Row:

    @pytest.mark.parametrize(
        ("tr_cxml", "expected_cxml"),
        [
            ("w:tr", "w:tr/w:trPr"),
            ("w:tr/w:tblPrEx", "w:tr/(w:tblPrEx,w:trPr)"),
            ("w:tr/w:tc", "w:tr/(w:trPr,w:tc)"),
            ("w:tr/(w:sdt,w:del,w:tc)", "w:tr/(w:trPr,w:sdt,w:del,w:tc)"),
        ],
    )
    def it_can_add_a_trPr(self, tr_cxml: str, expected_cxml: str):
        tr = cast(CT_Row, element(tr_cxml))
        tr._add_trPr()
        assert tr.xml == xml(expected_cxml)

    @pytest.mark.parametrize(("snippet_idx", "row_idx", "col_idx"), [(0, 0, 3), (1, 0, 1)])
    def it_raises_on_tc_at_grid_col(self, snippet_idx: int, row_idx: int, col_idx: int):
        tr = cast(CT_Tbl, parse_xml(snippet_seq("tbl-cells")[snippet_idx])).tr_lst[row_idx]
        with pytest.raises(ValueError, match=f"no `tc` element at grid_offset={col_idx}"):
            tr.tc_at_grid_offset(col_idx)


class DescribeCT_Tc:
    """Unit-test suite for `docx.oxml.table.CT_Tc` objects."""

    @pytest.mark.parametrize(
        ("tr_cxml", "tc_idx", "expected_value"),
        [
            ("w:tr/(w:tc/w:p,w:tc/w:p)", 0, 0),
            ("w:tr/(w:tc/w:p,w:tc/w:p)", 1, 1),
            ("w:tr/(w:trPr/w:gridBefore{w:val=2},w:tc/w:p,w:tc/w:p)", 0, 2),
            ("w:tr/(w:trPr/w:gridBefore{w:val=2},w:tc/w:p,w:tc/w:p)", 1, 3),
            ("w:tr/(w:trPr/w:gridBefore{w:val=4},w:tc/w:p,w:tc/w:p,w:tc/w:p,w:tc/w:p)", 2, 6),
        ],
    )
    def it_knows_its_grid_offset(self, tr_cxml: str, tc_idx: int, expected_value: int):
        tr = cast(CT_Row, element(tr_cxml))
        tc = tr.tc_lst[tc_idx]

        assert tc.grid_offset == expected_value

    def it_can_merge_to_another_tc(
        self, tr_: Mock, _span_dimensions_: Mock, _tbl_: Mock, _grow_to_: Mock, top_tc_: Mock
    ):
        top_tr_ = tr_
        tc, other_tc = cast(CT_Tc, element("w:tc")), cast(CT_Tc, element("w:tc"))
        top, left, height, width = 0, 1, 2, 3
        _span_dimensions_.return_value = top, left, height, width
        _tbl_.return_value.tr_lst = [tr_]
        tr_.tc_at_grid_offset.return_value = top_tc_

        merged_tc = tc.merge(other_tc)

        _span_dimensions_.assert_called_once_with(tc, other_tc)
        top_tr_.tc_at_grid_offset.assert_called_once_with(left)
        top_tc_._grow_to.assert_called_once_with(width, height)
        assert merged_tc is top_tc_

    @pytest.mark.parametrize(
        ("snippet_idx", "row", "col", "attr_name", "expected_value"),
        [
            (0, 0, 0, "top", 0),
            (2, 0, 1, "top", 0),
            (2, 1, 1, "top", 0),
            (4, 2, 1, "top", 1),
            (0, 0, 0, "left", 0),
            (1, 0, 1, "left", 2),
            (3, 1, 0, "left", 0),
            (3, 1, 1, "left", 2),
            (0, 0, 0, "bottom", 1),
            (1, 0, 0, "bottom", 1),
            (2, 0, 1, "bottom", 2),
            (4, 1, 1, "bottom", 3),
            (0, 0, 0, "right", 1),
            (1, 0, 0, "right", 2),
            (4, 2, 1, "right", 3),
        ],
    )
    def it_knows_its_extents_to_help(
        self, snippet_idx: int, row: int, col: int, attr_name: str, expected_value: int
    ):
        tbl = self._snippet_tbl(snippet_idx)
        tc = tbl.tr_lst[row].tc_lst[col]

        extent = getattr(tc, attr_name)

        assert extent == expected_value

    @pytest.mark.parametrize(
        ("snippet_idx", "row", "col", "row_2", "col_2", "expected_value"),
        [
            (0, 0, 0, 0, 1, (0, 0, 1, 2)),
            (0, 0, 1, 2, 1, (0, 1, 3, 1)),
            (0, 2, 2, 1, 1, (1, 1, 2, 2)),
            (0, 1, 2, 1, 0, (1, 0, 1, 3)),
            (1, 0, 0, 1, 1, (0, 0, 2, 2)),
            (1, 0, 1, 0, 0, (0, 0, 1, 3)),
            (2, 0, 1, 2, 1, (0, 1, 3, 1)),
            (2, 0, 1, 1, 0, (0, 0, 2, 2)),
            (2, 1, 2, 0, 1, (0, 1, 2, 2)),
            (4, 0, 1, 0, 0, (0, 0, 1, 3)),
        ],
    )
    def it_calculates_the_dimensions_of_a_span_to_help(
        self,
        snippet_idx: int,
        row: int,
        col: int,
        row_2: int,
        col_2: int,
        expected_value: tuple[int, int, int, int],
    ):
        tbl = self._snippet_tbl(snippet_idx)
        tc = tbl.tr_lst[row].tc_lst[col]
        other_tc = tbl.tr_lst[row_2].tc_lst[col_2]

        dimensions = tc._span_dimensions(other_tc)

        assert dimensions == expected_value

    @pytest.mark.parametrize(
        ("snippet_idx", "row", "col", "row_2", "col_2"),
        [
            (1, 0, 0, 1, 0),  # inverted-L horz
            (1, 1, 0, 0, 0),  # same in opposite order
            (2, 0, 2, 0, 1),  # inverted-L vert
            (5, 0, 1, 1, 0),  # tee-shape horz bar
            (5, 1, 0, 2, 1),  # same, opposite side
            (6, 1, 0, 0, 1),  # tee-shape vert bar
            (6, 0, 1, 1, 2),  # same, opposite side
        ],
    )
    def it_raises_on_invalid_span(
        self, snippet_idx: int, row: int, col: int, row_2: int, col_2: int
    ):
        tbl = self._snippet_tbl(snippet_idx)
        tc = tbl.tr_lst[row].tc_lst[col]
        other_tc = tbl.tr_lst[row_2].tc_lst[col_2]

        with pytest.raises(InvalidSpanError):
            tc._span_dimensions(other_tc)

    @pytest.mark.parametrize(
        ("snippet_idx", "row", "col", "width", "height"),
        [
            (0, 0, 0, 2, 1),
            (0, 0, 1, 1, 2),
            (0, 1, 1, 2, 2),
            (1, 0, 0, 2, 2),
            (2, 0, 0, 2, 2),
            (2, 1, 2, 1, 2),
        ],
    )
    def it_can_grow_itself_to_help_merge(
        self, snippet_idx: int, row: int, col: int, width: int, height: int, _span_to_width_: Mock
    ):
        tbl = self._snippet_tbl(snippet_idx)
        tc = tbl.tr_lst[row].tc_lst[col]
        start = 0 if height == 1 else 1
        end = start + height

        tc._grow_to(width, height, None)

        assert (
            _span_to_width_.call_args_list
            == [
                call(width, tc, None),
                call(width, tc, "restart"),
                call(width, tc, "continue"),
                call(width, tc, "continue"),
            ][start:end]
        )

    def it_can_extend_its_horz_span_to_help_merge(
        self, top_tc_: Mock, grid_span_: Mock, _move_content_to_: Mock, _swallow_next_tc_: Mock
    ):
        grid_span_.side_effect = [1, 3, 4]
        grid_width, vMerge = 4, "continue"
        tc = cast(CT_Tc, element("w:tc"))

        tc._span_to_width(grid_width, top_tc_, vMerge)

        _move_content_to_.assert_called_once_with(tc, top_tc_)
        assert _swallow_next_tc_.call_args_list == [
            call(tc, grid_width, top_tc_),
            call(tc, grid_width, top_tc_),
        ]
        assert tc.vMerge == vMerge

    def it_knows_its_inner_content_block_item_elements(self):
        tc = cast(CT_Tc, element("w:tc/(w:p,w:tbl,w:p)"))
        assert [type(e) for e in tc.inner_content_elements] == [CT_P, CT_Tbl, CT_P]

    @pytest.mark.parametrize(
        ("tr_cxml", "tc_idx", "grid_width", "expected_cxml"),
        [
            (
                "w:tr/(w:tc/w:p,w:tc/w:p)",
                0,
                2,
                "w:tr/(w:tc/(w:tcPr/w:gridSpan{w:val=2},w:p))",
            ),
            (
                "w:tr/(w:tc/w:p,w:tc/w:p,w:tc/w:p)",
                1,
                2,
                "w:tr/(w:tc/w:p,w:tc/(w:tcPr/w:gridSpan{w:val=2},w:p))",
            ),
            (
                'w:tr/(w:tc/w:p/w:r/w:t"a",w:tc/w:p/w:r/w:t"b")',
                0,
                2,
                'w:tr/(w:tc/(w:tcPr/w:gridSpan{w:val=2},w:p/w:r/w:t"a",' 'w:p/w:r/w:t"b"))',
            ),
            (
                "w:tr/(w:tc/(w:tcPr/w:gridSpan{w:val=2},w:p),w:tc/w:p)",
                0,
                3,
                "w:tr/(w:tc/(w:tcPr/w:gridSpan{w:val=3},w:p))",
            ),
            (
                "w:tr/(w:tc/w:p,w:tc/(w:tcPr/w:gridSpan{w:val=2},w:p))",
                0,
                3,
                "w:tr/(w:tc/(w:tcPr/w:gridSpan{w:val=3},w:p))",
            ),
        ],
    )
    def it_can_swallow_the_next_tc_help_merge(
        self, tr_cxml: str, tc_idx: int, grid_width: int, expected_cxml: str
    ):
        tr = cast(CT_Row, element(tr_cxml))
        tc = top_tc = tr.tc_lst[tc_idx]

        tc._swallow_next_tc(grid_width, top_tc)

        assert tr.xml == xml(expected_cxml)

    @pytest.mark.parametrize(
        ("tr_cxml", "tc_idx", "grid_width", "expected_cxml"),
        [
            # both cells have a width
            (
                "w:tr/(w:tc/(w:tcPr/w:tcW{w:w=1440,w:type=dxa},w:p),"
                "w:tc/(w:tcPr/w:tcW{w:w=1440,w:type=dxa},w:p))",
                0,
                2,
                "w:tr/(w:tc/(w:tcPr/(w:tcW{w:w=2880,w:type=dxa}," "w:gridSpan{w:val=2}),w:p))",
            ),
            # neither have a width
            (
                "w:tr/(w:tc/w:p,w:tc/w:p)",
                0,
                2,
                "w:tr/(w:tc/(w:tcPr/w:gridSpan{w:val=2},w:p))",
            ),
            # only second one has a width
            (
                "w:tr/(w:tc/w:p," "w:tc/(w:tcPr/w:tcW{w:w=1440,w:type=dxa},w:p))",
                0,
                2,
                "w:tr/(w:tc/(w:tcPr/w:gridSpan{w:val=2},w:p))",
            ),
            # only first one has a width
            (
                "w:tr/(w:tc/(w:tcPr/w:tcW{w:w=1440,w:type=dxa},w:p)," "w:tc/w:p)",
                0,
                2,
                "w:tr/(w:tc/(w:tcPr/(w:tcW{w:w=1440,w:type=dxa}," "w:gridSpan{w:val=2}),w:p))",
            ),
        ],
    )
    def it_adds_cell_widths_on_swallow(
        self, tr_cxml: str, tc_idx: int, grid_width: int, expected_cxml: str
    ):
        tr = cast(CT_Row, element(tr_cxml))
        tc = top_tc = tr.tc_lst[tc_idx]
        tc._swallow_next_tc(grid_width, top_tc)
        assert tr.xml == xml(expected_cxml)

    @pytest.mark.parametrize(
        ("tr_cxml", "tc_idx", "grid_width"),
        [
            ("w:tr/w:tc/w:p", 0, 2),
            ("w:tr/(w:tc/w:p,w:tc/(w:tcPr/w:gridSpan{w:val=2},w:p))", 0, 2),
        ],
    )
    def it_raises_on_invalid_swallow(self, tr_cxml: str, tc_idx: int, grid_width: int):
        tr = cast(CT_Row, element(tr_cxml))
        tc = top_tc = tr.tc_lst[tc_idx]

        with pytest.raises(InvalidSpanError):
            tc._swallow_next_tc(grid_width, top_tc)

    @pytest.mark.parametrize(
        ("tc_cxml", "tc_2_cxml", "expected_tc_cxml", "expected_tc_2_cxml"),
        [
            ("w:tc/w:p", "w:tc/w:p", "w:tc/w:p", "w:tc/w:p"),
            ("w:tc/w:p", "w:tc/w:p/w:r", "w:tc/w:p", "w:tc/w:p/w:r"),
            ("w:tc/w:p/w:r", "w:tc/w:p", "w:tc/w:p", "w:tc/w:p/w:r"),
            ("w:tc/(w:p/w:r,w:sdt)", "w:tc/w:p", "w:tc/w:p", "w:tc/(w:p/w:r,w:sdt)"),
            (
                "w:tc/(w:p/w:r,w:sdt)",
                "w:tc/(w:tbl,w:p)",
                "w:tc/w:p",
                "w:tc/(w:tbl,w:p/w:r,w:sdt)",
            ),
        ],
    )
    def it_can_move_its_content_to_help_merge(
        self, tc_cxml: str, tc_2_cxml: str, expected_tc_cxml: str, expected_tc_2_cxml: str
    ):
        tc, tc_2 = cast(CT_Tc, element(tc_cxml)), cast(CT_Tc, element(tc_2_cxml))

        tc._move_content_to(tc_2)

        assert tc.xml == xml(expected_tc_cxml)
        assert tc_2.xml == xml(expected_tc_2_cxml)

    @pytest.mark.parametrize(("snippet_idx", "row_idx", "col_idx"), [(0, 0, 0), (4, 0, 0)])
    def it_raises_on_tr_above(self, snippet_idx: int, row_idx: int, col_idx: int):
        tbl = cast(CT_Tbl, parse_xml(snippet_seq("tbl-cells")[snippet_idx]))
        tc = tbl.tr_lst[row_idx].tc_lst[col_idx]

        with pytest.raises(ValueError, match="no tr above topmost tr"):
            tc._tr_above

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def grid_span_(self, request: FixtureRequest):
        return property_mock(request, CT_Tc, "grid_span")

    @pytest.fixture
    def _grow_to_(self, request: FixtureRequest):
        return method_mock(request, CT_Tc, "_grow_to")

    @pytest.fixture
    def _move_content_to_(self, request: FixtureRequest):
        return method_mock(request, CT_Tc, "_move_content_to")

    @pytest.fixture
    def _span_dimensions_(self, request: FixtureRequest):
        return method_mock(request, CT_Tc, "_span_dimensions")

    @pytest.fixture
    def _span_to_width_(self, request: FixtureRequest):
        return method_mock(request, CT_Tc, "_span_to_width", autospec=False)

    def _snippet_tbl(self, idx: int) -> CT_Tbl:
        """A <w:tbl> element for snippet at `idx` in 'tbl-cells' snippet file."""
        return cast(CT_Tbl, parse_xml(snippet_seq("tbl-cells")[idx]))

    @pytest.fixture
    def _swallow_next_tc_(self, request: FixtureRequest):
        return method_mock(request, CT_Tc, "_swallow_next_tc")

    @pytest.fixture
    def _tbl_(self, request: FixtureRequest):
        return property_mock(request, CT_Tc, "_tbl")

    @pytest.fixture
    def top_tc_(self, request: FixtureRequest):
        return instance_mock(request, CT_Tc)

    @pytest.fixture
    def tr_(self, request: FixtureRequest):
        return instance_mock(request, CT_Row)
