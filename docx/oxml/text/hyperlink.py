# encoding: utf-8

"""
Custom element classes related to hyperlinks (CT_Hyperlink).
"""

from ..ns import qn
from ..xmlchemy import BaseOxmlElement, OptionalAttribute, ZeroOrMore
from ..simpletypes import ST_RelationshipId, ST_String


class CT_Hyperlink(BaseOxmlElement):
    """
    ``<w:hyperlink>`` element, containing properties and text for a hyperlink 
    (internal and external)
    """
    r = ZeroOrMore('w:r')
    anchor = OptionalAttribute('r:anchor', ST_String)
    id = OptionalAttribute('r:id', ST_RelationshipId)

    def clear_content(self):
        """
        Remove all child run (``<w:r>``) elements.
        """
        for child in self[:]:
            if child.tag == qn('w:r'):
                self.remove(child)
