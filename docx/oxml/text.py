# encoding: utf-8

"""
Custom element classes related to text, such as paragraph (CT_P) and runs
(CT_R).
"""

from docx.enum.text import WD_UNDERLINE
from docx.oxml.parts.numbering import CT_NumPr
from docx.oxml.shared import (
    CT_String, nsdecls, OxmlBaseElement, OxmlElement, oxml_fromstring, qn
)


class CT_Br(OxmlBaseElement):
    """
    ``<w:br>`` element, indicating a line, page, or column break in a run.
    """
    @classmethod
    def new(cls):
        """
        Return a new ``<w:br>`` element.
        """
        return OxmlElement('w:br')

    @property
    def clear(self):
        self.get(qn('w:clear'))

    @clear.setter
    def clear(self, clear_str):
        self.set(qn('w:clear'), clear_str)

    @property
    def type(self):
        return self.get(qn('w:type'))

    @type.setter
    def type(self, type_str):
        self.set(qn('w:type'), type_str)


class CT_P(OxmlBaseElement):
    """
    ``<w:p>`` element, containing the properties and text for a paragraph.
    """
    def add_r(self):
        """
        Return a newly added CT_R (<w:r>) element.
        """
        r = CT_R.new()
        self.append(r)
        return r

    def get_or_add_pPr(self):
        """
        Return the pPr child element, newly added if not present.
        """
        pPr = self.pPr
        if pPr is None:
            pPr = self._add_pPr()
        return pPr

    @staticmethod
    def new():
        """
        Return a new ``<w:p>`` element.
        """
        xml = '<w:p %s/>' % nsdecls('w')
        p = oxml_fromstring(xml)
        return p

    @property
    def pPr(self):
        """
        ``<w:pPr>`` child element or None if not present.
        """
        return self.find(qn('w:pPr'))

    @property
    def r_lst(self):
        """
        Sequence containing a reference to each run element in this paragraph.
        """
        return self.findall(qn('w:r'))

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

    def _add_pPr(self):
        """
        Return a newly added pPr child element. Assumes one is not present.
        """
        pPr = CT_PPr.new()
        self.insert(0, pPr)
        return pPr


class CT_PPr(OxmlBaseElement):
    """
    ``<w:pPr>`` element, containing the properties for a paragraph.
    """
    def get_or_add_numPr(self):
        """
        Return the numPr child element, newly added if not present.
        """
        numPr = self.numPr
        if numPr is None:
            numPr = self._add_numPr()
        return numPr

    def get_or_add_pStyle(self):
        """
        Return the pStyle child element, newly added if not present.
        """
        pStyle = self.pStyle
        if pStyle is None:
            pStyle = self._add_pStyle()
        return pStyle

    @staticmethod
    def new():
        """
        Return a new ``<w:pPr>`` element.
        """
        xml = '<w:pPr %s/>' % nsdecls('w')
        pPr = oxml_fromstring(xml)
        return pPr

    @property
    def numPr(self):
        """
        ``<w:numPr>`` child element or None if not present.
        """
        return self.find(qn('w:numPr'))

    @property
    def pStyle(self):
        """
        ``<w:pStyle>`` child element or None if not present.
        """
        return self.find(qn('w:pStyle'))

    def remove_pStyle(self):
        pStyle = self.pStyle
        if pStyle is not None:
            self.remove(pStyle)

    @property
    def style(self):
        """
        String contained in <w:pStyle> child, or None if that element is not
        present.
        """
        pStyle = self.pStyle
        if pStyle is None:
            return None
        return pStyle.get(qn('w:val'))

    @style.setter
    def style(self, style):
        """
        Set val attribute of <w:pStyle> child element to *style*, adding a
        new element if necessary. If *style* is |None|, remove the <w:pStyle>
        element if present.
        """
        if style is None:
            self.remove_pStyle()
        elif self.pStyle is None:
            self._add_pStyle(style)
        else:
            self.pStyle.val = style

    def _add_numPr(self):
        numPr = CT_NumPr.new()
        return self._insert_numPr(numPr)

    def _add_pStyle(self, style):
        pStyle = CT_String.new_pStyle(style)
        return self._insert_pStyle(pStyle)

    def _insert_numPr(self, numPr):
        return self.insert_element_before(
            numPr, 'w:suppressLineNumbers', 'w:pBdr', 'w:shd', 'w:tabs',
            'w:suppressAutoHyphens', 'w:kinsoku', 'w:wordWrap',
            'w:overflowPunct', 'w:topLinePunct', 'w:autoSpaceDE',
            'w:autoSpaceDN', 'w:bidi', 'w:adjustRightInd', 'w:snapToGrid',
            'w:spacing', 'w:ind', 'w:contextualSpacing', 'w:mirrorIndents',
            'w:suppressOverlap', 'w:jc', 'w:textDirection',
            'w:textAlignment', 'w:textboxTightWrap', 'w:outlineLvl',
            'w:divId', 'w:cnfStyle', 'w:rPr', 'w:sectPr', 'w:pPrChange'
        )

    def _insert_pStyle(self, pStyle):
        self.insert(0, pStyle)
        return pStyle


