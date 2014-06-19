# encoding: utf-8

"""
Step implementations for document-related features
"""

from __future__ import absolute_import, print_function, unicode_literals

from behave import given, then

from docx import Document
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


@then('the length of the section collection is 3')
def then_the_length_of_the_section_collection_is_3(context):
    sections = context.document.sections
    assert len(sections) == 3, (
        'expected len(sections) of 2, got %s' % len(sections)
    )
