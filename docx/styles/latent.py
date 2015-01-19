# encoding: utf-8

"""
Latent style-related objects.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..shared import ElementProxy


class LatentStyles(ElementProxy):
    """
    Provides access to the default behaviors for latent styles in this
    document and to the collection of |_LatentStyle| objects that define
    overrides of those defaults for a particular named latent style.
    """

    __slots__ = ()

    def __getitem__(self, key):
        """
        Enables dictionary-style access to a latent style by name.
        """
        lsdException = self._element.get_by_name(key)
        if lsdException is None:
            raise KeyError("no latent style with name '%s'" % key)
        return _LatentStyle(lsdException)

    def __iter__(self):
        return (_LatentStyle(ls) for ls in self._element.lsdException_lst)

    def __len__(self):
        return len(self._element.lsdException_lst)


class _LatentStyle(ElementProxy):
    """
    Proxy for an `w:lsdException` element, which specifies display behaviors
    for a built-in style when no definition for that style is stored yet in
    the `styles.xml` part. The values in this element override the defaults
    specified in the parent `w:latentStyles` element.
    """

    __slots__ = ()
