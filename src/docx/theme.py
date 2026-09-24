"""Document theme font scheme."""

from __future__ import annotations

from typing import TYPE_CHECKING

from docx.oxml.ns import qn

if TYPE_CHECKING:
    from lxml.etree import _Element  # pyright: ignore[reportPrivateUsage]


class ThemeFonts:
    """The font scheme used by theme references in a document.

    Accessed through :attr:`.Document.theme_fonts`. Changing a typeface does not
    change styles or runs. Only text already referring to that theme slot follows
    the change. East Asian, complex-script, and supplemental fonts are preserved.
    """

    def __init__(self, element: _Element):
        self._element = element
        # Validate before any setters can partially update an incomplete scheme.
        self._latin("major")
        self._latin("minor")

    @property
    def name(self) -> str:
        """Read/write font scheme name shown in the application's theme settings."""
        return self._element.get("name", "")

    @name.setter
    def name(self, value: str) -> None:
        self._element.set("name", value)

    @property
    def major_latin(self) -> str:
        """Read/write Latin typeface for the major (heading) theme font."""
        return self._latin("major").get("typeface", "")

    @major_latin.setter
    def major_latin(self, value: str) -> None:
        self._set_latin("major", value)

    @property
    def minor_latin(self) -> str:
        """Read/write Latin typeface for the minor (body) theme font."""
        return self._latin("minor").get("typeface", "")

    @minor_latin.setter
    def minor_latin(self, value: str) -> None:
        self._set_latin("minor", value)

    def _latin(self, role: str) -> _Element:
        latin = self._element.find(f"{qn(f'a:{role}Font')}/{qn('a:latin')}")
        if latin is None:
            raise ValueError(f"theme font scheme is missing the {role} Latin font")
        return latin

    def _set_latin(self, role: str, value: object) -> None:
        if not isinstance(value, str):
            raise TypeError("theme typeface must be a string")
        latin = self._latin(role)
        latin.set("typeface", value)
        # These optional metrics describe the previous typeface.
        for attribute in ("panose", "pitchFamily", "charset"):
            latin.attrib.pop(attribute, None)
