# encoding: utf-8

"""
Custom element classes related to the styles part
"""

from ...enum.style import WD_STYLE_TYPE
from ..simpletypes import ST_String
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
    name = ZeroOrOne('w:name', successors=_tag_seq[1:])
    pPr = ZeroOrOne('w:pPr', successors=_tag_seq[17:])
    type = OptionalAttribute('w:type', WD_STYLE_TYPE)
    styleId = OptionalAttribute('w:styleId', ST_String)
    del _tag_seq

    @property
    def name_val(self):
        """
        Value of ``<w:name>`` child or |None| if not present.
        """
        name = self.name
        if name is None:
            return None
        return name.val


class CT_Styles(BaseOxmlElement):
    """
    ``<w:styles>`` element, the root element of a styles part, i.e.
    styles.xml
    """
    style = ZeroOrMore('w:style', successors=())

    def get_by_id(self, styleId):
        """
        Return the ``<w:style>`` child element having ``styleId`` attribute
        matching *styleId*, or |None| if not found.
        """
        xpath = 'w:style[@w:styleId="%s"]' % styleId
        try:
            return self.xpath(xpath)[0]
        except IndexError:
            return None

    def get_by_name(self, name):
        """
        Return the ``<w:style>`` child element having ``<w:name>`` child
        element with value *name*, or |None| if not found.
        """
        xpath = 'w:style[w:name/@w:val="%s"]' % name
        try:
            return self.xpath(xpath)[0]
        except IndexError:
            return None
