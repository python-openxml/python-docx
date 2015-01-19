
.. _style_api:

Style-related objects
=====================

A style is used to collect a set of formatting properties under a single name
and apply those properties to a content object all at once. This promotes
formatting consistency thoroughout a document and across related documents
and allows formatting changes to be made globally by changing the definition
in the appropriate style.

.. currentmodule:: docx.styles.style


|BaseStyle| objects
-------------------

.. autoclass:: BaseStyle()
   :members:
   :inherited-members:
   :exclude-members:
       part, style_id


|_CharacterStyle| objects
-------------------------

.. autoclass:: _CharacterStyle()
   :show-inheritance:
   :members:
   :inherited-members:
   :exclude-members:
       element, part, style_id, type


|_ParagraphStyle| objects
-------------------------

.. autoclass:: _ParagraphStyle()
   :show-inheritance:
   :members:
   :inherited-members:
   :exclude-members:
       element, part, style_id, type


|_TableStyle| objects
---------------------

.. autoclass:: _TableStyle()
   :show-inheritance:
   :members:
   :inherited-members:
   :exclude-members:
       element, part, style_id, type


|_NumberingStyle| objects
-------------------------

.. autoclass:: _NumberingStyle()
   :members:
