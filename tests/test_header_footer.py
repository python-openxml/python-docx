# encoding: utf-8

"""
Test suite for the docx.settings module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest
from .unitutil.mock import (
    instance_mock, method_mock
)

from docx.section import Section

from docx.opc.packuri import PackURI
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.parts.document import DocumentPart
from .unitutil.cxml import element, xml
from docx.parts.header_footer import HeaderPart, FooterPart


class DescribeSettings(object):

    def it_knows_its_default_header(self, section_with_default_header_fixture):
        assert section_with_default_header_fixture.header.is_linked_to_previous is False
        assert section_with_default_header_fixture.first_page_header.is_linked_to_previous is True
        assert section_with_default_header_fixture.even_odd_header.is_linked_to_previous is True

    def it_knows_its_first_header(self, section_with_first_header_fixture):
        assert section_with_first_header_fixture.header.is_linked_to_previous is True
        assert section_with_first_header_fixture.first_page_header.is_linked_to_previous is False
        assert section_with_first_header_fixture.even_odd_header.is_linked_to_previous is True

    def it_knows_its_even_header(self, section_with_even_header_fixture):
        assert section_with_even_header_fixture.header.is_linked_to_previous is True
        assert section_with_even_header_fixture.first_page_header.is_linked_to_previous is True
        assert section_with_even_header_fixture.even_odd_header.is_linked_to_previous is False

    def it_can_change_header_set_is_linked(self, section_with_default_header_can_change_is_linked_fixture):
        section, value, expected_xml = section_with_default_header_can_change_is_linked_fixture
        section.header.is_linked_to_previous = value
        assert section._sectPr.xml == expected_xml

    def it_knows_its_default_footer(self, section_with_default_footer_fixture):
        assert section_with_default_footer_fixture.footer.is_linked_to_previous is False
        assert section_with_default_footer_fixture.first_page_footer.is_linked_to_previous is True
        assert section_with_default_footer_fixture.even_odd_footer.is_linked_to_previous is True

    def it_knows_its_first_footer(self, section_with_first_footer_fixture):
        assert section_with_first_footer_fixture.footer.is_linked_to_previous is True
        assert section_with_first_footer_fixture.first_page_footer.is_linked_to_previous is False
        assert section_with_first_footer_fixture.even_odd_footer.is_linked_to_previous is True

    def it_knows_its_even_footer(self, section_with_even_footer_fixture):
        assert section_with_even_footer_fixture.footer.is_linked_to_previous is True
        assert section_with_even_footer_fixture.first_page_footer.is_linked_to_previous is True
        assert section_with_even_footer_fixture.even_odd_footer.is_linked_to_previous is False

    def it_can_change__footer_set_is_linked(self, section_with_default_footer_can_change_is_linked_fixture):
        section, value, expected_xml = section_with_default_footer_can_change_is_linked_fixture
        section.footer.is_linked_to_previous = value
        assert section._sectPr.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('w:sectPr/(w:footerReference{w:type=default,r:id=rId1}, r:id)', True,
         'w:sectPr/r:id'),
        ('w:sectPr/r:id', False,
         'w:sectPr/(r:id, w:footerReference{w:type=default,r:id=rId1})')
    ])
    def section_with_default_footer_can_change_is_linked_fixture(self, request, document_part_,
                                     footer_rel_):
        footer_reltype, footer_part, rId = footer_rel_
        sectPr_cxml, value, expected_xml = request.param
        document_part_.load_rel(footer_reltype, footer_part, rId)
        section = Section(element(sectPr_cxml), document_part_)
        return section, value, xml(expected_xml)

    @pytest.fixture(params=[
        'w:sectPr/w:footerReference{w:type=default,r:id=rId1}/r:id'
    ])
    def section_with_default_footer_fixture(self, request, document_part_,
                                     footer_rel_):
        footer_reltype, footer_part, rId = footer_rel_
        sectPr_cxml = request.param
        document_part_.load_rel(footer_reltype, footer_part, rId)
        section = Section(element(sectPr_cxml), document_part_)
        return section

    @pytest.fixture(params=[
        'w:sectPr/w:footerReference{w:type=first,r:id=rId1}/r:id'
    ])
    def section_with_first_footer_fixture(self, request, document_part_,
                                            footer_rel_):
        footer_reltype, footer_part, rId = footer_rel_
        sectPr_cxml = request.param
        document_part_.load_rel(footer_reltype, footer_part, rId)
        section = Section(element(sectPr_cxml), document_part_)
        return section

    @pytest.fixture(params=[
        'w:sectPr/w:footerReference{w:type=even,r:id=rId1}/r:id'
    ])
    def section_with_even_footer_fixture(self, request, document_part_,
                                            footer_rel_):
        footer_reltype, footer_part, rId = footer_rel_
        sectPr_cxml = request.param
        document_part_.load_rel(footer_reltype, footer_part, rId)
        section = Section(element(sectPr_cxml), document_part_)
        return section

    @pytest.fixture(params=[
        ('w:sectPr/(w:headerReference{w:type=default,r:id=rId1}, r:id)', True,
         'w:sectPr/r:id'),
        ('w:sectPr/r:id', False,
         'w:sectPr/(r:id, w:headerReference{w:type=default,r:id=rId1})')
    ])
    def section_with_default_header_can_change_is_linked_fixture(self, request, document_part_,
                                     header_rel_):
        header_reltype, header_part, rId = header_rel_
        sectPr_cxml, value, expected_xml = request.param
        document_part_.load_rel(header_reltype, header_part, rId)
        section = Section(element(sectPr_cxml), document_part_)
        return section, value, xml(expected_xml)

    @pytest.fixture(params=[
        'w:sectPr/w:headerReference{w:type=default,r:id=rId1}/r:id'
    ])
    def section_with_default_header_fixture(self, request, document_part_,
                                     header_rel_):
        header_reltype, header_part, rId = header_rel_
        sectPr_cxml = request.param
        document_part_.load_rel(header_reltype, header_part, rId)
        section = Section(element(sectPr_cxml), document_part_)
        return section

    @pytest.fixture(params=[
        'w:sectPr/w:headerReference{w:type=first,r:id=rId1}/r:id'
    ])
    def section_with_first_header_fixture(self, request, document_part_,
                                            header_rel_):
        header_reltype, header_part, rId = header_rel_
        sectPr_cxml = request.param
        document_part_.load_rel(header_reltype, header_part, rId)
        section = Section(element(sectPr_cxml), document_part_)
        return section


    @pytest.fixture(params=[
        'w:sectPr/w:headerReference{w:type=even,r:id=rId1}/r:id'
    ])
    def section_with_even_header_fixture(self, request, document_part_,
                                            header_rel_):
        header_reltype, header_part, rId = header_rel_
        sectPr_cxml = request.param
        document_part_.load_rel(header_reltype, header_part, rId)
        section = Section(element(sectPr_cxml), document_part_)
        return section

    @pytest.fixture
    def header_rel_(self, header_rId_, header_reltype_, header_part_):
        return header_reltype_, header_part_, header_rId_


    @pytest.fixture
    def footer_rel_(self, footer_rId_, footer_reltype_, footer_part_):
        return footer_reltype_, footer_part_, footer_rId_

    @pytest.fixture
    def footer_rId_(self):
        return 'rId1'

    @pytest.fixture
    def header_rId_(self):
        return 'rId1'

    @pytest.fixture
    def document_part_(self, request, document_partname_, _add_header_part_, _add_footer_part_):
        document_part = instance_mock(request, DocumentPart)
        document_part.add_header_part = _add_header_part_
        document_part.add_footer_part = _add_footer_part_
        return document_part

    @pytest.fixture
    def _add_header_part_(self, request, header_rId_):
        return method_mock(
            request, DocumentPart, 'add_header_part',
            return_value=header_rId_
        )

    @pytest.fixture
    def _add_footer_part_(self, request, footer_rId_):
        return method_mock(
            request, DocumentPart, 'add_footer_part',
            return_value=footer_rId_
        )


    @pytest.fixture
    def header_part_(self, request):
        return instance_mock(request, HeaderPart)

    @pytest.fixture
    def footer_part_(self, request):
        return instance_mock(request, FooterPart)

    @pytest.fixture
    def header_reltype_(self):
        return RT.HEADER

    @pytest.fixture
    def footer_reltype_(self):
        return RT.FOOTER

    @pytest.fixture
    def document_partname_(self, _baseURI):
        return PackURI(_baseURI)

    @pytest.fixture
    def _baseURI(self):
        return '/baseURI'
