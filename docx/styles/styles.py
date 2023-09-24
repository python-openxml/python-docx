# encoding: utf-8

"""Styles object, container for all objects in the styles part"""

from __future__ import absolute_import, division, print_function, unicode_literals

from warnings import warn

from docx.shared import ElementProxy
from docx.styles import BabelFish
from docx.styles.latent import LatentStyles
from docx.styles.style import BaseStyle, StyleFactory


class Styles(ElementProxy):
    """Provides access to the styles defined in a document.

    Accessed using the :attr:`.Document.styles` property. Supports ``len()``, iteration,
    and dictionary-style access by style name.
    """

    __slots__ = ()

    def __contains__(self, name):
        """
        Enables `in` operator on style name.
        """
        internal_name = BabelFish.ui2internal(name)
        for style in self._element.style_lst:
            if style.name_val == internal_name:
                return True
        return False

    def __getitem__(self, key):
        """
        Enables dictionary-style access by UI name. Lookup by style id is
        deprecated, triggers a warning, and will be removed in a near-future
        release.
        """
        style_elm = self._element.get_by_name(BabelFish.ui2internal(key))
        if style_elm is not None:
            return StyleFactory(style_elm)

        style_elm = self._element.get_by_id(key)
        if style_elm is not None:
            msg = (
                "style lookup by style_id is deprecated. Use style name as "
                "key instead."
            )
            warn(msg, UserWarning, stacklevel=2)
            return StyleFactory(style_elm)

        raise KeyError("no style with name '%s'" % key)

    def __iter__(self):
        return (StyleFactory(style) for style in self._element.style_lst)

    def __len__(self):
        return len(self._element.style_lst)

    def add_style(self, name, style_type, builtin=False):
        """
        Return a newly added style object of *style_type* and identified
        by *name*. A builtin style can be defined by passing True for the
        optional *builtin* argument.
        """
        style_name = BabelFish.ui2internal(name)
        if style_name in self:
            raise ValueError("document already contains style '%s'" % name)
        style = self._element.add_style_of_type(style_name, style_type, builtin)
        return StyleFactory(style)

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
        """Return the style of *style_type* matching *style_id*.

        Returns the default for *style_type* if *style_id* is not found or is |None|, or
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

    @property
    def latent_styles(self):
        """
        A |LatentStyles| object providing access to the default behaviors for
        latent styles and the collection of |_LatentStyle| objects that
        define overrides of those defaults for a particular named latent
        style.
        """
        return LatentStyles(self._element.get_or_add_latentStyles())

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
        if style.type != style_type:
            raise ValueError(
                "assigned style is type %s, need type %s" % (style.type, style_type)
            )
        if style == self.default(style_type):
            return None
        return style.style_id
