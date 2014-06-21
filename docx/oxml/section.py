# encoding: utf-8

"""
Section-related custom element classes.
"""

from ..enum.section import WD_SECTION_START
from .simpletypes import ST_TwipsMeasure
from .xmlchemy import BaseOxmlElement, OptionalAttribute, ZeroOrOne


class CT_PageSz(BaseOxmlElement):
    """
    ``<w:pgSz>`` element, defining page dimensions and orientation.
    """
    w = OptionalAttribute('w:w', ST_TwipsMeasure)
    h = OptionalAttribute('w:h', ST_TwipsMeasure)


class CT_SectPr(BaseOxmlElement):
    """
    ``<w:sectPr>`` element, the container element for section properties.
    """
    __child_sequence__ = (
        'w:footnotePr', 'w:endnotePr', 'w:type', 'w:pgSz', 'w:pgMar',
        'w:paperSrc', 'w:pgBorders', 'w:lnNumType', 'w:pgNumType', 'w:cols',
        'w:formProt', 'w:vAlign', 'w:noEndnote', 'w:titlePg',
        'w:textDirection', 'w:bidi', 'w:rtlGutter', 'w:docGrid',
        'w:printerSettings', 'w:sectPrChange',
    )
    type = ZeroOrOne('w:type', successors=(
        __child_sequence__[__child_sequence__.index('w:type')+1:]
    ))
    pgSz = ZeroOrOne('w:pgSz', successors=(
        __child_sequence__[__child_sequence__.index('w:pgSz')+1:]
    ))

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


class CT_SectType(BaseOxmlElement):
    """
    ``<w:sectType>`` element, defining the section start type.
    """
    val = OptionalAttribute('w:val', WD_SECTION_START)
