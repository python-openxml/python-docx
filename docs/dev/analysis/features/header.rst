.. _header:

Header and Footer
=================

In a WordprocessingML document, a page header is text that is separated from the main
body of text and appears at the top of a printed page. The page headers in a document
are often the same from page to page, with only small differences in content, such as
a section title or page number. Such a header is also known as a running head.

A page footer is analogous in every way to a page header except that it appears at the
bottom of a page. It should not be confused with a footnote, which is not uniform
between pages. For brevity's sake, the term `header` is often used here to refer to what
may be either a header or footer object, trusting the reader to understand its
applicability to both object types.

In book-printed documents, where pages are printed on both sides, when opened, the front
or `recto` side of each page appears to the right of the bound edge and the back or
`verso` side of each page appears on the left. The first printed page receives the
page-number "1", and is always a recto page. Because pages are numbered consecutively,
each recto page receives an `odd` page number and each verso page receives an `even`
page number.

The header appearing on a recto page often differs from that on a verso page. Supporting
this difference gives rise to the option to have an even-page header that differs from
the default odd-page header in a document. This "both odd-and-even headers" option is
applied at the document level and affects all sections of the document.

The header appearing on the first page of a section (e.g. a chapter) may differ from
that appearing on subsequent pages. Supporting this difference gives rise to the option
to set a distinct first-page header. This "different first-page-header" option is
applied at the section level and may differ from section-to-section in the document.

In WordprocessingML, a header or footer appears within the margin area of a page. With
a few exceptions, a header or footer may contain all the types of content that can
appear in the main body, including text and images. Each header and footer has access to
the styles defined in ``/word/styles.xml``.

Each section has its own set of headers and footers, although a section can be
configured to "inherit" headers and footers from the prior section. Each section can
have three header definitions, the default header, even header, and first page header.
When different even/odd headers are not enabled, the default header appears on both even
and odd numbered pages. If even/odd headers are enabled, the default header is used for
odd pages. A corresponding set of three footer definitions are also possible. All
header/footer definitions are optional.


Open Questions
--------------

* What about a continuous section break? What is the header/footer behavior there?


Candidate Protocol
------------------

Every section has a header; it is never None::

    >>> header = section.header
    >>> header
    <docx.hdrftr.Header object at 0x02468ACE>


There are three header properties on |Section|: `.header`,
`.even_page_header`, and `.first_page_header`. All header objects share the
same properties and methods. There are three corresponding properties for the
footers.

Header is a subclass of |BlockItemContainer|, from which it inherits the same
content editing capabilities as |Document|, such as `.add_paragraph()`.

If the `w:headerReference` element for a header is not present, the
definition for that header is "inherited" from the prior section. This action
is recursive, such that, for example, the header definition from the first
section could be applied to the third section. A header that inherits its
definition is said to be "linked to previous". Perhaps counterintuitively,
a header for the first section can be "linked to previous", even though no
previous section exists. The `.is_linked_to_previous` property is simply
a test for the existence of a header definition in the current section::

    >>> header.is_linked_to_previous
    True

Editing operations transparently operate on the source header, the one in the
first prior section having a header of that type (when one is not present in
the current section). If no prior sections have a header, one is created in
the first section of the document on the first constructive edit call::

    >>> header = document.sections[0].header
    >>> header.is_linked_to_previous
    True
    >>> header.text = 'foobar'
    >>> header.is_linked_to_previous
    False

Assigning False to `.is_linked_to_previous` creates a blank header for that
section when one does not already exist::

    >>> header.is_linked_to_previous
    True
    >>> header.is_linked_to_previous = False
    >>> header.is_linked_to_previous
    False

Conversely, an existing header is deleted from a section by assigning True to
`.is_linked_to_previous`::

    >>> header.is_linked_to_previous
    False
    >>> header.is_linked_to_previous = True
    >>> header.is_linked_to_previous
    True

The document settings object has a read/write `.odd_and_even_pages_header_footer`
property that indicates verso and recto pages will have a different header. Any existing
even page header definitions are preserved when `.odd_and_even_pages_header_footer` is
False; they are simply not rendered by Word. Assigning `True` to
`.odd_and_even_pages_header_footer` does not automatically create new even header
definitions::

    >>> document.settings.odd_and_even_pages_header_footer
    False
    >>> document.settings.odd_and_even_pages_header_footer = True
    >>> section.even_page_header.is_linked_to_previous
    True

`Section` has a read/write `.different_first_page_header_footer` property
that indicates whether the first page of the section should have a distinct
header. Assigning `True` to `.different_first_page_header_footer` does not
automatically create a new first page header definition::

    >>> section.different_first_page_header_footer
    False
    >>> section.different_first_page_header_footer = True
    >>> section.different_first_page_header_footer
    True
    >>> section.first_page_header.is_linked_to_previous
    True


Specimen XML
------------

.. highlight:: xml

There are seven different permutations of headers:

The same header on all pages of the document::

   <w:sectPr>
       <w:headerReference w:type="default" r:id="rId3"/>
       ...
   </w:sectPr>


Only an odd header. The section is exactly the same as above but
`settings.xml` has the the `<w:evenAndOddHeaders>` property::

   <w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
      ...
      <w:evenAndOddHeaders w:val="1"/>
      ...
   </w:settings>

