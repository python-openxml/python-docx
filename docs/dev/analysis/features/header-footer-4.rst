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

There are three headers: header, even_header, and first_page_header. They all
function similarly to header.

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

    # A blank header can be explicitly added to a section by assigning False to
    # Header.is_linked_to_previous

    >>> header.is_linked_to_previous
    True
    >>> header.is_linked_to_previous = False
    >>> header.is_linked_to_previous
    False

    # after setting is_linked_to_previous = False, the variable header changes
    # from the header from the previous section to a new blank header on the
    # current section.

    # Conversely, a header can be deleted from a section by assigning True to
    # Header.is_linked_to_previous

    >>> header.is_linked_to_previous
    False
    # There's a bit of a conundrum here, where .is_linked_to_previous can be
    # True on the first section, even though by definition there can't be a
    # previous section. For the first section, "is_linked_to_previous" is
    # really just a way to create blank headers or delete headers.

    >>> header.is_linked_to_previous = True
    >>> header.is_linked_to_previous
    True

    >>> document.settings.odd_and_even_pages_header_footer = True
    >>> header = document.sections[0].header
    # if odd_and_even_pages_header_footer is False, then header will be on all pages
    # if odd_and_even_pages_header_footer is True, then header will be on odd pages

    >>> even_header = document.sections[0].even_header
    >>> even_header.add_paragraph('foobar')
    # creates a new blank even_header
    # if odd_and_even_pages_header_footer is False, then even_header will be present
    # but not displayed
    # if odd_and_even_pages_header_footer is True, then even_header will be displayed
    # on even pages

    >>> section = document.sections[2]
    >>> section.different_first_page_header_footer
    False
    >>> section.different_first_page_header_footer = True
    >>> section.different_first_page_header_footer
    True

    >>> first_page_header = document.sections[0].first_page_header
    >>> first_page_header.add_paragraph('barbar')
    # if section.different_first_page_header_footer is True, the first_page_header is
    # displayed on the first page of the section
    # if section.different_first_page_header_footer is False, the first_page_header is
    # not displayed
    # by default new sections have different_first_page_header_footer set to False

    # Header.text - read/write, full text, no character formatting, \n for line
    # break, \n\n for paragraph (or whatever other .text bits do). Assignment can
    # only be a single paragraph; can include tabs and line breaks, but no
    # paragraphs.


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


Now just an odd header. The section is exactly the same as above but
`settings.xml` has the the `<w:evenAndOddHeaders>` property:

