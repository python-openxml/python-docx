"""Unit test suite for the docx.parts.hdrftr module."""

from __future__ import annotations

from typing import cast

import pytest

from docx.comments import Comments
from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.packuri import PackURI
from docx.oxml.comments import CT_Comments
from docx.package import Package
from docx.parts.comments import CommentsPart

from ..unitutil.cxml import element
from ..unitutil.mock import FixtureRequest, Mock, class_mock, instance_mock


class DescribeCommentsPart:
    """Unit test suite for `docx.parts.comments.CommentsPart` objects."""

    def it_provides_access_to_its_comments_collection(
        self, Comments_: Mock, comments_: Mock, package_: Mock
    ):
        Comments_.return_value = comments_
        comments_elm = cast(CT_Comments, element("w:comments"))
        comments_part = CommentsPart(
            PackURI("/word/comments.xml"), CT.WML_COMMENTS, comments_elm, package_
        )

        comments = comments_part.comments

        Comments_.assert_called_once_with(comments_part.element, comments_part)
        assert comments is comments_

    def it_constructs_a_default_comments_part_to_help(self):
        package = Package()

        comments_part = CommentsPart.default(package)

        assert isinstance(comments_part, CommentsPart)
        assert comments_part.partname == "/word/comments.xml"
        assert comments_part.content_type == CT.WML_COMMENTS
        assert comments_part.package is package
        assert comments_part.element.tag == (
            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}comments"
        )
        assert len(comments_part.element) == 0

    # -- fixtures --------------------------------------------------------------------------------

    @pytest.fixture
    def Comments_(self, request: FixtureRequest) -> Mock:
        return class_mock(request, "docx.parts.comments.Comments")

    @pytest.fixture
    def comments_(self, request: FixtureRequest) -> Mock:
        return instance_mock(request, Comments)

    @pytest.fixture
    def package_(self, request: FixtureRequest) -> Mock:
        return instance_mock(request, Package)
