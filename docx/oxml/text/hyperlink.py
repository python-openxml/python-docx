# encoding: utf-8

"""
Custom element classes related to hyperlinks (CT_Hyperlink).
"""

from ..ns import qn
from ..simpletypes import ST_String, ST_RelationshipId
from ..xmlchemy import (
    BaseOxmlElement, OptionalAttribute, ZeroOrMore
)


class CT_Hyperlink(BaseOxmlElement):
    """
    ``<w:hyperlink>`` element, containing the properties and text for a external hyperlink.
    """
    r = ZeroOrMore('w:r')
    rid = OptionalAttribute('r:id', ST_RelationshipId)
    anchor = OptionalAttribute('w:anchor', ST_String)

    @property
    def relationship(self):
        """
        String contained in ``r:id`` attribute of <w:hyperlink>. It should
        point to a URL in the document's relationships.
        """
        val = self.get(qn('r:id'))
        return val

    @relationship.setter
    def relationship(self, rId):
        self.set(qn('r:id'), rId)

    def clear_content(self):
        """
        Remove all child elements.
        """
        for child in self[:]:
            self.remove(child)
