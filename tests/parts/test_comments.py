"""Unit test suite for the docx.parts.hdrftr module."""

from __future__ import annotations

from docx.opc.constants import CONTENT_TYPE as CT
from docx.package import Package
from docx.parts.comments import CommentsPart


class DescribeCommentsPart:
    """Unit test suite for `docx.parts.comments.CommentsPart` objects."""

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
