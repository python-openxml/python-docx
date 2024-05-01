"""Core properties part, corresponds to ``/docProps/core.xml`` part in package."""

from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING

from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.coreprops import CoreProperties
from docx.opc.packuri import PackURI
from docx.opc.part import XmlPart
from docx.oxml.coreprops import CT_CoreProperties

if TYPE_CHECKING:
    from docx.opc.package import OpcPackage


class CorePropertiesPart(XmlPart):
    """Corresponds to part named ``/docProps/core.xml``.

    The "core" is short for "Dublin Core" and contains document metadata relatively common across
    documents of all types, not just DOCX.
    """

    @classmethod
    def default(cls, package: OpcPackage):
        """Return a new |CorePropertiesPart| object initialized with default values for
        its base properties."""
        core_properties_part = cls._new(package)
        core_properties = core_properties_part.core_properties
        core_properties.title = "Word Document"
        core_properties.last_modified_by = "python-docx"
        core_properties.revision = 1
        core_properties.modified = dt.datetime.now(dt.timezone.utc)
        return core_properties_part

    @property
    def core_properties(self):
        """A |CoreProperties| object providing read/write access to the core properties
        contained in this core properties part."""
        return CoreProperties(self.element)

    @classmethod
    def _new(cls, package: OpcPackage) -> CorePropertiesPart:
        partname = PackURI("/docProps/core.xml")
        content_type = CT.OPC_CORE_PROPERTIES
        coreProperties = CT_CoreProperties.new()
        return CorePropertiesPart(partname, content_type, coreProperties, package)
