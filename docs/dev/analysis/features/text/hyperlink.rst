
Hyperlink
=========

Word allows hyperlinks to be placed in the document or existing objects to be
turned into hyperlinks.

Hyperlinks can point to a named object or range within the current document or
to an external resource. Hyperlinks can contain multiple runs of text.


Candidate protocol
------------------

Add a simple hyperlink with text and url:

    >>> hyperlink = paragraph.add_hyperlink(text='Google', url='http://google.com')
    >>> hyperlink.text
    'Google'
    >>> hyperlink.url
    'http://google.com'
    >>> hyperlink.anchor
    None
    >>> len(hyperlink.runs)
    1

Add multiple runs to a hyperlink:

    >>> hyperlink = paragraph.add_hyperlink(url='http://github.com')
    >>> hyperlink.add_run('A')
    >>> hyperlink.add_run('formatted').italic = True
    >>> hyperlink.add_run('link').bold = True
    >>> len(hyperlink.runs)
    3

Add a hyperlink pointing to a named range in the current document:

    >>> hyperlink = paragraph.add_hyperlink(text='Section 1', anchor='section1')
    >>> hyperlink.anchor
    'section1'
    >>> hyperlink.url
    None

Turning an existing object into a hyperlink:

    >>> existing_object = document.add_paragraph('Some text')
    >>> hyperlink = existing_object.hyperlink(url='http://google.com')
    >>> hyperlink.text
    'Some text'
    >>> len(hyperlink.runs)
    1


Specimen XML
------------

.. highlight:: xml

A simple hyperlink to an external url::

  <w:hyperlink r:id="rId9">
    <w:r>
      <w:rPr>
        <w:rStyle w:val="Hyperlink"/>
      </w:rPr>
      <w:t>Google</w:t>
    </w:r>
  </w:hyperlink>


The relationship for the above url::

    <Relationships xmlns="…">
      <Relationship Id="rId9" Mode="External" Target=http://google.com />
    </Relationships>

A hyperlink to an internal named range::

    <w:hyperlink r:anchor="section1">
      <w:r>
        <w:rPr>
          <w:rStyle w:val="Hyperlink"/>
        </w:rPr>
        <w:t>Google</w:t>
      </w:r>
    </w:hyperlink>

A hyperlink with multiple runs of text::

    <w:hyperlink r:id="rId2">
      <w:r>
        <w:rPr>
          <w:rStyle w:val="Hyperlink"/>
        </w:rPr>
        <w:t>A</w:t>
      </w:r>
      <w:r>
        <w:rPr>
          <w:rStyle w:val="Hyperlink"/>
          <w:i/>
        </w:rPr>
        <w:t xml:space="preserve">formatted</w:t>
      </w:r>
      <w:r>
        <w:rPr>
          <w:rStyle w:val="Hyperlink"/>
          <w:b/>
        </w:rPr>
        <w:t xml:space="preserve">link</w:t>
      </w:r>
    </w:hyperlink>


Resources
---------

* `Document Members (Word) on MSDN`_
* `Hyperlink Members (Word) on MSDN`_
* `Hyperlinks Members (Word) on MSDN`_
* `Hyperlink Class (OpenXML.Office2010.CustomUI) on MSDN`_
* `Hyperlink Class (OpenXML.Wordprocessing) on MSDN`_


.. _Document Members (Word) on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff840898.aspx

.. _Hyperlink Members (Word) on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff195109.aspx

.. _Hyperlinks Members (Word) on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff192421.aspx

.. _Hyperlink Class (OpenXML.Office2010.CustomUI) on MSDN:
   http://msdn.microsoft.com/en-us/library/documentformat.openxml.office2010.customui.hyperlink.aspx

.. _Hyperlink Class (OpenXML.Wordprocessing) on MSDN:
   http://msdn.microsoft.com/en-us/library/documentformat.openxml.wordprocessing.hyperlink.aspx


MS API
------

The Hyperlinks property on Document holds references to hyperlink
objects in the MS API.

Hyperlinks contain the following properties:

* Address
* SubAddress
* EmailSubject
* ExtraInfoRequired
* Range (In python-docx this would be the runs inside the hyperlink)
* ScreenTip
* Shape
* Target (where to open the hyperlink. e.g. "_blank", "_left", "_top", "_self", "_parent" etc)
* TextToDisplay
* Type (msoHyperlinkRange, msoHyperlinkShape or msoHyperlinkInlineShape)


Spec references
---------------

* 17.16.17 hyperlink (Hyperlink)
* 2.3.61 CT_Hyperlink
