# encoding: utf-8

"""
Step implementations for text-related features
"""

from __future__ import absolute_import, print_function, unicode_literals

import hashlib

from behave import given, then, when

from docx import Document
from docx.enum.text import (
    WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING, WD_UNDERLINE
)
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Pt
from docx.text.run import Font, Run

from helpers import test_docx, test_file, test_text


# given ===================================================

@given('a font having typeface name {name}')
def given_a_font_having_typeface_name(context, name):
    document = Document(test_docx('txt-font-props'))
    style_name = {
        'not specified': 'Normal',
        'Avenir Black':  'Having Typeface',
    }[name]
    context.font = document.styles[style_name].font


@given('a font having {underline_type} underline')
def given_a_font_having_type_underline(context, underline_type):
    style_name = {
        'inherited': 'Normal',
        'no':        'None Underlined',
        'single':    'Underlined',
        'double':    'Double Underlined',
    }[underline_type]
    document = Document(test_docx('txt-font-props'))
    context.font = document.styles[style_name].font


@given('a font having {vertAlign_state} vertical alignment')
def given_a_font_having_vertAlign_state(context, vertAlign_state):
    style_name = {
        'inherited':   'Normal',
        'subscript':   'Subscript',
        'superscript': 'Superscript',
    }[vertAlign_state]
    document = Document(test_docx('txt-font-props'))
    context.font = document.styles[style_name].font


@given('a font of size {size}')
def given_a_font_of_size(context, size):
    document = Document(test_docx('txt-font-props'))
    style_name = {
        'unspecified': 'Normal',
        '14 pt':       'Having Typeface',
        '18 pt':       'Large Size',
    }[size]
    context.font = document.styles[style_name].font


@given('a paragraph format having {prop_name} set {setting}')
def given_a_paragraph_format_having_prop_set(context, prop_name, setting):
    style_name = {
        'to inherit': 'Normal',
        'On':         'Base',
        'Off':        'Citation',
    }[setting]
    document = Document(test_docx('sty-known-styles'))
    context.paragraph_format = document.styles[style_name].paragraph_format


@given('a paragraph format having {setting} line spacing')
def given_a_paragraph_format_having_setting_line_spacing(context, setting):
    style_name = {
        'inherited': 'Normal',
        '14 pt':     'Base',
        'double':    'Citation',
    }[setting]
    document = Document(test_docx('sty-known-styles'))
    context.paragraph_format = document.styles[style_name].paragraph_format


@given('a paragraph format having {setting} space {side}')
def given_a_paragraph_format_having_setting_spacing(context, setting, side):
    style_name = 'Normal' if setting == 'inherited' else 'Base'
    document = Document(test_docx('sty-known-styles'))
    context.paragraph_format = document.styles[style_name].paragraph_format


@given('a paragraph format having {type} alignment')
def given_a_paragraph_format_having_align_type_alignment(context, type):
    style_name = {
        'inherited': 'Normal',
        'center':    'Base',
        'right':     'Citation',
    }[type]
    document = Document(test_docx('sty-known-styles'))
    context.paragraph_format = document.styles[style_name].paragraph_format


@given('a paragraph format having {type} indent of {value}')
def given_a_paragraph_format_having_type_indent_value(context, type, value):
    style_name = {
        'inherit':  'Normal',
        '18 pt':    'Base',
        '17.3 pt':  'Base',
        '-17.3 pt': 'Citation',
        '46.1 pt':  'Citation',
    }[value]
    document = Document(test_docx('sty-known-styles'))
    context.paragraph_format = document.styles[style_name].paragraph_format


@given('a run')
def given_a_run(context):
    document = Document()
    run = document.add_paragraph().add_run()
    context.document = document
    context.run = run


@given('a run having {bool_prop_name} set on')
def given_a_run_having_bool_prop_set_on(context, bool_prop_name):
    run = Document().add_paragraph().add_run()
    setattr(run, bool_prop_name, True)
    context.run = run


