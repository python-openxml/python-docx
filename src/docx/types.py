"""Abstract types used by `python-docx`."""

from __future__ import annotations

from typing_extensions import Protocol

from docx.parts.story import StoryPart


class AbstractSimpleTypeMember(Protocol):
    """A simple-type member is a valid value for a simple-type.

    The name *simple-type* comes from the ISO spec which refers to XML attribute value
    types as simple types and gives those the prefix `ST_` in the XML Schema. Many are
    enumerations but that is not strictly required.
    """


class AbstractSimpleType(Protocol):
    """A simple-type can provide XML attribute value mapping."""

    @classmethod
    def from_xml(cls, xml_value: str) -> AbstractSimpleTypeMember: ...

    @classmethod
    def to_xml(cls, value: AbstractSimpleTypeMember) -> str: ...


class StoryChild(Protocol):
    """An object that can fulfill the `parent` role in a `Parented` class.

    This type is for objects that have a story part like document or header as their
    root part.
    """

    @property
    def part(self) -> StoryPart:
        ...
