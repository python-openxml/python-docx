
Inline shape size
=================

The position of an inline shape is completely determined by the text it is
inline with, however its dimensions can be specified. For some shape types,
both the contained shape and the shape container specify a width and height.
In the case of a picture, the dimensions of the inline shape (container)
determine the display size while the dimension of the pic element determine the
"original size" of the image.


Candidate protocol -- inline shape access
-----------------------------------------

The following interactive session illustrates the protocol for accessing and
changing the size of an inline shape::

    >>> inline_shape = inline_shapes[0]
    >>> assert inline_shape.type == MSO_SHAPE_TYPE.PICTURE
    >>> inline_shape.width
    914400
    >>> inline_shape.height
    457200
    >>> inline_shape.width = 457200
    >>> inline_shape.height = 228600
    >>> inline_shape.width, inline_shape.height
    457200, 228600


Resources
---------

* `InlineShape Members (Word) on MSDN`_
* `Shape Members (Word) on MSDN`_

.. _InlineShape Members (Word) on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff840794.aspx

.. _Shape Members (Word) on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff195191.aspx


Specimen XML
------------

.. highlight:: xml

This XML represents an inline shape inserted inline on a paragraph by itself::

    <w:p>
      <w:r>
        <w:rPr/>
          <w:noProof/>
        </w:rPr>
        <w:drawing>
          <wp:inline distT="0" distB="0" distL="0" distR="0" wp14:anchorId="1BDE1558" wp14:editId="31E593BB">
            <wp:extent cx="859536" cy="343814"/>
            <wp:effectExtent l="0" t="0" r="4445" b="12065"/>
            <wp:docPr id="1" name="Picture 1"/>
            <wp:cNvGraphicFramePr>
              <a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>
            </wp:cNvGraphicFramePr>
            <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
              <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">

                <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
                  <pic:nvPicPr>
                    <pic:cNvPr id="1" name="python-powered.png"/>
                    <pic:cNvPicPr/>
                  </pic:nvPicPr>
                  <pic:blipFill>
                    <a:blip r:embed="rId7">
                      <a:alphaModFix/>
                      <a:extLst>
                        <a:ext uri="{28A0092B-C50C-407E-A947-70E740481C1C}">
                          <a14:useLocalDpi xmlns:a14="http://schemas.microsoft.com/office/drawing/2010/main" val="0"/>
                        </a:ext>
                      </a:extLst>
                    </a:blip>
                    <a:stretch>
                      <a:fillRect/>
                    </a:stretch>
                  </pic:blipFill>
                  <pic:spPr>
                    <a:xfrm>
                      <a:off x="0" y="0"/>
                      <a:ext cx="859536" cy="343814"/>
                    </a:xfrm>
                    <a:prstGeom prst="rect">
                      <a:avLst/>
                    </a:prstGeom>
                  </pic:spPr>
                </pic:pic>

              </a:graphicData>
            </a:graphic>
          </wp:inline>
        </w:drawing>
      </w:r>
    </w:p>
