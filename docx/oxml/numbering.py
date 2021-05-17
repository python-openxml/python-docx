# encoding: utf-8

"""
Custom element classes related to the numbering part
"""

from . import OxmlElement
from .shared import CT_DecimalNumber
from .simpletypes import (
        ST_DecimalNumber, ST_LevelSuffix, ST_NumberFormat, ST_String, ST_MultiLevelType,
        ST_TwipsMeasure, ST_SignedTwipsMeasure, ST_OnOff, ST_LongHexNumber
)
from .xmlchemy import (
    BaseOxmlElement, OneAndOnlyOne, RequiredAttribute, ZeroOrMore, ZeroOrOne, 
    OptionalAttribute, Choice
)

class CT_LevelText(BaseOxmlElement):
    """``<w:lvlText>`` element, which specifies
    the formatting of the numeral in a numbered
    list.
    """
    val = OptionalAttribute('w:val', ST_String )
    null = OptionalAttribute('w:null', ST_OnOff )

    @classmethod
    def new(cls, val):
        """
        Return a new ``<w:lvlText>`` element with
        ``val`` attribute set to *val*
        """
        lvlText = OxmlElement('w:lvlText')
        lvlText.val = val
        return lvlText

class CT_LevelSuffix(BaseOxmlElement):
    """
    ``<w:suff>`` element, which specifies the form of the space
    between a list number and the list paragraph
    """
    val = RequiredAttribute('w:val', ST_LevelSuffix )

    @classmethod
    def new(cls, val):
            """
            Return a new ``<w:suff>`` element with ``val``
            attribute set to *val*
            """
            suff = OxmlElement('w:suff')
            suff.val = val
            return suff

class CT_NumFmt(BaseOxmlElement):
    """
    ``<w:numFmt>`` element, which specifies the formatting
    of the numeral in a numbered list
    """
    val = RequiredAttribute('w:val', ST_NumberFormat )
    fmt = OptionalAttribute('w:format', ST_String )

    @classmethod
    def new(cls, val):
        """
        Return a new ``<w:numFmt>`` element with ``val``
        attrribute set to *val*
        """
        numFmt = OxmlElement('w:numFmt')
        numFmt.val = val
        return numFmt

class CT_LvlLegacy(BaseOxmlElement):
    """
    ``<w:legacy>`` element. Implemented here in
    case the module eventually supports parsing
    of documents in the target legacy format.
    """
    legacy = OptionalAttribute('w:legacy', ST_OnOff)
    legacySpace = OptionalAttribute('w:legacySpace', ST_TwipsMeasure )
    legacyIndent = OptionalAttribute('w:legacyIndent', ST_SignedTwipsMeasure )

class CT_MultiLevelType(BaseOxmlElement):
    """
    ``<w:multiLevelType>`` element, which indicates
    whether a numbering style is single-level,
    multi-level, or hybrid.
    """
    val = RequiredAttribute('w:val', ST_MultiLevelType )

    @classmethod
    def new(cls, val):
        """
        Return a new ``<w:multiLevelType>`` element with ``val``
        attribute set to *val*
        """
        multiLevelType = OxmlElement('w:multiLevelType')
        multiLevelType.val = val
        return multiLevelType

class CT_AbstractNum(BaseOxmlElement):
    """
    ``<w:abstractNum>`` element, which collects
    all of the level-specific style information
    for a particular style.
    """
    nsid = ZeroOrMore('w:nsid')
    multiLevelType = ZeroOrMore('w:multiLevelType')
    tmpl = ZeroOrMore('w:tmpl')
    name = ZeroOrMore('w:name')
    styleLink = ZeroOrMore('w:styleLink')
    numStyleLink = ZeroOrMore('w:numStyleLink')
    lvl = ZeroOrMore('w:lvl')
    abstractNumId = RequiredAttribute('w:abstractNumId', ST_DecimalNumber)

    @classmethod
    def new(cls, abstractNumId):
        """
        Return a new ``<w:abstractNum>`` element with ``abstractNumId``
        set to *abstractNumId*.
        """
        abstractNum = OxmlElement('w:abstractNum')
        abstractNum.abstractNumId = abstractNumId
        return abstractNum

class CT_Lvl(BaseOxmlElement):
    """
    ``<w:lvl>`` element, which contains all of
    the actual, level-specific formatting for
    a list style.
    """
    start = ZeroOrMore('w:start')
    numFmt = ZeroOrMore('w:numFmt')
    lvlRestart = ZeroOrMore('w:lvlRestart')
    pStyle = ZeroOrMore('w:pStyle')
    isLgl = ZeroOrMore('w:isLgl')
    suff = ZeroOrMore('w:suff')
    lvlText = ZeroOrMore('w:lvlText')
    lvlPicBulletId = ZeroOrMore('w:lvlPicBulletId')
    legacy = ZeroOrMore('w:legacy')
    lvlJc = ZeroOrMore('w:lvlJc')
    pPr = ZeroOrMore('w:pPr')
    rPr = ZeroOrMore('w:rPr')
    ilvl = RequiredAttribute('w:ilvl', ST_DecimalNumber)
    tplc = OptionalAttribute('w:tplc', ST_LongHexNumber)
    tentative = OptionalAttribute('w:tentative', ST_OnOff)

    @classmethod
    def new(cls, ilvl):
        """
        Return a new ``<w:lvl>`` element with ``ilvl``
        attribute set to *ilvl*
        """
        lvl = OxmlElement('w:lvl')
        lvl.ilvl = ilvl
        return lvl