.. code-block:: xml

   <w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
      ...
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
      <xsd:sequence>
        <xsd:element name="writeProtection"            type="CT_WriteProtection" minOccurs="0"/>
        <xsd:element name="view"                       type="CT_View"            minOccurs="0"/>
        <xsd:element name="zoom"                       type="CT_Zoom"            minOccurs="0"/>
        <xsd:element name="removePersonalInformation"  type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="removeDateAndTime"          type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="doNotDisplayPageBoundaries" type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="displayBackgroundShape"     type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="printPostScriptOverText"    type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="printFractionalCharacterWidth" type="CT_OnOff"        minOccurs="0"/>
        <xsd:element name="printFormsData"             type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="embedTrueTypeFonts"         type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="embedSystemFonts"           type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="saveSubsetFonts"            type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="saveFormsData"              type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="mirrorMargins"              type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="alignBordersAndEdges"       type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="bordersDoNotSurroundHeader" type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="bordersDoNotSurroundFooter" type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="gutterAtTop"                type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="hideSpellingErrors"         type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="hideGrammaticalErrors"      type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="activeWritingStyle"         type="CT_WritingStyle"    minOccurs="0" maxOccurs="unbounded"/>
        <xsd:element name="proofState"                 type="CT_Proof"           minOccurs="0"/>
        <xsd:element name="formsDesign"                type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="attachedTemplate"           type="CT_Rel"             minOccurs="0"/>
        <xsd:element name="linkStyles"                 type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="stylePaneFormatFilter"      type="CT_StylePaneFilter" minOccurs="0"/>
        <xsd:element name="stylePaneSortMethod"        type="CT_StyleSort"       minOccurs="0"/>
        <xsd:element name="documentType"               type="CT_DocType"         minOccurs="0"/>
        <xsd:element name="mailMerge"                  type="CT_MailMerge"       minOccurs="0"/>
        <xsd:element name="revisionView"               type="CT_TrackChangesView" minOccurs="0"/>
        <xsd:element name="trackRevisions"             type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="doNotTrackMoves"            type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="doNotTrackFormatting"       type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="documentProtection"         type="CT_DocProtect"      minOccurs="0"/>
        <xsd:element name="autoFormatOverride"         type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="styleLockTheme"             type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="styleLockQFSet"             type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="defaultTabStop"             type="CT_TwipsMeasure"    minOccurs="0"/>
        <xsd:element name="autoHyphenation"            type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="consecutiveHyphenLimit"     type="CT_DecimalNumber"   minOccurs="0"/>
        <xsd:element name="hyphenationZone"            type="CT_TwipsMeasure"    minOccurs="0"/>
        <xsd:element name="doNotHyphenateCaps"         type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="showEnvelope"               type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="summaryLength"              type="CT_DecimalNumberOrPrecent" minOccurs="0"/>
        <xsd:element name="clickAndTypeStyle"          type="CT_String"          minOccurs="0"/>
        <xsd:element name="defaultTableStyle"          type="CT_String"          minOccurs="0"/>
        <xsd:element name="evenAndOddHeaders"          type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="bookFoldRevPrinting"        type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="bookFoldPrinting"           type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="bookFoldPrintingSheets"      type="CT_DecimalNumber"   minOccurs="0"/>
        <xsd:element name="drawingGridHorizontalSpacing"        type="CT_TwipsMeasure"  minOccurs="0"/>
        <xsd:element name="drawingGridVerticalSpacing"          type="CT_TwipsMeasure"  minOccurs="0"/>
        <xsd:element name="displayHorizontalDrawingGridEvery"   type="CT_DecimalNumber" minOccurs="0"/>
        <xsd:element name="displayVerticalDrawingGridEvery"     type="CT_DecimalNumber" minOccurs="0"/>
        <xsd:element name="doNotUseMarginsForDrawingGridOrigin" type="CT_OnOff"         minOccurs="0"/>
        <xsd:element name="drawingGridHorizontalOrigin"         type="CT_TwipsMeasure"  minOccurs="0"/>
        <xsd:element name="drawingGridVerticalOrigin"  type="CT_TwipsMeasure"    minOccurs="0"/>
        <xsd:element name="doNotShadeFormData"         type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="noPunctuationKerning"       type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="characterSpacingControl"    type="CT_CharacterSpacing" minOccurs="0"/>
        <xsd:element name="printTwoOnOne"              type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="strictFirstAndLastChars"    type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="noLineBreaksAfter"          type="CT_Kinsoku"         minOccurs="0"/>
        <xsd:element name="noLineBreaksBefore"         type="CT_Kinsoku"         minOccurs="0"/>
        <xsd:element name="savePreviewPicture"         type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="doNotValidateAgainstSchema" type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="saveInvalidXml"             type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="ignoreMixedContent"         type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="alwaysShowPlaceholderText"  type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="doNotDemarcateInvalidXml"   type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="saveXmlDataOnly"            type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="useXSLTWhenSaving"          type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="saveThroughXslt"            type="CT_SaveThroughXslt" minOccurs="0"/>
        <xsd:element name="showXMLTags"                type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="alwaysMergeEmptyNamespace"  type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="updateFields"               type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="hdrShapeDefaults"           type="CT_ShapeDefaults"   minOccurs="0"/>
        <xsd:element name="footnotePr"                 type="CT_FtnDocProps"     minOccurs="0"/>
        <xsd:element name="endnotePr"                  type="CT_EdnDocProps"     minOccurs="0"/>
        <xsd:element name="compat"                     type="CT_Compat"          minOccurs="0"/>
        <xsd:element name="docVars"                    type="CT_DocVars"         minOccurs="0"/>
        <xsd:element name="rsids"                      type="CT_DocRsids"        minOccurs="0"/>
        <xsd:element  ref="m:mathPr"                                             minOccurs="0"/>
        <xsd:element name="attachedSchema"             type="CT_String"          minOccurs="0" maxOccurs="unbounded"/>
        <xsd:element name="themeFontLang"              type="CT_Language"        minOccurs="0"/>
        <xsd:element name="clrSchemeMapping"           type="CT_ColorSchemeMapping" minOccurs="0"/>
        <xsd:element name="doNotIncludeSubdocsInStats" type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="doNotAutoCompressPictures"  type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="forceUpgrade"               type="CT_Empty"           minOccurs="0"/>
        <xsd:element name="captions"                   type="CT_Captions"        minOccurs="0"/>
        <xsd:element name="readModeInkLockDown"        type="CT_ReadingModeInkLockDown" minOccurs="0"/>
        <xsd:element name="smartTagType"               type="CT_SmartTagType"    minOccurs="0" maxOccurs="unbounded"/>
        <xsd:element  ref="sl:schemaLibrary"                                     minOccurs="0"/>
        <xsd:element name="shapeDefaults"              type="CT_ShapeDefaults"   minOccurs="0"/>
        <xsd:element name="doNotEmbedSmartTags"        type="CT_OnOff"           minOccurs="0"/>
        <xsd:element name="decimalSymbol"              type="CT_String"          minOccurs="0"/>
        <xsd:element name="listSeparator"              type="CT_String"          minOccurs="0"/>
      </xsd:sequence>
    </xsd:complexType>
