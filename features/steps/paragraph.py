# encoding: utf-8

"""
Step implementations for paragraph-related features
"""

from behave import then, when

from docx import Document

from helpers import saved_docx_path, test_text


TEST_STYLE = 'Heading1'


# when ====================================================

@when('I add a run to the paragraph')
def when_add_new_run_to_paragraph(context):
    context.r = context.p.add_run()


@when('I add text to the run')
def when_add_new_text_to_run(context):
    context.r.add_text(test_text)


@when('I set the paragraph style')
def when_I_set_the_paragraph_style(context):
    context.paragraph.add_run().add_text(test_text)
    context.paragraph.style = TEST_STYLE


# then =====================================================

@then('the document contains the text I added')
def then_document_contains_text_I_added(context):
    document = Document(saved_docx_path)
    paragraphs = document.paragraphs
    p = paragraphs[-1]
    r = p.runs[0]
    assert r.text == test_text


@then('the paragraph has the style I set')
def then_the_paragraph_has_the_style_I_set(context):
    paragraph = Document(saved_docx_path).paragraphs[-1]
    assert paragraph.style == TEST_STYLE
