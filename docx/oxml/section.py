# encoding: utf-8

"""
Section-related custom element classes.
"""

from __future__ import absolute_import, print_function

from copy import deepcopy

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
    rId = RequiredAttribute('r:id', ST_RelationshipId)


class CT_PageMar(BaseOxmlElement):
    """
    ``<w:pgMar>`` element, defining page margins.
    """
    top = OptionalAttribute('w:top', ST_SignedTwipsMeasure)
    right = OptionalAttribute('w:right', ST_TwipsMeasure)
    bottom = OptionalAttribute('w:bottom', ST_SignedTwipsMeasure)
    left = OptionalAttribute('w:left', ST_TwipsMeasure)
    header = OptionalAttribute('w:header', ST_TwipsMeasure)
    footer = OptionalAttribute('w:footer', ST_TwipsMeasure)
    gutter = OptionalAttribute('w:gutter', ST_TwipsMeasure)


class CT_PageSz(BaseOxmlElement):
    """
    ``<w:pgSz>`` element, defining page dimensions and orientation.
    """
    w = OptionalAttribute('w:w', ST_TwipsMeasure)
    h = OptionalAttribute('w:h', ST_TwipsMeasure)
    orient = OptionalAttribute(
        'w:orient', WD_ORIENTATION, default=WD_ORIENTATION.PORTRAIT
    )


class CT_SectPr(BaseOxmlElement):
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
    val = OptionalAttribute('w:val', WD_SECTION_START)
