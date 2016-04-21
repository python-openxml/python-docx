# encoding: utf-8

"""
Test suite for the docx.text.tabstops module, containing the TabStops and
TabStop objects.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from docx.text.tabstops import TabStops

import pytest

from ..unitutil.cxml import element


class DescribeTabStops(object):

    def it_knows_its_length(self, len_fixture):
        tab_stops, expected_value = len_fixture
        assert len(tab_stops) == expected_value

    # fixture --------------------------------------------------------

    @pytest.fixture(params=[
        ('w:pPr',                          0),
        ('w:pPr/w:tabs/w:tab{w:pos=2880}', 1),
    ])
    def len_fixture(self, request):
        tab_stops_cxml, expected_value = request.param
        tab_stops = TabStops(element(tab_stops_cxml))
        return tab_stops, expected_value
