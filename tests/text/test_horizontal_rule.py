# pyright: reportPrivateUsage=false

"""Saved-document tests for Word horizontal rules."""

from __future__ import annotations

from io import BytesIO

from docx import Document
from docx.oxml.ns import qn


def it_applies_a_bottom_border_to_an_empty_paragraph() -> None:
    document = Document()
    paragraph = document.add_paragraph()
    paragraph.add_horizontal_rule()
    stream = BytesIO()
    document.save(stream)
    stream.seek(0)

    reopened = Document(stream)
    rule = reopened.paragraphs[0]
    assert rule.text == ""
    border = rule._p.xpath("./w:pPr/w:pBdr/w:bottom")[0]
    assert {name: border.get(qn(f"w:{name}")) for name in ("val", "sz", "space", "color")} == {
        "val": "single",
        "sz": "6",
        "space": "1",
        "color": "auto",
    }


def it_preserves_existing_paragraph_properties_and_is_idempotent() -> None:
    paragraph = Document().add_paragraph(style="Quote")
    paragraph.paragraph_format.left_indent = 914400
    paragraph.add_horizontal_rule()
    paragraph.add_horizontal_rule()
    assert len(paragraph._p.xpath("./w:pPr/w:pBdr/w:bottom")) == 1
    assert paragraph.style is not None
    assert paragraph.style.name == "Quote"
    assert paragraph.paragraph_format.left_indent == 914400
