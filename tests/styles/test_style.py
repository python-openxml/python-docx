# encoding: utf-8

"""
Test suite for the docx.styles.style module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.enum.style import WD_STYLE_TYPE
from docx.styles.style import (
    BaseStyle, _CharacterStyle, _ParagraphStyle, _NumberingStyle,
    StyleFactory, _TableStyle
)
from docx.text.run import Font

from ..unitutil.cxml import element, xml
from ..unitutil.mock import call, class_mock, function_mock, instance_mock


class DescribeStyleFactory(object):

    def it_constructs_the_right_type_of_style(self, factory_fixture):
        style_elm, StyleCls_, style_ = factory_fixture
        style = StyleFactory(style_elm)
        StyleCls_.assert_called_once_with(style_elm)
        assert style is style_

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=['paragraph', 'character', 'table', 'numbering'])
    def factory_fixture(
            self, request, paragraph_style_, _ParagraphStyle_,
            character_style_, _CharacterStyle_, table_style_, _TableStyle_,
            numbering_style_, _NumberingStyle_):
        type_attr_val = request.param
        StyleCls_, style_mock = {
            'paragraph': (_ParagraphStyle_, paragraph_style_),
            'character': (_CharacterStyle_, character_style_),
            'table':     (_TableStyle_,     table_style_),
            'numbering': (_NumberingStyle_, numbering_style_),
        }[request.param]
        style_cxml = 'w:style{w:type=%s}' % type_attr_val
        style_elm = element(style_cxml)
        return style_elm, StyleCls_, style_mock

    # fixture components -----------------------------------

    @pytest.fixture
    def _ParagraphStyle_(self, request, paragraph_style_):
        return class_mock(
            request, 'docx.styles.style._ParagraphStyle',
            return_value=paragraph_style_
        )

    @pytest.fixture
    def paragraph_style_(self, request):
        return instance_mock(request, _ParagraphStyle)

    @pytest.fixture
    def _CharacterStyle_(self, request, character_style_):
        return class_mock(
            request, 'docx.styles.style._CharacterStyle',
            return_value=character_style_
        )

    @pytest.fixture
    def character_style_(self, request):
        return instance_mock(request, _CharacterStyle)

    @pytest.fixture
    def _TableStyle_(self, request, table_style_):
        return class_mock(
            request, 'docx.styles.style._TableStyle',
            return_value=table_style_
        )

    @pytest.fixture
    def table_style_(self, request):
        return instance_mock(request, _TableStyle)

    @pytest.fixture
    def _NumberingStyle_(self, request, numbering_style_):
        return class_mock(
            request, 'docx.styles.style._NumberingStyle',
            return_value=numbering_style_
        )

    @pytest.fixture
    def numbering_style_(self, request):
        return instance_mock(request, _NumberingStyle)


class DescribeBaseStyle(object):

    def it_knows_its_style_id(self, id_get_fixture):
        style, expected_value = id_get_fixture
        assert style.style_id == expected_value

    def it_can_change_its_style_id(self, id_set_fixture):
        style, new_value, expected_xml = id_set_fixture
        style.style_id = new_value
        assert style._element.xml == expected_xml

    def it_knows_its_type(self, type_get_fixture):
        style, expected_value = type_get_fixture
        assert style.type == expected_value

    def it_knows_its_name(self, name_get_fixture):
        style, expected_value = name_get_fixture
        assert style.name == expected_value

    def it_can_change_its_name(self, name_set_fixture):
        style, new_value, expected_xml = name_set_fixture
        style.name = new_value
        assert style._element.xml == expected_xml

    def it_knows_whether_its_a_builtin_style(self, builtin_get_fixture):
        style, expected_value = builtin_get_fixture
        assert style.builtin is expected_value

    def it_can_delete_itself_from_the_document(self, delete_fixture):
        style, styles, expected_xml = delete_fixture
        style.delete()
        assert styles.xml == expected_xml
        assert style._element is None

    # fixture --------------------------------------------------------

    @pytest.fixture(params=[
        ('w:style',                  True),
        ('w:style{w:customStyle=0}', True),
        ('w:style{w:customStyle=1}', False),
    ])
    def builtin_get_fixture(self, request):
        style_cxml, expected_value = request.param
        style = BaseStyle(element(style_cxml))
        return style, expected_value

    @pytest.fixture
    def delete_fixture(self):
        styles = element('w:styles/w:style')
        style = BaseStyle(styles[0])
        expected_xml = xml('w:styles')
        return style, styles, expected_xml

    @pytest.fixture(params=[
        ('w:style',                   None),
        ('w:style{w:styleId=Foobar}', 'Foobar'),
    ])
    def id_get_fixture(self, request):
        style_cxml, expected_value = request.param
        style = BaseStyle(element(style_cxml))
        return style, expected_value

    @pytest.fixture(params=[
        ('w:style',                'Foo', 'w:style{w:styleId=Foo}'),
        ('w:style{w:styleId=Foo}', 'Bar', 'w:style{w:styleId=Bar}'),
        ('w:style{w:styleId=Bar}', None,  'w:style'),
        ('w:style',                None,  'w:style'),
    ])
    def id_set_fixture(self, request):
        style_cxml, new_value, expected_style_cxml = request.param
        style = BaseStyle(element(style_cxml))
        expected_xml = xml(expected_style_cxml)
        return style, new_value, expected_xml

    @pytest.fixture(params=[
        ('w:style{w:type=table}',                         None),
        ('w:style{w:type=table}/w:name{w:val=Boofar}',    'Boofar'),
        ('w:style{w:type=table}/w:name{w:val=heading 1}', 'Heading 1'),
    ])
    def name_get_fixture(self, request):
        style_cxml, expected_value = request.param
        style = BaseStyle(element(style_cxml))
        return style, expected_value

    @pytest.fixture(params=[
        ('w:style',                   'Foo', 'w:style/w:name{w:val=Foo}'),
        ('w:style/w:name{w:val=Foo}', 'Bar', 'w:style/w:name{w:val=Bar}'),
        ('w:style/w:name{w:val=Bar}', None,  'w:style'),
    ])
    def name_set_fixture(self, request):
        style_cxml, new_value, expected_style_cxml = request.param
        style = BaseStyle(element(style_cxml))
        expected_xml = xml(expected_style_cxml)
        return style, new_value, expected_xml

    @pytest.fixture(params=[
        ('w:style',                   WD_STYLE_TYPE.PARAGRAPH),
        ('w:style{w:type=paragraph}', WD_STYLE_TYPE.PARAGRAPH),
        ('w:style{w:type=character}', WD_STYLE_TYPE.CHARACTER),
        ('w:style{w:type=numbering}', WD_STYLE_TYPE.LIST),
    ])
    def type_get_fixture(self, request):
        style_cxml, expected_value = request.param
        style = BaseStyle(element(style_cxml))
        return style, expected_value


class Describe_CharacterStyle(object):

    def it_knows_which_style_it_is_based_on(self, base_get_fixture):
        style, StyleFactory_, StyleFactory_calls, base_style_ = (
            base_get_fixture
        )
        base_style = style.base_style

        assert StyleFactory_.call_args_list == StyleFactory_calls
        assert base_style == base_style_

    def it_can_change_its_base_style(self, base_set_fixture):
        style, value, expected_xml = base_set_fixture
        style.base_style = value
        assert style._element.xml == expected_xml

    def it_provides_access_to_its_font(self, font_fixture):
        style, Font_, font_ = font_fixture
        font = style.font
        Font_.assert_called_once_with(style._element)
        assert font is font_

    # fixture --------------------------------------------------------

    @pytest.fixture(params=[
        ('w:styles/(w:style{w:styleId=Foo},w:style/w:basedOn{w:val=Foo})',
         1, 0),
        ('w:styles/(w:style{w:styleId=Foo},w:style/w:basedOn{w:val=Bar})',
         1, -1),
        ('w:styles/w:style',
         0, -1),
    ])
    def base_get_fixture(self, request, StyleFactory_):
        styles_cxml, style_idx, base_style_idx = request.param
        styles = element(styles_cxml)
        style = _CharacterStyle(styles[style_idx])
        if base_style_idx >= 0:
            base_style = styles[base_style_idx]
            StyleFactory_calls = [call(base_style)]
            expected_value = StyleFactory_.return_value
        else:
            StyleFactory_calls = []
            expected_value = None
        return style, StyleFactory_, StyleFactory_calls, expected_value

    @pytest.fixture(params=[
        ('w:style',                       'Foo',
         'w:style/w:basedOn{w:val=Foo}'),
        ('w:style/w:basedOn{w:val=Foo}',  'Bar',
         'w:style/w:basedOn{w:val=Bar}'),
        ('w:style/w:basedOn{w:val=Bar}',  None,
         'w:style'),
    ])
    def base_set_fixture(self, request, style_):
        style_cxml, base_style_id, expected_style_cxml = request.param
        style = _CharacterStyle(element(style_cxml))
        style_.style_id = base_style_id
        base_style = style_ if base_style_id is not None else None
        expected_xml = xml(expected_style_cxml)
        return style, base_style, expected_xml

    @pytest.fixture
    def font_fixture(self, Font_, font_):
        style = _CharacterStyle(element('w:style'))
        return style, Font_, font_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def Font_(self, request, font_):
        return class_mock(
            request, 'docx.styles.style.Font', return_value=font_
        )

    @pytest.fixture
    def font_(self, request):
        return instance_mock(request, Font)

    @pytest.fixture
    def style_(self, request):
        return instance_mock(request, BaseStyle)

    @pytest.fixture
    def StyleFactory_(self, request):
        return function_mock(request, 'docx.styles.style.StyleFactory')
