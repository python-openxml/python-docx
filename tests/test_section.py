# encoding: utf-8

"""
Test suite for the docx.section module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.section import Section, Sections
from docx.shared import Inches

from .unitutil.cxml import element, xml


class DescribeSections(object):

    def it_knows_how_many_sections_it_contains(self, len_fixture):
        sections, expected_len = len_fixture
        assert len(sections) == expected_len

    def it_can_iterate_over_its_Section_instances(self, iter_fixture):
        sections, expected_count = iter_fixture
        section_count = 0
        for section in sections:
            section_count += 1
            assert isinstance(section, Section)
        assert section_count == expected_count

    def it_can_access_its_Section_instances_by_index(self, index_fixture):
        sections, indicies = index_fixture
        assert len(sections[0:2]) == 2
        for index in indicies:
            assert isinstance(sections[index], Section)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def index_fixture(self, document_elm):
        sections = Sections(document_elm)
        return sections, [0, 1]

    @pytest.fixture
    def iter_fixture(self, document_elm):
        sections = Sections(document_elm)
        return sections, 2

    @pytest.fixture
    def len_fixture(self, document_elm):
        sections = Sections(document_elm)
        return sections, 2

    # fixture components ---------------------------------------------

    @pytest.fixture
    def document_elm(self):
        return element('w:document/w:body/(w:p/w:pPr/w:sectPr, w:sectPr)')


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
        section, margin_prop_name, expected_value = margins_get_fixture
        value = getattr(section, margin_prop_name)
        assert value == expected_value

    def it_can_change_its_page_margins(self, margins_set_fixture):
        section, margin_prop_name, new_value, expected_xml = (
            margins_set_fixture
        )
        setattr(section, margin_prop_name, new_value)
        assert section._sectPr.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('w:sectPr/w:pgMar{w:left=120}',   'left_margin',      76200),
        ('w:sectPr/w:pgMar{w:right=240}',  'right_margin',    152400),
        ('w:sectPr/w:pgMar{w:top=-360}',   'top_margin',     -228600),
        ('w:sectPr/w:pgMar{w:bottom=480}', 'bottom_margin',   304800),
        ('w:sectPr/w:pgMar{w:gutter=600}', 'gutter',          381000),
        ('w:sectPr/w:pgMar{w:header=720}', 'header_distance', 457200),
        ('w:sectPr/w:pgMar{w:footer=840}', 'footer_distance', 533400),
        ('w:sectPr/w:pgMar',               'left_margin',       None),
        ('w:sectPr',                       'top_margin',        None),
    ])
    def margins_get_fixture(self, request):
        sectPr_cxml, margin_prop_name, expected_value = request.param
        section = Section(element(sectPr_cxml))
        return section, margin_prop_name, expected_value

    @pytest.fixture(params=[
        ('w:sectPr', 'left_margin',     Inches(1),
         'w:sectPr/w:pgMar{w:left=1440}'),
        ('w:sectPr', 'right_margin',    Inches(0.5),
         'w:sectPr/w:pgMar{w:right=720}'),
        ('w:sectPr', 'top_margin',      Inches(-0.25),
         'w:sectPr/w:pgMar{w:top=-360}'),
        ('w:sectPr', 'bottom_margin',   Inches(0.75),
         'w:sectPr/w:pgMar{w:bottom=1080}'),
        ('w:sectPr', 'gutter',          Inches(0.25),
         'w:sectPr/w:pgMar{w:gutter=360}'),
        ('w:sectPr', 'header_distance', Inches(1.25),
         'w:sectPr/w:pgMar{w:header=1800}'),
        ('w:sectPr', 'footer_distance', Inches(1.35),
         'w:sectPr/w:pgMar{w:footer=1944}'),
        ('w:sectPr', 'left_margin', None, 'w:sectPr/w:pgMar'),
        ('w:sectPr/w:pgMar{w:top=-360}', 'top_margin', Inches(0.6),
         'w:sectPr/w:pgMar{w:top=864}'),
    ])
    def margins_set_fixture(self, request):
        sectPr_cxml, property_name, new_value, expected_cxml = request.param
        section = Section(element(sectPr_cxml))
        expected_xml = xml(expected_cxml)
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
