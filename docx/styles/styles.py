# encoding: utf-8

"""
Styles object, container for all objects in the styles part.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..shared import ElementProxy
from .style import StyleFactory


class Styles(ElementProxy):
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
        key = self._translate_special_case_names(key)
        for get in (self._element.get_by_id, self._element.get_by_name):
            style_elm = get(key)
            if style_elm is not None:
                return StyleFactory(style_elm)
        raise KeyError("no style with id or name '%s'" % key)

    def __iter__(self):
        return (StyleFactory(style) for style in self._element.style_lst)

    def __len__(self):
        return len(self._element.style_lst)

    @staticmethod
    def _translate_special_case_names(name):
        """
        Translate special-case style names from their English UI
        counterparts. Some style names are stored differently than they
        appear in the UI, with a leading lowercase letter, perhaps for legacy
        reasons.
        """
        return {
            'Caption':   'caption',
            'Heading 1': 'heading 1',
            'Heading 2': 'heading 2',
            'Heading 3': 'heading 3',
            'Heading 4': 'heading 4',
            'Heading 5': 'heading 5',
            'Heading 6': 'heading 6',
            'Heading 7': 'heading 7',
            'Heading 8': 'heading 8',
            'Heading 9': 'heading 9',
        }.get(name, name)
