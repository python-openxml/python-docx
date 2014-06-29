# encoding: utf-8

"""
Test suite for the docx.section module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.section import Section
from docx.shared import Inches

from .oxml.unitdata.section import a_pgMar, a_sectPr
from .unitutil.cxml import element, xml


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
        assert section._sectPr.xml == expected_xml

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

    def it_can_change_its_page_margins(self, margins_set_fixture):
        section, margin_prop_name, new_value, expected_xml = (
            margins_set_fixture
        )
        print(section._sectPr.xml)
        setattr(section, margin_prop_name, new_value)
        print(section._sectPr.xml)
        assert section._sectPr.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        (True,   720,  720,  720,  720,  720,  720,  720),
        (True,  None,  360, None,  360, None,  360, None),
        (False, None, None, None, None, None, None, None),
    ])
    def margins_get_fixture(self, request):
        (has_pgMar_child, left, right, top, bottom, gutter, header,
         footer) = request.param
        pgMar_bldr = self.pgMar_bldr(**{
            'has_pgMar': has_pgMar_child, 'left': left, 'right': right,
            'top': top, 'bottom': bottom, 'gutter': gutter, 'header': header,
            'footer': footer
        })
        sectPr = self.sectPr_bldr(pgMar_bldr).element
        section = Section(sectPr)
        expected_left = self.twips_to_emu(left)
        expected_right = self.twips_to_emu(right)
        expected_top = self.twips_to_emu(top)
        expected_bottom = self.twips_to_emu(bottom)
        expected_gutter = self.twips_to_emu(gutter)
        expected_header = self.twips_to_emu(header)
        expected_footer = self.twips_to_emu(footer)
        return (
            section, expected_left, expected_right, expected_top,
            expected_bottom, expected_gutter, expected_header,
            expected_footer
        )

    @pytest.fixture(params=[
        ('left', 1440, 720), ('right', None, 1800), ('top', 2160, None),
        ('bottom', 720, 2160), ('gutter', None, 360), ('header', 720, 630),
        ('footer', None, 810)
    ])
    def margins_set_fixture(self, request):
        margin_side, initial_margin, new_margin = request.param
        # section ----------------------
        pgMar_bldr = self.pgMar_bldr(**{margin_side: initial_margin})
        sectPr = self.sectPr_bldr(pgMar_bldr).element
        section = Section(sectPr)
        # property name ----------------
        property_name = {
            'left': 'left_margin', 'right': 'right_margin',
            'top': 'top_margin', 'bottom': 'bottom_margin',
            'gutter': 'gutter', 'header': 'header_distance',
            'footer': 'footer_distance'
        }[margin_side]
        # expected_xml -----------------
        pgMar_bldr = self.pgMar_bldr(**{margin_side: new_margin})
        expected_xml = self.sectPr_bldr(pgMar_bldr).xml()
        new_value = self.twips_to_emu(new_margin)
        return section, property_name, new_value, expected_xml

    @pytest.fixture(params=[
        ('w:sectPr/w:pgSz{w:orient=landscape}', WD_ORIENT.LANDSCAPE),
        ('w:sectPr/w:pgSz{w:orient=portrait}',  WD_ORIENT.PORTRAIT),
        ('w:sectPr/w:pgSz',                     WD_ORIENT.PORTRAIT),
        ('w:sectPr',                            WD_ORIENT.PORTRAIT),
    ])
    def orientation_get_fixture(self, request):
        sectPr_cxml, expected_orientation = request.param
        section = Section(element(sectPr_cxml))
        return section, expected_orientation

    @pytest.fixture(params=[
        (WD_ORIENT.LANDSCAPE, 'w:sectPr/w:pgSz{w:orient=landscape}'),
        (WD_ORIENT.PORTRAIT,  'w:sectPr/w:pgSz'),
        (None,                'w:sectPr/w:pgSz'),
    ])
    def orientation_set_fixture(self, request):
        new_orientation, expected_cxml = request.param
        section = Section(element('w:sectPr'))
        expected_xml = xml(expected_cxml)
        return section, new_orientation, expected_xml

    @pytest.fixture(params=[
        ('w:sectPr/w:pgSz{w:h=2880}', Inches(2)),
        ('w:sectPr/w:pgSz',           None),
        ('w:sectPr',                  None),
    ])
    def page_height_get_fixture(self, request):
        sectPr_cxml, expected_page_height = request.param
        section = Section(element(sectPr_cxml))
        return section, expected_page_height

    @pytest.fixture(params=[
        (None,      'w:sectPr/w:pgSz'),
        (Inches(2), 'w:sectPr/w:pgSz{w:h=2880}'),
    ])
    def page_height_set_fixture(self, request):
        new_page_height, expected_cxml = request.param
        section = Section(element('w:sectPr'))
        expected_xml = xml(expected_cxml)
        return section, new_page_height, expected_xml

    @pytest.fixture(params=[
        ('w:sectPr/w:pgSz{w:w=1440}', Inches(1)),
        ('w:sectPr/w:pgSz',           None),
        ('w:sectPr',                  None),
    ])
    def page_width_get_fixture(self, request):
        sectPr_cxml, expected_page_width = request.param
        section = Section(element(sectPr_cxml))
        return section, expected_page_width

    @pytest.fixture(params=[
        (None,      'w:sectPr/w:pgSz'),
        (Inches(4), 'w:sectPr/w:pgSz{w:w=5760}'),
    ])
    def page_width_set_fixture(self, request):
        new_page_width, expected_cxml = request.param
        section = Section(element('w:sectPr'))
        expected_xml = xml(expected_cxml)
        return section, new_page_width, expected_xml

    @pytest.fixture(params=[
        ('w:sectPr',                          WD_SECTION.NEW_PAGE),
        ('w:sectPr/w:type',                   WD_SECTION.NEW_PAGE),
        ('w:sectPr/w:type{w:val=continuous}', WD_SECTION.CONTINUOUS),
        ('w:sectPr/w:type{w:val=nextPage}',   WD_SECTION.NEW_PAGE),
        ('w:sectPr/w:type{w:val=oddPage}',    WD_SECTION.ODD_PAGE),
        ('w:sectPr/w:type{w:val=evenPage}',   WD_SECTION.EVEN_PAGE),
        ('w:sectPr/w:type{w:val=nextColumn}', WD_SECTION.NEW_COLUMN),
    ])
    def start_type_get_fixture(self, request):
        sectPr_cxml, expected_start_type = request.param
        section = Section(element(sectPr_cxml))
        return section, expected_start_type

    @pytest.fixture(params=[
        ('w:sectPr/w:type{w:val=oddPage}',    WD_SECTION.EVEN_PAGE,
         'w:sectPr/w:type{w:val=evenPage}'),
        ('w:sectPr/w:type{w:val=nextPage}',   None,
         'w:sectPr'),
        ('w:sectPr',                          None,
         'w:sectPr'),
        ('w:sectPr/w:type{w:val=continuous}', WD_SECTION.NEW_PAGE,
         'w:sectPr'),
        ('w:sectPr/w:type',                   WD_SECTION.NEW_PAGE,
         'w:sectPr'),
        ('w:sectPr/w:type',                   WD_SECTION.NEW_COLUMN,
         'w:sectPr/w:type{w:val=nextColumn}'),
    ])
    def start_type_set_fixture(self, request):
        initial_cxml, new_start_type, expected_cxml = request.param
        section = Section(element(initial_cxml))
        expected_xml = xml(expected_cxml)
        return section, new_start_type, expected_xml

    # fixture components ---------------------------------------------

    @staticmethod
    def twips_to_emu(twips):
        if twips is None:
            return None
        return twips * 635

    def pgMar_bldr(self, **kwargs):
        if kwargs.pop('has_pgMar', True) is False:
            return None
        pgMar_bldr = a_pgMar()
        for key, value in kwargs.items():
            if value is None:
                continue
            set_attr_method = getattr(pgMar_bldr, 'with_%s' % key)
            set_attr_method(value)
        return pgMar_bldr

    def sectPr_bldr(self, *child_bldrs):
        sectPr_bldr = a_sectPr().with_nsdecls()
        for child_bldr in child_bldrs:
            if child_bldr is not None:
                sectPr_bldr.with_child(child_bldr)
        return sectPr_bldr
