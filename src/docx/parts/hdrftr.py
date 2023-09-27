"""Header and footer part objects."""

import os

from docx.opc.constants import CONTENT_TYPE as CT
from docx.oxml.parser import parse_xml
from docx.parts.story import StoryPart


class FooterPart(StoryPart):
    """Definition of a section footer."""

    @classmethod
    def new(cls, package):
        """Return newly created footer part."""
        partname = package.next_partname("/word/footer%d.xml")
        content_type = CT.WML_FOOTER
        element = parse_xml(cls._default_footer_xml())
        return cls(partname, content_type, element, package)

    @classmethod
    def _default_footer_xml(cls):
        """Return bytes containing XML for a default footer part."""
        path = os.path.join(
            os.path.split(__file__)[0], "..", "templates", "default-footer.xml"
        )
        with open(path, "rb") as f:
            xml_bytes = f.read()
        return xml_bytes


class HeaderPart(StoryPart):
    """Definition of a section header."""

    @classmethod
    def new(cls, package):
        """Return newly created header part."""
        partname = package.next_partname("/word/header%d.xml")
        content_type = CT.WML_HEADER
        element = parse_xml(cls._default_header_xml())
        return cls(partname, content_type, element, package)

    @classmethod
    def _default_header_xml(cls):
        """Return bytes containing XML for a default header part."""
        path = os.path.join(
            os.path.split(__file__)[0], "..", "templates", "default-header.xml"
        )
        with open(path, "rb") as f:
            xml_bytes = f.read()
        return xml_bytes
