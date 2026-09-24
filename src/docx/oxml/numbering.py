"""Custom element classes related to the numbering part."""

from __future__ import annotations

from typing import Callable

from docx.oxml.parser import OxmlElement
from docx.oxml.shared import CT_DecimalNumber
from docx.oxml.simpletypes import ST_DecimalNumber
from docx.oxml.xmlchemy import (
    BaseOxmlElement,
    OneAndOnlyOne,
    RequiredAttribute,
    ZeroOrMore,
    ZeroOrOne,
)


class CT_Num(BaseOxmlElement):
    """``<w:num>`` element, which represents a concrete list definition instance, having
    a required child <w:abstractNumId> that references an abstract numbering definition
    that defines most of the formatting details."""

    abstractNumId: CT_DecimalNumber = OneAndOnlyOne("w:abstractNumId")  # pyright: ignore[reportAssignmentType]
    lvlOverride = ZeroOrMore("w:lvlOverride")
    numId: int = RequiredAttribute("w:numId", ST_DecimalNumber)  # pyright: ignore[reportAssignmentType]

    _add_lvlOverride: Callable[..., CT_NumLvl]

    def add_lvlOverride(self, ilvl: int) -> CT_NumLvl:
        """Return a newly added CT_NumLvl (<w:lvlOverride>) element having its ``ilvl``
        attribute set to `ilvl`."""
        return self._add_lvlOverride(ilvl=ilvl)

    @classmethod
    def new(cls, num_id, abstractNum_id):
        """Return a new ``<w:num>`` element having numId of `num_id` and having a
        ``<w:abstractNumId>`` child with val attribute set to `abstractNum_id`."""
        num = OxmlElement("w:num")
        num.numId = num_id
        abstractNumId = CT_DecimalNumber.new("w:abstractNumId", abstractNum_id)
        num.append(abstractNumId)
        return num


class CT_NumLvl(BaseOxmlElement):
    """``<w:lvlOverride>`` element, which identifies a level in a list definition to
    override with settings it contains."""

    get_or_add_startOverride: Callable[[], CT_DecimalNumber]

    startOverride = ZeroOrOne("w:startOverride", successors=("w:lvl",))
    ilvl = RequiredAttribute("w:ilvl", ST_DecimalNumber)

    def add_startOverride(self, val):
        """Return a newly added CT_DecimalNumber element having tagname
        ``w:startOverride`` and ``val`` attribute set to `val`."""
        return self._add_startOverride(val=val)


class CT_NumPr(BaseOxmlElement):
    """A ``<w:numPr>`` element, a container for numbering properties applied to a
    paragraph."""

    ilvl: CT_DecimalNumber | None = ZeroOrOne(
        "w:ilvl", successors=("w:numId", "w:numberingChange", "w:ins")
    )  # pyright: ignore[reportAssignmentType]
    numId: CT_DecimalNumber | None = ZeroOrOne("w:numId", successors=("w:numberingChange", "w:ins"))  # pyright: ignore[reportAssignmentType]

    get_or_add_ilvl: Callable[[], CT_DecimalNumber]
    get_or_add_numId: Callable[[], CT_DecimalNumber]
    _remove_ilvl: Callable[[], None]

    # @ilvl.setter
    # def _set_ilvl(self, val):
    #     """
    #     Get or add a <w:ilvl> child and set its ``w:val`` attribute to `val`.
    #     """
    #     ilvl = self.get_or_add_ilvl()
    #     ilvl.val = val

    # @numId.setter
    # def numId(self, val):
    #     """
    #     Get or add a <w:numId> child and set its ``w:val`` attribute to
    #     `val`.
    #     """
    #     numId = self.get_or_add_numId()
    #     numId.val = val


class CT_Numbering(BaseOxmlElement):
    """``<w:numbering>`` element, the root element of a numbering part, i.e.
    numbering.xml."""

    _insert_num: Callable[[CT_Num], CT_Num]

    num = ZeroOrMore("w:num", successors=("w:numIdMacAtCleanup",))

    def add_num(self, abstractNum_id):
        """Return a newly added CT_Num (<w:num>) element referencing the abstract
        numbering definition identified by `abstractNum_id`."""
        next_num_id = self._next_numId
        num = CT_Num.new(next_num_id, abstractNum_id)
        return self._insert_num(num)

    def num_having_numId(self, numId: int) -> CT_Num:
        """Return the ``<w:num>`` child element having ``numId`` attribute matching
        `numId`."""
        xpath = './w:num[@w:numId="%d"]' % numId
        try:
            return self.xpath(xpath)[0]
        except IndexError:
            raise KeyError("no <w:num> element with numId %d" % numId)

    @property
    def _next_numId(self) -> int:
        """The first ``numId`` unused by a ``<w:num>`` element, starting at 1 and
        filling any gaps in numbering between existing ``<w:num>`` elements."""
        numId_strs = self.xpath("./w:num/@w:numId")
        num_ids = [int(numId_str) for numId_str in numId_strs]
        for num in range(1, len(num_ids) + 2):
            if num not in num_ids:
                break
        return num
