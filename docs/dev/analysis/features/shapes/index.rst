
Shapes (in general)
===================

A graphical object that appears in a Word document is known as a `shape`.
A shape can be `inline` or `floating`. An inline shape appears on a text
baseline as though it were a character glyph and affects the line height.
A floating shape appears at an arbitrary location on the document and text may
wrap around it. Several types of shape can be placed, including a picture, a
chart, and a drawing canvas.

The graphical object itself is placed in a container, and it is the container
that determines the placement of the graphic. The same graphical object can be
placed inline or floating by changing its container. The graphic itself is
unaffected.

In addition to this overview, there are the following more specialized
feature analyses:

.. toctree::
   :titlesonly:

   shapes-inline
   shapes-inline-size
   picture


MS API
------

Access to shapes is provided by the Shapes and InlineShapes properties on the
Document object.

The API for a floating shape overlaps that for an inline shapes, but there are
substantial differences. The following properties are some of those common to
both:

* Fill
* Glow
* HasChart
* HasSmartArt
* Height
* Shadow
* Hyperlink
* PictureFormat (providing brightness, color, crop, transparency, contrast)
* Type (Chart, LockedCanvas, Picture, SmartArt, etc.)
* Width


Resources
---------

* `Document Members (Word) on MSDN`_
* `InlineShape Members (Word) on MSDN`_
* `InlineShapes Members (Word) on MSDN`_
* `Shape Members (Word) on MSDN`_

.. _Document Members (Word) on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff840898.aspx

.. _InlineShape Members (Word) on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff840794.aspx

.. _InlineShapes Members (Word) on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff836984.aspx

.. _Shape Members (Word) on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff195191.aspx
