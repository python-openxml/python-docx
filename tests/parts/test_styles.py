# encoding: utf-8

"""
Test suite for the docx.parts.styles module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.oxml.parts.styles import CT_Styles
from docx.parts.styles import StylesPart, _Styles

from ..oxml.unitdata.styles import a_style, a_styles
from ..unitutil.mock import class_mock, instance_mock


class DescribeStylesPart(object):

    def it_provides_access_to_the_styles(self, styles_fixture):
        styles_part, _Styles_, styles_elm_, styles_ = styles_fixture
        styles = styles_part.styles
        _Styles_.assert_called_once_with(styles_elm_)
        assert styles is styles_

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def styles_fixture(self, _Styles_, styles_elm_, styles_):
        styles_part = StylesPart(None, None, styles_elm_, None)
        return styles_part, _Styles_, styles_elm_, styles_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _Styles_(self, request, styles_):
        return class_mock(
            request, 'docx.parts.styles._Styles', return_value=styles_
        )

    @pytest.fixture
    def styles_(self, request):
        return instance_mock(request, _Styles)

    @pytest.fixture
    def styles_elm_(self, request):
        return instance_mock(request, CT_Styles)


class Describe_Styles(object):

    def it_knows_how_many_styles_it_contains(self, len_fixture):
        styles, style_count = len_fixture
        assert len(styles) == style_count

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[0, 1, 2, 3])
    def len_fixture(self, request):
        style_count = request.param
        styles_bldr = a_styles().with_nsdecls()
        for idx in range(style_count):
            styles_bldr.with_child(a_style())
        styles_elm = styles_bldr.element
        styles = _Styles(styles_elm)
        return styles, style_count
