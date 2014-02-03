# encoding: utf-8

"""
Step implementations for styles-related features
"""

from behave import given, then, when

from docx import Document

from helpers import test_docx


# given ===================================================

@given('a document having a styles part')
def given_a_document_having_a_styles_part(context):
    docx_path = test_docx('sty-having-styles-part')
    context.document = Document(docx_path)


# when ====================================================

@when('I get the styles part from the document')
def when_get_styles_part_from_document(context):
    document = context.document
    context.styles_part = document.styles_part


# then =====================================================

@then('the styles part has the expected number of style definitions')
def then_styles_part_has_expected_number_of_style_definitions(context):
    styles_part = context.styles_part
    assert len(styles_part.styles) == 4
