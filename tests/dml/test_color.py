# pyright: reportPrivateUsage=false

"""Unit-test suite for the `docx.dml.color` module."""

from __future__ import annotations

from typing import cast

import pytest

from docx.dml.color import ColorFormat
from docx.enum.dml import MSO_COLOR_TYPE, MSO_THEME_COLOR
from docx.oxml.text.run import CT_R
from docx.shared import RGBColor

from ..unitutil.cxml import element, xml


class DescribeColorFormat:
    """Unit-test suite for `docx.dml.color.ColorFormat` objects."""

    @pytest.mark.parametrize(
        ("r_cxml", "expected_value"),
        [
            ("w:r", None),
            ("w:r/w:rPr", None),
            ("w:r/w:rPr/w:color{w:val=auto}", MSO_COLOR_TYPE.AUTO),
            ("w:r/w:rPr/w:color{w:val=4224FF}", MSO_COLOR_TYPE.RGB),
            ("w:r/w:rPr/w:color{w:themeColor=dark1}", MSO_COLOR_TYPE.THEME),
            (
                "w:r/w:rPr/w:color{w:val=F00BA9,w:themeColor=accent1}",
                MSO_COLOR_TYPE.THEME,
            ),
        ],
    )
    def it_knows_its_color_type(self, r_cxml: str, expected_value: MSO_COLOR_TYPE | None):
        assert ColorFormat(cast(CT_R, element(r_cxml))).type == expected_value

    @pytest.mark.parametrize(
        ("r_cxml", "rgb"),
        [
            ("w:r", None),
            ("w:r/w:rPr", None),
            ("w:r/w:rPr/w:color{w:val=auto}", None),
            ("w:r/w:rPr/w:color{w:val=4224FF}", "4224ff"),
            ("w:r/w:rPr/w:color{w:val=auto,w:themeColor=accent1}", None),
            ("w:r/w:rPr/w:color{w:val=F00BA9,w:themeColor=accent1}", "f00ba9"),
        ],
    )
    def it_knows_its_RGB_value(self, r_cxml: str, rgb: str | None):
        expected_value = RGBColor.from_string(rgb) if rgb else None
        assert ColorFormat(cast(CT_R, element(r_cxml))).rgb == expected_value

    @pytest.mark.parametrize(
        ("r_cxml", "new_value", "expected_cxml"),
        [
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
        ],
    )
    def it_can_change_its_RGB_value(
        self, r_cxml: str, new_value: RGBColor | None, expected_cxml: str
    ):
        color_format = ColorFormat(cast(CT_R, element(r_cxml)))
        color_format.rgb = new_value
        assert color_format._element.xml == xml(expected_cxml)

    @pytest.mark.parametrize(
        ("r_cxml", "expected_value"),
        [
            ("w:r", None),
            ("w:r/w:rPr", None),
            ("w:r/w:rPr/w:color{w:val=auto}", None),
            ("w:r/w:rPr/w:color{w:val=4224FF}", None),
            ("w:r/w:rPr/w:color{w:themeColor=accent1}", MSO_THEME_COLOR.ACCENT_1),
            ("w:r/w:rPr/w:color{w:val=F00BA9,w:themeColor=dark1}", MSO_THEME_COLOR.DARK_1),
        ],
    )
    def it_knows_its_theme_color(self, r_cxml: str, expected_value: MSO_THEME_COLOR | None):
        color_format = ColorFormat(cast(CT_R, element(r_cxml)))
        assert color_format.theme_color == expected_value

    @pytest.mark.parametrize(
        ("r_cxml", "new_value", "expected_cxml"),
        [
            (
                "w:r",
                MSO_THEME_COLOR.ACCENT_1,
                "w:r/w:rPr/w:color{w:val=000000,w:themeColor=accent1}",
            ),
            (
                "w:r/w:rPr",
                MSO_THEME_COLOR.ACCENT_2,
                "w:r/w:rPr/w:color{w:val=000000,w:themeColor=accent2}",
            ),
            (
                "w:r/w:rPr/w:color{w:val=101112}",
                MSO_THEME_COLOR.ACCENT_3,
                "w:r/w:rPr/w:color{w:val=101112,w:themeColor=accent3}",
            ),
            (
                "w:r/w:rPr/w:color{w:val=234bcd,w:themeColor=dark1}",
                MSO_THEME_COLOR.LIGHT_2,
                "w:r/w:rPr/w:color{w:val=234bcd,w:themeColor=light2}",
            ),
            ("w:r/w:rPr/w:color{w:val=234bcd,w:themeColor=dark1}", None, "w:r/w:rPr"),
            ("w:r", None, "w:r"),
        ],
    )
    def it_can_change_its_theme_color(
        self, r_cxml: str, new_value: MSO_THEME_COLOR | None, expected_cxml: str
    ):
        color_format = ColorFormat(cast(CT_R, element(r_cxml)))
        color_format.theme_color = new_value
        assert color_format._element.xml == xml(expected_cxml)
