# encoding: utf-8

"""
Custom element classes related to the styles part
"""

from ..enum.style import WD_STYLE_TYPE
from .simpletypes import ST_DecimalNumber, ST_OnOff, ST_String
from .xmlchemy import (
    BaseOxmlElement, OneAndOnlyOne, ZeroOrOne
)


class CT_EvenOrOddHeader(BaseOxmlElement):
    """
    ``<w:evenAndOddHeaders>`` element
    """

    def delete(self):
        """
        Remove this `w:evenAndOddHeaders` element from the XML document.
        """
        self.getparent().remove(self)


class CT_Settings(BaseOxmlElement):
    """
    `w:settings` element, defining behavior defaults for settings
    and containing `w:evenAndOddHeaders` child elements that define even and odd headers
    """
    _tag_seq = (
        'w:evenAndOddHeaders'
    )

    evenAndOddHeaders = ZeroOrOne('w:evenAndOddHeaders')

    @property
    def evenOrOddHeaders_val(self):
        """
        The value of `evenAndOddHeaders/@val` or |None| if not present.
        """
        evenAndOddHeaders = self.evenAndOddHeaders
        if evenAndOddHeaders is None:
            return None
        return evenAndOddHeaders.val

    @evenOrOddHeaders_val.setter
    def evenOrOddHeaders_val(self, value):
        if value in [None, False]:
            self._remove_evenAndOddHeaders()
        else:
            self.get_or_add_evenAndOddHeaders().val = value
