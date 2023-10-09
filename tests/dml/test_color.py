"""Test suite for docx.dml.color module."""

import pytest

from docx.dml.color import ColorFormat
from docx.enum.dml import MSO_COLOR_TYPE, MSO_THEME_COLOR
from docx.shared import RGBColor

from ..unitutil.cxml import element, xml


class DescribeColorFormat:
    def it_knows_its_color_type(self, type_fixture):
        color_format, expected_value = type_fixture
        assert color_format.type == expected_value

    def it_knows_its_RGB_value(self, rgb_get_fixture):
        color_format, expected_value = rgb_get_fixture
        assert color_format.rgb == expected_value

    def it_can_change_its_RGB_value(self, rgb_set_fixture):
        color_format, new_value, expected_xml = rgb_set_fixture
        color_format.rgb = new_value
        assert color_format._element.xml == expected_xml

    def it_knows_its_theme_color(self, theme_color_get_fixture):
        color_format, expected_value = theme_color_get_fixture
        assert color_format.theme_color == expected_value

    def it_can_change_its_theme_color(self, theme_color_set_fixture):
        color_format, new_value, expected_xml = theme_color_set_fixture
        color_format.theme_color = new_value
        assert color_format._element.xml == expected_xml

    # fixtures ---------------------------------------------

    @pytest.fixture(
        params=[
            ("w:r", None),
            ("w:r/w:rPr", None),
            ("w:r/w:rPr/w:color{w:val=auto}", None),
            ("w:r/w:rPr/w:color{w:val=4224FF}", "4224ff"),
            ("w:r/w:rPr/w:color{w:val=auto,w:themeColor=accent1}", None),
            ("w:r/w:rPr/w:color{w:val=F00BA9,w:themeColor=accent1}", "f00ba9"),
        ]
    )
    def rgb_get_fixture(self, request):
        r_cxml, rgb = request.param
        color_format = ColorFormat(element(r_cxml))
        expected_value = None if rgb is None else RGBColor.from_string(rgb)
        return color_format, expected_value

    @pytest.fixture(
        params=[
            ("w:r", RGBColor(10, 20, 30), "w:r/w:rPr/w:color{w:val=0A141E}"),
            ("w:r/w:rPr", RGBColor(1, 2, 3), "w:r/w:rPr/w:color{w:val=010203}"),
            (
                "w:r/w:rPr/w:color{w:val=123abc}",
                RGBColor(42, 24, 99),
                "w:r/w:rPr/w:color{w:val=2A1863}",
            ),
            (
                "w:r/w:rPr/w:color{w:val=auto}",
                RGBColor(16, 17, 18),
                "w:r/w:rPr/w:color{w:val=101112}",
            ),
            (
                "w:r/w:rPr/w:color{w:val=234bcd,w:themeColor=dark1}",
                RGBColor(24, 42, 99),
                "w:r/w:rPr/w:color{w:val=182A63}",
            ),
            ("w:r/w:rPr/w:color{w:val=234bcd,w:themeColor=dark1}", None, "w:r/w:rPr"),
            ("w:r", None, "w:r"),
        ]
    )
    def rgb_set_fixture(self, request):
        r_cxml, new_value, expected_cxml = request.param
        color_format = ColorFormat(element(r_cxml))
        expected_xml = xml(expected_cxml)
        return color_format, new_value, expected_xml

    @pytest.fixture(
        params=[
            ("w:r", None),
            ("w:r/w:rPr", None),
            ("w:r/w:rPr/w:color{w:val=auto}", None),
            ("w:r/w:rPr/w:color{w:val=4224FF}", None),
            ("w:r/w:rPr/w:color{w:themeColor=accent1}", "ACCENT_1"),
            ("w:r/w:rPr/w:color{w:val=F00BA9,w:themeColor=dark1}", "DARK_1"),
        ]
    )
    def theme_color_get_fixture(self, request):
        r_cxml, value = request.param
        color_format = ColorFormat(element(r_cxml))
        expected_value = None if value is None else getattr(MSO_THEME_COLOR, value)
        return color_format, expected_value

    @pytest.fixture(
        params=[
            ("w:r", "ACCENT_1", "w:r/w:rPr/w:color{w:val=000000,w:themeColor=accent1}"),
            (
                "w:r/w:rPr",
                "ACCENT_2",
                "w:r/w:rPr/w:color{w:val=000000,w:themeColor=accent2}",
            ),
            (
                "w:r/w:rPr/w:color{w:val=101112}",
                "ACCENT_3",
                "w:r/w:rPr/w:color{w:val=101112,w:themeColor=accent3}",
            ),
            (
                "w:r/w:rPr/w:color{w:val=234bcd,w:themeColor=dark1}",
                "LIGHT_2",
                "w:r/w:rPr/w:color{w:val=234bcd,w:themeColor=light2}",
            ),
            ("w:r/w:rPr/w:color{w:val=234bcd,w:themeColor=dark1}", None, "w:r/w:rPr"),
            ("w:r", None, "w:r"),
        ]
    )
    def theme_color_set_fixture(self, request):
        r_cxml, member, expected_cxml = request.param
        color_format = ColorFormat(element(r_cxml))
        new_value = None if member is None else getattr(MSO_THEME_COLOR, member)
        expected_xml = xml(expected_cxml)
        return color_format, new_value, expected_xml

    @pytest.fixture(
        params=[
            ("w:r", None),
            ("w:r/w:rPr", None),
            ("w:r/w:rPr/w:color{w:val=auto}", MSO_COLOR_TYPE.AUTO),
            ("w:r/w:rPr/w:color{w:val=4224FF}", MSO_COLOR_TYPE.RGB),
            ("w:r/w:rPr/w:color{w:themeColor=dark1}", MSO_COLOR_TYPE.THEME),
            (
                "w:r/w:rPr/w:color{w:val=F00BA9,w:themeColor=accent1}",
                MSO_COLOR_TYPE.THEME,
            ),
        ]
    )
    def type_fixture(self, request):
        r_cxml, expected_value = request.param
        color_format = ColorFormat(element(r_cxml))
        return color_format, expected_value
