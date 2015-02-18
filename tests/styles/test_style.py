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
from docx.text.font import Font
from docx.text.parfmt import ParagraphFormat

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

    def it_knows_whether_its_hidden(self, hidden_get_fixture):
        style, expected_value = hidden_get_fixture
        assert style.hidden == expected_value

    def it_can_change_whether_its_hidden(self, hidden_set_fixture):
        style, value, expected_xml = hidden_set_fixture
        style.hidden = value
        assert style._element.xml == expected_xml

    def it_knows_its_sort_order(self, priority_get_fixture):
        style, expected_value = priority_get_fixture
        assert style.priority == expected_value

    def it_can_change_its_sort_order(self, priority_set_fixture):
        style, value, expected_xml = priority_set_fixture
        style.priority = value
        assert style._element.xml == expected_xml

    def it_knows_whether_its_unhide_when_used(self, unhide_get_fixture):
        style, expected_value = unhide_get_fixture
        assert style.unhide_when_used == expected_value

    def it_can_change_its_unhide_when_used_value(self, unhide_set_fixture):
        style, value, expected_xml = unhide_set_fixture
        style.unhide_when_used = value
        assert style._element.xml == expected_xml

    def it_knows_its_quick_style_setting(self, quick_get_fixture):
        style, expected_value = quick_get_fixture
        assert style.quick_style == expected_value

    def it_can_change_its_quick_style_setting(self, quick_set_fixture):
        style, new_value, expected_xml = quick_set_fixture
        style.quick_style = new_value
        assert style._element.xml == expected_xml

    def it_knows_whether_its_locked(self, locked_get_fixture):
        style, expected_value = locked_get_fixture
        assert style.locked == expected_value

    def it_can_change_whether_its_locked(self, locked_set_fixture):
        style, value, expected_xml = locked_set_fixture
        style.locked = value
        assert style._element.xml == expected_xml

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
        ('w:style',                       False),
        ('w:style/w:semiHidden',          True),
        ('w:style/w:semiHidden{w:val=0}', False),
        ('w:style/w:semiHidden{w:val=1}', True),
    ])
    def hidden_get_fixture(self, request):
        style_cxml, expected_value = request.param
        style = BaseStyle(element(style_cxml))
        return style, expected_value

    @pytest.fixture(params=[
        ('w:style',                       True,  'w:style/w:semiHidden'),
        ('w:style/w:semiHidden{w:val=0}', True,  'w:style/w:semiHidden'),
        ('w:style/w:semiHidden{w:val=1}', True,  'w:style/w:semiHidden'),
        ('w:style',                       False, 'w:style'),
        ('w:style/w:semiHidden',          False, 'w:style'),
        ('w:style/w:semiHidden{w:val=1}', False, 'w:style'),
    ])
    def hidden_set_fixture(self, request):
        style_cxml, value, expected_cxml = request.param
        style = BaseStyle(element(style_cxml))
        expected_xml = xml(expected_cxml)
        return style, value, expected_xml

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
        ('w:style',                   False),
        ('w:style/w:locked',          True),
        ('w:style/w:locked{w:val=0}', False),
        ('w:style/w:locked{w:val=1}', True),
    ])
    def locked_get_fixture(self, request):
        style_cxml, expected_value = request.param
        style = BaseStyle(element(style_cxml))
        return style, expected_value

    @pytest.fixture(params=[
        ('w:style',                   True,  'w:style/w:locked'),
        ('w:style/w:locked{w:val=0}', True,  'w:style/w:locked'),
        ('w:style/w:locked{w:val=1}', True,  'w:style/w:locked'),
        ('w:style',                   False, 'w:style'),
        ('w:style/w:locked',          False, 'w:style'),
        ('w:style/w:locked{w:val=1}', False, 'w:style'),
    ])
    def locked_set_fixture(self, request):
        style_cxml, value, expected_cxml = request.param
        style = BaseStyle(element(style_cxml))
        expected_xml = xml(expected_cxml)
        return style, value, expected_xml

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
        ('w:style',                        None),
        ('w:style/w:uiPriority{w:val=42}', 42),
    ])
    def priority_get_fixture(self, request):
        style_cxml, expected_value = request.param
        style = BaseStyle(element(style_cxml))
        return style, expected_value

    @pytest.fixture(params=[
        ('w:style',                        42,
         'w:style/w:uiPriority{w:val=42}'),
        ('w:style/w:uiPriority{w:val=42}', 24,
         'w:style/w:uiPriority{w:val=24}'),
        ('w:style/w:uiPriority{w:val=24}', None,
         'w:style'),
    ])
    def priority_set_fixture(self, request):
        style_cxml, value, expected_cxml = request.param
        style = BaseStyle(element(style_cxml))
        expected_xml = xml(expected_cxml)
        return style, value, expected_xml

    @pytest.fixture(params=[
        ('w:style',                     False),
        ('w:style/w:qFormat',           True),
        ('w:style/w:qFormat{w:val=0}',  False),
        ('w:style/w:qFormat{w:val=on}', True),
    ])
    def quick_get_fixture(self, request):
        style_cxml, expected_value = request.param
        style = BaseStyle(element(style_cxml))
        return style, expected_value

    @pytest.fixture(params=[
        ('w:style',                     True,  'w:style/w:qFormat'),
        ('w:style/w:qFormat',           False, 'w:style'),
        ('w:style/w:qFormat',           True,  'w:style/w:qFormat'),
        ('w:style/w:qFormat{w:val=0}',  False, 'w:style'),
        ('w:style/w:qFormat{w:val=on}', True,  'w:style/w:qFormat'),
    ])
    def quick_set_fixture(self, request):
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

    @pytest.fixture(params=[
        ('w:style',                           False),
        ('w:style/w:unhideWhenUsed',          True),
        ('w:style/w:unhideWhenUsed{w:val=0}', False),
        ('w:style/w:unhideWhenUsed{w:val=1}', True),
    ])
    def unhide_get_fixture(self, request):
        style_cxml, expected_value = request.param
        style = BaseStyle(element(style_cxml))
        return style, expected_value

    @pytest.fixture(params=[
        ('w:style',                           True,
         'w:style/w:unhideWhenUsed'),
        ('w:style/w:unhideWhenUsed',          False,
         'w:style'),
        ('w:style/w:unhideWhenUsed{w:val=0}', True,
         'w:style/w:unhideWhenUsed'),
        ('w:style/w:unhideWhenUsed{w:val=1}', True,
         'w:style/w:unhideWhenUsed'),
        ('w:style/w:unhideWhenUsed{w:val=1}', False,
         'w:style'),
        ('w:style',                           False,
         'w:style'),
    ])
    def unhide_set_fixture(self, request):
        style_cxml, value, expected_cxml = request.param
        style = BaseStyle(element(style_cxml))
        expected_xml = xml(expected_cxml)
        return style, value, expected_xml


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


