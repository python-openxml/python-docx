"""Latent style-related objects."""

from docx.shared import ElementProxy
from docx.styles import BabelFish


class LatentStyles(ElementProxy):
    """Provides access to the default behaviors for latent styles in this document and
    to the collection of |_LatentStyle| objects that define overrides of those defaults
    for a particular named latent style."""

    def __getitem__(self, key):
        """Enables dictionary-style access to a latent style by name."""
        style_name = BabelFish.ui2internal(key)
        lsdException = self._element.get_by_name(style_name)
        if lsdException is None:
            raise KeyError("no latent style with name '%s'" % key)
        return _LatentStyle(lsdException)

    def __iter__(self):
        return (_LatentStyle(ls) for ls in self._element.lsdException_lst)

    def __len__(self):
        return len(self._element.lsdException_lst)

    def add_latent_style(self, name):
        """Return a newly added |_LatentStyle| object to override the inherited defaults
        defined in this latent styles object for the built-in style having `name`."""
        lsdException = self._element.add_lsdException()
        lsdException.name = BabelFish.ui2internal(name)
        return _LatentStyle(lsdException)

    @property
    def default_priority(self):
        """Integer between 0 and 99 inclusive specifying the default sort order for
        latent styles in style lists and the style gallery.

        |None| if no value is assigned, which causes Word to use the default value 99.
        """
        return self._element.defUIPriority

    @default_priority.setter
    def default_priority(self, value):
        self._element.defUIPriority = value

    @property
    def default_to_hidden(self):
        """Boolean specifying whether the default behavior for latent styles is to be
        hidden.

        A hidden style does not appear in the recommended list or in the style gallery.
        """
        return self._element.bool_prop("defSemiHidden")

    @default_to_hidden.setter
    def default_to_hidden(self, value):
        self._element.set_bool_prop("defSemiHidden", value)

    @property
    def default_to_locked(self):
        """Boolean specifying whether the default behavior for latent styles is to be
        locked.

        A locked style does not appear in the styles panel or the style gallery and
        cannot be applied to document content. This behavior is only active when
        formatting protection is turned on for the document (via the Developer menu).
        """
        return self._element.bool_prop("defLockedState")

    @default_to_locked.setter
    def default_to_locked(self, value):
        self._element.set_bool_prop("defLockedState", value)

    @property
    def default_to_quick_style(self):
        """Boolean specifying whether the default behavior for latent styles is to
        appear in the style gallery when not hidden."""
        return self._element.bool_prop("defQFormat")

    @default_to_quick_style.setter
    def default_to_quick_style(self, value):
        self._element.set_bool_prop("defQFormat", value)

    @property
    def default_to_unhide_when_used(self):
        """Boolean specifying whether the default behavior for latent styles is to be
        unhidden when first applied to content."""
        return self._element.bool_prop("defUnhideWhenUsed")

    @default_to_unhide_when_used.setter
    def default_to_unhide_when_used(self, value):
        self._element.set_bool_prop("defUnhideWhenUsed", value)

    @property
    def load_count(self):
        """Integer specifying the number of built-in styles to initialize to the
        defaults specified in this |LatentStyles| object.

        |None| if there is no setting in the XML (very uncommon). The default Word 2011
        template sets this value to 276, accounting for the built-in styles in Word
        2010.
        """
        return self._element.count

    @load_count.setter
    def load_count(self, value):
        self._element.count = value


class _LatentStyle(ElementProxy):
    """Proxy for an `w:lsdException` element, which specifies display behaviors for a
    built-in style when no definition for that style is stored yet in the `styles.xml`
    part.

    The values in this element override the defaults specified in the parent
    `w:latentStyles` element.
    """

    def delete(self):
        """Remove this latent style definition such that the defaults defined in the
        containing |LatentStyles| object provide the effective value for each of its
        attributes.

        Attempting to access any attributes on this object after calling this method
        will raise |AttributeError|.
        """
        self._element.delete()
        self._element = None

    @property
    def hidden(self):
        """Tri-state value specifying whether this latent style should appear in the
        recommended list.

        |None| indicates the effective value is inherited from the parent
        ``<w:latentStyles>`` element.
        """
        return self._element.on_off_prop("semiHidden")

    @hidden.setter
    def hidden(self, value):
        self._element.set_on_off_prop("semiHidden", value)

    @property
    def locked(self):
        """Tri-state value specifying whether this latent styles is locked.

        A locked style does not appear in the styles panel or the style gallery and
        cannot be applied to document content. This behavior is only active when
        formatting protection is turned on for the document (via the Developer menu).
        """
        return self._element.on_off_prop("locked")

    @locked.setter
    def locked(self, value):
        self._element.set_on_off_prop("locked", value)

    @property
    def name(self):
        """The name of the built-in style this exception applies to."""
        return BabelFish.internal2ui(self._element.name)

    @property
    def priority(self):
        """The integer sort key for this latent style in the Word UI."""
        return self._element.uiPriority

    @priority.setter
    def priority(self, value):
        self._element.uiPriority = value

    @property
    def quick_style(self):
        """Tri-state value specifying whether this latent style should appear in the
        Word styles gallery when not hidden.

        |None| indicates the effective value should be inherited from the default values
        in its parent |LatentStyles| object.
        """
        return self._element.on_off_prop("qFormat")

    @quick_style.setter
    def quick_style(self, value):
        self._element.set_on_off_prop("qFormat", value)

    @property
    def unhide_when_used(self):
        """Tri-state value specifying whether this style should have its :attr:`hidden`
        attribute set |False| the next time the style is applied to content.

        |None| indicates the effective value should be inherited from the default
        specified by its parent |LatentStyles| object.
        """
        return self._element.on_off_prop("unhideWhenUsed")

    @unhide_when_used.setter
    def unhide_when_used(self, value):
        self._element.set_on_off_prop("unhideWhenUsed", value)
