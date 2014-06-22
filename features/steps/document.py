# encoding: utf-8

"""
Step implementations for document-related features
"""

from __future__ import absolute_import, print_function, unicode_literals

from behave import given, then, when

from docx import Document
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.parts.document import Sections
from docx.section import Section

from helpers import test_docx


# given ===================================================

@given('a document having three sections')
def given_a_document_having_three_sections(context):
    context.document = Document(test_docx('doc-access-sections'))


@given('a section collection')
def given_a_section_collection(context):
    document = Document(test_docx('doc-access-sections'))
    context.sections = document.sections


@given('a single-section document having portrait layout')
def given_a_single_section_document_having_portrait_layout(context):
    context.document = Document(test_docx('doc-add-section'))
    section = context.document.sections[-1]
    context.original_dimensions = (section.page_width, section.page_height)


# when ====================================================

@when('I add an even-page section to the document')
def when_I_add_an_even_page_section_to_the_document(context):
    context.section = context.document.add_section(WD_SECTION.EVEN_PAGE)


@when('I change the new section layout to landscape')
def when_I_change_the_new_section_layout_to_landscape(context):
    new_height, new_width = context.original_dimensions
    section = context.section
    section.orientation = WD_ORIENT.LANDSCAPE
    section.page_width = new_width
    section.page_height = new_height


# then ====================================================

@then('I can access a section by index')
def then_I_can_access_a_section_by_index(context):
    sections = context.sections
    for idx in range(3):
        section = sections[idx]
        assert isinstance(section, Section)


@then('I can access the section collection of the document')
def then_I_can_access_the_section_collection_of_the_document(context):
    sections = context.document.sections
    msg = 'document.sections not instance of Sections'
    assert isinstance(sections, Sections), msg


@then('I can iterate over the sections')
def then_I_can_iterate_over_the_sections(context):
    sections = context.sections
    actual_count = 0
    for section in sections:
        actual_count += 1
        assert isinstance(section, Section)
    assert actual_count == 3


@then('the document has two sections')
def then_the_document_has_two_sections(context):
    assert len(context.document.sections) == 2


@then('the first section is portrait')
def then_the_first_section_is_portrait(context):
    first_section = context.document.sections[0]
    expected_width, expected_height = context.original_dimensions
    assert first_section.orientation == WD_ORIENT.PORTRAIT
    assert first_section.page_width == expected_width
    assert first_section.page_height == expected_height


@then('the length of the section collection is 3')
def then_the_length_of_the_section_collection_is_3(context):
    sections = context.document.sections
    assert len(sections) == 3, (
        'expected len(sections) of 2, got %s' % len(sections)
    )


@then('the second section is landscape')
def then_the_second_section_is_landscape(context):
    new_section = context.document.sections[-1]
    expected_height, expected_width = context.original_dimensions
    assert new_section.orientation == WD_ORIENT.LANDSCAPE
    assert new_section.page_width == expected_width
    assert new_section.page_height == expected_height
