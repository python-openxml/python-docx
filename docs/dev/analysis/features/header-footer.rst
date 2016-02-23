=================
Header and Footer
=================

Word supports headers and footers on documents. Headers and footers can include paragraphs with styles, text, and images.

Many documents use headers in order to have a logo at the top of every page.

Or use a footer to have company contact information at the bottom of every page.

For brevity in the discussion below I will occasionally use the term *header* to refer to either a header and footer object, trusting the reader to understand its applicability to either type of object.

Structure
=========

For the sake of simplicity, we will assume we have a single header applied to all pages.

This header consists of five parts:

1. /word/header1.xml
--------------------

This file contains the header contents. It could be named anything but it is often named header1.

A file can contain multiple headers. Each one should be stored in a different file:
``/word/header1.xml``, ``/word/header2.xml``, etc.

Here's a simple example:

.. code-block:: xml

   <w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
   <w:p>
       <w:pPr>
           <w:pStyle w:val="Header" />
           <w:rPr />
       </w:pPr>
       <w:r>
           <w:rPr />
           <w:t>This is a header.</w:t>
       </w:r>
   </w:p>
   </w:hdr>

Footers are identical to headers except they use the ``<w:ftr>`` tag instead of ``<w:hdr>``.

2. /word/_rels/document.xmls.rels
---------------------------------

This file contains unique relationship ids between all the different parts of a document: settings, styles, numbering, images, themes, fonts, etc.

When a header, it too will have a unique relationship id.

Here's an example, with the header as defined above having ``rId3``:

.. code-block:: xml

   <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
     <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
     <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
     <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>
   </Relationships>

3. /word/document.xml
---------------------

This file is the motherload: it contains the bulk of the document contents.

With respect to the headers though, this file contains very little: all it contains is a reference to the header in the sentinel sectPr (the final and often only sectPr in a document just before the closing body tag) via the relationship id defined in ``/word/_rels/document.xml.rels``

Here's an example, again with the ``header1.xml`` as ``rId3``:

.. code-block:: xml

   <w:body>
       ...
       <w:sectPr>
           <w:headerReference w:type="default" r:id="rId3"/>
           <w:pgSz w:w="12240" w:h="15840"/>
           <w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800" w:header="720" w:footer="720" w:gutter="0"/>
           <w:cols w:space="720"/>
           <w:docGrid w:linePitch="360"/>
       </w:sectPr>
   </w:body>

Footers are identical to headers except they use the ``<w:footerReference>``
instead of the ``<w:headerReference>`` tag.

The ``<w:headerReference>`` (if present) should be the first element of the sentinel sectPr, and the ``<w:footerReference>`` should be the next element.  (The OpenXML SDK 2.5 docx validator gives a warning if the ``<w:headerReference>`` is not the first element.)

4. [Content Types].xml
-----------------------

If the header is present, it needs to be added to the ``[Content Types].xml`` file. Like so:

.. code-block:: xml

   <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
   <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
     <Default Extension="xml" ContentType="application/xml"/>
     <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
     <Default Extension="jpeg" ContentType="image/jpeg"/>
     <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
     <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
     <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
     <Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>
   </Types>

The footer if present also needs to be added. Its ``ContentType`` should be

.. code-block:: xml

    "application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"

All header and footer files referenced in document.xml.rels need to be added to ``[Content Types].xml.``


5. /word/_rels/header1.xml.rels
-------------------------------

(OPTIONAL) This file is only present if the header has an image.

This is the header's relationships file. It is similar to the document's relationships file at ``/word/_rels/document.xml.rels``.

This file is stored with the same name as the header xml file under ``/word/_rels/``.

Suppose the header above had an image stored at ``/word/media/image1.png``.

The relationships file would be stored ``/word/_rels/header1.xml.rels``. It will look like this:

.. code-block:: xml

   <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
   <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
     <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image1.png"/>
   </Relationships>

Note the ``rIds`` of the header are completely independent of the relationships of the main ``document.xml``.


All Pages, Even Pages, Odd Pages, First Page
--------------------------------------------

There are seven different permutations of headers:

1. All Pages
~~~~~~~~~~~~

This most basic scenario was used above. When there is a single header of type ``default`` and ``settings.xml`` does not contain the ``w:evenAndOddHeaders`` element, then the header will appear on every page.

.. code-block:: xml

   <!-- document.xml -->
   <w:body>
       ...
       <w:sectPr>
           <w:headerReference w:type="default" r:id="rId3"/>
           <w:pgSz w:w="12240" w:h="15840"/>
           <w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800" w:header="720" w:footer="720" w:gutter="0"/>
           <w:cols w:space="720"/>
           <w:docGrid w:linePitch="360"/>
       </w:sectPr>
   </w:body>


2. Odd Pages
~~~~~~~~~~~~

The next scenario is just an odd header. In this scenario the ``document.xml`` is exactly the same as above, but the ``settings.xml`` contains the ``w:evenAndOddHeaders`` element.


3. Even Pages
~~~~~~~~~~~~~

