"""
Footnotes and endnotes part objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os

from ..opc.constants import CONTENT_TYPE as CT
from ..opc.packuri import PackURI
from ..opc.part import XmlPart
from ..oxml import parse_xml
from ..fntent.fntent import Footnotes, Endnotes
from .story import BaseStoryPart


class FootnotesPart(BaseStoryPart):
    """
    Proxy for the footnotes.xml part containing footnote definitions for a document.
    """
    @classmethod
    def default(cls, package):
        """
        Return a newly created footnote part, containing a default set of
        elements.
        """
        partname = PackURI('/word/footnotes.xml')
        content_type = CT.WML_FOOTNOTES
        element = parse_xml(cls._default_footnotes_xml())
        return cls(partname, content_type, element, package)

    @property
    def footnotes(self):
        """
        The |_Footnotes| instance containing the footnotes (<w:footnote> element
        proxies) for this footnotes part.
        """
        return Footnotes(self.element, self)

    @classmethod
    def _default_footnotes_xml(cls):
        """
        Return a bytestream containing XML for a default footnotes part.
        """
        path = os.path.join(
            os.path.split(__file__)[0], '..', 'templates',
            'default-footnotes.xml'
        )
        with open(path, 'rb') as f:
            xml_bytes = f.read()
        return xml_bytes


class EndnotesPart(BaseStoryPart):
    """
    Proxy for the endnotes.xml part containing endnote definitions for a document.
    """
    @classmethod
    def default(cls, package):
        """
        Return a newly created endnote part, containing a default set of
        elements.
        """
        partname = PackURI('/word/endnotes.xml')
        content_type = CT.WML_FOOTNOTES
        element = parse_xml(cls._default_endnotes_xml())
        return cls(partname, content_type, element, package)

    @property
    def endnotes(self):
        """
        The |_Endnotes| instance containing the endnotes (<w:endnote> element
        proxies) for this endnotes part.
        """
        return Endnotes(self.element, self)

    @classmethod
    def _default_endnotes_xml(cls):
        """
        Return a bytestream containing XML for a default endnotes part.
        """
        path = os.path.join(
            os.path.split(__file__)[0], '..', 'templates',
            'default-endnotes.xml'
        )
        with open(path, 'rb') as f:
            xml_bytes = f.read()
        return xml_bytes