@given('a run having known text and formatting')
def given_a_run_having_known_text_and_formatting(context):
    run = Document().add_paragraph().add_run('foobar')
    run.bold = True
    run.italic = True
    context.run = run


@given('a run having mixed text content')
def given_a_run_having_mixed_text_content(context):
    """
    Mixed here meaning it contains ``<w:tab/>``, ``<w:cr/>``, etc. elements.
    """
    r_xml = """\
        <w:r %s>
          <w:t>abc</w:t>
          <w:tab/>
          <w:t>def</w:t>
          <w:cr/>
          <w:t>ghi</w:t>
          <w:drawing/>
          <w:br/>
          <w:t>jkl</w:t>
        </w:r>""" % nsdecls('w')
    r = parse_xml(r_xml)
    context.run = Run(r, None)


@given('a run having {underline_type} underline')
def given_a_run_having_underline_type(context, underline_type):
    run_idx = {
        'inherited': 0, 'no': 1, 'single': 2, 'double': 3
    }[underline_type]
    document = Document(test_docx('run-enumerated-props'))
    context.run = document.paragraphs[0].runs[run_idx]


@given('a run having {style} style')
def given_a_run_having_style(context, style):
    run_idx = {
        'no explicit': 0,
        'Emphasis':    1,
        'Strong':      2,
    }[style]
    context.document = document = Document(test_docx('run-char-style'))
    context.run = document.paragraphs[0].runs[run_idx]


@given('a run inside a table cell retrieved from {cell_source}')
def given_a_run_inside_a_table_cell_from_source(context, cell_source):
    document = Document()
    table = document.add_table(rows=2, cols=2)
    if cell_source == 'Table.cell':
        cell = table.cell(0, 0)
    elif cell_source == 'Table.row.cells':
        cell = table.rows[0].cells[1]
    elif cell_source == 'Table.column.cells':
        cell = table.columns[1].cells[0]
    run = cell.paragraphs[0].add_run()
    context.document = document
    context.run = run


# when ====================================================

@when('I add a column break')
def when_add_column_break(context):
    run = context.run
    run.add_break(WD_BREAK.COLUMN)


@when('I add a line break')
def when_add_line_break(context):
    run = context.run
    run.add_break()


@when('I add a page break')
def when_add_page_break(context):
    run = context.run
    run.add_break(WD_BREAK.PAGE)


@when('I add a picture to the run')
def when_I_add_a_picture_to_the_run(context):
    run = context.run
    run.add_picture(test_file('monty-truth.png'))


@when('I add a run specifying its text')
def when_I_add_a_run_specifying_its_text(context):
    context.run = context.paragraph.add_run(test_text)


@when('I add a run specifying the character style Emphasis')
def when_I_add_a_run_specifying_the_character_style_Emphasis(context):
    context.run = context.paragraph.add_run(test_text, 'Emphasis')


@when('I add a tab')
def when_I_add_a_tab(context):
    context.run.add_tab()


@when('I add text to the run')
def when_I_add_text_to_the_run(context):
    context.run.add_text(test_text)


@when('I assign mixed text to the text property')
def when_I_assign_mixed_text_to_the_text_property(context):
    context.run.text = 'abc\tdef\nghi\rjkl'


@when('I assign {value} to font.name')
def when_I_assign_value_to_font_name(context, value):
    font = context.font
    value = None if value == 'None' else value
    font.name = value


@when('I assign {value} to font.size')
def when_I_assign_value_str_to_font_size(context, value):
    value = None if value == 'None' else int(value)
    font = context.font
    font.size = value


@when('I assign {value_key} to font.underline')
def when_I_assign_value_to_font_underline(context, value_key):
    value = {
        'True':                True,
        'False':               False,
        'None':                None,
        'WD_UNDERLINE.SINGLE': WD_UNDERLINE.SINGLE,
        'WD_UNDERLINE.DOUBLE': WD_UNDERLINE.DOUBLE,
    }[value_key]
    font = context.font
    font.underline = value


