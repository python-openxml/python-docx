# encoding: utf-8

"""Header and footer part objects"""

from __future__ import absolute_import, division, print_function, unicode_literals

from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.part import XmlPart
from docx.oxml import parse_xml


class HeaderPart(XmlPart):
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
        raise NotImplementedError
