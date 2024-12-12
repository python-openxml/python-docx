# pyright: reportImportCycles=false

"""XML parser for python-docx."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Type, cast

from lxml import etree

from docx.oxml.ns import NamespacePrefixedTag, nsmap

if TYPE_CHECKING:
    from docx.oxml.xmlchemy import BaseOxmlElement


# -- configure XML parser --
element_class_lookup = etree.ElementNamespaceClassLookup()
oxml_parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
oxml_parser.set_element_class_lookup(element_class_lookup)


def parse_xml(xml: str | bytes) -> "BaseOxmlElement":
    """Root lxml element obtained by parsing XML character string `xml`.

    The custom parser is used, so custom element classes are produced for elements in
    `xml` that have them.
    """
    return cast("BaseOxmlElement", etree.fromstring(xml, oxml_parser))


def register_element_cls(tag: str, cls: Type["BaseOxmlElement"]):
    """Register an lxml custom element-class to use for `tag`.

    A instance of `cls` to be constructed when the oxml parser encounters an element
    with matching `tag`. `tag` is a string of the form `nspfx:tagroot`, e.g.
    `'w:document'`.
    """
    nspfx, tagroot = tag.split(":")
    namespace = element_class_lookup.get_namespace(nsmap[nspfx])
    namespace[tagroot] = cls


def OxmlElement(
    nsptag_str: str,
    attrs: Dict[str, str] | None = None,
    nsdecls: Dict[str, str] | None = None,
) -> BaseOxmlElement | etree._Element:  # pyright: ignore[reportPrivateUsage]
    """Return a 'loose' lxml element having the tag specified by `nsptag_str`.

    The tag in `nsptag_str` must contain the standard namespace prefix, e.g. `a:tbl`.
    The resulting element is an instance of the custom element class for this tag name
    if one is defined. A dictionary of attribute values may be provided as `attrs`; they
    are set if present. All namespaces defined in the dict `nsdecls` are declared in the
    element using the key as the prefix and the value as the namespace name. If
    `nsdecls` is not provided, a single namespace declaration is added based on the
    prefix on `nsptag_str`.
    """
    nsptag = NamespacePrefixedTag(nsptag_str)
    if nsdecls is None:
        nsdecls = nsptag.nsmap
    return oxml_parser.makeelement(nsptag.clark_name, attrib=attrs, nsmap=nsdecls)