@when('I assign {value_key} to paragraph_format.line_spacing')
def when_I_assign_value_to_paragraph_format_line_spacing(context, value_key):
    value = {
        'Pt(14)': Pt(14),
        '2':      2,
    }.get(value_key)
    value = float(value_key) if value is None else value
    context.paragraph_format.line_spacing = value


@when('I assign {value_key} to paragraph_format.line_spacing_rule')
def when_I_assign_value_to_paragraph_format_line_rule(context, value_key):
    value = {
        'None':                           None,
        'WD_LINE_SPACING.EXACTLY':        WD_LINE_SPACING.EXACTLY,
        'WD_LINE_SPACING.MULTIPLE':       WD_LINE_SPACING.MULTIPLE,
        'WD_LINE_SPACING.SINGLE':         WD_LINE_SPACING.SINGLE,
        'WD_LINE_SPACING.DOUBLE':         WD_LINE_SPACING.DOUBLE,
        'WD_LINE_SPACING.AT_LEAST':       WD_LINE_SPACING.AT_LEAST,
        'WD_LINE_SPACING.ONE_POINT_FIVE': WD_LINE_SPACING.ONE_POINT_FIVE,
    }[value_key]
    paragraph_format = context.paragraph_format
    paragraph_format.line_spacing_rule = value


@when('I assign {value_key} to font.{sub_super}script')
def when_I_assign_value_to_font_sub_super(context, value_key, sub_super):
    font = context.font
    name = {
        'sub':   'subscript',
        'super': 'superscript',
    }[sub_super]
    value = {
        'None':  None,
        'True':  True,
        'False': False,
    }[value_key]

    setattr(font, name, value)


@when('I assign {value_key} to paragraph_format.alignment')
def when_I_assign_value_to_paragraph_format_alignment(context, value_key):
    value = {
        'None':                      None,
        'WD_ALIGN_PARAGRAPH.CENTER': WD_ALIGN_PARAGRAPH.CENTER,
        'WD_ALIGN_PARAGRAPH.RIGHT':  WD_ALIGN_PARAGRAPH.RIGHT,
    }[value_key]
    paragraph_format = context.paragraph_format
    paragraph_format.alignment = value


@when('I assign {value_key} to paragraph_format.space_{side}')
def when_I_assign_value_to_paragraph_format_space(context, value_key, side):
    paragraph_format = context.paragraph_format
    prop_name = 'space_%s' % side
    value = {
        'None':   None,
        'Pt(12)': Pt(12),
        'Pt(18)': Pt(18),
    }[value_key]
    setattr(paragraph_format, prop_name, value)


@when('I assign {value} to paragraph_format.{type_}_indent')
def when_I_assign_value_to_paragraph_format_indent(context, value, type_):
    paragraph_format = context.paragraph_format
    prop_name = '%s_indent' % type_
    value = None if value == 'None' else Pt(float(value.split()[0]))
    setattr(paragraph_format, prop_name, value)


@when('I assign {value} to paragraph_format.{prop_name}')
def when_I_assign_value_to_paragraph_format_prop(context, value, prop_name):
    paragraph_format = context.paragraph_format
    value = {'None': None, 'True': True, 'False': False}[value]
    setattr(paragraph_format, prop_name, value)


@when('I assign {value_str} to its {bool_prop_name} property')
def when_assign_true_to_bool_run_prop(context, value_str, bool_prop_name):
    value = {'True': True, 'False': False, 'None': None}[value_str]
    run = context.run
    setattr(run, bool_prop_name, value)


@when('I assign {value} to run.style')
def when_I_assign_value_to_run_style(context, value):
    if value == 'None':
        new_value = None
    elif value.startswith('styles['):
        new_value = context.document.styles[value.split('\'')[1]]
    else:
        new_value = context.document.styles[value]

    context.run.style = new_value


@when('I clear the run')
def when_I_clear_the_run(context):
    context.run.clear()


