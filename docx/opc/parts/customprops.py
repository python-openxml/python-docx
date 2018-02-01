# encoding: utf-8

"""
Custom properties part, corresponds to ``/docProps/custom.xml`` part in package.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from lxml import etree

from datetime import datetime

from ..constants import CONTENT_TYPE as CT
from ..customprops import CustomProperties
from ...oxml.customprops import CT_CustomProperties, ct_parse_xml
from ..packuri import PackURI
from ..part import XmlPart


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
        custom_properties = custom_properties_part.custom_properties
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
