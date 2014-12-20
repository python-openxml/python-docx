# encoding: utf-8

"""
Step implementations for styles-related features
"""

from behave import given, then, when

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
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


@given('a style having a known style id')
def given_a_style_having_a_known_style_id(context):
    docx_path = test_docx('sty-having-styles-part')
    document = Document(docx_path)
    context.style = document.styles['Normal']


@given('a style having a known type')
def given_a_style_having_a_known_type(context):
    docx_path = test_docx('sty-having-styles-part')
    document = Document(docx_path)
    context.style = document.styles['Normal']


# when =====================================================

@when('I assign a new value to style.style_id')
def when_I_assign_a_new_value_to_style_style_id(context):
    context.style.style_id = 'Foo42'


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


@then('style.style_id is the {which} style id')
def then_style_style_id_is_the_which_style_id(context, which):
    expected_style_id = {
        'known': 'Normal',
        'new':   'Foo42',
    }[which]
    style = context.style
    assert style.style_id == expected_style_id


@then('style.type is the known type')
def then_style_type_is_the_known_type(context):
    style = context.style
    assert style.type == WD_STYLE_TYPE.PARAGRAPH
