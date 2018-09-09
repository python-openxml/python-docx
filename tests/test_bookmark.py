# encoding: utf-8

"""Test suite for the docx.bookmark module."""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.bookmark import Bookmarks, _DocumentBookmarkFinder
from docx.opc.part import Part
from docx.parts.document import DocumentPart

from .unitutil.mock import call, class_mock, instance_mock, property_mock


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


class Describe_DocumentBookmarkFinder(object):

    def it_finds_all_the_bookmark_pairs_in_the_document(
            self, pairs_fixture, _PartBookmarkFinder_):
        document_part_, calls, expected_value = pairs_fixture
        document_bookmark_finder = _DocumentBookmarkFinder(document_part_)

        bookmark_pairs = document_bookmark_finder.bookmark_pairs

        document_part_.iter_story_parts.assert_called_once_with()
        assert (
            _PartBookmarkFinder_.iter_start_end_pairs.call_args_list == calls
        )
        assert bookmark_pairs == expected_value

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ([[(1, 2)]],
         [(1, 2)]),
        ([[(1, 2), (3, 4), (5, 6)]],
         [(1, 2), (3, 4), (5, 6)]),
        ([[(1, 2)], [(3, 4)], [(5, 6)]],
         [(1, 2), (3, 4), (5, 6)]),
        ([[(1, 2), (3, 4)], [(5, 6), (7, 8)], [(9, 10)]],
         [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]),
    ])
    def pairs_fixture(self, request, document_part_, _PartBookmarkFinder_):
        parts_pairs, expected_value = request.param
        mock_parts = [
            instance_mock(request, Part, name='Part-%d' % idx)
            for idx, part_pairs in enumerate(parts_pairs)
        ]
        calls = [call(part_) for part_ in mock_parts]

        document_part_.iter_story_parts.return_value = (p for p in mock_parts)
        _PartBookmarkFinder_.iter_start_end_pairs.side_effect = parts_pairs

        return document_part_, calls, expected_value

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _PartBookmarkFinder_(self, request):
        return class_mock(request, 'docx.bookmark._PartBookmarkFinder')

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)
