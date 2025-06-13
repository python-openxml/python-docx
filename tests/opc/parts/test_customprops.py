# encoding: utf-8

"""
Unit test suite for the docx.opc.parts.customprops module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.opc.customprops import CustomProperties
from docx.opc.parts.customprops import CustomPropertiesPart
from docx.oxml.customprops import CT_CustomProperties

from tests.unitutil.mock import class_mock, instance_mock


class DescribeCustomPropertiesPart(object):

    def it_provides_access_to_its_custom_props_object(self, element_, mock_custom_properties_):
        custom_properties_part = CustomPropertiesPart(None, None, element_, None)
        custom_properties = custom_properties_part.custom_properties
        mock_custom_properties_.assert_called_once_with(custom_properties_part.element)
        assert isinstance(custom_properties, CustomProperties)

    def it_can_create_a_default_custom_properties_part(self):
        custom_properties_part = CustomPropertiesPart.default(None)
        assert isinstance(custom_properties_part, CustomPropertiesPart)
        custom_properties = custom_properties_part.custom_properties
        assert len(custom_properties) == 0

    # fixtures ---------------------------------------------

    @pytest.fixture
    def mock_custom_properties_(self, request):
        return class_mock(request, 'docx.opc.parts.customprops.CustomProperties')

    @pytest.fixture
    def element_(self, request):
        return instance_mock(request, CT_CustomProperties)