class CT_R(OxmlBaseElement):
    """
    ``<w:r>`` element, containing the properties and text for a run.
    """
    def add_br(self):
        """
        Return a newly appended CT_Br (<w:br>) child element.
        """
        br = CT_Br.new()
        self.append(br)
        return br

    def add_drawing(self, inline_or_anchor):
        """
        Return a newly appended ``CT_Drawing`` (``<w:drawing>``) child
        element having *inline_or_anchor* as its child.
        """
        drawing = OxmlElement('w:drawing')
        self.append(drawing)
        drawing.append(inline_or_anchor)
        return drawing

    def add_t(self, text):
        """
        Return a newly added CT_T (<w:t>) element containing *text*.
        """
        t = CT_Text.new(text)
        if len(text.strip()) < len(text):
            t.set(qn('xml:space'), 'preserve')
        self.append(t)
        return t

    def get_or_add_rPr(self):
        """
        Return the rPr child element, newly added if not present.
        """
        rPr = self.rPr
        if rPr is None:
            rPr = self._add_rPr()
        return rPr

    @classmethod
    def new(cls):
        """
        Return a new ``<w:r>`` element.
        """
        return OxmlElement('w:r')

    @property
    def rPr(self):
        """
        ``<w:rPr>`` child element or None if not present.
        """
        return self.find(qn('w:rPr'))

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
    def t_lst(self):
        """
        Sequence of <w:t> elements in this paragraph.
        """
        return self.findall(qn('w:t'))

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

    def _add_rPr(self):
        """
        Return a newly added rPr child element. Assumes one is not present.
        """
        rPr = CT_RPr.new()
        self.insert(0, rPr)
        return rPr


