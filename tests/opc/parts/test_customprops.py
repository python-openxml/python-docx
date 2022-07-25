# encoding: utf-8

"""
Unit test suite for the docx.opc.parts.customprops module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from datetime import datetime, timedelta

import pytest

from docx.opc.customprops import CustomProperties
from docx.opc.parts.customprops import CustomPropertiesPart
from docx.oxml.customprops import CT_CustomProperties

from ...unitutil.mock import class_mock, instance_mock


class DescribeCustomPropertiesPart(object):

    def it_provides_access_to_its_custom_props_object(self, customprops_fixture):
        custom_properties_part, CustomProperties_ = customprops_fixture
        custom_properties = custom_properties_part.custom_properties
        CustomProperties_.assert_called_once_with(custom_properties_part.element)
        assert isinstance(custom_properties, CustomProperties)

    def it_can_create_a_default_custom_properties_part(self):
        custom_properties_part = CustomPropertiesPart.default(None)
        assert isinstance(custom_properties_part, CustomPropertiesPart)
        custom_properties = custom_properties_part.custom_properties
        assert len(custom_properties) == 0

    # fixtures ---------------------------------------------

    @pytest.fixture
    def customprops_fixture(self, element_, CustomProperties_):
        custom_properties_part = CustomPropertiesPart(None, None, element_, None)
        return custom_properties_part, CustomProperties_

    # fixture components -----------------------------------

    @pytest.fixture
    def CustomProperties_(self, request):
        return class_mock(request, 'docx.opc.parts.customprops.CustomProperties')

    @pytest.fixture
    def element_(self, request):
        return instance_mock(request, CT_CustomProperties)
