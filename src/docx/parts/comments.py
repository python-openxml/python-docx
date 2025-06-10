"""Contains comments added to the document."""

from __future__ import annotations

from docx.comments import Comments
from docx.parts.story import StoryPart


class CommentsPart(StoryPart):
    """Container part for comments added to the document."""

    @property
    def comments(self) -> Comments:
        """A |Comments| proxy object for the `w:comments` root element of this part."""
        raise NotImplementedError
