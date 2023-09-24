# encoding: utf-8

"""Parser for Compact XML Expression Language (CXEL) ('see-ex-ell').

CXEL is a compact XML specification language I made up that's useful for producing XML
element trees suitable for unit testing.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from pyparsing import (
    alphas,
    alphanums,
    Combine,
    dblQuotedString,
    delimitedList,
    Forward,
    Group,
    Literal,
    Optional,
    removeQuotes,
    stringEnd,
    Suppress,
    Word,
)

from docx.oxml import parse_xml
from docx.oxml.ns import nsmap


# ====================================================================
# api functions
# ====================================================================


def element(cxel_str):
    """
    Return an oxml element parsed from the XML generated from *cxel_str*.
    """
    _xml = xml(cxel_str)
    return parse_xml(_xml)


def xml(cxel_str):
    """
    Return the XML generated from *cxel_str*.
    """
    root_token = root_node.parseString(cxel_str)
    xml = root_token.element.xml
    return xml


# ====================================================================
# internals
# ====================================================================


def nsdecls(*nspfxs):
    """
    Return a string containing a namespace declaration for each of *nspfxs*,
    in the order they are specified.
    """
    nsdecls = ""
    for nspfx in nspfxs:
        nsdecls += ' xmlns:%s="%s"' % (nspfx, nsmap[nspfx])
    return nsdecls


class Element(object):
    """
    Represents an XML element, having a namespace, tagname, attributes, and
    may contain either text or children (but not both) or may be empty.
    """

    def __init__(self, tagname, attrs, text):
        self._tagname = tagname
        self._attrs = attrs
        self._text = text
        self._children = []
        self._is_root = False

    def __repr__(self):
        """
        Provide a more meaningful repr value for an Element object, one that
        displays the tagname as a simple empty element, e.g. ``<w:pPr/>``.
        """
        return "<%s/>" % self._tagname

    def connect_children(self, child_node_list):
        """
        Make each of the elements appearing in *child_node_list* a child of
        this element.
        """
        for node in child_node_list:
            child = node.element
            self._children.append(child)

    @classmethod
    def from_token(cls, token):
        """
        Return an ``Element`` object constructed from a parser element token.
        """
        tagname = token.tagname
        attrs = [(name, value) for name, value in token.attr_list]
        text = token.text
        return cls(tagname, attrs, text)

    @property
    def is_root(self):
        """
        |True| if this element is the root of the tree and should include the
        namespace prefixes. |False| otherwise.
        """
        return self._is_root

    @is_root.setter
    def is_root(self, value):
        self._is_root = bool(value)

    @property
    def local_nspfxs(self):
        """
        The namespace prefixes local to this element, both on the tagname and
        all of its attributes. An empty string (``''``) is used to represent
        the default namespace for an element tag having no prefix.
        """

        def nspfx(name, is_element=False):
            idx = name.find(":")
            if idx == -1:
                return "" if is_element else None
            return name[:idx]

        nspfxs = [nspfx(self._tagname, True)]
        for name, val in self._attrs:
            pfx = nspfx(name)
            if pfx is None or pfx in nspfxs or pfx == "xml":
                continue
            nspfxs.append(pfx)
        return nspfxs

    @property
    def nspfxs(self):
        """
        A sequence containing each of the namespace prefixes appearing in
        this tree. Each prefix appears once and only once, and in document
        order.
        """

        def merge(seq, seq_2):
            for item in seq_2:
                if item in seq:
                    continue
                seq.append(item)

        nspfxs = self.local_nspfxs
        for child in self._children:
            merge(nspfxs, child.nspfxs)
        return nspfxs

    @property
    def xml(self):
        """
        The XML corresponding to the tree rooted at this element,
        pretty-printed using 2-spaces indentation at each level and with
        a trailing '\n'.
        """
        return self._xml(indent=0)

    def _xml(self, indent):
        """
        Return a string containing the XML of this element and all its
        children with a starting indent of *indent* spaces.
        """
        self._indent_str = " " * indent
        xml = self._start_tag
        for child in self._children:
            xml += child._xml(indent + 2)
        xml += self._end_tag
        return xml

    @property
    def _start_tag(self):
        """
        The text of the opening tag of this element, including attributes. If
        this is the root element, a namespace declaration for each of the
        namespace prefixes that occur in this tree is added in front of any
        attributes. If this element contains text, that text follows the
        start tag. If not, and this element has no children, an empty tag is
        returned. Otherwise, an opening tag is returned, followed by
        a newline. The tag is indented by this element's indent value in all
        cases.
        """
        _nsdecls = nsdecls(*self.nspfxs) if self.is_root else ""
        tag = "%s<%s%s" % (self._indent_str, self._tagname, _nsdecls)
        for attr in self._attrs:
            name, value = attr
            tag += ' %s="%s"' % (name, value)
        if self._text:
            tag += ">%s" % self._text
        elif self._children:
            tag += ">\n"
        else:
            tag += "/>\n"
        return tag

    @property
    def _end_tag(self):
        """
        The text of the closing tag of this element, if there is one. If the
        element contains text, no leading indentation is included.
        """
        if self._text:
            tag = "</%s>\n" % self._tagname
        elif self._children:
            tag = "%s</%s>\n" % (self._indent_str, self._tagname)
        else:
            tag = ""
        return tag


# ====================================================================
# parser
# ====================================================================

# parse actions ----------------------------------


def connect_node_children(s, loc, tokens):
    node = tokens[0]
    node.element.connect_children(node.child_node_list)


def connect_root_node_children(root_node):
    root_node.element.connect_children(root_node.child_node_list)
    root_node.element.is_root = True


def grammar():
    # terminals ----------------------------------
    colon = Literal(":")
    equal = Suppress("=")
    slash = Suppress("/")
    open_paren = Suppress("(")
    close_paren = Suppress(")")
    open_brace = Suppress("{")
    close_brace = Suppress("}")

    # np:tagName ---------------------------------
    nspfx = Word(alphas)
    local_name = Word(alphanums)
    tagname = Combine(nspfx + colon + local_name)

    # np:attr_name=attr_val ----------------------
    attr_name = Word(alphas + ":")
    attr_val = Word(alphanums + " %-./:_")
    attr_def = Group(attr_name + equal + attr_val)
    attr_list = open_brace + delimitedList(attr_def) + close_brace

    text = dblQuotedString.setParseAction(removeQuotes)

    # w:jc{val=right} ----------------------------
    element = (
        tagname("tagname")
        + Group(Optional(attr_list))("attr_list")
        + Optional(text, default="")("text")
    ).setParseAction(Element.from_token)

    child_node_list = Forward()

    node = Group(
        element("element") + Group(Optional(slash + child_node_list))("child_node_list")
    ).setParseAction(connect_node_children)

    child_node_list << (open_paren + delimitedList(node) + close_paren | node)

    root_node = (
        element("element")
        + Group(Optional(slash + child_node_list))("child_node_list")
        + stringEnd
    ).setParseAction(connect_root_node_children)

    return root_node


root_node = grammar()
