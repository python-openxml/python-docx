# encoding: utf-8
# docx\opc\parts\extendedprops.py
"""
App properties part, corresponds to ``/docProps/app.xml`` part in package.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)


from ..constants import CONTENT_TYPE as CT
from ..extendedprops import ExtendedProperties
from ..part import XmlPart
from ...oxml.extendedprops import CT_ExtendedProperties
from ..packuri import PackURI


class ExtendedPropertiesPart(XmlPart):
    """
    Corresponds to part named ``/docProps/app.xml``, containing the app
    document properties for this document package.
    """
    @classmethod
    def default(cls, package):
        """
        Return a new |ExtendedPropertiesPart| object initialized with default
        values for its base properties.
        """
        extended_properties_part = cls._new(package)
        extended_properties = extended_properties_part.extended_properties
        extended_properties.total_time = '1'
        # extended_properties.pages = '1'
        # extended_properties.company = 'Company'
        # extended_properties.manager = 'Manager'
        # extended_properties.category = 'Category'
        # extended_properties.presentation_format = 'Presentation Format'
        # extended_properties.links_up_to_date = 'false'
        # extended_properties.characters = '1'
        # extended_properties.lines = '1'
        # extended_properties.paragraphs = '1'

        return extended_properties_part

    @property
    def extended_properties(self):
        """
        A |ExtendedProperties| object providing read/write access to the app
        properties contained in this app properties part.
        """
        return ExtendedProperties(self.element)

    @classmethod
    def _new(cls, package):
        partname = PackURI('/docProps/app.xml')
        content_type = CT.OFC_EXTENDED_PROPERTIES
        extended_properties = CT_ExtendedProperties.new()
        return ExtendedPropertiesPart(
            partname, content_type, extended_properties, package
        )