class CT_RPr(OxmlBaseElement):
    """
    ``<w:rPr>`` element, containing the properties for a run.
    """
    def add_b(self):
        """
        Return a newly added <w:b/> child element.
        """
        b = OxmlElement('w:b')
        self.insert(0, b)
        return b

    def add_bCs(self):
        """
        Return a newly added <w:bCs/> child element.
        """
        bCs = OxmlElement('w:bCs')
        self.insert(0, bCs)
        return bCs

    def add_caps(self):
        """
        Return a newly added <w:caps/> child element.
        """
        caps = OxmlElement('w:caps')
        self.insert(0, caps)
        return caps

    def add_cs(self):
        """
        Return a newly added <w:cs/> child element.
        """
        cs = OxmlElement('w:cs')
        self.insert(0, cs)
        return cs

    def add_dstrike(self):
        """
        Return a newly added <w:dstrike/> child element.
        """
        dstrike = OxmlElement('w:dstrike')
        self.insert(0, dstrike)
        return dstrike

    def add_emboss(self):
        """
        Return a newly added <w:emboss/> child element.
        """
        emboss = OxmlElement('w:emboss')
        self.insert(0, emboss)
        return emboss

    def add_i(self):
        """
        Return a newly added <w:i/> child element.
        """
        i = OxmlElement('w:i')
        self.insert(0, i)
        return i

    def add_iCs(self):
        """
        Return a newly added <w:iCs/> child element.
        """
        iCs = OxmlElement('w:iCs')
        self.insert(0, iCs)
        return iCs

    def add_imprint(self):
        """
        Return a newly added <w:imprint/> child element.
        """
        imprint = OxmlElement('w:imprint')
        self.insert(0, imprint)
        return imprint

    def add_noProof(self):
        """
        Return a newly added <w:noProof/> child element.
        """
        noProof = OxmlElement('w:noProof')
        self.insert(0, noProof)
        return noProof

    def add_oMath(self):
        """
        Return a newly added <w:oMath/> child element.
        """
        oMath = OxmlElement('w:oMath')
        self.insert(0, oMath)
        return oMath

    def add_outline(self):
        """
        Return a newly added <w:outline/> child element.
        """
        outline = OxmlElement('w:outline')
        self.insert(0, outline)
        return outline

    def add_rtl(self):
        """
        Return a newly added <w:rtl/> child element.
        """
        rtl = OxmlElement('w:rtl')
        self.insert(0, rtl)
        return rtl

    def add_shadow(self):
        """
        Return a newly added <w:shadow/> child element.
        """
        shadow = OxmlElement('w:shadow')
        self.insert(0, shadow)
        return shadow

    def add_smallCaps(self):
        """
        Return a newly added <w:smallCaps/> child element.
        """
        smallCaps = OxmlElement('w:smallCaps')
        self.insert(0, smallCaps)
        return smallCaps

    def add_snapToGrid(self):
        """
        Return a newly added <w:snapToGrid/> child element.
        """
        snapToGrid = OxmlElement('w:snapToGrid')
        self.insert(0, snapToGrid)
        return snapToGrid

    def add_specVanish(self):
        """
        Return a newly added <w:specVanish/> child element.
        """
        specVanish = OxmlElement('w:specVanish')
        self.insert(0, specVanish)
        return specVanish

    def add_strike(self):
        """
        Return a newly added <w:strike/> child element.
        """
        strike = OxmlElement('w:strike')
        self.insert(0, strike)
        return strike

    def add_vanish(self):
        """
        Return a newly added <w:vanish/> child element.
        """
        vanish = OxmlElement('w:vanish')
        self.insert(0, vanish)
        return vanish

    def add_webHidden(self):
        """
        Return a newly added <w:webHidden/> child element.
        """
        webHidden = OxmlElement('w:webHidden')
        self.insert(0, webHidden)
        return webHidden

    @property
    def b(self):
        """
        First ``<w:b>`` child element or None if none are present.
        """
        return self.find(qn('w:b'))

    @property
    def bCs(self):
        """
        First ``<w:bCs>`` child element or None if none are present.
        """
        return self.find(qn('w:bCs'))

    @property
    def caps(self):
        """
        First ``<w:caps>`` child element or None if none are present.
        """
        return self.find(qn('w:caps'))

    @property
    def cs(self):
        """
        First ``<w:cs>`` child element or None if none are present.
        """
        return self.find(qn('w:cs'))

    @property
    def dstrike(self):
        """
        First ``<w:dstrike>`` child element or None if none are present.
        """
        return self.find(qn('w:dstrike'))

    @property
    def emboss(self):
        """
        First ``<w:emboss>`` child element or None if none are present.
        """
        return self.find(qn('w:emboss'))

    @property
    def i(self):
        """
        First ``<w:i>`` child element or None if none are present.
        """
        return self.find(qn('w:i'))

    @property
    def iCs(self):
        """
        First ``<w:iCs>`` child element or None if none are present.
        """
        return self.find(qn('w:iCs'))

    @property
    def imprint(self):
        """
        First ``<w:imprint>`` child element or None if none are present.
        """
        return self.find(qn('w:imprint'))

    @classmethod
    def new(cls):
        """
        Return a new ``<w:rPr>`` element.
        """
        return OxmlElement('w:rPr')

    @property
    def noProof(self):
        """
        First ``<w:noProof>`` child element or None if none are present.
        """
        return self.find(qn('w:noProof'))

    @property
    def oMath(self):
        """
        First ``<w:oMath>`` child element or None if none are present.
        """
        return self.find(qn('w:oMath'))

    @property
    def outline(self):
        """
        First ``<w:outline>`` child element or None if none are present.
        """
        return self.find(qn('w:outline'))

    def remove_b(self):
        b_lst = self.findall(qn('w:b'))
        for b in b_lst:
            self.remove(b)

    def remove_bCs(self):
        bCs_lst = self.findall(qn('w:bCs'))
        for bCs in bCs_lst:
            self.remove(bCs)

    def remove_caps(self):
        caps_lst = self.findall(qn('w:caps'))
        for caps in caps_lst:
            self.remove(caps)

    def remove_cs(self):
        cs_lst = self.findall(qn('w:cs'))
        for cs in cs_lst:
            self.remove(cs)

    def remove_dstrike(self):
        dstrike_lst = self.findall(qn('w:dstrike'))
        for dstrike in dstrike_lst:
            self.remove(dstrike)

    def remove_emboss(self):
        emboss_lst = self.findall(qn('w:emboss'))
        for emboss in emboss_lst:
            self.remove(emboss)

    def remove_i(self):
        i_lst = self.findall(qn('w:i'))
        for i in i_lst:
            self.remove(i)

    def remove_iCs(self):
        iCs_lst = self.findall(qn('w:iCs'))
        for iCs in iCs_lst:
            self.remove(iCs)

    def remove_imprint(self):
        imprint_lst = self.findall(qn('w:imprint'))
        for imprint in imprint_lst:
            self.remove(imprint)

    def remove_noProof(self):
        noProof_lst = self.findall(qn('w:noProof'))
        for noProof in noProof_lst:
            self.remove(noProof)

    def remove_oMath(self):
        oMath_lst = self.findall(qn('w:oMath'))
        for oMath in oMath_lst:
            self.remove(oMath)

    def remove_outline(self):
        outline_lst = self.findall(qn('w:outline'))
        for outline in outline_lst:
            self.remove(outline)

    def remove_rStyle(self):
        rStyle = self.rStyle
        if rStyle is not None:
            self.remove(rStyle)

    def remove_rtl(self):
        rtl_lst = self.findall(qn('w:rtl'))
        for rtl in rtl_lst:
            self.remove(rtl)

    def remove_shadow(self):
        shadow_lst = self.findall(qn('w:shadow'))
        for shadow in shadow_lst:
            self.remove(shadow)

    def remove_smallCaps(self):
        smallCaps_lst = self.findall(qn('w:smallCaps'))
        for smallCaps in smallCaps_lst:
            self.remove(smallCaps)

    def remove_snapToGrid(self):
        snapToGrid_lst = self.findall(qn('w:snapToGrid'))
        for snapToGrid in snapToGrid_lst:
            self.remove(snapToGrid)

    def remove_specVanish(self):
        specVanish_lst = self.findall(qn('w:specVanish'))
        for specVanish in specVanish_lst:
            self.remove(specVanish)

    def remove_strike(self):
        strike_lst = self.findall(qn('w:strike'))
        for strike in strike_lst:
            self.remove(strike)

    def remove_u(self):
        u_lst = self.findall(qn('w:u'))
        for u in u_lst:
            self.remove(u)

    def remove_vanish(self):
        vanish_lst = self.findall(qn('w:vanish'))
        for vanish in vanish_lst:
            self.remove(vanish)

    def remove_webHidden(self):
        webHidden_lst = self.findall(qn('w:webHidden'))
        for webHidden in webHidden_lst:
            self.remove(webHidden)

    @property
    def rStyle(self):
        """
        ``<w:rStyle>`` child element or None if not present.
        """
        return self.find(qn('w:rStyle'))

    @property
    def rtl(self):
        """
        First ``<w:rtl>`` child element or None if none are present.
        """
        return self.find(qn('w:rtl'))

    @property
    def shadow(self):
        """
        First ``<w:shadow>`` child element or None if none are present.
        """
        return self.find(qn('w:shadow'))

    @property
    def smallCaps(self):
        """
        First ``<w:smallCaps>`` child element or None if none are present.
        """
        return self.find(qn('w:smallCaps'))

    @property
    def snapToGrid(self):
        """
        First ``<w:snapToGrid>`` child element or None if none are present.
        """
        return self.find(qn('w:snapToGrid'))

    @property
    def specVanish(self):
        """
        First ``<w:specVanish>`` child element or None if none are present.
        """
        return self.find(qn('w:specVanish'))

    @property
    def strike(self):
        """
        First ``<w:strike>`` child element or None if none are present.
        """
        return self.find(qn('w:strike'))

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
            self.remove_rStyle()
        elif self.rStyle is None:
            self._add_rStyle(style)
        else:
            self.rStyle.val = style

    @property
    def u(self):
        """
        First ``<w:u>`` child element or |None| if none are present.
        """
        return self.find(qn('w:u'))

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
        self.remove_u()
        if value is not None:
            u = self._add_u()
            u.val = value

    @property
    def vanish(self):
        """
        First ``<w:vanish>`` child element or None if none are present.
        """
        return self.find(qn('w:vanish'))

    @property
    def webHidden(self):
        """
        First ``<w:webHidden>`` child element or None if none are present.
        """
        return self.find(qn('w:webHidden'))

    def _add_rStyle(self, style):
        rStyle = CT_String.new_rStyle(style)
        self.insert(0, rStyle)
        return rStyle

    def _add_u(self):
        """
        Return a newly added <w:u/> child element.
        """
        u = OxmlElement('w:u')
        self.insert(0, u)
        return u


