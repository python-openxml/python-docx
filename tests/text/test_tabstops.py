# encoding: utf-8

"""
Test suite for the docx.text.tabstops module, containing the TabStops and
TabStop objects.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from docx.text.tabstops import TabStop, TabStops

import pytest

from ..unitutil.cxml import element
from ..unitutil.mock import call, class_mock, instance_mock


class DescribeTabStops(object):

    def it_knows_its_length(self, len_fixture):
        tab_stops, expected_value = len_fixture
        assert len(tab_stops) == expected_value

    def it_can_iterate_over_its_tab_stops(self, iter_fixture):
        tab_stops, expected_count, tab_stop_, TabStop_, expected_calls = (
            iter_fixture
        )
        count = 0
        for tab_stop in tab_stops:
            assert tab_stop is tab_stop_
            count += 1
        assert count == expected_count
        assert TabStop_.call_args_list == expected_calls

    def it_can_get_a_tab_stop_by_index(self, index_fixture):
        tab_stops, idx, TabStop_, tab, tab_stop_ = index_fixture
        tab_stop = tab_stops[idx]
        TabStop_.assert_called_once_with(tab)
        assert tab_stop is tab_stop_

    def it_raises_on_indexed_access_when_empty(self):
        tab_stops = TabStops(element('w:pPr'))
        with pytest.raises(IndexError):
            tab_stops[0]

    # fixture --------------------------------------------------------

    @pytest.fixture(params=[
        ('w:pPr/w:tabs/w:tab{w:pos=0}',                                 0),
        ('w:pPr/w:tabs/(w:tab{w:pos=1},w:tab{w:pos=2},w:tab{w:pos=3})', 1),
        ('w:pPr/w:tabs/(w:tab{w:pos=4},w:tab{w:pos=5},w:tab{w:pos=6})', 2),
    ])
    def index_fixture(self, request, TabStop_, tab_stop_):
        pPr_cxml, idx = request.param
        pPr = element(pPr_cxml)
        tab = pPr.xpath('./w:tabs/w:tab')[idx]
        tab_stops = TabStops(pPr)
        return tab_stops, idx, TabStop_, tab, tab_stop_

    @pytest.fixture(params=[
        ('w:pPr',                                              0),
        ('w:pPr/w:tabs/w:tab{w:pos=2880}',                     1),
        ('w:pPr/w:tabs/(w:tab{w:pos=2880},w:tab{w:pos=5760})', 2),
    ])
    def iter_fixture(self, request, TabStop_, tab_stop_):
        pPr_cxml, expected_count = request.param
        pPr = element(pPr_cxml)
        tab_elms = pPr.xpath('//w:tab')
        tab_stops = TabStops(pPr)
        expected_calls = [call(tab) for tab in tab_elms]
        return tab_stops, expected_count, tab_stop_, TabStop_, expected_calls

    @pytest.fixture(params=[
        ('w:pPr',                          0),
        ('w:pPr/w:tabs/w:tab{w:pos=2880}', 1),
    ])
    def len_fixture(self, request):
        tab_stops_cxml, expected_value = request.param
        tab_stops = TabStops(element(tab_stops_cxml))
        return tab_stops, expected_value

    # fixture components ---------------------------------------------

    @pytest.fixture
    def TabStop_(self, request, tab_stop_):
        return class_mock(
            request, 'docx.text.tabstops.TabStop', return_value=tab_stop_
        )

    @pytest.fixture
    def tab_stop_(self, request):
        return instance_mock(request, TabStop)
