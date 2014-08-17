# encoding: utf-8

"""
Step implementations for table cell-related features
"""

from __future__ import absolute_import, print_function, unicode_literals

from behave import given, then, when

from docx import Document


# given ===================================================

@given('a table cell')
def given_a_table_cell(context):
    table = Document().add_table(rows=2, cols=2)
    context.cell = table.cell(0, 0)


# when =====================================================

@when('I assign a string to the cell text attribute')
def when_assign_string_to_cell_text_attribute(context):
    cell = context.cell
    text = 'foobar'
    cell.text = text
    context.expected_text = text


@when('I attempt to merge the cells')
def when_I_attempt_to_merge_the_cells(context): 
    cell1 = context.cell1
    cell2 = context.cell2
    try:
        cell1.merge(cell2)
    except Exception as e:
        context.exception = e


@when('I merge the {nrows} x {ncols} topleftmost cells')
def when_I_merge_the_nrows_x_ncols_topleftmost_cells(context, nrows, ncols):
    table = context.table_
    row = int(nrows) - 1
    col = int(ncols) - 1
    try:
        table.cell(0, 0).merge(table.cell(row, col))
    except Exception as e:
        context.exception = e
        raise

# then =====================================================

@then('the cell row index value is {row_index_val}')
def then_the_cell_row_index_value_is_row_index_val(context, row_index_val):
    assert context.cell.row_index == int(row_index_val)


@then('the cell column index value is {col_index_val}')
def then_the_cell_column_index_value_is_col_index_val(context, col_index_val):
    assert context.cell.column_index == int(col_index_val)


@then('the cell contains the string I assigned')
def then_cell_contains_string_assigned(context):
    cell, expected_text = context.cell, context.expected_text
    text = cell.paragraphs[0].runs[0].text
    msg = "expected '%s', got '%s'" % (expected_text, text)
    assert text == expected_text, msg

