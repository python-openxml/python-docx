# encoding: utf-8

"""
Custom element classes related to the styles part
"""

from .xmlchemy import (
    BaseOxmlElement, ZeroOrOne
)


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
    def evenAndOddHeaders_val(self):
        """
        The value of `evenAndOddHeaders/@val` or |None| if not present.
        """
        evenAndOddHeaders = self.evenAndOddHeaders
        if evenAndOddHeaders is None:
            return False
        return evenAndOddHeaders.val

    @evenAndOddHeaders_val.setter
    def evenAndOddHeaders_val(self, value):
        if value in [None, False]:
            self._remove_evenAndOddHeaders()
        else:
            self.get_or_add_evenAndOddHeaders().val = value
