# encoding: utf-8

"""
Gherkin step implementations for core properties-related features.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from datetime import datetime

from behave import given, then, when

from docx import Document
from docx.opc.coreprops import CoreProperties

from helpers import test_docx


# given ===================================================

@given('a document having known core properties')
def given_a_document_having_known_core_properties(context):
    context.document = Document(test_docx('doc-coreprops'))


# when ====================================================

@when("I assign new values to the properties")
def when_I_assign_new_values_to_the_properties(context):
    context.propvals = (
        ('author',           'Creator'),
        ('category',         'Category'),
        ('comments',         'Description'),
        ('content_status',   'Content Status'),
        ('created',          datetime(2013, 6, 15, 12, 34, 56)),
        ('identifier',       'Identifier'),
        ('keywords',         'key; word; keyword'),
        ('language',         'Language'),
        ('last_modified_by', 'Last Modified By'),
        ('last_printed',     datetime(2013, 6, 15, 12, 34, 56)),
        ('modified',         datetime(2013, 6, 15, 12, 34, 56)),
        ('revision',         9),
        ('subject',          'Subject'),
        ('title',            'Title'),
        ('version',          'Version'),
    )
    core_properties = context.document.core_properties
    for name, value in context.propvals:
        setattr(core_properties, name, value)


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


@then('the core property values match the new values')
def then_the_core_property_values_match_the_new_values(context):
    core_properties = context.document.core_properties
    for name, expected_value in context.propvals:
        value = getattr(core_properties, name)
        assert value == expected_value, (
            "got '%s' for core property '%s'" % (value, name)
        )
