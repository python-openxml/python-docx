# encoding: utf-8

"""
Step implementations for top-level features
"""

from behave import then, when


# when ====================================================

@when('I add a paragraph specifying its style')
def when_add_paragraph_specifying_style(context):
    document = context.document
    context.paragraph_style = 'barfoo'
    document.add_paragraph(style=context.paragraph_style)


@when('I add a paragraph specifying its text')
def when_add_paragraph_specifying_text(context):
    document = context.document
    context.paragraph_text = 'foobar'
    document.add_paragraph(context.paragraph_text)


@when('I add a paragraph without specifying text or style')
def when_add_paragraph_without_specifying_text_or_style(context):
    document = context.document
    document.add_paragraph()


# then =====================================================

@then('the last paragraph contains the text I specified')
def then_last_p_contains_specified_text(context):
    document = context.document
    text = context.paragraph_text
    p = document.paragraphs[-1]
    assert p.text == text


@then('the last paragraph is the empty paragraph I added')
def then_last_p_is_empty_paragraph_added(context):
    document = context.document
    p = document.paragraphs[-1]
    assert p.text == ''


@then('the last paragraph has the style I specified')
def then_last_p_has_specified_style(context):
    document = context.document
    style = context.paragraph_style
    p = document.paragraphs[-1]
    assert p.style == style
