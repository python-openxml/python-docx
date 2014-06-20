# encoding: utf-8

"""
Test suite for the docx.section module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.enum.section import WD_SECTION
from docx.section import Section

from .oxml.unitdata.section import a_sectPr, a_type


class DescribeSection(object):

    def it_knows_its_start_type(self, start_type_get_fixture):
        section, expected_start_type = start_type_get_fixture
        assert section.start_type is expected_start_type

    def it_can_change_its_start_type(self, start_type_set_fixture):
        section, new_start_type, expected_xml = start_type_set_fixture
        section.start_type = new_start_type
        assert section._sectPr.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        (None,         WD_SECTION.NEW_PAGE),
        ('continuous', WD_SECTION.CONTINUOUS),
        ('nextPage',   WD_SECTION.NEW_PAGE),
        ('oddPage',    WD_SECTION.ODD_PAGE),
        ('evenPage',   WD_SECTION.EVEN_PAGE),
        ('nextColumn', WD_SECTION.NEW_COLUMN),
    ])
    def start_type_get_fixture(self, request):
        type_val, expected_start_type = request.param
        sectPr = self.sectPr_bldr(type_val).element
        section = Section(sectPr)
        return section, expected_start_type

    @pytest.fixture(params=[
        ('oddPage',    WD_SECTION.EVEN_PAGE,  'evenPage'),
        ('nextPage',   None,                  None),
        ('continuous', WD_SECTION.NEW_PAGE,   None),
        (None,         WD_SECTION.NEW_COLUMN, 'nextColumn'),
    ])
    def start_type_set_fixture(self, request):
        initial_type_val, new_type, expected_type_val = request.param
        sectPr = self.sectPr_bldr(initial_type_val).element
        section = Section(sectPr)
        expected_xml = self.sectPr_bldr(expected_type_val).xml()
        return section, new_type, expected_xml

    # fixture components ---------------------------------------------

    def sectPr_bldr(self, start_type=None):
        sectPr_bldr = a_sectPr().with_nsdecls()
        if start_type is not None:
            sectPr_bldr.with_child(
                a_type().with_val(start_type)
            )
        return sectPr_bldr
