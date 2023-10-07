"""Enumerations used by DrawingML objects."""

from .base import BaseEnum, BaseXmlEnum


class MSO_COLOR_TYPE(BaseEnum):
    """Specifies the color specification scheme.

    Example::

        from docx.enum.dml import MSO_COLOR_TYPE

        assert font.color.type == MSO_COLOR_TYPE.SCHEME

    MS API name: `MsoColorType`

    http://msdn.microsoft.com/en-us/library/office/ff864912(v=office.15).aspx
    """

    RGB = (1, "Color is specified by an |RGBColor| value.")
    """Color is specified by an |RGBColor| value."""

    THEME = (2, "Color is one of the preset theme colors.")
    """Color is one of the preset theme colors."""

    AUTO = (101, "Color is determined automatically by the application.")
    """Color is determined automatically by the application."""


class MSO_THEME_COLOR_INDEX(BaseXmlEnum):
    """Indicates the Office theme color, one of those shown in the color gallery on the
    formatting ribbon.

    Alias: ``MSO_THEME_COLOR``

    Example::

        from docx.enum.dml import MSO_THEME_COLOR

        font.color.theme_color = MSO_THEME_COLOR.ACCENT_1

    MS API name: `MsoThemeColorIndex`

    http://msdn.microsoft.com/en-us/library/office/ff860782(v=office.15).aspx
    """

    NOT_THEME_COLOR = (0, "UNMAPPED", "Indicates the color is not a theme color.")
    """Indicates the color is not a theme color."""

    ACCENT_1 = (5, "accent1", "Specifies the Accent 1 theme color.")
    """Specifies the Accent 1 theme color."""

    ACCENT_2 = (6, "accent2", "Specifies the Accent 2 theme color.")
    """Specifies the Accent 2 theme color."""

    ACCENT_3 = (7, "accent3", "Specifies the Accent 3 theme color.")
    """Specifies the Accent 3 theme color."""

    ACCENT_4 = (8, "accent4", "Specifies the Accent 4 theme color.")
    """Specifies the Accent 4 theme color."""

    ACCENT_5 = (9, "accent5", "Specifies the Accent 5 theme color.")
    """Specifies the Accent 5 theme color."""

    ACCENT_6 = (10, "accent6", "Specifies the Accent 6 theme color.")
    """Specifies the Accent 6 theme color."""

    BACKGROUND_1 = (14, "background1", "Specifies the Background 1 theme color.")
    """Specifies the Background 1 theme color."""

    BACKGROUND_2 = (16, "background2", "Specifies the Background 2 theme color.")
    """Specifies the Background 2 theme color."""

    DARK_1 = (1, "dark1", "Specifies the Dark 1 theme color.")
    """Specifies the Dark 1 theme color."""

    DARK_2 = (3, "dark2", "Specifies the Dark 2 theme color.")
    """Specifies the Dark 2 theme color."""

    FOLLOWED_HYPERLINK = (
        12,
        "followedHyperlink",
        "Specifies the theme color for a clicked hyperlink.",
    )
    """Specifies the theme color for a clicked hyperlink."""

    HYPERLINK = (11, "hyperlink", "Specifies the theme color for a hyperlink.")
    """Specifies the theme color for a hyperlink."""

    LIGHT_1 = (2, "light1", "Specifies the Light 1 theme color.")
    """Specifies the Light 1 theme color."""

    LIGHT_2 = (4, "light2", "Specifies the Light 2 theme color.")
    """Specifies the Light 2 theme color."""

    TEXT_1 = (13, "text1", "Specifies the Text 1 theme color.")
    """Specifies the Text 1 theme color."""

    TEXT_2 = (15, "text2", "Specifies the Text 2 theme color.")
    """Specifies the Text 2 theme color."""


MSO_THEME_COLOR = MSO_THEME_COLOR_INDEX
