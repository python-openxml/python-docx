# encoding: utf-8

"""
Test suite for the docx.styles.styles module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.enum.style import WD_STYLE_TYPE
from docx.styles.style import BaseStyle
from docx.styles.styles import Styles

from ..unitutil.cxml import element
from ..unitutil.mock import call, function_mock, instance_mock, method_mock


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

    def it_can_get_a_style_by_id(self, getitem_id_fixture):
        styles, key, expected_element = getitem_id_fixture
        style = styles[key]
        assert style._element is expected_element

    def it_can_get_a_style_by_name(self, getitem_name_fixture):
        styles, key, expected_element = getitem_name_fixture
        style = styles[key]
        assert style._element is expected_element

    def it_raises_on_style_not_found(self, get_raises_fixture):
        styles, key = get_raises_fixture
        with pytest.raises(KeyError):
            styles[key]

    def it_can_get_the_default_style_for_a_type(self, default_fixture):
        styles, style_type, StyleFactory_ = default_fixture[:3]
        StyleFactory_calls, style_ = default_fixture[3:]

        style = styles.default(style_type)

        assert StyleFactory_.call_args_list == StyleFactory_calls
        assert style is style_

    def it_can_get_a_style_of_type_by_id(self, get_by_id_fixture):
        styles, style_id, style_type = get_by_id_fixture[:3]
        default_calls, _get_by_id_calls, style_ = get_by_id_fixture[3:]

        style = styles.get_by_id(style_id, style_type)

        assert styles.default.call_args_list == default_calls
        assert styles._get_by_id.call_args_list == _get_by_id_calls
        assert style is style_

    def it_gets_a_style_by_id_to_help(self, _get_by_id_fixture):
        styles, style_id, style_type, default_calls = _get_by_id_fixture[:4]
        StyleFactory_, StyleFactory_calls, style_ = _get_by_id_fixture[4:]

        style = styles._get_by_id(style_id, style_type)

        assert styles.default.call_args_list == default_calls
        assert StyleFactory_.call_args_list == StyleFactory_calls
        assert style is style_

    # fixture --------------------------------------------------------

    @pytest.fixture(params=[
        ('w:styles',
         False, WD_STYLE_TYPE.CHARACTER),
        ('w:styles/w:style{w:type=paragraph,w:default=1}',
         True, WD_STYLE_TYPE.PARAGRAPH),
        ('w:styles/(w:style{w:type=table,w:default=1},w:style{w:type=table,w'
         ':default=1})',
         True, WD_STYLE_TYPE.TABLE),
    ])
    def default_fixture(self, request, StyleFactory_, style_):
        styles_cxml, is_defined, style_type = request.param
        styles_elm = element(styles_cxml)
        styles = Styles(styles_elm)
        StyleFactory_calls = [call(styles_elm[-1])] if is_defined else []
        StyleFactory_.return_value = style_
        expected_value = style_ if is_defined else None
        return (
            styles, style_type, StyleFactory_, StyleFactory_calls,
            expected_value
        )

    @pytest.fixture(params=[None, 'Foo'])
    def get_by_id_fixture(self, request, default_, _get_by_id_, style_):
        style_id, style_type = request.param, 1
        styles = Styles(None)
        default_calls = [call(style_type)] if style_id is None else []
        _get_by_id_calls = (
            [] if style_id is None else [call(style_id, style_type)]
        )
        default_.return_value = _get_by_id_.return_value = style_
        return (
            styles, style_id, style_type, default_calls, _get_by_id_calls,
            style_
        )

    @pytest.fixture(params=[
        ('w:styles/w:style{w:type=paragraph,w:styleId=Foo}', 'Foo',
         WD_STYLE_TYPE.PARAGRAPH),
        ('w:styles/w:style{w:type=paragraph,w:styleId=Foo}', 'Bar',
         WD_STYLE_TYPE.PARAGRAPH),
        ('w:styles/w:style{w:type=table,w:styleId=Bar}',     'Bar',
         WD_STYLE_TYPE.PARAGRAPH),
    ])
    def _get_by_id_fixture(self, request, default_, StyleFactory_, style_):
        styles_cxml, style_id, style_type = request.param
        styles_elm = element(styles_cxml)
        style_elm = styles_elm[0]
        styles = Styles(styles_elm)
        default_calls = [] if style_id == 'Foo' else [call(style_type)]
        StyleFactory_calls = [call(style_elm)] if style_id == 'Foo' else []
        default_.return_value = StyleFactory_.return_value = style_
        return (
            styles, style_id, style_type, default_calls, StyleFactory_,
            StyleFactory_calls, style_
        )

    @pytest.fixture(params=[
        ('w:styles/(w:style{%s,w:styleId=Foobar},w:style,w:style)', 0),
        ('w:styles/(w:style,w:style{%s,w:styleId=Foobar},w:style)', 1),
        ('w:styles/(w:style,w:style,w:style{%s,w:styleId=Foobar})', 2),
    ])
    def getitem_id_fixture(self, request):
        styles_cxml_tmpl, style_idx = request.param
        styles_cxml = styles_cxml_tmpl % 'w:type=paragraph'
        styles = Styles(element(styles_cxml))
        expected_element = styles._element[style_idx]
        return styles, 'Foobar', expected_element

    @pytest.fixture(params=[
        ('w:styles/(w:style%s/w:name{w:val=foo},w:style)', 'foo',       0),
        ('w:styles/(w:style,w:style%s/w:name{w:val=foo})', 'foo',       1),
        ('w:styles/w:style%s/w:name{w:val=heading 1}',     'Heading 1', 0),
    ])
    def getitem_name_fixture(self, request):
        styles_cxml_tmpl, key, style_idx = request.param
        styles_cxml = styles_cxml_tmpl % '{w:type=character}'
        styles = Styles(element(styles_cxml))
        expected_element = styles._element[style_idx]
        return styles, key, expected_element

    @pytest.fixture(params=[
        ('w:styles/(w:style,w:style/w:name{w:val=foo},w:style)'),
        ('w:styles/(w:style{w:styleId=foo},w:style,w:style)'),
    ])
    def get_raises_fixture(self, request):
        styles_cxml = request.param
        styles = Styles(element(styles_cxml))
        return styles, 'bar'

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
    def default_(self, request):
        return method_mock(request, Styles, 'default')

    @pytest.fixture
    def _get_by_id_(self, request):
        return method_mock(request, Styles, '_get_by_id')

    @pytest.fixture
    def style_(self, request):
        return instance_mock(request, BaseStyle)

    @pytest.fixture
    def StyleFactory_(self, request):
        return function_mock(request, 'docx.styles.styles.StyleFactory')
