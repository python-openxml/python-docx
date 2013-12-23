# encoding: utf-8

"""
Step implementations for table-related features
"""

from __future__ import absolute_import, print_function, unicode_literals

from behave import given, then, when

from docx import Document
from docx.table import (
    _Cell, _Column, _ColumnCellCollection, _ColumnCollection, _Row,
    _RowCellCollection, _RowCollection
)

from .helpers import test_docx


# given ===================================================

@given('a column cell collection having two cells')
def given_a_column_cell_collection_having_two_cells(context):
    docx_path = test_docx('blk-containing-table')
    document = Document(docx_path)
    context.cells = document.body.tables[0].columns[0].cells


@given('a column collection having two columns')
def given_a_column_collection_having_two_columns(context):
    docx_path = test_docx('blk-containing-table')
    document = Document(docx_path)
    context.columns = document.body.tables[0].columns


@given('a row cell collection having two cells')
def given_a_row_cell_collection_having_two_cells(context):
    docx_path = test_docx('blk-containing-table')
    document = Document(docx_path)
    context.cells = document.body.tables[0].rows[0].cells


@given('a row collection having two rows')
def given_a_row_collection_having_two_rows(context):
    docx_path = test_docx('blk-containing-table')
    document = Document(docx_path)
    context.rows = document.body.tables[0].rows


@given('a table')
def given_a_table(context):
    context.table_ = Document().body.add_table(rows=2, cols=2)


@given('a table having an applied style')
def given_a_table_having_an_applied_style(context):
    docx_path = test_docx('tbl-having-applied-style')
    document = Document(docx_path)
    context.table_ = document.body.tables[0]


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


@given('a table column having two cells')
def given_a_table_column_having_two_cells(context):
    docx_path = test_docx('blk-containing-table')
    document = Document(docx_path)
    context.column = document.body.tables[0].columns[0]


@given('a table row having two cells')
def given_a_table_row_having_two_cells(context):
    docx_path = test_docx('blk-containing-table')
    document = Document(docx_path)
    context.row = document.body.tables[0].rows[0]


# when =====================================================

@when('I apply a style to the table')
def when_apply_style_to_table(context):
    table = context.table_
    table.style = 'LightShading-Accent1'


# then =====================================================

@then('I can access a cell using its row and column indices')
def then_can_access_cell_using_its_row_and_col_indices(context):
    table = context.table_
    for row_idx in range(2):
        for col_idx in range(2):
            cell = table.cell(row_idx, col_idx)
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


@then('I can access a column cell by index')
def then_can_access_column_cell_by_index(context):
    cells = context.cells
    for idx in range(2):
        cell = cells[idx]
        assert isinstance(cell, _Cell)


@then('I can access a row cell by index')
def then_can_access_row_cell_by_index(context):
    cells = context.cells
    for idx in range(2):
        cell = cells[idx]
        assert isinstance(cell, _Cell)


@then('I can access the cell collection of the column')
def then_can_access_cell_collection_of_column(context):
    column = context.column
    cells = column.cells
    assert isinstance(cells, _ColumnCellCollection)


@then('I can access the cell collection of the row')
def then_can_access_cell_collection_of_row(context):
    row = context.row
    cells = row.cells
    assert isinstance(cells, _RowCellCollection)


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


@then('I can get the length of the column cell collection')
def then_can_get_length_of_column_cell_collection(context):
    column = context.column
    cells = column.cells
    assert len(cells) == 2


@then('I can get the length of the row cell collection')
def then_can_get_length_of_row_cell_collection(context):
    row = context.row
    cells = row.cells
    assert len(cells) == 2


@then('I can get the table style name')
def then_can_get_table_style_name(context):
    table = context.table_
    msg = "got '%s'" % table.style
    assert table.style == 'LightShading-Accent1', msg


@then('I can iterate over the column cells')
def then_can_iterate_over_the_column_cells(context):
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


@then('I can iterate over the row cells')
def then_can_iterate_over_the_row_cells(context):
    cells = context.cells
    actual_count = 0
    for cell in cells:
        actual_count += 1
        assert isinstance(cell, _Cell)
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


@then('the table style matches the name I applied')
def then_table_style_matches_name_applied(context):
    table = context.table_
    tmpl = "table.style doesn't match, got '%s'"
    assert table.style == 'LightShading-Accent1', tmpl % table.style
