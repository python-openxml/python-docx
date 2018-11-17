# encoding: utf-8

"""
Test suite for the docx.oxml.styles module.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from ..unitutil.cxml import element, xml


class DescribeCT_Settings(object):

    def it_can_add_evenOrOddHeaders_val(self, add_evenOrOddHeaders_val_fixture):
        settings, expected_xml = add_evenOrOddHeaders_val_fixture
        settings.evenOrOddHeaders_val = True
        assert settings.xml == expected_xml

    def it_can_remove_evenOrOddHeaders_val(self, remove_evenOrOddHeaders_val_fixture):
        settings, expected_xml = remove_evenOrOddHeaders_val_fixture
        settings.evenOrOddHeaders_val = False
        assert settings.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('w:settings',
         'w:settings/w:evenAndOddHeaders'),
    ])
    def add_evenOrOddHeaders_val_fixture(self, request):
        settings_cxml, expected_cxml = request.param
        settings = element(settings_cxml)
        expected_xml = xml(expected_cxml)
        return settings, expected_xml

    @pytest.fixture(params=[
        ('w:settings/w:evenAndOddHeaders{w:val=1}',
         'w:settings'),
    ])
    def remove_evenOrOddHeaders_val_fixture(self, request):
        settings_cxml, expected_cxml = request.param
        settings = element(settings_cxml)
        expected_xml = xml(expected_cxml)
        return settings, expected_xml