# encoding: utf-8

"""Test suite for the docx.bookmark module."""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.bookmark import Bookmarks, _DocumentBookmarkFinder

from .unitutil.mock import instance_mock, property_mock


class DescribeBookmarks(object):

    def it_knows_how_many_bookmarks_the_document_contains(
            self, _finder_prop_, finder_):
        _finder_prop_.return_value = finder_
        finder_.bookmark_pairs = tuple((1, 2) for _ in range(42))
        bookmarks = Bookmarks(None)

        count = len(bookmarks)

        assert count == 42

    # fixture components ---------------------------------------------

    @pytest.fixture
    def finder_(self, request):
        return instance_mock(request, _DocumentBookmarkFinder)

    @pytest.fixture
    def _finder_prop_(self, request):
        return property_mock(request, Bookmarks, '_finder')
