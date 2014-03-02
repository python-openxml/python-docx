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


@given('a run having {bool_prop_name} set on')
def given_a_run_having_bool_prop_set_on(context, bool_prop_name):
    run = Document().add_paragraph().add_run()
    setattr(run, bool_prop_name, True)
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


@when('I assign {value_str} to its {bool_prop_name} property')
def when_assign_true_to_bool_run_prop(context, value_str, bool_prop_name):
    value = {'True': True, 'False': False, 'None': None}[value_str]
    run = context.run
    setattr(run, bool_prop_name, value)


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
