# encoding: utf-8

"""
Namespace-related objects.
"""

from __future__ import absolute_import, print_function, unicode_literals


nsmap = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcmitype": "http://purl.org/dc/dcmitype/",
    "dcterms": "http://purl.org/dc/terms/",
    "dgm": "http://schemas.openxmlformats.org/drawingml/2006/diagram",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "sl": "http://schemas.openxmlformats.org/schemaLibrary/2006/main",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    'w14': "http://schemas.microsoft.com/office/word/2010/wordml",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "xml": "http://www.w3.org/XML/1998/namespace",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

pfxmap = dict((value, key) for key, value in nsmap.items())


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

    @classmethod
    def from_clark_name(cls, clark_name):
        nsuri, local_name = clark_name[1:].split('}')
        nstag = '%s:%s' % (pfxmap[nsuri], local_name)
        return cls(nstag)

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
    """
    Return a string containing a namespace declaration for each of the
    namespace prefix strings, e.g. 'p', 'ct', passed as *prefixes*.
    """
    return ' '.join(['xmlns:%s="%s"' % (pfx, nsmap[pfx]) for pfx in prefixes])


def nspfxmap(*nspfxs):
    """
    Return a dict containing the subset namespace prefix mappings specified by
    *nspfxs*. Any number of namespace prefixes can be supplied, e.g.
    namespaces('a', 'r', 'p').
    """
    return dict((pfx, nsmap[pfx]) for pfx in nspfxs)


def qn(tag):
    """
    Stands for "qualified name", a utility function to turn a namespace
    prefixed tag name into a Clark-notation qualified tag name for lxml. For
    example, ``qn('p:cSld')`` returns ``'{http://schemas.../main}cSld'``.
    """
    prefix, tagroot = tag.split(':')
    uri = nsmap[prefix]
    return '{%s}%s' % (uri, tagroot)
