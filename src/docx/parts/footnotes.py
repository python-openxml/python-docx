"""The story part owning footnote content and relationships."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from typing_extensions import Self

from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.packuri import PackURI
from docx.oxml.ns import nsdecls
from docx.oxml.parser import parse_xml
from docx.parts.story import StoryPart

if TYPE_CHECKING:
    from docx.oxml.footnotes import CT_Footnotes
    from docx.package import Package


class FootnotesPart(StoryPart):
    """A typed footnotes part, also used for existing package content."""

    _element: CT_Footnotes

    @classmethod
    def default(cls, package: Package) -> Self:
        """Create a part containing the two standard separator notes."""
        element = cast(
            "CT_Footnotes",
            parse_xml(
                f"<w:footnotes {nsdecls('w')}>"
                '<w:footnote w:type="separator" w:id="-1">'
                "<w:p><w:r><w:separator/></w:r></w:p></w:footnote>"
                '<w:footnote w:type="continuationSeparator" w:id="0">'
                "<w:p><w:r><w:continuationSeparator/></w:r></w:p></w:footnote>"
                "</w:footnotes>"
            ),
        )
        partname = package.next_partname("/word/footnotes%d.xml")
        return cls(PackURI(partname), CT.WML_FOOTNOTES, element, package)
