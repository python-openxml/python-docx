"""Unit test suite for the docx.comments module."""

from __future__ import annotations

from typing import cast

import pytest

from docx.comments import Comments
from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.packuri import PackURI
from docx.oxml.comments import CT_Comments
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

    # -- fixtures --------------------------------------------------------------------------------

    @pytest.fixture
    def package_(self, request: FixtureRequest):
        return instance_mock(request, Package)
