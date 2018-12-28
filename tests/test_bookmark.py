# encoding: utf-8

"""Test suite for the docx.bookmark module."""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from docx.bookmark import (
    _Bookmark,
    Bookmarks,
    _DocumentBookmarkFinder,
    _PartBookmarkFinder,
)
from docx.opc.part import Part, XmlPart
from docx.parts.document import DocumentPart

from .unitutil.cxml import element
from .unitutil.mock import (
    ANY,
    call,
    class_mock,
    initializer_mock,
    instance_mock,
    method_mock,
    property_mock,
)


class DescribeBookmarks(object):
    """Unit-test suite for `docx.bookmark.Bookmarks` object."""

    def it_provides_access_to_bookmarks_by_index(
        self, _finder_prop_, finder_, _Bookmark_, bookmark_
    ):
        bookmarkStarts = tuple(element("w:bookmarkStart") for _ in range(3))
        bookmarkEnds = tuple(element("w:bookmarkEnd") for _ in range(3))
        _finder_prop_.return_value = finder_
        finder_.bookmark_pairs = list(zip(bookmarkStarts, bookmarkEnds))
        _Bookmark_.return_value = bookmark_
        bookmarks = Bookmarks(None)

        bookmark = bookmarks[1]

        _Bookmark_.assert_called_once_with((bookmarkStarts[1], bookmarkEnds[1]))
        assert bookmark == bookmark_

    def it_provides_access_to_bookmarks_by_slice(
        self, _finder_prop_, finder_, _Bookmark_, bookmark_
    ):
        bookmarkStarts = tuple(element("w:bookmarkStart") for _ in range(4))
        bookmarkEnds = tuple(element("w:bookmarkEnd") for _ in range(4))
        _finder_prop_.return_value = finder_
        finder_.bookmark_pairs = list(zip(bookmarkStarts, bookmarkEnds))
        _Bookmark_.return_value = bookmark_
        bookmarks = Bookmarks(None)

        bookmarks_slice = bookmarks[1:3]

        assert _Bookmark_.call_args_list == [
            call((bookmarkStarts[1], bookmarkEnds[1])),
            call((bookmarkStarts[2], bookmarkEnds[2])),
        ]
        assert bookmarks_slice == [bookmark_, bookmark_]

    def it_can_iterate_its_bookmarks(
        self, _finder_prop_, finder_, _Bookmark_, bookmark_
    ):
        bookmarkStarts = tuple(element("w:bookmarkStart") for _ in range(3))
        bookmarkEnds = tuple(element("w:bookmarkEnd") for _ in range(3))
        _finder_prop_.return_value = finder_
        finder_.bookmark_pairs = list(zip(bookmarkStarts, bookmarkEnds))
        _Bookmark_.return_value = bookmark_
        bookmarks = Bookmarks(None)

        _bookmarks = list(b for b in bookmarks)

        assert _Bookmark_.call_args_list == [
            call((bookmarkStarts[0], bookmarkEnds[0])),
            call((bookmarkStarts[1], bookmarkEnds[1])),
            call((bookmarkStarts[2], bookmarkEnds[2])),
        ]
        assert _bookmarks == [bookmark_, bookmark_, bookmark_]

    def it_knows_how_many_bookmarks_the_document_contains(self, _finder_prop_, finder_):
        _finder_prop_.return_value = finder_
        finder_.bookmark_pairs = tuple((1, 2) for _ in range(42))
        bookmarks = Bookmarks(None)

        count = len(bookmarks)

        assert count == 42

    def it_provides_access_to_its_bookmark_finder_to_help(
        self, document_part_, _DocumentBookmarkFinder_, finder_
    ):
        _DocumentBookmarkFinder_.return_value = finder_
        bookmarks = Bookmarks(document_part_)

        finder = bookmarks._finder

        _DocumentBookmarkFinder_.assert_called_once_with(document_part_)
        assert finder is finder_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _Bookmark_(self, request):
        return class_mock(request, "docx.bookmark._Bookmark")

    @pytest.fixture
    def bookmark_(self, request):
        return instance_mock(request, _Bookmark)

    @pytest.fixture
    def _DocumentBookmarkFinder_(self, request):
        return class_mock(request, "docx.bookmark._DocumentBookmarkFinder")

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def finder_(self, request):
        return instance_mock(request, _DocumentBookmarkFinder)

    @pytest.fixture
    def _finder_prop_(self, request):
        return property_mock(request, Bookmarks, "_finder")


