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
            return [Section(sectPr, *self._assign_headers_footers(sectPr)) for sectPr in sectPr_lst]
        sectPr = self._document_elm.sectPr_lst[key]
        return Section(sectPr, *self._assign_headers_footers(sectPr))

    def __iter__(self):
        for sectPr in self._document_elm.sectPr_lst:
            yield Section(sectPr, *self._assign_headers_footers(sectPr))

    def __len__(self):
        return len(self._document_elm.sectPr_lst)

    def _assign_headers_footers(self, sectPr):
        header_types = Header_Types()
        footer_types = Footer_Types()

        for header_reference in sectPr.header_reference_lst:
            if header_reference.type == 'default':
                header_types.header = self._part.get_part_by_rid(header_reference.rId)
            elif header_reference.type == 'first':
                header_types.first_page_header = self._part.get_part_by_rid(header_reference.rId)
            elif header_reference.type == 'even':
                header_types.even_odd_header = self._part.get_part_by_rid(header_reference.rId)

        for footer_reference in sectPr.footer_reference_lst:
            if footer_reference.type == 'default':
                footer_types.footer = self._part.get_part_by_rid(footer_reference.rId)
            elif footer_reference.type == 'first':
                footer_types.first_page_footer = self._part.get_part_by_rid(footer_reference.rId)
            elif footer_reference.type == 'even':
                footer_types.even_odd_footer = self._part.get_part_by_rid(footer_reference.rId)

        return header_types, footer_types


class Section(object):
    """
    Document section, providing access to section and page setup settings.
    """
    def __init__(self, sectPr, header_types, footer_types):
        super(Section, self).__init__()
        self._sectPr = sectPr
        self._header_types = header_types
        self._footer_types = footer_types

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
    def footer(self):
        """
        |Length| object representing the distance from the bottom edge of the
        page to the bottom edge of the footer. |None| if no setting is present
        in the XML.
        """
        return self._sectPr.footer

    @footer.setter
    def footer(self, value):
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
    def header(self):
        """
        |Length| object representing the distance from the top edge of the
        page to the top edge of the header. |None| if no setting is present
        in the XML.
        """
        return self._sectPr.header

    @header.setter
    def header(self, value):
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
    def _different_first_page_header_footer(self):
        return self._sectPr.titlePg_val

    @_different_first_page_header_footer.setter
    def _different_first_page_header_footer(self, value):
        self._sectPr.titlePg_val = value

    @property
    def default_header(self):
        return self._header_types.default_header.header if self._header_types.default_header is not None else Header(None, None, True)

    @property
    def first_page_header(self):
        return self._header_types.first_page_header.header if self._header_types.first_page_header is not None else Header(None, None, True)

    @property
    def even_odd_header(self):
        return self._header_types.even_odd_header.header if self._header_types.even_odd_header is not None else Header(None, None, True)

    @property
    def default_footer(self):
        return self._footer_types.default_footer.footer if self._footer_types.default_footer is not None else Footer(None, None, True)

    @property
    def first_page_footer(self):
        return self._footer_types.first_page_footer.footer if self._footer_types.first_page_footer is not None else Footer(
            None, None, True)

    @property
    def even_odd_footer(self):
        return self._footer_types.even_odd_footer.footer if self._footer_types.even_odd_footer is not None else Footer(
            None, None, True)


class Header_Types(object):

    def __init__(self, header=None, first_page_header=None, even_odd_header=None):
        super(Header_Types, self).__init__()
        self.default_header = header
        self.first_page_header = first_page_header
        self.even_odd_header = even_odd_header


class Footer_Types(object):

    def __init__(self, footer=None, first_page_footer=None, even_odd_footer=None):
        super(Footer_Types, self).__init__()
        self.default_footer = footer
        self.first_page_footer = first_page_footer
        self.even_odd_footer = even_odd_footer