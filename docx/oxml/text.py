# encoding: utf-8

"""
Custom element classes related to text, such as paragraph (CT_P) and runs
(CT_R).
"""

from docx.oxml.parts.numbering import CT_NumPr
from docx.oxml.shared import (
    CT_String,
    nsdecls, OxmlBaseElement, OxmlElement, oxml_fromstring, qn
)
from docx.enum.text import WD_UNDERLINE

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
        
    @property
    def jc(self):
        """
        String contained in w:val attribute of <w:pPr><w:jc> child, or
        None if that element is not present.
        """
        pPr = self.pPr
        if pPr is None:
            return None
        return pPr.jc

    @jc.setter
    def jc(self, jc):
        """
        Set style of this <w:p> element to *jc*. If *jc* is None,
        remove the style element.
        """
        pPr = self.get_or_add_pPr()
        pPr.jc = jc
        
    @property
    def textDirection(self):
        """
        String contained in w:val attribute of <w:pPr><w:textDirection> child,
        or None if that element is not present.
        """
        pPr = self.pPr
        if pPr is None:
            return None
        return pPr.textdirection

    @textDirection.setter
    def textDirection(self, textdirection):
        """
        Set style of this <w:p> element to *style*. If *style* is None,
        remove the style element.
        """
        pPr = self.get_or_add_pPr()
        pPr.textdirection = textdirection

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
        
    def get_or_add_textDirectionElement(self):
        """
        Return the textDirection child element, newly added if not present.
        """
        textDirection = self.textDirection
        if textDirection is None:
            textDirection = self._add_textDirection()
        return textDirection

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
            
    @property
    def jcElement(self):
        """
        ``<w:jc>`` child element or None if not present.
        """
        return self.find(qn('w:jc'))
        
    def remove_jcElement(self):
        jcElement = self.jcElement
        if jcElement is not None:
            self.remove(jcElement)
            
    @property
    def jc(self):
        """
        String contained in <w:jc> child, or None if that element is
        not present.
        """
        jc = self.jcElement
        if jc is None:
            return None
        return jc.get(qn('w:val'))
        
    @jc.setter
    def jc(self, jc):
        """
        Set val attribute of <w:jc> child element to *jc*, adding a
        new element if necessary. If *jc* is |None|, remove the <w:jc>
        element if present.
        """
        if jc is None:
            self.remove_jcDirection()
        elif self.jcElement is None:
            self._add_jcElement(jc)
        else:
            self.jcElement.val = jc
            
    @property
    def textDirectionElement(self):
        """
        ``<w:pStyle>`` child element or None if not present.
        """
        return self.find(qn('w:textDirection'))
        
    def remove_textDirectionElement(self):
        textDirectionElement = self.textDirectionElement
        if textDirectionElement is not None:
            self.remove(textDirectionElement)
            
    @property
    def textDirection(self):
        """
        String contained in <w:textDirection> child, or None if that element is
        not present.
        """
        textDirection = self.textDirectionElement
        if textDirection is None:
            return None
        return textDirection.get(qn('w:val'))
        
    @textDirection.setter
    def textDirection(self, textDirection):
        """
        Set val attribute of <w:textDirection> child element to
        *textDirection*, adding a new element if necessary. If *textDirection*
        is |None|, remove the <w:textDirection> element if present.
        """
        if textDirection is None:
            self.remove_textDirectionElement()
        elif self.textDirectionElement is None:
            self._add_textDirectionElement(textDirection)
        else:
            self.textDirectionElement.val = textDirection

    def _add_numPr(self):
        numPr = CT_NumPr.new()
        return self._insert_numPr(numPr)

    def _add_pStyle(self, style):
        pStyle = CT_String.new_pStyle(style)
        return self._insert_pStyle(pStyle)
        
    def _add_jcElement(self, jc):
        jcElement = CT_String.new('w:jc', jc)
        return self._insert_jcElement(jcElement)
        
    def _add_textDirectionElement(self, textDirection):
        textDirectionElement = CT_String.new('w:textDirection', textDirection)
        return self._insert_textDirectionElement(textDirectionElement)

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
        
    def _insert_jcElement(self, jc):
        return self.insert_element_before(
            jc, 'w:textDirection', 'w:textAlignment', 'w:textboxTightWrap',
            'w:outlineLvl', 'w:divId', 'w:cnfStyle', 'w:rPr', 'w:sectPr',
            'w:pPrChange'
        )        
        
    def _insert_textDirectionElement(self, textDirection):
        return self.insert_element_before(
            textDirection, 'w:textAlignment', 'w:textboxTightWrap',
            'w:outlineLvl', 'w:divId', 'w:cnfStyle', 'w:rPr', 'w:sectPr',
            'w:pPrChange'
        )

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
    def t_lst(self):
        """
        Sequence of <w:t> elements in this paragraph.
        """
        return self.findall(qn('w:t'))

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
        
    def add_underline(self, utype):
        """
        Return a newly added <w:u w:val=utype/> child element.
        """
        u = CT_String.new('w:u', WD_UNDERLINE.stringDict[utype])
        self.insert(0, u)
        return u

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

    def remove_vanish(self):
        vanish_lst = self.findall(qn('w:vanish'))
        for vanish in vanish_lst:
            self.remove(vanish)

    def remove_webHidden(self):
        webHidden_lst = self.findall(qn('w:webHidden'))
        for webHidden in webHidden_lst:
            self.remove(webHidden)
            
    def remove_underline(self):
        underline_lst = self.findall(qn('w:u'))
        for underline in underline_lst:
            self.remove(underline)

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
        
    @property
    def underline(self):
        """
        First ``<w:u>`` child element or None if none are present.
        """
        return self.find(qn('w:u'))


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
