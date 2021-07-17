encoding: utf-8

"""Section-related custom element classes"""

from __future__ import absolute_import, division, print_function, unicode_literals

from copy import deepcopy

  <<<<<<< feature/header
from ..enum.header import WD_HEADER_FOOTER
from ..enum.section import WD_ORIENTATION, WD_SECTION_START
from .simpletypes import (
    ST_RelationshipId, ST_SignedTwipsMeasure, ST_TwipsMeasure
)
from .xmlchemy import (
    BaseOxmlElement, OptionalAttribute, RequiredAttribute, ZeroOrMore,
    ZeroOrOne
)


class CT_HdrFtrRef(BaseOxmlElement):
    """
    `w:headerReference` and `w:footerReference` elements, specifying the
    various headers and footers for a section.
    """
    rId == RequiredAttribute('r:id', ST_RelationshipId)
  =======
from docx.enum.section import WD_HEADER_FOOTER, WD_ORIENTATION, WD_SECTION_START
from docx.oxml.simpletypes import ST_SignedTwipsMeasure, ST_TwipsMeasure, XsdString
from docx.oxml.xmlchemy import (
    BaseOxmlElement,
    OptionalAttribute,
    RequiredAttribute,
    ZeroOrMore,
    ZeroOrOne,
)


class CT_HdrFtr(BaseOxmlElement):
    """`w:hdr` and `w:ftr`, the root element for header and footer part respectively"""

    p = ZeroOrMore("w:p", successors=())
    tbl = ZeroOrMore("w:tbl", successors=())
    bookmarkStart = ZeroOrMore("w:bookmarkStart", successors=())
    bookmarkEnd = ZeroOrMore("w:bookmarkEnd", successors=())

    def add_bookmarkEnd(self, bookmark_id):
        """Return `w:bookmarkEnd` element added at end of this header or footer.

        The newly added `w:bookmarkEnd` element is linked to it's `w:bookmarkStart`
        counterpart by `bookmark_id`. It is the caller's responsibility to determine
        `bookmark_id` matches that of the intended `bookmarkStart` element.
        """
        bookmarkEnd = self._add_bookmarkEnd()
        bookmarkEnd.id = bookmark_id
        return bookmarkEnd

    def add_bookmarkStart(self, name, bookmark_id):
        """Return `w:bookmarkStart` element added at the end of this header or footer.

        The newly added `w:bookmarkStart` element is identified by both `name` and
        `bookmark_id`. It is the caller's responsibility to determine that both `name`
        and `bookmark_id` are unique, document-wide.
        """
        bookmarkStart = self._add_bookmarkStart()
        bookmarkStart.name = name
        bookmarkStart.id = bookmark_id
        return bookmarkStart


class CT_HdrFtrRef(BaseOxmlElement):
    """`w:headerReference` and `w:footerReference` elements"""

  <<<<<<< feature/bookmarks
    type_ = RequiredAttribute("w:type", WD_HEADER_FOOTER)
    rId = RequiredAttribute("r:id", XsdString)
  =======
    type_ = RequiredAttribute('w:type', WD_HEADER_FOOTER)
    rId = RequiredAttribute('r:id', XsdString)
  >>>>>>> master
  >>>>>>> develop


class CT_PageMar(BaseOxmlElement):
    """
    ``<w:pgMar>`` element, defining page margins.
    """

    top = OptionalAttribute("w:top", ST_SignedTwipsMeasure)
    right = OptionalAttribute("w:right", ST_TwipsMeasure)
    bottom = OptionalAttribute("w:bottom", ST_SignedTwipsMeasure)
    left = OptionalAttribute("w:left", ST_TwipsMeasure)
    header = OptionalAttribute("w:header", ST_TwipsMeasure)
    footer = OptionalAttribute("w:footer", ST_TwipsMeasure)
    gutter = OptionalAttribute("w:gutter", ST_TwipsMeasure)


class CT_PageSz(BaseOxmlElement):
    """
    ``<w:pgSz>`` element, defining page dimensions and orientation.
    """

    w = OptionalAttribute("w:w", ST_TwipsMeasure)
    h = OptionalAttribute("w:h", ST_TwipsMeasure)
    orient = OptionalAttribute(
        "w:orient", WD_ORIENTATION, default=WD_ORIENTATION.PORTRAIT
    )


