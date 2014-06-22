.. _WdOrientation:

``WD_ORIENTATION``
==================

alias: **WD_ORIENT**

Specifies the page layout orientation.

Example::

    from docx.enum.section import WD_ORIENT

    section = document.sections[-1]
    section.orientation = WD_ORIENT.LANDSCAPE

----

PORTRAIT
    Portrait orientation.

LANDSCAPE
    Landscape orientation.
