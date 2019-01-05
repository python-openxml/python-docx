# encoding: utf-8

"""Unit test suite for the docx.settings module"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from docx.settings import Settings

from .unitutil.cxml import element


class DescribeSettings(object):

    def it_knows_when_the_document_has_distinct_odd_and_even_headers(
        self, odd_and_even_get_fixture
    ):
        settings_elm, expected_value = odd_and_even_get_fixture
        settings = Settings(settings_elm)

        odd_and_even_pages_header_footer = settings.odd_and_even_pages_header_footer

        assert odd_and_even_pages_header_footer is expected_value

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            ("w:settings", False),
            ("w:settings/w:evenAndOddHeaders", True),
            ("w:settings/w:evenAndOddHeaders{w:val=0}", False),
            ("w:settings/w:evenAndOddHeaders{w:val=1}", True),
            ("w:settings/w:evenAndOddHeaders{w:val=true}", True),
        ]
    )
    def odd_and_even_get_fixture(self, request):
        settings_cxml, expected_value = request.param
        settings_elm = element(settings_cxml)
        return settings_elm, expected_value
