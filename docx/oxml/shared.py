# encoding: utf-8

"""
Objects shared by modules in the docx.oxml subpackage.
"""

from __future__ import absolute_import

from . import OxmlElement
from .exceptions import InvalidXmlError
from .ns import qn
from .simpletypes import ST_DecimalNumber
from .xmlchemy import BaseOxmlElement, RequiredAttribute


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
    @property
    def val(self):
        val = self.get(qn('w:val'))
        if val is None:
            return True
        elif val in ('0', 'false', 'off'):
            return False
        elif val in ('1', 'true', 'on'):
            return True
        raise InvalidXmlError("expected xsd:boolean, got '%s'" % val)

    @val.setter
    def val(self, value):
        val = qn('w:val')
        if bool(value) is True:
            if val in self.attrib:
                del self.attrib[val]
        else:
            self.set(val, '0')


class CT_String(BaseOxmlElement):
    """
    Used for ``<w:pStyle>`` and ``<w:tblStyle>`` elements and others,
    containing a style name in its ``val`` attribute.
    """
    @classmethod
    def new(cls, nsptagname, val):
        """
        Return a new ``CT_String`` element with tagname *nsptagname* and
        ``val`` attribute set to *val*.
        """
        return OxmlElement(nsptagname, attrs={qn('w:val'): val})

    @classmethod
    def new_pStyle(cls, val):
        """
        Return a new ``<w:pStyle>`` element with ``val`` attribute set to
        *val*.
        """
        return OxmlElement('w:pStyle', attrs={qn('w:val'): val})

    @classmethod
    def new_rStyle(cls, val):
        """
        Return a new ``<w:rStyle>`` element with ``val`` attribute set to
        *val*.
        """
        return OxmlElement('w:rStyle', attrs={qn('w:val'): val})

    @property
    def val(self):
        return self.get(qn('w:val'))

    @val.setter
    def val(self, val):
        return self.set(qn('w:val'), val)
