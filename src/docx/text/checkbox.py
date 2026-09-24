# pyright: reportPrivateUsage=false

"""Public proxy for a clickable Word check box content control."""

from __future__ import annotations

from lxml.etree import _Element

from docx.oxml.text.checkbox import checkbox_checked, set_checkbox_checked
from docx.shared import StoryChild


class CheckBox(StoryChild):
    """A clickable check box inside a paragraph."""

    def __init__(self, sdt: _Element, parent: StoryChild):
        super().__init__(parent)
        self._element = sdt

    @property
    def checked(self) -> bool:
        """Whether this check box is checked."""
        return checkbox_checked(self._element)

    @checked.setter
    def checked(self, value: bool) -> None:
        if not isinstance(value, bool):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("checked must be a bool")
        set_checkbox_checked(self._element, value)
