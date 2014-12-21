# encoding: utf-8

"""
Custom element classes related to text, such as paragraph (CT_P) and runs
(CT_R).
"""

from ...enum.text import WD_ALIGN_PARAGRAPH
from ..ns import qn
from ..xmlchemy import (
    BaseOxmlElement, OxmlElement, RequiredAttribute, ZeroOrMore, ZeroOrOne
)


class CT_Jc(BaseOxmlElement):
    """
    ``<w:jc>`` element, specifying paragraph justification.
    """
    val = RequiredAttribute('w:val', WD_ALIGN_PARAGRAPH)


class CT_P(BaseOxmlElement):
    """
    ``<w:p>`` element, containing the properties and text for a paragraph.
    """
    pPr = ZeroOrOne('w:pPr')
    r = ZeroOrMore('w:r')

    def _insert_pPr(self, pPr):
        self.insert(0, pPr)
        return pPr

    def add_p_before(self):
        """
        Return a new ``<w:p>`` element inserted directly prior to this one.
        """
        new_p = OxmlElement('w:p')
        self.addprevious(new_p)
        return new_p

    @property
    def alignment(self):
        """
        The value of the ``<w:jc>`` grandchild element or |None| if not
        present.
        """
        pPr = self.pPr
        if pPr is None:
            return None
        return pPr.alignment

    @alignment.setter
    def alignment(self, value):
        pPr = self.get_or_add_pPr()
        pPr.alignment = value

    def clear_content(self):
        """
        Remove all child elements, except the ``<w:pPr>`` element if present.
        """
        for child in self[:]:
            if child.tag == qn('w:pPr'):
                continue
            self.remove(child)

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
        String contained in w:val attribute of ./w:pPr/w:pStyle grandchild,
        or |None| if not present.
        """
        pPr = self.pPr
        if pPr is None:
            return None
        return pPr.style

    @style.setter
    def style(self, style):
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
    jc = ZeroOrOne('w:jc', successors=__child_sequence__[27:])
    sectPr = ZeroOrOne('w:sectPr', successors=('w:pPrChange',))

    def _insert_pStyle(self, pStyle):
        self.insert(0, pStyle)
        return pStyle

    @property
    def alignment(self):
        """
        The value of the ``<w:jc>`` child element or |None| if not present.
        """
        jc = self.jc
        if jc is None:
            return None
        return jc.val

    @alignment.setter
    def alignment(self, value):
        if value is None:
            self._remove_jc()
            return
        jc = self.get_or_add_jc()
        jc.val = value

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
