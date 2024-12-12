"""Custom element classes related to the styles part."""

from __future__ import annotations

from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.simpletypes import ST_DecimalNumber, ST_OnOff, ST_String
from docx.oxml.xmlchemy import (
    BaseOxmlElement,
    OptionalAttribute,
    RequiredAttribute,
    ZeroOrMore,
    ZeroOrOne,
)


def styleId_from_name(name):
    """Return the style id corresponding to `name`, taking into account special-case
    names such as 'Heading 1'."""
    return {
        "caption": "Caption",
        "heading 1": "Heading1",
        "heading 2": "Heading2",
        "heading 3": "Heading3",
        "heading 4": "Heading4",
        "heading 5": "Heading5",
        "heading 6": "Heading6",
        "heading 7": "Heading7",
        "heading 8": "Heading8",
        "heading 9": "Heading9",
    }.get(name, name.replace(" ", ""))


class CT_LatentStyles(BaseOxmlElement):
    """`w:latentStyles` element, defining behavior defaults for latent styles and
    containing `w:lsdException` child elements that each override those defaults for a
    named latent style."""

    lsdException = ZeroOrMore("w:lsdException", successors=())

    count = OptionalAttribute("w:count", ST_DecimalNumber)
    defLockedState = OptionalAttribute("w:defLockedState", ST_OnOff)
    defQFormat = OptionalAttribute("w:defQFormat", ST_OnOff)
    defSemiHidden = OptionalAttribute("w:defSemiHidden", ST_OnOff)
    defUIPriority = OptionalAttribute("w:defUIPriority", ST_DecimalNumber)
    defUnhideWhenUsed = OptionalAttribute("w:defUnhideWhenUsed", ST_OnOff)

    def bool_prop(self, attr_name):
        """Return the boolean value of the attribute having `attr_name`, or |False| if
        not present."""
        value = getattr(self, attr_name)
        if value is None:
            return False
        return value

    def get_by_name(self, name):
        """Return the `w:lsdException` child having `name`, or |None| if not found."""
        found = self.xpath('w:lsdException[@w:name="%s"]' % name)
        if not found:
            return None
        return found[0]

    def set_bool_prop(self, attr_name, value):
        """Set the on/off attribute having `attr_name` to `value`."""
        setattr(self, attr_name, bool(value))


class CT_LsdException(BaseOxmlElement):
    """``<w:lsdException>`` element, defining override visibility behaviors for a named
    latent style."""

    locked = OptionalAttribute("w:locked", ST_OnOff)
    name = RequiredAttribute("w:name", ST_String)
    qFormat = OptionalAttribute("w:qFormat", ST_OnOff)
    semiHidden = OptionalAttribute("w:semiHidden", ST_OnOff)
    uiPriority = OptionalAttribute("w:uiPriority", ST_DecimalNumber)
    unhideWhenUsed = OptionalAttribute("w:unhideWhenUsed", ST_OnOff)

    def delete(self):
        """Remove this `w:lsdException` element from the XML document."""
        self.getparent().remove(self)

    def on_off_prop(self, attr_name):
        """Return the boolean value of the attribute having `attr_name`, or |None| if
        not present."""
        return getattr(self, attr_name)

    def set_on_off_prop(self, attr_name, value):
        """Set the on/off attribute having `attr_name` to `value`."""
        setattr(self, attr_name, value)


