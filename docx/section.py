# encoding: utf-8

"""The |Section| object and related proxy classes"""

from __future__ import absolute_import, division, print_function, unicode_literals

from docx.blkcntnr import BlockItemContainer
from docx.compat import Sequence
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

    @property
    def different_first_page_header_footer(self):
        """True if this section displays a distinct first-page header and footer.

        Read/write. The definition of the first-page header and footer are accessed
        using :attr:`.first_page_header` and :attr:`.first_page_footer` respectively.
        """
        return self._sectPr.titlePg_val

    @different_first_page_header_footer.setter
    def different_first_page_header_footer(self, value):
        self._sectPr.titlePg_val = value

    @property
    def even_page_footer(self):
        """|_Footer| object defining footer content for even pages.

        The content of this footer definition is ignored unless the document setting
        :attr:`~.Settings.odd_and_even_pages_header_footer` is set True.
        """
        return _Footer(self._sectPr, self._document_part, WD_HEADER_FOOTER.EVEN_PAGE)

    @property
    def even_page_header(self):
        """|_Header| object defining header content for even pages.

        The content of this header definition is ignored unless the document setting
        :attr:`~.Settings.odd_and_even_pages_header_footer` is set True.
        """
        return _Header(self._sectPr, self._document_part, WD_HEADER_FOOTER.EVEN_PAGE)

    @property
    def first_page_footer(self):
        """|_Footer| object defining footer content for the first page of this section.

        The content of this footer definition is ignored unless the property
        :attr:`.different_first_page_header_footer` is set True.
        """
        return _Footer(self._sectPr, self._document_part, WD_HEADER_FOOTER.FIRST_PAGE)

    @property
    def first_page_header(self):
        """|_Header| object defining header content for the first page of this section.

        The content of this header definition is ignored unless the property
        :attr:`.different_first_page_header_footer` is set True.
        """
        return _Header(self._sectPr, self._document_part, WD_HEADER_FOOTER.FIRST_PAGE)

    @lazyproperty
    def footer(self):
        """|_Footer| object representing default page footer for this section.

        The default footer is used for odd-numbered pages when separate odd/even footers
        are enabled. It is used for both odd and even-numbered pages otherwise.
        """
        return _Footer(self._sectPr, self._document_part, WD_HEADER_FOOTER.PRIMARY)

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
        return _Header(self._sectPr, self._document_part, WD_HEADER_FOOTER.PRIMARY)

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


class _BaseHeaderFooter(BlockItemContainer):
    """Base class for header and footer classes"""

    def __init__(self, sectPr, document_part, header_footer_index):
        self._sectPr = sectPr
        self._document_part = document_part
        self._hdrftr_index = header_footer_index

    @property
    def is_linked_to_previous(self):
        """``True`` if this header/footer uses the definition from the prior section.

        ``False`` if this header/footer has an explicit definition.

        Assigning ``True`` to this property removes the header/footer definition for
        this section, causing it to "inherit" the corresponding definition of the prior
        section. Assigning ``False`` causes a new, empty definition to be added for this
        section, but only if no definition is already present.
        """
        # ---absence of a header/footer part indicates "linked" behavior---
        return not self._has_definition

    @is_linked_to_previous.setter
    def is_linked_to_previous(self, value):
        new_state = bool(value)
        # ---do nothing when value is not being changed---
        if new_state == self.is_linked_to_previous:
            return
        if new_state is True:
            self._drop_definition()
        else:
            self._add_definition()

    @property
    def part(self):
        """The |HeaderPart| or |FooterPart| for this header/footer.

        This overrides `BlockItemContainer.part` and is required to support image
        insertion and perhaps other content like hyperlinks.
        """
        # ---should not appear in documentation;
        # ---not an interface property, even though public
        return self._get_or_add_definition()

    def _add_definition(self):
        """Return newly-added header/footer part."""
        raise NotImplementedError("must be implemented by each subclass")

    @property
    def _definition(self):
        """|HeaderPart| or |FooterPart| object containing header/footer content."""
        raise NotImplementedError("must be implemented by each subclass")

    def _drop_definition(self):
        """Remove header/footer part containing the definition of this header/footer."""
        raise NotImplementedError("must be implemented by each subclass")

    @property
    def _element(self):
        """`w:hdr` or `w:ftr` element, root of header/footer part."""
        return self._get_or_add_definition().element

    def _get_or_add_definition(self):
        """Return HeaderPart or FooterPart object for this section.

        If this header/footer inherits its content, the part for the prior header/footer
        is returned; this process continue recursively until a definition is found. If
        the definition cannot be inherited (because the header/footer belongs to the
        first section), a new definition is added for that first section and then
        returned.
        """
        # ---note this method is called recursively to access inherited definitions---
        # ---case-1: definition is not inherited---
        if self._has_definition:
            return self._definition
        # ---case-2: definition is inherited and belongs to second-or-later section---
        prior_headerfooter = self._prior_headerfooter
        if prior_headerfooter:
            return prior_headerfooter._get_or_add_definition()
        # ---case-3: definition is inherited, but belongs to first section---
        return self._add_definition()

    @property
    def _has_definition(self):
        """True if this header/footer has a related part containing its definition."""
        raise NotImplementedError("must be implemented by each subclass")

    @property
    def _prior_headerfooter(self):
        """|_Header| or |_Footer| proxy on prior sectPr element.

        Returns None if this is first section.
        """
        raise NotImplementedError("must be implemented by each subclass")


