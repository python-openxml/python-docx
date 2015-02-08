# encoding: utf-8

"""
Test suite for the docx.text module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.text.paragraph import CT_P
from docx.oxml.text.run import CT_R
from docx.parts.document import DocumentPart
from docx.shared import Pt
from docx.text.paragraph import Paragraph, ParagraphFormat
from docx.text.run import Run

import pytest

from ..unitutil.cxml import element, xml
from ..unitutil.mock import (
    call, class_mock, instance_mock, method_mock, property_mock
)


class DescribeParagraph(object):

    def it_knows_its_paragraph_style(self, style_get_fixture):
        paragraph, style_id_, style_ = style_get_fixture
        style = paragraph.style
        paragraph.part.get_style.assert_called_once_with(
            style_id_, WD_STYLE_TYPE.PARAGRAPH
        )
        assert style is style_

    def it_can_change_its_paragraph_style(self, style_set_fixture):
        paragraph, value, expected_xml = style_set_fixture

        paragraph.style = value

        paragraph.part.get_style_id.assert_called_once_with(
            value, WD_STYLE_TYPE.PARAGRAPH
        )
        assert paragraph._p.xml == expected_xml

    def it_knows_the_text_it_contains(self, text_get_fixture):
        paragraph, expected_text = text_get_fixture
        assert paragraph.text == expected_text

    def it_can_replace_the_text_it_contains(self, text_set_fixture):
        paragraph, text, expected_text = text_set_fixture
        paragraph.text = text
        assert paragraph.text == expected_text

    def it_knows_its_alignment_value(self, alignment_get_fixture):
        paragraph, expected_value = alignment_get_fixture
        assert paragraph.alignment == expected_value

    def it_can_change_its_alignment_value(self, alignment_set_fixture):
        paragraph, value, expected_xml = alignment_set_fixture
        paragraph.alignment = value
        assert paragraph._p.xml == expected_xml

    def it_provides_access_to_its_paragraph_format(self, parfmt_fixture):
        paragraph, ParagraphFormat_, paragraph_format_ = parfmt_fixture
        paragraph_format = paragraph.paragraph_format
        ParagraphFormat_.assert_called_once_with(paragraph._element)
        assert paragraph_format is paragraph_format_

    def it_provides_access_to_the_runs_it_contains(self, runs_fixture):
        paragraph, Run_, r_, r_2_, run_, run_2_ = runs_fixture
        runs = paragraph.runs
        assert Run_.mock_calls == [
            call(r_, paragraph), call(r_2_, paragraph)
        ]
        assert runs == [run_, run_2_]

    def it_can_add_a_run_to_itself(self, add_run_fixture):
        paragraph, text, style, style_prop_, expected_xml = add_run_fixture
        run = paragraph.add_run(text, style)
        assert paragraph._p.xml == expected_xml
        assert isinstance(run, Run)
        assert run._r is paragraph._p.r_lst[0]
        if style:
            style_prop_.assert_called_once_with(style)

    def it_can_insert_a_paragraph_before_itself(self, insert_before_fixture):
        paragraph, text, style, paragraph_, add_run_calls = (
            insert_before_fixture
        )
        new_paragraph = paragraph.insert_paragraph_before(text, style)

        paragraph._insert_paragraph_before.assert_called_once_with()
        assert new_paragraph.add_run.call_args_list == add_run_calls
        assert new_paragraph.style == style
        assert new_paragraph is paragraph_

    def it_can_remove_its_content_while_preserving_formatting(
            self, clear_fixture):
        paragraph, expected_xml = clear_fixture
        _paragraph = paragraph.clear()
        assert paragraph._p.xml == expected_xml
        assert _paragraph is paragraph

    def it_inserts_a_paragraph_before_to_help(self, _insert_before_fixture):
        paragraph, body, expected_xml = _insert_before_fixture
        new_paragraph = paragraph._insert_paragraph_before()
        assert isinstance(new_paragraph, Paragraph)
        assert body.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('w:p', None,     None,     'w:p/w:r'),
        ('w:p', 'foobar', None,     'w:p/w:r/w:t"foobar"'),
        ('w:p', None,     'Strong', 'w:p/w:r'),
        ('w:p', 'foobar', 'Strong', 'w:p/w:r/w:t"foobar"'),
    ])
    def add_run_fixture(self, request, run_style_prop_):
        before_cxml, text, style, after_cxml = request.param
        paragraph = Paragraph(element(before_cxml), None)
        expected_xml = xml(after_cxml)
        return paragraph, text, style, run_style_prop_, expected_xml

    @pytest.fixture(params=[
        ('w:p/w:pPr/w:jc{w:val=center}', WD_ALIGN_PARAGRAPH.CENTER),
        ('w:p', None),
    ])
    def alignment_get_fixture(self, request):
        cxml, expected_alignment_value = request.param
        paragraph = Paragraph(element(cxml), None)
        return paragraph, expected_alignment_value

    @pytest.fixture(params=[
        ('w:p', WD_ALIGN_PARAGRAPH.LEFT,
         'w:p/w:pPr/w:jc{w:val=left}'),
        ('w:p/w:pPr/w:jc{w:val=left}', WD_ALIGN_PARAGRAPH.CENTER,
         'w:p/w:pPr/w:jc{w:val=center}'),
        ('w:p/w:pPr/w:jc{w:val=left}', None,
         'w:p/w:pPr'),
        ('w:p', None, 'w:p/w:pPr'),
    ])
    def alignment_set_fixture(self, request):
        initial_cxml, new_alignment_value, expected_cxml = request.param
        paragraph = Paragraph(element(initial_cxml), None)
        expected_xml = xml(expected_cxml)
        return paragraph, new_alignment_value, expected_xml

    @pytest.fixture(params=[
        ('w:p', 'w:p'),
        ('w:p/w:pPr', 'w:p/w:pPr'),
        ('w:p/w:r/w:t"foobar"', 'w:p'),
        ('w:p/(w:pPr, w:r/w:t"foobar")', 'w:p/w:pPr'),
    ])
    def clear_fixture(self, request):
        initial_cxml, expected_cxml = request.param
        paragraph = Paragraph(element(initial_cxml), None)
        expected_xml = xml(expected_cxml)
        return paragraph, expected_xml

    @pytest.fixture(params=[
        (None,  None),
        ('Foo', None),
        (None,  'Bar'),
        ('Foo', 'Bar'),
    ])
    def insert_before_fixture(self, request, _insert_paragraph_before_,
                              add_run_):
        paragraph = Paragraph(None, None)
        paragraph_ = _insert_paragraph_before_.return_value
        text, style = request.param
        add_run_calls = [] if text is None else [call(text)]
        paragraph_.style = None
        return (
            paragraph, text, style, paragraph_, add_run_calls
        )

    @pytest.fixture(params=[
        ('w:body/w:p{id=42}', 'w:body/(w:p,w:p{id=42})')
    ])
    def _insert_before_fixture(self, request):
        body_cxml, expected_cxml = request.param
        body = element(body_cxml)
        paragraph = Paragraph(body[0], None)
        expected_xml = xml(expected_cxml)
        return paragraph, body, expected_xml

    @pytest.fixture
    def parfmt_fixture(self, ParagraphFormat_, paragraph_format_):
        paragraph = Paragraph(element('w:p'), None)
        return paragraph, ParagraphFormat_, paragraph_format_

    @pytest.fixture
    def runs_fixture(self, p_, Run_, r_, r_2_, runs_):
        paragraph = Paragraph(p_, None)
        run_, run_2_ = runs_
        return paragraph, Run_, r_, r_2_, run_, run_2_

    @pytest.fixture
    def style_get_fixture(self, part_prop_):
        style_id = 'Foobar'
        p_cxml = 'w:p/w:pPr/w:pStyle{w:val=%s}' % style_id
        paragraph = Paragraph(element(p_cxml), None)
        style_ = part_prop_.return_value.get_style.return_value
        return paragraph, style_id, style_

    @pytest.fixture(params=[
        ('w:p',                                 'Heading 1', 'Heading1',
         'w:p/w:pPr/w:pStyle{w:val=Heading1}'),
        ('w:p/w:pPr',                           'Heading 1', 'Heading1',
         'w:p/w:pPr/w:pStyle{w:val=Heading1}'),
        ('w:p/w:pPr/w:pStyle{w:val=Heading1}',  'Heading 2', 'Heading2',
         'w:p/w:pPr/w:pStyle{w:val=Heading2}'),
        ('w:p/w:pPr/w:pStyle{w:val=Heading1}',  'Normal',    None,
         'w:p/w:pPr'),
        ('w:p',                                 None,        None,
         'w:p/w:pPr'),
    ])
    def style_set_fixture(self, request, part_prop_):
        p_cxml, value, style_id, expected_cxml = request.param
        paragraph = Paragraph(element(p_cxml), None)
        part_prop_.return_value.get_style_id.return_value = style_id
        expected_xml = xml(expected_cxml)
        return paragraph, value, expected_xml

    @pytest.fixture(params=[
        ('w:p', ''),
        ('w:p/w:r', ''),
        ('w:p/w:r/w:t', ''),
        ('w:p/w:r/w:t"foo"', 'foo'),
        ('w:p/w:r/(w:t"foo", w:t"bar")', 'foobar'),
        ('w:p/w:r/(w:t"fo ", w:t"bar")', 'fo bar'),
        ('w:p/w:r/(w:t"foo", w:tab, w:t"bar")', 'foo\tbar'),
        ('w:p/w:r/(w:t"foo", w:br,  w:t"bar")', 'foo\nbar'),
        ('w:p/w:r/(w:t"foo", w:cr,  w:t"bar")', 'foo\nbar'),
    ])
    def text_get_fixture(self, request):
        p_cxml, expected_text_value = request.param
        paragraph = Paragraph(element(p_cxml), None)
        return paragraph, expected_text_value

    @pytest.fixture
    def text_set_fixture(self):
        paragraph = Paragraph(element('w:p'), None)
        paragraph.add_run('must not appear in result')
        new_text_value = 'foo\tbar\rbaz\n'
        expected_text_value = 'foo\tbar\nbaz\n'
        return paragraph, new_text_value, expected_text_value

    # fixture components ---------------------------------------------

    @pytest.fixture
    def add_run_(self, request):
        return method_mock(request, Paragraph, 'add_run')

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def _insert_paragraph_before_(self, request):
        return method_mock(request, Paragraph, '_insert_paragraph_before')

    @pytest.fixture
    def p_(self, request, r_, r_2_):
        return instance_mock(request, CT_P, r_lst=(r_, r_2_))

    @pytest.fixture
    def ParagraphFormat_(self, request, paragraph_format_):
        return class_mock(
            request, 'docx.text.paragraph.ParagraphFormat',
            return_value=paragraph_format_
        )

    @pytest.fixture
    def paragraph_format_(self, request):
        return instance_mock(request, ParagraphFormat)

    @pytest.fixture
    def part_prop_(self, request, document_part_):
        return property_mock(
            request, Paragraph, 'part', return_value=document_part_
        )

    @pytest.fixture
    def Run_(self, request, runs_):
        run_, run_2_ = runs_
        return class_mock(
            request, 'docx.text.paragraph.Run', side_effect=[run_, run_2_]
        )

    @pytest.fixture
    def r_(self, request):
        return instance_mock(request, CT_R)

    @pytest.fixture
    def r_2_(self, request):
        return instance_mock(request, CT_R)

    @pytest.fixture
    def run_style_prop_(self, request):
        return property_mock(request, Run, 'style')

    @pytest.fixture
    def runs_(self, request):
        run_ = instance_mock(request, Run, name='run_')
        run_2_ = instance_mock(request, Run, name='run_2_')
        return run_, run_2_


class DescribeParagraphFormat(object):

    def it_knows_its_alignment_value(self, alignment_get_fixture):
        paragraph_format, expected_value = alignment_get_fixture
        assert paragraph_format.alignment == expected_value

    def it_can_change_its_alignment_value(self, alignment_set_fixture):
        paragraph_format, value, expected_xml = alignment_set_fixture
        paragraph_format.alignment = value
        assert paragraph_format._element.xml == expected_xml

    def it_knows_its_space_before(self, space_before_get_fixture):
        paragraph_format, expected_value = space_before_get_fixture
        assert paragraph_format.space_before == expected_value

    def it_can_change_its_space_before(self, space_before_set_fixture):
        paragraph_format, value, expected_xml = space_before_set_fixture
        paragraph_format.space_before = value
        assert paragraph_format._element.xml == expected_xml

    def it_knows_its_space_after(self, space_after_get_fixture):
        paragraph_format, expected_value = space_after_get_fixture
        assert paragraph_format.space_after == expected_value

    def it_can_change_its_space_after(self, space_after_set_fixture):
        paragraph_format, value, expected_xml = space_after_set_fixture
        paragraph_format.space_after = value
        assert paragraph_format._element.xml == expected_xml

    def it_knows_its_line_spacing(self, line_spacing_get_fixture):
        paragraph_format, expected_value = line_spacing_get_fixture
        assert paragraph_format.line_spacing == expected_value

    def it_can_change_its_line_spacing(self, line_spacing_set_fixture):
        paragraph_format, value, expected_xml = line_spacing_set_fixture
        paragraph_format.line_spacing = value
        assert paragraph_format._element.xml == expected_xml

    def it_knows_its_line_spacing_rule(self, line_spacing_rule_get_fixture):
        paragraph_format, expected_value = line_spacing_rule_get_fixture
        assert paragraph_format.line_spacing_rule == expected_value

    def it_can_change_its_line_spacing_rule(self,
                                            line_spacing_rule_set_fixture):
        paragraph_format, value, expected_xml = line_spacing_rule_set_fixture
        paragraph_format.line_spacing_rule = value
        assert paragraph_format._element.xml == expected_xml

    def it_knows_its_first_line_indent(self, first_indent_get_fixture):
        paragraph_format, expected_value = first_indent_get_fixture
        assert paragraph_format.first_line_indent == expected_value

    def it_can_change_its_first_line_indent(self, first_indent_set_fixture):
        paragraph_format, value, expected_xml = first_indent_set_fixture
        paragraph_format.first_line_indent = value
        assert paragraph_format._element.xml == expected_xml

    def it_knows_its_left_indent(self, left_indent_get_fixture):
        paragraph_format, expected_value = left_indent_get_fixture
        assert paragraph_format.left_indent == expected_value

    def it_can_change_its_left_indent(self, left_indent_set_fixture):
        paragraph_format, value, expected_xml = left_indent_set_fixture
        paragraph_format.left_indent = value
        assert paragraph_format._element.xml == expected_xml

    def it_knows_its_right_indent(self, right_indent_get_fixture):
        paragraph_format, expected_value = right_indent_get_fixture
        assert paragraph_format.right_indent == expected_value

    def it_can_change_its_right_indent(self, right_indent_set_fixture):
        paragraph_format, value, expected_xml = right_indent_set_fixture
        paragraph_format.right_indent = value
        assert paragraph_format._element.xml == expected_xml

    def it_knows_its_on_off_prop_values(self, on_off_get_fixture):
        paragraph_format, prop_name, expected_value = on_off_get_fixture
        assert getattr(paragraph_format, prop_name) == expected_value

    def it_can_change_its_on_off_props(self, on_off_set_fixture):
        paragraph_format, prop_name, value, expected_xml = on_off_set_fixture
        setattr(paragraph_format, prop_name, value)
        assert paragraph_format._element.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('w:p',                          None),
        ('w:p/w:pPr',                    None),
        ('w:p/w:pPr/w:jc{w:val=center}', WD_ALIGN_PARAGRAPH.CENTER),
    ])
    def alignment_get_fixture(self, request):
        p_cxml, expected_value = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        return paragraph_format, expected_value

    @pytest.fixture(params=[
        ('w:p',                          WD_ALIGN_PARAGRAPH.LEFT,
         'w:p/w:pPr/w:jc{w:val=left}'),
        ('w:p/w:pPr',                    WD_ALIGN_PARAGRAPH.CENTER,
         'w:p/w:pPr/w:jc{w:val=center}'),
        ('w:p/w:pPr/w:jc{w:val=center}', WD_ALIGN_PARAGRAPH.RIGHT,
         'w:p/w:pPr/w:jc{w:val=right}'),
        ('w:p/w:pPr/w:jc{w:val=right}',  None,
         'w:p/w:pPr'),
        ('w:p',                          None,
         'w:p/w:pPr'),
    ])
    def alignment_set_fixture(self, request):
        p_cxml, value, expected_cxml = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        expected_xml = xml(expected_cxml)
        return paragraph_format, value, expected_xml

    @pytest.fixture(params=[
        ('w:p',                              None),
        ('w:p/w:pPr',                        None),
        ('w:p/w:pPr/w:ind',                  None),
        ('w:p/w:pPr/w:ind{w:firstLine=240}', Pt(12)),
        ('w:p/w:pPr/w:ind{w:hanging=240}',   Pt(-12)),
    ])
    def first_indent_get_fixture(self, request):
        p_cxml, expected_value = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        return paragraph_format, expected_value

    @pytest.fixture(params=[
        ('w:p', Pt(36),  'w:p/w:pPr/w:ind{w:firstLine=720}'),
        ('w:p', Pt(-36), 'w:p/w:pPr/w:ind{w:hanging=720}'),
        ('w:p', 0,       'w:p/w:pPr/w:ind{w:firstLine=0}'),
        ('w:p', None,    'w:p/w:pPr'),
        ('w:p/w:pPr/w:ind{w:firstLine=240}', None,
         'w:p/w:pPr/w:ind'),
        ('w:p/w:pPr/w:ind{w:firstLine=240}', Pt(-18),
         'w:p/w:pPr/w:ind{w:hanging=360}'),
        ('w:p/w:pPr/w:ind{w:hanging=240}',   Pt(18),
         'w:p/w:pPr/w:ind{w:firstLine=360}'),
    ])
    def first_indent_set_fixture(self, request):
        p_cxml, value, expected_p_cxml = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        expected_xml = xml(expected_p_cxml)
        return paragraph_format, value, expected_xml

    @pytest.fixture(params=[
        ('w:p',                             None),
        ('w:p/w:pPr',                       None),
        ('w:p/w:pPr/w:ind',                 None),
        ('w:p/w:pPr/w:ind{w:left=120}',     Pt(6)),
        ('w:p/w:pPr/w:ind{w:left=-06.3pt}', Pt(-6.3)),
    ])
    def left_indent_get_fixture(self, request):
        p_cxml, expected_value = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        return paragraph_format, expected_value

    @pytest.fixture(params=[
        ('w:p', Pt(36), 'w:p/w:pPr/w:ind{w:left=720}'),
        ('w:p', Pt(-3), 'w:p/w:pPr/w:ind{w:left=-60}'),
        ('w:p', 0,      'w:p/w:pPr/w:ind{w:left=0}'),
        ('w:p', None,   'w:p/w:pPr'),
        ('w:p/w:pPr/w:ind{w:left=240}', None, 'w:p/w:pPr/w:ind'),
    ])
    def left_indent_set_fixture(self, request):
        p_cxml, value, expected_p_cxml = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        expected_xml = xml(expected_p_cxml)
        return paragraph_format, value, expected_xml

    @pytest.fixture(params=[
        ('w:p',                                                None),
        ('w:p/w:pPr',                                          None),
        ('w:p/w:pPr/w:spacing',                                None),
        ('w:p/w:pPr/w:spacing{w:line=420}',                    1.75),
        ('w:p/w:pPr/w:spacing{w:line=840,w:lineRule=exact}',   Pt(42)),
        ('w:p/w:pPr/w:spacing{w:line=840,w:lineRule=atLeast}', Pt(42)),
    ])
    def line_spacing_get_fixture(self, request):
        p_cxml, expected_value = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        return paragraph_format, expected_value

    @pytest.fixture(params=[
        ('w:p', 1,      'w:p/w:pPr/w:spacing{w:line=240,w:lineRule=auto}'),
        ('w:p', 2.0,    'w:p/w:pPr/w:spacing{w:line=480,w:lineRule=auto}'),
        ('w:p', Pt(42), 'w:p/w:pPr/w:spacing{w:line=840,w:lineRule=exact}'),
        ('w:p/w:pPr',                                          2,
         'w:p/w:pPr/w:spacing{w:line=480,w:lineRule=auto}'),
        ('w:p/w:pPr/w:spacing{w:line=360}',                    1,
         'w:p/w:pPr/w:spacing{w:line=240,w:lineRule=auto}'),
        ('w:p/w:pPr/w:spacing{w:line=240,w:lineRule=exact}',   1.75,
         'w:p/w:pPr/w:spacing{w:line=420,w:lineRule=auto}'),
        ('w:p/w:pPr/w:spacing{w:line=240,w:lineRule=atLeast}', Pt(42),
         'w:p/w:pPr/w:spacing{w:line=840,w:lineRule=atLeast}'),
        ('w:p/w:pPr/w:spacing{w:line=240,w:lineRule=exact}',   None,
         'w:p/w:pPr/w:spacing'),
        ('w:p/w:pPr',                                          None,
         'w:p/w:pPr'),
    ])
    def line_spacing_set_fixture(self, request):
        p_cxml, value, expected_p_cxml = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        expected_xml = xml(expected_p_cxml)
        return paragraph_format, value, expected_xml

    @pytest.fixture(params=[
        ('w:p',                             None),
        ('w:p/w:pPr',                       None),
        ('w:p/w:pPr/w:spacing',             None),
        ('w:p/w:pPr/w:spacing{w:line=240}', WD_LINE_SPACING.SINGLE),
        ('w:p/w:pPr/w:spacing{w:line=360}', WD_LINE_SPACING.ONE_POINT_FIVE),
        ('w:p/w:pPr/w:spacing{w:line=480}', WD_LINE_SPACING.DOUBLE),
        ('w:p/w:pPr/w:spacing{w:line=420}', WD_LINE_SPACING.MULTIPLE),
        ('w:p/w:pPr/w:spacing{w:lineRule=auto}',
         WD_LINE_SPACING.MULTIPLE),
        ('w:p/w:pPr/w:spacing{w:lineRule=exact}',
         WD_LINE_SPACING.EXACTLY),
        ('w:p/w:pPr/w:spacing{w:lineRule=atLeast}',
         WD_LINE_SPACING.AT_LEAST),
    ])
    def line_spacing_rule_get_fixture(self, request):
        p_cxml, expected_value = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        return paragraph_format, expected_value

    @pytest.fixture(params=[
        ('w:p', WD_LINE_SPACING.SINGLE,
         'w:p/w:pPr/w:spacing{w:line=240,w:lineRule=auto}'),
        ('w:p', WD_LINE_SPACING.ONE_POINT_FIVE,
         'w:p/w:pPr/w:spacing{w:line=360,w:lineRule=auto}'),
        ('w:p', WD_LINE_SPACING.DOUBLE,
         'w:p/w:pPr/w:spacing{w:line=480,w:lineRule=auto}'),
        ('w:p', WD_LINE_SPACING.MULTIPLE,
         'w:p/w:pPr/w:spacing{w:lineRule=auto}'),
        ('w:p', WD_LINE_SPACING.EXACTLY,
         'w:p/w:pPr/w:spacing{w:lineRule=exact}'),
        ('w:p/w:pPr/w:spacing{w:line=280,w:lineRule=exact}',
         WD_LINE_SPACING.AT_LEAST,
         'w:p/w:pPr/w:spacing{w:line=280,w:lineRule=atLeast}'),
    ])
    def line_spacing_rule_set_fixture(self, request):
        p_cxml, value, expected_p_cxml = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        expected_xml = xml(expected_p_cxml)
        return paragraph_format, value, expected_xml

    @pytest.fixture(params=[
        ('w:p',                                  'keep_together',     None),
        ('w:p/w:pPr/w:keepLines{w:val=on}',      'keep_together',     True),
        ('w:p/w:pPr/w:keepLines{w:val=0}',       'keep_together',     False),
        ('w:p',                                  'keep_with_next',    None),
        ('w:p/w:pPr/w:keepNext{w:val=1}',        'keep_with_next',    True),
        ('w:p/w:pPr/w:keepNext{w:val=false}',    'keep_with_next',    False),
        ('w:p',                                  'page_break_before', None),
        ('w:p/w:pPr/w:pageBreakBefore',          'page_break_before', True),
        ('w:p/w:pPr/w:pageBreakBefore{w:val=0}', 'page_break_before', False),
        ('w:p',                                  'widow_control',     None),
        ('w:p/w:pPr/w:widowControl{w:val=true}', 'widow_control',     True),
        ('w:p/w:pPr/w:widowControl{w:val=off}',  'widow_control',     False),
    ])
    def on_off_get_fixture(self, request):
        p_cxml, prop_name, expected_value = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        return paragraph_format, prop_name, expected_value

    @pytest.fixture(params=[
        ('w:p', 'keep_together',     True,  'w:p/w:pPr/w:keepLines'),
        ('w:p', 'keep_with_next',    True,  'w:p/w:pPr/w:keepNext'),
        ('w:p', 'page_break_before', True,  'w:p/w:pPr/w:pageBreakBefore'),
        ('w:p', 'widow_control',     True,  'w:p/w:pPr/w:widowControl'),
        ('w:p/w:pPr/w:keepLines',                 'keep_together',     False,
         'w:p/w:pPr/w:keepLines{w:val=0}'),
        ('w:p/w:pPr/w:keepNext',                  'keep_with_next',    False,
         'w:p/w:pPr/w:keepNext{w:val=0}'),
        ('w:p/w:pPr/w:pageBreakBefore',           'page_break_before', False,
         'w:p/w:pPr/w:pageBreakBefore{w:val=0}'),
        ('w:p/w:pPr/w:widowControl',              'widow_control',     False,
         'w:p/w:pPr/w:widowControl{w:val=0}'),
        ('w:p/w:pPr/w:keepLines{w:val=0}',        'keep_together',     None,
         'w:p/w:pPr'),
        ('w:p/w:pPr/w:keepNext{w:val=0}',         'keep_with_next',    None,
         'w:p/w:pPr'),
        ('w:p/w:pPr/w:pageBreakBefore{w:val=0}',  'page_break_before', None,
         'w:p/w:pPr'),
        ('w:p/w:pPr/w:widowControl{w:val=0}',     'widow_control',     None,
         'w:p/w:pPr'),
    ])
    def on_off_set_fixture(self, request):
        p_cxml, prop_name, value, expected_cxml = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        expected_xml = xml(expected_cxml)
        return paragraph_format, prop_name, value, expected_xml

    @pytest.fixture(params=[
        ('w:p',                             None),
        ('w:p/w:pPr',                       None),
        ('w:p/w:pPr/w:ind',                 None),
        ('w:p/w:pPr/w:ind{w:right=160}',    Pt(8)),
        ('w:p/w:pPr/w:ind{w:right=-4.2pt}', Pt(-4.2)),
    ])
    def right_indent_get_fixture(self, request):
        p_cxml, expected_value = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        return paragraph_format, expected_value

    @pytest.fixture(params=[
        ('w:p', Pt(36), 'w:p/w:pPr/w:ind{w:right=720}'),
        ('w:p', Pt(-3), 'w:p/w:pPr/w:ind{w:right=-60}'),
        ('w:p', 0,      'w:p/w:pPr/w:ind{w:right=0}'),
        ('w:p', None,   'w:p/w:pPr'),
        ('w:p/w:pPr/w:ind{w:right=240}', None, 'w:p/w:pPr/w:ind'),
    ])
    def right_indent_set_fixture(self, request):
        p_cxml, value, expected_p_cxml = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        expected_xml = xml(expected_p_cxml)
        return paragraph_format, value, expected_xml

    @pytest.fixture(params=[
        ('w:p',                              None),
        ('w:p/w:pPr',                        None),
        ('w:p/w:pPr/w:spacing',              None),
        ('w:p/w:pPr/w:spacing{w:after=240}', Pt(12)),
    ])
    def space_after_get_fixture(self, request):
        p_cxml, expected_value = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        return paragraph_format, expected_value

    @pytest.fixture(params=[
        ('w:p',                 Pt(12), 'w:p/w:pPr/w:spacing{w:after=240}'),
        ('w:p',                 None,   'w:p/w:pPr'),
        ('w:p/w:pPr',           Pt(12), 'w:p/w:pPr/w:spacing{w:after=240}'),
        ('w:p/w:pPr',           None,   'w:p/w:pPr'),
        ('w:p/w:pPr/w:spacing', Pt(12), 'w:p/w:pPr/w:spacing{w:after=240}'),
        ('w:p/w:pPr/w:spacing', None,   'w:p/w:pPr/w:spacing'),
        ('w:p/w:pPr/w:spacing{w:after=240}', Pt(42),
         'w:p/w:pPr/w:spacing{w:after=840}'),
        ('w:p/w:pPr/w:spacing{w:after=840}', None,
         'w:p/w:pPr/w:spacing'),
    ])
    def space_after_set_fixture(self, request):
        p_cxml, value, expected_p_cxml = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        expected_xml = xml(expected_p_cxml)
        return paragraph_format, value, expected_xml

    @pytest.fixture(params=[
        ('w:p',                               None),
        ('w:p/w:pPr',                         None),
        ('w:p/w:pPr/w:spacing',               None),
        ('w:p/w:pPr/w:spacing{w:before=420}', Pt(21)),
    ])
    def space_before_get_fixture(self, request):
        p_cxml, expected_value = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        return paragraph_format, expected_value

    @pytest.fixture(params=[
        ('w:p',                 Pt(12), 'w:p/w:pPr/w:spacing{w:before=240}'),
        ('w:p',                 None,   'w:p/w:pPr'),
        ('w:p/w:pPr',           Pt(12), 'w:p/w:pPr/w:spacing{w:before=240}'),
        ('w:p/w:pPr',           None,   'w:p/w:pPr'),
        ('w:p/w:pPr/w:spacing', Pt(12), 'w:p/w:pPr/w:spacing{w:before=240}'),
        ('w:p/w:pPr/w:spacing', None,   'w:p/w:pPr/w:spacing'),
        ('w:p/w:pPr/w:spacing{w:before=240}', Pt(42),
         'w:p/w:pPr/w:spacing{w:before=840}'),
        ('w:p/w:pPr/w:spacing{w:before=840}', None,
         'w:p/w:pPr/w:spacing'),
    ])
    def space_before_set_fixture(self, request):
        p_cxml, value, expected_p_cxml = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        expected_xml = xml(expected_p_cxml)
        return paragraph_format, value, expected_xml
