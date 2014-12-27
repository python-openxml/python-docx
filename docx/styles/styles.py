# encoding: utf-8

"""
Styles object, container for all objects in the styles part.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..shared import ElementProxy
from .style import BaseStyle, StyleFactory


class Styles(ElementProxy):
    """
    A collection of |Style| objects defined in a document. Supports
    ``len()``, iteration, and dictionary-style access by style id and style
    UI name.
    """

    __slots__ = ()

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

    def default(self, style_type):
        """
        Return the default style for *style_type* or |None| if no default is
        defined for that type (not common).
        """
        style = self._element.default_for(style_type)
        if style is None:
            return None
        return StyleFactory(style)

    def get_by_id(self, style_id, style_type):
        """
        Return the style of *style_type* matching *style_id*. Returns the
        default for *style_type* if *style_id* is not found or is |None|, or
        if the style having *style_id* is not of *style_type*.
        """
        if style_id is None:
            return self.default(style_type)
        return self._get_by_id(style_id, style_type)

    def get_style_id(self, style_or_name, style_type):
        """
        Return the id of the style corresponding to *style_or_name*, or
        |None| if *style_or_name* is |None|. If *style_or_name* is not
        a style object, the style is looked up using *style_or_name* as
        a style name, raising |ValueError| if no style with that name is
        defined. Raises |ValueError| if the target style is not of
        *style_type*.
        """
        if style_or_name is None:
            return None
        elif isinstance(style_or_name, BaseStyle):
            return self._get_style_id_from_style(style_or_name, style_type)
        else:
            return self._get_style_id_from_name(style_or_name, style_type)

    def _get_by_id(self, style_id, style_type):
        """
        Return the style of *style_type* matching *style_id*. Returns the
        default for *style_type* if *style_id* is not found or if the style
        having *style_id* is not of *style_type*.
        """
        style = self._element.get_by_id(style_id)
        if style is None or style.type != style_type:
            return self.default(style_type)
        return StyleFactory(style)

    def _get_style_id_from_name(self, style_name, style_type):
        """
        Return the id of the style of *style_type* corresponding to
        *style_name*. Returns |None| if that style is the default style for
        *style_type*. Raises |ValueError| if the named style is not found in
        the document or does not match *style_type*.
        """
        return self._get_style_id_from_style(self[style_name], style_type)

    def _get_style_id_from_style(self, style, style_type):
        """
        Return the id of *style*, or |None| if it is the default style of
        *style_type*. Raises |ValueError| if style is not of *style_type*.
        """
        raise NotImplementedError

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
