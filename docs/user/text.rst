
Low-level text API
==================

For the greatest control over inserted text, an understanding of the low-level
text API is required.

Block-level vs. inline text objects
-----------------------------------

The paragraph is the primary block-level object in Word. A table is also
a block-level object, however its acts primarily as a container rather than
content. Each cell of a table is a block-level container, much like the
document body itself. Its rows and columns simply provide structure to the
cells.

A paragraph contains one or more inline elements called *runs*. It is the
run that actually contains text content.

The main purpose of a run it to carry character formatting information, such as
font typeface and size. Bold, italic, and underline formatting are also
examples. All text within a run shares the same character formatting. So
a three-word paragraph having the middle word bold would require three runs.

Producing paragraphs containing so-called "rich" text requires building the
paragraph up out of multiple runs. Runs can also contain other content objects
such as line breaks and fields, so there are other reasons you may need to use
the low-level text API.
