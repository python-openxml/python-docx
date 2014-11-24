# encoding: utf-8

"""
Test suite for the docx.oxml.text module.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.oxml.table import CT_Row, CT_Tc

from ..unitutil.cxml import element
from ..unitutil.mock import instance_mock, method_mock, property_mock


class DescribeCT_Tc(object):

    def it_can_merge_to_another_tc(self, merge_fixture):
        tc, other_tc, top_tr_, top_tc_, left, height, width = merge_fixture
        merged_tc = tc.merge(other_tc)
        tc._span_dimensions.assert_called_once_with(other_tc)
        top_tr_.tc_at_grid_col.assert_called_once_with(left)
        top_tc_._grow_to.assert_called_once_with(width, height)
        assert merged_tc is top_tc_

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def merge_fixture(
            self, tr_, _span_dimensions_, _tbl_, _grow_to_, top_tc_):
        tc, other_tc = element('w:tc'), element('w:tc')
        top, left, height, width = 0, 1, 2, 3
        _span_dimensions_.return_value = top, left, height, width
        _tbl_.return_value.tr_lst = [tr_]
        tr_.tc_at_grid_col.return_value = top_tc_
        return tc, other_tc, tr_, top_tc_, left, height, width

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
