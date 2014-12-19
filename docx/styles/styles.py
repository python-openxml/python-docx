# encoding: utf-8

"""
Styles object, container for all objects in the styles part.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)


class Styles(object):
    """
    A collection of |Style| objects defined in a document. Supports
    ``len()``, iteration, and dictionary-style access by style id and style
    UI name.
    """
