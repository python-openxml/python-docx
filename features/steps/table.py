# encoding: utf-8

"""
Step implementations for table-related features
"""

from __future__ import absolute_import, print_function, unicode_literals

from behave import given, then

from docx import Document
from docx.table import _Row

from .helpers import test_docx


# given ===================================================

@given('a table having two rows')
def given_a_table_having_two_rows(context):
    docx_path = test_docx('blk-containing-table')
    document = Document(docx_path)
    context.table_ = document.body.tables[0]


# then =====================================================

@then('the length of its row collection is 2')
def then_len_of_row_collection_is_2(context):
    rows = context.table_.rows
    assert len(rows) == 2


@then('each item in its row collection is a table row')
def then_each_item_in_row_collection_is_a_table_row(context):
    rows = context.table_.rows
    count = 0
    for item in rows:
        count += 1
        assert isinstance(item, _Row)
    assert count == 2