class Describe_DocumentBookmarkFinder(object):
    def it_finds_all_the_bookmark_pairs_in_the_document(
        self, pairs_fixture, _PartBookmarkFinder_
    ):
        document_part_, calls, expected_value = pairs_fixture
        document_bookmark_finder = _DocumentBookmarkFinder(document_part_)

        bookmark_pairs = document_bookmark_finder.bookmark_pairs

        document_part_.iter_story_parts.assert_called_once_with()
        assert _PartBookmarkFinder_.iter_start_end_pairs.call_args_list == calls
        assert bookmark_pairs == expected_value

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            ([[(1, 2)]], [(1, 2)]),
            ([[(1, 2), (3, 4), (5, 6)]], [(1, 2), (3, 4), (5, 6)]),
            ([[(1, 2)], [(3, 4)], [(5, 6)]], [(1, 2), (3, 4), (5, 6)]),
            (
                [[(1, 2), (3, 4)], [(5, 6), (7, 8)], [(9, 10)]],
                [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)],
            ),
        ]
    )
    def pairs_fixture(self, request, document_part_, _PartBookmarkFinder_):
        parts_pairs, expected_value = request.param
        mock_parts = [
            instance_mock(request, Part, name="Part-%d" % idx)
            for idx, part_pairs in enumerate(parts_pairs)
        ]
        calls = [call(part_) for part_ in mock_parts]

        document_part_.iter_story_parts.return_value = (p for p in mock_parts)
        _PartBookmarkFinder_.iter_start_end_pairs.side_effect = parts_pairs

        return document_part_, calls, expected_value

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _PartBookmarkFinder_(self, request):
        return class_mock(request, "docx.bookmark._PartBookmarkFinder")

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)


