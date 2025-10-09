"""Test suite for the docx.shared module."""

from __future__ import annotations

import pytest

from docx.opc.part import XmlPart
from docx.shared import Cm, ElementProxy, Emu, Inches, Length, Mm, Pt, RGBColor, Twips

from .unitutil.cxml import element
from .unitutil.mock import FixtureRequest, Mock, instance_mock


class DescribeElementProxy:
    """Unit-test suite for `docx.shared.ElementProxy` objects."""

    def it_knows_when_its_equal_to_another_proxy_object(self):
        p, q = element("w:p"), element("w:p")
        proxy = ElementProxy(p)
        proxy_2 = ElementProxy(p)
        proxy_3 = ElementProxy(q)
        not_a_proxy = "Foobar"

        assert (proxy == proxy_2) is True
        assert (proxy == proxy_3) is False
        assert (proxy == not_a_proxy) is False

        assert (proxy != proxy_2) is False
        assert (proxy != proxy_3) is True
        assert (proxy != not_a_proxy) is True

    def it_knows_its_element(self):
        p = element("w:p")
        proxy = ElementProxy(p)
        assert proxy.element is p

    def it_knows_its_part(self, other_proxy_: Mock, part_: Mock):
        other_proxy_.part = part_
        proxy = ElementProxy(element("w:p"), other_proxy_)
        assert proxy.part is part_

    # -- fixture ---------------------------------------------------------------------------------

    @pytest.fixture
    def other_proxy_(self, request: FixtureRequest):
        return instance_mock(request, ElementProxy)

    @pytest.fixture
    def part_(self, request: FixtureRequest):
        return instance_mock(request, XmlPart)


class DescribeLength:
    """Unit-test suite for `docx.shared.Length` objects."""

    @pytest.mark.parametrize(
        ("UnitCls", "units_val", "emu"),
        [
            (Length, 914400, 914400),
            (Inches, 1.1, 1005840),
            (Cm, 2.53, 910799),
            (Emu, 9144.9, 9144),
            (Mm, 13.8, 496800),
            (Pt, 24.5, 311150),
            (Twips, 360, 228600),
        ],
    )
    def it_can_construct_from_convenient_units(self, UnitCls: type, units_val: float, emu: int):
        length = UnitCls(units_val)
        assert isinstance(length, Length)
        assert length == emu

    @pytest.mark.parametrize(
        ("prop_name", "expected_value", "expected_type"),
        [
            ("inches", 1.0, float),
            ("cm", 2.54, float),
            ("emu", 914400, int),
            ("mm", 25.4, float),
            ("pt", 72.0, float),
            ("twips", 1440, int),
        ],
    )
    def it_can_self_convert_to_convenient_units(
        self, prop_name: str, expected_value: float, expected_type: type
    ):
        # -- use an inch for the initial value --
        length = Length(914400)
        length_in_units = getattr(length, prop_name)
        assert length_in_units == expected_value
        assert isinstance(length_in_units, expected_type)


class DescribeRGBColor:
    """Unit-test suite for `docx.shared.RGBColor` objects."""

    def it_is_natively_constructed_using_three_ints_0_to_255(self):
        rgb_color = RGBColor(0x12, 0x34, 0x56)

        assert isinstance(rgb_color, RGBColor)
        # -- it is comparable to a tuple[int, int, int] --
        assert rgb_color == (18, 52, 86)

    def it_raises_with_helpful_error_message_on_wrong_types(self):
        with pytest.raises(TypeError, match=r"RGBColor\(\) takes three integer valu"):
            RGBColor("12", "34", "56")  # pyright: ignore
        with pytest.raises(ValueError, match=r"\(\) takes three integer values 0-255"):
            RGBColor(-1, 34, 56)
        with pytest.raises(ValueError, match=r"RGBColor\(\) takes three integer valu"):
            RGBColor(12, 256, 56)

    def it_can_construct_from_a_hex_string_rgb_value(self):
        rgb = RGBColor.from_string("123456")
        assert rgb == RGBColor(0x12, 0x34, 0x56)

    def it_can_provide_a_hex_string_rgb_value(self):
        assert str(RGBColor(0xF3, 0x8A, 0x56)) == "F38A56"

    def it_has_a_custom_repr(self):
        rgb_color = RGBColor(0x42, 0xF0, 0xBA)
        assert repr(rgb_color) == "RGBColor(0x42, 0xf0, 0xba)"
