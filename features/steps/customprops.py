# encoding: utf-8

"""
Gherkin step implementations for custom properties-related features.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from datetime import datetime, timedelta

from behave import given, then, when

from docx import Document
from docx.opc.customprops import CustomProperties

from helpers import test_docx


# given ===================================================

@given('a document having known custom properties')
def given_a_document_having_known_custom_properties(context):
    context.document = Document(test_docx('doc-customprops'))


@given('a document having no custom properties part')
def given_a_document_having_no_custom_properties_part(context):
    context.document = Document(test_docx('doc-no-customprops'))


# when ====================================================

@when('I access the custom properties object')
def when_I_access_the_custom_properties_object(context):
    context.document.custom_properties


@when("I assign new values to the custom properties")
def when_I_assign_new_values_to_the_custom_properties(context):
    context.propvals = (
        ('CustomPropBool',   False),
        ('CustomPropInt',    1),
        ('CustomPropString', 'Lorem ipsum'),
    )
    custom_properties = context.document.custom_properties
    for name, value in context.propvals:
        custom_properties[name] = value


# then ====================================================

@then('a custom properties part with no values is added')
def then_a_custom_properties_part_with_no_values_is_added(context):
    custom_properties = context.document.custom_properties
    assert len(custom_properties) == 0


@then('I can access the custom properties object')
def then_I_can_access_the_custom_properties_object(context):
    document = context.document
    custom_properties = document.custom_properties
    assert isinstance(custom_properties, CustomProperties)


@then('the custom property values match the known values')
def then_the_custom_property_values_match_the_known_values(context):
    known_propvals = (
        ('CustomPropBool',   True),
        ('CustomPropInt',    13),
        ('CustomPropString', 'Test String'),
    )
    custom_properties = context.document.custom_properties
    for name, expected_value in known_propvals:
        value = custom_properties[name]
        assert value == expected_value, (
            "got '%s' for custom property '%s'" % (value, name)
        )


@then('the custom property values match the new values')
def then_the_custom_property_values_match_the_new_values(context):
    custom_properties = context.document.custom_properties
    for name, expected_value in context.propvals:
        value = custom_properties[name]
        assert value == expected_value, (
            "got '%s' for custom property '%s'" % (value, name)
        )
