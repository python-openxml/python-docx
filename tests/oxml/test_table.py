# encoding: utf-8

"""
Test suite for the docx.oxml.text module.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.oxml import parse_xml
from docx.oxml.table import CT_Row, CT_Tc

from ..unitutil.cxml import element
from ..unitutil.file import snippet_seq
from ..unitutil.mock import instance_mock, method_mock, property_mock


class DescribeCT_Row(object):

    def it_raises_on_tc_at_grid_col(self, tc_raise_fixture):
        tr, idx = tc_raise_fixture
        with pytest.raises(ValueError):
            tr.tc_at_grid_col(idx)

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[(0, 0, 3), (1, 0, 1)])
    def tc_raise_fixture(self, request):
        snippet_idx, row_idx, col_idx = request.param
        tbl = parse_xml(snippet_seq('tbl-cells')[snippet_idx])
        tr = tbl.tr_lst[row_idx]
        return tr, col_idx


class DescribeCT_Tc(object):

    def it_can_merge_to_another_tc(self, merge_fixture):
        tc, other_tc, top_tr_, top_tc_, left, height, width = merge_fixture
        merged_tc = tc.merge(other_tc)
        tc._span_dimensions.assert_called_once_with(other_tc)
        top_tr_.tc_at_grid_col.assert_called_once_with(left)
        top_tc_._grow_to.assert_called_once_with(width, height)
        assert merged_tc is top_tc_

    def it_knows_its_extents_to_help(self, extents_fixture):
        tc, attr_name, expected_value = extents_fixture
        extent = getattr(tc, attr_name)
        assert extent == expected_value

    def it_raises_on_tr_above(self, tr_above_raise_fixture):
        tc = tr_above_raise_fixture
        with pytest.raises(ValueError):
            tc._tr_above

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        (0, 0, 0, 'top',    0), (2, 0, 1, 'top',    0),
        (2, 1, 1, 'top',    0), (4, 2, 1, 'top',    1),
        (0, 0, 0, 'left',   0), (1, 0, 1, 'left',   2),
        (3, 1, 0, 'left',   0), (3, 1, 1, 'left',   2),
        (0, 0, 0, 'bottom', 1), (1, 0, 0, 'bottom', 1),
        (2, 0, 1, 'bottom', 2), (4, 1, 1, 'bottom', 3),
        (0, 0, 0, 'right',  1), (1, 0, 0, 'right',  2),
        (0, 0, 0, 'right',  1), (4, 2, 1, 'right',  3),
    ])
    def extents_fixture(self, request):
        snippet_idx, row, col, attr_name, expected_value = request.param
        tbl = parse_xml(snippet_seq('tbl-cells')[snippet_idx])
        tc = tbl.tr_lst[row].tc_lst[col]
        return tc, attr_name, expected_value

    @pytest.fixture
    def merge_fixture(
            self, tr_, _span_dimensions_, _tbl_, _grow_to_, top_tc_):
        tc, other_tc = element('w:tc'), element('w:tc')
        top, left, height, width = 0, 1, 2, 3
        _span_dimensions_.return_value = top, left, height, width
        _tbl_.return_value.tr_lst = [tr_]
        tr_.tc_at_grid_col.return_value = top_tc_
        return tc, other_tc, tr_, top_tc_, left, height, width

    @pytest.fixture(params=[(0, 0, 0), (4, 0, 0)])
    def tr_above_raise_fixture(self, request):
        snippet_idx, row_idx, col_idx = request.param
        tbl = parse_xml(snippet_seq('tbl-cells')[snippet_idx])
        tc = tbl.tr_lst[row_idx].tc_lst[col_idx]
        return tc

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _grow_to_(self, request):
        return method_mock(request, CT_Tc, '_grow_to')

    @pytest.fixture
    def _span_dimensions_(self, request):
        return method_mock(request, CT_Tc, '_span_dimensions')

    @pytest.fixture
    def _tbl_(self, request):
        return property_mock(request, CT_Tc, '_tbl')

    @pytest.fixture
    def top_tc_(self, request):
        return instance_mock(request, CT_Tc)

    @pytest.fixture
    def tr_(self, request):
        return instance_mock(request, CT_Row)
