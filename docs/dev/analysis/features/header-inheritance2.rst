I confirmed that toggling "Different even and odd headers" in the UI is always global and affects all sections simultaneously. Which makes perfect sense given the XML!

Experiment 1:
=============

Summary: "Different first page" can be toggled section by section. "Different first page" only applies to default, even, and first headers individually.

Steps:
------

> Create new file, set even-odd headers on
> Create an even header and a different odd header with content S1Even and S1Odd respectively
> Add a second section.
> Add second page to second section

Section 2 inherits S1Even and S1Odd header from Section 1.

> Toggle "Different First Page" on section 1 header. Add content S1First.

Section 2 page 2 still shows S1Odd

> Toggle "Different First Page" on section 2 header

Section 2 header shows S1First

> Alternate scenario: Toggle "Different First Page" on section 1 before adding Section 2.

Same end result. Section 2 still starts off with "Different First Page" as false.

In other words, for new sections, Word defaults to "Different First Page" being false and inherits the appropriate even/odd header from the previous section. Which seems like a reasonable default we should copy.

> Uncheck "Different First Page" for Section 1 and 2
> Add a third section.
> Add second page to third section.

Section 3 has S1Odd and S1Even headers.

> Change the default (odd) header for section 2 to S2Odd

Both Section 3 AND Section 1 headers flip to S2Odd.

> Set Section 2 "Link to Previous" to False./

Section 1 header remains "S2Odd"

> Change Section 2 header to "S3Odd"

Section 1 header remains "S2Odd"  whereas Section 3 header becomes "S3Odd" (as you'd expect).

> Set Section 2 "Different First Page" to True.

Section 2 "Link to Previous" flips from True to False. (Weird) Section 2 header now has the S1First header.

> Set Section 2 "Link to Previous" to false.

Section 2 remains S1First.

> Change Section 2 to "S2First"

Section 1 remains S1First.

It looks like "Link to Previous" operates independently for first / odd headers. That's why when you flip on "Different First Page" it switches automagically to "Link to Previous". The odd header has had "Link to Previous" set to false, but the first page header has not!

Experiment 2:
=============

Document with two two-page sections.

Purpose: Examining the XML behavior of "Link to Previous"

Summary:

"Link to previous" is not actually reflected in the Word XML as such. It's just a UI affordance to copy/paste headers.

Word Header/Footer Inheritance is copypasta. Setting "Link to Previous" to False actually means: copy first section's sectPr's header to sentinel sectPr.

Setting "Link to Previous" to True means: remove sentinel sectPr's header.
Whereupon Word by default will inherit the first section's headers.

Steps:
------

> Create new file, set even-odd headers on
> Create an even header and a different odd header with content S1Even and S1Odd respectively
> Add a second section.
> Add second page to second section

XML: even / odd header in last paragraph of Section 1. no headers in sentinel sectPr.

> Set "link to previous" to False in section 2's odd header.

XML: even / odd header in last paragraph of Section 1. odd header in sentinel sectPr.

> Change Section 2 odd header to "S2Odd"

XML: text in sentinel sectPr odd header changed to "S2Odd". Confirmed: Section 2 is displaying sentinel sectPr's header data.

> Set "link to previous" back to True on section 1's

Word displays alert: "Do you want to delete this header/footer and connect to the header/footer in the previous section?"

> Click "Yes".

XML: sentinel sectPr header is gone.

Experiment 2:
=============

Setup:
------

Document with four two-page sections.

Purpose:
--------

Set "Link to Previous" to False at Section 3 Pg header. Examine how Section 1/2 inherit, vs Section 3/4.

Summary:
--------

The sectPr of the last paragraph of section 1 has even/odd headers.

The sectPr of the last paragraph of section 3 has odd header.

No sentinel sectPr header.

Experiment 3:
=============

Purpose:
--------

Discover when exactly the sentinel sectPr is used, vs the sectPr of the last paragraph of the section.

Setup:
------

Document with three two-page sections.

Summary:
--------

If the last section has "Link to Previous" set to False, the header used by the previous section will be copied to the sentinel sectPr.

If any non-last section has "Link to Previous" set to False, the header used by the previous section will be copied to the sectPr of the final paragraph of the that section.

Steps:
------

Scenario 1:

> Set Section 3's Odd Header "Link to Previous" to False.

XML:  Header is in sentinel sectPr

Scenario 2:

> Set Section 2's Odd Header "Link to Previous" to False.

XML: Header is in sectPr of last paragraph of section 2, not in sentinel sectPr.

Scenario 3:

> Set Section 3's Odd Header "Link to Previous" to False.
> Add Section 4

XML: Header is in sectPr of last paragraph of section 3, not in sentinel sectPr.
