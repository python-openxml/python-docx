.. _WdSectionStart:

``WD_SECTION_START``
====================

alias: **WD_SECTION**

Specifies the start type of a section break.

Example::

    from docx.enum.section import WD_SECTION

    section = document.sections[0]
    section.start_type = WD_SECTION.NEW_PAGE

----

CONTINUOUS
    Continuous section break.

NEW_COLUMN
    New column section break.

NEW_PAGE
    New page section break.

EVEN_PAGE
    Even pages section break.

ODD_PAGE
    Section begins on next odd page.
