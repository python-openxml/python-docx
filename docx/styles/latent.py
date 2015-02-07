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

    @property
    def default_priority(self):
        """
        Integer between 0 and 99 inclusive specifying the default sort order
        for latent styles in style lists and the style gallery. |None| if no
        value is assigned, which causes Word to use the default value 99.
        """
        return self._element.defUIPriority

    @default_priority.setter
    def default_priority(self, value):
        self._element.defUIPriority = value

    @property
    def default_to_hidden(self):
        """
        Boolean specifying whether the default behavior for latent styles is
        to be hidden. A hidden style does not appear in the recommended list
        or in the style gallery.
        """
        return self._element.bool_prop('defSemiHidden')

    @default_to_hidden.setter
    def default_to_hidden(self, value):
        self._element.set_bool_prop('defSemiHidden', value)

    @property
    def default_to_locked(self):
        """
        Boolean specifying whether the default behavior for latent styles is
        to be locked. A locked style does not appear in the styles panel or
        the style gallery and cannot be applied to document content. This
        behavior is only active when formatting protection is turned on for
        the document (via the Developer menu).
        """
        return self._element.bool_prop('defLockedState')

    @default_to_locked.setter
    def default_to_locked(self, value):
        self._element.set_bool_prop('defLockedState', value)

    @property
    def default_to_quick_style(self):
        """
        Boolean specifying whether the default behavior for latent styles is
        to appear in the style gallery when not hidden.
        """
        return self._element.bool_prop('defQFormat')

    @default_to_quick_style.setter
    def default_to_quick_style(self, value):
        self._element.set_bool_prop('defQFormat', value)

    @property
    def default_to_unhide_when_used(self):
        """
        Boolean specifying whether the default behavior for latent styles is
        to be unhidden when first applied to content.
        """
        return self._element.bool_prop('defUnhideWhenUsed')

    @default_to_unhide_when_used.setter
    def default_to_unhide_when_used(self, value):
        self._element.set_bool_prop('defUnhideWhenUsed', value)

    @property
    def load_count(self):
        """
        Integer specifying the number of built-in styles to initialize to the
        defaults specified in this |LatentStyles| object. |None| if there is
        no setting in the XML (very uncommon). The default Word 2011 template
        sets this value to 276, accounting for the built-in styles in Word
        2010.
        """
        return self._element.count

    @load_count.setter
    def load_count(self, value):
        self._element.count = value


class _LatentStyle(ElementProxy):
    """
    Proxy for an `w:lsdException` element, which specifies display behaviors
    for a built-in style when no definition for that style is stored yet in
    the `styles.xml` part. The values in this element override the defaults
    specified in the parent `w:latentStyles` element.
    """

    __slots__ = ()

    @property
    def name(self):
        """
        The name of the built-in style this exception applies to.
        """
        return self._element.name

    @property
    def priority(self):
        """
        The integer sort key for this latent style in the Word UI.
        """
        return self._element.uiPriority
