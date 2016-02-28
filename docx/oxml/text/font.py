# encoding: utf-8

"""
Custom element classes related to run properties (font).
"""

from .. import parse_xml
from ...enum.dml import MSO_THEME_COLOR
from ...enum.text import WD_COLOR, WD_UNDERLINE
from ..ns import nsdecls, qn
from ..simpletypes import (
    ST_HexColor, ST_HpsMeasure, ST_String, ST_VerticalAlignRun
)
from ..xmlchemy import (
    BaseOxmlElement, OptionalAttribute, RequiredAttribute, ZeroOrOne
)


class CT_Color(BaseOxmlElement):
    """
    `w:color` element, specifying the color of a font and perhaps other
    objects.
    """
    val = RequiredAttribute('w:val', ST_HexColor)
    themeColor = OptionalAttribute('w:themeColor', MSO_THEME_COLOR)


class CT_Fonts(BaseOxmlElement):
    """
    ``<w:rFonts>`` element, specifying typeface name for the various language
    types.
    """
    ascii = OptionalAttribute('w:ascii', ST_String)
    hAnsi = OptionalAttribute('w:hAnsi', ST_String)


class CT_Highlight(BaseOxmlElement):
    """
    `w:highlight` element, specifying font highlighting/background color.
    """
    val = RequiredAttribute('w:val', WD_COLOR)


class CT_HpsMeasure(BaseOxmlElement):
    """
    Used for ``<w:sz>`` element and others, specifying font size in
    half-points.
    """
    val = RequiredAttribute('w:val', ST_HpsMeasure)


