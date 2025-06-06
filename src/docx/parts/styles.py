"""Provides StylesPart and related objects."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.packuri import PackURI
from docx.opc.part import XmlPart
from docx.oxml.parser import parse_xml
from docx.styles.styles import Styles

if TYPE_CHECKING:
    from docx.opc.package import OpcPackage


class StylesPart(XmlPart):
    """Proxy for the styles.xml part containing style definitions for a document or
    glossary."""

    @classmethod
    def default(cls, package: OpcPackage) -> StylesPart:
        """Return a newly created styles part, containing a default set of elements."""
        partname = PackURI("/word/styles.xml")
        content_type = CT.WML_STYLES
        element = parse_xml(cls._default_styles_xml())
        return cls(partname, content_type, element, package)

    @property
    def styles(self):
        """The |_Styles| instance containing the styles (<w:style> element proxies) for
        this styles part."""
        return Styles(self.element)

    @classmethod
    def _default_styles_xml(cls):
        """Return a bytestream containing XML for a default styles part."""
        path = os.path.join(os.path.split(__file__)[0], "..", "templates", "default-styles.xml")
        with open(path, "rb") as f:
            xml_bytes = f.read()
        return xml_bytes
