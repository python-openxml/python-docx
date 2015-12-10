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

The footer if present also needs to be added. Its ``ContentType`` should be ``application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml``.

5. /word/_rels/header1.xml.rels (OPTIONAL)
------------------------------------------

If the header has an image, it will also need to have its relationships file.

Suppose the header above had an image stored at ``/word//media/image1.png``:

.. code-block:: xml

   <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
   <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
     <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image1.png"/>
   </Relationships>

Note on Styles:
---------------

The header and footer has access to all the normal styles defined in ``/word/styles.xml``.


Candidate Protocol
==================

The following methods are added to the main_document_part (aka docx.document.Document)

.. code-block:: python

   class Document(ElementProxy):
       def clear_headers(self):
           """ clears all headers from a docx
           """

       def add_header(self):
           """ removes all existing headers from a docx then adds a new footer
           :returns: a new Header instance
           """

       def clear_footers(self):
           """ clears all footers from a docx
           """

       def add_footer(self):
           """ removes all existing footers from a docx then adds a new footer
           :returns: a new Footer instance
           """


(Note: a file could contain multiple headers or footers but the proposed protocol below only allows
adding a single header / footer for now, for simplicities sake.

Documents with multiple heaeders will reuetrn )

Header
------

.. code-block:: python

   class Header(BlockItemContainer):
       """ Proxy object wrapping around a CT_Hdr <w:hdr> element

       paragraph = header.add_paragraph()
       run_text = paragraph.add_run('foobar', style='FOO')
       run_img = paragraph.add_run()
       run_img.add_picture(logo, width, height)
       """
       pass

Footer
------

.. code-block:: python

   class Footer(BlockItemContainer):
       """ Proxy object wrapping around a CT_Ftr <w:ftr> element

       paragraph = footer.add_paragraph()
       run_text = paragraph.add_run('foobar', style='FOO')
       run_img = paragraph.add_run()
       run_img.add_picture(logo, width, height)
       """
       pass



What currently works:

Clear Headers / Footers.
Add Header / Footer.
Add Header / Footer paragraph with style.
Add Header / Footer paragraph run with style.
Add Header / Footer paragraph run with image.
Add Header / Footer paragraph run with other inline shapes (probably).

What might not work so hot:

Editing existing headers easily.

What does not work:

Adding a second header to a document that already has a header.
(The `document.add_header` method clears all headers first.)
But this sounds like an edge case. Maybe it's not needed.
