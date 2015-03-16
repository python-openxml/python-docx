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

from helpers import test_docx


# given ====================================================

@given('a document having a settings part')
def given_a_document_having_a_settings_part(context):
    context.document = Document(test_docx('doc-word-default-blank'))


@given('a document having no settings part')
def given_a_document_having_no_settings_part(context):
    context.document = Document(test_docx('set-no-settings-part'))


# then =====================================================

@then('document.settings is a Settings object')
def then_document_settings_is_a_Settings_object(context):
    document = context.document
    assert type(document.settings) is Settings
