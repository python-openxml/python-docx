# encoding: utf-8

"""
|HeaderFooterPart| and closely related objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..opc.constants import CONTENT_TYPE as CT
from ..opc.packuri import PackURI
from ..oxml import parse_xml

from ..opc.part import XmlPart


class _HeaderFooterPart(XmlPart):
    pass


class HeaderPart(_HeaderFooterPart):
    """
    Main header and footer part of a WordprocessingML (WML) package, aka a .docx file.
    Acts as broker to other parts such as image, core properties, and style
    parts. It also acts as a convenient delegate when a mid-document object
    needs a service involving a remote ancestor. The `Parented.part` property
    inherited by many content objects provides access to this part object for
    that purpose.
    """

    @classmethod
    def new(cls, blob, package, header_number):
        """
        Return a newly created header part, containing a default
        `w:hdr` element tree.
        """
        partname = PackURI('/word/header%s.xml' % str(header_number))
        content_type = CT.WML_HEADER
        element = parse_xml(blob)
        header_part = cls(partname, content_type, element, package)
        header_part.element.clear_content()
        return header_part


class FooterPart(_HeaderFooterPart):
    """
    Main header and footer part of a WordprocessingML (WML) package, aka a .docx file.
    Acts as broker to other parts such as image, core properties, and style
    parts. It also acts as a convenient delegate when a mid-document object
    needs a service involving a remote ancestor. The `Parented.part` property
    inherited by many content objects provides access to this part object for
    that purpose.
    """

    @classmethod
    def new(cls, blob, package, footer_number):
        """
        Return a newly created footer part, containing a default
        `w:ftr` element tree.
        """
        partname = PackURI('/word/footer%s.xml' % str(footer_number))
        content_type = CT.WML_FOOTER
        element = parse_xml(blob)
        footer_part = cls(partname, content_type, element, package)
        footer_part.element.clear_content()
        return footer_part
