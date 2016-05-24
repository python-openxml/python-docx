# encoding: utf-8

"""
Step implementations for header-related features
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from behave import given, then

from docx import Document

from helpers import test_docx


# given ===================================================

@given('a header {having_or_no} definition')
def given_a_header_having_or_no_definition(context, having_or_no):
    filename = {
        'having a':  'hdr-header-props',
        'having no': 'doc-default',
    }[having_or_no]
    document = Document(test_docx(filename))
    context.header = document.sections[0].header


# then =====================================================

@then('header.body contains the text of the header')
def then_header_body_contains_the_text_of_the_header(context):
    header = context.header
    text = header.body.paragraphs[0].text
    assert text == 'S1HP1'


@then('header.body is a BlockItemContainer object')
def then_header_body_is_a_BlockItemContainer_object(context):
    header = context.header
    assert type(header.body).__name__ == 'BlockItemContainer'


@then('header.is_linked_to_previous is {value}')
def then_header_is_linked_to_previous_is_value(context, value):
    expected_value = {'True': True, 'False': False}[value]
    header = context.header
    assert header.is_linked_to_previous is expected_value
