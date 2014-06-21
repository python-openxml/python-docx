# encoding: utf-8

"""
Test suite for the docx.section module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.section import Section
from docx.shared import Inches

from .oxml.unitdata.section import a_pgMar, a_pgSz, a_sectPr, a_type


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

    def it_knows_its_page_orientation(self, orientation_get_fixture):
        section, expected_orientation = orientation_get_fixture
        assert section.orientation is expected_orientation

    def it_can_change_its_orientation(self, orientation_set_fixture):
        section, new_orientation, expected_xml = orientation_set_fixture
        section.orientation = new_orientation
        assert section._sectPr.xml == expected_xml

    def it_knows_its_page_margins(self, margins_get_fixture):
        section, left, right, top, bottom, gutter, header, footer = (
            margins_get_fixture
        )
        assert section.left_margin == left
        assert section.right_margin == right
        assert section.top_margin == top
        assert section.bottom_margin == bottom
        assert section.gutter == gutter
        assert section.header_distance == header
        assert section.footer_distance == footer

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        (True,   720,  720,  720,  720,  720,  720,  720),
        (True,  None,  360, None,  360, None,  360, None),
        (False, None, None, None, None, None, None, None),
    ])
    def margins_get_fixture(self, request):
        (has_pgMar_child, left, right, top, bottom, gutter, header,
         footer) = request.param
        pgMar_bldr = self.pgMar_bldr(
            has_pgMar_child, left=left, right=right, top=top, bottom=bottom,
            gutter=gutter, header=header, footer=footer
        )
        sectPr = self.sectPr_bldr(pgMar_bldr).element
        section = Section(sectPr)
        expected_left = left * 635 if left else None
        expected_right = right * 635 if right else None
        expected_top = top * 635 if top else None
        expected_bottom = bottom * 635 if bottom else None
        expected_gutter = gutter * 635 if gutter else None
        expected_header = header * 635 if header else None
        expected_footer = footer * 635 if footer else None
        return (
            section, expected_left, expected_right, expected_top,
            expected_bottom, expected_gutter, expected_header,
            expected_footer
        )

    @pytest.fixture(params=[
        (True,  'landscape', WD_ORIENT.LANDSCAPE),
        (True,  'portrait',  WD_ORIENT.PORTRAIT),
        (True,  None,        WD_ORIENT.PORTRAIT),
        (False, None,        WD_ORIENT.PORTRAIT),
    ])
    def orientation_get_fixture(self, request):
        has_pgSz_child, orient, expected_orientation = request.param
        pgSz_bldr = self.pgSz_bldr(has_pgSz_child, orient=orient)
        sectPr = self.sectPr_bldr(pgSz_bldr).element
        section = Section(sectPr)
        return section, expected_orientation

    @pytest.fixture(params=[
        (WD_ORIENT.LANDSCAPE, 'landscape'),
        (WD_ORIENT.PORTRAIT,  None),
        (None,                None),
    ])
    def orientation_set_fixture(self, request):
        new_orientation, expected_orient_val = request.param
        # section ----------------------
        sectPr = self.sectPr_bldr().element
        section = Section(sectPr)
        # expected_xml -----------------
        pgSz_bldr = self.pgSz_bldr(orient=expected_orient_val)
        expected_xml = self.sectPr_bldr(pgSz_bldr).xml()
        return section, new_orientation, expected_xml

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

    def pgMar_bldr(
            self, has_pgMar=True, left=None, right=None, top=None,
            bottom=None, header=None, footer=None, gutter=None):
        if not has_pgMar:
            return None
        pgMar_bldr = a_pgMar()
        if left is not None:
            pgMar_bldr.with_left(left)
        if right is not None:
            pgMar_bldr.with_right(right)
        if top is not None:
            pgMar_bldr.with_top(top)
        if bottom is not None:
            pgMar_bldr.with_bottom(bottom)
        if header is not None:
            pgMar_bldr.with_header(header)
        if footer is not None:
            pgMar_bldr.with_footer(footer)
        if gutter is not None:
            pgMar_bldr.with_gutter(gutter)
        return pgMar_bldr

    def pgSz_bldr(self, has_pgSz=True, w=None, h=None, orient=None):
        if not has_pgSz:
            return None
        pgSz_bldr = a_pgSz()
        if w is not None:
            pgSz_bldr.with_w(w)
        if h is not None:
            pgSz_bldr.with_h(h)
        if orient is not None:
            pgSz_bldr.with_orient(orient)
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
