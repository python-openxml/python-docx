"""Unit test suite for the docx.oxml.simpletypes module."""

import pytest

from docx.oxml.simpletypes import ST_TwipsMeasure
from docx.shared import Inches, Twips


class DescribeST_TwipsMeasure:
    @pytest.mark.parametrize(
        ("str_value", "expected_twips"),
        [("0.49", 0), ("0.51", 1), ("1.49", 1), ("1.51", 2)],
    )
    def it_accepts_fractional_twips(self, str_value: str, expected_twips: int):
        value = ST_TwipsMeasure.convert_from_xml(str_value)

        assert value == Twips(expected_twips)

    @pytest.mark.parametrize("str_value", ["120", "9007199254740993"])
    def it_preserves_exact_integer_twips(self, str_value: str):
        value = ST_TwipsMeasure.convert_from_xml(str_value)

        assert value == Twips(int(str_value))

    def it_preserves_unit_suffixed_measurements(self):
        value = ST_TwipsMeasure.convert_from_xml("1in")

        assert value == Inches(1)

    @pytest.mark.parametrize("str_value", ["not-a-number", "NaN", "Infinity", "-Infinity"])
    def it_rejects_invalid_or_non_finite_measurements(self, str_value: str):
        with pytest.raises((ValueError, OverflowError)):
            ST_TwipsMeasure.convert_from_xml(str_value)

    def it_serializes_measurements_as_integer_twips(self):
        str_value = ST_TwipsMeasure.convert_to_xml(Twips(42))

        assert str_value == "42"
