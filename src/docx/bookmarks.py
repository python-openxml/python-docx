# pyright: reportPrivateUsage=false

"""Named navigation destinations and main-story bookmark authoring."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Iterator, Sequence, cast

from docx.opc.part import XmlPart
from docx.oxml.ns import qn
from docx.oxml.parser import OxmlElement, parse_xml
from docx.oxml.text.paragraph import CT_P
from docx.text.paragraph import Paragraph
from docx.text.run import Run

if TYPE_CHECKING:
    from lxml.etree import _Element

    from docx.parts.document import DocumentPart


def validate_bookmark_name(name: object) -> None:
    """Validate the portable subset of Word bookmark names used for authoring."""
    if not isinstance(name, str):
        raise TypeError("bookmark name must be a string")
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,39}", name) is None:
        raise ValueError(
            "bookmark names must be 1-40 ASCII letters, digits, or underscores "
            "and cannot start with a digit"
        )


def _require_run(value: object) -> Run:
    if not isinstance(value, Run):
        raise ValueError("runs must contain Run objects")
    return value


class Bookmark:
    """A read-only bookmark name and its starting paragraph, if supported.

    Existing bookmarks outside main-story paragraphs return |None| for ``paragraph``.
    Creation and lookup are provided by :attr:`Document.bookmarks`.
    """

    def __init__(self, element: _Element, part: DocumentPart):
        self._element = element
        self._part = part

    @property
    def name(self) -> str:
        """The stored name, without normalization."""
        return self._element.attrib[qn("w:name")]

    @property
    def paragraph(self) -> Paragraph | None:
        """Main-story paragraph containing the start, or |None| for other locations."""
        if self._element.getroottree().getroot() is not self._part.element:
            return None
        for parent in self._element.iterancestors():
            if parent.tag == qn("w:p"):
                return Paragraph(cast(CT_P, parent), self._part)
        return None


class Bookmarks:
    """Bookmarks in the document package, including related Word stories.

    Existing names are read unchanged. New names use a portable Word-compatible
    subset of 1-40 ASCII letters, digits, and underscores, starting with a letter
    or underscore. Names beginning with an underscore are hidden in Word's UI.
    Duplicate names are rejected case-insensitively, never replaced.
    """

    def __init__(self, part: DocumentPart):
        self._part = part

    def __iter__(self) -> Iterator[Bookmark]:
        return (
            Bookmark(element, self._part)
            for root in self._roots()
            for element in root.iter(qn("w:bookmarkStart"))
        )

    def __len__(self) -> int:
        return sum(1 for _ in self)

    def get(self, name: str) -> Bookmark | None:
        """Return the first matching name, case-insensitively, or |None|."""
        key = name.casefold()
        return next((bookmark for bookmark in self if bookmark.name.casefold() == key), None)

    def add(
        self,
        name: str,
        *,
        paragraph: Paragraph | None = None,
        runs: Run | Sequence[Run] | None = None,
    ) -> Bookmark:
        """Create a paragraph-start target or a range around consecutive runs.

        Supply exactly one of `paragraph` or `runs`. A paragraph target is an
        empty range at the beginning of that paragraph. Run ranges must be
        consecutive direct runs of one paragraph, in order. Runs inside
        hyperlinks and ranges crossing paragraphs are not supported.

        Only body and table-cell paragraphs in this document are supported.
        Validate all arguments before adding markers. Existing markers and
        visible text are preserved. Rename and deletion are not provided.
        """
        validate_bookmark_name(name)
        if (paragraph is None) == (runs is None):
            raise ValueError("supply exactly one of paragraph or runs")
        first = last = None
        if runs is not None:
            selected = [runs] if isinstance(runs, Run) else list(runs)
            if not selected:
                raise ValueError("runs must contain at least one Run")
            selected = [_require_run(run) for run in selected]
            first, last = selected[0]._r, selected[-1]._r
            parent = first.getparent()
            if parent is None or parent.tag != qn("w:p"):
                raise ValueError("runs must be direct children of one paragraph")
            if any(
                run.part is not self._part or run._r.getparent() is not parent for run in selected
            ):
                raise ValueError("runs must belong to one paragraph in this document")
            siblings = list(parent)
            start, end = siblings.index(first), siblings.index(last)
            content = [
                element
                for element in siblings[start : end + 1]
                if element.tag not in {qn("w:bookmarkStart"), qn("w:bookmarkEnd")}
            ]
            if content != [run._r for run in selected]:
                raise ValueError("runs must be consecutive and in document order")
            paragraph = Paragraph(cast(CT_P, parent), self._part)
        if not isinstance(paragraph, Paragraph) or paragraph.part is not self._part:
            raise ValueError("paragraph must belong to this document's main story")
        if paragraph._p.getroottree().getroot() is not self._part.element:
            raise ValueError("paragraph must be attached to this document")
        used_ids: set[int] = set()
        # Reserve names and IDs in related Word XML parts as well as the body.
        # This avoids collisions with existing header, footer, or note markers.
        for root in self._roots():
            for marker in root.iter(qn("w:bookmarkStart"), qn("w:bookmarkEnd")):
                existing = marker.get(qn("w:name"))
                if existing is not None and existing.casefold() == name.casefold():
                    raise ValueError(f"bookmark name already exists: {name}")
                value = marker.get(qn("w:id"))
                if value is not None:
                    try:
                        used_ids.add(int(value))
                    except ValueError:
                        continue
        identifier = next(value for value in range(len(used_ids) + 1) if value not in used_ids)
        start_marker = OxmlElement("w:bookmarkStart")
        start_marker.set(qn("w:id"), str(identifier))
        start_marker.set(qn("w:name"), name)
        end_marker = OxmlElement("w:bookmarkEnd")
        end_marker.set(qn("w:id"), str(identifier))
        if first is not None and last is not None:
            first.addprevious(start_marker)
            last.addnext(end_marker)
        else:
            position = 1 if paragraph._p.pPr is not None else 0
            paragraph._p.insert(position, start_marker)
            paragraph._p.insert(position + 1, end_marker)
        return Bookmark(start_marker, self._part)

    def _roots(self) -> Iterator[_Element]:
        """Read Word XML without creating missing parts or changing their bytes."""
        package = self._part.package
        assert package is not None
        for part in package.parts:
            if isinstance(part, XmlPart):
                root = part.element
            elif part.content_type.startswith(
                "application/vnd.openxmlformats-officedocument.wordprocessingml."
            ) and part.content_type.endswith("+xml"):
                root = parse_xml(part.blob)
            else:
                continue
            yield root
