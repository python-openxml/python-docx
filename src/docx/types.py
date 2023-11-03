"""Abstract types used by `python-docx`."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import Protocol

if TYPE_CHECKING:
    from docx.opc.part import XmlPart
    from docx.parts.story import StoryPart


class ProvidesStoryPart(Protocol):
    """An object that provides access to the StoryPart.

    This type is for objects that have a story part like document or header as their
    root part.
    """

    @property
    def part(self) -> StoryPart:
        ...


class ProvidesXmlPart(Protocol):
    """An object that provides access to its XmlPart.

    This type is for objects that need access to their part but it either isn't a
    StoryPart or they don't care, possibly because they just need access to the package
    or related parts.
    """

    @property
    def part(self) -> XmlPart:
        ...
