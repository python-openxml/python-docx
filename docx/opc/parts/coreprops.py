# encoding: utf-8

"""
Core properties part, corresponds to ``/docProps/core.xml`` part in package.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from datetime import datetime

from ..constants import CONTENT_TYPE as CT
from ..coreprops import CoreProperties
from ...oxml.coreprops import CT_CoreProperties
from ..packuri import PackURI
from ..part import XmlPart


class CorePropertiesPart(XmlPart):
    """
    Corresponds to part named ``/docProps/core.xml``, containing the core
    document properties for this document package.
    """
    @classmethod
    def default(cls, package):
        """
        Return a new |CorePropertiesPart| object initialized with default
        values for its base properties.
        """
        core_properties_part = cls._new(package)
        core_properties = core_properties_part.core_properties
        core_properties.title = 'Word Document'
        core_properties.last_modified_by = 'python-docx'
        core_properties.revision = 1
        core_properties.modified = datetime.utcnow()
        return core_properties_part

    @property
    def core_properties(self):
        """
        A |CoreProperties| object providing read/write access to the core
        properties contained in this core properties part.
        """
        return CoreProperties(self.element)

    @classmethod
    def _new(cls, package):
        partname = PackURI('/docProps/core.xml')
        content_type = CT.OPC_CORE_PROPERTIES
        coreProperties = CT_CoreProperties.new()
        return CorePropertiesPart(
            partname, content_type, coreProperties, package
        )
