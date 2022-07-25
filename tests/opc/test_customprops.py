# encoding: utf-8

"""
Unit test suite for the docx.opc.customprops module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from datetime import datetime

from docx.opc.customprops import CustomProperties
from docx.oxml.customprops import CT_CustomProperties
from docx.oxml import parse_xml
from lxml import etree

class DescribeCustomProperties(object):

    def it_can_read_existing_prop_values(self, prop_get_fixture):
        custom_properties, prop_name, exp_value = prop_get_fixture
        actual_value = custom_properties[prop_name]
        assert actual_value == exp_value

    def it_can_change_existing_prop_values(self):
        pass

    def it_can_set_new_prop_values(self, prop_set_fixture):
        custom_properties, prop_name, value, exp_xml = prop_set_fixture
        custom_properties[prop_name] = value
        assert custom_properties._element.xml == exp_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('CustomPropString', 'Test String'),
        ('CustomPropBool',   True),
        ('CustomPropInt',    13),
        ('CustomPropFoo',    None),
    ])
    def prop_get_fixture(self, request, custom_properties_default):
        prop_name, expected_value = request.param
        return custom_properties_default, prop_name, expected_value

    @pytest.fixture(params=[
        ('CustomPropString',  'lpwstr',  'Hi there!',  'Hi there!'),
        ('CustomPropBool',    'bool',    '0',          False),
        ('CustomPropInt',     'i4',      '5',          5),
    ])
    def prop_set_fixture(self, request, custom_properties_blank):
        prop_name, str_type, str_value, value = request.param
        expected_xml = self.customProperties(prop_name, str_type, str_value)
        return custom_properties_blank, prop_name, value, expected_xml

    # fixture components ---------------------------------------------

    def customProperties(self, prop_name, str_type, str_value):
        tmpl = (
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/custom-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">\n'
            '  <property name="%s" fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="2">\n'
            '    <vt:%s>%s</vt:%s>\n'
            '  </property>\n'
            '</Properties>'
        )
        return tmpl %(prop_name, str_type, str_value, str_type)

    @pytest.fixture
    def custom_properties_blank(self):
        element = parse_xml(
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/custom-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
            '</Properties>\n'
        )
        return CustomProperties(element)

    @pytest.fixture
    def custom_properties_default(self):
        element = parse_xml(
            b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            b'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/custom-properties" '
            b'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">\n'
            b'  <property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="2" name="CustomPropBool"><vt:bool>1</vt:bool></property>\n'
            b'  <property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="3" name="CustomPropInt"><vt:i4>13</vt:i4></property>\n'
            b'  <property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="4" name="CustomPropString"><vt:lpwstr>Test String</vt:lpwstr></property>\n'
            b'</Properties>\n'
        )
        return CustomProperties(element)
