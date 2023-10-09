"""Abstract types used by `python-docx`."""

from __future__ import annotations

from typing_extensions import Protocol

from docx.parts.story import StoryPart


class StoryChild(Protocol):
    """An object that can fulfill the `parent` role in a `Parented` class.

    This type is for objects that have a story part like document or header as their
    root part.
    """

    @property
    def part(self) -> StoryPart:
        ...
