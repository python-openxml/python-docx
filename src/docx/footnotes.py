# pyright: reportPrivateUsage=false

"""Native footnote creation and access to existing editable notes."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterator, cast

from docx.blkcntnr import BlockItemContainer
from docx.enum.style import WD_STYLE_TYPE
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml.footnotes import CT_Footnote
from docx.oxml.ns import qn
from docx.oxml.parser import OxmlElement
from docx.oxml.text.paragraph import CT_P
from docx.oxml.text.run import CT_R
from docx.parts.footnotes import FootnotesPart
from docx.text.paragraph import Paragraph
from docx.text.run import Run

if TYPE_CHECKING:
    from docx.oxml.settings import CT_Settings
    from docx.parts.document import DocumentPart
    from docx.styles.style import CharacterStyle, ParagraphStyle


class Footnotes:
    """Ordinary footnotes, excluding separator and continuation entries.

    Iteration follows part order, which need not match reference order. Reading this
    collection does not create a part. Use ``Document.add_footnote()`` to create notes.
    """

    def __init__(self, document_part: DocumentPart):
        self._document_part = document_part

    @property
    def _part(self) -> FootnotesPart | None:
        try:
            return cast(FootnotesPart, self._document_part.part_related_by(RT.FOOTNOTES))
        except KeyError:
            return None

    def __iter__(self) -> Iterator[Footnote]:
        part = self._part
        if part is not None:
            for element in part._element.footnote_lst:
                if element.type in (None, "normal"):
                    yield Footnote(element, part)

    def __len__(self) -> int:
        return sum(1 for _ in self)

    def get(self, footnote_id: int) -> Footnote | None:
        """Return the ordinary note with this ID, or |None| if absent."""
        return next((note for note in self if note.footnote_id == footnote_id), None)

    def _add(self, after: object, text: object) -> Footnote:
        """Validate and prepare the note before attaching its part or reference."""
        if not isinstance(after, Run):
            raise TypeError("after must be a Run")
        paragraph = after._r.getparent()
        container = paragraph.getparent() if paragraph is not None else None
        if (
            after.part is not self._document_part
            or not isinstance(paragraph, CT_P)
            or self._document_part.element not in paragraph.iterancestors()
            or container is None
            or container.tag not in (qn("w:body"), qn("w:tc"))
        ):
            raise ValueError("footnote references require an attached body or table-cell run")
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        styles = self._document_part.styles
        for name, kind in (
            ("Footnote Text", WD_STYLE_TYPE.PARAGRAPH),
            ("Footnote Reference", WD_STYLE_TYPE.CHARACTER),
        ):
            if name in styles and styles[name].type != kind:
                raise ValueError(f"{name} has an incompatible style type")

        part = self._part
        used = {
            int(value)
            for value in self._document_part.element.xpath(".//w:footnoteReference/@w:id")
        }
        if part is not None:
            used.update(note.id for note in part._element.footnote_lst)
        note_id = max(used | {0}) + 1
        if note_id > 2**31 - 1:
            note_id = next(i for i in range(1, len(used) + 2) if i not in used)
        element = CT_Footnote.new(note_id)
        # Text is added while detached so invalid XML characters cannot leave a note.
        first, *remaining = text.split("\n")
        element.p_lst[0].add_r().text = first
        for content in remaining:
            p = element.add_p()
            p.style = "FootnoteText"
            p.add_r().text = content
        reference = cast(CT_R, OxmlElement("w:r"))
        reference.get_or_add_rPr().style = "FootnoteReference"
        marker = OxmlElement("w:footnoteReference")
        marker.set(qn("w:id"), str(note_id))
        reference.append(marker)

        if "Footnote Text" not in styles:
            style = cast(
                "ParagraphStyle",
                styles.add_style(  # pyright: ignore[reportUnknownMemberType]
                    "Footnote Text", WD_STYLE_TYPE.PARAGRAPH, builtin=True
                ),
            )
            style.base_style = styles.default(WD_STYLE_TYPE.PARAGRAPH)
        if "Footnote Reference" not in styles:
            reference_style = cast(
                "CharacterStyle",
                styles.add_style(  # pyright: ignore[reportUnknownMemberType]
                    "Footnote Reference", WD_STYLE_TYPE.CHARACTER, builtin=True
                ),
            )
            reference_style.font.superscript = True
        if part is None:
            package = self._document_part.package
            assert package is not None
            part = FootnotesPart.default(package)
            self._document_part.relate_to(part, RT.FOOTNOTES)
            cast("CT_Settings", self._document_part.settings.element).ensure_footnote_separators()
        part._element.append(element)
        after._r.addnext(reference)
        return Footnote(element, part)


class Footnote(BlockItemContainer):
    """An editable ordinary note with native Word numbering.

    The first paragraph contains a native number marker and a space. Preserve that
    marker when editing the note. Replacing the paragraph's text removes it.
    """

    def __init__(self, element: CT_Footnote, part: FootnotesPart):
        super().__init__(element, part)
        self._footnote = element

    @property
    def footnote_id(self) -> int:
        """Read-only identifier used by reference runs."""
        return self._footnote.id

    def add_paragraph(self, text: str = "", style: str | ParagraphStyle | None = None) -> Paragraph:
        """Append a paragraph using Footnote Text unless a style is specified."""
        paragraph = super().add_paragraph(text, style)
        if style is None:
            paragraph._p.style = "FootnoteText"
        return paragraph

    @property
    def text(self) -> str:
        """Paragraph text joined by newlines, including the initial marker space."""
        return "\n".join(paragraph.text for paragraph in self.paragraphs)
