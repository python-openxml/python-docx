# encoding: utf-8

"""Test suite for the docx.bookmark module."""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.bookmark import Bookmarks, _DocumentBookmarkFinder
from docx.parts.document import DocumentPart

from .unitutil.mock import class_mock, instance_mock, property_mock


class DescribeBookmarks(object):

    def it_knows_how_many_bookmarks_the_document_contains(
            self, _finder_prop_, finder_):
        _finder_prop_.return_value = finder_
        finder_.bookmark_pairs = tuple((1, 2) for _ in range(42))
        bookmarks = Bookmarks(None)

        count = len(bookmarks)

        assert count == 42

    def it_provides_access_to_its_bookmark_finder_to_help(
            self, document_part_, _DocumentBookmarkFinder_, finder_):
        _DocumentBookmarkFinder_.return_value = finder_
        bookmarks = Bookmarks(document_part_)

        finder = bookmarks._finder

        _DocumentBookmarkFinder_.assert_called_once_with(document_part_)
        assert finder is finder_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _DocumentBookmarkFinder_(self, request):
        return class_mock(request, 'docx.bookmark._DocumentBookmarkFinder')

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def finder_(self, request):
        return instance_mock(request, _DocumentBookmarkFinder)

    @pytest.fixture
    def _finder_prop_(self, request):
        return property_mock(request, Bookmarks, '_finder')
