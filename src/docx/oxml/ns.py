"""Namespace-related objects."""

from typing import Any, Dict

from typing_extensions import Self

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
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "xml": "http://www.w3.org/XML/1998/namespace",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

pfxmap = {value: key for key, value in nsmap.items()}


class NamespacePrefixedTag(str):
    """Value object that knows the semantics of an XML tag having a namespace prefix."""

    def __new__(cls, nstag: str, *args: Any):
        return super(NamespacePrefixedTag, cls).__new__(cls, nstag)

    def __init__(self, nstag: str):
        self._pfx, self._local_part = nstag.split(":")
        self._ns_uri = nsmap[self._pfx]

    @property
    def clark_name(self) -> str:
        return "{%s}%s" % (self._ns_uri, self._local_part)

    @classmethod
    def from_clark_name(cls, clark_name: str) -> Self:
        nsuri, local_name = clark_name[1:].split("}")
        nstag = "%s:%s" % (pfxmap[nsuri], local_name)
        return cls(nstag)

    @property
    def local_part(self) -> str:
        """The local part of this tag.

        E.g. "foobar" is returned for tag "f:foobar".
        """
        return self._local_part

    @property
    def nsmap(self) -> Dict[str, str]:
        """Single-member dict mapping prefix of this tag to it's namespace name.

        Example: `{"f": "http://foo/bar"}`. This is handy for passing to xpath calls
        and other uses.
        """
        return {self._pfx: self._ns_uri}

    @property
    def nspfx(self) -> str:
        """The namespace-prefix for this tag.

        For example, "f" is returned for tag "f:foobar".
        """
        return self._pfx

    @property
    def nsuri(self) -> str:
        """The namespace URI for this tag.

        For example, "http://foo/bar" would be returned for tag "f:foobar" if the "f"
        prefix maps to "http://foo/bar" in nsmap.
        """
        return self._ns_uri


def nsdecls(*prefixes: str) -> str:
    """Namespace declaration including each namespace-prefix in `prefixes`.

    Handy for adding required namespace declarations to a tree root element.
    """
    return " ".join(['xmlns:%s="%s"' % (pfx, nsmap[pfx]) for pfx in prefixes])


def nspfxmap(*nspfxs: str) -> Dict[str, str]:
    """Subset namespace-prefix mappings specified by *nspfxs*.

    Any number of namespace prefixes can be supplied, e.g. namespaces("a", "r", "p").
    """
    return {pfx: nsmap[pfx] for pfx in nspfxs}


def qn(tag: str) -> str:
    """Stands for "qualified name".

    This utility function converts a familiar namespace-prefixed tag name like "w:p"
    into a Clark-notation qualified tag name for lxml. For example, `qn("w:p")` returns
    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p".
    """
    prefix, tagroot = tag.split(":")
    uri = nsmap[prefix]
    return "{%s}%s" % (uri, tagroot)
