"""Unit test suite for the docx.parts.hdrftr module."""

from __future__ import annotations

from typing import cast

import pytest

from docx.comments import Comments
from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.opc.packuri import PackURI
from docx.opc.part import PartFactory
from docx.oxml.comments import CT_Comments
from docx.package import Package
from docx.parts.comments import CommentsPart

from ..unitutil.cxml import element
from ..unitutil.mock import FixtureRequest, Mock, class_mock, instance_mock, method_mock


class DescribeCommentsPart:
    """Unit test suite for `docx.parts.comments.CommentsPart` objects."""

    def it_is_used_by_the_part_loader_to_construct_a_comments_part(
        self, package_: Mock, CommentsPart_load_: Mock, comments_part_: Mock
    ):
        partname = PackURI("/word/comments.xml")
        content_type = CT.WML_COMMENTS
        reltype = RT.COMMENTS
        blob = b"<w:comments/>"
        CommentsPart_load_.return_value = comments_part_

        part = PartFactory(partname, content_type, reltype, blob, package_)

        CommentsPart_load_.assert_called_once_with(partname, content_type, blob, package_)
        assert part is comments_part_

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
    def comments_part_(self, request: FixtureRequest) -> Mock:
        return instance_mock(request, CommentsPart)

    @pytest.fixture
    def CommentsPart_load_(self, request: FixtureRequest) -> Mock:
        return method_mock(request, CommentsPart, "load", autospec=False)

    @pytest.fixture
    def package_(self, request: FixtureRequest) -> Mock:
        return instance_mock(request, Package)
