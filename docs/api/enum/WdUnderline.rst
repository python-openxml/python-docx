.. py:currentmodule:: docx.enum.text

.. _WdUnderline:

``WD_UNDERLINE``
================

.. autoclass:: WD_UNDERLINE

   .. attribute:: NONE
      :annotation:

      No underline. This setting overrides any inherited underline
      value, so can be used to remove underline from a run that inherits
      underlining from its containing paragraph. Note this is not the
      same as assigning |None| to Run.underline. |None| is a valid
      assignment value, but causes the run to inherit its underline
      value. Assigning ``WD_UNDERLINE.NONE`` causes underlining to be
      unconditionally turned off.

   .. attribute:: SINGLE
      :annotation:

      A single line. Note that this setting is write-only in the sense
      that |True| (rather than ``WD_UNDERLINE.SINGLE``) is returned for
      a run having this setting.

   .. attribute:: WORDS
      :annotation:

      Underline individual words only.

   .. attribute:: DOUBLE
      :annotation:

      A double line.

   .. attribute:: DOTTED
      :annotation:

      Dots.

   .. attribute:: THICK
      :annotation:

      A single thick line.

   .. attribute:: DASH
      :annotation:

      Dashes.

   .. attribute:: DOT_DASH
      :annotation:

      Alternating dots and dashes.

   .. attribute:: DOT_DOT_DASH
      :annotation:

      An alternating dot-dot-dash pattern.

   .. attribute:: WAVY
      :annotation:

      A single wavy line.

   .. attribute:: DOTTED_HEAVY
      :annotation:

      Heavy dots.

   .. attribute:: DASH_HEAVY
      :annotation:

      Heavy dashes.

   .. attribute:: DOT_DASH_HEAVY
      :annotation:

      Alternating heavy dots and heavy dashes.

   .. attribute:: DOT_DOT_DASH_HEAVY
      :annotation:

      An alternating heavy dot-dot-dash pattern.

   .. attribute:: WAVY_HEAVY
      :annotation:

      A heavy wavy line.

   .. attribute:: DASH_LONG
      :annotation:

      Long dashes.

   .. attribute:: WAVY_DOUBLE
      :annotation:

      A double wavy line.

   .. attribute:: DASH_LONG_HEAVY
      :annotation:

      Long heavy dashes.
