
.. _shared_api:

Shared classes
==============

.. currentmodule:: docx.shared


Length objects
--------------

Length values in |docx| are expressed as a standardized |Length| value object.
|Length| is a subclass of |int|, having all the behavior of an |int|. In
addition, it has built-in units conversion properties, e.g.::

    >>> inline_shape.height
    914400
    >>> inline_shape.height.inches
    1.0

Length objects are constructed using a selection of convenience constructors,
allowing values to be expressed in the units most appropriate to the context.

.. autoclass:: Length
   :members:
   :member-order: bysource

.. autoclass:: Inches
   :members:

.. autoclass:: Cm
   :members:

.. autoclass:: Mm
   :members:

.. autoclass:: Pt
   :members:

.. autoclass:: Twips
   :members:

.. autoclass:: Emu
   :members:


|RGBColor| objects
------------------

.. autoclass:: RGBColor(r, g, b)
   :members:
   :undoc-members:

   `r`, `g`, and `b` are each an integer in the range 0-255 inclusive. Using
   the hexidecimal integer notation, e.g. `0x42` may enhance readability
   where hex RGB values are in use::

       >>> lavender = RGBColor(0xff, 0x99, 0xcc)
