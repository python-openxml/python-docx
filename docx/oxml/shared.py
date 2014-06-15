# encoding: utf-8

"""
Objects shared by modules in the docx.oxml subpackage.
"""

from __future__ import absolute_import

from lxml import etree

from . import OxmlElement
from .exceptions import ValidationError
from .ns import qn
from .xmlchemy import serialize_for_reading


class OxmlBaseElement(etree.ElementBase):
    """
    Base class for all custom element classes, to add standardized behavior
    to all classes in one place.
    """
    def first_child_found_in(self, *tagnames):
        """
        Return the first child found with tag in *tagnames*, or None if
        not found.
        """
        for tagname in tagnames:
            child = self.find(qn(tagname))
            if child is not None:
                return child
        return None

    def insert_element_before(self, elm, *tagnames):
        successor = self.first_child_found_in(*tagnames)
        if successor is not None:
            successor.addprevious(elm)
        else:
            self.append(elm)
        return elm

    @property
    def xml(self):
        """
        Return XML string for this element, suitable for testing purposes.
        Pretty printed for readability and without an XML declaration at the
        top.
        """
        return serialize_for_reading(self)


class CT_DecimalNumber(OxmlBaseElement):
    """
    Used for ``<w:numId>``, ``<w:ilvl>``, ``<w:abstractNumId>`` and several
    others, containing a text representation of a decimal number (e.g. 42) in
    its ``val`` attribute.
    """
    @classmethod
    def new(cls, nsptagname, val):
        """
        Return a new ``CT_DecimalNumber`` element having tagname *nsptagname*
        and ``val`` attribute set to *val*.
        """
        return OxmlElement(nsptagname, attrs={qn('w:val'): str(val)})

    @property
    def val(self):
        """
        Required attribute containing a decimal integer
        """
        number_str = self.get(qn('w:val'))
        return int(number_str)

    @val.setter
    def val(self, val):
        decimal_number_str = '%d' % val
        self.set(qn('w:val'), decimal_number_str)


class CT_OnOff(OxmlBaseElement):
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
        raise ValidationError("expected xsd:boolean, got '%s'" % val)

    @val.setter
    def val(self, value):
        val = qn('w:val')
        if bool(value) is True:
            if val in self.attrib:
                del self.attrib[val]
        else:
            self.set(val, '0')


class CT_String(OxmlBaseElement):
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
