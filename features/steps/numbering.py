# encoding: utf-8

"""
Step implementations for numbering-related features
"""

from behave import given, then, when

from docx import Document

from helpers import test_docx


# given ===================================================

@given('a document having a numbering part')
def given_a_document_having_a_numbering_part(context):
    context.document = Document(test_docx('num-having-numbering-part'))


# when ====================================================

@when('I get the numbering part from the document')
def when_get_numbering_part_from_document(context):
    document = context.document
    context.numbering_part = document.part.numbering_part


# then =====================================================

@then('the numbering part has the expected numbering definitions')
def then_numbering_part_has_expected_numbering_definitions(context):
    numbering_part = context.numbering_part
    assert len(numbering_part.numbering_definitions) == 10
