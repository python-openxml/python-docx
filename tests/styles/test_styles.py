# encoding: utf-8

"""
Test suite for the docx.styles module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.styles.style import BaseStyle
from docx.styles.styles import Styles

from ..unitutil.cxml import element
from ..unitutil.mock import call, function_mock, instance_mock


class DescribeStyles(object):

    def it_knows_its_length(self, len_fixture):
        styles, expected_value = len_fixture
        assert len(styles) == expected_value

    def it_can_iterate_over_its_styles(self, iter_fixture):
        styles, expected_count, style_, StyleFactory_, expected_calls = (
            iter_fixture
        )
        count = 0
        for style in styles:
            assert style is style_
            count += 1
        assert count == expected_count
        assert StyleFactory_.call_args_list == expected_calls

    # fixture --------------------------------------------------------

    @pytest.fixture(params=[
        ('w:styles',                           0),
        ('w:styles/w:style',                   1),
        ('w:styles/(w:style,w:style)',         2),
        ('w:styles/(w:style,w:style,w:style)', 3),
    ])
    def iter_fixture(self, request, StyleFactory_, style_):
        styles_cxml, expected_count = request.param
        styles_elm = element(styles_cxml)
        styles = Styles(styles_elm)
        expected_calls = [call(style_elm) for style_elm in styles_elm]
        StyleFactory_.return_value = style_
        return styles, expected_count, style_, StyleFactory_, expected_calls

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

    # fixture components ---------------------------------------------

    @pytest.fixture
    def style_(self, request):
        return instance_mock(request, BaseStyle)

    @pytest.fixture
    def StyleFactory_(self, request):
        return function_mock(request, 'docx.styles.styles.StyleFactory')
