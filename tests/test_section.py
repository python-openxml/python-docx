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

    def it_knows_its_start_type(self, start_type_fixture):
        section, expected_start_type = start_type_fixture
        assert section.start_type is expected_start_type

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        (None,         WD_SECTION.NEW_PAGE),
        ('continuous', WD_SECTION.CONTINUOUS),
        ('nextPage',   WD_SECTION.NEW_PAGE),
        ('oddPage',    WD_SECTION.ODD_PAGE),
        ('evenPage',   WD_SECTION.EVEN_PAGE),
        ('nextColumn', WD_SECTION.NEW_COLUMN),
    ])
    def start_type_fixture(self, request):
        type_val, expected_start_type = request.param
        sectPr_bldr = a_sectPr().with_nsdecls()
        if type_val is not None:
            sectPr_bldr.with_child(a_type().with_val(type_val))
        sectPr = sectPr_bldr.element
        section = Section(sectPr)
        return section, expected_start_type