@when('I set the run underline to {underline_value}')
def when_I_set_the_run_underline_to_value(context, underline_value):
    new_value = {
        'True': True, 'False': False, 'None': None,
        'WD_UNDERLINE.SINGLE': WD_UNDERLINE.SINGLE,
        'WD_UNDERLINE.DOUBLE': WD_UNDERLINE.DOUBLE,
    }[underline_value]
    context.run.underline = new_value


# then =====================================================

@then('font.name is {value}')
def then_font_name_is_value(context, value):
    font = context.font
    value = None if value == 'None' else value
    assert font.name == value


@then('font.size is {value}')
def then_font_size_is_value(context, value):
    value = None if value == 'None' else int(value)
    font = context.font
    assert font.size == value


@then('font.underline is {value_key}')
def then_font_underline_is_value(context, value_key):
    value = {
        'None':                None,
        'True':                True,
        'False':               False,
        'WD_UNDERLINE.DOUBLE': WD_UNDERLINE.DOUBLE,
    }[value_key]
    font = context.font
    assert font.underline == value


@then('font.{sub_super}script is {value_key}')
def then_font_sub_super_is_value(context, sub_super, value_key):
    name = {
        'sub':   'subscript',
        'super': 'superscript',
    }[sub_super]
    expected_value = {
        'None':  None,
        'True':  True,
        'False': False,
    }[value_key]
    font = context.font
    actual_value = getattr(font, name)
    assert actual_value == expected_value


@then('it is a column break')
def then_type_is_column_break(context):
    attrib = context.last_child.attrib
    assert attrib == {qn('w:type'): 'column'}


@then('it is a line break')
def then_type_is_line_break(context):
    attrib = context.last_child.attrib
    assert attrib == {}


@then('it is a page break')
def then_type_is_page_break(context):
    attrib = context.last_child.attrib
    assert attrib == {qn('w:type'): 'page'}


@then('paragraph_format.alignment is {value_key}')
def then_paragraph_format_alignment_is_value(context, value_key):
    value = {
        'None':                      None,
        'WD_ALIGN_PARAGRAPH.LEFT':   WD_ALIGN_PARAGRAPH.LEFT,
        'WD_ALIGN_PARAGRAPH.CENTER': WD_ALIGN_PARAGRAPH.CENTER,
        'WD_ALIGN_PARAGRAPH.RIGHT':  WD_ALIGN_PARAGRAPH.RIGHT,
    }[value_key]
    paragraph_format = context.paragraph_format
    assert paragraph_format.alignment == value


@then('paragraph_format.line_spacing is {value}')
def then_paragraph_format_line_spacing_is_value(context, value):
    value = (
        None if value == 'None' else
        float(value) if '.' in value else
        int(value)
    )
    paragraph_format = context.paragraph_format

    if value is None or isinstance(value, int):
        assert paragraph_format.line_spacing == value
    else:
        assert abs(paragraph_format.line_spacing - value) < 0.001


@then('paragraph_format.line_spacing_rule is {value_key}')
def then_paragraph_format_line_spacing_rule_is_value(context, value_key):
    value = {
        'None':                           None,
        'WD_LINE_SPACING.EXACTLY':        WD_LINE_SPACING.EXACTLY,
        'WD_LINE_SPACING.MULTIPLE':       WD_LINE_SPACING.MULTIPLE,
        'WD_LINE_SPACING.SINGLE':         WD_LINE_SPACING.SINGLE,
        'WD_LINE_SPACING.DOUBLE':         WD_LINE_SPACING.DOUBLE,
        'WD_LINE_SPACING.AT_LEAST':       WD_LINE_SPACING.AT_LEAST,
        'WD_LINE_SPACING.ONE_POINT_FIVE': WD_LINE_SPACING.ONE_POINT_FIVE,
    }[value_key]
    paragraph_format = context.paragraph_format
    assert paragraph_format.line_spacing_rule == value


@then('paragraph_format.space_{side} is {value}')
def then_paragraph_format_space_side_is_value(context, side, value):
    expected_value = None if value == 'None' else int(value)
    prop_name = 'space_%s' % side
    paragraph_format = context.paragraph_format
    actual_value = getattr(paragraph_format, prop_name)
    assert actual_value == expected_value


