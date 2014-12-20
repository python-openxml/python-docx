# encoding: utf-8

"""
Provides StylesPart and related objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..opc.part import XmlPart
from ..styles.styles import Styles


class StylesPart(XmlPart):
    """
    Proxy for the styles.xml part containing style definitions for a document
    or glossary.
    """
    @classmethod
    def default(cls, package):
        """
        Return a newly created styles part, containing a default set of
        elements.
        """
        raise NotImplementedError

    @classmethod
    def new(cls):
        """
        Return newly created empty styles part, containing only the root
        ``<w:styles>`` element.
        """
        raise NotImplementedError

    @property
    def styles(self):
        """
        The |_Styles| instance containing the styles (<w:style> element
        proxies) for this styles part.
        """
        return Styles(self.element)
