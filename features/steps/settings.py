# encoding: utf-8

"""
Step implementations for document settings-related features
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from behave import given, then

from docx import Document
from docx.settings import Settings

from helpers import test_docx, tri_state_vals


# given ====================================================

@given('a document having a settings part')
def given_a_document_having_a_settings_part(context):
    context.document = Document(test_docx('doc-word-default-blank'))


@given('a document having no settings part')
def given_a_document_having_no_settings_part(context):
    context.document = Document(test_docx('set-no-settings-part'))


@given('a settings having a even and odd headers settings')
def given_a_even_and_odd_headers_settings(context):
    context.document = Document(test_docx('have_a_even_and_odd_header_settings'))

@given('a settings having no even and odd headers settings')
def given_no_even_and_odd_headers_settings(context):
    context.document = Document(test_docx('have_no_even_and_odd_header_settings'))


# then =====================================================

@then('document.settings is a Settings object')
def then_document_settings_is_a_Settings_object(context):
    document = context.document
    assert type(document.settings) is Settings

@then('document.settings.even_and_odd_headers is {value}')
def then_document_settings_even_and_odd_header_is_value(context, value):
    document, expected_value = context.document, tri_state_vals[value]
    assert document.settings.odd_and_even_pages_header_footer is expected_value