# encoding: utf-8

"""
Step implementations for table-related features
"""

from __future__ import absolute_import, print_function, unicode_literals

from behave import given, then

from docx import Document
from docx.table import (
    _Cell, _CellCollection, _Column, _ColumnCollection, _Row, _RowCollection
)

from .helpers import test_docx


# given ===================================================

@given('a cell collection having two cells')
def given_a_cell_collection_having_two_cells(context):
    docx_path = test_docx('blk-containing-table')
    document = Document(docx_path)
    context.cells = document.body.tables[0].rows[0].cells


@given('a column collection having two columns')
def given_a_column_collection_having_two_columns(context):
    docx_path = test_docx('blk-containing-table')
    document = Document(docx_path)
    context.columns = document.body.tables[0].columns


@given('a row collection having two rows')
def given_a_row_collection_having_two_rows(context):
    docx_path = test_docx('blk-containing-table')
    document = Document(docx_path)
    context.rows = document.body.tables[0].rows


@given('a table having two columns')
def given_a_table_having_two_columns(context):
    docx_path = test_docx('blk-containing-table')
    document = Document(docx_path)
    # context.table is used internally by behave, underscore added
    # to distinguish this one
    context.table_ = document.body.tables[0]


@given('a table having two rows')
def given_a_table_having_two_rows(context):
    docx_path = test_docx('blk-containing-table')
    document = Document(docx_path)
    context.table_ = document.body.tables[0]


@given('a table row having two cells')
def given_a_table_row_having_two_cells(context):
    docx_path = test_docx('blk-containing-table')
    document = Document(docx_path)
    context.row = document.body.tables[0].rows[0]


# then =====================================================

@then('I can access a collection cell by index')
def then_can_access_collection_cell_by_index(context):
    cells = context.cells
    for idx in range(2):
        cell = cells[idx]
        assert isinstance(cell, _Cell)


@then('I can access a collection column by index')
def then_can_access_collection_column_by_index(context):
    columns = context.columns
    for idx in range(2):
        column = columns[idx]
        assert isinstance(column, _Column)


@then('I can access a collection row by index')
def then_can_access_collection_row_by_index(context):
    rows = context.rows
    for idx in range(2):
        row = rows[idx]
        assert isinstance(row, _Row)


@then('I can access the cell collection of the row')
def then_can_access_cell_collection_of_row(context):
    row = context.row
    cells = row.cells
    assert isinstance(cells, _CellCollection)


@then('I can access the column collection of the table')
def then_can_access_column_collection_of_table(context):
    table = context.table_
    columns = table.columns
    assert isinstance(columns, _ColumnCollection)


@then('I can access the row collection of the table')
def then_can_access_row_collection_of_table(context):
    table = context.table_
    rows = table.rows
    assert isinstance(rows, _RowCollection)


@then('I can get the length of the cell collection')
def then_can_get_length_of_cell_collection(context):
    row = context.row
    cells = row.cells
    assert len(cells) == 2


@then('I can iterate over the cell collection')
def then_can_iterate_over_cell_collection(context):
    cells = context.cells
    actual_count = 0
    for cell in cells:
        actual_count += 1
        assert isinstance(cell, _Cell)
    assert actual_count == 2


@then('I can iterate over the column collection')
def then_can_iterate_over_column_collection(context):
    columns = context.columns
    actual_count = 0
    for column in columns:
        actual_count += 1
        assert isinstance(column, _Column)
    assert actual_count == 2


@then('I can iterate over the row collection')
def then_can_iterate_over_row_collection(context):
    rows = context.rows
    actual_count = 0
    for row in rows:
        actual_count += 1
        assert isinstance(row, _Row)
    assert actual_count == 2


@then('the length of the column collection is 2')
def then_len_of_column_collection_is_2(context):
    columns = context.table_.columns
    assert len(columns) == 2


@then('the length of the row collection is 2')
def then_len_of_row_collection_is_2(context):
    rows = context.table_.rows
    assert len(rows) == 2