class CT_Text(OxmlBaseElement):
    """
    ``<w:t>`` element, containing a sequence of characters within a run.
    """
    @classmethod
    def new(cls, text):
        """
        Return a new ``<w:t>`` element.
        """
        t = OxmlElement('w:t')
        t.text = text
        return t


class CT_Underline(OxmlBaseElement):
    """
    ``<w:u>`` element, specifying the underlining style for a run.
    """
    @property
    def val(self):
        """
        The underline type corresponding to the ``w:val`` attribute value.
        """
        underline_type_map = {
            None:              None,
            'none':            False,
            'single':          True,
            'words':           WD_UNDERLINE.WORDS,
            'double':          WD_UNDERLINE.DOUBLE,
            'dotted':          WD_UNDERLINE.DOTTED,
            'thick':           WD_UNDERLINE.THICK,
            'dash':            WD_UNDERLINE.DASH,
            'dotDash':         WD_UNDERLINE.DOT_DASH,
            'dotDotDash':      WD_UNDERLINE.DOT_DOT_DASH,
            'wave':            WD_UNDERLINE.WAVY,
            'dottedHeavy':     WD_UNDERLINE.DOTTED_HEAVY,
            'dashedHeavy':     WD_UNDERLINE.DASH_HEAVY,
            'dashDotHeavy':    WD_UNDERLINE.DOT_DASH_HEAVY,
            'dashDotDotHeavy': WD_UNDERLINE.DOT_DOT_DASH_HEAVY,
            'wavyHeavy':       WD_UNDERLINE.WAVY_HEAVY,
            'dashLong':        WD_UNDERLINE.DASH_LONG,
            'wavyDouble':      WD_UNDERLINE.WAVY_DOUBLE,
            'dashLongHeavy':   WD_UNDERLINE.DASH_LONG_HEAVY,
        }
        val = self.get(qn('w:val'))
        return underline_type_map[val]

    @val.setter
    def val(self, value):
        underline_vals = {
            True:                            'single',
            False:                           'none',
            WD_UNDERLINE.WORDS:              'words',
            WD_UNDERLINE.DOUBLE:             'double',
            WD_UNDERLINE.DOTTED:             'dotted',
            WD_UNDERLINE.THICK:              'thick',
            WD_UNDERLINE.DASH:               'dash',
            WD_UNDERLINE.DOT_DASH:           'dotDash',
            WD_UNDERLINE.DOT_DOT_DASH:       'dotDotDash',
            WD_UNDERLINE.WAVY:               'wave',
            WD_UNDERLINE.DOTTED_HEAVY:       'dottedHeavy',
            WD_UNDERLINE.DASH_HEAVY:         'dashedHeavy',
            WD_UNDERLINE.DOT_DASH_HEAVY:     'dashDotHeavy',
            WD_UNDERLINE.DOT_DOT_DASH_HEAVY: 'dashDotDotHeavy',
            WD_UNDERLINE.WAVY_HEAVY:         'wavyHeavy',
            WD_UNDERLINE.DASH_LONG:          'dashLong',
            WD_UNDERLINE.WAVY_DOUBLE:        'wavyDouble',
            WD_UNDERLINE.DASH_LONG_HEAVY:    'dashLongHeavy',
        }
        val = underline_vals[value]
        self.set(qn('w:val'), val)
