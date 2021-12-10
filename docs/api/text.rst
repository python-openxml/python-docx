
.. _text_api:

Text-related objects
====================


|Paragraph| objects
-------------------

.. autoclass:: docx.text.paragraph.Paragraph()
   :members:


|ParagraphFormat| objects
-------------------------

.. autoclass:: docx.text.parfmt.ParagraphFormat()
   :members:


|Run| objects
-------------

.. autoclass:: docx.text.run.Run()
   :members:


|Font| objects
--------------

.. autoclass:: docx.text.run.Font()
   :members:


|TabStop| objects
-----------------

.. autoclass:: docx.text.tabstops.TabStop()
   :members:


|TabStops| objects
------------------

.. autoclass:: docx.text.tabstops.TabStops()
   :members: clear_all

   .. automethod:: docx.text.tabstops.TabStops.add_tab_stop(position, alignment=WD_TAB_ALIGNMENT.LEFT, leader=WD_TAB_LEADER.SPACES)
