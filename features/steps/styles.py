# encoding: utf-8

"""
Step implementations for styles-related features
"""

from behave import given, then, when

from docx import Document
from docx.styles.styles import Styles
from docx.styles.style import BaseStyle

from helpers import test_docx


# given ===================================================

@given('a document having a styles part')
def given_a_document_having_a_styles_part(context):
    docx_path = test_docx('sty-having-styles-part')
    context.document = Document(docx_path)


@given('a document having no styles part')
def given_a_document_having_no_styles_part(context):
    docx_path = test_docx('sty-having-no-styles-part')
    context.document = Document(docx_path)


# when ====================================================

@when('I get the styles part from the document')
def when_get_styles_part_from_document(context):
    document = context.document
    context.styles_part = document.styles_part


# then =====================================================

@then('I can access a style by its UI name')
def then_I_can_access_a_style_by_its_UI_name(context):
    styles = context.document.styles
    style = styles['Default Paragraph Font']
    assert isinstance(style, BaseStyle)


@then('I can access a style by style id')
def then_I_can_access_a_style_by_style_id(context):
    styles = context.document.styles
    style = styles['DefaultParagraphFont']
    assert isinstance(style, BaseStyle)


@then('I can access the document styles collection')
def then_I_can_access_the_document_styles_collection(context):
    document = context.document
    styles = document.styles
    assert isinstance(styles, Styles)


@then('I can iterate over its styles')
def then_I_can_iterate_over_its_styles(context):
    styles = [s for s in context.document.styles]
    assert len(styles) > 0
    assert all(isinstance(s, BaseStyle) for s in styles)


@then('len(styles) is {style_count_str}')
def then_len_styles_is_style_count(context, style_count_str):
    assert len(context.document.styles) == int(style_count_str)


@then('the styles part has the expected number of style definitions')
def then_styles_part_has_expected_number_of_style_definitions(context):
    styles_part = context.styles_part
    assert len(styles_part.styles) == 6
