=================
Header and Footer
=================

Word supports headers and footers on documents. Headers and footers can include paragraphs with styles, text, and images.

Many documents use headers in order to have a logo at the top of every page.

Or use a footer to have company contact information at the bottom of every page.

Structure
=========

A header consists of five parts:

1. /word/header1.xml
--------------------

This file contains the header contents. It could be named anything but it is often named header1.

A file can contain multiple headers and/or multiple footers. Each one should be stored in a different file:
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

When a header or footer is present, it too will have a unique relationship id.

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

With respect to the headers or footers though, this file contains very little:
all it contains is a reference to the header or footer in the sentinel sectPr
(the final and often only sectPr in a document just before the closing body tag)
via the relationship id defined in ``/word/_rels/document.xml.rels``

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

The ``<w:headerReference>`` (if present) should be the first element of the sentinel sectPr,
and the ``<w:footerReference>`` should be the next element.
(The OpenXML SDK 2.5 docx validator gives a warning if the ``<w:headerReference>``
is not the first element.)

4. /[Content Types].xml
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

Note on Styles:
---------------

The header and footer has access to all the normal styles defined in ``/word/styles.xml``.


Candidate Protocol
==================

headers
-------

:class:`docx.document.Document` has a ``headers`` property which is a list of headers
in the document of type :class:`docx.header.Header`:

.. code-block:: python

   >>> from docx import Document
   >>> document = Document('document_with_single_header.docx')
   >>> isinstance(document.headers, list)
   True
   >>> len(document.headers)
   1
   >>> header = document.headers[0]
   >>> isinstance(header, Header)
   True

clear_headers
-------------

:class:`docx.document.Document` has a ``clear_headers`` method which removes all headers
from the document

.. code-block:: python

   >>> from docx import Document
   >>> document = Document('document_with_single_header.docx')
   >>> document.clear_headers()
   >>> len(document.headers)
   0

add_header
-------------

:class:`docx.document.Document` has an ``add_header`` method which adds an instance
of type :class:`docx.header.Header` with no text to the document and returns the new
header instance.

.. code-block:: python

   >>> from docx import Document
   >>> document = Document('document_without_header.docx')
   >>> header = document.add_header()
   >>> isinstance(header, Header)
   True

:class:`docx.document.Document`'s ``add_header`` method will raise an ``Exception`` (of type ?)
if a header already exists on the document.

.. code-block:: python

   >>> from docx import Document
   >>> document = Document('document_with_single_header.docx')
   >>> document.add_header()
   *** Exception: Document has one or more headers. Remove those headers first!

The user should remove the existing headers explicitly and then they can add a header.

.. code-block:: python

   >>> document.clear_headers()
   >>> header = document.add_header()
   >>> isinstance(header, Header)
   True

In the future I hope to add support for adding multiple headers,
but for simplicity's sake, I'd like to leave it out for now.

header.add_paragraph
--------------------

A :class:`docx.header.Header` instance behaves just like any other BlockItemContainer subclass
(e.g. ``_Body``).
It possesses methods for adding and removing child paragraphs, which in turn
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

:class:`docx.document.Document` has all the same methods for footers
(``footers``, ``clear_footers``, ``add_footers``)
