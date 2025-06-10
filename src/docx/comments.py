"""Collection providing access to comments added to this document."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

from docx.blkcntnr import BlockItemContainer

if TYPE_CHECKING:
    from docx.oxml.comments import CT_Comment, CT_Comments
    from docx.parts.comments import CommentsPart


class Comments:
    """Collection containing the comments added to this document."""

    def __init__(self, comments_elm: CT_Comments, comments_part: CommentsPart):
        self._comments_elm = comments_elm
        self._comments_part = comments_part

    def __iter__(self) -> Iterator[Comment]:
        """Iterator over the comments in this collection."""
        return (
            Comment(comment_elm, self._comments_part)
            for comment_elm in self._comments_elm.comment_lst
        )

    def __len__(self) -> int:
        """The number of comments in this collection."""
        return len(self._comments_elm.comment_lst)

    def get(self, comment_id: int) -> Comment | None:
        """Return the comment identified by `comment_id`, or |None| if not found."""
        comment_elm = self._comments_elm.get_comment_by_id(comment_id)
        return Comment(comment_elm, self._comments_part) if comment_elm is not None else None


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

    def __init__(self, comment_elm: CT_Comment, comments_part: CommentsPart):
        super().__init__(comment_elm, comments_part)
        self._comment_elm = comment_elm

    @property
    def comment_id(self) -> int:
        """The unique identifier of this comment."""
        return self._comment_elm.id
