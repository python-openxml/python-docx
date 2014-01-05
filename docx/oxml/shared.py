# encoding: utf-8

"""
Objects shared by modules in the docx.oxml subpackage.
"""

from lxml import etree

from .exceptions import ValidationError


nsmap = {
    'a':   ('http://schemas.openxmlformats.org/drawingml/2006/main'),
    'c':   ('http://schemas.openxmlformats.org/drawingml/2006/chart'),
    'dgm': ('http://schemas.openxmlformats.org/drawingml/2006/diagram'),
    'pic': ('http://schemas.openxmlformats.org/drawingml/2006/picture'),
    'r':   ('http://schemas.openxmlformats.org/officeDocument/2006/relations'
            'hips'),
    'w':   ('http://schemas.openxmlformats.org/wordprocessingml/2006/main'),
    'wp':  ('http://schemas.openxmlformats.org/drawingml/2006/wordprocessing'
            'Drawing'),
    'xml': ('http://www.w3.org/XML/1998/namespace')
}

# configure XML parser
element_class_lookup = etree.ElementNamespaceClassLookup()
oxml_parser = etree.XMLParser(remove_blank_text=True)
oxml_parser.set_element_class_lookup(element_class_lookup)


# ===========================================================================
# utility functions
# ===========================================================================

class NamespacePrefixedTag(str):
    """
    Value object that knows the semantics of an XML tag having a namespace
    prefix.
    """
    def __new__(cls, nstag, *args):
        return super(NamespacePrefixedTag, cls).__new__(cls, nstag)

    def __init__(self, nstag):
        self._pfx, self._local_part = nstag.split(':')
        self._ns_uri = nsmap[self._pfx]

    @property
    def clark_name(self):
        return '{%s}%s' % (self._ns_uri, self._local_part)

    @property
    def local_part(self):
        """
        Return the local part of the tag as a string. E.g. 'foobar' is
        returned for tag 'f:foobar'.
        """
        return self._local_part

    @property
    def nsmap(self):
        """
        Return a dict having a single member, mapping the namespace prefix of
        this tag to it's namespace name (e.g. {'f': 'http://foo/bar'}). This
        is handy for passing to xpath calls and other uses.
        """
        return {self._pfx: self._ns_uri}

    @property
    def nspfx(self):
        """
        Return the string namespace prefix for the tag, e.g. 'f' is returned
        for tag 'f:foobar'.
        """
        return self._pfx

    @property
    def nsuri(self):
        """
        Return the namespace URI for the tag, e.g. 'http://foo/bar' would be
        returned for tag 'f:foobar' if the 'f' prefix maps to
        'http://foo/bar' in nsmap.
        """
        return self._ns_uri


def nsdecls(*prefixes):
    return ' '.join(['xmlns:%s="%s"' % (pfx, nsmap[pfx]) for pfx in prefixes])


def nspfxmap(*nspfxs):
    """
    Return a dict containing the subset namespace prefix mappings specified by
    *nspfxs*. Any number of namespace prefixes can be supplied, e.g.
    namespaces('a', 'r', 'p').
    """
    return dict((pfx, nsmap[pfx]) for pfx in nspfxs)


def OxmlElement(nsptag_str, attrs=None, nsmap=None):
    """
    Return a 'loose' lxml element having the tag specified by *nsptag_str*.
    *nsptag_str* must contain the standard namespace prefix, e.g. 'a:tbl'.
    The resulting element is an instance of the custom element class for this
    tag name if one is defined. A dictionary of attribute values may be
    provided as *attrs*; they are set if present.
    """
    nsptag = NamespacePrefixedTag(nsptag_str)
    nsmap = nsmap if nsmap is not None else nsptag.nsmap
    return oxml_parser.makeelement(
        nsptag.clark_name, attrib=attrs, nsmap=nsmap
    )


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


# ===========================================================================
# shared custom element classes
# ===========================================================================

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

    @property
    def val(self):
        return self.get(qn('w:val'))

    @val.setter
    def val(self, val):
        return self.set(qn('w:val'), val)
