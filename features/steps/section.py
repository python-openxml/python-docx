# encoding: utf-8

"""
Step implementations for section-related features
"""

from __future__ import absolute_import, print_function, unicode_literals

from behave import given, then, when

from docx import Document
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.section import Section
from docx.shared import Inches

from helpers import test_docx


# given ====================================================

@given('a section collection containing 3 sections')
def given_a_section_collection_containing_3_sections(context):
    document = Document(test_docx('doc-access-sections'))
    context.sections = document.sections


@given('a section having known page dimension')
def given_a_section_having_known_page_dimension(context):
    document = Document(test_docx('sct-section-props'))
    context.section = document.sections[-1]


@given('a section having known page margins')
def given_a_section_having_known_page_margins(context):
    document = Document(test_docx('sct-section-props'))
    context.section = document.sections[0]


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


@given('a section known to have {orientation} orientation')
def given_a_section_having_known_orientation(context, orientation):
    section_idx = {
        'landscape': 0,
        'portrait':  1
    }[orientation]
    document = Document(test_docx('sct-section-props'))
    context.section = document.sections[section_idx]


# when =====================================================

@when('I set the {margin_side} margin to {inches} inches')
def when_I_set_the_margin_side_length(context, margin_side, inches):
    prop_name = {
        'left':   'left_margin',
        'right':  'right_margin',
        'top':    'top_margin',
        'bottom': 'bottom_margin',
        'gutter': 'gutter',
        'header': 'header_distance',
        'footer': 'footer_distance',
    }[margin_side]
    new_value = Inches(float(inches))
    setattr(context.section, prop_name, new_value)


@when('I set the section orientation to {orientation}')
def when_I_set_the_section_orientation(context, orientation):
    new_orientation = {
        'WD_ORIENT.PORTRAIT':  WD_ORIENT.PORTRAIT,
        'WD_ORIENT.LANDSCAPE': WD_ORIENT.LANDSCAPE,
        'None':                None,
    }[orientation]
    context.section.orientation = new_orientation


@when('I set the section page height to {y} inches')
def when_I_set_the_section_page_height_to_y_inches(context, y):
    context.section.page_height = Inches(float(y))


@when('I set the section page width to {x} inches')
def when_I_set_the_section_page_width_to_x_inches(context, x):
    context.section.page_width = Inches(float(x))


@when('I set the section start type to {start_type}')
def when_I_set_the_section_start_type_to_start_type(context, start_type):
    new_start_type = {
        'None':       None,
        'CONTINUOUS': WD_SECTION.CONTINUOUS,
        'EVEN_PAGE':  WD_SECTION.EVEN_PAGE,
        'NEW_COLUMN': WD_SECTION.NEW_COLUMN,
        'NEW_PAGE':   WD_SECTION.NEW_PAGE,
        'ODD_PAGE':   WD_SECTION.ODD_PAGE,
    }[start_type]
    context.section.start_type = new_start_type


# then =====================================================

@then('I can access a section by index')
def then_I_can_access_a_section_by_index(context):
    sections = context.sections
    for idx in range(3):
        section = sections[idx]
        assert isinstance(section, Section)


@then('I can iterate over the sections')
def then_I_can_iterate_over_the_sections(context):
    sections = context.sections
    actual_count = 0
    for section in sections:
        actual_count += 1
        assert isinstance(section, Section)
    assert actual_count == 3


@then('len(sections) is 3')
def then_len_sections_is_3(context):
    sections = context.sections
    assert len(sections) == 3, (
        'expected len(sections) of 3, got %s' % len(sections)
    )


@then('the reported {margin_side} margin is {inches} inches')
def then_the_reported_margin_is_inches(context, margin_side, inches):
    prop_name = {
        'left':   'left_margin',
        'right':  'right_margin',
        'top':    'top_margin',
        'bottom': 'bottom_margin',
        'gutter': 'gutter',
        'header': 'header_distance',
        'footer': 'footer_distance',
    }[margin_side]
    expected_value = Inches(float(inches))
    actual_value = getattr(context.section, prop_name)
    assert actual_value == expected_value


@then('the reported page orientation is {orientation}')
def then_the_reported_page_orientation_is_orientation(context, orientation):
    expected_value = {
        'WD_ORIENT.LANDSCAPE': WD_ORIENT.LANDSCAPE,
        'WD_ORIENT.PORTRAIT':  WD_ORIENT.PORTRAIT,
    }[orientation]
    assert context.section.orientation == expected_value


@then('the reported page width is {x} inches')
def then_the_reported_page_width_is_width(context, x):
    assert context.section.page_width == Inches(float(x))


@then('the reported page height is {y} inches')
def then_the_reported_page_height_is_11_inches(context, y):
    assert context.section.page_height == Inches(float(y))


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