class CT_SectPr(BaseOxmlElement):
  <<<<<<< feature/header
    """
    ``<w:sectPr>`` element, the container element for section properties.
    """
    _tag_seq = (
        'w:headerReference', 'w:footerReference', 'w:footnotePr',
        'w:endnotePr', 'w:type', 'w:pgSz', 'w:pgMar', 'w:paperSrc',
        'w:pgBorders', 'w:lnNumType', 'w:pgNumType', 'w:cols', 'w:formProt',
        'w:vAlign', 'w:noEndnote', 'w:titlePg', 'w:textDirection', 'w:bidi',
        'w:rtlGutter', 'w:docGrid', 'w:printerSettings', 'w:sectPrChange',
    )
    headerReference = ZeroOrMore('w:headerReference', successors=_tag_seq[1:])
    type = ZeroOrOne('w:type', successors=_tag_seq[5:])
    pgSz = ZeroOrOne('w:pgSz', successors=_tag_seq[6:])
    pgMar = ZeroOrOne('w:pgMar', successors=_tag_seq[7:])
    del _tag_seq
  =======
    """`w:sectPr` element, the container element for section properties"""

    _tag_seq = (
        "w:footnotePr",
        "w:endnotePr",
        "w:type",
        "w:pgSz",
        "w:pgMar",
        "w:paperSrc",
        "w:pgBorders",
        "w:lnNumType",
        "w:pgNumType",
        "w:cols",
        "w:formProt",
        "w:vAlign",
        "w:noEndnote",
        "w:titlePg",
        "w:textDirection",
        "w:bidi",
        "w:rtlGutter",
        "w:docGrid",
        "w:printerSettings",
        "w:sectPrChange",
    )
    headerReference = ZeroOrMore("w:headerReference", successors=_tag_seq)
    footerReference = ZeroOrMore("w:footerReference", successors=_tag_seq)
    type = ZeroOrOne("w:type", successors=_tag_seq[3:])
    pgSz = ZeroOrOne("w:pgSz", successors=_tag_seq[4:])
    pgMar = ZeroOrOne("w:pgMar", successors=_tag_seq[5:])
    titlePg = ZeroOrOne("w:titlePg", successors=_tag_seq[14:])
    del _tag_seq

    def add_footerReference(self, type_, rId):
        """Return newly added CT_HdrFtrRef element of *type_* with *rId*.

        The element tag is `w:footerReference`.
        """
        footerReference = self._add_footerReference()
        footerReference.type_ = type_
        footerReference.rId = rId
        return footerReference

    def add_headerReference(self, type_, rId):
        """Return newly added CT_HdrFtrRef element of *type_* with *rId*.

        The element tag is `w:headerReference`.
        """
        headerReference = self._add_headerReference()
        headerReference.type_ = type_
        headerReference.rId = rId
        return headerReference
  >>>>>>> master

    @property
    def bottom_margin(self):
        """
        The value of the ``w:bottom`` attribute in the ``<w:pgMar>`` child
        element, as a |Length| object, or |None| if either the element or the
        attribute is not present.
        """
        pgMar = self.pgMar
        if pgMar is None:
            return None
        return pgMar.bottom

    @bottom_margin.setter
    def bottom_margin(self, value):
        pgMar = self.get_or_add_pgMar()
        pgMar.bottom = value

    def clone(self):
        """
        Return an exact duplicate of this ``<w:sectPr>`` element tree
        suitable for use in adding a section break. All rsid* attributes are
        removed from the root ``<w:sectPr>`` element.
        """
        clone_sectPr = deepcopy(self)
        clone_sectPr.attrib.clear()
        return clone_sectPr

    @property
    def footer(self):
        """
        The value of the ``w:footer`` attribute in the ``<w:pgMar>`` child
        element, as a |Length| object, or |None| if either the element or the
        attribute is not present.
        """
        pgMar = self.pgMar
        if pgMar is None:
            return None
        return pgMar.footer

    @footer.setter
    def footer(self, value):
        pgMar = self.get_or_add_pgMar()
        pgMar.footer = value

  <<<<<<< feature/header
    def get_headerReference_of_type(self, type_member):
        """
        Return the `w:headerReference` child having type attribute value
        associated with *type_member*, or |None| if not present.
        """
        type_str = WD_HEADER_FOOTER.to_xml(type_member)
        matches = self.xpath('w:headerReference[@w:type="%s"]' % type_str)
        if matches:
            return matches[0]
        return None
  =======
    def get_footerReference(self, type_):
        """Return footerReference element of *type_* or None if not present."""
        path = "./w:footerReference[@w:type='%s']" % WD_HEADER_FOOTER.to_xml(type_)
        footerReferences = self.xpath(path)
        if not footerReferences:
            return None
        return footerReferences[0]

    def get_headerReference(self, type_):
        """Return headerReference element of *type_* or None if not present."""
        matching_headerReferences = self.xpath(
            "./w:headerReference[@w:type='%s']" % WD_HEADER_FOOTER.to_xml(type_)
        )
        if len(matching_headerReferences) == 0:
            return None
        return matching_headerReferences[0]
  >>>>>>> master

    @property
    def gutter(self):
        """
        The value of the ``w:gutter`` attribute in the ``<w:pgMar>`` child
        element, as a |Length| object, or |None| if either the element or the
        attribute is not present.
        """
        pgMar = self.pgMar
        if pgMar is None:
            return None
        return pgMar.gutter

    @gutter.setter
    def gutter(self, value):
        pgMar = self.get_or_add_pgMar()
        pgMar.gutter = value

    @property
    def header(self):
        """
        The value of the ``w:header`` attribute in the ``<w:pgMar>`` child
        element, as a |Length| object, or |None| if either the element or the
        attribute is not present.
        """
        pgMar = self.pgMar
        if pgMar is None:
            return None
        return pgMar.header

    @header.setter
    def header(self, value):
        pgMar = self.get_or_add_pgMar()
        pgMar.header = value

    @property
    def left_margin(self):
        """
        The value of the ``w:left`` attribute in the ``<w:pgMar>`` child
        element, as a |Length| object, or |None| if either the element or the
        attribute is not present.
        """
        pgMar = self.pgMar
        if pgMar is None:
            return None
        return pgMar.left

    @left_margin.setter
    def left_margin(self, value):
        pgMar = self.get_or_add_pgMar()
        pgMar.left = value

    @property
    def orientation(self):
        """
        The member of the ``WD_ORIENTATION`` enumeration corresponding to the
        value of the ``orient`` attribute of the ``<w:pgSz>`` child element,
        or ``WD_ORIENTATION.PORTRAIT`` if not present.
        """
        pgSz = self.pgSz
        if pgSz is None:
            return WD_ORIENTATION.PORTRAIT
        return pgSz.orient

    @orientation.setter
    def orientation(self, value):
        pgSz = self.get_or_add_pgSz()
        pgSz.orient = value

    @property
    def page_height(self):
        """
        Value in EMU of the ``h`` attribute of the ``<w:pgSz>`` child
        element, or |None| if not present.
        """
        pgSz = self.pgSz
        if pgSz is None:
            return None
        return pgSz.h

    @page_height.setter
    def page_height(self, value):
        pgSz = self.get_or_add_pgSz()
        pgSz.h = value

    @property
    def page_width(self):
        """
        Value in EMU of the ``w`` attribute of the ``<w:pgSz>`` child
        element, or |None| if not present.
        """
        pgSz = self.pgSz
        if pgSz is None:
            return None
        return pgSz.w

    @page_width.setter
    def page_width(self, value):
        pgSz = self.get_or_add_pgSz()
        pgSz.w = value

    @property
    def preceding_sectPr(self):
        """sectPr immediately preceding this one or None if this is the first."""
        # ---[1] predicate returns list of zero or one value---
        preceding_sectPrs = self.xpath("./preceding::w:sectPr[1]")
        return preceding_sectPrs[0] if len(preceding_sectPrs) > 0 else None

    def remove_footerReference(self, type_):
        """Return rId of w:footerReference child of *type_* after removing it."""
        footerReference = self.get_footerReference(type_)
        rId = footerReference.rId
        self.remove(footerReference)
        return rId

    def remove_headerReference(self, type_):
        """Return rId of w:headerReference child of *type_* after removing it."""
        headerReference = self.get_headerReference(type_)
        rId = headerReference.rId
        self.remove(headerReference)
        return rId

    @property
    def right_margin(self):
        """
        The value of the ``w:right`` attribute in the ``<w:pgMar>`` child
        element, as a |Length| object, or |None| if either the element or the
        attribute is not present.
        """
        pgMar = self.pgMar
        if pgMar is None:
            return None
        return pgMar.right

    @right_margin.setter
    def right_margin(self, value):
        pgMar = self.get_or_add_pgMar()
        pgMar.right = value

    @property
    def start_type(self):
        """
        The member of the ``WD_SECTION_START`` enumeration corresponding to
        the value of the ``val`` attribute of the ``<w:type>`` child element,
        or ``WD_SECTION_START.NEW_PAGE`` if not present.
        """
        type = self.type
        if type is None or type.val is None:
            return WD_SECTION_START.NEW_PAGE
        return type.val

    @start_type.setter
    def start_type(self, value):
        if value is None or value is WD_SECTION_START.NEW_PAGE:
            self._remove_type()
            return
        type = self.get_or_add_type()
        type.val = value

    @property
    def titlePg_val(self):
        """Value of `w:titlePg/@val` or |None| if not present"""
        titlePg = self.titlePg
        if titlePg is None:
            return False
        return titlePg.val

    @titlePg_val.setter
    def titlePg_val(self, value):
        if value in [None, False]:
            self._remove_titlePg()
        else:
            self.get_or_add_titlePg().val = value

    @property
    def top_margin(self):
        """
        The value of the ``w:top`` attribute in the ``<w:pgMar>`` child
        element, as a |Length| object, or |None| if either the element or the
        attribute is not present.
        """
        pgMar = self.pgMar
        if pgMar is None:
            return None
        return pgMar.top

    @top_margin.setter
    def top_margin(self, value):
        pgMar = self.get_or_add_pgMar()
        pgMar.top = value


class CT_SectType(BaseOxmlElement):
    """
    ``<w:sectType>`` element, defining the section start type.
    """

    val = OptionalAttribute("w:val", WD_SECTION_START)