In this scenario the ``settings.xml`` contains the ``w:evenAndOddHeaders`` element. And the ``document.xml`` looks exactly the same as the odd page scenario, except the ``w:type`` of the ``w:headerReference`` has changed from ``default`` to ``even``.

.. code-block:: xml

   <!-- document.xml -->
   <w:body>
       ...
       <w:sectPr>
           <w:headerReference w:type="even" r:id="rId3"/>
           <w:pgSz w:w="12240" w:h="15840"/>
           <w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800" w:header="720" w:footer="720" w:gutter="0"/>
           <w:cols w:space="720"/>
           <w:docGrid w:linePitch="360"/>
       </w:sectPr>
   </w:body>


4. Even and Odd Pages
~~~~~~~~~~~~~~~~~~~~~

In this scenario the document has two different headers: one for even pages, and another for odd pages. The ``settings.xml`` contains the ``w:evenAndOddHeaders`` element. And the ``document.xml`` has two ``w:headerReferences``:

.. code-block:: xml

   <!-- document.xml -->
   <w:body>
       ...
       <w:sectPr>
           <w:headerReference w:type="default" r:id="rId3"/>
           <w:headerReference w:type="even" r:id="rId4"/>
           <w:pgSz w:w="12240" w:h="15840"/>
           <w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800" w:header="720" w:footer="720" w:gutter="0"/>
           <w:cols w:space="720"/>
           <w:docGrid w:linePitch="360"/>
       </w:sectPr>
   </w:body>


5. First Page
~~~~~~~~~~~~~

In this scenario a header appears on the first page and only the first page. The ``settings.xml`` may or may not contain the ``w:evenAndOddHeaders`` element. And the ``document.xml`` has a single ``w:headerReference`` of type ``first``:

.. code-block:: xml

   <!-- document.xml -->
   <w:body>
       ...
       <w:sectPr>
           <w:headerReference w:type="first" r:id="rId3"/>
           <w:pgSz w:w="12240" w:h="15840"/>
           <w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800" w:header="720" w:footer="720" w:gutter="0"/>
           <w:cols w:space="720"/>
           <w:docGrid w:linePitch="360"/>
       </w:sectPr>
   </w:body>


6. First Page Then All Pages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this scenario one header appears on the first page and a different header appears on all subsequent pages. The ``settings.xml`` does not contain the ``w:evenAndOddHeaders`` element. And the ``document.xml`` has two ``w:headerReferences``:

.. code-block:: xml

   <!-- document.xml -->
   <w:body>
       ...
       <w:sectPr>
           <w:headerReference w:type="default" r:id="rId3"/>
           <w:headerReference w:type="first" r:id="rId4"/>
           <w:pgSz w:w="12240" w:h="15840"/>
           <w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800" w:header="720" w:footer="720" w:gutter="0"/>
           <w:cols w:space="720"/>
           <w:docGrid w:linePitch="360"/>
       </w:sectPr>
   </w:body>


7. First Page Then Even/Odd Pages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this scenario one header appears on the first page, and then alternating even/odd headers appear on all subsequent pages. The ``settings.xml`` contains the ``w:evenAndOddHeaders`` element. And the ``document.xml`` has two ``w:headerReferences``:

.. code-block:: xml

   <!-- document.xml -->
   <w:body>
       ...
       <w:sectPr>
           <w:headerReference w:type="default" r:id="rId3"/>
           <w:headerReference w:type="first" r:id="rId4"/>
           <w:headerReference w:type="even" r:id="rId5"/>
           <w:pgSz w:w="12240" w:h="15840"/>
           <w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800" w:header="720" w:footer="720" w:gutter="0"/>
           <w:cols w:space="720"/>
           <w:docGrid w:linePitch="360"/>
       </w:sectPr>
   </w:body>

It's also theoretically possible to have a first page header then just an even page header, or a first page then just an odd page header.


Note on Styles:
---------------

The header and footer has access to all the normal styles defined in ``/word/styles.xml``.


Candidate Protocol
==================

Section
-------

headers
-------

:class:`docx.section.Section` has a read_only ``headers`` property which is a list of headers
in the section of type :class:`docx.header.Header`:

.. code-block:: python

   >>> from docx import Document
   >>> document = Document('document_with_single_header.docx')
   >>> section = document.sections[-1]
   >>> isinstance(section.headers, list)
   True
   >>> len(section.headers)
   1
   >>> section.headers[0]
   <docx.Header object at 0xdeadbeef0>

This property is present in the MS API: https://msdn.microsoft.com/en-us/library/office/ff820779.aspx

header
----------------

read-only property, returns the default type header if present, else ``None``

even_page_header
----------------

read-only property, returns the even page header if present, else ``None``

In theory an odd_page_header property could also be added. But for v1 we can just leave that to the user to figure out where their ``default`` header represents an all-pages header and when it represents an odd-page header.

first_page_header
-----------------

read-only property, returns the first page header if present, else ``None``

clear_headers
-------------

:class:`docx.section.Section` has a ``clear_headers`` method which removes all headers
from the section