Different even and odd headers::

   <w:sectPr>
       <w:headerReference w:type="default" r:id="rId3"/>
       <w:headerReference w:type="even" r:id="rId4"/>
       ...
   </w:sectPr>

Distinct first page header, subsequent pages all have the same header::

   <w:sectPr>
       <w:headerReference w:type="default" r:id="rId3"/>
       <w:headerReference w:type="first" r:id="rId4"/>
       <w:titlePg/>
       ...
   </w:sectPr>

Distinct first, even, and odd page headers::

   <w:sectPr>
       <w:headerReference w:type="default" r:id="rId3"/>
       <w:headerReference w:type="first" r:id="rId4"/>
       <w:headerReference w:type="even" r:id="rId5"/>
       <w:titlePg/>
       ...
   </w:sectPr>

A header part::

   <w:hdr>
     <w:p>
       <w:pPr>
         <w:pStyle w:val="Header"/>
       </w:pPr>
       <w:r>
         <w:t>Header for section-1</w:t>
       </w:r>
     </w:p>
   </w:hdr>


Word Behavior
-------------

* When you turn off even/odd headers, Word sets the value of
  `w:evenAndOddHeaders` to 0, but does not actually remove the even header.

* When you turn off first page header, Word sets the value of `w:titlePg` to
  0, but does not actually remove the even header.

* Word will load a file with an even page header but no odd page header.


MS API
------

.. highlight:: python

WdHeaderFooterIndex Enumeration::

   EVEN_PAGES = 3
   FIRST_PAGE = 2
   PRIMARY    = 1

Create footer in MS API::

   section = Document.Sections(1)
   footers = section.Footers  # a HeadersFooters collection object
   default_footer = footers(wdHeaderFooterPrimary)
   default_footer.Range.Text = "Footer text"

PageSetup object::

   DifferentFirstPageHeaderFooter: Read/write {True, False, WD_UNDEFINED}
   OddAndEvenPagesHeaderFooter: Read/write {True, False, WD_UNDEFINED}


Schema Excerpt
--------------

.. code-block:: xml

    <xsd:complexType name="CT_SectPr">  <!-- denormalized -->
      <xsd:sequence>
        <xsd:choice minOccurs="0" maxOccurs="6"/>
          <xsd:element name="headerReference" type="CT_HdrFtrRef"/>
          <xsd:element name="footerReference" type="CT_HdrFtrRef"/>
        </xsd:choice>
        <xsd:element name="footnotePr"      type="CT_FtnProps"      minOccurs="0"/>
        <xsd:element name="endnotePr"       type="CT_EdnProps"      minOccurs="0"/>
        <xsd:element name="type"            type="CT_SectType"      minOccurs="0"/>
        <xsd:element name="pgSz"            type="CT_PageSz"        minOccurs="0"/>
        <xsd:element name="pgMar"           type="CT_PageMar"       minOccurs="0"/>
        <xsd:element name="paperSrc"        type="CT_PaperSource"   minOccurs="0"/>
        <xsd:element name="pgBorders"       type="CT_PageBorders"   minOccurs="0"/>
        <xsd:element name="lnNumType"       type="CT_LineNumber"    minOccurs="0"/>
        <xsd:element name="pgNumType"       type="CT_PageNumber"    minOccurs="0"/>
        <xsd:element name="cols"            type="CT_Columns"       minOccurs="0"/>
        <xsd:element name="formProt"        type="CT_OnOff"         minOccurs="0"/>
        <xsd:element name="vAlign"          type="CT_VerticalJc"    minOccurs="0"/>
        <xsd:element name="noEndnote"       type="CT_OnOff"         minOccurs="0"/>
        <xsd:element name="titlePg"         type="CT_OnOff"         minOccurs="0"/>
        <xsd:element name="textDirection"   type="CT_TextDirection" minOccurs="0"/>
        <xsd:element name="bidi"            type="CT_OnOff"         minOccurs="0"/>
        <xsd:element name="rtlGutter"       type="CT_OnOff"         minOccurs="0"/>
        <xsd:element name="docGrid"         type="CT_DocGrid"       minOccurs="0"/>
        <xsd:element name="printerSettings" type="CT_Rel"           minOccurs="0"/>
        <xsd:element name="sectPrChange"    type="CT_SectPrChange"  minOccurs="0"/>
      </xsd:sequence>
      <xsd:attribute name="rsidRPr"  type="ST_LongHexNumber"/>
      <xsd:attribute name="rsidDel"  type="ST_LongHexNumber"/>
      <xsd:attribute name="rsidR"    type="ST_LongHexNumber"/>
      <xsd:attribute name="rsidSect" type="ST_LongHexNumber"/>
    </xsd:complexType>

    <xsd:complexType name="CT_HdrFtrRef">
      <xsd:attribute ref="r:id" use="required"/>
      <xsd:attribute name="type" type="ST_HdrFtr" use="required"/>
    </xsd:complexType>

    <xsd:simpleType name="ST_HdrFtr">
      <xsd:restriction base="xsd:string">
        <xsd:enumeration value="even"/>
        <xsd:enumeration value="default"/>
        <xsd:enumeration value="first"/>
      </xsd:restriction>
    </xsd:simpleType>
