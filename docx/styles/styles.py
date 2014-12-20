# encoding: utf-8

"""
Styles object, container for all objects in the styles part.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from .style import StyleFactory


class Styles(object):
    """
    A collection of |Style| objects defined in a document. Supports
    ``len()``, iteration, and dictionary-style access by style id and style
    UI name.
    """
    def __init__(self, element):
        self._element = element

    def __getitem__(self, key):
        """
        Enables dictionary-style access by style id or UI name.
        """
        for get in (self._element.get_by_id, self._element.get_by_name):
            style_elm = get(key)
            if style_elm is not None:
                return StyleFactory(style_elm)
        raise KeyError("no style with id or name '%s'" % key)

    def __iter__(self):
        return (StyleFactory(style) for style in self._element.style_lst)

    def __len__(self):
        return len(self._element.style_lst)
