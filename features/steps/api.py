# encoding: utf-8

"""
Step implementations for top-level features
"""

from behave import then, when


# when ====================================================

@when('I add a paragraph without specifying text or style')
def step_when_add_paragraph_without_specifying_text_or_style(context):
    document = context.document
    document.add_paragraph()


# then =====================================================

@then('the last paragraph is the empty paragraph I added')
def step_then_document_contains_text_I_added(context):
    document = context.document
    p = document.paragraphs[-1]
    assert p.text == ''
