# encoding: utf-8

"""
Test suite for the docx.styles module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.styles.styles import Styles

from ..unitutil.cxml import element


class DescribeStyles(object):

    def it_knows_its_length(self, len_fixture):
        styles, expected_value = len_fixture
        assert len(styles) == expected_value

    # fixture --------------------------------------------------------

    @pytest.fixture(params=[
        ('w:styles',                           0),
        ('w:styles/w:style',                   1),
        ('w:styles/(w:style,w:style)',         2),
        ('w:styles/(w:style,w:style,w:style)', 3),
    ])
    def len_fixture(self, request):
        styles_cxml, expected_value = request.param
        styles = Styles(element(styles_cxml))
        return styles, expected_value
