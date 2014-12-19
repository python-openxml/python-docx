# encoding: utf-8

"""
Style object hierarchy.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..shared import ElementProxy


class BaseStyle(ElementProxy):
    """
    Base class for the various types of style object, paragraph, character,
    table, and numbering.
    """

    __slots__ = ()