.. code-block:: python

   >>> from docx import Document
   >>> document = Document('document_with_single_header.docx')
   >>> section = document.sections[-1]
   >>> section.clear_headers()
   >>> len(section.headers)
   0

If you wanted to clear all headers from every section you could iterate over every section and call ``clear_headers`` on each.

By default the sections will then inherit the headers you define on the ``w:sectPr`` of ``w:body``. (TODO: IS THIS TRUE? CONFIRM!)

This method also removes the ``<w:evenAndOddHeaders/>`` element from ``settings.xml`` so that any subsequent headers added are added to all pages.


add_header
-------------

:class:`docx.section.Section` has an ``add_header`` method which adds an instance
of type :class:`docx.header.Header` with no text to the document and returns the new
header instance.

.. code-block:: python

   >>> from docx import Document
   >>> document = Document('document_without_header.docx')
   >>> section = document.sections[-1]
   >>> header = section.add_header()
   >>> isinstance(header, Header)
   True
   >>> header.type
   'default'

:class:`docx.section.Section`'s ``add_header`` method will raise an ``Exception`` (of type ?)
if a header of type default already exists on the document.

.. code-block:: python

   >>> from docx import Document
   >>> document = Document('document_with_default_header.docx')
   >>> section = document.sections[-1]
   >>> section.add_header()
   *** Exception: Document already has a default header!

The user should remove the existing header explicitly with clear_headers and then they can add a header.

add_even_page_header
--------------------

:class:`docx.section.Section` has an ``add_even_page_header`` method which adds the
``<w:evenAndOddHeaders/>`` element to ``settings.xml`` (if not already present)
and adds a header of type :class:`docx.header.Header` with no text to the document, and returns the new
header instance.

.. code-block:: python

   >>> from docx import Document
   >>> document = Document('document_without_header.docx')
   >>> section = document.sections[-1]
   >>> header = section.add_even_page_header()
   >>> isinstance(header, Header)
   True

:class:`docx.section.Section`'s ``add_even_page_header`` method will raise an ``Exception`` (of type ?)
if a header of type even already exists on the document.

.. code-block:: python

   >>> from docx import Document
   >>> document = Document('document_with_even_header.docx')
   >>> section = document.sections[-1]
   >>> section.add_even_page_header()
   *** Exception: Document already has an even header!

NOTE:

Because ``add_even_page_header`` implicitly sets the ``<w:evenAndOddHeaders/>`` property of ``settings.xml``, this could confuse people.

If they want to add a header to every page, they may need to remove all headers with ``clear_headers`` and then call ``add_header`` if a document already has ``<w:evenAndOddHeaders/>``.

Still, that seems like the simplest way to expose this functionality so that users of the API don't have to understand all the internal implementation details of headers.

Especially if in the docs it is specified that for even/odd page headers you first call ``add_header`` then call ``add_even_page_header``.

And the docs should also point out, if you want to add headers to a document that might already have them, it is generally a good idea to call ``clear_headers`` first then add your headers.

add_first_page_header
---------------------

:class:`docx.section.Section` has an ``add_first_page_header`` method adds a header of type :class:`docx.header.Header` with no text to the document, and returns the new header instance.

.. code-block:: python

   >>> from docx import Document
   >>> document = Document('document_without_header.docx')
   >>> section = document.sections[-1]
   >>> header = section.add_first_page_header()
   >>> isinstance(header, Header)
   True

:class:`docx.section.Section`'s ``add_first_page_header`` method will raise an ``Exception`` (of type ?)
if a header of type first already exists on the document.

.. code-block:: python

   >>> from docx import Document
   >>> document = Document('document_with_first_header.docx')
   >>> section = document.sections[-1]
   >>> section.add_first_page_header()
   *** Exception: Document already has a first header!


Header
======

A :class:`docx.header.Header` instance behaves just like any other BlockItemContainer subclass
(e.g. ``_Body``).

header.add_paragraph
--------------------
Headers possesses methods for adding and removing child paragraphs, which in turn
have methods for adding and removing runs.

.. code-block:: python

   from docx.text.run import Run
   from docx.text.paragraph import Paragraph
   >>> paragraph = header.add_paragraph()
   >>> isinstance(paragraph, Paragraph)
   True
   >>> run1 = paragraph.add_run('Some text for the header')
   >>> isinstance(run1, Run)
   True
   >>> run2 = paragraph.add_run('More text for the header')
   >>> isinstance(run2, Run)
   True

A :class:`docx.text.run.Run` instance inside of a :class:`docx.header.Header` can add an image.

.. code-block:: python

   >>> from docx.shared import Pt
   >>> from docx.shape import InlineShape
   >>> width = Pt(160)
   >>> height = Pt(40)
   >>> picture = run2.add_picture('/logo.png', width, height)
   >>> isinstance(picture, InlineShape)
   True

Styles work in the normal way on both paragraphs and runs.

footer stuff
------------

:class:`docx.document.Document` has all the same methods for footers.
