# encoding: utf-8

"""Unit test suite for the docx.section module"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.parts.document import DocumentPart
from docx.section import _Footer, Section, Sections
from docx.shared import Inches

from .unitutil.cxml import element, xml
from .unitutil.mock import call, class_mock, instance_mock


class DescribeSections(object):

    def it_knows_how_many_sections_it_contains(self):
        sections = Sections(
            element("w:document/w:body/(w:p/w:pPr/w:sectPr, w:sectPr)"), None
        )
        assert len(sections) == 2

    def it_can_iterate_over_its_Section_instances(
        self, Section_, section_, document_part_
    ):
        document_elm = element("w:document/w:body/(w:p/w:pPr/w:sectPr, w:sectPr)")
        sectPrs = document_elm.xpath("//w:sectPr")
        Section_.return_value = section_
        sections = Sections(document_elm, document_part_)

        section_lst = [s for s in sections]

        assert Section_.call_args_list == [
            call(sectPrs[0], document_part_), call(sectPrs[1], document_part_)
        ]
        assert section_lst == [section_, section_]

    def it_can_access_its_Section_instances_by_index(
        self, Section_, section_, document_part_
    ):
        document_elm = element(
            "w:document/w:body/(w:p/w:pPr/w:sectPr,w:p/w:pPr/w:sectPr,w:sectPr)"
        )
        sectPrs = document_elm.xpath("//w:sectPr")
        Section_.return_value = section_
        sections = Sections(document_elm, document_part_)

        section_lst = [sections[idx] for idx in range(3)]

        assert Section_.call_args_list == [
            call(sectPrs[0], document_part_),
            call(sectPrs[1], document_part_),
            call(sectPrs[2], document_part_),
        ]
        assert section_lst == [section_, section_, section_]

    def it_can_access_its_Section_instances_by_slice(
        self, Section_, section_, document_part_
    ):
        document_elm = element(
            "w:document/w:body/(w:p/w:pPr/w:sectPr,w:p/w:pPr/w:sectPr,w:sectPr)"
        )
        sectPrs = document_elm.xpath("//w:sectPr")
        Section_.return_value = section_
        sections = Sections(document_elm, document_part_)

        section_lst = sections[1:9]

        assert Section_.call_args_list == [
            call(sectPrs[1], document_part_), call(sectPrs[2], document_part_)
        ]
        assert section_lst == [section_, section_]

    # fixture components ---------------------------------------------

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def Section_(self, request):
        return class_mock(request, "docx.section.Section")

    @pytest.fixture
    def section_(self, request):
        return instance_mock(request, Section)


class DescribeSection(object):

    def it_provides_access_to_its_default_footer(
        self, document_part_, _Footer_, footer_
    ):
        sectPr = element('w:sectPr')
        _Footer_.return_value = footer_
        section = Section(sectPr, document_part_)

        footer = section.footer

        _Footer_.assert_called_once_with(sectPr, document_part_)
        assert footer is footer_

    def it_knows_its_start_type(self, start_type_get_fixture):
        sectPr, expected_start_type = start_type_get_fixture
        section = Section(sectPr, None)

        start_type = section.start_type

        assert start_type is expected_start_type

    def it_can_change_its_start_type(self, start_type_set_fixture):
        sectPr, new_start_type, expected_xml = start_type_set_fixture
        section = Section(sectPr, None)

        section.start_type = new_start_type

        assert section._sectPr.xml == expected_xml

    def it_knows_its_page_width(self, page_width_get_fixture):
        sectPr, expected_page_width = page_width_get_fixture
        section = Section(sectPr, None)

        page_width = section.page_width

        assert page_width == expected_page_width

    def it_can_change_its_page_width(self, page_width_set_fixture):
        sectPr, new_page_width, expected_xml = page_width_set_fixture
        section = Section(sectPr, None)

        section.page_width = new_page_width

        assert section._sectPr.xml == expected_xml

    def it_knows_its_page_height(self, page_height_get_fixture):
        sectPr, expected_page_height = page_height_get_fixture
        section = Section(sectPr, None)

        page_height = section.page_height

        assert page_height == expected_page_height

    def it_can_change_its_page_height(self, page_height_set_fixture):
        sectPr, new_page_height, expected_xml = page_height_set_fixture
        section = Section(sectPr, None)

        section.page_height = new_page_height

        assert section._sectPr.xml == expected_xml

    def it_knows_its_page_orientation(self, orientation_get_fixture):
        sectPr, expected_orientation = orientation_get_fixture
        section = Section(sectPr, None)

        orientation = section.orientation

        assert orientation is expected_orientation

    def it_can_change_its_orientation(self, orientation_set_fixture):
        sectPr, new_orientation, expected_xml = orientation_set_fixture
        section = Section(sectPr, None)

        section.orientation = new_orientation

        assert section._sectPr.xml == expected_xml

    def it_knows_its_page_margins(self, margins_get_fixture):
        sectPr, margin_prop_name, expected_value = margins_get_fixture
        section = Section(sectPr, None)

        value = getattr(section, margin_prop_name)

        assert value == expected_value

    def it_can_change_its_page_margins(self, margins_set_fixture):
        sectPr, margin_prop_name, new_value, expected_xml = margins_set_fixture
        section = Section(sectPr, None)

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
        sectPr = element(sectPr_cxml)
        return sectPr, margin_prop_name, expected_value

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
        sectPr = element(sectPr_cxml)
        expected_xml = xml(expected_cxml)
        return sectPr, property_name, new_value, expected_xml

    @pytest.fixture(params=[
        ('w:sectPr/w:pgSz{w:orient=landscape}', WD_ORIENT.LANDSCAPE),
        ('w:sectPr/w:pgSz{w:orient=portrait}',  WD_ORIENT.PORTRAIT),
        ('w:sectPr/w:pgSz',                     WD_ORIENT.PORTRAIT),
        ('w:sectPr',                            WD_ORIENT.PORTRAIT),
    ])
    def orientation_get_fixture(self, request):
        sectPr_cxml, expected_orientation = request.param
        sectPr = element(sectPr_cxml)
        return sectPr, expected_orientation

    @pytest.fixture(params=[
        (WD_ORIENT.LANDSCAPE, 'w:sectPr/w:pgSz{w:orient=landscape}'),
        (WD_ORIENT.PORTRAIT,  'w:sectPr/w:pgSz'),
        (None,                'w:sectPr/w:pgSz'),
    ])
    def orientation_set_fixture(self, request):
        new_orientation, expected_cxml = request.param
        sectPr = element('w:sectPr')
        expected_xml = xml(expected_cxml)
        return sectPr, new_orientation, expected_xml

    @pytest.fixture(params=[
        ('w:sectPr/w:pgSz{w:h=2880}', Inches(2)),
        ('w:sectPr/w:pgSz',           None),
        ('w:sectPr',                  None),
    ])
    def page_height_get_fixture(self, request):
        sectPr_cxml, expected_page_height = request.param
        sectPr = element(sectPr_cxml)
        return sectPr, expected_page_height

    @pytest.fixture(params=[
        (None,      'w:sectPr/w:pgSz'),
        (Inches(2), 'w:sectPr/w:pgSz{w:h=2880}'),
    ])
    def page_height_set_fixture(self, request):
        new_page_height, expected_cxml = request.param
        sectPr = element('w:sectPr')
        expected_xml = xml(expected_cxml)
        return sectPr, new_page_height, expected_xml

    @pytest.fixture(params=[
        ('w:sectPr/w:pgSz{w:w=1440}', Inches(1)),
        ('w:sectPr/w:pgSz',           None),
        ('w:sectPr',                  None),
    ])
    def page_width_get_fixture(self, request):
        sectPr_cxml, expected_page_width = request.param
        sectPr = element(sectPr_cxml)
        return sectPr, expected_page_width

    @pytest.fixture(params=[
        (None,      'w:sectPr/w:pgSz'),
        (Inches(4), 'w:sectPr/w:pgSz{w:w=5760}'),
    ])
    def page_width_set_fixture(self, request):
        new_page_width, expected_cxml = request.param
        sectPr = element('w:sectPr')
        expected_xml = xml(expected_cxml)
        return sectPr, new_page_width, expected_xml

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
        sectPr = element(sectPr_cxml)
        return sectPr, expected_start_type

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
        sectPr = element(initial_cxml)
        expected_xml = xml(expected_cxml)
        return sectPr, new_start_type, expected_xml

    # fixture components ---------------------------------------------

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def _Footer_(self, request):
        return class_mock(request, "docx.section._Footer")

    @pytest.fixture
    def footer_(self, request):
        return instance_mock(request, _Footer)
