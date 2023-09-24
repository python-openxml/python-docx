# encoding: utf-8

"""
Test suite for the docx.shared module
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from docx.opc.part import XmlPart
from docx.shared import ElementProxy, Length, Cm, Emu, Inches, Mm, Pt, RGBColor, Twips

from .unitutil.cxml import element
from .unitutil.mock import instance_mock


class DescribeElementProxy(object):
    def it_knows_when_its_equal_to_another_proxy_object(self, eq_fixture):
        proxy, proxy_2, proxy_3, not_a_proxy = eq_fixture

        assert (proxy == proxy_2) is True
        assert (proxy == proxy_3) is False
        assert (proxy == not_a_proxy) is False

        assert (proxy != proxy_2) is False
        assert (proxy != proxy_3) is True
        assert (proxy != not_a_proxy) is True

    def it_knows_its_element(self, element_fixture):
        proxy, element = element_fixture
        assert proxy.element is element

    def it_knows_its_part(self, part_fixture):
        proxy, part_ = part_fixture
        assert proxy.part is part_

    # fixture --------------------------------------------------------

    @pytest.fixture
    def element_fixture(self):
        p = element("w:p")
        proxy = ElementProxy(p)
        return proxy, p

    @pytest.fixture
    def eq_fixture(self):
        p, q = element("w:p"), element("w:p")
        proxy = ElementProxy(p)
        proxy_2 = ElementProxy(p)
        proxy_3 = ElementProxy(q)
        not_a_proxy = "Foobar"
        return proxy, proxy_2, proxy_3, not_a_proxy

    @pytest.fixture
    def part_fixture(self, other_proxy_, part_):
        other_proxy_.part = part_
        proxy = ElementProxy(None, other_proxy_)
        return proxy, part_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def other_proxy_(self, request):
        return instance_mock(request, ElementProxy)

    @pytest.fixture
    def part_(self, request):
        return instance_mock(request, XmlPart)


class DescribeLength(object):
    def it_can_construct_from_convenient_units(self, construct_fixture):
        UnitCls, units_val, emu = construct_fixture
        length = UnitCls(units_val)
        assert isinstance(length, Length)
        assert length == emu

    def it_can_self_convert_to_convenient_units(self, units_fixture):
        emu, units_prop_name, expected_length_in_units, type_ = units_fixture
        length = Length(emu)
        length_in_units = getattr(length, units_prop_name)
        assert length_in_units == expected_length_in_units
        assert isinstance(length_in_units, type_)

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            (Length, 914400, 914400),
            (Inches, 1.1, 1005840),
            (Cm, 2.53, 910799),
            (Emu, 9144.9, 9144),
            (Mm, 13.8, 496800),
            (Pt, 24.5, 311150),
            (Twips, 360, 228600),
        ]
    )
    def construct_fixture(self, request):
        UnitCls, units_val, emu = request.param
        return UnitCls, units_val, emu

    @pytest.fixture(
        params=[
            (914400, "inches", 1.0, float),
            (914400, "cm", 2.54, float),
            (914400, "emu", 914400, int),
            (914400, "mm", 25.4, float),
            (914400, "pt", 72.0, float),
            (914400, "twips", 1440, int),
        ]
    )
    def units_fixture(self, request):
        emu, units_prop_name, expected_length_in_units, type_ = request.param
        return emu, units_prop_name, expected_length_in_units, type_


class DescribeRGBColor(object):
    def it_is_natively_constructed_using_three_ints_0_to_255(self):
        RGBColor(0x12, 0x34, 0x56)
        with pytest.raises(ValueError):
            RGBColor("12", "34", "56")
        with pytest.raises(ValueError):
            RGBColor(-1, 34, 56)
        with pytest.raises(ValueError):
            RGBColor(12, 256, 56)

    def it_can_construct_from_a_hex_string_rgb_value(self):
        rgb = RGBColor.from_string("123456")
        assert rgb == RGBColor(0x12, 0x34, 0x56)

    def it_can_provide_a_hex_string_rgb_value(self):
        assert str(RGBColor(0x12, 0x34, 0x56)) == "123456"

    def it_has_a_custom_repr(self):
        rgb_color = RGBColor(0x42, 0xF0, 0xBA)
        assert repr(rgb_color) == "RGBColor(0x42, 0xf0, 0xba)"
