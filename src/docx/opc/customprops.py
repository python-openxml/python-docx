# encoding: utf-8

"""
Support reading and writing custom properties to and from a .docx file.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import numbers
from lxml import etree

NS_VT = "http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"

class CustomProperties(object):
    """
    Corresponds to part named ``/docProps/custom.xml``, containing the custom
    document properties for this document package.
    """
    def __init__(self, element):
        self._element = element

    def __getitem__( self, item ):
        prop = self.lookup(item)
        if prop is not None :
            # print(etree.tostring(prop, pretty_print=True))
            elm = prop[0]
            if elm.tag == f"{{{NS_VT}}}i4":
                try:
                    return int(elm.text)
                except:
                    return elm.text
            elif elm.tag == f"{{{NS_VT}}}bool":
                return True if elm.text == '1' else False
            return elm.text

    def __setitem__( self, key, value ):
        prop = self.lookup(key)
        if prop is None :
            elmType = 'lpwstr'
            if isinstance(value, bool):
                elmType = 'bool'
                value = str(1 if value else 0)
            elif isinstance(value, numbers.Number):
                elmType = 'i4'
                value = str(int(value))
            prop = etree.SubElement( self._element, "property" )
            elm = etree.SubElement(prop, f"{{{NS_VT}}}{elmType}", nsmap = {'vt':NS_VT} )
            elm.text = value
            prop.set("name", key)
            prop.set("fmtid", "{D5CDD505-2E9C-101B-9397-08002B2CF9AE}")
            prop.set("pid", "%s" % str(len(self._element) + 1))
        else:
            elm = prop[0]
            if elm.tag == f"{{{NS_VT}}}i4":
                elm.text = str(int(value))
            elif elm.tag == f"{{{NS_VT}}}bool":
                elm.text = str(1 if value else 0)
            else:
                elm.text = str(value)

    def __len__( self ):
        return len(self._element)

    def lookup(self, item):
        for child in self._element :
            if child.get("name") == item :
                return child
        return None