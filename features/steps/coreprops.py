# encoding: utf-8

"""
Gherkin step implementations for core properties-related features.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from datetime import datetime

from behave import given, then

from docx import Document
from docx.opc.coreprops import CoreProperties

from helpers import test_docx


# given ===================================================

@given('a document having known core properties')
def given_a_document_having_known_core_properties(context):
    context.document = Document(test_docx('doc-coreprops'))


# then ====================================================

@then('I can access the core properties object')
def then_I_can_access_the_core_properties_object(context):
    document = context.document
    core_properties = document.core_properties
    assert isinstance(core_properties, CoreProperties)


@then('the core property values match the known values')
def then_the_core_property_values_match_the_known_values(context):
    known_propvals = (
        ('author',           'Steve Canny'),
        ('category',         'Category'),
        ('comments',         'Description'),
        ('content_status',   'Content Status'),
        ('created',          datetime(2014, 12, 13, 22, 2, 0)),
        ('identifier',       'Identifier'),
        ('keywords',         'key; word; keyword'),
        ('language',         'Language'),
        ('last_modified_by', 'Steve Canny'),
        ('last_printed',     datetime(2014, 12, 13, 22, 2, 42)),
        ('modified',         datetime(2014, 12, 13, 22, 6, 0)),
        ('revision',         2),
        ('subject',          'Subject'),
        ('title',            'Title'),
        ('version',          '0.7.1a3'),
    )
    core_properties = context.document.core_properties
    for name, expected_value in known_propvals:
        value = getattr(core_properties, name)
        assert value == expected_value, (
            "got '%s' for core property '%s'" % (value, name)
        )
