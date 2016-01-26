# encoding: utf-8

"""
Objects shared by modules in the docx.oxml subpackage.
"""

from __future__ import absolute_import
from . import OxmlElement
from .ns import qn
from .simpletypes import ST_DecimalNumber, ST_OnOff, ST_String, ST_HexColor, ST_ThemeColor, ST_UcharHexNumber, ST_Shd
from .xmlchemy import BaseOxmlElement, OptionalAttribute, RequiredAttribute


class CT_DecimalNumber(BaseOxmlElement):
    """
    Used for ``<w:numId>``, ``<w:ilvl>``, ``<w:abstractNumId>`` and several
    others, containing a text representation of a decimal number (e.g. 42) in
    its ``val`` attribute.
    """
    val = RequiredAttribute('w:val', ST_DecimalNumber)

    @classmethod
    def new(cls, nsptagname, val):
        """
        Return a new ``CT_DecimalNumber`` element having tagname *nsptagname*
        and ``val`` attribute set to *val*.
        """
        return OxmlElement(nsptagname, attrs={qn('w:val'): str(val)})


class CT_OnOff(BaseOxmlElement):
    """
    Used for ``<w:b>``, ``<w:i>`` elements and others, containing a bool-ish
    string in its ``val`` attribute, xsd:boolean plus 'on' and 'off'.
    """
    val = OptionalAttribute('w:val', ST_OnOff, default=True)


class CT_String(BaseOxmlElement):
    """
    Used for ``<w:pStyle>`` and ``<w:tblStyle>`` elements and others,
    containing a style name in its ``val`` attribute.
    """
    val = RequiredAttribute('w:val', ST_String)

    @classmethod
    def new(cls, nsptagname, val):
        """
        Return a new ``CT_String`` element with tagname *nsptagname* and
        ``val`` attribute set to *val*.
        """
        elm = OxmlElement(nsptagname)
        elm.val = val
        return elm


class CT_Shd(BaseOxmlElement):
    """
    Used for ``<w:shd>`` element
    """
    color = OptionalAttribute('w:color', ST_HexColor)
    fill = OptionalAttribute('w:fill', ST_HexColor)
    themeColor = OptionalAttribute('w:themeColor', ST_ThemeColor)
    themeFill = OptionalAttribute('w:themeFill', ST_ThemeColor)
    themeFillShade = OptionalAttribute('w:themeFillShade', ST_UcharHexNumber)
    themeFillTint = OptionalAttribute('w:themeFillTint', ST_UcharHexNumber)
    themeShade = OptionalAttribute('w:themeShade', ST_UcharHexNumber)
    themeTint = OptionalAttribute('w:themeTint', ST_UcharHexNumber)
    val = RequiredAttribute('w:val', ST_Shd)

    def __eq__(self, other):
        if other is not None and isinstance(other, CT_Shd):
            if self.color == other.color and self.fill == other.fill and self.themeColor == other.themeColor and \
                            self.themeFill == other.themeFill and self.themeFillShade == other.themeFillShade and \
                            self.themeFillTint == other.themeFillTint and self.themeShade == other.themeShade and \
                            self.themeTint == other.themeTint :
                return True
        return False
