"""Custom element classes related to document comments."""

from __future__ import annotations

from docx.oxml.xmlchemy import BaseOxmlElement


class CT_Comments(BaseOxmlElement):
    """`w:comments` element, the root element for the comments part.

    Simply contains a collection of `w:comment` elements, each representing a single comment. Each
    contained comment is identified by a unique `w:id` attribute, used to reference the comment
    from the document text. The offset of the comment in this collection is arbitrary; it is
    essentially a _set_ implemented as a list.
    """