class _Footer(_BaseHeaderFooter):
    """Page footer, used for all three types (default, even-page, and first-page).

    Note that, like a document or table cell, a footer must contain a minimum of one
    paragraph and a new or otherwise "empty" footer contains a single empty paragraph.
    This first paragraph can be accessed as `footer.paragraphs[0]` for purposes of
    adding content to it. Using :meth:`add_paragraph()` by itself to add content will
    leave an empty paragraph above the newly added one.
    """

    def _add_definition(self):
        """Return newly-added footer part."""
        footer_part, rId = self._document_part.add_footer_part()
        self._sectPr.add_footerReference(self._hdrftr_index, rId)
        return footer_part

    @property
    def _definition(self):
        """|FooterPart| object containing content of this footer."""
        footerReference = self._sectPr.get_footerReference(self._hdrftr_index)
        return self._document_part.footer_part(footerReference.rId)

    def _drop_definition(self):
        """Remove footer definition (footer part) associated with this section."""
        rId = self._sectPr.remove_footerReference(self._hdrftr_index)
        self._document_part.drop_rel(rId)

    @property
    def _has_definition(self):
        """True if a footer is defined for this section."""
        footerReference = self._sectPr.get_footerReference(self._hdrftr_index)
        return False if footerReference is None else True

    @property
    def _prior_headerfooter(self):
        """|_Footer| proxy on prior sectPr element or None if this is first section."""
        preceding_sectPr = self._sectPr.preceding_sectPr
        return (
            None
            if preceding_sectPr is None
            else _Footer(preceding_sectPr, self._document_part, self._hdrftr_index)
        )


class _Header(_BaseHeaderFooter):
    """Page header, used for all three types (default, even-page, and first-page).

    Note that, like a document or table cell, a header must contain a minimum of one
    paragraph and a new or otherwise "empty" header contains a single empty paragraph.
    This first paragraph can be accessed as `header.paragraphs[0]` for purposes of
    adding content to it. Using :meth:`add_paragraph()` by itself to add content will
    leave an empty paragraph above the newly added one.
    """

    def _add_definition(self):
        """Return newly-added header part."""
        header_part, rId = self._document_part.add_header_part()
        self._sectPr.add_headerReference(self._hdrftr_index, rId)
        return header_part

    @property
    def _definition(self):
        """|HeaderPart| object containing content of this header."""
        headerReference = self._sectPr.get_headerReference(self._hdrftr_index)
        return self._document_part.header_part(headerReference.rId)

    def _drop_definition(self):
        """Remove header definition associated with this section."""
        rId = self._sectPr.remove_headerReference(self._hdrftr_index)
        self._document_part.drop_header_part(rId)

    @property
    def _has_definition(self):
        """True if a header is explicitly defined for this section."""
        headerReference = self._sectPr.get_headerReference(self._hdrftr_index)
        return False if headerReference is None else True

    @property
    def _prior_headerfooter(self):
        """|_Header| proxy on prior sectPr element or None if this is first section."""
        preceding_sectPr = self._sectPr.preceding_sectPr
        return (
            None
            if preceding_sectPr is None
            else _Header(preceding_sectPr, self._document_part, self._hdrftr_index)
        )
