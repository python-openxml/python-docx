# encoding: utf-8

"""
Custom element classes related to text, such as paragraph (CT_P) and runs
(CT_R).
"""

from ..enum.text import WD_UNDERLINE
from .ns import qn
from .simpletypes import ST_BrClear, ST_BrType
from .xmlchemy import (
    BaseOxmlElement, OptionalAttribute, ZeroOrMore, ZeroOrOne
)


class CT_Br(BaseOxmlElement):
    """
    ``<w:br>`` element, indicating a line, page, or column break in a run.
    """
    type = OptionalAttribute('w:type', ST_BrType)
    clear = OptionalAttribute('w:clear', ST_BrClear)


class CT_P(BaseOxmlElement):
    """
    ``<w:p>`` element, containing the properties and text for a paragraph.
    """
    pPr = ZeroOrOne('w:pPr')
    r = ZeroOrMore('w:r')

    def _insert_pPr(self, pPr):
        self.insert(0, pPr)
        return pPr

    def set_sectPr(self, sectPr):
        """
        Unconditionally replace or add *sectPr* as a grandchild in the
        correct sequence.
        """
        pPr = self.get_or_add_pPr()
        pPr._remove_sectPr()
        pPr._insert_sectPr(sectPr)

    @property
    def style(self):
        """
        String contained in w:val attribute of <w:pPr><w:pStyle> child, or
        None if that element is not present.
        """
        pPr = self.pPr
        if pPr is None:
            return None
        return pPr.style

    @style.setter
    def style(self, style):
        """
        Set style of this <w:p> element to *style*. If *style* is None,
        remove the style element.
        """
        pPr = self.get_or_add_pPr()
        pPr.style = style


class CT_PPr(BaseOxmlElement):
    """
    ``<w:pPr>`` element, containing the properties for a paragraph.
    """
    __child_sequence__ = (
        'w:pStyle', 'w:keepNext', 'w:keepLines', 'w:pageBreakBefore',
        'w:framePr', 'w:widowControl', 'w:numPr', 'w:suppressLineNumbers',
        'w:pBdr', 'w:shd', 'w:tabs', 'w:suppressAutoHyphens', 'w:kinsoku',
        'w:wordWrap', 'w:overflowPunct', 'w:topLinePunct', 'w:autoSpaceDE',
        'w:autoSpaceDN', 'w:bidi', 'w:adjustRightInd', 'w:snapToGrid',
        'w:spacing', 'w:ind', 'w:contextualSpacing', 'w:mirrorIndents',
        'w:suppressOverlap', 'w:jc', 'w:textDirection', 'w:textAlignment',
        'w:textboxTightWrap', 'w:outlineLvl', 'w:divId', 'w:cnfStyle',
        'w:rPr', 'w:sectPr', 'w:pPrChange'
    )
    pStyle = ZeroOrOne('w:pStyle')
    numPr = ZeroOrOne('w:numPr', successors=__child_sequence__[7:])
    sectPr = ZeroOrOne('w:sectPr', successors=('w:pPrChange',))

    def _insert_pStyle(self, pStyle):
        self.insert(0, pStyle)
        return pStyle

    @property
    def style(self):
        """
        String contained in <w:pStyle> child, or None if that element is not
        present.
        """
        pStyle = self.pStyle
        if pStyle is None:
            return None
        return pStyle.val

    @style.setter
    def style(self, style):
        """
        Set val attribute of <w:pStyle> child element to *style*, adding a
        new element if necessary. If *style* is |None|, remove the <w:pStyle>
        element if present.
        """
        if style is None:
            self._remove_pStyle()
            return
        pStyle = self.get_or_add_pStyle()
        pStyle.val = style


