# encoding: utf-8

"""
Test suite for the docx.settings module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.settings import Settings

from .unitutil.cxml import element, xml


class DescribeSettings(object):

    def it_can_remove_odd_and_even_pages_header_footer(self, remove_even_and_odd_headers_fixture):
        settings, expected_xml = remove_even_and_odd_headers_fixture
        settings.odd_and_even_pages_header_footer = False
        assert settings._element.xml == expected_xml

    def it_can_add_odd_and_even_pages_header_footer(self, add_even_and_odd_headers_fixture):
        settings, expected_xml = add_even_and_odd_headers_fixture
        settings.odd_and_even_pages_header_footer = True
        assert settings._element.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('w:settings/w:evenAndOddHeaders{w:val=1}',
         'w:settings'),
    ])
    def remove_even_and_odd_headers_fixture(self, request):
        initial_cxml, expected_cxml = request.param
        settings = Settings(element(initial_cxml))
        expected_xml = xml(expected_cxml)
        return settings, expected_xml

    @pytest.fixture(params=[
        ('w:settings',
         'w:settings/w:evenAndOddHeaders'),
    ])
    def add_even_and_odd_headers_fixture(self, request):
        initial_cxml, expected_cxml = request.param
        settings = Settings(element(initial_cxml))
        expected_xml = xml(expected_cxml)
        return settings, expected_xml