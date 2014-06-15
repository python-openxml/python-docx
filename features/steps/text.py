# encoding: utf-8

"""
Step implementations for text-related features
"""

from __future__ import absolute_import, print_function, unicode_literals

from behave import given, then, when

from docx import Document
from docx.enum.text import WD_BREAK, WD_UNDERLINE
from docx.oxml.ns import qn

from helpers import test_docx, test_text


# given ===================================================

@given('a run')
def given_a_run(context):
    p = Document().add_paragraph()
    context.run = p.add_run()


@given('a run having {bool_prop_name} set on')
def given_a_run_having_bool_prop_set_on(context, bool_prop_name):
    run = Document().add_paragraph().add_run()
    setattr(run, bool_prop_name, True)
    context.run = run


@given('a run having {underline_type} underline')
def given_a_run_having_underline_type(context, underline_type):
    run_idx = {
        'inherited': 0, 'no': 1, 'single': 2, 'double': 3
    }[underline_type]
    document = Document(test_docx('run-enumerated-props'))
    context.run = document.paragraphs[0].runs[run_idx]


@given('a run having style {char_style}')
def given_a_run_having_style_char_style(context, char_style):
    run_idx = {
        'None': 0, 'Emphasis': 1, 'Strong': 2
    }[char_style]
    document = Document(test_docx('run-char-style'))
    context.run = document.paragraphs[0].runs[run_idx]


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


@when('I add a run specifying its text')
def when_I_add_a_run_specifying_its_text(context):
    context.run = context.paragraph.add_run(test_text)


@when('I add a run specifying the character style Emphasis')
def when_I_add_a_run_specifying_the_character_style_Emphasis(context):
    context.run = context.paragraph.add_run(test_text, 'Emphasis')


@when('I assign {value_str} to its {bool_prop_name} property')
def when_assign_true_to_bool_run_prop(context, value_str, bool_prop_name):
    value = {'True': True, 'False': False, 'None': None}[value_str]
    run = context.run
    setattr(run, bool_prop_name, value)


@when('I set the character style of the run to {char_style}')
def when_I_set_the_character_style_of_the_run(context, char_style):
    style_value = {
        'None': None, 'Emphasis': 'Emphasis', 'Strong': 'Strong'
    }[char_style]
    context.run.style = style_value


@when('I set the run underline to {underline_value}')
def when_I_set_the_run_underline_to_value(context, underline_value):
    new_value = {
        'True': True, 'False': False, 'None': None,
        'WD_UNDERLINE.SINGLE': WD_UNDERLINE.SINGLE,
        'WD_UNDERLINE.DOUBLE': WD_UNDERLINE.DOUBLE,
    }[underline_value]
    context.run.underline = new_value


# then =====================================================

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


@then('the last item in the run is a break')
def then_last_item_in_run_is_a_break(context):
    run = context.run
    context.last_child = run._r[-1]
    expected_tag = (
        '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}br'
    )
    assert context.last_child.tag == expected_tag


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


@then('the run contains the text I specified')
def then_the_run_contains_the_text_I_specified(context):
    assert context.run.text == test_text


@then('the run underline property value is {underline_value}')
def then_the_run_underline_property_value_is(context, underline_value):
    expected_value = {
        'None': None, 'False': False, 'True': True,
        'WD_UNDERLINE.DOUBLE': WD_UNDERLINE.DOUBLE
    }[underline_value]
    assert context.run.underline == expected_value


@then('the style of the run is {char_style}')
def then_the_style_of_the_run_is_char_style(context, char_style):
    expected_value = {
        'None': None, 'Emphasis': 'Emphasis', 'Strong': 'Strong'
    }[char_style]
    assert context.run.style == expected_value
