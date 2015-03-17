# encoding: utf-8

"""
Custom element classes related to hyperlinks (CT_Hyperlink).
"""

from ..ns import qn
from ..simpletypes import ST_RelationshipId
from ..xmlchemy import (
    BaseOxmlElement, RequiredAttribute, ZeroOrMore
)


class CT_Hyperlink(BaseOxmlElement):
    """
    ``<w:hyperlink>`` element, containing the properties and text for a hyperlink.

    The ``<w:hyperlink>`` contains a ``<w:r>`` element which holds all the
    visible content. The ``<w:hyperlink>`` has an attribute ``r:id`` which
    holds an ID relating a URL in the document's relationships.
    """
    r = ZeroOrMore('w:r')
    rid = RequiredAttribute('r:id', ST_RelationshipId)

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
        self.set(qn('w:history'), '1')

    def clear_content(self):
        """
        Remove all child r elements
        """
        r_to_rm = []
        for child in self[:]:
            if child.tag == qn('w:r'):
                r_to_rm.append(child)
        for r in r_to_rm:
            self.remove(r)
