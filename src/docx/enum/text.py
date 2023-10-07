"""Enumerations related to text in WordprocessingML files."""

from __future__ import annotations

import enum

from docx.enum.base import BaseXmlEnum


class WD_PARAGRAPH_ALIGNMENT(BaseXmlEnum):
    """Alias: **WD_ALIGN_PARAGRAPH**

    Specifies paragraph justification type.

    Example::

        from docx.enum.text import WD_ALIGN_PARAGRAPH

        paragraph = document.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    """

    LEFT = (0, "left", "Left-aligned")
    """Left-aligned"""

    CENTER = (1, "center", "Center-aligned.")
    """Center-aligned."""

    RIGHT = (2, "right", "Right-aligned.")
    """Right-aligned."""

    JUSTIFY = (3, "both", "Fully justified.")
    """Fully justified."""

    DISTRIBUTE = (
        4,
        "distribute",
        "Paragraph characters are distributed to fill entire width of paragraph.",
    )
    """Paragraph characters are distributed to fill entire width of paragraph."""

    JUSTIFY_MED = (
        5,
        "mediumKashida",
        "Justified with a medium character compression ratio.",
    )
    """Justified with a medium character compression ratio."""

    JUSTIFY_HI = (
        7,
        "highKashida",
        "Justified with a high character compression ratio.",
    )
    """Justified with a high character compression ratio."""

    JUSTIFY_LOW = (8, "lowKashida", "Justified with a low character compression ratio.")
    """Justified with a low character compression ratio."""

    THAI_JUSTIFY = (
        9,
        "thaiDistribute",
        "Justified according to Thai formatting layout.",
    )
    """Justified according to Thai formatting layout."""


WD_ALIGN_PARAGRAPH = WD_PARAGRAPH_ALIGNMENT


class WD_BREAK_TYPE(enum.Enum):
    """Corresponds to WdBreakType enumeration.

    http://msdn.microsoft.com/en-us/library/office/ff195905.aspx.
    """

    COLUMN = 8
    LINE = 6
    LINE_CLEAR_LEFT = 9
    LINE_CLEAR_RIGHT = 10
    LINE_CLEAR_ALL = 11  # -- added for consistency, not in MS version --
    PAGE = 7
    SECTION_CONTINUOUS = 3
    SECTION_EVEN_PAGE = 4
    SECTION_NEXT_PAGE = 2
    SECTION_ODD_PAGE = 5
    TEXT_WRAPPING = 11


WD_BREAK = WD_BREAK_TYPE


class WD_COLOR_INDEX(BaseXmlEnum):
    """Specifies a standard preset color to apply.

    Used for font highlighting and perhaps other applications.

    * MS API name: `WdColorIndex`
    * URL: https://msdn.microsoft.com/EN-US/library/office/ff195343.aspx
    """

    INHERITED = (-1, None, "Color is inherited from the style hierarchy.")
    """Color is inherited from the style hierarchy."""

    AUTO = (0, "default", "Automatic color. Default; usually black.")
    """Automatic color. Default; usually black."""

    BLACK = (1, "black", "Black color.")
    """Black color."""

    BLUE = (2, "blue", "Blue color")
    """Blue color"""

    BRIGHT_GREEN = (4, "green", "Bright green color.")
    """Bright green color."""

    DARK_BLUE = (9, "darkBlue", "Dark blue color.")
    """Dark blue color."""

    DARK_RED = (13, "darkRed", "Dark red color.")
    """Dark red color."""

    DARK_YELLOW = (14, "darkYellow", "Dark yellow color.")
    """Dark yellow color."""

    GRAY_25 = (16, "lightGray", "25% shade of gray color.")
    """25% shade of gray color."""

    GRAY_50 = (15, "darkGray", "50% shade of gray color.")
    """50% shade of gray color."""

    GREEN = (11, "darkGreen", "Green color.")
    """Green color."""

    PINK = (5, "magenta", "Pink color.")
    """Pink color."""

    RED = (6, "red", "Red color.")
    """Red color."""

    TEAL = (10, "darkCyan", "Teal color.")
    """Teal color."""

    TURQUOISE = (3, "cyan", "Turquoise color.")
    """Turquoise color."""

    VIOLET = (12, "darkMagenta", "Violet color.")
    """Violet color."""

    WHITE = (8, "white", "White color.")
    """White color."""

    YELLOW = (7, "yellow", "Yellow color.")
    """Yellow color."""


WD_COLOR = WD_COLOR_INDEX


class WD_LINE_SPACING(BaseXmlEnum):
    """Specifies a line spacing format to be applied to a paragraph.

    Example::

        from docx.enum.text import WD_LINE_SPACING

        paragraph = document.add_paragraph()
        paragraph.line_spacing_rule = WD_LINE_SPACING.EXACTLY


    MS API name: `WdLineSpacing`

    URL: http://msdn.microsoft.com/en-us/library/office/ff844910.aspx
    """

    SINGLE = (0, "UNMAPPED", "Single spaced (default).")
    """Single spaced (default)."""

    ONE_POINT_FIVE = (1, "UNMAPPED", "Space-and-a-half line spacing.")
    """Space-and-a-half line spacing."""

    DOUBLE = (2, "UNMAPPED", "Double spaced.")
    """Double spaced."""

    AT_LEAST = (
        3,
        "atLeast",
        "Minimum line spacing is specified amount. Amount is specified separately.",
    )
    """Minimum line spacing is specified amount. Amount is specified separately."""

    EXACTLY = (
        4,
        "exact",
        "Line spacing is exactly specified amount. Amount is specified separately.",
    )
    """Line spacing is exactly specified amount. Amount is specified separately."""

    MULTIPLE = (
        5,
        "auto",
        "Line spacing is specified as multiple of line heights. Changing font size"
        " will change line spacing proportionately.",
    )
    """Line spacing is specified as multiple of line heights. Changing font size will
       change the line spacing proportionately."""