class CT_RPr(BaseOxmlElement):
    """
    ``<w:rPr>`` element, containing the properties for a run.
    """
    _tag_seq = (
        'w:rStyle', 'w:rFonts', 'w:b', 'w:bCs', 'w:i', 'w:iCs', 'w:caps',
        'w:smallCaps', 'w:strike', 'w:dstrike', 'w:outline', 'w:shadow',
        'w:emboss', 'w:imprint', 'w:noProof', 'w:snapToGrid', 'w:vanish',
        'w:webHidden', 'w:color', 'w:spacing', 'w:w', 'w:kern', 'w:position',
        'w:sz', 'w:szCs', 'w:highlight', 'w:u', 'w:effect', 'w:bdr', 'w:shd',
        'w:fitText', 'w:vertAlign', 'w:rtl', 'w:cs', 'w:em', 'w:lang',
        'w:eastAsianLayout', 'w:specVanish', 'w:oMath'
    )
    rStyle = ZeroOrOne('w:rStyle', successors=_tag_seq[1:])
    rFonts = ZeroOrOne('w:rFonts', successors=_tag_seq[2:])
    b = ZeroOrOne('w:b', successors=_tag_seq[3:])
    bCs = ZeroOrOne('w:bCs', successors=_tag_seq[4:])
    i = ZeroOrOne('w:i', successors=_tag_seq[5:])
    iCs = ZeroOrOne('w:iCs', successors=_tag_seq[6:])
    caps = ZeroOrOne('w:caps', successors=_tag_seq[7:])
    smallCaps = ZeroOrOne('w:smallCaps', successors=_tag_seq[8:])
    strike = ZeroOrOne('w:strike', successors=_tag_seq[9:])
    dstrike = ZeroOrOne('w:dstrike', successors=_tag_seq[10:])
    outline = ZeroOrOne('w:outline', successors=_tag_seq[11:])
    shadow = ZeroOrOne('w:shadow', successors=_tag_seq[12:])
    emboss = ZeroOrOne('w:emboss', successors=_tag_seq[13:])
    imprint = ZeroOrOne('w:imprint', successors=_tag_seq[14:])
    noProof = ZeroOrOne('w:noProof', successors=_tag_seq[15:])
    snapToGrid = ZeroOrOne('w:snapToGrid', successors=_tag_seq[16:])
    vanish = ZeroOrOne('w:vanish', successors=_tag_seq[17:])
    webHidden = ZeroOrOne('w:webHidden', successors=_tag_seq[18:])
    color = ZeroOrOne('w:color', successors=_tag_seq[19:])
    sz = ZeroOrOne('w:sz', successors=_tag_seq[24:])
    highlight = ZeroOrOne('w:highlight', successors=_tag_seq[26:])
    u = ZeroOrOne('w:u', successors=_tag_seq[27:])
    vertAlign = ZeroOrOne('w:vertAlign', successors=_tag_seq[32:])
    rtl = ZeroOrOne('w:rtl', successors=_tag_seq[33:])
    cs = ZeroOrOne('w:cs', successors=_tag_seq[34:])
    specVanish = ZeroOrOne('w:specVanish', successors=_tag_seq[38:])
    oMath = ZeroOrOne('w:oMath', successors=_tag_seq[39:])
    del _tag_seq

    def _new_color(self):
        """
        Override metaclass method to set `w:color/@val` to RGB black on
        create.
        """
        return parse_xml('<w:color %s w:val="000000"/>' % nsdecls('w'))

    @property
    def highlight_val(self):
        """
        Value of `w:highlight/@val` attribute, specifying a font's highlight
        color, or `None` if the text is not highlighted.
        """
        highlight = self.highlight
        if highlight is None:
            return None
        return highlight.val

    @highlight_val.setter
    def highlight_val(self, value):
        if value is None:
            self._remove_highlight()
            return
        highlight = self.get_or_add_highlight()
        highlight.val = value

    @property
    def rFonts_ascii(self):
        """
        The value of `w:rFonts/@w:ascii` or |None| if not present. Represents
        the assigned typeface name. The rFonts element also specifies other
        special-case typeface names; this method handles the case where just
        the common name is required.
        """
        rFonts = self.rFonts
        if rFonts is None:
            return None
        return rFonts.ascii

    @rFonts_ascii.setter
    def rFonts_ascii(self, value):
        if value is None:
            self._remove_rFonts()
            return
        rFonts = self.get_or_add_rFonts()
        rFonts.ascii = value

    @property
    def rFonts_hAnsi(self):
        """
        The value of `w:rFonts/@w:hAnsi` or |None| if not present.
        """
        rFonts = self.rFonts
        if rFonts is None:
            return None
        return rFonts.hAnsi

    @rFonts_hAnsi.setter
    def rFonts_hAnsi(self, value):
        if value is None and self.rFonts is None:
            return
        rFonts = self.get_or_add_rFonts()
        rFonts.hAnsi = value

    @property
    def style(self):
        """
        String contained in <w:rStyle> child, or None if that element is not
        present.
        """
        rStyle = self.rStyle
        if rStyle is None:
            return None
        return rStyle.val

    @style.setter
    def style(self, style):
        """
        Set val attribute of <w:rStyle> child element to *style*, adding a
        new element if necessary. If *style* is |None|, remove the <w:rStyle>
        element if present.
        """
        if style is None:
            self._remove_rStyle()
        elif self.rStyle is None:
            self._add_rStyle(val=style)
        else:
            self.rStyle.val = style

    @property
    def subscript(self):
        """
        |True| if `w:vertAlign/@w:val` is 'subscript'. |False| if
        `w:vertAlign/@w:val` contains any other value. |None| if
        `w:vertAlign` is not present.
        """
        vertAlign = self.vertAlign
        if vertAlign is None:
            return None
        if vertAlign.val == ST_VerticalAlignRun.SUBSCRIPT:
            return True
        return False

    @subscript.setter
    def subscript(self, value):
        if value is None:
            self._remove_vertAlign()
        elif bool(value) is True:
            self.get_or_add_vertAlign().val = ST_VerticalAlignRun.SUBSCRIPT
        elif self.vertAlign is None:
            return
        elif self.vertAlign.val == ST_VerticalAlignRun.SUBSCRIPT:
            self._remove_vertAlign()

    @property
    def superscript(self):
        """
        |True| if `w:vertAlign/@w:val` is 'superscript'. |False| if
        `w:vertAlign/@w:val` contains any other value. |None| if
        `w:vertAlign` is not present.
        """
        vertAlign = self.vertAlign
        if vertAlign is None:
            return None
        if vertAlign.val == ST_VerticalAlignRun.SUPERSCRIPT:
            return True
        return False

    @superscript.setter
    def superscript(self, value):
        if value is None:
            self._remove_vertAlign()
        elif bool(value) is True:
            self.get_or_add_vertAlign().val = ST_VerticalAlignRun.SUPERSCRIPT
        elif self.vertAlign is None:
            return
        elif self.vertAlign.val == ST_VerticalAlignRun.SUPERSCRIPT:
            self._remove_vertAlign()

    @property
    def sz_val(self):
        """
        The value of `w:sz/@w:val` or |None| if not present.
        """
        sz = self.sz
        if sz is None:
            return None
        return sz.val

    @sz_val.setter
    def sz_val(self, value):
        if value is None:
            self._remove_sz()
            return
        sz = self.get_or_add_sz()
        sz.val = value

    @property
    def u_val(self):
        """
        Value of `w:u/@val`, or None if not present.
        """
        u = self.u
        if u is None:
            return None
        return u.val

    @u_val.setter
    def u_val(self, value):
        self._remove_u()
        if value is not None:
            self._add_u().val = value

    def _get_bool_val(self, name):
        """
        Return the value of the boolean child element having *name*, e.g.
        'b', 'i', and 'smallCaps'.
        """
        element = getattr(self, name)
        if element is None:
            return None
        return element.val

    def _set_bool_val(self, name, value):
        if value is None:
            getattr(self, '_remove_%s' % name)()
            return
        element = getattr(self, 'get_or_add_%s' % name)()
        element.val = value


class CT_Underline(BaseOxmlElement):
    """
    ``<w:u>`` element, specifying the underlining style for a run.
    """
    @property
    def val(self):
        """
        The underline type corresponding to the ``w:val`` attribute value.
        """
        val = self.get(qn('w:val'))
        underline = WD_UNDERLINE.from_xml(val)
        if underline == WD_UNDERLINE.SINGLE:
            return True
        if underline == WD_UNDERLINE.NONE:
            return False
        return underline

    @val.setter
    def val(self, value):
        # works fine without these two mappings, but only because True == 1
        # and False == 0, which happen to match the mapping for WD_UNDERLINE
        # .SINGLE and .NONE respectively.
        if value is True:
            value = WD_UNDERLINE.SINGLE
        elif value is False:
            value = WD_UNDERLINE.NONE

        val = WD_UNDERLINE.to_xml(value)
        self.set(qn('w:val'), val)


class CT_VerticalAlignRun(BaseOxmlElement):
    """
    ``<w:vertAlign>`` element, specifying subscript or superscript.
    """
    val = RequiredAttribute('w:val', ST_VerticalAlignRun)
