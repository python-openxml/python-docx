# encoding: utf-8

"""
The |Section| object and related proxy classes.
"""

from __future__ import absolute_import, print_function, unicode_literals

from collections import Sequence
from .header import Header
from .footer import Footer


class Sections(Sequence):
    """
    Sequence of |Section| objects corresponding to the sections in the
    document. Supports ``len()``, iteration, and indexed access.
    """
    def __init__(self, document_elm, part):
        super(Sections, self).__init__()
        self._document_elm = document_elm
        self._part = part

    def __getitem__(self, key):
        if isinstance(key, slice):
            sectPr_lst = self._document_elm.sectPr_lst[key]
            return [Section(sectPr, self._part) for sectPr in sectPr_lst]
        sectPr = self._document_elm.sectPr_lst[key]
        return Section(sectPr, self._part)

    def __iter__(self):
        for sectPr in self._document_elm.sectPr_lst:
            yield Section(sectPr, self._part)

    def __len__(self):
        return len(self._document_elm.sectPr_lst)


class Section(object):
    """
    Document section, providing access to section and page setup settings.
    """

    H_F_TYPE_DEFAULT = 'default'
    H_F_TYPE_FIRST = 'first'
    H_F_TYPE_EVEN = 'even'

    def __init__(self, sectPr, part):
        super(Section, self).__init__()
        self._sectPr = sectPr
        self._part = part

        self._default_header = None
        self.__default_header_is_linked = True
        self._first_page_header = None
        self.__first_page_header_is_linked = True
        self._even_odd_header = None
        self.__even_odd_header_is_linked = True

        self._default_footer = None
        self._first_page_footer = None
        self._even_odd_footer = None

        self._init_headers_footers()

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

    @property
    def different_first_page_header_footer(self):
        return self._sectPr.titlePg_val

    @different_first_page_header_footer.setter
    def different_first_page_header_footer(self, value):
        self._sectPr.titlePg_val = value

    @property
    def header(self):
        return self._default_header if self._default_header is not None else Header(None, None, self._default_header_is_linked)

    @property
    def _default_header_is_linked(self):
        return self.__default_header_is_linked

    @_default_header_is_linked.setter
    def _default_header_is_linked(self, value):
        # create new rel + add ref to section
        if self.__default_header_is_linked is True and value is False:
            pass
        #
        elif self.__default_header_is_linked is False and value is True:
            pass
        self.__default_header_is_linked = value

    @property
    def first_page_header(self):
        return self._first_page_header if self._first_page_header is not None else Header(None, None, self._first_page_header_is_linked)

    @property
    def _first_page_header_is_linked(self):
        return self.__first_page_header_is_linked

    @_first_page_header_is_linked.setter
    def _first_page_header_is_linked(self, value):
        self.__first_page_header_is_linked = value

    @property
    def even_odd_header(self):
        return self._even_odd_header if self._even_odd_header is not None else Header(None, None, self._even_odd_header_is_linked)

    @property
    def _even_odd_header_is_linked(self):
        return self.__even_odd_header_is_linked

    @_even_odd_header_is_linked.setter
    def _even_odd_header_is_linked(self, value):
        self.__even_odd_header_is_linked = value

    @property
    def footer(self):
        return self._default_footer

    @property
    def first_page_footer(self):
        return self._first_page_footer

    @property
    def even_odd_footer(self):
        return self._even_odd_footer

    def _init_headers_footers(self):

        for header_reference in self._sectPr.header_reference_lst:
            if header_reference.type == Section.H_F_TYPE_DEFAULT:
                self._default_header = self._part.get_part_by_rid(header_reference.rId).header
                self.__default_header_is_linked = False
                self._default_header.is_linked_to_previous = self._default_header_is_linked

            elif header_reference.type == Section.H_F_TYPE_FIRST:
                self._first_page_header = self._part.get_part_by_rid(header_reference.rId).header
                self.__first_page_header_is_linked = False
                self._first_page_header.is_linked_to_previous = self._first_page_header_is_linked

            elif header_reference.type == Section.H_F_TYPE_EVEN:
                self._even_odd_header = self._part.get_part_by_rid(header_reference.rId).header
                self.__even_odd_header_is_linked = False
                self._even_odd_header.is_linked_to_previous = self._even_odd_header_is_linked

        for footer_reference in self._sectPr.footer_reference_lst:
            if footer_reference.type == Section.H_F_TYPE_DEFAULT:
                self._default_footer = self._part.get_part_by_rid(footer_reference.rId).footer
                self._default_footer.is_linked_to_previous = False

            elif footer_reference.type == Section.H_F_TYPE_FIRST:
                self._first_page_footer = self._part.get_part_by_rid(footer_reference.rId).footer
                self._first_page_footer.is_linked_to_previous = False

            elif footer_reference.type == Section.H_F_TYPE_EVEN:
                self._even_odd_footer = self._part.get_part_by_rid(footer_reference.rId).footer
                self._even_odd_footer.is_linked_to_previous = False
