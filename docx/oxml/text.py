# encoding: utf-8

"""
Custom element classes related to text, such as paragraph (CT_P) and runs
(CT_R).
"""

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
        self.get(qn('w:type'))

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

    def _add_pStyle(self, style):
        pStyle = CT_String.new_pStyle(style)
        return self._insert_pStyle(pStyle)

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
        self.append(t)
        return t

    @classmethod
    def new(cls):
        """
        Return a new ``<w:r>`` element.
        """
        return OxmlElement('w:r')

    @property
    def t_lst(self):
        """
        Sequence of <w:t> elements in this paragraph.
        """
        return self.findall(qn('w:t'))


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
