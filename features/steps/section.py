# encoding: utf-8

"""
Step implementations for section-related features
"""

from __future__ import absolute_import, print_function, unicode_literals

from behave import given, then

from docx import Document
from docx.enum.section import WD_SECTION

from helpers import test_docx


# given ====================================================

@given('a section having start type {start_type}')
def given_a_section_having_start_type(context, start_type):
    section_idx = {
        'CONTINUOUS': 0,
        'NEW_PAGE':   1,
        'ODD_PAGE':   2,
        'EVEN_PAGE':  3,
        'NEW_COLUMN': 4,
    }[start_type]
    document = Document(test_docx('sct-section-props'))
    context.section = document.sections[section_idx]


# then =====================================================

@then('the reported section start type is {start_type}')
def then_the_reported_section_start_type_is_type(context, start_type):
    expected_start_type = {
        'CONTINUOUS': WD_SECTION.CONTINUOUS,
        'EVEN_PAGE':  WD_SECTION.EVEN_PAGE,
        'NEW_COLUMN': WD_SECTION.NEW_COLUMN,
        'NEW_PAGE':   WD_SECTION.NEW_PAGE,
        'ODD_PAGE':   WD_SECTION.ODD_PAGE,
    }[start_type]
    assert context.section.start_type == expected_start_type
