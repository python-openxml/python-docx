# encoding: utf-8

"""
|NumberingPart| and closely related objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..opc.package import Part
from ..oxml.shared import oxml_fromstring


class NumberingPart(Part):
    """
    Proxy for the numbering.xml part containing numbering definitions for
    a document or glossary.
    """
    def __init__(self, partname, content_type, element, package):
        super(NumberingPart, self).__init__(
            partname, content_type, element=element, package=package
        )

    @classmethod
    def load(cls, partname, content_type, blob, package):
        """
        Provides PartFactory interface for loading a numbering part from
        a WML package.
        """
        numbering_elm = oxml_fromstring(blob)
        numbering_part = cls(partname, content_type, numbering_elm, package)
        return numbering_part

    @classmethod
    def new(cls):
        """
        Return newly created empty numbering part, containing only the root
        ``<w:numbering>`` element.
        """
        raise NotImplementedError
