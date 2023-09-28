.. _hdrftr:

Working with Headers and Footers
================================

Word supports *page headers* and *page footers*. A page header is text that appears in
the top margin area of each page, separated from the main body of text, and usually
conveying context information, such as the document title, author, creation date, or the
page number. The page headers in a document are the same from page to page, with only
small differences in content, such as a changing section title or page number. A page
header is also known as a *running head*.

A *page footer* is analogous in every way to a page header except that it appears at the
bottom of a page. It should not be confused with a footnote, which is not uniform
between pages. For brevity's sake, the term `header` is often used here to refer to what
may be either a header or footer object, trusting the reader to understand its
applicability to both object types.


Accessing the header for a section
----------------------------------

Headers and footers are linked to a `section`; this allows each section to have
a distinct header and/or footer. For example, a landscape section might have a wider
header than a portrait section.

Each section object has a ``.header`` property providing access to a |_Header| object
for that section::

    >>> document = Document()
    >>> section = document.sections[0]
    >>> header = section.header
    >>> header
    <docx.section._Header object at 0x...>

A |_Header| object is `always` present on ``Section.header``, even when no header is
defined for that section. The presence of an actual header definition is indicated by
``_Header.is_linked_to_previous``::

    >>> header.is_linked_to_previous
    True

A value of ``True`` indicates the |_Header| object contains no header definition and the
section will display the same header as the previous section. This "inheritance"
behavior is recursive, such that a "linked" header actually gets its definition from the
first prior section having a header definition. This "linked" state is indicated as
*"Same as previous"* in the Word UI.

A new document does not have a header (on the single section it contains) and so
``.is_linked_to_previous`` is ``True`` in that case. Note this case may be a bit
counterintuitive in that there *is no previous section header* to link to. In
this "no previous header" case, no header is displayed.


Adding a header (simple case)
-----------------------------

A header can be added to a new document simply by editing the content of the |_Header|
object. A |_Header| object is a "story" container and its content is edited just like
a |Document| object. Note that like a new document, a new header already contains
a single (empty) paragraph::

    >>> paragraph = header.paragraphs[0]
    >>> paragraph.text = "Title of my document"

.. image:: /_static/img/hdrftr-01.png
   :scale: 50%

Note also that the act of adding content (or even just accessing ``header.paragraphs``)
added a header definition and changed the state of ``.is_linked_to_previous``::

    >>> header.is_linked_to_previous
    False


Adding "zoned" header content
-----------------------------

A header with multiple "zones" is often accomplished using carefully placed tab stops.

The required tab-stops for a center and right-aligned "zone" are part of the ``Header``
and ``Footer`` styles in Word. If you're using a custom template rather than the
`python-docx` default, it probably makes sense to define that style in your template.

Inserted tab characters (``"\t"``) are used to separate left, center, and right-aligned
header content::

    >>> paragraph = header.paragraphs[0]
    >>> paragraph.text = "Left Text\tCenter Text\tRight Text"
    >>> paragraph.style = document.styles["Header"]

.. image:: /_static/img/hdrftr-02.png
   :scale: 75%

The ``Header`` style is automatically applied to a new header, so the third line just
above (applying the ``Header`` style) is unnecessary in this case, but included here to
illustrate the general case.


Removing a header
-----------------

An unwanted header can be removed by assigning ``True`` to its
``.is_linked_to_previous`` attribute::

    >>> header.is_linked_to_previous = True
    >>> header.is_linked_to_previous
    True

The content for a header is irreversably deleted when ``True`` is assigned to
``.is_linked_to_previous``.


Understanding headers in a multi-section document
-------------------------------------------------

The "just start editing" approach works fine for the simple case, but to make sense of
header behaviors in a multi-section document, a few simple concepts will be helpful.
Here they are in a nutshell:

1. Each section can have its own header definition (but doesn't have to).

2. A section that lacks a header definition inherits the header of the section before
   it. The ``_Header.is_linked_to_previous`` property simply reflects the presence of
   a header definition, ``False`` when a definition is present and ``True`` when not.

3. Lacking a header definition is the default state. A new document has no defined
   header and neither does a newly-inserted section. ``.is_linked_to_previous`` reports
   ``True`` in both those cases.

4. The content of a ``_Header`` object is its own content if it has a header definition.
   If not, its content is that of the first prior section that `does` have a header
   definition. If no sections have a header definition, a new one is added on the first
   section and all other sections inherit that one. This adding of a header definition
   happens the first time header content is accessed, perhaps by referencing
   ``header.paragraphs``.


Adding a header definition (general case)
-----------------------------------------

An explicit header definition can be given to a section that lacks one by assigning
``False`` to its ``.is_linked_to_previous`` property::

    >>> header.is_linked_to_previous
    True
    >>> header.is_linked_to_previous = False
    >>> header.is_linked_to_previous
    False

The newly added header definition contains a single empty paragraph. Note that leaving
the header this way is occasionally useful as it effectively "turns-off" a header for
that section and those after it until the next section with a defined header.

Assigning ``False`` to ``.is_linked_to_previous`` on a header that already has a header
definition does nothing.


Inherited content is automatically located
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Editing the content of a header edits the content of the `source` header, taking into
account any "inheritance". So for example, if the section 2 header inherits from section
1 and you edit the section 2 header, you actually change the contents of the section
1 header. A new header definition is not added for section 2 unless you first explicitly
assign ``False`` to its ``.is_linked_to_previous`` property.
