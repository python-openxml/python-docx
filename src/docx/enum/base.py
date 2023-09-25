# encoding: utf-8

"""
Base classes and other objects used by enumerations
"""

from __future__ import absolute_import, print_function

import sys
import textwrap

from ..exceptions import InvalidXmlError


def alias(*aliases):
    """
    Decorating a class with @alias('FOO', 'BAR', ..) allows the class to
    be referenced by each of the names provided as arguments.
    """

    def decorator(cls):
        # alias must be set in globals from caller's frame
        caller = sys._getframe(1)
        globals_dict = caller.f_globals
        for alias in aliases:
            globals_dict[alias] = cls
        return cls

    return decorator


class _DocsPageFormatter(object):
    """Generate an .rst doc page for an enumeration.

    Formats a RestructuredText documention page (string) for the enumeration
    class parts passed to the constructor. An immutable one-shot service
    object.
    """

    def __init__(self, clsname, clsdict):
        self._clsname = clsname
        self._clsdict = clsdict

    @property
    def page_str(self):
        """
        The RestructuredText documentation page for the enumeration. This is
        the only API member for the class.
        """
        tmpl = ".. _%s:\n\n%s\n\n%s\n\n----\n\n%s"
        components = (
            self._ms_name,
            self._page_title,
            self._intro_text,
            self._member_defs,
        )
        return tmpl % components

    @property
    def _intro_text(self):
        """Docstring of the enumeration, formatted for documentation page."""
        try:
            cls_docstring = self._clsdict["__doc__"]
        except KeyError:
            cls_docstring = ""

        if cls_docstring is None:
            return ""

        return textwrap.dedent(cls_docstring).strip()

    def _member_def(self, member):
        """
        Return an individual member definition formatted as an RST glossary
        entry, wrapped to fit within 78 columns.
        """
        member_docstring = textwrap.dedent(member.docstring).strip()
        member_docstring = textwrap.fill(
            member_docstring,
            width=78,
            initial_indent=" " * 4,
            subsequent_indent=" " * 4,
        )
        return "%s\n%s\n" % (member.name, member_docstring)

    @property
    def _member_defs(self):
        """
        A single string containing the aggregated member definitions section
        of the documentation page
        """
        members = self._clsdict["__members__"]
        member_defs = [
            self._member_def(member) for member in members if member.name is not None
        ]
        return "\n".join(member_defs)

    @property
    def _ms_name(self):
        """
        The Microsoft API name for this enumeration
        """
        return self._clsdict["__ms_name__"]

    @property
    def _page_title(self):
        """
        The title for the documentation page, formatted as code (surrounded
        in double-backtics) and underlined with '=' characters
        """
        title_underscore = "=" * (len(self._clsname) + 4)
        return "``%s``\n%s" % (self._clsname, title_underscore)


class MetaEnumeration(type):
    """
    The metaclass for Enumeration and its subclasses. Adds a name for each
    named member and compiles state needed by the enumeration class to
    respond to other attribute gets
    """

    def __new__(meta, clsname, bases, clsdict):
        meta._add_enum_members(clsdict)
        meta._collect_valid_settings(clsdict)
        meta._generate_docs_page(clsname, clsdict)
        return type.__new__(meta, clsname, bases, clsdict)

    @classmethod
    def _add_enum_members(meta, clsdict):
        """
        Dispatch ``.add_to_enum()`` call to each member so it can do its
        thing to properly add itself to the enumeration class. This
        delegation allows member sub-classes to add specialized behaviors.
        """
        enum_members = clsdict["__members__"]
        for member in enum_members:
            member.add_to_enum(clsdict)

    @classmethod
    def _collect_valid_settings(meta, clsdict):
        """
        Return a sequence containing the enumeration values that are valid
        assignment values. Return-only values are excluded.
        """
        enum_members = clsdict["__members__"]
        valid_settings = []
        for member in enum_members:
            valid_settings.extend(member.valid_settings)
        clsdict["_valid_settings"] = valid_settings

    @classmethod
    def _generate_docs_page(meta, clsname, clsdict):
        """
        Return the RST documentation page for the enumeration.
        """
        clsdict["__docs_rst__"] = _DocsPageFormatter(clsname, clsdict).page_str


class EnumerationBase(object):
    """
    Base class for all enumerations, used directly for enumerations requiring
    only basic behavior. It's __dict__ is used below in the Python 2+3
    compatible metaclass definition.
    """

    __members__ = ()
    __ms_name__ = ""

    @classmethod
    def validate(cls, value):
        """
        Raise |ValueError| if *value* is not an assignable value.
        """
        if value not in cls._valid_settings:
            raise ValueError(
                "%s not a member of %s enumeration" % (value, cls.__name__)
            )


Enumeration = MetaEnumeration("Enumeration", (object,), dict(EnumerationBase.__dict__))


