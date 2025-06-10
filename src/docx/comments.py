"""Collection providing access to comments added to this document."""

from __future__ import annotations

from docx.blkcntnr import BlockItemContainer


class Comments:
    """Collection containing the comments added to this document."""


class Comment(BlockItemContainer):
    """Proxy for a single comment in the document.

    Provides methods to access comment metadata such as author, initials, and date.

    A comment is also a block-item container, similar to a table cell, so it can contain both
    paragraphs and tables and its paragraphs can contain rich text, hyperlinks and images,
    although the common case is that a comment contains a single paragraph of plain text like a
    sentence or phrase.

    Note that certain content like tables may not be displayed in the Word comment sidebar due to
    space limitations. Such "over-sized" content can still be viewed in the review pane.
    """
