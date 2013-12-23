# encoding: utf-8

"""
Objects shared by modules in the docx.oxml subpackage.
"""

from lxml import etree


nsmap = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
}

# configure XML parser
element_class_lookup = etree.ElementNamespaceClassLookup()
oxml_parser = etree.XMLParser(remove_blank_text=True)
oxml_parser.set_element_class_lookup(element_class_lookup)


# ===========================================================================
# utility functions
# ===========================================================================

# def _Element(tag, nsmap=None):
#     return oxml_parser.makeelement(qn(tag), nsmap=nsmap)


def nsdecls(*prefixes):
    return ' '.join(['xmlns:%s="%s"' % (pfx, nsmap[pfx]) for pfx in prefixes])


def OxmlElement(tag, attrs=None):
    return oxml_parser.makeelement(qn(tag), attrib=attrs, nsmap=nsmap)


def oxml_fromstring(text):
    """
    ``etree.fromstring()`` replacement that uses oxml parser
    """
    return etree.fromstring(text, oxml_parser)


def qn(tag):
    """
    Stands for "qualified name", a utility function to turn a namespace
    prefixed tag name into a Clark-notation qualified tag name for lxml. For
    example, ``qn('p:cSld')`` returns ``'{http://schemas.../main}cSld'``.
    """
    prefix, tagroot = tag.split(':')
    uri = nsmap[prefix]
    return '{%s}%s' % (uri, tagroot)


def register_custom_element_class(tag, cls):
    """
    Register *cls* to be constructed when the oxml parser encounters an
    element with matching *tag*. *tag* is a string of the form
    ``nspfx:tagroot``, e.g. ``'w:document'``.
    """
    nspfx, tagroot = tag.split(':')
    namespace = element_class_lookup.get_namespace(nsmap[nspfx])
    namespace[tagroot] = cls


def serialize_for_reading(element):
    """
    Serialize *element* to human-readable XML suitable for tests. No XML
    declaration.
    """
    return etree.tostring(element, encoding='unicode', pretty_print=True)


def _SubElement(parent, tag):
    return etree.SubElement(parent, qn(tag), nsmap=nsmap)


class OxmlBaseElement(etree.ElementBase):
    """
    Base class for all custom element classes, to add standardized behavior
    to all classes in one place.
    """
    @property
    def xml(self):
        """
        Return XML string for this element, suitable for testing purposes.
        Pretty printed for readability and without an XML declaration at the
        top.
        """
        return serialize_for_reading(self)


# ===========================================================================
# shared custom element classes
# ===========================================================================

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

    @property
    def val(self):
        return self.get(qn('w:val'))

    @val.setter
    def val(self, val):
        return self.set(qn('w:val'), val)
