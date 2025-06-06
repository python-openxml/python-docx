# pyright: reportPrivateUsage=false

"""Unit test suite for the docx.settings module."""

from __future__ import annotations

import pytest

from docx.settings import Settings

from .unitutil.cxml import element, xml


class DescribeSettings:
    """Unit-test suite for the `docx.settings.Settings` objects."""

    @pytest.mark.parametrize(
        ("cxml", "expected_value"),
        [
            ("w:settings", False),
            ("w:settings/w:evenAndOddHeaders", True),
            ("w:settings/w:evenAndOddHeaders{w:val=0}", False),
            ("w:settings/w:evenAndOddHeaders{w:val=1}", True),
            ("w:settings/w:evenAndOddHeaders{w:val=true}", True),
        ],
    )
    def it_knows_when_the_document_has_distinct_odd_and_even_headers(
        self, cxml: str, expected_value: bool
    ):
        assert Settings(element(cxml)).odd_and_even_pages_header_footer is expected_value

    @pytest.mark.parametrize(
        ("cxml", "new_value", "expected_cxml"),
        [
            ("w:settings", True, "w:settings/w:evenAndOddHeaders"),
            ("w:settings/w:evenAndOddHeaders", False, "w:settings"),
            ("w:settings/w:evenAndOddHeaders{w:val=1}", True, "w:settings/w:evenAndOddHeaders"),
            ("w:settings/w:evenAndOddHeaders{w:val=off}", False, "w:settings"),
        ],
    )
    def it_can_change_whether_the_document_has_distinct_odd_and_even_headers(
        self, cxml: str, new_value: bool, expected_cxml: str
    ):
        settings = Settings(element(cxml))

        settings.odd_and_even_pages_header_footer = new_value

        assert settings._settings.xml == xml(expected_cxml)
