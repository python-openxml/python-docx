# encoding: utf-8

"""
Custom element classes related to the numbering part
"""

from docx.oxml.shared import (
    CT_DecimalNumber, nsmap, OxmlBaseElement, OxmlElement, qn
)


class CT_Num(OxmlBaseElement):
    """
    ``<w:num>`` element, which represents a concrete list definition
    instance, having a required child <w:abstractNumId> that references an
    abstract numbering definition that defines most of the formatting details.
    """
    @property
    def abstractNumId(self):
        return self.find(qn('w:abstractNumId'))

    def add_lvlOverride(self, ilvl):
        """
        Return a newly added CT_NumLvl (<w:lvlOverride>) element having its
        ``ilvl`` attribute set to *ilvl*.
        """
        lvlOverride = CT_NumLvl.new(ilvl)
        self.append(lvlOverride)
        return lvlOverride

    @classmethod
    def new(cls, num_id, abstractNum_id):
        """
        Return a new ``<w:num>`` element having numId of *num_id* and having
        a ``<w:abstractNumId>`` child with val attribute set to
        *abstractNum_id*.
        """
        abstractNumId = CT_DecimalNumber.new(
            'w:abstractNumId', abstractNum_id
        )
        num = OxmlElement('w:num', {qn('w:numId'): str(num_id)})
        num.append(abstractNumId)
        return num

    @property
    def numId(self):
        numId_str = self.get(qn('w:numId'))
        return int(numId_str)


class CT_NumLvl(OxmlBaseElement):
    """
    ``<w:lvlOverride>`` element, which identifies a level in a list
    definition to override with settings it contains.
    """
    def add_startOverride(self, val):
        """
        Return a newly added CT_DecimalNumber element having tagname
        ``w:startOverride`` and ``val`` attribute set to *val*.
        """
        startOverride = CT_DecimalNumber.new('w:startOverride', val)
        self.insert(0, startOverride)
        return startOverride

    @classmethod
    def new(cls, ilvl):
        """
        Return a new ``<w:lvlOverride>`` element having its ``ilvl``
        attribute set to *ilvl*.
        """
        return OxmlElement('w:lvlOverride', {qn('w:ilvl'): str(ilvl)})


class CT_Numbering(OxmlBaseElement):
    """
    ``<w:numbering>`` element, the root element of a numbering part, i.e.
    numbering.xml
    """
    def add_num(self, abstractNum_id):
        """
        Return a newly added CT_Num (<w:num>) element that references
        the abstract numbering definition having id *abstractNum_id*.
        """
        next_num_id = self._next_numId
        num = CT_Num.new(next_num_id, abstractNum_id)
        # insert in proper sequence among children ---------
        successor = self.first_child_found_in('w:numIdMacAtCleanup')
        if successor is not None:
            successor.addprevious(num)
        else:
            self.append(num)
        return num

    @property
    def num_lst(self):
        """
        List of <w:num> child elements.
        """
        return self.findall(qn('w:num'))

    def num_having_numId(self, numId):
        """
        Return the ``<w:num>`` child element having ``numId`` attribute
        matching *numId*.
        """
        xpath = './w:num[@w:numId="%d"]' % numId
        try:
            return self.xpath(xpath, namespaces=nsmap)[0]
        except IndexError:
            raise KeyError('no <w:num> element with numId %d' % numId)

    @property
    def _next_numId(self):
        """
        The first ``numId`` unused by a ``<w:num>`` element, starting at
        1 and filling any gaps in numbering between existing ``<w:num>``
        elements.
        """
        numId_strs = self.xpath('./w:num/@w:numId', namespaces=nsmap)
        num_ids = [int(numId_str) for numId_str in numId_strs]
        for num in range(1, len(num_ids)+2):
            if num not in num_ids:
                break
        return num
