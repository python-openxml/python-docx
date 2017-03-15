Shapes in Runs
==============

This document is aimed at accessing image information when reading docx files.  Adding image information as part of creating docx files is handled elsewhere.

A Run <w:r> can contain a Drawing <w:drawing>, which can can contain an Inline <wp:inline>, which can contain a Graphic <a:graphic>, which can contain graphicData <a:graphicData>, which can contain a Picture <pic:pic>.  A Picture can contain a blipFill <pic:blipFill> and a "Shape Properties" spPr <pic:spPr>.  A blipFill contains a Blip <a:blip> with an embed property that provides the graphic's Resource ID (rId) needed to look the image up in document.part.rels.  The spPr contains informtion about the image's size.  All of this except the Drawing element are documented in docs/dev/analysis/features/shapes/shapes-inline.rst.


Word Behavior
-------------

In theory, a Run can contain multiple Drawings.  In practice, I have not found a way to create a Run with more than a single Drawing.


Protocol
--------

.. highlight:: python

To stay parallel with document.add_picture() behavior, which creates an Inline object, the Run should have an Inlines property, producing a list of Inline objects.

  >>> inlines = run.inline_lst
  >>> inline = inlines[0]
  >>> inline
  <CT_Inline '<wp:inline>' at 0x43de510>
  
From here, we can access properties which characterize the image.

  >>> rId = inline.graphic.graphicData.pic.blipFill.blip.embed
  >>> rId
  'rId7'
  >>> cx, cy = inline.graphic.graphicData.pic.spPr.cx, inline.graphic.graphicData.pic.spPr.cy
  >>> cx.inches, cy.inches
  (4.61111111111, 2.33333333333)
  >>> document.part.rels[rId]._target.image.content_type
  'image/png'
  >>> rels[rId]._target.image.filename, rels[rId]._target.image.ext
  ('image.png', 'png')
  >>> originalx, originaly = rels[rId]._target.image.width, rels[rId]._target.image.height
  >>> originalx, originaly
  (4.61111111111, 2.33333333333)
  >>> image_data = rels[rId]._target.image.blob
  >>> len(image_data)
  23442
  
This interface, while (mostly) following Microsoft's object model (except for leaving out the Drawing level), seems unfriendly to the python_docx user.  Therefore, I would recommend the following additional interface elements.

  >>> pictures = run.picture_lst
  >>> picture = pictures[0]
  >>> picture.rId
  'rId7'
  >>> picture.cx.inches, picture.cy.inches, picture.originalx.inches, picture.originaly.inches
  (4.61111111111, 2.33333333333, 4.61111111111, 2.33333333333)
  >>> picture.content_type
  'image/png'
  >>> picture.filename, picture.ext
  ('media/image.png', 'png')
  >>> image_data = picture.image_data
  >>> f = open('image_export.%s' % picture.ext, 'wb')
  >>> f.write(image_data)
  >>> f.close()
  (produces a PNG image file named 'image_export.png' containing the image) 


Minimal XML
-----------

.. highlight:: xml

<w:drawing>
  <wp:inline>
    <a:graphic>
      <a:graphicData>
        <pic:pic>
          <pic:blipFill>
            <a:blip r:embed='rId7'>
            </a:blip>
          </pic:blipFill>
          <pic:spPr>
            (information about image offset and size)
          </pic:spPr>
        </pic:pic>
      </a:graphicData>
    </a:graphic>
  </wp:inline>
</w:drawing>

See documentation of CT_Inline, CT_GraphicalObject, CT_GraphicalObjectData, CT_Picture, CT_BlipFillProperties, and CT_Blip for more information.
                   
                   
Resources
---------

* `Document Members (Word) on MSDN`_
* `InlineShape Members (Word) on MSDN`_
* `Shape Members (Word) on MSDN`_

.. _Document Members (Word) on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff840898.aspx

.. _InlineShape Members (Word) on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff840794.aspx

.. _Shape Members (Word) on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff195191.aspx
