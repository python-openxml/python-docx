# encoding: utf-8

"""Step implementations for bookmark-related features."""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from behave import given, then

from docx import Document

from helpers import test_docx


# given ===================================================

@given('a Bookmarks object of length 5 as bookmarks')
def given_a_Bookmarks_object_of_length_5_as_bookmarks(context):
    document = Document(test_docx('bmk-bookmarks'))
    context.bookmarks = document.bookmarks


# then =====================================================

@then('bookmarks[{idx}] is a _Bookmark object')
def then_bookmarks_idx_is_a_Bookmark_object(context, idx):
    item = context.bookmarks[int(idx)]
    expected = '_Bookmark'
    actual = item.__class__.__name__
    assert actual == expected, 'bookmarks[%s] is a %s object' % (idx, actual)


@then('iterating bookmarks produces {n} _Bookmark objects')
def then_iterating_bookmarks_produces_n_Bookmark_objects(context, n):
    items = [item for item in context.bookmarks]
    assert len(items) == int(n)
    assert all(item.__class__.__name__ == '_Bookmark' for item in items)


@then('len(bookmarks) == {count}')
def then_len_bookmarks_eq_count(context, count):
    expected = int(count)
    actual = len(context.bookmarks)
    assert actual == expected, 'len(bookmarks) == %s' % actual
