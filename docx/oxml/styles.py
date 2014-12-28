# encoding: utf-8

"""
Custom element classes related to the styles part
"""

from ..enum.style import WD_STYLE_TYPE
from .simpletypes import ST_OnOff, ST_String
from .xmlchemy import (
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
    default = OptionalAttribute('w:default', ST_OnOff)
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

    @name_val.setter
    def name_val(self, value):
        self._remove_name()
        if value is not None:
            name = self._add_name()
            name.val = value


class CT_Styles(BaseOxmlElement):
    """
    ``<w:styles>`` element, the root element of a styles part, i.e.
    styles.xml
    """
    style = ZeroOrMore('w:style', successors=())

    def add_style_of_type(self, name, style_type, builtin):
        """
        Return a newly added `w:style` element having *name* and
        *style_type*. `w:style/@customStyle` is set based on the value of
        *builtin*.
        """
        raise NotImplementedError

    def default_for(self, style_type):
        """
        Return `w:style[@w:type="*{style_type}*][-1]` or |None| if not found.
        """
        default_styles_for_type = [
            s for s in self._iter_styles()
            if s.type == style_type and s.default
        ]
        if not default_styles_for_type:
            return None
        # spec calls for last default in document order
        return default_styles_for_type[-1]

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

    def _iter_styles(self):
        """
        Generate each of the `w:style` child elements in document order.
        """
        return (style for style in self.xpath('w:style'))
