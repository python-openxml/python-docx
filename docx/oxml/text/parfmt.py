# encoding: utf-8

"""
Custom element classes related to paragraph properties (CT_PPr).
"""

from ...enum.text import (
    WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT, WD_TAB_LEADER
)
from ...shared import Length
from ..simpletypes import ST_SignedTwipsMeasure, ST_TwipsMeasure
from ..xmlchemy import (
    BaseOxmlElement, OneOrMore, OptionalAttribute, RequiredAttribute,
    ZeroOrOne
)


class CT_Ind(BaseOxmlElement):
    """
    ``<w:ind>`` element, specifying paragraph indentation.
    """
    left = OptionalAttribute('w:left', ST_SignedTwipsMeasure)
    right = OptionalAttribute('w:right', ST_SignedTwipsMeasure)
    firstLine = OptionalAttribute('w:firstLine', ST_TwipsMeasure)
    hanging = OptionalAttribute('w:hanging', ST_TwipsMeasure)


class CT_Jc(BaseOxmlElement):
    """
    ``<w:jc>`` element, specifying paragraph justification.
    """
    val = RequiredAttribute('w:val', WD_ALIGN_PARAGRAPH)


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
    keepNext = ZeroOrOne('w:keepNext', successors=_tag_seq[2:])
    keepLines = ZeroOrOne('w:keepLines', successors=_tag_seq[3:])
    pageBreakBefore = ZeroOrOne('w:pageBreakBefore', successors=_tag_seq[4:])
    widowControl = ZeroOrOne('w:widowControl', successors=_tag_seq[6:])
    numPr = ZeroOrOne('w:numPr', successors=_tag_seq[7:])
    tabs = ZeroOrOne('w:tabs', successors=_tag_seq[11:])
    spacing = ZeroOrOne('w:spacing', successors=_tag_seq[22:])
    ind = ZeroOrOne('w:ind', successors=_tag_seq[23:])
    jc = ZeroOrOne('w:jc', successors=_tag_seq[27:])
    rPr = ZeroOrOne('w:rPr', successors=_tag_seq[34:])
    sectPr = ZeroOrOne('w:sectPr', successors=_tag_seq[35:])
    del _tag_seq

    @property
    def first_line_indent(self):
        """
        A |Length| value calculated from the values of `w:ind/@w:firstLine`
        and `w:ind/@w:hanging`. Returns |None| if the `w:ind` child is not
        present.
        """
        ind = self.ind
        if ind is None:
            return None
        hanging = ind.hanging
        if hanging is not None:
            return Length(-hanging)
        firstLine = ind.firstLine
        if firstLine is None:
            return None
        return firstLine

    @first_line_indent.setter
    def first_line_indent(self, value):
        if self.ind is None and value is None:
            return
        ind = self.get_or_add_ind()
        ind.firstLine = ind.hanging = None
        if value is None:
            return
        elif value < 0:
            ind.hanging = -value
        else:
            ind.firstLine = value

    @property
    def ind_left(self):
        """
        The value of `w:ind/@w:left` or |None| if not present.
        """
        ind = self.ind
        if ind is None:
            return None
        return ind.left

    @ind_left.setter
    def ind_left(self, value):
        if value is None and self.ind is None:
            return
        ind = self.get_or_add_ind()
        ind.left = value

    @property
    def ind_right(self):
        """
        The value of `w:ind/@w:right` or |None| if not present.
        """
        ind = self.ind
        if ind is None:
            return None
        return ind.right

    @ind_right.setter
    def ind_right(self, value):
        if value is None and self.ind is None:
            return
        ind = self.get_or_add_ind()
        ind.right = value

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
    def keepLines_val(self):
        """
        The value of `keepLines/@val` or |None| if not present.
        """
        keepLines = self.keepLines
        if keepLines is None:
            return None
        return keepLines.val

    @keepLines_val.setter
    def keepLines_val(self, value):
        if value is None:
            self._remove_keepLines()
        else:
            self.get_or_add_keepLines().val = value

    @property
    def keepNext_val(self):
        """
        The value of `keepNext/@val` or |None| if not present.
        """
        keepNext = self.keepNext
        if keepNext is None:
            return None
        return keepNext.val

    @keepNext_val.setter
    def keepNext_val(self, value):
        if value is None:
            self._remove_keepNext()
        else:
            self.get_or_add_keepNext().val = value

    @property
    def pageBreakBefore_val(self):
        """
        The value of `pageBreakBefore/@val` or |None| if not present.
        """
        pageBreakBefore = self.pageBreakBefore
        if pageBreakBefore is None:
            return None
        return pageBreakBefore.val

    @pageBreakBefore_val.setter
    def pageBreakBefore_val(self, value):
        if value is None:
            self._remove_pageBreakBefore()
        else:
            self.get_or_add_pageBreakBefore().val = value

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

    @spacing_line.setter
    def spacing_line(self, value):
        if value is None and self.spacing is None:
            return
        self.get_or_add_spacing().line = value

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

    @spacing_lineRule.setter
    def spacing_lineRule(self, value):
        if value is None and self.spacing is None:
            return
        self.get_or_add_spacing().lineRule = value

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

    @property
    def widowControl_val(self):
        """
        The value of `widowControl/@val` or |None| if not present.
        """
        widowControl = self.widowControl
        if widowControl is None:
            return None
        return widowControl.val

    @widowControl_val.setter
    def widowControl_val(self, value):
        if value is None:
            self._remove_widowControl()
        else:
            self.get_or_add_widowControl().val = value


class CT_Spacing(BaseOxmlElement):
    """
    ``<w:spacing>`` element, specifying paragraph spacing attributes such as
    space before and line spacing.
    """
    after = OptionalAttribute('w:after', ST_TwipsMeasure)
    before = OptionalAttribute('w:before', ST_TwipsMeasure)
    line = OptionalAttribute('w:line', ST_SignedTwipsMeasure)
    lineRule = OptionalAttribute('w:lineRule', WD_LINE_SPACING)


class CT_TabStop(BaseOxmlElement):
    """
    ``<w:tab>`` element, representing an individual tab stop.
    """
    val = RequiredAttribute('w:val', WD_TAB_ALIGNMENT)
    leader = OptionalAttribute(
        'w:leader', WD_TAB_LEADER, default=WD_TAB_LEADER.SPACES
    )
    pos = RequiredAttribute('w:pos', ST_SignedTwipsMeasure)


class CT_TabStops(BaseOxmlElement):
    """
    ``<w:tabs>`` element, container for a sorted sequence of tab stops.
    """
    tab = OneOrMore('w:tab', successors=())

    def insert_tab_in_order(self, pos, align, leader):
        """
        Insert a newly created `w:tab` child element in *pos* order.
        """
        new_tab = self._new_tab()
        new_tab.pos, new_tab.val, new_tab.leader = pos, align, leader
        for tab in self.tab_lst:
            if new_tab.pos < tab.pos:
                tab.addprevious(new_tab)
                return new_tab
        self.append(new_tab)
        return new_tab
