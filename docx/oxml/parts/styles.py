# encoding: utf-8

"""
Custom element classes related to the styles part
"""

from ...enum.style import WD_STYLE_TYPE
from ..xmlchemy import (
    BaseOxmlElement, OptionalAttribute, ZeroOrMore, ZeroOrOne
)


class CT_Style(BaseOxmlElement):
    """
    A ``<w:style>`` element, representing a style definition
    """
    _tag_seq = (
        'w:name', 'w:aliases', 'w:basedOn', 'w:next', 'w:link',
        'w:autoRedefine', 'w:hidden', 'w:uiPriority', 'w:semiHidden',
        'w:unhideWhenUsed', 'w:qFormat', 'w:locked', 'w:personal',
        'w:personalCompose', 'w:personalReply', 'w:rsid', 'w:pPr', 'w:rPr',
        'w:tblPr', 'w:trPr', 'w:tcPr', 'w:tblStylePr'
    )
    pPr = ZeroOrOne('w:pPr', successors=_tag_seq[17:])
    type = OptionalAttribute('w:type', WD_STYLE_TYPE)
    del _tag_seq


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
            raise KeyError('no <w:style> element with styleId %s' % styleId)