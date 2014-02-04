# encoding: utf-8

"""
Custom element classes related to the styles part
"""

from docx.oxml.shared import nsmap, OxmlBaseElement, qn


class CT_Style(OxmlBaseElement):
    """
    A ``<w:style>`` element, representing a style definition
    """
    @property
    def pPr(self):
        return self.find(qn('w:pPr'))


class CT_Styles(OxmlBaseElement):
    """
    ``<w:styles>`` element, the root element of a styles part, i.e.
    styles.xml
    """
    def style_having_styleId(self, styleId):
        """
        Return the ``<w:style>`` child element having ``styleId`` attribute
        matching *styleId*.
        """
        xpath = './w:style[@w:styleId="%s"]' % styleId
        try:
            return self.xpath(xpath, namespaces=nsmap)[0]
        except IndexError:
            raise KeyError('no <w:style> element with styleId %d' % styleId)

    @property
    def style_lst(self):
        """
        List of <w:style> child elements.
        """
        return self.findall(qn('w:style'))
