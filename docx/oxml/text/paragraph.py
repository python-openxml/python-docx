# encoding: utf-8

"""
Custom element classes related to paragraphs (CT_P).
"""

from ...enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from ..ns import qn
from ..simpletypes import ST_SignedTwipsMeasure, ST_TwipsMeasure
from ..xmlchemy import (
    BaseOxmlElement, OptionalAttribute, OxmlElement, RequiredAttribute,
    ZeroOrMore, ZeroOrOne
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
        return pPr.jc_val

    @alignment.setter
    def alignment(self, value):
        pPr = self.get_or_add_pPr()
        pPr.jc_val = value

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
    _tag_seq = (
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
    pStyle = ZeroOrOne('w:pStyle', successors=_tag_seq[1:])
    numPr = ZeroOrOne('w:numPr', successors=_tag_seq[7:])
    spacing = ZeroOrOne('w:spacing', successors=_tag_seq[22:])
    jc = ZeroOrOne('w:jc', successors=_tag_seq[27:])
    sectPr = ZeroOrOne('w:sectPr', successors=_tag_seq[35:])
    del _tag_seq

    @property
    def jc_val(self):
        """
        The value of the ``<w:jc>`` child element or |None| if not present.
        """
        jc = self.jc
        if jc is None:
            return None
        return jc.val

    @jc_val.setter
    def jc_val(self, value):
        if value is None:
            self._remove_jc()
            return
        self.get_or_add_jc().val = value

    @property
    def spacing_after(self):
        """
        The value of `w:spacing/@w:after` or |None| if not present.
        """
        spacing = self.spacing
        if spacing is None:
            return None
        return spacing.after

    @spacing_after.setter
    def spacing_after(self, value):
        if value is None and self.spacing is None:
            return
        self.get_or_add_spacing().after = value

    @property
    def spacing_before(self):
        """
        The value of `w:spacing/@w:before` or |None| if not present.
        """
        spacing = self.spacing
        if spacing is None:
            return None
        return spacing.before

    @spacing_before.setter
    def spacing_before(self, value):
        if value is None and self.spacing is None:
            return
        self.get_or_add_spacing().before = value

    @property
    def spacing_line(self):
        """
        The value of `w:spacing/@w:line` or |None| if not present.
        """
        spacing = self.spacing
        if spacing is None:
            return None
        return spacing.line

    @property
    def spacing_lineRule(self):
        """
        The value of `w:spacing/@w:lineRule` as a member of the
        :ref:`WdLineSpacing` enumeration. Only the `MULTIPLE`, `EXACTLY`, and
        `AT_LEAST` members are used. It is the responsibility of the client
        to calculate the use of `SINGLE`, `DOUBLE`, and `MULTIPLE` based on
        the value of `w:spacing/@w:line` if that behavior is desired.
        """
        spacing = self.spacing
        if spacing is None:
            return None
        lineRule = spacing.lineRule
        if lineRule is None and spacing.line is not None:
            return WD_LINE_SPACING.MULTIPLE
        return lineRule

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


class CT_Spacing(BaseOxmlElement):
    """
    ``<w:spacing>`` element, specifying paragraph spacing attributes such as
    space before and line spacing.
    """
    after = OptionalAttribute('w:after', ST_TwipsMeasure)
    before = OptionalAttribute('w:before', ST_TwipsMeasure)
    line = OptionalAttribute('w:line', ST_SignedTwipsMeasure)
    lineRule = OptionalAttribute('w:lineRule', WD_LINE_SPACING)
