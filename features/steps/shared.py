"""General-purpose step implementations."""

import os

from behave import given, when

from docx import Document

from helpers import saved_docx_path

# given ===================================================


@given("a document")
def given_a_document(context):
    context.document = Document()


# when ====================================================


@when("I save the document")
def when_save_document(context):
    if os.path.isfile(saved_docx_path):
        os.remove(saved_docx_path)
    context.document.save(saved_docx_path)