class CT_NumPicBullet(BaseOxmlElement):
    """
    ``<w:numPicBullet>``` for specifying
    a picture or SVG drawing as the bullet
    symbol in a bulleted list.
    """
    pict = Choice('w:pict')
    drawing = Choice('w:drawing')
    numPicBulletId = RequiredAttribute('w:numPicBulletId', ST_DecimalNumber )

    @classmethod
    def new(cls, Id):
        """
        Return a new ``<w:numPicBullet>`` element with ``numPicBulletId``
        attribute set to *numPicBulletId*
        """
        numPicBullet = OxmlElement('w:numPicBullet')
        numPicBullet.numPicBulletId = Id
        return numPicBullet

class CT_Num(BaseOxmlElement):
    """
    ``<w:num>`` element, which represents a concrete list definition
    instance, having a required child <w:abstractNumId> that references an
    abstract numbering definition that defines most of the formatting details.
    """
    abstractNumId = OneAndOnlyOne('w:abstractNumId')
    lvlOverride = ZeroOrMore('w:lvlOverride')
    numId = RequiredAttribute('w:numId', ST_DecimalNumber)

    def add_lvlOverride(self, ilvl):
        """
        Return a newly added CT_NumLvl (<w:lvlOverride>) element having its
        ``ilvl`` attribute set to *ilvl*.
        """
        return self._add_lvlOverride(ilvl=ilvl)

    @classmethod
    def new(cls, num_id, abstractNum_id):
        """
        Return a new ``<w:num>`` element having numId of *num_id* and having
        a ``<w:abstractNumId>`` child with val attribute set to
        *abstractNum_id*.
        """
        num = OxmlElement('w:num')
        num.numId = num_id
        abstractNumId = CT_DecimalNumber.new(
            'w:abstractNumId', abstractNum_id
        )
        num.append(abstractNumId)
        return num


class CT_NumLvl(BaseOxmlElement):
    """
    ``<w:lvlOverride>`` element, which identifies a level in a list
    definition to override with settings it contains.
    """
    startOverride = ZeroOrOne('w:startOverride', successors=('w:lvl',))
    ilvl = RequiredAttribute('w:ilvl', ST_DecimalNumber)

    def add_startOverride(self, val):
        """
        Return a newly added CT_DecimalNumber element having tagname
        ``w:startOverride`` and ``val`` attribute set to *val*.
        """
        return self._add_startOverride(val=val)


class CT_NumPr(BaseOxmlElement):
    """
    A ``<w:numPr>`` element, a container for numbering properties applied to
    a paragraph.
    """
    ilvl = ZeroOrOne('w:ilvl', successors=(
        'w:numId', 'w:numberingChange', 'w:ins'
    ))
    numId = ZeroOrOne('w:numId', successors=('w:numberingChange', 'w:ins'))

    # @ilvl.setter
    # def _set_ilvl(self, val):
    #     """
    #     Get or add a <w:ilvl> child and set its ``w:val`` attribute to *val*.
    #     """
    #     ilvl = self.get_or_add_ilvl()
    #     ilvl.val = val

    # @numId.setter
    # def numId(self, val):
    #     """
    #     Get or add a <w:numId> child and set its ``w:val`` attribute to
    #     *val*.
    #     """
    #     numId = self.get_or_add_numId()
    #     numId.val = val


class CT_Numbering(BaseOxmlElement):
    """
    ``<w:numbering>`` element, the root element of a numbering part, i.e.
    numbering.xml
    """
    num = ZeroOrMore('w:num', successors=('w:numIdMacAtCleanup',))
    abstractNum = ZeroOrMore('w:abstractNum')

    def add_num(self, abstractNum_id):
        """
        Return a newly added CT_Num (<w:num>) element referencing the
        abstract numbering definition identified by *abstractNum_id*.
        """
        next_num_id = self._next_numId
        num = CT_Num.new(next_num_id, abstractNum_id)
        return self._insert_num(num)

    def num_having_numId(self, numId):
        """
        Return the ``<w:num>`` child element having ``numId`` attribute
        matching *numId*.
        """
        xpath = './w:num[@w:numId="%d"]' % numId
        try:
            return self.xpath(xpath)[0]
        except IndexError:
            raise KeyError('no <w:num> element with numId %d' % numId)

    def abstractNum_having_abstractNumId(self, abstractNumId):
        """
        Return the ``<w:abstractNum>`` child element having ``abstractNumId`` attribute
        matching *numId*.
        """
        xpath = './w:abstractNum[@w:abstractNumId="%d"]' % abstractNumId
        try:
            return self.xpath(xpath)[0]
        except IndexError:
            raise KeyError('no <w:abstractNum> element with abstractNumId %d' % abstractNumId)

    @property
    def _next_numId(self):
        """
        The first ``numId`` unused by a ``<w:num>`` element, starting at
        1 and filling any gaps in numbering between existing ``<w:num>``
        elements.
        """
        numId_strs = self.xpath('./w:num/@w:numId')
        num_ids = [int(numId_str) for numId_str in numId_strs]
        for num in range(1, len(num_ids)+2):
            if num not in num_ids:
                break
        return num
