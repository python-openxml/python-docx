# encoding: utf-8

"""
Objects shared by modules in the docx.oxml subpackage.
"""

from __future__ import absolute_import

from lxml import etree

import re

from . import oxml_parser
from .exceptions import ValidationError
from .ns import NamespacePrefixedTag, nsmap, qn


# ===========================================================================
# utility functions
# ===========================================================================


def OxmlElement(nsptag_str, attrs=None, nsmap=None):
    """
    Return a 'loose' lxml element having the tag specified by *nsptag_str*.
    *nsptag_str* must contain the standard namespace prefix, e.g. 'a:tbl'.
    The resulting element is an instance of the custom element class for this
    tag name if one is defined. A dictionary of attribute values may be
    provided as *attrs*; they are set if present.
    """
    nsptag = NamespacePrefixedTag(nsptag_str)
    _nsmap = nsptag.nsmap if nsmap is None else nsmap
    return oxml_parser.makeelement(
        nsptag.clark_name, attrib=attrs, nsmap=_nsmap
    )


def serialize_for_reading(element):
    """
    Serialize *element* to human-readable XML suitable for tests. No XML
    declaration.
    """
    xml = etree.tostring(element, encoding='unicode', pretty_print=True)
    return XmlString(xml)


def _SubElement(parent, tag):
    return etree.SubElement(parent, qn(tag), nsmap=nsmap)


class XmlString(str):
    """
    Provides string comparison override suitable for serialized XML that is
    useful for tests.
    """

    # '    <w:xyz xmlns:a="http://ns/decl/a" attr_name="val">text</w:xyz>'
    # |          |                                          ||           |
    # +----------+------------------------------------------++-----------+
    #  front      attrs                                     | text
    #                                                     close

    _xml_elm_line_patt = re.compile(
        '( *</?[\w:]+)(.*?)(/?>)([^<]*</\w+>)?'
    )

    def __eq__(self, other):
        lines = self.splitlines()
        lines_other = other.splitlines()
        if len(lines) != len(lines_other):
            return False
        for line, line_other in zip(lines, lines_other):
            if not self._eq_elm_strs(line, line_other):
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def _attr_seq(self, attrs):
        """
        Return a sequence of attribute strings parsed from *attrs*. Each
        attribute string is stripped of whitespace on both ends.
        """
        attrs = attrs.strip()
        attr_lst = attrs.split()
        return sorted(attr_lst)

    def _eq_elm_strs(self, line, line_2):
        """
        Return True if the element in *line_2* is XML equivalent to the
        element in *line*.
        """
        front, attrs, close, text = self._parse_line(line)
        front_2, attrs_2, close_2, text_2 = self._parse_line(line_2)
        if front != front_2:
            return False
        if self._attr_seq(attrs) != self._attr_seq(attrs_2):
            return False
        if close != close_2:
            return False
        if text != text_2:
            return False
        return True

    def _parse_line(self, line):
        """
        Return front, attrs, close, text 4-tuple result of parsing XML element
        string *line*.
        """
        match = self._xml_elm_line_patt.match(line)
        front, attrs, close, text = [match.group(n) for n in range(1, 5)]
        return front, attrs, close, text


# ===========================================================================
# shared custom element classes
# ===========================================================================

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
