# pyright: reportPrivateUsage=false

"""Unit test suite for the docx.comments module."""

from __future__ import annotations

from typing import cast

import pytest

from docx.comments import Comment, Comments
from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.packuri import PackURI
from docx.oxml.comments import CT_Comment, CT_Comments
from docx.package import Package
from docx.parts.comments import CommentsPart

from .unitutil.cxml import element
from .unitutil.mock import FixtureRequest, Mock, instance_mock


class DescribeComments:
    """Unit-test suite for `docx.comments.Comments`."""

    @pytest.mark.parametrize(
        ("cxml", "count"),
        [
            ("w:comments", 0),
            ("w:comments/w:comment", 1),
            ("w:comments/(w:comment,w:comment,w:comment)", 3),
        ],
    )
    def it_knows_how_many_comments_it_contains(self, cxml: str, count: int, package_: Mock):
        comments_elm = cast(CT_Comments, element(cxml))
        comments = Comments(
            comments_elm,
            CommentsPart(
                PackURI("/word/comments.xml"),
                CT.WML_COMMENTS,
                comments_elm,
                package_,
            ),
        )

        assert len(comments) == count

    def it_is_iterable_over_the_comments_it_contains(self, package_: Mock):
        comments_elm = cast(CT_Comments, element("w:comments/(w:comment,w:comment)"))
        comments = Comments(
            comments_elm,
            CommentsPart(
                PackURI("/word/comments.xml"),
                CT.WML_COMMENTS,
                comments_elm,
                package_,
            ),
        )

        comment_iter = iter(comments)

        comment1 = next(comment_iter)
        assert type(comment1) is Comment, "expected a `Comment` object"
        comment2 = next(comment_iter)
        assert type(comment2) is Comment, "expected a `Comment` object"
        with pytest.raises(StopIteration):
            next(comment_iter)

    def it_can_get_a_comment_by_id(self, package_: Mock):
        comments_elm = cast(
            CT_Comments,
            element("w:comments/(w:comment{w:id=1},w:comment{w:id=2},w:comment{w:id=3})"),
        )
        comments = Comments(
            comments_elm,
            CommentsPart(
                PackURI("/word/comments.xml"),
                CT.WML_COMMENTS,
                comments_elm,
                package_,
            ),
        )

        comment = comments.get(2)

        assert type(comment) is Comment, "expected a `Comment` object"
        assert comment._comment_elm is comments_elm.comment_lst[1]

    # -- fixtures --------------------------------------------------------------------------------

    @pytest.fixture
    def package_(self, request: FixtureRequest):
        return instance_mock(request, Package)


class DescribeComment:
    """Unit-test suite for `docx.comments.Comment`."""

    def it_knows_its_comment_id(self, comments_part_: Mock):
        comment_elm = cast(CT_Comment, element("w:comment{w:id=42}"))
        comment = Comment(comment_elm, comments_part_)

        assert comment.comment_id == 42

    def it_knows_its_author(self, comments_part_: Mock):
        comment_elm = cast(CT_Comment, element("w:comment{w:id=42,w:author=Steve Canny}"))
        comment = Comment(comment_elm, comments_part_)

        assert comment.author == "Steve Canny"

    def it_knows_the_initials_of_its_author(self, comments_part_: Mock):
        comment_elm = cast(CT_Comment, element("w:comment{w:id=42,w:initials=SJC}"))
        comment = Comment(comment_elm, comments_part_)

        assert comment.initials == "SJC"

    # -- fixtures --------------------------------------------------------------------------------

    @pytest.fixture
    def comments_part_(self, request: FixtureRequest):
        return instance_mock(request, CommentsPart)
