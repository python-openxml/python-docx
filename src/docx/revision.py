"""Provides TrackedInsertion and TrackedDeletion classes for accessing and manipulating
tracked changes (revisions) in a Word document."""

from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING, Iterator, List

from docx.oxml.ns import qn
from docx.shared import Parented

if TYPE_CHECKING:
    import docx.types as t
    from docx.oxml.revision import CT_RunTrackChange
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    from docx.text.run import Run


class TrackedChange(Parented):
    """Base class for tracked change proxy objects.

    Provides common functionality for both insertions and deletions.
    """

    def __init__(self, element: CT_RunTrackChange, parent: t.ProvidesStoryPart):
        super().__init__(parent)
        self._element = element

    @property
    def author(self) -> str:
        """The author who made this change."""
        return self._element.author

    @author.setter
    def author(self, value: str):
        self._element.author = value

    @property
    def date(self) -> dt.datetime | None:
        """The date/time when this change was made, or None if not recorded."""
        return self._element.date_value

    @date.setter
    def date(self, value: dt.datetime | None):
        self._element.date_value = value

    @property
    def revision_id(self) -> int:
        """The unique identifier for this revision."""
        return self._element.id

    @revision_id.setter
    def revision_id(self, value: int):
        self._element.id = value

    def accept(self) -> None:
        """Accept this tracked change.

        For an insertion, this removes the revision wrapper, keeping the content.
        For a deletion, this removes both the wrapper and the content.
        """
        raise NotImplementedError("Subclasses must implement accept()")

    def reject(self) -> None:
        """Reject this tracked change.

        For an insertion, this removes both the wrapper and the content.
        For a deletion, this removes the revision wrapper, keeping the content.
        """
        raise NotImplementedError("Subclasses must implement reject()")


class TrackedInsertion(TrackedChange):
    """Proxy object wrapping a `w:ins` element.

    Represents content that was inserted while track changes was enabled.
    The inserted content can be paragraphs, tables, or runs depending on context.
    """

    @property
    def is_block_level(self) -> bool:
        """True if this insertion contains block-level content (paragraphs/tables)."""
        return bool(self._element.inner_content_elements)

    @property
    def is_run_level(self) -> bool:
        """True if this insertion contains run-level content."""
        return bool(self._element.run_content_elements)

    def iter_inner_content(self) -> Iterator[Paragraph | Table]:
        """Generate Paragraph or Table objects for block-level inserted content."""
        from docx.table import Table
        from docx.text.paragraph import Paragraph

        for element in self._element.inner_content_elements:
            tag = element.tag  # pyright: ignore[reportUnknownMemberType]
            if tag == qn("w:p"):
                yield Paragraph(
                    element,
                    self._parent,  # pyright: ignore[reportArgumentType]
                )
            elif tag == qn("w:tbl"):
                yield Table(
                    element,
                    self._parent,  # pyright: ignore[reportArgumentType]
                )

    def iter_runs(self) -> Iterator[Run]:
        """Generate Run objects for run-level inserted content."""
        from docx.text.run import Run

        for r in self._element.run_content_elements:
            yield Run(r, self._parent)  # pyright: ignore[reportArgumentType]

    @property
    def paragraphs(self) -> List[Paragraph]:
        """List of paragraphs in this insertion (for block-level insertions)."""
        from docx.text.paragraph import Paragraph

        return [
            Paragraph(p, self._parent)  # pyright: ignore[reportArgumentType]
            for p in self._element.p_lst
        ]

    @property
    def runs(self) -> List[Run]:
        """List of runs in this insertion (for run-level insertions)."""
        from docx.text.run import Run

        return [
            Run(r, self._parent)  # pyright: ignore[reportArgumentType]
            for r in self._element.r_lst
        ]

    @property
    def text(self) -> str:
        """The text content of this insertion.

        For block-level insertions, returns concatenated text of all paragraphs.
        For run-level insertions, returns concatenated text of all runs.
        """
        if self.is_block_level:
            return "\n".join(p.text for p in self.paragraphs)
        return "".join(r.text for r in self.runs)

    def accept(self) -> None:
        """Accept this insertion, keeping the content but removing the revision wrapper."""
        parent = self._element.getparent()
        if parent is None:
            return

        index = list(parent).index(self._element)
        for child in reversed(list(self._element)):
            parent.insert(index, child)

        parent.remove(self._element)

    def reject(self) -> None:
        """Reject this insertion, removing both the content and the revision wrapper."""
        parent = self._element.getparent()
        if parent is not None:
            parent.remove(self._element)


class TrackedDeletion(TrackedChange):
    """Proxy object wrapping a `w:del` element.

    Represents content that was deleted while track changes was enabled.
    The deleted content is still present in the document but marked as deleted.
    """

    @property
    def is_block_level(self) -> bool:
        """True if this deletion contains block-level content (paragraphs/tables)."""
        return bool(self._element.inner_content_elements)

    @property
    def is_run_level(self) -> bool:
        """True if this deletion contains run-level content."""
        return bool(self._element.run_content_elements)

    def iter_inner_content(self) -> Iterator[Paragraph | Table]:
        """Generate Paragraph or Table objects for block-level deleted content."""
        from docx.table import Table
        from docx.text.paragraph import Paragraph

        for element in self._element.inner_content_elements:
            tag = element.tag  # pyright: ignore[reportUnknownMemberType]
            if tag == qn("w:p"):
                yield Paragraph(
                    element,
                    self._parent,  # pyright: ignore[reportArgumentType]
                )
            elif tag == qn("w:tbl"):
                yield Table(
                    element,
                    self._parent,  # pyright: ignore[reportArgumentType]
                )

    def iter_runs(self) -> Iterator[Run]:
        """Generate Run objects for run-level deleted content."""
        from docx.text.run import Run

        for r in self._element.run_content_elements:
            yield Run(r, self._parent)  # pyright: ignore[reportArgumentType]

    @property
    def paragraphs(self) -> List[Paragraph]:
        """List of paragraphs in this deletion (for block-level deletions)."""
        from docx.text.paragraph import Paragraph

        return [
            Paragraph(p, self._parent)  # pyright: ignore[reportArgumentType]
            for p in self._element.p_lst
        ]

    @property
    def runs(self) -> List[Run]:
        """List of runs in this deletion (for run-level deletions)."""
        from docx.text.run import Run

        return [
            Run(r, self._parent)  # pyright: ignore[reportArgumentType]
            for r in self._element.r_lst
        ]

    @property
    def text(self) -> str:
        """The text content of this deletion.

        For block-level deletions, returns concatenated text of all paragraphs.
        For run-level deletions, returns concatenated text of all runs.
        """
        if self.is_block_level:
            return "\n".join(p.text for p in self.paragraphs)
        return "".join(r.text for r in self.runs)

    def accept(self) -> None:
        """Accept this deletion, removing both the content and the revision wrapper."""
        parent = self._element.getparent()
        if parent is not None:
            parent.remove(self._element)

    def reject(self) -> None:
        """Reject this deletion, keeping the content but removing the revision wrapper."""
        parent = self._element.getparent()
        if parent is None:
            return

        index = list(parent).index(self._element)
        for child in reversed(list(self._element)):
            parent.insert(index, child)

        parent.remove(self._element)
