"""Custom element classes for revision tracking (tracked changes)."""

from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING, List

from docx.oxml.ns import qn
from docx.oxml.simpletypes import ST_String, XsdInt
from docx.oxml.xmlchemy import (
    BaseOxmlElement,
    OptionalAttribute,
    RequiredAttribute,
    ZeroOrMore,
    ZeroOrOne,
)

if TYPE_CHECKING:
    from docx.oxml.table import CT_Tbl
    from docx.oxml.text.paragraph import CT_P
    from docx.oxml.text.run import CT_R


class CT_TrackChange(BaseOxmlElement):
    """Base class for tracked change elements.

    This serves as the base for `w:ins`, `w:del`, and other revision tracking elements.
    Provides common attributes: `w:id`, `w:author`, and `w:date`.
    """

    id: int = RequiredAttribute("w:id", XsdInt)  # pyright: ignore[reportAssignmentType]
    author: str = RequiredAttribute("w:author", ST_String)  # pyright: ignore[reportAssignmentType]
    date: str | None = OptionalAttribute("w:date", ST_String)  # pyright: ignore[reportAssignmentType]

    @property
    def date_value(self) -> dt.datetime | None:
        """The `w:date` attribute as a datetime object, or None if not set."""
        date_str = self.date
        if date_str is None:
            return None
        try:
            return dt.datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except ValueError:
            return None

    @date_value.setter
    def date_value(self, value: dt.datetime | None):
        """Set the `w:date` attribute from a datetime object."""
        if value is None:
            date_qn = qn("w:date")
            if date_qn in self.attrib:  # pyright: ignore[reportUnknownMemberType]
                del self.attrib[date_qn]  # pyright: ignore[reportUnknownMemberType]
        else:
            self.date = value.strftime("%Y-%m-%dT%H:%M:%SZ")


class CT_RunTrackChange(CT_TrackChange):
    """`w:ins` or `w:del` element containing run-level content.

    Used for tracking insertions and deletions at the run level within a paragraph,
    or at the block level containing paragraphs and tables.
    """

    p_lst: List[CT_P]
    tbl_lst: List[CT_Tbl]
    r_lst: List[CT_R]

    p = ZeroOrMore("w:p")
    tbl = ZeroOrMore("w:tbl")
    r = ZeroOrMore("w:r")

    @property
    def inner_content_elements(self) -> List[CT_P | CT_Tbl]:
        """All `w:p` and `w:tbl` elements in this tracked change, in document order."""
        return self.xpath("./w:p | ./w:tbl")

    @property
    def run_content_elements(self) -> List[CT_R]:
        """All `w:r` elements in this tracked change, in document order."""
        return self.xpath("./w:r")


class CT_RPrChange(CT_TrackChange):
    """`w:rPrChange` element, tracking changes to run properties.

    Contains the previous run properties before the change was made.
    """

    rPr: BaseOxmlElement | None = ZeroOrOne("w:rPr")  # pyright: ignore[reportAssignmentType]


class CT_PPrChange(CT_TrackChange):
    """`w:pPrChange` element, tracking changes to paragraph properties.

    Contains the previous paragraph properties before the change was made.
    """

    pPr: BaseOxmlElement | None = ZeroOrOne("w:pPr")  # pyright: ignore[reportAssignmentType]


class CT_SectPrChange(CT_TrackChange):
    """`w:sectPrChange` element, tracking changes to section properties.

    Contains the previous section properties before the change was made.
    """

    sectPr: BaseOxmlElement | None = ZeroOrOne("w:sectPr")  # pyright: ignore[reportAssignmentType]


class CT_TblPrChange(CT_TrackChange):
    """`w:tblPrChange` element, tracking changes to table properties.

    Contains the previous table properties before the change was made.
    """

    tblPr: BaseOxmlElement | None = ZeroOrOne("w:tblPr")  # pyright: ignore[reportAssignmentType]


class CT_TcPrChange(CT_TrackChange):
    """`w:tcPrChange` element, tracking changes to table cell properties.

    Contains the previous cell properties before the change was made.
    """

    tcPr: BaseOxmlElement | None = ZeroOrOne("w:tcPr")  # pyright: ignore[reportAssignmentType]


class CT_TrPrChange(CT_TrackChange):
    """`w:trPrChange` element, tracking changes to table row properties.

    Contains the previous row properties before the change was made.
    """

    trPr: BaseOxmlElement | None = ZeroOrOne("w:trPr")  # pyright: ignore[reportAssignmentType]