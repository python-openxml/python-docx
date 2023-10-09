"""Sub-package module for docx.styles sub-package."""

from __future__ import annotations

from typing import Dict


class BabelFish:
    """Translates special-case style names from UI name (e.g. Heading 1) to
    internal/styles.xml name (e.g. heading 1) and back."""

    style_aliases = (
        ("Caption", "caption"),
        ("Footer", "footer"),
        ("Header", "header"),
        ("Heading 1", "heading 1"),
        ("Heading 2", "heading 2"),
        ("Heading 3", "heading 3"),
        ("Heading 4", "heading 4"),
        ("Heading 5", "heading 5"),
        ("Heading 6", "heading 6"),
        ("Heading 7", "heading 7"),
        ("Heading 8", "heading 8"),
        ("Heading 9", "heading 9"),
    )

    internal_style_names: Dict[str, str] = dict(style_aliases)
    ui_style_names = {item[1]: item[0] for item in style_aliases}

    @classmethod
    def ui2internal(cls, ui_style_name: str) -> str:
        """Return the internal style name corresponding to `ui_style_name`, such as
        'heading 1' for 'Heading 1'."""
        return cls.internal_style_names.get(ui_style_name, ui_style_name)

    @classmethod
    def internal2ui(cls, internal_style_name: str) -> str:
        """Return the user interface style name corresponding to `internal_style_name`,
        such as 'Heading 1' for 'heading 1'."""
        return cls.ui_style_names.get(internal_style_name, internal_style_name)
