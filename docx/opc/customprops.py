# encoding: utf-8

"""
The :mod:`pptx.packaging` module coheres around the concerns of reading and
writing presentations to and from a .pptx file.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

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
        # print(etree.tostring(self._element, pretty_print=True))
        prop = self.lookup(item)
        if prop is not None :
            return prop[0].text

    def __setitem__( self, key, value ):
        prop = self.lookup(key)
        if prop is None :
            prop = etree.SubElement( self._element, "property" )
            elm = etree.SubElement(prop, '{%s}lpwstr' % NS_VT, nsmap = {'vt':NS_VT} )
            prop.set("name", key)
            prop.set("fmtid", "{D5CDD505-2E9C-101B-9397-08002B2CF9AE}")
            prop.set("pid", "%s" % str(len(self._element) + 1))
        else:
            elm = prop[0]
        elm.text = value
        # etree.tostring(prop, pretty_print=True)

    def lookup(self, item):
        for child in self._element :
            if child.get("name") == item :
                return child
        return None

