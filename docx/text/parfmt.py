# encoding: utf-8

"""
Paragraph-related proxy types.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..enum.text import WD_LINE_SPACING
from ..shared import ElementProxy, Emu, lazyproperty, Length, Pt, Twips
from .tabstops import TabStops


class ParagraphFormat(ElementProxy):
    """
    Provides access to paragraph formatting such as justification,
    indentation, line spacing, space before and after, and widow/orphan
    control.
    """

    __slots__ = ('_tab_stops',)

    @property
    def alignment(self):
        """
        A member of the :ref:`WdParagraphAlignment` enumeration specifying
        the justification setting for this paragraph. A value of |None|
        indicates paragraph alignment is inherited from the style hierarchy.
        """
        pPr = self._element.pPr
        if pPr is None:
            return None
        return pPr.jc_val

    @alignment.setter
    def alignment(self, value):
        pPr = self._element.get_or_add_pPr()
        pPr.jc_val = value

    @property
    def first_line_indent(self):
        """
        |Length| value specifying the relative difference in indentation for
        the first line of the paragraph. A positive value causes the first
        line to be indented. A negative value produces a hanging indent.
        |None| indicates first line indentation is inherited from the style
        hierarchy.
        """
        pPr = self._element.pPr
        if pPr is None:
            return None
        return pPr.first_line_indent

    @first_line_indent.setter
    def first_line_indent(self, value):
        pPr = self._element.get_or_add_pPr()
        pPr.first_line_indent = value

    @property
    def keep_together(self):
        """
        |True| if the paragraph should be kept "in one piece" and not broken
        across a page boundary when the document is rendered. |None|
        indicates its effective value is inherited from the style hierarchy.
        """
        pPr = self._element.pPr
        if pPr is None:
            return None
        return pPr.keepLines_val

    @keep_together.setter
    def keep_together(self, value):
        self._element.get_or_add_pPr().keepLines_val = value

    @property
    def keep_with_next(self):
        """
        |True| if the paragraph should be kept on the same page as the
        subsequent paragraph when the document is rendered. For example, this
        property could be used to keep a section heading on the same page as
        its first paragraph. |None| indicates its effective value is
        inherited from the style hierarchy.
        """
        pPr = self._element.pPr
        if pPr is None:
            return None
        return pPr.keepNext_val

    @keep_with_next.setter
    def keep_with_next(self, value):
        self._element.get_or_add_pPr().keepNext_val = value

    @property
    def left_indent(self):
        """
        |Length| value specifying the space between the left margin and the
        left side of the paragraph. |None| indicates the left indent value is
        inherited from the style hierarchy. Use an |Inches| value object as
        a convenient way to apply indentation in units of inches.
        """
        pPr = self._element.pPr
        if pPr is None:
            return None
        return pPr.ind_left

    @left_indent.setter
    def left_indent(self, value):
        pPr = self._element.get_or_add_pPr()
        pPr.ind_left = value

    @property
    def line_spacing(self):
        """
        |float| or |Length| value specifying the space between baselines in
        successive lines of the paragraph. A value of |None| indicates line
        spacing is inherited from the style hierarchy. A float value, e.g.
        ``2.0`` or ``1.75``, indicates spacing is applied in multiples of
        line heights. A |Length| value such as ``Pt(12)`` indicates spacing
        is a fixed height. The |Pt| value class is a convenient way to apply
        line spacing in units of points. Assigning |None| resets line spacing
        to inherit from the style hierarchy.
        """
        pPr = self._element.pPr
        if pPr is None:
            return None
        return self._line_spacing(pPr.spacing_line, pPr.spacing_lineRule)

    @line_spacing.setter
    def line_spacing(self, value):
        pPr = self._element.get_or_add_pPr()
        if value is None:
            pPr.spacing_line = None
            pPr.spacing_lineRule = None
        elif isinstance(value, Length):
            pPr.spacing_line = value
            if pPr.spacing_lineRule != WD_LINE_SPACING.AT_LEAST:
                pPr.spacing_lineRule = WD_LINE_SPACING.EXACTLY
        else:
            pPr.spacing_line = Emu(value * Twips(240))
            pPr.spacing_lineRule = WD_LINE_SPACING.MULTIPLE

    @property
    def line_spacing_rule(self):
        """
        A member of the :ref:`WdLineSpacing` enumeration indicating how the
        value of :attr:`line_spacing` should be interpreted. Assigning any of
        the :ref:`WdLineSpacing` members :attr:`SINGLE`, :attr:`DOUBLE`, or
        :attr:`ONE_POINT_FIVE` will cause the value of :attr:`line_spacing`
        to be updated to produce the corresponding line spacing.
        """
        pPr = self._element.pPr
        if pPr is None:
            return None
        return self._line_spacing_rule(
            pPr.spacing_line, pPr.spacing_lineRule
        )

    @line_spacing_rule.setter
    def line_spacing_rule(self, value):
        pPr = self._element.get_or_add_pPr()
        if value == WD_LINE_SPACING.SINGLE:
            pPr.spacing_line = Twips(240)
            pPr.spacing_lineRule = WD_LINE_SPACING.MULTIPLE
        elif value == WD_LINE_SPACING.ONE_POINT_FIVE:
            pPr.spacing_line = Twips(360)
            pPr.spacing_lineRule = WD_LINE_SPACING.MULTIPLE
        elif value == WD_LINE_SPACING.DOUBLE:
            pPr.spacing_line = Twips(480)
            pPr.spacing_lineRule = WD_LINE_SPACING.MULTIPLE
        else:
            pPr.spacing_lineRule = value

    @property
    def page_break_before(self):
        """
        |True| if the paragraph should appear at the top of the page
        following the prior paragraph. |None| indicates its effective value
        is inherited from the style hierarchy.
        """
        pPr = self._element.pPr
        if pPr is None:
            return None
        return pPr.pageBreakBefore_val

    @page_break_before.setter
    def page_break_before(self, value):
        self._element.get_or_add_pPr().pageBreakBefore_val = value

    @property
    def right_indent(self):
        """
        |Length| value specifying the space between the right margin and the
        right side of the paragraph. |None| indicates the right indent value
        is inherited from the style hierarchy. Use a |Cm| value object as
        a convenient way to apply indentation in units of centimeters.
        """
        pPr = self._element.pPr
        if pPr is None:
            return None
        return pPr.ind_right

    @right_indent.setter
    def right_indent(self, value):
        pPr = self._element.get_or_add_pPr()
        pPr.ind_right = value

    @property
    def space_after(self):
        """
        |Length| value specifying the spacing to appear between this
        paragraph and the subsequent paragraph. |None| indicates this value
        is inherited from the style hierarchy. |Length| objects provide
        convenience properties, such as :attr:`~.Length.pt` and
        :attr:`~.Length.inches`, that allow easy conversion to various length
        units.
        """
        pPr = self._element.pPr
        if pPr is None:
            return None
        return pPr.spacing_after

    @space_after.setter
    def space_after(self, value):
        self._element.get_or_add_pPr().spacing_after = value

    @property
    def space_before(self):
        """
        |Length| value specifying the spacing to appear between this
        paragraph and the prior paragraph. |None| indicates this value is
        inherited from the style hierarchy. |Length| objects provide
        convenience properties, such as :attr:`~.Length.pt` and
        :attr:`~.Length.cm`, that allow easy conversion to various length
        units.
        """
        pPr = self._element.pPr
        if pPr is None:
            return None
        return pPr.spacing_before

    @space_before.setter
    def space_before(self, value):
        self._element.get_or_add_pPr().spacing_before = value

    @lazyproperty
    def tab_stops(self):
        """
        |TabStops| object providing access to the tab stops defined for this
        paragraph format.
        """
        pPr = self._element.get_or_add_pPr()
        return TabStops(pPr)

    @property
    def widow_control(self):
        """
        |True| if the first and last lines in the paragraph remain on the
        same page as the rest of the paragraph when Word repaginates the
        document. |None| indicates its effective value is inherited from the
        style hierarchy.
        """
        pPr = self._element.pPr
        if pPr is None:
            return None
        return pPr.widowControl_val

    @widow_control.setter
    def widow_control(self, value):
        self._element.get_or_add_pPr().widowControl_val = value

    @staticmethod
    def _line_spacing(spacing_line, spacing_lineRule):
        """
        Return the line spacing value calculated from the combination of
        *spacing_line* and *spacing_lineRule*. Returns a |float| number of
        lines when *spacing_lineRule* is ``WD_LINE_SPACING.MULTIPLE``,
        otherwise a |Length| object of absolute line height is returned.
        Returns |None| when *spacing_line* is |None|.
        """
        if spacing_line is None:
            return None
        if spacing_lineRule == WD_LINE_SPACING.MULTIPLE:
            return spacing_line / Pt(12)
        return spacing_line

    @staticmethod
    def _line_spacing_rule(line, lineRule):
        """
        Return the line spacing rule value calculated from the combination of
        *line* and *lineRule*. Returns special members of the
        :ref:`WdLineSpacing` enumeration when line spacing is single, double,
        or 1.5 lines.
        """
        if lineRule == WD_LINE_SPACING.MULTIPLE:
            if line == Twips(240):
                return WD_LINE_SPACING.SINGLE
            if line == Twips(360):
                return WD_LINE_SPACING.ONE_POINT_FIVE
            if line == Twips(480):
                return WD_LINE_SPACING.DOUBLE
        return lineRule
