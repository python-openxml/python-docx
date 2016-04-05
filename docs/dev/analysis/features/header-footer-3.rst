=================
Header and Footer
=================

In a WordprocessingML document, a page header is text that is separated from
the main body of text and appears at the top of a printed page. The page
headers in a document are often the same from page to page, with only small
differences in content, such as a section and/or page number. Such a header is
also known as a running head.

In book-printed documents, where pages are intended to bound on the long edge
and presented side-by-side, the header on the right-hand (recto) pages is often
different than that on the left-hand (verso) pages. The need to support this
difference gives rise to the option to have an even-page header that differs
from the default odd-page header in a document.

A page footer is analogous in every way to a page header except that it appears
at the bottom of a page. It should not be confused with a footnote, which is
not uniform between pages.

In WordprocessingML, a header or footer appears within the margin area of a
page. With a few exceptions, a header or footer can contain all types of
content that can appear in the main body, including text and images. Each
section has its own set of headers and footers, although a section can be
configured to "inherit" headers and footers from the prior section.

Each section can have three distinct header definitions and footer definitions.
These apply to odd pages (the default), even pages, and the first page of the
section. All three are optional.

For brevity in the discussion below I will occasionally use the term *header*
to refer to either a header and footer object, trusting the reader to
understand its applicability to either type of object.

Note on Styles:

The header and footer has access to all the normal styles defined in
``/word/styles.xml``.

Candidate Protocol
==================


.. code-block:: xml

    # every section has a header; it is never None

    >>> header = section.header
    >>> header
    <docx.hdrftr.Header object at 0x02468ACE>

    # Header.text - read/write, full text, no character formatting, \n for line
    # break, \n\n for paragraph (or whatever other .text bits do). Assignment can
    # only be a single paragraph; can include tabs and line breaks, but no
    # paragraphs.

Header inherits from docx.blkcntnr.BlockItemContainer. It has access to all the
normal header.add_paragraph, paragraph.add_run, paragraph.add_image functions.

.. code-block:: xml

    # if a section has no w:headerReference, it inherits from the prior
    # section

    >>> header.is_linked_to_previous
    True

constructive editing operations transparently operate on the source
header, that of the first prior section having a header (if the current
section has none). If no prior sections have a header, one is created
in the first section of the document on the first constructive edit
call.

.. code-block:: xml

    >>> header = document.sections[0].header
    >>> header.is_linked_to_previous
    True
    >>> header.text = 'foobar'
    >>> header.is_linked_to_previous
    False

    # A header can be explicitly added to a section by assigning False to
    # Header.is_linked_to_previous

    >>> header.is_linked_to_previous
    True
    >>> header.is_linked_to_previous = False
    >>> header.is_linked_to_previous
    False

    # after setting is_linked_to_previous = False, the variable header changes
    # from the header from the previous section to a brand new copy of the header
    # from the previous section. edits to header will affect the current section,
    # not the previous section.

    # Conversely, a header can be deleted from a section by assigning True to
    # Header.is_linked_to_previous

    >>> header.is_linked_to_previous
    False
    >>> header.is_linked_to_previous = True
    >>> header.is_linked_to_previous
    True

There are three headers: header, even_header, and first_page_header. They all
function similarly to header described above.

.. code-block:: xml

    >>> document.settings.different_even_odd_headers = True
    # the first time this is set to True, this creates a blank even header
    # in the first section which all other sections inherit.
    # because by default "linked_to_previous" == True

    >>> header = document.sections[0].header
    # if different_even_odd_headers is False, then header will be on all pages
    # if different_even_odd_headers is True, then header will be on odd pages

    >>> even_header = document.sections[0].even_header
    # creates a new even_header just like header
    # if different_even_odd_headers is False, then even_header will be present
    # but not displayed
    # if different_even_odd_headers is True, then even_header will be displayed
    # on even pages

    >>> section = document.sections[2]
    >>> section.different_first_page_header
    False
    >>> section.different_first_page_header = True
    # if there is no first_page_header, a new blank first_page_header is
    # created in the first section
    >>> section.different_first_page_header
    True

    >>> first_page_header = document.sections[0].first_page_header
    # get_or_creates a new first_page_header just like header
    # if section.different_first_page_header is True, the first_page_header is
    # displayed on the first page of the section
    # if section.different_first_page_header is False, the first_page_header is
    # not displayed
    # by default new sections have different_first_page_header set to False


