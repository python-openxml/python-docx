# pyright: reportPrivateUsage=false

"""Low-level elements for inline Word check box content controls."""

from __future__ import annotations

from lxml.etree import _Element

from docx.oxml.ns import qn
from docx.oxml.parser import OxmlElement


def new_checkbox(checked: bool) -> _Element:
    """Return an inline content control with a clickable Word check box."""
    sdt = OxmlElement("w:sdt")
    properties = OxmlElement("w:sdtPr")
    checkbox = OxmlElement("w14:checkbox")
    state = OxmlElement("w14:checked")
    state.set(qn("w14:val"), "1" if checked else "0")
    checkbox.append(state)
    for name, value in (("checkedState", "2612"), ("uncheckedState", "2610")):
        state_definition = OxmlElement(f"w14:{name}")
        state_definition.set(qn("w14:val"), value)
        state_definition.set(qn("w14:font"), "MS Gothic")
        checkbox.append(state_definition)
    properties.append(checkbox)
    sdt.append(properties)
    content = OxmlElement("w:sdtContent")
    run = OxmlElement("w:r")
    run_properties = OxmlElement("w:rPr")
    fonts = OxmlElement("w:rFonts")
    fonts.set(qn("w:ascii"), "MS Gothic")
    fonts.set(qn("w:hAnsi"), "MS Gothic")
    run_properties.append(fonts)
    run.append(run_properties)
    glyph = OxmlElement("w:t")
    glyph.text = "\u2612" if checked else "\u2610"
    run.append(glyph)
    content.append(run)
    sdt.append(content)
    return sdt


def checkbox_checked(sdt: _Element) -> bool:
    """Read the checked state from an inline check box content control."""
    state = sdt.find("./" + qn("w:sdtPr") + "/" + qn("w14:checkbox") + "/" + qn("w14:checked"))
    return state is not None and state.get(qn("w14:val")) in ("1", "true", "on")


def set_checkbox_checked(sdt: _Element, checked: bool) -> None:
    """Update the content control state and its visible glyph together."""
    state = sdt.find("./" + qn("w:sdtPr") + "/" + qn("w14:checkbox") + "/" + qn("w14:checked"))
    if state is None:
        raise ValueError("content control is not a check box")
    state.set(qn("w14:val"), "1" if checked else "0")
    glyph = sdt.find("./" + qn("w:sdtContent") + "/" + qn("w:r") + "/" + qn("w:t"))
    if glyph is not None:
        glyph.text = "\u2612" if checked else "\u2610"
