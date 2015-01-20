
.. _style_api:

Style-related objects
=====================

A style is used to collect a set of formatting properties under a single name
and apply those properties to a content object all at once. This promotes
formatting consistency thoroughout a document and across related documents
and allows formatting changes to be made globally by changing the definition
in the appropriate style.


|Styles| objects
----------------

.. currentmodule:: docx.styles.styles

.. autoclass:: Styles()
   :members:
   :inherited-members:
   :exclude-members:
       get_by_id, get_style_id, part


|BaseStyle| objects
-------------------

.. currentmodule:: docx.styles.style

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


|LatentStyles| objects
----------------------

.. currentmodule:: docx.styles.latent

.. autoclass:: LatentStyles()
   :members:
   :inherited-members:
   :exclude-members:
       part


|_LatentStyle| objects
----------------------

.. autoclass:: _LatentStyle()
   :members:
   :inherited-members:
   :exclude-members:
       part
