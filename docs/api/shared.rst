
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

.. autoclass:: Emu
   :members:
