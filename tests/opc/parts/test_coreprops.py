# encoding: utf-8

"""
Unit test suite for the docx.opc.parts.coreprops module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.opc.coreprops import CoreProperties
from docx.opc.parts.coreprops import CorePropertiesPart
from docx.oxml.parts.coreprops import CT_CoreProperties

from ...unitutil.mock import class_mock, instance_mock


class DescribeCorePropertiesPart(object):

    def it_provides_access_to_its_core_props_object(self, coreprops_fixture):
        core_properties_part, CoreProperties_ = coreprops_fixture
        core_properties = core_properties_part.core_properties
        CoreProperties_.assert_called_once_with(core_properties_part.element)
        assert isinstance(core_properties, CoreProperties)

    # fixtures ---------------------------------------------

    @pytest.fixture
    def coreprops_fixture(self, element_, CoreProperties_):
        core_properties_part = CorePropertiesPart(None, None, element_, None)
        return core_properties_part, CoreProperties_

    # fixture components -----------------------------------

    @pytest.fixture
    def CoreProperties_(self, request):
        return class_mock(request, 'docx.opc.parts.coreprops.CoreProperties')

    @pytest.fixture
    def element_(self, request):
        return instance_mock(request, CT_CoreProperties)
