# encoding: utf-8

"""
Section-related custom element classes.
"""

from ..enum.section import WD_SECTION_START
from .xmlchemy import BaseOxmlElement, OptionalAttribute, ZeroOrOne


class CT_SectPr(BaseOxmlElement):
    """
    ``<w:sectPr>`` element, the container element for section properties.
    """
    type = ZeroOrOne('w:type')

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


class CT_SectType(BaseOxmlElement):
    """
    ``<w:sectType>`` element, defining the section start type.
    """
    val = OptionalAttribute('w:val', WD_SECTION_START)