class CT_R(BaseOxmlElement):
    """
    ``<w:r>`` element, containing the properties and text for a run.
    """
    rPr = ZeroOrOne('w:rPr')
    t = ZeroOrMore('w:t')
    br = ZeroOrMore('w:br')
    drawing = ZeroOrMore('w:drawing')

    def _insert_rPr(self, rPr):
        self.insert(0, rPr)
        return rPr

    def add_t(self, text):
        """
        Return a newly added ``<w:t>`` element containing *text*.
        """
        t = self._add_t(text=text)
        if len(text.strip()) < len(text):
            t.set(qn('xml:space'), 'preserve')
        return t

    def add_drawing(self, inline_or_anchor):
        """
        Return a newly appended ``CT_Drawing`` (``<w:drawing>``) child
        element having *inline_or_anchor* as its child.
        """
        drawing = self._add_drawing()
        drawing.append(inline_or_anchor)
        return drawing

    @property
    def style(self):
        """
        String contained in w:val attribute of <w:rStyle> grandchild, or
        |None| if that element is not present.
        """
        rPr = self.rPr
        if rPr is None:
            return None
        return rPr.style

    @style.setter
    def style(self, style):
        """
        Set the character style of this <w:r> element to *style*. If *style*
        is None, remove the style element.
        """
        rPr = self.get_or_add_rPr()
        rPr.style = style

    @property
    def underline(self):
        """
        String contained in w:val attribute of <w:u> grandchild, or |None| if
        that element is not present.
        """
        rPr = self.rPr
        if rPr is None:
            return None
        return rPr.underline

    @underline.setter
    def underline(self, value):
        rPr = self.get_or_add_rPr()
        rPr.underline = value


class CT_RPr(BaseOxmlElement):
    """
    ``<w:rPr>`` element, containing the properties for a run.
    """
    rStyle = ZeroOrOne('w:rStyle', successors=('w:rPrChange',))
    b = ZeroOrOne('w:b', successors=('w:rPrChange',))
    bCs = ZeroOrOne('w:bCs', successors=('w:rPrChange',))
    caps = ZeroOrOne('w:caps', successors=('w:rPrChange',))
    cs = ZeroOrOne('w:cs', successors=('w:rPrChange',))
    dstrike = ZeroOrOne('w:dstrike', successors=('w:rPrChange',))
    emboss = ZeroOrOne('w:emboss', successors=('w:rPrChange',))
    i = ZeroOrOne('w:i', successors=('w:rPrChange',))
    iCs = ZeroOrOne('w:iCs', successors=('w:rPrChange',))
    imprint = ZeroOrOne('w:imprint', successors=('w:rPrChange',))
    noProof = ZeroOrOne('w:noProof', successors=('w:rPrChange',))
    oMath = ZeroOrOne('w:oMath', successors=('w:rPrChange',))
    outline = ZeroOrOne('w:outline', successors=('w:rPrChange',))
    rtl = ZeroOrOne('w:rtl', successors=('w:rPrChange',))
    shadow = ZeroOrOne('w:shadow', successors=('w:rPrChange',))
    smallCaps = ZeroOrOne('w:smallCaps', successors=('w:rPrChange',))
    snapToGrid = ZeroOrOne('w:snapToGrid', successors=('w:rPrChange',))
    specVanish = ZeroOrOne('w:specVanish', successors=('w:rPrChange',))
    strike = ZeroOrOne('w:strike', successors=('w:rPrChange',))
    u = ZeroOrOne('w:u', successors=('w:rPrChange',))
    vanish = ZeroOrOne('w:vanish', successors=('w:rPrChange',))
    webHidden = ZeroOrOne('w:webHidden', successors=('w:rPrChange',))

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
    def underline(self):
        """
        Underline type specified in <w:u> child, or None if that element is
        not present.
        """
        u = self.u
        if u is None:
            return None
        return u.val

    @underline.setter
    def underline(self, value):
        self._remove_u()
        if value is not None:
            u = self._add_u()
            u.val = value


class CT_Text(BaseOxmlElement):
    """
    ``<w:t>`` element, containing a sequence of characters within a run.
    """


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
