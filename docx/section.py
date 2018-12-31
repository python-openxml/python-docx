# encoding: utf-8

"""The |Section| object and related proxy classes"""

from __future__ import absolute_import, division, print_function, unicode_literals

from collections import Sequence

from docx.blkcntnr import BlockItemContainer
from docx.enum.section import WD_HEADER_FOOTER
from docx.shared import lazyproperty


class Sections(Sequence):
    """Sequence of |Section| objects corresponding to the sections in the document.

    Supports ``len()``, iteration, and indexed access.
    """

    def __init__(self, document_elm, document_part):
        super(Sections, self).__init__()
        self._document_elm = document_elm
        self._document_part = document_part

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [
                Section(sectPr, self._document_part)
                for sectPr in self._document_elm.sectPr_lst[key]
            ]
        return Section(self._document_elm.sectPr_lst[key], self._document_part)

    def __iter__(self):
        for sectPr in self._document_elm.sectPr_lst:
            yield Section(sectPr, self._document_part)

    def __len__(self):
        return len(self._document_elm.sectPr_lst)


class Section(object):
    """Document section, providing access to section and page setup settings.

    Also provides access to headers and footers.
    """

    def __init__(self, sectPr, document_part):
        super(Section, self).__init__()
        self._sectPr = sectPr
        self._document_part = document_part

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

    @lazyproperty
    def footer(self):
        """|_Footer| object representing default page footer for this section.

        The default footer is used for odd-numbered pages when separate odd/even footers
        are enabled. It is used for both odd and even-numbered pages otherwise.
        """
        return _Footer(self._sectPr, self._document_part)

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

    @lazyproperty
    def header(self):
        """|_Header| object representing default page header for this section.

        The default header is used for odd-numbered pages when separate odd/even headers
        are enabled. It is used for both odd and even-numbered pages otherwise.
        """
        return _Header(self._sectPr, self._document_part)

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


class _Footer(BlockItemContainer):
    """Page footer."""

    def __init__(self, sectPr, document_part):
        self._sectPr = sectPr
        self._document_part = document_part


class _Header(BlockItemContainer):
    """Page header."""

    def __init__(self, sectPr, document_part):
        self._sectPr = sectPr
        self._document_part = document_part

    @property
    def is_linked_to_previous(self):
        """True if this header uses the header definition of the preceding section.

        False if this header has an explicit definition.

        Assigning ``True`` to this property removes any header definition for this
        section, causing it to "inherit" the header definition of the prior section.
        Assigning ``False`` causes a new, empty header definition to be added for this
        section, but only if no existing definition is present.
        """
        # ---absence of a header (definition) part indicates "linked" behavior---
        return not self._has_header_part

    @is_linked_to_previous.setter
    def is_linked_to_previous(self, value):
        new_state = bool(value)
        # ---do nothing when value is not being changed---
        if new_state == self.is_linked_to_previous:
            return
        if new_state is True:
            self._drop_header_part()
        else:
            self._add_header_part()

    def _add_header_part(self):
        """Return newly-added header part."""
        raise NotImplementedError

    def _drop_header_part(self):
        """Remove header definition associated with this section."""
        raise NotImplementedError

    @property
    def _has_header_part(self):
        """True if a header is explicitly defined for this section."""
        headerReference = self._sectPr.get_headerReference(WD_HEADER_FOOTER.PRIMARY)
        return False if headerReference is None else True
