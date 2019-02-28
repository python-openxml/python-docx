# encoding: utf-8

"""
The |Section| object and related proxy classes.
"""

from __future__ import absolute_import, print_function, unicode_literals

from collections import Sequence


class Sections(Sequence):
    """
    Sequence of |Section| objects corresponding to the sections in the
    document. Supports ``len()``, iteration, and indexed access.
    """
    def __init__(self, document_elm):
        super(Sections, self).__init__()
        self._document_elm = document_elm

    def __getitem__(self, key):
        if isinstance(key, slice):
            sectPr_lst = self._document_elm.sectPr_lst[key]
            return [Section(sectPr) for sectPr in sectPr_lst]
        sectPr = self._document_elm.sectPr_lst[key]
        return Section(sectPr)

    def __iter__(self):
        for sectPr in self._document_elm.sectPr_lst:
            yield Section(sectPr)

    def __len__(self):
        return len(self._document_elm.sectPr_lst)


class Section(object):
    """
    Document section, providing access to section and page setup settings.
    """
    def __init__(self, sectPr):
        super(Section, self).__init__()
        self._sectPr = sectPr

    @property
    def bottom_margin(self):
        """
        |Length| object representing the bottom margin for all pages in this
        section in English Metric Units.
        """
        return self._sectPr.bottom_margin

    @bottom_margin.setter
    def bottom_margin(self, value):
        self._sectPr.bottom_margin = value

    @property
    def footer_distance(self):
        """
        |Length| object representing the distance from the bottom edge of the
        page to the bottom edge of the footer. |None| if no setting is present
        in the XML.
        """
        return self._sectPr.footer

    @footer_distance.setter
    def footer_distance(self, value):
        self._sectPr.footer = value

    @property
    def gutter(self):
        """
        |Length| object representing the page gutter size in English Metric
        Units for all pages in this section. The page gutter is extra spacing
        added to the *inner* margin to ensure even margins after page
        binding.
        """
        return self._sectPr.gutter

    @gutter.setter
    def gutter(self, value):
        self._sectPr.gutter = value

    @property
    def header_distance(self):
        """
        |Length| object representing the distance from the top edge of the
        page to the top edge of the header. |None| if no setting is present
        in the XML.
        """
        return self._sectPr.header

    @header_distance.setter
    def header_distance(self, value):
        self._sectPr.header = value

    @property
    def left_margin(self):
        """
        |Length| object representing the left margin for all pages in this
        section in English Metric Units.
        """
        return self._sectPr.left_margin

    @left_margin.setter
    def left_margin(self, value):
        self._sectPr.left_margin = value

    @property
    def orientation(self):
        """
        Member of the :ref:`WdOrientation` enumeration specifying the page
        orientation for this section, one of ``WD_ORIENT.PORTRAIT`` or
        ``WD_ORIENT.LANDSCAPE``.
        """
        return self._sectPr.orientation

    @orientation.setter
    def orientation(self, value):
        self._sectPr.orientation = value

    @property
    def page_height(self):
        """
        Total page height used for this section, inclusive of all edge spacing
        values such as margins. Page orientation is taken into account, so
        for example, its expected value would be ``Inches(8.5)`` for
        letter-sized paper when orientation is landscape.
        """
        return self._sectPr.page_height

    @page_height.setter
    def page_height(self, value):
        self._sectPr.page_height = value

    @property
    def page_width(self):
        """
        Total page width used for this section, inclusive of all edge spacing
        values such as margins. Page orientation is taken into account, so
        for example, its expected value would be ``Inches(11)`` for
        letter-sized paper when orientation is landscape.
        """
        return self._sectPr.page_width

    @page_width.setter
    def page_width(self, value):
        self._sectPr.page_width = value

    @property
    def right_margin(self):
        """
        |Length| object representing the right margin for all pages in this
        section in English Metric Units.
        """
        return self._sectPr.right_margin

    @right_margin.setter
    def right_margin(self, value):
        self._sectPr.right_margin = value

    @property
    def start_type(self):
        """
        The member of the :ref:`WdSectionStart` enumeration corresponding to
        the initial break behavior of this section, e.g.
        ``WD_SECTION.ODD_PAGE`` if the section should begin on the next odd
        page.
        """
        return self._sectPr.start_type

    @start_type.setter
    def start_type(self, value):
        self._sectPr.start_type = value

    @property
    def top_margin(self):
        """
        |Length| object representing the top margin for all pages in this
        section in English Metric Units.
        """
        return self._sectPr.top_margin

    @top_margin.setter
    def top_margin(self, value):
        self._sectPr.top_margin = value
