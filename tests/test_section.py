# encoding: utf-8

"""Unit test suite for the docx.section module"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from docx.enum.section import WD_HEADER_FOOTER, WD_ORIENT, WD_SECTION
from docx.parts.document import DocumentPart
from docx.parts.hdrftr import FooterPart, HeaderPart
from docx.section import _BaseHeaderFooter, _Footer, _Header, Section, Sections
from docx.shared import Inches

from .unitutil.cxml import element, xml
from .unitutil.mock import call, class_mock, instance_mock, method_mock, property_mock


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
            call(sectPrs[0], document_part_),
            call(sectPrs[1], document_part_),
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
            call(sectPrs[1], document_part_),
            call(sectPrs[2], document_part_),
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
    def it_knows_when_it_displays_a_distinct_first_page_header(
        self, diff_first_header_get_fixture
    ):
        sectPr, expected_value = diff_first_header_get_fixture
        section = Section(sectPr, None)

        different_first_page_header_footer = section.different_first_page_header_footer

        assert different_first_page_header_footer is expected_value

    def it_can_change_whether_the_document_has_distinct_odd_and_even_headers(
        self, diff_first_header_set_fixture
    ):
        sectPr, value, expected_xml = diff_first_header_set_fixture
        section = Section(sectPr, None)

        section.different_first_page_header_footer = value

        assert sectPr.xml == expected_xml

    def it_provides_access_to_its_even_page_footer(
        self, document_part_, _Footer_, footer_
    ):
        sectPr = element("w:sectPr")
        _Footer_.return_value = footer_
        section = Section(sectPr, document_part_)

        footer = section.even_page_footer

        _Footer_.assert_called_once_with(
            sectPr, document_part_, WD_HEADER_FOOTER.EVEN_PAGE
        )
        assert footer is footer_

    def it_provides_access_to_its_even_page_header(
        self, document_part_, _Header_, header_
    ):
        sectPr = element("w:sectPr")
        _Header_.return_value = header_
        section = Section(sectPr, document_part_)

        header = section.even_page_header

        _Header_.assert_called_once_with(
            sectPr, document_part_, WD_HEADER_FOOTER.EVEN_PAGE
        )
        assert header is header_

    def it_provides_access_to_its_first_page_footer(
        self, document_part_, _Footer_, footer_
    ):
        sectPr = element("w:sectPr")
        _Footer_.return_value = footer_
        section = Section(sectPr, document_part_)

        footer = section.first_page_footer

        _Footer_.assert_called_once_with(
            sectPr, document_part_, WD_HEADER_FOOTER.FIRST_PAGE
        )
        assert footer is footer_

    def it_provides_access_to_its_first_page_header(
        self, document_part_, _Header_, header_
    ):
        sectPr = element("w:sectPr")
        _Header_.return_value = header_
        section = Section(sectPr, document_part_)

        header = section.first_page_header

        _Header_.assert_called_once_with(
            sectPr, document_part_, WD_HEADER_FOOTER.FIRST_PAGE
        )
        assert header is header_

    def it_provides_access_to_its_default_footer(
        self, document_part_, _Footer_, footer_
    ):
        sectPr = element("w:sectPr")
        _Footer_.return_value = footer_
        section = Section(sectPr, document_part_)

        footer = section.footer

        _Footer_.assert_called_once_with(
            sectPr, document_part_, WD_HEADER_FOOTER.PRIMARY
        )
        assert footer is footer_

    def it_provides_access_to_its_default_header(
        self, document_part_, _Header_, header_
    ):
        sectPr = element("w:sectPr")
        _Header_.return_value = header_
        section = Section(sectPr, document_part_)

        header = section.header

        _Header_.assert_called_once_with(
            sectPr, document_part_, WD_HEADER_FOOTER.PRIMARY
        )
        assert header is header_

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

    @pytest.fixture(
        params=[
            ("w:sectPr", False),
            ("w:sectPr/w:titlePg", True),
            ("w:sectPr/w:titlePg{w:val=0}", False),
            ("w:sectPr/w:titlePg{w:val=1}", True),
            ("w:sectPr/w:titlePg{w:val=true}", True),
        ]
    )
    def diff_first_header_get_fixture(self, request):
        sectPr_cxml, expected_value = request.param
        sectPr = element(sectPr_cxml)
        return sectPr, expected_value

    @pytest.fixture(
        params=[
            ("w:sectPr", True, "w:sectPr/w:titlePg"),
            ("w:sectPr/w:titlePg", False, "w:sectPr"),
            ("w:sectPr/w:titlePg{w:val=1}", True, "w:sectPr/w:titlePg"),
            ("w:sectPr/w:titlePg{w:val=off}", False, "w:sectPr"),
        ]
    )
    def diff_first_header_set_fixture(self, request):
        sectPr_cxml, value, expected_cxml = request.param
        sectPr = element(sectPr_cxml)
        expected_xml = xml(expected_cxml)
        return sectPr, value, expected_xml

    @pytest.fixture(
        params=[
            ("w:sectPr/w:pgMar{w:left=120}", "left_margin", 76200),
            ("w:sectPr/w:pgMar{w:right=240}", "right_margin", 152400),
            ("w:sectPr/w:pgMar{w:top=-360}", "top_margin", -228600),
            ("w:sectPr/w:pgMar{w:bottom=480}", "bottom_margin", 304800),
            ("w:sectPr/w:pgMar{w:gutter=600}", "gutter", 381000),
            ("w:sectPr/w:pgMar{w:header=720}", "header_distance", 457200),
            ("w:sectPr/w:pgMar{w:footer=840}", "footer_distance", 533400),
            ("w:sectPr/w:pgMar", "left_margin", None),
            ("w:sectPr", "top_margin", None),
        ]
    )
    def margins_get_fixture(self, request):
        sectPr_cxml, margin_prop_name, expected_value = request.param
        sectPr = element(sectPr_cxml)
        return sectPr, margin_prop_name, expected_value

    @pytest.fixture(
        params=[
            ("w:sectPr", "left_margin", Inches(1), "w:sectPr/w:pgMar{w:left=1440}"),
            ("w:sectPr", "right_margin", Inches(0.5), "w:sectPr/w:pgMar{w:right=720}"),
            ("w:sectPr", "top_margin", Inches(-0.25), "w:sectPr/w:pgMar{w:top=-360}"),
            (
                "w:sectPr",
                "bottom_margin",
                Inches(0.75),
                "w:sectPr/w:pgMar{w:bottom=1080}",
            ),
            ("w:sectPr", "gutter", Inches(0.25), "w:sectPr/w:pgMar{w:gutter=360}"),
            (
                "w:sectPr",
                "header_distance",
                Inches(1.25),
                "w:sectPr/w:pgMar{w:header=1800}",
            ),
            (
                "w:sectPr",
                "footer_distance",
                Inches(1.35),
                "w:sectPr/w:pgMar{w:footer=1944}",
            ),
            ("w:sectPr", "left_margin", None, "w:sectPr/w:pgMar"),
            (
                "w:sectPr/w:pgMar{w:top=-360}",
                "top_margin",
                Inches(0.6),
                "w:sectPr/w:pgMar{w:top=864}",
            ),
        ]
    )
    def margins_set_fixture(self, request):
        sectPr_cxml, property_name, new_value, expected_cxml = request.param
        sectPr = element(sectPr_cxml)
        expected_xml = xml(expected_cxml)
        return sectPr, property_name, new_value, expected_xml

    @pytest.fixture(
        params=[
            ("w:sectPr/w:pgSz{w:orient=landscape}", WD_ORIENT.LANDSCAPE),
            ("w:sectPr/w:pgSz{w:orient=portrait}", WD_ORIENT.PORTRAIT),
            ("w:sectPr/w:pgSz", WD_ORIENT.PORTRAIT),
            ("w:sectPr", WD_ORIENT.PORTRAIT),
        ]
    )
    def orientation_get_fixture(self, request):
        sectPr_cxml, expected_orientation = request.param
        sectPr = element(sectPr_cxml)
        return sectPr, expected_orientation

    @pytest.fixture(
        params=[
            (WD_ORIENT.LANDSCAPE, "w:sectPr/w:pgSz{w:orient=landscape}"),
            (WD_ORIENT.PORTRAIT, "w:sectPr/w:pgSz"),
            (None, "w:sectPr/w:pgSz"),
        ]
    )
    def orientation_set_fixture(self, request):
        new_orientation, expected_cxml = request.param
        sectPr = element("w:sectPr")
        expected_xml = xml(expected_cxml)
        return sectPr, new_orientation, expected_xml

    @pytest.fixture(
        params=[
            ("w:sectPr/w:pgSz{w:h=2880}", Inches(2)),
            ("w:sectPr/w:pgSz", None),
            ("w:sectPr", None),
        ]
    )
    def page_height_get_fixture(self, request):
        sectPr_cxml, expected_page_height = request.param
        sectPr = element(sectPr_cxml)
        return sectPr, expected_page_height

    @pytest.fixture(
        params=[
            (None, "w:sectPr/w:pgSz"),
            (Inches(2), "w:sectPr/w:pgSz{w:h=2880}"),
        ]
    )
    def page_height_set_fixture(self, request):
        new_page_height, expected_cxml = request.param
        sectPr = element("w:sectPr")
        expected_xml = xml(expected_cxml)
        return sectPr, new_page_height, expected_xml

    @pytest.fixture(
        params=[
            ("w:sectPr/w:pgSz{w:w=1440}", Inches(1)),
            ("w:sectPr/w:pgSz", None),
            ("w:sectPr", None),
        ]
    )
    def page_width_get_fixture(self, request):
        sectPr_cxml, expected_page_width = request.param
        sectPr = element(sectPr_cxml)
        return sectPr, expected_page_width

    @pytest.fixture(
        params=[
            (None, "w:sectPr/w:pgSz"),
            (Inches(4), "w:sectPr/w:pgSz{w:w=5760}"),
        ]
    )
    def page_width_set_fixture(self, request):
        new_page_width, expected_cxml = request.param
        sectPr = element("w:sectPr")
        expected_xml = xml(expected_cxml)
        return sectPr, new_page_width, expected_xml

    @pytest.fixture(
        params=[
            ("w:sectPr", WD_SECTION.NEW_PAGE),
            ("w:sectPr/w:type", WD_SECTION.NEW_PAGE),
            ("w:sectPr/w:type{w:val=continuous}", WD_SECTION.CONTINUOUS),
            ("w:sectPr/w:type{w:val=nextPage}", WD_SECTION.NEW_PAGE),
            ("w:sectPr/w:type{w:val=oddPage}", WD_SECTION.ODD_PAGE),
            ("w:sectPr/w:type{w:val=evenPage}", WD_SECTION.EVEN_PAGE),
            ("w:sectPr/w:type{w:val=nextColumn}", WD_SECTION.NEW_COLUMN),
        ]
    )
    def start_type_get_fixture(self, request):
        sectPr_cxml, expected_start_type = request.param
        sectPr = element(sectPr_cxml)
        return sectPr, expected_start_type

    @pytest.fixture(
        params=[
            (
                "w:sectPr/w:type{w:val=oddPage}",
                WD_SECTION.EVEN_PAGE,
                "w:sectPr/w:type{w:val=evenPage}",
            ),
            ("w:sectPr/w:type{w:val=nextPage}", None, "w:sectPr"),
            ("w:sectPr", None, "w:sectPr"),
            ("w:sectPr/w:type{w:val=continuous}", WD_SECTION.NEW_PAGE, "w:sectPr"),
            ("w:sectPr/w:type", WD_SECTION.NEW_PAGE, "w:sectPr"),
            (
                "w:sectPr/w:type",
                WD_SECTION.NEW_COLUMN,
                "w:sectPr/w:type{w:val=nextColumn}",
            ),
        ]
    )
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

    @pytest.fixture
    def _Header_(self, request):
        return class_mock(request, "docx.section._Header")

    @pytest.fixture
    def header_(self, request):
        return instance_mock(request, _Header)


class Describe_BaseHeaderFooter(object):
    def it_knows_when_its_linked_to_the_previous_header_or_footer(
        self, is_linked_get_fixture, _has_definition_prop_
    ):
        has_definition, expected_value = is_linked_get_fixture
        _has_definition_prop_.return_value = has_definition
        header = _BaseHeaderFooter(None, None, None)

        is_linked = header.is_linked_to_previous

        assert is_linked is expected_value

    def it_can_change_whether_it_is_linked_to_previous_header_or_footer(
        self,
        is_linked_set_fixture,
        _has_definition_prop_,
        _drop_definition_,
        _add_definition_,
    ):
        has_definition, new_value, drop_calls, add_calls = is_linked_set_fixture
        _has_definition_prop_.return_value = has_definition
        header = _BaseHeaderFooter(None, None, None)

        header.is_linked_to_previous = new_value

        assert _drop_definition_.call_args_list == [call(header)] * drop_calls
        assert _add_definition_.call_args_list == [call(header)] * add_calls

    def it_provides_access_to_the_header_or_footer_part_for_BlockItemContainer(
        self, _get_or_add_definition_, header_part_
    ):
        # ---this override fulfills part of the BlockItemContainer subclass interface---
        _get_or_add_definition_.return_value = header_part_
        header = _BaseHeaderFooter(None, None, None)

        header_part = header.part

        _get_or_add_definition_.assert_called_once_with(header)
        assert header_part is header_part_

    def it_provides_access_to_the_hdr_or_ftr_element_to_help(
        self, _get_or_add_definition_, header_part_
    ):
        hdr = element("w:hdr")
        _get_or_add_definition_.return_value = header_part_
        header_part_.element = hdr
        header = _BaseHeaderFooter(None, None, None)

        hdr_elm = header._element

        _get_or_add_definition_.assert_called_once_with(header)
        assert hdr_elm is hdr

    def it_gets_the_definition_when_it_has_one(
        self, _has_definition_prop_, _definition_prop_, header_part_
    ):
        _has_definition_prop_.return_value = True
        _definition_prop_.return_value = header_part_
        header = _BaseHeaderFooter(None, None, None)

        header_part = header._get_or_add_definition()

        assert header_part is header_part_

    def but_it_gets_the_prior_definition_when_it_is_linked(
        self,
        _has_definition_prop_,
        _prior_headerfooter_prop_,
        prior_headerfooter_,
        header_part_,
    ):
        _has_definition_prop_.return_value = False
        _prior_headerfooter_prop_.return_value = prior_headerfooter_
        prior_headerfooter_._get_or_add_definition.return_value = header_part_
        header = _BaseHeaderFooter(None, None, None)

        header_part = header._get_or_add_definition()

        prior_headerfooter_._get_or_add_definition.assert_called_once_with()
        assert header_part is header_part_

    def and_it_adds_a_definition_when_it_is_linked_and_the_first_section(
        self,
        _has_definition_prop_,
        _prior_headerfooter_prop_,
        _add_definition_,
        header_part_,
    ):
        _has_definition_prop_.return_value = False
        _prior_headerfooter_prop_.return_value = None
        _add_definition_.return_value = header_part_
        header = _BaseHeaderFooter(None, None, None)

        header_part = header._get_or_add_definition()

        _add_definition_.assert_called_once_with(header)
        assert header_part is header_part_

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[(False, True), (True, False)])
    def is_linked_get_fixture(self, request):
        has_definition, expected_value = request.param
        return has_definition, expected_value

    @pytest.fixture(
        params=[
            (False, True, 0, 0),
            (True, False, 0, 0),
            (True, True, 1, 0),
            (False, False, 0, 1),
        ]
    )
    def is_linked_set_fixture(self, request):
        has_definition, new_value, drop_calls, add_calls = request.param
        return has_definition, new_value, drop_calls, add_calls

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _add_definition_(self, request):
        return method_mock(request, _BaseHeaderFooter, "_add_definition")

    @pytest.fixture
    def _definition_prop_(self, request):
        return property_mock(request, _BaseHeaderFooter, "_definition")

    @pytest.fixture
    def _drop_definition_(self, request):
        return method_mock(request, _BaseHeaderFooter, "_drop_definition")

    @pytest.fixture
    def _get_or_add_definition_(self, request):
        return method_mock(request, _BaseHeaderFooter, "_get_or_add_definition")

    @pytest.fixture
    def _has_definition_prop_(self, request):
        return property_mock(request, _BaseHeaderFooter, "_has_definition")

    @pytest.fixture
    def header_part_(self, request):
        return instance_mock(request, HeaderPart)

    @pytest.fixture
    def prior_headerfooter_(self, request):
        return instance_mock(request, _BaseHeaderFooter)

    @pytest.fixture
    def _prior_headerfooter_prop_(self, request):
        return property_mock(request, _BaseHeaderFooter, "_prior_headerfooter")


class Describe_Footer(object):
    def it_can_add_a_footer_part_to_help(self, document_part_, footer_part_):
        sectPr = element("w:sectPr{r:a=b}")
        document_part_.add_footer_part.return_value = footer_part_, "rId3"
        footer = _Footer(sectPr, document_part_, WD_HEADER_FOOTER.PRIMARY)

        footer_part = footer._add_definition()

        document_part_.add_footer_part.assert_called_once_with()
        assert sectPr.xml == xml(
            "w:sectPr{r:a=b}/w:footerReference{w:type=default,r:id=rId3}"
        )
        assert footer_part is footer_part_

    def it_provides_access_to_its_footer_part_to_help(
        self, document_part_, footer_part_
    ):
        sectPr = element("w:sectPr/w:footerReference{w:type=even,r:id=rId3}")
        document_part_.footer_part.return_value = footer_part_
        footer = _Footer(sectPr, document_part_, WD_HEADER_FOOTER.EVEN_PAGE)

        footer_part = footer._definition

        document_part_.footer_part.assert_called_once_with("rId3")
        assert footer_part is footer_part_

    def it_can_drop_the_related_footer_part_to_help(self, document_part_):
        sectPr = element("w:sectPr{r:a=b}/w:footerReference{w:type=first,r:id=rId42}")
        footer = _Footer(sectPr, document_part_, WD_HEADER_FOOTER.FIRST_PAGE)

        footer._drop_definition()

        assert sectPr.xml == xml("w:sectPr{r:a=b}")
        document_part_.drop_rel.assert_called_once_with("rId42")

    def it_knows_when_it_has_a_definition_to_help(self, has_definition_fixture):
        sectPr, expected_value = has_definition_fixture
        footer = _Footer(sectPr, None, WD_HEADER_FOOTER.PRIMARY)

        has_definition = footer._has_definition

        assert has_definition is expected_value

    def it_provides_access_to_the_prior_Footer_to_help(
        self, request, document_part_, footer_
    ):
        doc_elm = element("w:document/(w:sectPr,w:sectPr)")
        prior_sectPr, sectPr = doc_elm[0], doc_elm[1]
        footer = _Footer(sectPr, document_part_, WD_HEADER_FOOTER.EVEN_PAGE)
        # ---mock must occur after construction of "real" footer---
        _Footer_ = class_mock(request, "docx.section._Footer", return_value=footer_)

        prior_footer = footer._prior_headerfooter

        _Footer_.assert_called_once_with(
            prior_sectPr, document_part_, WD_HEADER_FOOTER.EVEN_PAGE
        )
        assert prior_footer is footer_

    def but_it_returns_None_when_its_the_first_footer(self):
        doc_elm = element("w:document/w:sectPr")
        sectPr = doc_elm[0]
        footer = _Footer(sectPr, None, None)

        prior_footer = footer._prior_headerfooter

        assert prior_footer is None

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            ("w:sectPr", False),
            ("w:sectPr/w:footerReference{w:type=default}", True),
        ]
    )
    def has_definition_fixture(self, request):
        sectPr_cxml, expected_value = request.param
        sectPr = element(sectPr_cxml)
        return sectPr, expected_value

    # fixture components ---------------------------------------------

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def footer_(self, request):
        return instance_mock(request, _Footer)

    @pytest.fixture
    def footer_part_(self, request):
        return instance_mock(request, FooterPart)


class Describe_Header(object):
    def it_can_add_a_header_part_to_help(self, document_part_, header_part_):
        sectPr = element("w:sectPr{r:a=b}")
        document_part_.add_header_part.return_value = header_part_, "rId3"
        header = _Header(sectPr, document_part_, WD_HEADER_FOOTER.FIRST_PAGE)

        header_part = header._add_definition()

        document_part_.add_header_part.assert_called_once_with()
        assert sectPr.xml == xml(
            "w:sectPr{r:a=b}/w:headerReference{w:type=first,r:id=rId3}"
        )
        assert header_part is header_part_

    def it_provides_access_to_its_header_part_to_help(
        self, document_part_, header_part_
    ):
        sectPr = element("w:sectPr/w:headerReference{w:type=default,r:id=rId8}")
        document_part_.header_part.return_value = header_part_
        header = _Header(sectPr, document_part_, WD_HEADER_FOOTER.PRIMARY)

        header_part = header._definition

        document_part_.header_part.assert_called_once_with("rId8")
        assert header_part is header_part_

    def it_can_drop_the_related_header_part_to_help(self, document_part_):
        sectPr = element("w:sectPr{r:a=b}/w:headerReference{w:type=even,r:id=rId42}")
        header = _Header(sectPr, document_part_, WD_HEADER_FOOTER.EVEN_PAGE)

        header._drop_definition()

        assert sectPr.xml == xml("w:sectPr{r:a=b}")
        document_part_.drop_header_part.assert_called_once_with("rId42")

    def it_knows_when_it_has_a_header_part_to_help(self, has_definition_fixture):
        sectPr, expected_value = has_definition_fixture
        header = _Header(sectPr, None, WD_HEADER_FOOTER.FIRST_PAGE)

        has_definition = header._has_definition

        assert has_definition is expected_value

    def it_provides_access_to_the_prior_Header_to_help(
        self, request, document_part_, header_
    ):
        doc_elm = element("w:document/(w:sectPr,w:sectPr)")
        prior_sectPr, sectPr = doc_elm[0], doc_elm[1]
        header = _Header(sectPr, document_part_, WD_HEADER_FOOTER.PRIMARY)
        # ---mock must occur after construction of "real" header---
        _Header_ = class_mock(request, "docx.section._Header", return_value=header_)

        prior_header = header._prior_headerfooter

        _Header_.assert_called_once_with(
            prior_sectPr, document_part_, WD_HEADER_FOOTER.PRIMARY
        )
        assert prior_header is header_

    def but_it_returns_None_when_its_the_first_header(self):
        doc_elm = element("w:document/w:sectPr")
        sectPr = doc_elm[0]
        header = _Header(sectPr, None, None)

        prior_header = header._prior_headerfooter

        assert prior_header is None

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[("w:sectPr", False), ("w:sectPr/w:headerReference{w:type=first}", True)]
    )
    def has_definition_fixture(self, request):
        sectPr_cxml, expected_value = request.param
        sectPr = element(sectPr_cxml)
        return sectPr, expected_value

    # fixture components ---------------------------------------------

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def header_(self, request):
        return instance_mock(request, _Header)

    @pytest.fixture
    def header_part_(self, request):
        return instance_mock(request, HeaderPart)