Specimen XML
============

There are seven different permutations of headers:

This most basic scenario a single header on all pages of the document:

.. code-block:: xml

   <w:sectPr>
       <w:headerReference w:type="default" r:id="rId3"/>
       <w:pgSz w:w="12240" w:h="15840"/>
       ...
   </w:sectPr>


Now just an odd header. The section is exactly the same as above but `settings.xml`:

.. code-block:: xml

   <w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
      <w:evenAndOddHeaders w:val="1"/>
   </w:settings>

Now both even and odd header. `settings.xml` still has `w:evenAndOddHeaders`
and the section looks like this:

.. code-block:: xml

   <w:sectPr>
       <w:headerReference w:type="default" r:id="rId3"/>
       <w:headerReference w:type="even" r:id="rId4"/>
       <w:pgSz w:w="12240" w:h="15840"/>
       ...
   </w:sectPr>

One header appears on the first page, and a different header on all subsequent pages:

.. code-block:: xml

   <w:sectPr>
       <w:headerReference w:type="default" r:id="rId3"/>
       <w:headerReference w:type="first" r:id="rId4"/>
       <w:pgSz w:w="12240" w:h="15840"/>
       ...
   </w:sectPr>

In this scenario one header appears on the first page, and then alternating even/odd headers appear on all subsequent pages.

The ``settings.xml`` contains the ``w:evenAndOddHeaders`` element.

.. code-block:: xml

   <w:sectPr>
       <w:headerReference w:type="default" r:id="rId3"/>
       <w:headerReference w:type="first" r:id="rId4"/>
       <w:headerReference w:type="even" r:id="rId5"/>
       <w:pgSz w:w="12240" w:h="15840"/>
       ...
   </w:sectPr>

To better understand the header / footer XML, see also:
`Header Part </dev/analysis/features/header-part.html>`_

XML Semantics
=============

`<w:evenAndOddHeaders/>` seems to work equivalently to `<w:evenAndOddHeaders w:val="1"/>`

`<w:titlePg/>` seems to work equivalently to `<w:titlePg w:val="1"/>`

Word Behavior
=============

When you turn off even/odd headers, Word sets the value of
`w:evenAndOddHeaders` to 0, but does not actually remove the even header.

When you turn off first page header, Word sets the value of
`w:titlePg` to 0, but does not actually remove the even header.

Word will load a file with an even page header but no odd page header.

MS API
======

WdHeaderFooterIndex Enumeration

.. code-block:: python

   EVEN_PAGES = 3
   FIRST_PAGE = 2
   PRIMARY    = 1

.. code-block:: python

   section = Document.Sections(1)
   footers = section.Footers  # a HeadersFooters collection object
   default_footer = footers(wdHeaderFooterPrimary)
   default_footer.Range.Text = "Footer text"

PageSetup object

.. code-block:: python

   DifferentFirstPageHeaderFooter: Read/write {True, False, WD_UNDEFINED}
   OddAndEvenPagesHeaderFooter: Read/write {True, False, WD_UNDEFINED}


Schema Excerpt
==============

.. code-block:: xml

    <xsd:complexType name="CT_SectPr">  <!-- denormalized -->
      <xsd:sequence>
        <xsd:choice minOccurs="0" maxOccurs="6"/>
          <xsd:element name="headerReference" type="CT_HdrFtrRef"/>
          <xsd:element name="footerReference" type="CT_HdrFtrRef"/>
        <xsd:choice minOccurs="0" maxOccurs="6"/>
        <xsd:element name="titlePg" type="CT_OnOff" minOccurs="0"/>
    </xsd:complexType>

    <xsd:complexType name="CT_HdrFtrRef">
      <xsd:attribute  ref="r:id"                  use="required"/>
      <xsd:attribute name="type" type="ST_HdrFtr" use="required"/>
    </xsd:complexType>

    <xsd:simpleType name="ST_HdrFtr">
      <xsd:restriction base="xsd:string">
        <xsd:enumeration value="even"/>
        <xsd:enumeration value="default"/>
        <xsd:enumeration value="first"/>
      </xsd:restriction>
    </xsd:simpleType>

    <xsd:complexType name="CT_Settings">
        <xsd:element name="evenAndOddHeaders" type="CT_OnOff" minOccurs="0"/>
    </xsd:complexType>
