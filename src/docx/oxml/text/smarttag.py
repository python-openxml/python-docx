"""Custom element classes related to smart tags (CT_SmartTag)."""

from __future__ import annotations

from docx.oxml.xmlchemy import BaseOxmlElement


class CT_SmartTag(BaseOxmlElement):
    """`<w:smartTag>` element, a legacy inline wrapper for runs.

    A smart tag wraps runs whose content was filled in from an external source
    (e.g. a database or XML file) when the document was generated. Any runs it
    contains are part of the paragraph text, just like runs inside a
    `w:hyperlink`.
    """

    @property
    def text(self) -> str:
        """The textual content of this smart tag.

        `CT_SmartTag` stores its content as `w:r` children, possibly nested
        inside further `w:smartTag` elements.
        """
        return "".join(e.text for e in self.xpath("w:r | w:smartTag"))