class WD_TAB_ALIGNMENT(BaseXmlEnum):
    """Specifies the tab stop alignment to apply.

    MS API name: `WdTabAlignment`

    URL: https://msdn.microsoft.com/EN-US/library/office/ff195609.aspx
    """

    LEFT = (0, "left", "Left-aligned.")
    """Left-aligned."""

    CENTER = (1, "center", "Center-aligned.")
    """Center-aligned."""

    RIGHT = (2, "right", "Right-aligned.")
    """Right-aligned."""

    DECIMAL = (3, "decimal", "Decimal-aligned.")
    """Decimal-aligned."""

    BAR = (4, "bar", "Bar-aligned.")
    """Bar-aligned."""

    LIST = (6, "list", "List-aligned. (deprecated)")
    """List-aligned. (deprecated)"""

    CLEAR = (101, "clear", "Clear an inherited tab stop.")
    """Clear an inherited tab stop."""

    END = (102, "end", "Right-aligned.  (deprecated)")
    """Right-aligned.  (deprecated)"""

    NUM = (103, "num", "Left-aligned.  (deprecated)")
    """Left-aligned.  (deprecated)"""

    START = (104, "start", "Left-aligned.  (deprecated)")
    """Left-aligned.  (deprecated)"""


class WD_TAB_LEADER(BaseXmlEnum):
    """Specifies the character to use as the leader with formatted tabs.

    MS API name: `WdTabLeader`

    URL: https://msdn.microsoft.com/en-us/library/office/ff845050.aspx
    """

    SPACES = (0, "none", "Spaces. Default.")
    """Spaces. Default."""

    DOTS = (1, "dot", "Dots.")
    """Dots."""

    DASHES = (2, "hyphen", "Dashes.")
    """Dashes."""

    LINES = (3, "underscore", "Double lines.")
    """Double lines."""

    HEAVY = (4, "heavy", "A heavy line.")
    """A heavy line."""

    MIDDLE_DOT = (5, "middleDot", "A vertically-centered dot.")
    """A vertically-centered dot."""


class WD_UNDERLINE(BaseXmlEnum):
    """Specifies the style of underline applied to a run of characters.

    MS API name: `WdUnderline`

    URL: http://msdn.microsoft.com/en-us/library/office/ff822388.aspx
    """

    INHERITED = (-1, None, "Inherit underline setting from containing paragraph.")
    """Inherit underline setting from containing paragraph."""

    NONE = (
        0,
        "none",
        "No underline.\n\nThis setting overrides any inherited underline value, so can"
        " be used to remove underline from a run that inherits underlining from its"
        " containing paragraph. Note this is not the same as assigning |None| to"
        " Run.underline. |None| is a valid assignment value, but causes the run to"
        " inherit its underline value. Assigning `WD_UNDERLINE.NONE` causes"
        " underlining to be unconditionally turned off.",
    )
    """No underline.

    This setting overrides any inherited underline value, so can be used to remove
    underline from a run that inherits underlining from its containing paragraph. Note
    this is not the same as assigning |None| to Run.underline. |None| is a valid
    assignment value, but causes the run to inherit its underline value. Assigning
    ``WD_UNDERLINE.NONE`` causes underlining to be unconditionally turned off.
    """

    SINGLE = (
        1,
        "single",
        "A single line.\n\nNote that this setting is write-only in the sense that"
        " |True| (rather than `WD_UNDERLINE.SINGLE`) is returned for a run having"
        " this setting.",
    )
    """A single line.

    Note that this setting is write-only in the sense that |True|
    (rather than ``WD_UNDERLINE.SINGLE``) is returned for a run having this setting.
    """

    WORDS = (2, "words", "Underline individual words only.")
    """Underline individual words only."""

    DOUBLE = (3, "double", "A double line.")
    """A double line."""

    DOTTED = (4, "dotted", "Dots.")
    """Dots."""

    THICK = (6, "thick", "A single thick line.")
    """A single thick line."""

    DASH = (7, "dash", "Dashes.")
    """Dashes."""

    DOT_DASH = (9, "dotDash", "Alternating dots and dashes.")
    """Alternating dots and dashes."""

    DOT_DOT_DASH = (10, "dotDotDash", "An alternating dot-dot-dash pattern.")
    """An alternating dot-dot-dash pattern."""

    WAVY = (11, "wave", "A single wavy line.")
    """A single wavy line."""

    DOTTED_HEAVY = (20, "dottedHeavy", "Heavy dots.")
    """Heavy dots."""

    DASH_HEAVY = (23, "dashedHeavy", "Heavy dashes.")
    """Heavy dashes."""

    DOT_DASH_HEAVY = (25, "dashDotHeavy", "Alternating heavy dots and heavy dashes.")
    """Alternating heavy dots and heavy dashes."""

    DOT_DOT_DASH_HEAVY = (
        26,
        "dashDotDotHeavy",
        "An alternating heavy dot-dot-dash pattern.",
    )
    """An alternating heavy dot-dot-dash pattern."""

    WAVY_HEAVY = (27, "wavyHeavy", "A heavy wavy line.")
    """A heavy wavy line."""

    DASH_LONG = (39, "dashLong", "Long dashes.")
    """Long dashes."""

    WAVY_DOUBLE = (43, "wavyDouble", "A double wavy line.")
    """A double wavy line."""

    DASH_LONG_HEAVY = (55, "dashLongHeavy", "Long heavy dashes.")
    """Long heavy dashes."""
