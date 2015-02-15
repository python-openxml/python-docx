# encoding: utf-8

"""
Step implementations for paragraph-related features
"""

from behave import given, then, when

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.text.parfmt import ParagraphFormat

from helpers import saved_docx_path, test_docx, test_text


# given ===================================================

@given('a document containing three paragraphs')
def given_a_document_containing_three_paragraphs(context):
    document = Document()
    document.add_paragraph('foo')
    document.add_paragraph('bar')
    document.add_paragraph('baz')
    context.document = document


@given('a paragraph having {align_type} alignment')
def given_a_paragraph_align_type_alignment(context, align_type):
    paragraph_idx = {
        'inherited': 0,
        'left':      1,
        'center':    2,
        'right':     3,
        'justified': 4,
    }[align_type]
    document = Document(test_docx('par-alignment'))
    context.paragraph = document.paragraphs[paragraph_idx]


@given('a paragraph having {style_state} style')
def given_a_paragraph_having_style(context, style_state):
    paragraph_idx = {
        'no specified': 0,
        'a missing':    1,
        'Heading 1':    2,
        'Body Text':    3,
    }[style_state]
    document = context.document = Document(test_docx('par-known-styles'))
    context.paragraph = document.paragraphs[paragraph_idx]


@given('a paragraph with content and formatting')
def given_a_paragraph_with_content_and_formatting(context):
    document = Document(test_docx('par-known-paragraphs'))
    context.paragraph = document.paragraphs[0]


# when ====================================================

@when('I add a run to the paragraph')
def when_add_new_run_to_paragraph(context):
    context.run = context.p.add_run()


@when('I assign a {style_type} to paragraph.style')
def when_I_assign_a_style_type_to_paragraph_style(context, style_type):
    paragraph = context.paragraph
    style = context.style = context.document.styles['Heading 1']
    style_spec = {
        'style object': style,
        'style name':   'Heading 1',
    }[style_type]
    paragraph.style = style_spec


@when('I clear the paragraph content')
def when_I_clear_the_paragraph_content(context):
    context.paragraph.clear()


@when('I insert a paragraph above the second paragraph')
def when_I_insert_a_paragraph_above_the_second_paragraph(context):
    paragraph = context.document.paragraphs[1]
    paragraph.insert_paragraph_before('foobar', 'Heading1')


@when('I set the paragraph text')
def when_I_set_the_paragraph_text(context):
    context.paragraph.text = 'bar\tfoo\r'


# then =====================================================

@then('paragraph.paragraph_format is its ParagraphFormat object')
def then_paragraph_paragraph_format_is_its_parfmt_object(context):
    paragraph = context.paragraph
    paragraph_format = paragraph.paragraph_format
    assert isinstance(paragraph_format, ParagraphFormat)
    assert paragraph_format.element is paragraph._element


@then('paragraph.style is {value_key}')
def then_paragraph_style_is_value(context, value_key):
    styles = context.document.styles
    expected_value = {
        'Normal':    styles['Normal'],
        'Heading 1': styles['Heading 1'],
        'Body Text': styles['Body Text'],
    }[value_key]
    paragraph = context.paragraph
    assert paragraph.style == expected_value


@then('the document contains four paragraphs')
def then_the_document_contains_four_paragraphs(context):
    assert len(context.document.paragraphs) == 4


@then('the document contains the text I added')
def then_document_contains_text_I_added(context):
    document = Document(saved_docx_path)
    paragraphs = document.paragraphs
    p = paragraphs[-1]
    r = p.runs[0]
    assert r.text == test_text


@then('the paragraph alignment property value is {align_value}')
def then_the_paragraph_alignment_prop_value_is_value(context, align_value):
    expected_value = {
        'None':                      None,
        'WD_ALIGN_PARAGRAPH.LEFT':   WD_ALIGN_PARAGRAPH.LEFT,
        'WD_ALIGN_PARAGRAPH.CENTER': WD_ALIGN_PARAGRAPH.CENTER,
        'WD_ALIGN_PARAGRAPH.RIGHT':  WD_ALIGN_PARAGRAPH.RIGHT,
    }[align_value]
    assert context.paragraph.alignment == expected_value


@then('the paragraph formatting is preserved')
def then_the_paragraph_formatting_is_preserved(context):
    paragraph = context.paragraph
    assert paragraph.style.name == 'Heading 1'


@then('the paragraph has no content')
def then_the_paragraph_has_no_content(context):
    assert context.paragraph.text == ''


@then('the paragraph has the style I set')
def then_the_paragraph_has_the_style_I_set(context):
    paragraph, expected_style = context.paragraph, context.style
    assert paragraph.style == expected_style


@then('the paragraph has the text I set')
def then_the_paragraph_has_the_text_I_set(context):
    assert context.paragraph.text == 'bar\tfoo\n'


@then('the style of the second paragraph matches the style I set')
def then_the_style_of_the_second_paragraph_matches_the_style_I_set(context):
    second_paragraph = context.document.paragraphs[1]
    assert second_paragraph.style.name == 'Heading 1'


@then('the text of the second paragraph matches the text I set')
def then_the_text_of_the_second_paragraph_matches_the_text_I_set(context):
    second_paragraph = context.document.paragraphs[1]
    assert second_paragraph.text == 'foobar'
