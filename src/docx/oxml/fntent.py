from .xmlchemy import (
    BaseOxmlElement, OneAndOnlyOne, ZeroOrMore, OneOrMore, RequiredAttribute
)
from .simpletypes import ST_DecimalNumber, ST_OnOff, ST_String

class CT_Footnotes(BaseOxmlElement):
    """
    A ``<w:footnotes>`` element, the root element of a footnotes part, i.e.
    footnotes.xml
    """

    footnote = ZeroOrMore('w:footnote')

    def get_by_id(self, footnoteId):
        """
        Return the ``<w:footnote>`` child element having ``w:id`` attribute
        matching *footnoteId*, or |None| if not found.
        """
        xpath = 'w:footnote[@w:id="%s"]' % footnoteId
        try:
            return self.xpath(xpath)[0]
        except IndexError:
            return None


class CT_Footnote(BaseOxmlElement):
    """
    A ``<w:footnote>`` element, representing a footnote definition
    """

    p = OneOrMore('w:p')

class CT_Endnotes(BaseOxmlElement):
    """
    A ``<w:endnotes>`` element, the root element of a endnotes part, i.e.
    endnotes.xml
    """

    endnote = ZeroOrMore('w:endnote')

    def get_by_id(self, endnoteId):
        """
        Return the ``<w:endnote>`` child element having ``w:id`` attribute
        matching *endnoteId*, or |None| if not found.
        """
        xpath = 'w:endnote[@w:id="%s"]' % endnoteId
        try:
            return self.xpath(xpath)[0]
        except IndexError:
            return None



class CT_Endnote(BaseOxmlElement):
    """
    A ``<w:endnote>`` element, representing a endnote definition
    """

    p = OneOrMore('w:p')


class CT_FootnoteReference(BaseOxmlElement):
    """
    A ``<w:footnoteReference>`` element. provide access to footnote proxy object.
    """

    id = RequiredAttribute('w:id', ST_String)


class CT_EndnoteReference(BaseOxmlElement):
    """
    A ``<w:endnoteReference>`` element. provide access to endnote proxy object.
    """

    id = RequiredAttribute('w:id', ST_String)
