"""Collection providing access to comments added to this document."""

from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING, Iterator

from docx.blkcntnr import BlockItemContainer

if TYPE_CHECKING:
    from docx.oxml.comments import CT_Comment, CT_Comments
    from docx.parts.comments import CommentsPart
    from docx.styles.style import ParagraphStyle
    from docx.text.paragraph import Paragraph


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

    def add_comment(self, text: str = "", author: str = "", initials: str | None = "") -> Comment:
        """Add a new comment to the document and return it.

        The comment is added to the end of the comments collection and is assigned a unique
        comment-id.

        If `text` is provided, it is added to the comment. This option provides for the common
        case where a comment contains a modest passage of plain text. Multiple paragraphs can be
        added using the `text` argument by separating their text with newlines (`"\\\\n"`).
        Between newlines, text is interpreted as it is in `Document.add_paragraph(text=...)`.

        The default is to place a single empty paragraph in the comment, which is the same
        behavior as the Word UI when you add a comment. New runs can be added to the first
        paragraph in the empty comment with `comments.paragraphs[0].add_run()` to adding more
        complex text with emphasis or images. Additional paragraphs can be added using
        `.add_paragraph()`.

        `author` is a required attribute, set to the empty string by default.

        `initials` is an optional attribute, set to the empty string by default. Passing |None|
        for the `initials` parameter causes that attribute to be omitted from the XML.
        """
        comment_elm = self._comments_elm.add_comment()
        comment_elm.author = author
        comment_elm.initials = initials
        comment_elm.date = dt.datetime.now(dt.timezone.utc)
        comment = Comment(comment_elm, self._comments_part)

        if text == "":
            return comment

        para_text_iter = iter(text.split("\n"))

        first_para_text = next(para_text_iter)
        first_para = comment.paragraphs[0]
        first_para.add_run(first_para_text)

        for s in para_text_iter:
            comment.add_paragraph(text=s)

        return comment

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

    def add_paragraph(self, text: str = "", style: str | ParagraphStyle | None = None) -> Paragraph:
        """Return paragraph newly added to the end of the content in this container.

        The paragraph has `text` in a single run if present, and is given paragraph style `style`.
        When `style` is |None| or ommitted, the "CommentText" paragraph style is applied, which is
        the default style for comments.
        """
        paragraph = super().add_paragraph(text, style)

        # -- have to assign style directly to element because `paragraph.style` raises when
        # -- a style is not present in the styles part
        if style is None:
            paragraph._p.style = "CommentText"  # pyright: ignore[reportPrivateUsage]

        return paragraph

    @property
    def author(self) -> str:
        """Read/write. The recorded author of this comment.

        This field is required but can be set to the empty string.
        """
        return self._comment_elm.author

    @author.setter
    def author(self, value: str):
        self._comment_elm.author = value

    @property
    def comment_id(self) -> int:
        """The unique identifier of this comment."""
        return self._comment_elm.id

    @property
    def initials(self) -> str | None:
        """Read/write. The recorded initials of the comment author.

        This attribute is optional in the XML, returns |None| if not set. Assigning |None| removes
        any existing initials from the XML.
        """
        return self._comment_elm.initials

    @initials.setter
    def initials(self, value: str | None):
        self._comment_elm.initials = value

    @property
    def text(self) -> str:
        """The text content of this comment as a string.

        Only content in paragraphs is included and of course all emphasis and styling is stripped.

        Paragraph boundaries are indicated with a newline (`"\\\\n"`)
        """
        return "\n".join(p.text for p in self.paragraphs)

    @property
    def timestamp(self) -> dt.datetime | None:
        """The date and time this comment was authored.

        This attribute is optional in the XML, returns |None| if not set.
        """
        return self._comment_elm.date
