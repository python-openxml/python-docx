# pyright: reportPrivateUsage=false

"""Public list instances using numbering already defined by a template."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, cast
from uuid import uuid4

from lxml.etree import _Element

from docx.enum.style import WD_STYLE_TYPE
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml.ns import qn
from docx.oxml.numbering import CT_Num, CT_Numbering, CT_NumLvl
from docx.oxml.parser import OxmlElement
from docx.oxml.text.parfmt import CT_Ind, CT_PPr, CT_TabStops
from docx.parts.numbering import NumberingPart
from docx.shared import Length
from docx.styles.style import ParagraphStyle

if TYPE_CHECKING:
    from docx.document import Document
    from docx.parts.document import DocumentPart
    from docx.text.paragraph import Paragraph


class ListInstance:
    """An independent numbering sequence based on an existing paragraph style.

    Create with :meth:`Document.add_list`. Apply the same instance to successive
    paragraphs to continue its numbering, including after intervening content.
    Paragraph styles and direct formatting are not changed by :meth:`apply`.
    """

    @classmethod
    def _from_style(
        cls, document: Document, style: object, start: int, level: int | None
    ) -> ListInstance:
        _validate_start(start)
        _validate_level(level)
        styles = document.styles
        if isinstance(style, str):
            style = styles[style]
        if not isinstance(style, ParagraphStyle) or style.type != WD_STYLE_TYPE.PARAGRAPH:
            raise ValueError("style must be a paragraph style")
        if style.element.getparent() is not styles.element:
            raise ValueError("style must belong to this document")
        chain = _style_chain(style)
        num_id = None
        inherited_level = None
        for ancestor in chain:
            ppr = cast("CT_PPr | None", ancestor.element.find(qn("w:pPr")))
            if ppr is None or ppr.numPr is None:
                continue
            if ppr.numPr.numId is not None:
                num_id = ppr.numPr.numId.val
            if ppr.numPr.ilvl is not None:
                inherited_level = ppr.numPr.ilvl.val
        if not num_id:
            raise ValueError("style must reference an existing numbering definition")
        try:
            numbering = cast(
                CT_Numbering,
                cast(NumberingPart, document.part.part_related_by(RT.NUMBERING)).element,
            )
            source = numbering.num_having_numId(num_id)
            abstract_id = source.abstractNumId.val
            abstract = numbering.xpath(f'./w:abstractNum[@w:abstractNumId="{abstract_id}"]')[0]
        except (KeyError, IndexError) as exc:
            raise ValueError("style references a missing numbering definition") from exc
        if abstract.find(qn("w:numStyleLink")) is not None:
            raise ValueError("numbering style links are not supported")
        if level is None:
            # A level's pStyle selects the level for paragraph-style numbering.
            for ancestor in reversed(chain):
                matches = abstract.findall(qn("w:lvl") + "/" + qn("w:pStyle"))
                match = next((p for p in matches if p.get(qn("w:val")) == ancestor.style_id), None)
                if match is not None:
                    parent = match.getparent()
                    assert parent is not None
                    level = int(parent.attrib[qn("w:ilvl")])
                    break
            if level is None:
                level = inherited_level if inherited_level is not None else 0
        instance = cls(document.part, numbering, abstract, source, level)
        instance._level(level)
        return instance.restart(start=start)

    def __init__(
        self,
        part: DocumentPart,
        numbering: CT_Numbering,
        abstract: _Element,
        num: CT_Num,
        default_level: int,
    ):
        self._part = part
        self._numbering = numbering
        self._abstract = abstract
        self._num = num
        self._default_level = default_level

    @property
    def default_level(self) -> int:
        """Zero-based level selected when the instance was created."""
        return self._default_level

    @property
    def levels(self) -> tuple[int, ...]:
        """Zero-based levels defined by this instance, from 0 through 8."""
        values = [lvl.attrib[qn("w:ilvl")] for lvl in self._abstract.findall(qn("w:lvl"))]
        values += self._num.xpath("./w:lvlOverride/w:lvl/@w:ilvl")
        return tuple(sorted({int(value) for value in values}))

    def restart(self, *, start: int = 1, level: int | None = None) -> ListInstance:
        """Return a new sequence without changing this instance or its paragraphs.

        `start` is a non-negative integer. Other level settings and template
        overrides are preserved. Nested levels follow the template's restart
        rules when a preceding level advances.
        """
        _validate_start(start)
        selected = self._select_level(level)
        # Word can share counter state across instances of one abstract definition.
        # A private copy keeps interleaved sequences independent.
        abstract = deepcopy(self._abstract)
        used = {int(value) for value in self._numbering.xpath("./w:abstractNum/@w:abstractNumId")}
        abstract_id = next(value for value in range(len(used) + 1) if value not in used)
        abstract.set(qn("w:abstractNumId"), str(abstract_id))
        nsid = abstract.find(qn("w:nsid"))
        if nsid is None:
            nsid = OxmlElement("w:nsid")
            abstract.insert(0, nsid)
        nsid.set(qn("w:val"), uuid4().hex[:8].upper())
        num = deepcopy(self._num)
        num.attrib.pop("{http://schemas.microsoft.com/office/word/2016/wordml/cid}durableId", None)
        num.abstractNumId.val = abstract_id
        num.numId = self._numbering._next_numId
        overrides = num.xpath(f'./w:lvlOverride[@w:ilvl="{selected}"]')
        override = cast(CT_NumLvl, overrides[0]) if overrides else num.add_lvlOverride(selected)
        override.get_or_add_startOverride().val = start
        successors = self._numbering.xpath("./w:num | ./w:numIdMacAtCleanup")
        if successors:
            successors[0].addprevious(abstract)
        else:
            self._numbering.append(abstract)
        self._numbering._insert_num(num)
        return ListInstance(self._part, self._numbering, abstract, num, selected)

    def apply(self, paragraph: Paragraph, *, level: int | None = None) -> None:
        """Make `paragraph` an item in this sequence at a defined level.

        Only main-document paragraphs, including table cells, are supported.
        Invalid levels and paragraphs from other stories or documents raise
        |ValueError| before the paragraph is changed.
        """
        selected = self._validate_paragraph(paragraph, level)
        numpr = paragraph._p.get_or_add_pPr().get_or_add_numPr()
        numpr.get_or_add_ilvl().val = selected
        numpr.get_or_add_numId().val = self._num.numId

    def apply_continuation(self, paragraph: Paragraph, *, level: int | None = None) -> None:
        """Make `paragraph` an unnumbered continuation aligned with item text.

        Apply the same paragraph style and desired direct formatting as the
        item before calling this method. Effective indentation and tab stops
        are copied to the paragraph, then its first-line indent is removed.
        This is a formatting snapshot, not a live link to the previous item.
        Word has no container for a multi-paragraph list item. Placement next
        to the item remains the caller's responsibility.
        """
        selected = self._validate_paragraph(paragraph, level)
        ind, tabs = self._continuation_format(paragraph, selected)
        ppr = paragraph._p.get_or_add_pPr()
        ppr._remove_ind()
        ppr._insert_ind(ind)
        if len(tabs):
            ppr._remove_tabs()
            ppr._insert_tabs(tabs)
        numpr = ppr.get_or_add_numPr()
        numpr._remove_ilvl()
        numpr.get_or_add_numId().val = 0

    def continuation_left_indent(
        self, paragraph: Paragraph, *, level: int | None = None
    ) -> Length | None:
        """Return the left indent an unnumbered continuation would receive.

        This does not modify `paragraph`. It is useful when a table or other
        non-paragraph block must align with the text of a list item. |None|
        means no explicit left indent is supplied by the style or numbering.
        """
        selected = self._validate_paragraph(paragraph, level)
        ind, _ = self._continuation_format(paragraph, selected)
        return ind.left

    def _continuation_format(
        self, paragraph: Paragraph, selected: int
    ) -> tuple[CT_Ind, CT_TabStops]:
        lvl = self._level(selected)
        sources = [s.element.find(qn("w:pPr")) for s in _style_chain(paragraph.style)]
        sources += [lvl.find(qn("w:pPr")), paragraph._p.pPr]
        ind = cast(CT_Ind, OxmlElement("w:ind"))
        tabs = cast(CT_TabStops, OxmlElement("w:tabs"))
        for source in sources:
            if source is None:
                continue
            source_ind = source.find(qn("w:ind"))
            if source_ind is not None:
                ind.attrib.update(source_ind.attrib)
            source_tabs = source.find(qn("w:tabs"))
            if source_tabs is not None:
                for tab in source_tabs:
                    for previous in list(tabs):
                        if previous.get(qn("w:pos")) == tab.get(qn("w:pos")):
                            tabs.remove(previous)
                    tabs.append(deepcopy(tab))
        for attr in ("hanging", "hangingChars", "firstLineChars"):
            ind.attrib.pop(qn(f"w:{attr}"), None)
        ind.set(qn("w:firstLine"), "0")
        return ind, tabs

    def _level(self, level: int) -> _Element:
        matches = self._num.xpath(f'./w:lvlOverride[@w:ilvl="{level}"]/w:lvl')
        if not matches:
            matches = self._abstract.findall(qn("w:lvl") + f'[@{qn("w:ilvl")}="{level}"]')
        if not matches:
            raise ValueError(f"level {level} is not defined by this list")
        return matches[0]

    def _select_level(self, level: int | None) -> int:
        _validate_level(level)
        selected = self.default_level if level is None else level
        self._level(selected)
        return selected

    def _validate_paragraph(self, paragraph: object, level: int | None) -> int:
        from docx.text.paragraph import Paragraph

        if not isinstance(paragraph, Paragraph):
            raise TypeError("paragraph must be a Paragraph")
        if paragraph.part is not self._part:
            raise ValueError("paragraph must belong to this document's main story")
        return self._select_level(level)


def _style_chain(style: ParagraphStyle | None) -> list[ParagraphStyle]:
    chain: list[ParagraphStyle] = []
    seen: set[str] = set()
    while style is not None:
        if style.style_id in seen:
            raise ValueError("paragraph style inheritance contains a cycle")
        seen.add(style.style_id)
        chain.append(style)
        base = style.base_style
        if base is not None and not isinstance(base, ParagraphStyle):
            raise ValueError("paragraph style must inherit from a paragraph style")
        style = base
    return list(reversed(chain))


def _validate_start(start: int) -> None:
    if type(start) is not int:
        raise TypeError("start must be an integer")
    if not 0 <= start <= 2147483647:
        raise ValueError("start must be between 0 and 2147483647")


def _validate_level(level: int | None) -> None:
    if level is None:
        return
    if type(level) is not int:
        raise TypeError("level must be an integer or None")
    if not 0 <= level <= 8:
        raise ValueError("level must be between 0 and 8")
