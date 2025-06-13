# encoding: utf-8

"""
Custom properties part, corresponds to ``/docProps/custom.xml`` part in package.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from lxml import etree

from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.customprops import CustomProperties
from docx.oxml.customprops import CT_CustomProperties
from docx.opc.packuri import PackURI
from docx.opc.part import XmlPart

# configure XML parser
parser_lookup = etree.ElementDefaultClassLookup(element=CT_CustomProperties)
ct_parser = etree.XMLParser(remove_blank_text=True)
ct_parser.set_element_class_lookup(parser_lookup)


def ct_parse_xml(xml):
    """
    Return root lxml element obtained by parsing XML character string in
    *xml*, which can be either a Python 2.x string or unicode. The custom
    parser is used, so custom element classes are produced for elements in
    *xml* that have them.
    """
    root_element = etree.fromstring(xml, ct_parser)
    return root_element


class CustomPropertiesPart(XmlPart):
    """
    Corresponds to part named ``/docProps/custom.xml``, containing the custom
    document properties for this document package.
    """
    @classmethod
    def default(cls, package):
        """
        Return a new |CustomPropertiesPart| object initialized with default
        values for its base properties.
        """
        custom_properties_part = cls._new(package)
        return custom_properties_part

    @property
    def custom_properties(self):
        """
        A |CustomProperties| object providing read/write access to the custom
        properties contained in this custom properties part.
        """
        return CustomProperties(self.element)

    @classmethod
    def load(cls, partname, content_type, blob, package):
        element = ct_parse_xml(blob)
        return cls(partname, content_type, element, package)

    @classmethod
    def _new(cls, package):
        partname = PackURI('/docProps/custom.xml')
        content_type = CT.OPC_CUSTOM_PROPERTIES
        customProperties = CT_CustomProperties.new()
        return CustomPropertiesPart(
            partname, content_type, customProperties, package
        )
