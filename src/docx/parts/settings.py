"""|SettingsPart| and closely related objects."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, cast

from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.packuri import PackURI
from docx.opc.part import XmlPart
from docx.oxml.parser import parse_xml
from docx.settings import Settings

if TYPE_CHECKING:
    from docx.oxml.settings import CT_Settings
    from docx.package import Package


class SettingsPart(XmlPart):
    """Document-level settings part of a WordprocessingML (WML) package."""

    def __init__(
        self, partname: PackURI, content_type: str, element: CT_Settings, package: Package
    ):
        super().__init__(partname, content_type, element, package)
        self._settings = element

    @classmethod
    def default(cls, package: Package):
        """Return a newly created settings part, containing a default `w:settings` element tree."""
        partname = PackURI("/word/settings.xml")
        content_type = CT.WML_SETTINGS
        element = cast("CT_Settings", parse_xml(cls._default_settings_xml()))
        return cls(partname, content_type, element, package)

    @property
    def settings(self) -> Settings:
        """A |Settings| proxy object for the `w:settings` element in this part.

        Contains the document-level settings for this document.
        """
        return Settings(self._settings)

    @classmethod
    def _default_settings_xml(cls):
        """Return a bytestream containing XML for a default settings part."""
        path = os.path.join(os.path.split(__file__)[0], "..", "templates", "default-settings.xml")
        with open(path, "rb") as f:
            xml_bytes = f.read()
        return xml_bytes
