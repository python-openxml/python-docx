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
    context.exp_prop_names = [
        'AppVersion', 'CustomPropBool', 'CustomPropInt', 'CustomPropString',
        'DocSecurity', 'HyperlinksChanged', 'LinksUpToDate', 'ScaleCrop', 'ShareDoc'
    ]


@given('a document having no custom properties part')
def given_a_document_having_no_custom_properties_part(context):
    context.document = Document(test_docx('doc-no-customprops'))
    context.exp_prop_names = []


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


@when("I delete an existing custom property")
def when_I_delete_an_existing_custom_property(context):
    custom_properties = context.document.custom_properties
    del custom_properties["CustomPropInt"]
    context.prop_name = "CustomPropInt"


# then ====================================================

@then('a custom properties part with no values is added')
def then_a_custom_properties_part_with_no_values_is_added(context):
    custom_properties = context.document.custom_properties
    assert len(custom_properties) == 0


@then('I can access the custom properties object')
def then_I_can_access_the_custom_properties_object(context):
    custom_properties = context.document.custom_properties
    assert isinstance(custom_properties, CustomProperties)


@then('the expected custom properties are visible')
def then_the_expected_custom_properties_are_visible(context):
    custom_properties = context.document.custom_properties
    exp_prop_names = context.exp_prop_names
    for name in exp_prop_names:
        assert custom_properties.lookup(name) is not None


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


@then('I can iterate the custom properties object')
def then_I_can_iterate_the_custom_properties_object(context):
    custom_properties = context.document.custom_properties
    exp_prop_names = context.exp_prop_names
    act_prop_names = [name for name in custom_properties]
    assert act_prop_names == exp_prop_names


@then('the custom property is missing in the remaining list of custom properties')
def then_the_custom_property_is_missing_in_the_remaining_list_of_custom_properties(context):
    custom_properties = context.document.custom_properties
    prop_name = context.prop_name
    assert prop_name is not None
    assert custom_properties.lookup(prop_name) is None
    assert prop_name not in [name for name in custom_properties]
