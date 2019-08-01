# encoding: utf-8

"""
Custom element classes that correspond to the customXml part, e.g.
<w:smartTag>.
"""

from .simpletypes import ST_String, XsdAnyUri
from .xmlchemy import (
    BaseOxmlElement,
    ZeroOrOne, ZeroOrMore,
    RequiredAttribute, OptionalAttribute
)

class CT_SmartTag(BaseOxmlElement):
    """
    A ``<w:smartTag>`` element.
    """

    uri = RequiredAttribute('w:uri', XsdAnyUri)
    element = RequiredAttribute('w:element', ST_String)

    # element = "firstName"
    r = ZeroOrMore('w:r')


class CT_SmartTagPr(BaseOxmlElement):
    """
    A ''<w:smartTagPr>'' element.
    """

    attr = ZeroOrMore('w:attr')


class CT_CustomXml(BaseOxmlElement):
    """
    ``<w:customXml>`` element.
    """
    uri = RequiredAttribute('w:uri', XsdAnyUri)
    element = RequiredAttribute('w:element', ST_String)

    customXmlPr = ZeroOrOne('w:customXmlPr')
    # element = "address"
    p = ZeroOrOne('w:p')
    tbl = ZeroOrOne('w:tbl')

    # element = "firstName"
    r = ZeroOrMore('w:r')

    # element = invoiceItem"
    tr = ZeroOrOne('w:tr')

    # name = "company"
    tc = ZeroOrOne('w:tc')


class CT_CustomXmlPr(BaseOxmlElement):
    """
    ''<w:cumstomXmlPr>'' element.
    """

    attr = ZeroOrMore('w:attr')
    placeholder = ZeroOrOne('w:placeholder')


class CT_Attr(BaseOxmlElement):
    """
    A ''<w:attr>'' element. Custom XML Attribute and Smart Tag Property
    """
    name = RequiredAttribute('w:name', ST_String)
    uri = RequiredAttribute('w:uri', ST_String)
    val = RequiredAttribute('w:val', ST_String)


class CT_Placeholder(BaseOxmlElement):
    """
    A ''<w:placeholder> element.
    """
    val = RequiredAttribute('w:val', ST_String)

