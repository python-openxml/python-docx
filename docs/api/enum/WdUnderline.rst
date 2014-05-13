.. _WdUnderline:

``WD_UNDERLINE``
================

Specifies the style of underline applied to a run of characters.

----

NONE
    No underline. This setting overrides any inherited underline value, so can
    be used to remove underline from a run that inherits underlining from its
    containing paragraph. Note this is not the same as assigning |None| to
    Run.underline. |None| is a valid assignment value, but causes the run to
    inherit its underline value. Assigning ``WD_UNDERLINE.NONE`` causes
    underlining to be unconditionally turned off.

SINGLE
    A single line. Note that this setting is write-only in the sense that
    |True| (rather than ``WD_UNDERLINE.SINGLE``) is returned for a run having
    this setting.

WORDS
    Underline individual words only.

DOUBLE
    A double line.

DOTTED
    Dots.

THICK
    A single thick line.

DASH
    Dashes.

DOT_DASH
    Alternating dots and dashes.

DOT_DOT_DASH
    An alternating dot-dot-dash pattern.

WAVY
    A single wavy line.

DOTTED_HEAVY
    Heavy dots.

DASH_HEAVY
    Heavy dashes.

DOT_DASH_HEAVY
    Alternating heavy dots and heavy dashes.

DOT_DOT_DASH_HEAVY
    An alternating heavy dot-dot-dash pattern.

WAVY_HEAVY
    A heavy wavy line.

DASH_LONG
    Long dashes.

WAVY_DOUBLE
    A double wavy line.

DASH_LONG_HEAVY
    Long heavy dashes.
