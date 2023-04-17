# encoding: utf-8

"""
App properties part, corresponds to ``/docProps/app.xml`` part in package.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)


from ..constants import CONTENT_TYPE as CT
from ..extendedprops import ExtendedProperties
from ...oxml.extendedprops import CT_ExtendedProperties
from ..packuri import PackURI
from ..part import XmlPart


class ExtendedPropertiesPart(XmlPart):
    """
    Corresponds to part named ``/docProps/app.xml``, containing the app
    document properties for this document package.
    """
    @classmethod
    def default(cls, package):
        """
        Return a new |AppPropertiesPart| object initialized with default
        values for its base properties.
        """
        extended_properties_part = cls._new(package)
        extended_properties = extended_properties_part.extended_properties
        extended_properties.total_time = '1'
        # extended_properties.last_modified_by = 'python-docx'
        # extended_properties.revision = 1
        # extended_properties.modified = datetime.utc.now()

        # TODO : Fill in the values with the correct `'app'` properties
        return extended_properties_part

    @property
    def extended_properties(self):
        """
        A |AppProperties| object providing read/write access to the app
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
