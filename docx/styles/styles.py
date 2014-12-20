# encoding: utf-8

"""
Styles object, container for all objects in the styles part.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..shared import ElementProxy


class Styles(ElementProxy):
    """
    A collection of |Style| objects defined in a document. Supports
    ``len()``, iteration, and dictionary-style access by style id and style
    UI name.
    """

    __slots__ = ()
