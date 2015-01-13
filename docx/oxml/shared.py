# encoding: utf-8

"""
Objects shared by modules in the docx.oxml subpackage.
"""

from __future__ import absolute_import

from . import OxmlElement
from .ns import qn
from .simpletypes import ST_DecimalNumber, ST_OnOff, ST_String
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


class CT_HpsMeasure(CT_DecimalNumber):
    """
    Used for ``<w:size>``, ``<w:kern>``, ``<w:sz>``, ``<w:szCs>``, ``<w:hps>``,
    ``<w:hpsRaise>``, ``<w:hpsBaseText>``
    """
    _val = None

    @classmethod
    def new(cls, nsptagname, val):
        """
        Return a new ``CT_HpsMeasure`` element having tagname *nsptagname*
        and ``val`` attribute set to #val * 2#.
        """
        val = val * 2
        return super(CT_HpsMeasure, cls).new(nsptagname, val)

    @property
    def val(self):
        val = self.get(qn('w:val'))
        return int(val) / 2

    @val.setter
    def val(self, val):
        val = val * 2
        self.set(qn('w:val'), str(val))


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
