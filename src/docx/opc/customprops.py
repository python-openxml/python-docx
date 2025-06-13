# encoding: utf-8

"""
Support reading and writing custom properties to and from a .docx file.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import numbers
from lxml import etree
from docx.oxml.ns import nspfxmap, qn


class CustomProperties(object):
    """
    Corresponds to part named ``/docProps/custom.xml``, containing the custom
    document properties for this document package.
    """
    def __init__(self, element):
        self._element = element

    def __getitem__(self, item):
        prop = self.lookup(item)
        if prop is not None:
            elm = prop[0]
            if elm.tag == qn("vt:i4"):
                try:
                    return int(elm.text)
                except ValueError:
                    return elm.text
            elif elm.tag == qn("vt:bool"):
                return True if elm.text == '1' else False
            return elm.text

    def __setitem__(self, key, value):
        prop = self.lookup(key)
        if prop is None:
            elm_type = 'lpwstr'
            if isinstance(value, bool):
                elm_type = 'bool'
                value = str(1 if value else 0)
            elif isinstance(value, numbers.Number):
                elm_type = 'i4'
                value = str(int(value))
            prop = etree.SubElement(self._element, qn("op:property"), nsmap=nspfxmap("op"))
            elm = etree.SubElement(prop, qn(f"vt:{elm_type}"), nsmap=nspfxmap("vt"))
            elm.text = value
            prop.set("name", key)
            # magic number "FMTID_UserDefinedProperties"
            # MS doc ref: https://learn.microsoft.com/de-de/windows/win32/stg/predefined-property-set-format-identifiers
            prop.set("fmtid", "{D5CDD505-2E9C-101B-9397-08002B2CF9AE}")
            prop.set("pid", str(len(self._element) + 1))
        else:
            elm = prop[0]
            if elm.tag == qn("vt:i4"):
                elm.text = str(int(value))
            elif elm.tag == qn("vt:bool"):
                elm.text = str(1 if value else 0)
            else:
                elm.text = str(value)

    def __delitem__(self, key):
        prop = self.lookup(key)
        if prop is not None:
            self._element.remove(prop)

    def __len__(self):
        return len(self._element)

    def __iter__(self):
        for child in self._element:
            yield child.get("name")

    def lookup(self, item):
        for child in self._element:
            if child.get("name") == item:
                return child
        return None
