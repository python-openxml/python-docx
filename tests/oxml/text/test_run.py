# encoding: utf-8

"""
Test suite for the docx.oxml.text.run module.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from ...unitutil.cxml import element, xml


class DescribeCT_R(object):

    def it_can_add_a_t_preserving_edge_whitespace(self, add_t_fixture):
        r, text, expected_xml = add_t_fixture
        r.add_t(text)
        assert r.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('w:r', 'foobar',  'w:r/w:t"foobar"'),
        ('w:r', 'foobar ', 'w:r/w:t{xml:space=preserve}"foobar "'),
        ('w:r/(w:rPr/w:rStyle{w:val=emphasis}, w:cr)', 'foobar',
         'w:r/(w:rPr/w:rStyle{w:val=emphasis}, w:cr, w:t"foobar")'),
    ])
    def add_t_fixture(self, request):
        initial_cxml, text, expected_cxml = request.param
        r = element(initial_cxml)
        expected_xml = xml(expected_cxml)
        return r, text, expected_xml
