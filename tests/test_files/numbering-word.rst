Numbering fixture
=================

``numbering-word.docx`` was created with Microsoft Word on Windows.
It contains a nine-level list template. Its first two levels use ``%1.``
and ``%1.%2.`` with text indents of 18 and 36 points. The second level
restarts when the first level advances. The paragraph style ``Example outline``
is linked to the first level.

Word displays the three fixture paragraphs as 1., 1.1., and 2.
Library-generated additions were opened separately in Word and displayed
3., 3.1., an unnumbered continuation, 4., and 4.1. The continuation had a
36-point left indent and zero first-line indent.

The independent-sequence regression was also checked in Word. With a new
abstract definition for each sequence, interleaved paragraphs displayed
3., 4., 1., and 5. Reusing the same abstract definition incorrectly displayed
2. for the final paragraph despite its different concrete numbering instance.
