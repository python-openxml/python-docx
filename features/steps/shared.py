# encoding: utf-8

"""
General-purpose step implementations
"""

import os

from behave import given, when, then

from docx import Document

from helpers import saved_docx_path


# given ===================================================

@given('a document')
def given_a_document(context):
    context.document = Document()


# when ====================================================

@when('I save the document')
def when_save_document(context):
    if os.path.isfile(saved_docx_path):
        os.remove(saved_docx_path)
    context.document.save(saved_docx_path)

# then ====================================================

@then('a {ex_type} exception is raised with a detailed {error_message}')
def then_an_ex_is_raised_with_err_message(context, ex_type, error_message):
    exception = context.exception
    assert type(exception).__name__ == ex_type
    assert exception.args[0] == error_message
