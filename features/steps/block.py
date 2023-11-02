"""Step implementations for block content containers."""

from behave import given, then, when
from behave.runner import Context

from docx import Document
from docx.table import Table

from helpers import test_docx

# given ===================================================


@given("a document containing a table")
def given_a_document_containing_a_table(context: Context):
    context.document = Document(test_docx("blk-containing-table"))


@given("a paragraph")
def given_a_paragraph(context: Context):
    context.document = Document()
    context.paragraph = context.document.add_paragraph()


# when ====================================================


@when("I add a paragraph")
def when_add_paragraph(context: Context):
    document = context.document
    context.p = document.add_paragraph()


@when("I add a table")
def when_add_table(context: Context):
    rows, cols = 2, 2
    context.document.add_table(rows, cols)


# then =====================================================


@then("I can access the table")
def then_can_access_table(context: Context):
    table = context.document.tables[-1]
    assert isinstance(table, Table)


@then("the new table appears in the document")
def then_new_table_appears_in_document(context: Context):
    table = context.document.tables[-1]
    assert isinstance(table, Table)
