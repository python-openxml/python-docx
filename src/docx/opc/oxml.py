"""Temporary stand-in for main oxml module.

This module came across with the PackageReader transplant. Probably much will get
replaced with objects from the pptx.oxml.core and then this module will either get
deleted or only hold the package related custom element classes.
"""

from lxml import etree

from docx.opc.constants import NAMESPACE as NS
from docx.opc.constants import RELATIONSHIP_TARGET_MODE as RTM

# configure XML parser
element_class_lookup = etree.ElementNamespaceClassLookup()
oxml_parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
oxml_parser.set_element_class_lookup(element_class_lookup)

nsmap = {
    "ct": NS.OPC_CONTENT_TYPES,
    "pr": NS.OPC_RELATIONSHIPS,
    "r": NS.OFC_RELATIONSHIPS,
}


# ===========================================================================
# functions
# ===========================================================================


def parse_xml(text: str) -> etree._Element:  # pyright: ignore[reportPrivateUsage]
    """`etree.fromstring()` replacement that uses oxml parser."""
    return etree.fromstring(text, oxml_parser)


def qn(tag):
    """Stands for "qualified name", a utility function to turn a namespace prefixed tag
    name into a Clark-notation qualified tag name for lxml.

    For
    example, ``qn('p:cSld')`` returns ``'{http://schemas.../main}cSld'``.
    """
    prefix, tagroot = tag.split(":")
    uri = nsmap[prefix]
    return "{%s}%s" % (uri, tagroot)


def serialize_part_xml(part_elm):
    """Serialize `part_elm` etree element to XML suitable for storage as an XML part.

    That is to say, no insignificant whitespace added for readability, and an
    appropriate XML declaration added with UTF-8 encoding specified.
    """
    return etree.tostring(part_elm, encoding="UTF-8", standalone=True)


def serialize_for_reading(element):
    """Serialize `element` to human-readable XML suitable for tests.

    No XML declaration.
    """
    return etree.tostring(element, encoding="unicode", pretty_print=True)


# ===========================================================================
# Custom element classes
# ===========================================================================


class BaseOxmlElement(etree.ElementBase):
    """Base class for all custom element classes, to add standardized behavior to all
    classes in one place."""

    @property
    def xml(self):
        """Return XML string for this element, suitable for testing purposes.

        Pretty printed for readability and without an XML declaration at the top.
        """
        return serialize_for_reading(self)


class CT_Default(BaseOxmlElement):
    """``<Default>`` element, specifying the default content type to be applied to a
    part with the specified extension."""

    @property
    def content_type(self):
        """String held in the ``ContentType`` attribute of this ``<Default>``
        element."""
        return self.get("ContentType")

    @property
    def extension(self):
        """String held in the ``Extension`` attribute of this ``<Default>`` element."""
        return self.get("Extension")

    @staticmethod
    def new(ext, content_type):
        """Return a new ``<Default>`` element with attributes set to parameter
        values."""
        xml = '<Default xmlns="%s"/>' % nsmap["ct"]
        default = parse_xml(xml)
        default.set("Extension", ext)
        default.set("ContentType", content_type)
        return default


class CT_Override(BaseOxmlElement):
    """``<Override>`` element, specifying the content type to be applied for a part with
    the specified partname."""

    @property
    def content_type(self):
        """String held in the ``ContentType`` attribute of this ``<Override>``
        element."""
        return self.get("ContentType")

    @staticmethod
    def new(partname, content_type):
        """Return a new ``<Override>`` element with attributes set to parameter
        values."""
        xml = '<Override xmlns="%s"/>' % nsmap["ct"]
        override = parse_xml(xml)
        override.set("PartName", partname)
        override.set("ContentType", content_type)
        return override

    @property
    def partname(self):
        """String held in the ``PartName`` attribute of this ``<Override>`` element."""
        return self.get("PartName")


class CT_Relationship(BaseOxmlElement):
    """``<Relationship>`` element, representing a single relationship from a source to a
    target part."""

    @staticmethod
    def new(rId, reltype, target, target_mode=RTM.INTERNAL):
        """Return a new ``<Relationship>`` element."""
        xml = '<Relationship xmlns="%s"/>' % nsmap["pr"]
        relationship = parse_xml(xml)
        relationship.set("Id", rId)
        relationship.set("Type", reltype)
        relationship.set("Target", target)
        if target_mode == RTM.EXTERNAL:
            relationship.set("TargetMode", RTM.EXTERNAL)
        return relationship

    @property
    def rId(self):
        """String held in the ``Id`` attribute of this ``<Relationship>`` element."""
        return self.get("Id")

    @property
    def reltype(self):
        """String held in the ``Type`` attribute of this ``<Relationship>`` element."""
        return self.get("Type")

    @property
    def target_ref(self):
        """String held in the ``Target`` attribute of this ``<Relationship>``
        element."""
        return self.get("Target")

    @property
    def target_mode(self):
        """String held in the ``TargetMode`` attribute of this ``<Relationship>``
        element, either ``Internal`` or ``External``.

        Defaults to ``Internal``.
        """
        return self.get("TargetMode", RTM.INTERNAL)


class CT_Relationships(BaseOxmlElement):
    """``<Relationships>`` element, the root element in a .rels file."""

    def add_rel(self, rId, reltype, target, is_external=False):
        """Add a child ``<Relationship>`` element with attributes set according to
        parameter values."""
        target_mode = RTM.EXTERNAL if is_external else RTM.INTERNAL
        relationship = CT_Relationship.new(rId, reltype, target, target_mode)
        self.append(relationship)

    @staticmethod
    def new():
        """Return a new ``<Relationships>`` element."""
        xml = '<Relationships xmlns="%s"/>' % nsmap["pr"]
        relationships = parse_xml(xml)
        return relationships

    @property
    def Relationship_lst(self):
        """Return a list containing all the ``<Relationship>`` child elements."""
        return self.findall(qn("pr:Relationship"))

    @property
    def xml(self):
        """Return XML string for this element, suitable for saving in a .rels stream,
        not pretty printed and with an XML declaration at the top."""
        return serialize_part_xml(self)


class CT_Types(BaseOxmlElement):
    """``<Types>`` element, the container element for Default and Override elements in
    [Content_Types].xml."""

    def add_default(self, ext, content_type):
        """Add a child ``<Default>`` element with attributes set to parameter values."""
        default = CT_Default.new(ext, content_type)
        self.append(default)

    def add_override(self, partname, content_type):
        """Add a child ``<Override>`` element with attributes set to parameter
        values."""
        override = CT_Override.new(partname, content_type)
        self.append(override)

    @property
    def defaults(self):
        return self.findall(qn("ct:Default"))

    @staticmethod
    def new():
        """Return a new ``<Types>`` element."""
        xml = '<Types xmlns="%s"/>' % nsmap["ct"]
        types = parse_xml(xml)
        return types

    @property
    def overrides(self):
        return self.findall(qn("ct:Override"))


ct_namespace = element_class_lookup.get_namespace(nsmap["ct"])
ct_namespace["Default"] = CT_Default
ct_namespace["Override"] = CT_Override
ct_namespace["Types"] = CT_Types

pr_namespace = element_class_lookup.get_namespace(nsmap["pr"])
pr_namespace["Relationship"] = CT_Relationship
pr_namespace["Relationships"] = CT_Relationships
