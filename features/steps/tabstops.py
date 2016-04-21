# encoding: utf-8

"""
Step implementations for paragraph-related features
"""

from behave import given, then

from docx import Document
from docx.text.tabstops import TabStop

from helpers import test_docx


# given ===================================================

@given('a tab_stops having {count} tab stops')
def given_a_tab_stops_having_count_tab_stops(context, count):
    paragraph_idx = {'0': 0, '3': 1}[count]
    document = Document(test_docx('tab-stops'))
    paragraph_format = document.paragraphs[paragraph_idx].paragraph_format
    context.tab_stops = paragraph_format.tab_stops


# then =====================================================

@then('I can access a tab stop by index')
def then_I_can_access_a_tab_stop_by_index(context):
    tab_stops = context.tab_stops
    for idx in range(3):
        tab_stop = tab_stops[idx]
        assert isinstance(tab_stop, TabStop)


@then('I can iterate the TabStops object')
def then_I_can_iterate_the_TabStops_object(context):
    items = [ts for ts in context.tab_stops]
    assert len(items) == 3
    assert all(isinstance(item, TabStop) for item in items)


@then('len(tab_stops) is {count}')
def then_len_tab_stops_is_count(context, count):
    tab_stops = context.tab_stops
    assert len(tab_stops) == int(count)
