
Headers and Footers
===================

In a WordprocessingML document, a page header is text that is separated from
the main body of text and appears at the top of a printed page. The page
headers in a document are often the same from page to page, with only small
differences in content, such as a section and/or page number. Such a header
is also known as a *running head*.

In book-printed documents, where pages are intended to bound on the long edge
and presented side-by-side, the header on the right-hand (recto) pages is
often different than that on the left-hand (verso) pages. The need to support
this difference gives rise to the option to have an *even-page* header that
differs from the default *odd-page* header in a document.

A page footer is analogous in every way to a page header except that it
appears at the bottom of a page. It should not be confused with a footnote,
which is not uniform between pages.

In WordprocessingML, a header or footer appears within the margin area of
a page. With a few exceptions, a header or footer can contain all types of
content that can appear in the main body, including text and images. Each
section has its own set of headers and footers, although a section can be
configured to "inherit" headers and footers from the prior section.

Each section can have three distinct header definitions and footer
definitions. These apply to odd pages (the default), even pages, and the
first page of the section. All three are optional.

For brevity in the discussion below I will occasionally use the term *header*
to refer to either a header and footer object, trusting the reader to
understand its applicability to either type of object.


Header and footer parts
-----------------------

Each header or footer definition is a distinct part in the WordprocessingML
package.

A header/footer part is related to the document part by a relationship entry.
That relationship is referenced by a section in the document by its rId key.

A default document will contain no header or footer parts and no
`w:headerReference` or `w:footerReference` elements in its `w:sectPr`
element.


Research TODO
-------------

1. [ ] default blank document baseline
2. [ ] add section break
3. [ ] add section 2 header

   A. does Word create a blank default header for section 1?

4. [ ] set odd/even True on document with 2 sections, no header/footers

   A. does Word create a blank default header/footer for section 1?

5. [ ] if not, set a header on section 2 and document what happens
6. [ ] try the same on section 1 and see what happens

See if a pattern is discernable.

Hypothesis: Word inserts blank headers and footers only as needed to provide
a running default when the first section has no default. It does this for
both headers and footers whenever it does it at all.


Acceptance Tests
----------------

::

  Given a default blank document
   Then document.section[0].header is None
    And document.section[0].footer is None


  Given a document with a single section having a header and footer
   Then document.section[0].header is a Header object
    And document.section[0].footer is a Footer object


  Given a document with two sections having no headers or footers
   When I assign True to document.odd_and_even_pages_header_footer
   Then document.section[0].even_page_header is a blank Header object
    And document.section[0].footer is a blank Footer object
    And document.section[1].header is None
    And document.section[1].footer is None


Candidate Protocol
------------------

::

  >>> document = Document()
  >>> section = document.sections[-1]

  >>> section.header
  None
  >>> section.add_header()
  <docx.Header object at 0xdeadbeef0>

  >>> section.even_page_header
  None
  >>> section.add_even_page_header()
  <docx.Header object at 0xdeadbeef4>

  >>> section.first_page_header
  None
  >>> section.add_first_page_header()
  <docx.Header object at 0xdeadbeef8>


MS API
------

.. highlight:: python

WdHeaderFooterIndex Enumeration::

    EVEN_PAGES = 3
    FIRST_PAGE = 2
    PRIMARY    = 1

::

  section = Document.Sections(1)
  footers = section.Footers  # a HeadersFooters collection object
  default_footer = footers(wdHeaderFooterPrimary)
  default_footer.Range.Text = "Footer text"

PageSetup object::

  DifferentFirstPageHeaderFooter: Read/write {True, False, WD_UNDEFINED}
  OddAndEvenPagesHeaderFooter: Read/write {True, False, WD_UNDEFINED}


Specimen XML
------------

.. highlight:: xml

Baseline blank document (some unrelated details omitted)::

  <w:body>
    <w:p/>
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800"
               w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>

  <!--
    * no relationships to a header or footer part appear in document.xml.rels
    * no header or footer parts appear in the package
  -->

after adding a header::

  <!-- document.xml -->
  <w:sectPr>
    <w:headerReference w:type="default" r:id="rId8"/>
    <w:pgSz w:w="12240" w:h="15840"/>
    <w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800"
             w:header="720" w:footer="720" w:gutter="0"/>
  </w:sectPr>

  <!-- document.xml.rels -->
  <Relationship Id="rId8" Type="http://sc...ps/header" Target="header1.xml"/>

after then adding an even-page header::

  <!-- document.xml -->
  <w:sectPr>
    <w:headerReference w:type="even" r:id="rId8"/>
    <w:headerReference w:type="default" r:id="rId9"/>
    <w:pgSz w:w="12240" w:h="15840"/>
    <w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800"
             w:header="720" w:footer="720" w:gutter="0"/>
  </w:sectPr>

  <!-- document.xml.rels -->
  <Relationship Id="rId8" Type="http://sc...ps/header" Target="header1.xml"/>
  <Relationship Id="rId9" Type="http://sc...ps/header" Target="header2.xml"/>

Implementation sequence
-----------------------

* [ ] Implement skeleton SettingsPart
* [ ] A settings part is constructed by loader using the custom part
* [ ] Access header from section

* [ ] Implement skeleton HeaderPart, consider a HeaderFooterPart base class.
* [ ] A header/footer part is constructed by loader using the custom part
* [ ] Access header from section

Open topics
-----------

* [ ] notion that specifying different even/first header/footers is distinct
      from implementing different even/first header/footers. Auto-insertion
      of blank items on set different, when needed. Document Word behaviors.
* [ ] settings.xml `w:evenAndOddHeaders`
* [ ] interaction with `w:sectPr/w:titlePg` element for different first-page
      header and footer.
* [ ] describe inheritance behavior from user perspective, with examples, of
      header/footers and different even and first page header/footers.
* [ ] positioning of header and footer block in `w:pgMar` element
* [ ] part name/location is `word/header1.xml`

* [X] test whether Word will load a file with an even page header but no odd
      page header. Yes, works fine.


Differences between a document without and with a header
--------------------------------------------------------

If you create a default document and save it (let's call that test.docx),
then add a header to it like so...

    This is a header.   x of xx

...the following changes will occur in the package:

1) A part called header1.xml will be added to the package with the following
   pathname:

    /word/header1.xml

2) A new relationship is specified at word/_rels/document.xml.rels:

::

    <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml" />*

3) Within the <w:sectPr> element of document.xml, there will be a new element
   called headerReference:

::

    <w:sectPr>
        <w:headerReference w:type="default" r:id="rId2"/>*
        ...
    </w:sectPr>


Different Even/Odd Page Headers and Footers
-------------------------------------------

The `w:evenAndOddHeaders` element in the settings part specifies whether
sections have different headers and footers for even
and odd pages. This setting determines this behavior for all sections in the
document whether they have an even page header/footer defined or not.
A section not having an even-page header or footer defined will inherit it
from the prior section.

When this setting is set to |True|, a blank header and/or footer is created
in the first document section when one is not present and becomes the default
for the sections that follow until a header/footer is explicitly defined.
