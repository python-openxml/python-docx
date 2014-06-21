# encoding: utf-8

"""
Test suite for the docx.section module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.enum.section import WD_SECTION
from docx.section import Section
from docx.shared import Inches

from .oxml.unitdata.section import a_pgSz, a_sectPr, a_type


class DescribeSection(object):

    def it_knows_its_start_type(self, start_type_get_fixture):
        section, expected_start_type = start_type_get_fixture
        assert section.start_type is expected_start_type

    def it_can_change_its_start_type(self, start_type_set_fixture):
        section, new_start_type, expected_xml = start_type_set_fixture
        section.start_type = new_start_type
        assert section._sectPr.xml == expected_xml

    def it_knows_its_page_width(self, page_width_get_fixture):
        section, expected_page_width = page_width_get_fixture
        assert section.page_width == expected_page_width

    def it_can_change_its_page_width(self, page_width_set_fixture):
        section, new_page_width, expected_xml = page_width_set_fixture
        section.page_width = new_page_width

    def it_knows_its_page_height(self, page_height_get_fixture):
        section, expected_page_height = page_height_get_fixture
        assert section.page_height == expected_page_height

    def it_can_change_its_page_height(self, page_height_set_fixture):
        section, new_page_height, expected_xml = page_height_set_fixture
        section.page_height = new_page_height
        assert section._sectPr.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        (True,  2880, Inches(2)),
        (True,  None, None),
        (False, None, None),
    ])
    def page_height_get_fixture(self, request):
        has_pgSz_child, h, expected_page_height = request.param
        pgSz_bldr = self.pgSz_bldr(has_pgSz_child, h=h)
        sectPr = self.sectPr_bldr(pgSz_bldr).element
        section = Section(sectPr)
        return section, expected_page_height

    @pytest.fixture(params=[
        (None,      None),
        (Inches(2), 2880),
    ])
    def page_height_set_fixture(self, request):
        new_page_height, expected_h_val = request.param
        # section ----------------------
        sectPr = self.sectPr_bldr().element
        section = Section(sectPr)
        # expected_xml -----------------
        pgSz_bldr = self.pgSz_bldr(h=expected_h_val)
        expected_xml = self.sectPr_bldr(pgSz_bldr).xml()
        return section, new_page_height, expected_xml

    @pytest.fixture(params=[
        (True,  1440, Inches(1)),
        (True,  None, None),
        (False, None, None),
    ])
    def page_width_get_fixture(self, request):
        has_pgSz_child, w, expected_page_width = request.param
        pgSz_bldr = self.pgSz_bldr(has_pgSz_child, w=w)
        sectPr = self.sectPr_bldr(pgSz_bldr).element
        section = Section(sectPr)
        return section, expected_page_width

    @pytest.fixture(params=[
        (None,      None),
        (Inches(1), 1440),
    ])
    def page_width_set_fixture(self, request):
        new_page_width, expected_w_val = request.param
        # section ----------------------
        sectPr = self.sectPr_bldr().element
        section = Section(sectPr)
        # expected_xml -----------------
        pgSz_bldr = self.pgSz_bldr(w=expected_w_val)
        expected_xml = self.sectPr_bldr(pgSz_bldr).xml()
        return section, new_page_width, expected_xml

    @pytest.fixture(params=[
        (False, None,         WD_SECTION.NEW_PAGE),
        (True,  None,         WD_SECTION.NEW_PAGE),
        (True,  'continuous', WD_SECTION.CONTINUOUS),
        (True,  'nextPage',   WD_SECTION.NEW_PAGE),
        (True,  'oddPage',    WD_SECTION.ODD_PAGE),
        (True,  'evenPage',   WD_SECTION.EVEN_PAGE),
        (True,  'nextColumn', WD_SECTION.NEW_COLUMN),
    ])
    def start_type_get_fixture(self, request):
        has_type_child, type_val, expected_start_type = request.param
        type_bldr = self.type_bldr(has_type_child, type_val)
        sectPr = self.sectPr_bldr(type_bldr).element
        section = Section(sectPr)
        return section, expected_start_type

    @pytest.fixture(params=[
        (True,  'oddPage',    WD_SECTION.EVEN_PAGE,  True,  'evenPage'),
        (True,  'nextPage',   None,                  False, None),
        (False, None,         WD_SECTION.NEW_PAGE,   False, None),
        (True,  'continuous', WD_SECTION.NEW_PAGE,   False, None),
        (True,  None,         WD_SECTION.NEW_PAGE,   False, None),
        (True,  None,         WD_SECTION.NEW_COLUMN, True,  'nextColumn'),
    ])
    def start_type_set_fixture(self, request):
        (has_type_child, initial_type_val, new_type, has_type_child_after,
         expected_type_val) = request.param
        # section ----------------------
        type_bldr = self.type_bldr(has_type_child, initial_type_val)
        sectPr = self.sectPr_bldr(type_bldr).element
        section = Section(sectPr)
        # expected_xml -----------------
        type_bldr = self.type_bldr(has_type_child_after, expected_type_val)
        expected_xml = self.sectPr_bldr(type_bldr).xml()
        return section, new_type, expected_xml

    # fixture components ---------------------------------------------

    def pgSz_bldr(self, has_pgSz=True, w=None, h=None):
        if not has_pgSz:
            return None
        pgSz_bldr = a_pgSz()
        if w is not None:
            pgSz_bldr.with_w(w)
        if h is not None:
            pgSz_bldr.with_h(h)
        return pgSz_bldr

    def sectPr_bldr(self, *child_bldrs):
        sectPr_bldr = a_sectPr().with_nsdecls()
        for child_bldr in child_bldrs:
            if child_bldr is not None:
                sectPr_bldr.with_child(child_bldr)
        return sectPr_bldr

    def type_bldr(self, has_type_elm, val):
        if not has_type_elm:
            return None
        type_bldr = a_type()
        if val is not None:
            type_bldr.with_val(val)
        return type_bldr
