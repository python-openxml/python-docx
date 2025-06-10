"""Contains comments added to the document."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, cast

from typing_extensions import Self

from docx.comments import Comments
from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.packuri import PackURI
from docx.oxml.comments import CT_Comments
from docx.oxml.parser import parse_xml
from docx.package import Package
from docx.parts.story import StoryPart

if TYPE_CHECKING:
    from docx.oxml.comments import CT_Comments
    from docx.package import Package


class CommentsPart(StoryPart):
    """Container part for comments added to the document."""

    def __init__(
        self, partname: PackURI, content_type: str, element: CT_Comments, package: Package
    ):
        super().__init__(partname, content_type, element, package)
        self._comments = element

    @property
    def comments(self) -> Comments:
        """A |Comments| proxy object for the `w:comments` root element of this part."""
        return Comments(self._comments, self)

    @classmethod
    def default(cls, package: Package) -> Self:
        """A newly created comments part, containing a default empty `w:comments` element."""
        partname = PackURI("/word/comments.xml")
        content_type = CT.WML_COMMENTS
        element = cast("CT_Comments", parse_xml(cls._default_comments_xml()))
        return cls(partname, content_type, element, package)

    @classmethod
    def _default_comments_xml(cls) -> bytes:
        """A byte-string containing XML for a default comments part."""
        path = os.path.join(os.path.split(__file__)[0], "..", "templates", "default-comments.xml")
        with open(path, "rb") as f:
            xml_bytes = f.read()
        return xml_bytes
