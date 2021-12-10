.. _WdLineSpacing:

``WD_LINE_SPACING``
===================

Specifies a line spacing format to be applied to a paragraph.

Example::

    from docx.enum.text import WD_LINE_SPACING

    paragraph = document.add_paragraph()
    paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY

----

ONE_POINT_FIVE
    Space-and-a-half line spacing.

AT_LEAST
    Line spacing is always at least the specified amount. The amount is
    specified separately.

DOUBLE
    Double spaced.

EXACTLY
    Line spacing is exactly the specified amount. The amount is specified
    separately.

MULTIPLE
    Line spacing is specified as a multiple of line heights. Changing the font
    size will change the line spacing proportionately.

SINGLE
    Single spaced (default).
