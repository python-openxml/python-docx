# encoding: utf-8

"""
Custom element classes related to the styles part
"""

from ..xmlchemy import BaseOxmlElement, ZeroOrMore, ZeroOrOne


class CT_Style(BaseOxmlElement):
    """
    A ``<w:style>`` element, representing a style definition
    """
    pPr = ZeroOrOne('w:pPr', successors=(
        'w:rPr', 'w:tblPr', 'w:trPr', 'w:tcPr', 'w:tblStylePr'
    ))


class CT_Styles(BaseOxmlElement):
    """
    ``<w:styles>`` element, the root element of a styles part, i.e.
    styles.xml
    """
    style = ZeroOrMore('w:style', successors=())

    def style_having_styleId(self, styleId):
        """
        Return the ``<w:style>`` child element having ``styleId`` attribute
        matching *styleId*.
        """
        xpath = './w:style[@w:styleId="%s"]' % styleId
        try:
            return self.xpath(xpath)[0]
        except IndexError:
            raise KeyError('no <w:style> element with styleId %d' % styleId)
