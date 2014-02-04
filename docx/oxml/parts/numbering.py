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


class CT_NumPr(OxmlBaseElement):
    """
    A ``<w:numPr>`` element, a container for numbering properties applied to
    a paragraph.
    """
    def get_or_add_ilvl(self):
        """
        Return the ilvl child element, newly added if not present.
        """
        ilvl = self.ilvl
        if ilvl is None:
            ilvl = self._add_ilvl()
        return ilvl

    def get_or_add_numId(self):
        """
        Return the numId child element, newly added if not present.
        """
        numId = self.numId
        if numId is None:
            numId = self._add_numId()
        return numId

    @property
    def ilvl(self):
        return self.find(qn('w:ilvl'))

    @ilvl.setter
    def ilvl(self, val):
        """
        Get or add a <w:ilvl> child and set its ``w:val`` attribute to *val*.
        """
        ilvl = self.get_or_add_ilvl()
        ilvl.val = val

    @classmethod
    def new(cls):
        """
        Return a new ``<w:numPr>`` element
        """
        return OxmlElement('w:numPr')

    @property
    def numId(self):
        return self.find(qn('w:numId'))

    @numId.setter
    def numId(self, val):
        """
        Get or add a <w:numId> child and set its ``w:val`` attribute to *val*.
        """
        numId = self.get_or_add_numId()
        numId.val = val

    def _add_ilvl(self, val=0):
        """
        Return a newly added CT_DecimalNumber element having tagname 'w:ilvl'
        and ``val`` attribute set to *val*.
        """
        ilvl = CT_DecimalNumber.new('w:ilvl', val)
        return self._insert_ilvl(ilvl)

    def _add_numId(self, val=0):
        """
        Return a newly added CT_DecimalNumber element having tagname
        'w:numId' and ``val`` attribute set to *val*.
        """
        numId = CT_DecimalNumber.new('w:numId', val)
        return self._insert_numId(numId)

    def _insert_ilvl(self, ilvl):
        return self.insert_element_before(
            ilvl, 'w:numId', 'w:numberingChange', 'w:ins'
        )

    def _insert_numId(self, numId):
        return self.insert_element_before(
            numId, 'w:numberingChange', 'w:ins'
        )


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
        return self._insert_num(num)

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

    def _insert_num(self, num):
        return self.insert_element_before(num, 'w:numIdMacAtCleanup')

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
