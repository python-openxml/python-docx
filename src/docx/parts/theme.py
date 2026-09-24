"""DrawingML theme part."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING
from zipfile import ZipFile

from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.oxml import serialize_part_xml
from docx.opc.part import Part
from docx.oxml.ns import qn
from docx.oxml.parser import parse_xml
from docx.shared import lazyproperty
from docx.theme import ThemeFonts

if TYPE_CHECKING:
    from lxml.etree import _Element  # pyright: ignore[reportPrivateUsage]

    from docx.package import Package


class ThemePart(Part):
    """Theme XML, parsed on demand to preserve untouched theme parts verbatim."""

    @classmethod
    def default(cls, package: Package) -> ThemePart:
        """Create a complete theme using the bundled default document."""
        path = os.path.join(os.path.dirname(__file__), "..", "templates", "default.docx")
        with ZipFile(path) as archive:
            blob = archive.read("word/theme/theme1.xml")
        return cls(package.next_partname("/word/theme/theme%d.xml"), CT.OFC_THEME, blob, package)

    @property
    def blob(self) -> bytes:
        if "_theme" in self.__dict__:
            return serialize_part_xml(self._theme)
        return super().blob

    @property
    def fonts(self) -> ThemeFonts:
        """Font scheme proxy. Raise |ValueError| for an incomplete theme."""
        scheme = self._theme.find(f"{qn('a:themeElements')}/{qn('a:fontScheme')}")
        if scheme is None:
            raise ValueError("theme is missing its font scheme")
        return ThemeFonts(scheme)

    @lazyproperty
    def _theme(self) -> _Element:
        try:
            return parse_xml(super().blob)
        except SyntaxError as exc:
            raise ValueError("theme XML is malformed") from exc
