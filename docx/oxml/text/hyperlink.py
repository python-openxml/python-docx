
"""
Custom element classes related to hyperlinks (CT_Hyperlink).
"""

from ..ns import qn
from ..xmlchemy import BaseOxmlElement, OxmlElement, ZeroOrMore 

class CT_Hyperlink(BaseOxmlElement):
    """
    ``<w:hyperlink>`` element, containing the properties and text for a hyperlink.
    """
    r = ZeroOrMore('w:r')

    def clear_content(self):
        """
        Remove all child elements
        """
        for child in self[:]:
            self.remove(child)