class Describe_PartBookmarkFinder(object):
    """Unit tests for _PartBookmarkFinder class"""

    def it_provides_an_iter_start_end_pairs_interface_method(
        self, part_, _init_, _iter_start_end_pairs_
    ):
        pairs = _PartBookmarkFinder.iter_start_end_pairs(part_)

        _init_.assert_called_once_with(ANY, part_)
        _iter_start_end_pairs_.assert_called_once_with(ANY)
        assert pairs == _iter_start_end_pairs_.return_value

    def it_gathers_all_the_bookmark_start_and_end_elements_to_help(self, part_):
        body = element("w:body/(w:bookmarkStart,w:p,w:bookmarkEnd,w:p,w:bookmarkStart)")
        part_.element = body
        finder = _PartBookmarkFinder(part_)

        starts_and_ends = finder._all_starts_and_ends

        assert starts_and_ends == [body[0], body[2], body[4]]

    def it_iterates_start_end_pairs_to_help(
        self, _iter_starts_, _matching_end_, _name_already_used_
    ):
        bookmarkStarts = tuple(
            element("w:bookmarkStart{w:name=%s,w:id=%d}" % (name, idx))
            for idx, name in enumerate(("bmk-0", "bmk-1", "bmk-2", "bmk-1"))
        )
        bookmarkEnds = (
            None,
            element("w:bookmarkEnd{w:id=1}"),
            element("w:bookmarkEnd{w:id=2}"),
        )
        _iter_starts_.return_value = iter(enumerate(bookmarkStarts))
        _matching_end_.side_effect = (
            None,
            bookmarkEnds[1],
            bookmarkEnds[2],
            bookmarkEnds[1],
        )
        _name_already_used_.side_effect = (False, False, True)
        finder = _PartBookmarkFinder(None)

        start_end_pairs = list(finder._iter_start_end_pairs())

        assert _matching_end_.call_args_list == [
            call(finder, bookmarkStarts[0], 0),
            call(finder, bookmarkStarts[1], 1),
            call(finder, bookmarkStarts[2], 2),
            call(finder, bookmarkStarts[3], 3),
        ]
        assert _name_already_used_.call_args_list == [
            call(finder, "bmk-1"),
            call(finder, "bmk-2"),
            call(finder, "bmk-1"),
        ]
        assert start_end_pairs == [
            (bookmarkStarts[1], bookmarkEnds[1]),
            (bookmarkStarts[2], bookmarkEnds[2]),
        ]

    def it_iterates_bookmarkStart_elements_to_help(self, _all_starts_and_ends_prop_):
        starts_and_ends = (
            element("w:bookmarkStart"),
            element("w:bookmarkEnd"),
            element("w:bookmarkStart"),
            element("w:bookmarkEnd"),
            element("w:bookmarkStart"),
            element("w:bookmarkEnd"),
        )
        _all_starts_and_ends_prop_.return_value = list(starts_and_ends)
        finder = _PartBookmarkFinder(None)

        starts = list(finder._iter_starts())

        assert starts == [
            (0, starts_and_ends[0]),
            (2, starts_and_ends[2]),
            (4, starts_and_ends[4]),
        ]

    def it_finds_the_matching_end_for_a_start_to_help(
        self, matching_end_fixture, _all_starts_and_ends_prop_
    ):
        starts_and_ends, start_idx, expected_value = matching_end_fixture
        _all_starts_and_ends_prop_.return_value = starts_and_ends
        bookmarkStart = starts_and_ends[start_idx]
        finder = _PartBookmarkFinder(None)

        bookmarkEnd = finder._matching_end(bookmarkStart, start_idx)

        assert bookmarkEnd == expected_value

    def it_knows_whether_a_bookmark_name_was_already_used(
        self, name_used_fixture, _names_so_far_prop_, names_so_far_
    ):
        name, is_used, calls, expected_value = name_used_fixture
        _names_so_far_prop_.return_value = names_so_far_
        names_so_far_.__contains__.return_value = is_used
        finder = _PartBookmarkFinder(None)

        already_used = finder._name_already_used(name)

        assert names_so_far_.add.call_args_list == calls
        assert already_used is expected_value

    def it_composes_a_set_in_which_to_track_used_bookmark_names(self):
        finder = _PartBookmarkFinder(None)
        names_so_far = finder._names_so_far
        assert names_so_far == set()

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            # ---no subsequent end---
            ([element("w:bookmarkStart{w:name=foo,w:id=0}")], 0, None),
            # ---no matching end---
            (
                [element("w:bookmarkStart{w:id=0}"), element("w:bookmarkEnd{w:id=1}")],
                0,
                None,
            ),
            # ---end immediately follows start---
            (
                [element("w:bookmarkStart{w:id=0}"), element("w:bookmarkEnd{w:id=0}")],
                0,
                1,
            ),
            # ---end separated from start by other start---
            (
                [
                    element("w:bookmarkStart{w:name=foo,w:id=0}"),
                    element("w:bookmarkStart{w:name=bar,w:id=0}"),
                    element("w:bookmarkEnd{w:id=0}"),
                ],
                0,
                2,
            ),
            # ---end separated from start by other end---
            (
                [
                    element("w:bookmarkStart{w:name=foo,w:id=1}"),
                    element("w:bookmarkEnd{w:id=0}"),
                    element("w:bookmarkEnd{w:id=1}"),
                ],
                0,
                2,
            ),
        ]
    )
    def matching_end_fixture(self, request):
        starts_and_ends, start_idx, end_idx = request.param
        expected_value = None if end_idx is None else starts_and_ends[end_idx]
        return starts_and_ends, start_idx, expected_value

    @pytest.fixture(params=[(True, True), (False, False)])
    def name_used_fixture(self, request):
        is_used, expected_value = request.param
        name = "George"
        calls = [] if is_used else [call("George")]
        return name, is_used, calls, expected_value

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _all_starts_and_ends_prop_(self, request):
        return property_mock(request, _PartBookmarkFinder, "_all_starts_and_ends")

    @pytest.fixture
    def _init_(self, request):
        return initializer_mock(request, _PartBookmarkFinder)

    @pytest.fixture
    def _iter_start_end_pairs_(self, request):
        return method_mock(request, _PartBookmarkFinder, "_iter_start_end_pairs")

    @pytest.fixture
    def _iter_starts_(self, request):
        return method_mock(request, _PartBookmarkFinder, "_iter_starts")

    @pytest.fixture
    def _matching_end_(self, request):
        return method_mock(request, _PartBookmarkFinder, "_matching_end")

    @pytest.fixture
    def _name_already_used_(self, request):
        return method_mock(request, _PartBookmarkFinder, "_name_already_used")

    @pytest.fixture
    def _names_so_far_prop_(self, request):
        return property_mock(request, _PartBookmarkFinder, "_names_so_far")

    @pytest.fixture
    def names_so_far_(self, request):
        return instance_mock(request, set)

    @pytest.fixture
    def part_(self, request):
        return instance_mock(request, XmlPart)
