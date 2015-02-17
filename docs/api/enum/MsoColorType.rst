.. _MsoColorType:

``MSO_COLOR_TYPE``
==================

Specifies the color specification scheme

Example::

    from docx.enum.dml import MSO_COLOR_TYPE

    assert font.color.type == MSO_COLOR_TYPE.THEME

----

RGB
    Color is specified by an |RGBColor| value.

THEME
    Color is one of the preset theme colors.

AUTO
    Color is determined automatically be the application.
