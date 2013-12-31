# encoding: utf-8

"""
Step implementations for text-related features
"""

from __future__ import absolute_import, print_function, unicode_literals

from behave import given, then, when

from docx import Document


# given ===================================================

@given('a run')
def given_a_run(context):
    p = Document().body.paragraphs[0]
    context.run = p.add_run()


# when ====================================================

@when('I add a line break')
def when_add_line_break(context):
    run = context.run
    run.add_break()


# then =====================================================

@then('the last item in the run is a break')
def then_last_item_in_run_is_a_break(context):
    run = context.run
    context.last_child = run._r[-1]
    expected_tag = (
        '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}br'
    )
    assert context.last_child.tag == expected_tag


@then('it is a line break')
def then_type_is_line_break(context):
    attrib = context.last_child.attrib
    assert attrib == {}


@then('it is a page break')
def then_type_is_page_break(context):
    attrib = context.last_child.attrib
    assert attrib == {'type': 'page'}


@then('it is a column break')
def then_type_is_column_break(context):
    attrib = context.last_child.attrib
    assert attrib == {'type': 'column'}