class Describe_ParagraphStyle(object):

    def it_knows_its_next_paragraph_style(self, next_get_fixture):
        style, expected_value = next_get_fixture
        assert style.next_paragraph_style == expected_value

    def it_can_change_its_next_paragraph_style(self, next_set_fixture):
        style, next_style, expected_xml = next_set_fixture
        style.next_paragraph_style = next_style
        assert style.element.xml == expected_xml

    def it_provides_access_to_its_paragraph_format(self, parfmt_fixture):
        style, ParagraphFormat_, paragraph_format_ = parfmt_fixture
        paragraph_format = style.paragraph_format
        ParagraphFormat_.assert_called_once_with(style._element)
        assert paragraph_format is paragraph_format_

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('H1',   'Body'),
        ('H2',   'H2'),
        ('Body', 'Body'),
        ('Foo',  'Foo'),
    ])
    def next_get_fixture(self, request):
        style_name, next_style_name = request.param
        styles = element(
            'w:styles/('
            'w:style{w:type=paragraph,w:styleId=H1}/w:next{w:val=Body},'
            'w:style{w:type=paragraph,w:styleId=H2}/w:next{w:val=Char},'
            'w:style{w:type=paragraph,w:styleId=Body},'
            'w:style{w:type=paragraph,w:styleId=Foo}/w:next{w:val=Bar},'
            'w:style{w:type=character,w:styleId=Char})'
        )
        style_names = ['H1', 'H2', 'Body', 'Foo', 'Char']
        style_elm = styles[style_names.index(style_name)]
        next_style_elm = styles[style_names.index(next_style_name)]
        style = _ParagraphStyle(style_elm)
        if style_name == 'H1':
            next_style = _ParagraphStyle(next_style_elm)
        else:
            next_style = style
        return style, next_style

    @pytest.fixture(params=[
        ('H', 'B',  'w:style{w:type=paragraph,w:styleId=H}/w:next{w:val=B}'),
        ('H', None, 'w:style{w:type=paragraph,w:styleId=H}'),
        ('H', 'H',  'w:style{w:type=paragraph,w:styleId=H}'),
    ])
    def next_set_fixture(self, request):
        style_name, next_style_name, style_cxml = request.param
        styles = element(
            'w:styles/('
            'w:style{w:type=paragraph,w:styleId=H},'
            'w:style{w:type=paragraph,w:styleId=B})'
        )
        style_elms = {'H': styles[0], 'B': styles[1]}
        style = _ParagraphStyle(style_elms[style_name])
        next_style = (
            None if next_style_name is None else
            _ParagraphStyle(style_elms[next_style_name])
        )
        expected_xml = xml(style_cxml)
        return style, next_style, expected_xml

    @pytest.fixture
    def parfmt_fixture(self, ParagraphFormat_, paragraph_format_):
        style = _ParagraphStyle(element('w:style'))
        return style, ParagraphFormat_, paragraph_format_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def ParagraphFormat_(self, request, paragraph_format_):
        return class_mock(
            request, 'docx.styles.style.ParagraphFormat',
            return_value=paragraph_format_
        )

    @pytest.fixture
    def paragraph_format_(self, request):
        return instance_mock(request, ParagraphFormat)
