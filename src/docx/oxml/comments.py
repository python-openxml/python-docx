"""Custom element classes related to document comments."""

from __future__ import annotations

from docx.oxml.simpletypes import ST_DecimalNumber, ST_String
from docx.oxml.xmlchemy import BaseOxmlElement, OptionalAttribute, RequiredAttribute, ZeroOrMore


class CT_Comments(BaseOxmlElement):
    """`w:comments` element, the root element for the comments part.

    Simply contains a collection of `w:comment` elements, each representing a single comment. Each
    contained comment is identified by a unique `w:id` attribute, used to reference the comment
    from the document text. The offset of the comment in this collection is arbitrary; it is
    essentially a _set_ implemented as a list.
    """

    # -- type-declarations to fill in the gaps for metaclass-added methods --
    comment_lst: list[CT_Comment]

    comment = ZeroOrMore("w:comment")

    def get_comment_by_id(self, comment_id: int) -> CT_Comment | None:
        """Return the `w:comment` element identified by `comment_id`, or |None| if not found."""
        comment_elms = self.xpath(f"(./w:comment[@w:id='{comment_id}'])[1]")
        return comment_elms[0] if comment_elms else None


class CT_Comment(BaseOxmlElement):
    """`w:comment` element, representing a single comment.

    A comment is a so-called "story" and can contain paragraphs and tables much like a table-cell.
    While probably most often used for a single sentence or phrase, a comment can contain rich
    content, including multiple rich-text paragraphs, hyperlinks, images, and tables.
    """

    id: int = RequiredAttribute("w:id", ST_DecimalNumber)  # pyright: ignore[reportAssignmentType]
    author: str = RequiredAttribute("w:author", ST_String)  # pyright: ignore[reportAssignmentType]
    initials: str | None = OptionalAttribute(  # pyright: ignore[reportAssignmentType]
        "w:initials", ST_String
    )
