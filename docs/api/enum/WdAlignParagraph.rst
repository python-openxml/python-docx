.. _WdParagraphAlignment:

``WD_PARAGRAPH_ALIGNMENT``
==========================

alias: **WD_ALIGN_PARAGRAPH**

Specifies paragraph justification type.

Example::

    from docx.enum.text import WD_ALIGN_PARAGRAPH

    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

----

LEFT
    Left-aligned

CENTER
    Center-aligned.

RIGHT
    Right-aligned.

JUSTIFY
    Fully justified.

DISTRIBUTE
    Paragraph characters are distributed to fill the entire width of the
    paragraph.

JUSTIFY_MED
    Justified with a medium character compression ratio.

JUSTIFY_HI
    Justified with a high character compression ratio.

JUSTIFY_LOW
    Justified with a low character compression ratio.

THAI_JUSTIFY
    Justified according to Thai formatting layout.
