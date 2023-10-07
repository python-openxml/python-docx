"""Test suite for docx.enum module, focused on base classes.

Configured a little differently because of the meta-programming, the two enumeration
classes at the top constitute the entire fixture and the tests themselves just make
assertions on those.
"""

import enum

import pytest

from docx.enum.base import BaseXmlEnum


class SomeXmlAttr(BaseXmlEnum):
    """SomeXmlAttr docstring."""

    FOO = (1, "foo", "Do foo instead of bar.")
    """Do foo instead of bar."""

    BAR = (2, "bar", "Do bar instead of foo.")
    """Do bar instead of foo."""

    BAZ = (3, None, "Maps to the value assumed when the attribute is omitted.")
    """Maps to the value assumed when the attribute is omitted."""


class DescribeBaseXmlEnum:
    """Unit-test suite for `docx.enum.base.BaseXmlEnum`."""

    def it_is_an_instance_of_EnumMeta_just_like_a_regular_Enum(self):
        assert type(SomeXmlAttr) is enum.EnumMeta

    def it_has_the_same_repr_as_a_regular_Enum(self):
        assert repr(SomeXmlAttr) == "<enum 'SomeXmlAttr'>"

    def it_has_an_MRO_that_goes_through_the_base_class_int_and_Enum(self):
        assert SomeXmlAttr.__mro__ == (
            SomeXmlAttr,
            BaseXmlEnum,
            int,
            enum.Enum,
            object,
        ), f"got: {SomeXmlAttr.__mro__}"

    def it_knows_the_XML_value_for_each_member_by_the_member_instance(self):
        assert SomeXmlAttr.to_xml(SomeXmlAttr.FOO) == "foo"

    def it_knows_the_XML_value_for_each_member_by_the_member_value(self):
        assert SomeXmlAttr.to_xml(2) == "bar"

    def but_it_raises_when_there_is_no_such_member(self):
        with pytest.raises(ValueError, match="42 is not a valid SomeXmlAttr"):
            SomeXmlAttr.to_xml(42)

    def it_can_find_the_member_from_the_XML_attr_value(self):
        assert SomeXmlAttr.from_xml("bar") == SomeXmlAttr.BAR

    def and_it_can_find_the_member_from_None_when_a_member_maps_that(self):
        assert SomeXmlAttr.from_xml(None) == SomeXmlAttr.BAZ

    def but_it_raises_when_there_is_no_such_mapped_XML_value(self):
        with pytest.raises(
            ValueError, match="SomeXmlAttr has no XML mapping for 'baz'"
        ):
            SomeXmlAttr.from_xml("baz")


class DescribeBaseXmlEnumMembers:
    """Unit-test suite for `docx.enum.base.BaseXmlEnum`."""

    def it_is_an_instance_of_its_XmlEnum_subtype_class(self):
        assert type(SomeXmlAttr.FOO) is SomeXmlAttr

    def it_has_the_default_Enum_repr(self):
        assert repr(SomeXmlAttr.BAR) == "<SomeXmlAttr.BAR: 2>"

    def but_its_str_value_is_customized(self):
        assert str(SomeXmlAttr.FOO) == "FOO (1)"

    def its_value_is_the_same_int_as_its_corresponding_MS_API_enum_member(self):
        assert SomeXmlAttr.FOO.value == 1

    def its_name_is_its_member_name_the_same_as_a_regular_Enum(self):
        assert SomeXmlAttr.FOO.name == "FOO"

    def it_has_an_individual_member_specific_docstring(self):
        assert SomeXmlAttr.FOO.__doc__ == "Do foo instead of bar."

    def it_is_equivalent_to_its_int_value(self):
        assert SomeXmlAttr.FOO == 1
        assert SomeXmlAttr.FOO != 2
        assert SomeXmlAttr.BAR == 2
        assert SomeXmlAttr.BAR != 1
