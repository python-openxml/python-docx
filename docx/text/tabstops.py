# encoding: utf-8

"""
Tabstop-related proxy types.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..shared import ElementProxy


class TabStops(ElementProxy):
    """
    A sequence providing access to the tab stops of a paragraph or paragraph
    style. Supports iteration, indexed access, del, and len(). It is accesed
    using the `tab_stops` property of ParagraphFormat; it is not intended to
    be constructed directly.
    """
