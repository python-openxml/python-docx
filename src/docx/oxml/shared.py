"""Objects shared by modules in the docx.oxml subpackage."""

from __future__ import annotations

from typing import cast

from docx.oxml.ns import qn
from docx.oxml.parser import OxmlElement
from docx.oxml.simpletypes import ST_DecimalNumber, ST_OnOff, ST_String
from docx.oxml.xmlchemy import BaseOxmlElement, OptionalAttribute, RequiredAttribute


class CT_DecimalNumber(BaseOxmlElement):
    """Used for ``<w:numId>``, ``<w:ilvl>``, ``<w:abstractNumId>`` and several others,
    containing a text representation of a decimal number (e.g. 42) in its ``val``
    attribute."""

    val: int = RequiredAttribute("w:val", ST_DecimalNumber)  # pyright: ignore[reportAssignmentType]

    @classmethod
    def new(cls, nsptagname: str, val: int):
        """Return a new ``CT_DecimalNumber`` element having tagname `nsptagname` and
        ``val`` attribute set to `val`."""
        return OxmlElement(nsptagname, attrs={qn("w:val"): str(val)})


class CT_OnOff(BaseOxmlElement):
    """Used for `w:b`, `w:i` elements and others.

    Contains a bool-ish string in its `val` attribute, xsd:boolean plus "on" and
    "off". Defaults to `True`, so `<w:b>` for example means "bold is turned on".
    """

    val: bool = OptionalAttribute(  # pyright: ignore[reportAssignmentType]
        "w:val", ST_OnOff, default=True
    )


class CT_String(BaseOxmlElement):
    """Used for `w:pStyle` and `w:tblStyle` elements and others.

    In those cases, it containing a style name in its `val` attribute.
    """

    val: str = RequiredAttribute("w:val", ST_String)  # pyright: ignore[reportAssignmentType]

    @classmethod
    def new(cls, nsptagname: str, val: str):
        """Return a new ``CT_String`` element with tagname `nsptagname` and ``val``
        attribute set to `val`."""
        elm = cast(CT_String, OxmlElement(nsptagname))
        elm.val = val
        return elm
