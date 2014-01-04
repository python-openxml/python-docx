# encoding: utf-8

"""
Step implementations for text-related features
"""

from __future__ import absolute_import, print_function, unicode_literals

from behave import given, then, when

from docx import Document
from docx.enum.text import WD_BREAK
from docx.oxml.shared import qn


# given ===================================================

@given('a run')
def given_a_run(context):
    p = Document().add_paragraph()
    context.run = p.add_run()


@given('a run having bold set on')
def given_a_run_having_bold_set_on(context):
    run = Document().add_paragraph().add_run()
    run.bold = True
    context.run = run


@given('a run having italic set on')
def given_a_run_having_italic_set_on(context):
    run = Document().add_paragraph().add_run()
    run.italic = True
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


@when('I assign {value_str} to its bold property')
def when_assign_true_to_its_bold_property(context, value_str):
    value = {'True': True, 'False': False, 'None': None}[value_str]
    run = context.run
    run.bold = value


@when('I assign {value_str} to its italic property')
def when_assign_true_to_its_italic_property(context, value_str):
    value = {'True': True, 'False': False, 'None': None}[value_str]
    run = context.run
    run.italic = value


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


@then('the run appears in bold typeface')
def then_run_appears_in_bold_typeface(context):
    run = context.run
    assert run.bold is True


@then('the run appears in italic typeface')
def then_run_appears_in_italic_typeface(context):
    run = context.run
    assert run.italic is True


@then('the run appears with its inherited bold setting')
def then_run_appears_with_its_inherited_bold_setting(context):
    run = context.run
    assert run.bold is None


@then('the run appears with its inherited italic setting')
def then_run_appears_with_its_inherited_italic_setting(context):
    run = context.run
    assert run.italic is None


@then('the run appears without bold regardless of its style hierarchy')
def then_run_appears_without_bold_regardless(context):
    run = context.run
    assert run.bold is False


@then('the run appears without italic regardless of its style hierarchy')
def then_run_appears_without_italic_regardless(context):
    run = context.run
    assert run.italic is False