@then('paragraph_format.{type_}_indent is {value}')
def then_paragraph_format_type_indent_is_value(context, type_, value):
    expected_value = None if value == 'None' else int(value)
    prop_name = '%s_indent' % type_
    paragraph_format = context.paragraph_format
    actual_value = getattr(paragraph_format, prop_name)
    assert actual_value == expected_value


@then('paragraph_format.{prop_name} is {value}')
def then_paragraph_format_prop_name_is_value(context, prop_name, value):
    expected_value = {'None': None, 'True': True, 'False': False}[value]
    paragraph_format = context.paragraph_format
    actual_value = getattr(paragraph_format, prop_name)
    assert actual_value == expected_value


@then('run.font is the Font object for the run')
def then_run_font_is_the_Font_object_for_the_run(context):
    run, font = context.run, context.run.font
    assert isinstance(font, Font)
    assert font.element is run.element


@then('run.style is styles[\'{style_name}\']')
def then_run_style_is_style(context, style_name):
    expected_value = context.document.styles[style_name]
    run = context.run
    assert run.style == expected_value, 'got %s' % run.style


@then('the last item in the run is a break')
def then_last_item_in_run_is_a_break(context):
    run = context.run
    context.last_child = run._r[-1]
    expected_tag = (
        '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}br'
    )
    assert context.last_child.tag == expected_tag


@then('the picture appears at the end of the run')
def then_the_picture_appears_at_the_end_of_the_run(context):
    run = context.run
    r = run._r
    blip_rId = r.xpath(
        './w:drawing/wp:inline/a:graphic/a:graphicData/pic:pic/pic:blipFill/'
        'a:blip/@r:embed'
    )[0]
    image_part = run.part.related_parts[blip_rId]
    image_sha1 = hashlib.sha1(image_part.blob).hexdigest()
    expected_sha1 = '79769f1e202add2e963158b532e36c2c0f76a70c'
    assert image_sha1 == expected_sha1, (
        "image SHA1 doesn't match, expected %s, got %s" %
        (expected_sha1, image_sha1)
    )


@then('the run appears in {boolean_prop_name} unconditionally')
def then_run_appears_in_boolean_prop_name(context, boolean_prop_name):
    run = context.run
    assert getattr(run, boolean_prop_name) is True


@then('the run appears with its inherited {boolean_prop_name} setting')
def then_run_inherits_bool_prop_value(context, boolean_prop_name):
    run = context.run
    assert getattr(run, boolean_prop_name) is None


@then('the run appears without {boolean_prop_name} unconditionally')
def then_run_appears_without_bool_prop(context, boolean_prop_name):
    run = context.run
    assert getattr(run, boolean_prop_name) is False


@then('the run contains no text')
def then_the_run_contains_no_text(context):
    assert context.run.text == ''


@then('the run contains the text I specified')
def then_the_run_contains_the_text_I_specified(context):
    assert context.run.text == test_text


@then('the run formatting is preserved')
def then_the_run_formatting_is_preserved(context):
    assert context.run.bold is True
    assert context.run.italic is True


@then('the run underline property value is {underline_value}')
def then_the_run_underline_property_value_is(context, underline_value):
    expected_value = {
        'None': None, 'False': False, 'True': True,
        'WD_UNDERLINE.DOUBLE': WD_UNDERLINE.DOUBLE
    }[underline_value]
    assert context.run.underline == expected_value


@then('the tab appears at the end of the run')
def then_the_tab_appears_at_the_end_of_the_run(context):
    r = context.run._r
    tab = r.find(qn('w:tab'))
    assert tab is not None


@then('the text of the run represents the textual run content')
def then_the_text_of_the_run_represents_the_textual_run_content(context):
    assert context.run.text == 'abc\tdef\nghi\njkl', (
        'got \'%s\'' % context.run.text
    )
