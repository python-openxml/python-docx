.. py:currentmodule:: docx.enum.text

.. _WdBreakType:

``WD_BREAK_TYPE``
=================

.. autoclass:: WD_BREAK_TYPE

   .. attribute:: COLUMN
      :annotation:

      Column break at the insertion point.

   .. attribute:: LINE
      :annotation:

      Line break.

   .. attribute:: LINE_CLEAR_LEFT
      :annotation:

      Line break.

   .. attribute:: LINE_CLEAR_RIGHT
      :annotation:

      Line break.

   .. attribute:: LINE_CLEAR_ALL
      :annotation:

      Line break. Equivalent to :attr:`TEXT_WRAPPING`.

   .. attribute:: PAGE
      :annotation:

      Page break at the insertion point.

   .. attribute:: SECTION_CONTINUOUS
      :annotation:

      New section without a corresponding page break.

   .. attribute:: SECTION_EVEN_PAGE
      :annotation:

      Section break with the next section beginning on the next
      even-numbered page. If the section break falls on an even-numbered
      page, Word leaves the next odd-numbered page blank.

   .. attribute:: SECTION_NEXT_PAGE
      :annotation:

      Section break on next page.

   .. attribute:: SECTION_ODD_PAGE
      :annotation:

      Section break with the next section beginning on the next
      odd-numbered page. If the section break falls on an odd-numbered
      page, Word leaves the next even-numbered page blank.

   .. attribute:: TEXT_WRAPPING
      :annotation:

      Ends the current line and forces the text to continue below a
      picture, table, or other item. The text continues on the next
      blank line that does not contain a table aligned with the left or
      right margin.