class CT_Style(BaseOxmlElement):
    """A ``<w:style>`` element, representing a style definition."""

    _tag_seq = (
        "w:name",
        "w:aliases",
        "w:basedOn",
        "w:next",
        "w:link",
        "w:autoRedefine",
        "w:hidden",
        "w:uiPriority",
        "w:semiHidden",
        "w:unhideWhenUsed",
        "w:qFormat",
        "w:locked",
        "w:personal",
        "w:personalCompose",
        "w:personalReply",
        "w:rsid",
        "w:pPr",
        "w:rPr",
        "w:tblPr",
        "w:trPr",
        "w:tcPr",
        "w:tblStylePr",
    )
    name = ZeroOrOne("w:name", successors=_tag_seq[1:])
    basedOn = ZeroOrOne("w:basedOn", successors=_tag_seq[3:])
    next = ZeroOrOne("w:next", successors=_tag_seq[4:])
    uiPriority = ZeroOrOne("w:uiPriority", successors=_tag_seq[8:])
    semiHidden = ZeroOrOne("w:semiHidden", successors=_tag_seq[9:])
    unhideWhenUsed = ZeroOrOne("w:unhideWhenUsed", successors=_tag_seq[10:])
    qFormat = ZeroOrOne("w:qFormat", successors=_tag_seq[11:])
    locked = ZeroOrOne("w:locked", successors=_tag_seq[12:])
    pPr = ZeroOrOne("w:pPr", successors=_tag_seq[17:])
    rPr = ZeroOrOne("w:rPr", successors=_tag_seq[18:])
    del _tag_seq

    type: WD_STYLE_TYPE | None = OptionalAttribute(  # pyright: ignore[reportAssignmentType]
        "w:type", WD_STYLE_TYPE
    )
    styleId: str | None = OptionalAttribute(  # pyright: ignore[reportAssignmentType]
        "w:styleId", ST_String
    )
    default = OptionalAttribute("w:default", ST_OnOff)
    customStyle = OptionalAttribute("w:customStyle", ST_OnOff)

    @property
    def basedOn_val(self):
        """Value of `w:basedOn/@w:val` or |None| if not present."""
        basedOn = self.basedOn
        if basedOn is None:
            return None
        return basedOn.val

    @basedOn_val.setter
    def basedOn_val(self, value):
        if value is None:
            self._remove_basedOn()
        else:
            self.get_or_add_basedOn().val = value

    @property
    def base_style(self):
        """Sibling CT_Style element this style is based on or |None| if no base style or
        base style not found."""
        basedOn = self.basedOn
        if basedOn is None:
            return None
        styles = self.getparent()
        base_style = styles.get_by_id(basedOn.val)
        if base_style is None:
            return None
        return base_style

    def delete(self):
        """Remove this `w:style` element from its parent `w:styles` element."""
        self.getparent().remove(self)

    @property
    def locked_val(self):
        """Value of `w:locked/@w:val` or |False| if not present."""
        locked = self.locked
        if locked is None:
            return False
        return locked.val

    @locked_val.setter
    def locked_val(self, value):
        self._remove_locked()
        if bool(value) is True:
            locked = self._add_locked()
            locked.val = value

    @property
    def name_val(self):
        """Value of ``<w:name>`` child or |None| if not present."""
        name = self.name
        if name is None:
            return None
        return name.val

    @name_val.setter
    def name_val(self, value):
        self._remove_name()
        if value is not None:
            name = self._add_name()
            name.val = value

    @property
    def next_style(self):
        """Sibling CT_Style element identified by the value of `w:name/@w:val` or |None|
        if no value is present or no style with that style id is found."""
        next = self.next
        if next is None:
            return None
        styles = self.getparent()
        return styles.get_by_id(next.val)  # None if not found

    @property
    def qFormat_val(self):
        """Value of `w:qFormat/@w:val` or |False| if not present."""
        qFormat = self.qFormat
        if qFormat is None:
            return False
        return qFormat.val

    @qFormat_val.setter
    def qFormat_val(self, value):
        self._remove_qFormat()
        if bool(value):
            self._add_qFormat()

    @property
    def semiHidden_val(self):
        """Value of ``<w:semiHidden>`` child or |False| if not present."""
        semiHidden = self.semiHidden
        if semiHidden is None:
            return False
        return semiHidden.val

    @semiHidden_val.setter
    def semiHidden_val(self, value):
        self._remove_semiHidden()
        if bool(value) is True:
            semiHidden = self._add_semiHidden()
            semiHidden.val = value

    @property
    def uiPriority_val(self):
        """Value of ``<w:uiPriority>`` child or |None| if not present."""
        uiPriority = self.uiPriority
        if uiPriority is None:
            return None
        return uiPriority.val

    @uiPriority_val.setter
    def uiPriority_val(self, value):
        self._remove_uiPriority()
        if value is not None:
            uiPriority = self._add_uiPriority()
            uiPriority.val = value

    @property
    def unhideWhenUsed_val(self):
        """Value of `w:unhideWhenUsed/@w:val` or |False| if not present."""
        unhideWhenUsed = self.unhideWhenUsed
        if unhideWhenUsed is None:
            return False
        return unhideWhenUsed.val

    @unhideWhenUsed_val.setter
    def unhideWhenUsed_val(self, value):
        self._remove_unhideWhenUsed()
        if bool(value) is True:
            unhideWhenUsed = self._add_unhideWhenUsed()
            unhideWhenUsed.val = value


class CT_Styles(BaseOxmlElement):
    """``<w:styles>`` element, the root element of a styles part, i.e. styles.xml."""

    _tag_seq = ("w:docDefaults", "w:latentStyles", "w:style")
    latentStyles = ZeroOrOne("w:latentStyles", successors=_tag_seq[2:])
    style = ZeroOrMore("w:style", successors=())
    del _tag_seq

    def add_style_of_type(self, name, style_type, builtin):
        """Return a newly added `w:style` element having `name` and `style_type`.

        `w:style/@customStyle` is set based on the value of `builtin`.
        """
        style = self.add_style()
        style.type = style_type
        style.customStyle = None if builtin else True
        style.styleId = styleId_from_name(name)
        style.name_val = name
        return style

    def default_for(self, style_type):
        """Return `w:style[@w:type="*{style_type}*][-1]` or |None| if not found."""
        default_styles_for_type = [
            s for s in self._iter_styles() if s.type == style_type and s.default
        ]
        if not default_styles_for_type:
            return None
        # spec calls for last default in document order
        return default_styles_for_type[-1]

    def get_by_id(self, styleId: str) -> CT_Style | None:
        """`w:style` child where @styleId = `styleId`.

        |None| if not found.
        """
        xpath = f'w:style[@w:styleId="{styleId}"]'
        return next(iter(self.xpath(xpath)), None)

    def get_by_name(self, name: str) -> CT_Style | None:
        """`w:style` child with `w:name` grandchild having value `name`.

        |None| if not found.
        """
        xpath = 'w:style[w:name/@w:val="%s"]' % name
        return next(iter(self.xpath(xpath)), None)

    def _iter_styles(self):
        """Generate each of the `w:style` child elements in document order."""
        return (style for style in self.xpath("w:style"))