class XmlEnumeration(Enumeration):
    """
    Provides ``to_xml()`` and ``from_xml()`` methods in addition to base
    enumeration features
    """

    __members__ = ()
    __ms_name__ = ""

    @classmethod
    def from_xml(cls, xml_val):
        """
        Return the enumeration member corresponding to the XML value
        *xml_val*.
        """
        if xml_val not in cls._xml_to_member:
            raise InvalidXmlError(
                "attribute value '%s' not valid for this type" % xml_val
            )
        return cls._xml_to_member[xml_val]

    @classmethod
    def to_xml(cls, enum_val):
        """
        Return the XML value of the enumeration value *enum_val*.
        """
        if enum_val not in cls._member_to_xml:
            raise ValueError(
                "value '%s' not in enumeration %s" % (enum_val, cls.__name__)
            )
        return cls._member_to_xml[enum_val]


class EnumMember(object):
    """
    Used in the enumeration class definition to define a member value and its
    mappings
    """

    def __init__(self, name, value, docstring):
        self._name = name
        if isinstance(value, int):
            value = EnumValue(name, value, docstring)
        self._value = value
        self._docstring = docstring

    def add_to_enum(self, clsdict):
        """
        Add a name to *clsdict* for this member.
        """
        self.register_name(clsdict)

    @property
    def docstring(self):
        """
        The description of this member
        """
        return self._docstring

    @property
    def name(self):
        """
        The distinguishing name of this member within the enumeration class,
        e.g. 'MIDDLE' for MSO_VERTICAL_ANCHOR.MIDDLE, if this is a named
        member. Otherwise the primitive value such as |None|, |True| or
        |False|.
        """
        return self._name

    def register_name(self, clsdict):
        """
        Add a member name to the class dict *clsdict* containing the value of
        this member object. Where the name of this object is None, do
        nothing; this allows out-of-band values to be defined without adding
        a name to the class dict.
        """
        if self.name is None:
            return
        clsdict[self.name] = self.value

    @property
    def valid_settings(self):
        """
        A sequence containing the values valid for assignment for this
        member. May be zero, one, or more in number.
        """
        return (self._value,)

    @property
    def value(self):
        """
        The enumeration value for this member, often an instance of
        EnumValue, but may be a primitive value such as |None|.
        """
        return self._value


class EnumValue(int):
    """
    A named enumeration value, providing __str__ and __doc__ string values
    for its symbolic name and description, respectively. Subclasses int, so
    behaves as a regular int unless the strings are asked for.
    """

    def __new__(cls, member_name, int_value, docstring):
        return super(EnumValue, cls).__new__(cls, int_value)

    def __init__(self, member_name, int_value, docstring):
        super(EnumValue, self).__init__()
        self._member_name = member_name
        self._docstring = docstring

    @property
    def __doc__(self):
        """
        The description of this enumeration member
        """
        return self._docstring.strip()

    def __str__(self):
        """
        The symbolic name and string value of this member, e.g. 'MIDDLE (3)'
        """
        return "%s (%d)" % (self._member_name, int(self))


class ReturnValueOnlyEnumMember(EnumMember):
    """
    Used to define a member of an enumeration that is only valid as a query
    result and is not valid as a setting, e.g. MSO_VERTICAL_ANCHOR.MIXED (-2)
    """

    @property
    def valid_settings(self):
        """
        No settings are valid for a return-only value.
        """
        return ()


class XmlMappedEnumMember(EnumMember):
    """
    Used to define a member whose value maps to an XML attribute value.
    """

    def __init__(self, name, value, xml_value, docstring):
        super(XmlMappedEnumMember, self).__init__(name, value, docstring)
        self._xml_value = xml_value

    def add_to_enum(self, clsdict):
        """
        Compile XML mappings in addition to base add behavior.
        """
        super(XmlMappedEnumMember, self).add_to_enum(clsdict)
        self.register_xml_mapping(clsdict)

    def register_xml_mapping(self, clsdict):
        """
        Add XML mappings to the enumeration class state for this member.
        """
        member_to_xml = self._get_or_add_member_to_xml(clsdict)
        member_to_xml[self.value] = self.xml_value
        xml_to_member = self._get_or_add_xml_to_member(clsdict)
        xml_to_member[self.xml_value] = self.value

    @property
    def xml_value(self):
        """
        The XML attribute value that corresponds to this enumeration value
        """
        return self._xml_value

    @staticmethod
    def _get_or_add_member_to_xml(clsdict):
        """
        Add the enum -> xml value mapping to the enumeration class state
        """
        if "_member_to_xml" not in clsdict:
            clsdict["_member_to_xml"] = dict()
        return clsdict["_member_to_xml"]

    @staticmethod
    def _get_or_add_xml_to_member(clsdict):
        """
        Add the xml -> enum value mapping to the enumeration class state
        """
        if "_xml_to_member" not in clsdict:
            clsdict["_xml_to_member"] = dict()
        return clsdict["_xml_to_member"]
