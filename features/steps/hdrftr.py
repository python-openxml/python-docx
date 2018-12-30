# encoding: utf-8

"""Step implementations for header and footer-related features"""

from __future__ import absolute_import, division, print_function, unicode_literals

from behave import given, then, when

from docx import Document

from helpers import test_docx


# given ====================================================

@given("a _Footer object {with_or_no} footer definition as footer")
def given_a_Footer_object_with_or_no_footer_definition(context, with_or_no):
    section_idx = {"with a": 0, "with no": 1}[with_or_no]
    context.sections = Document(test_docx("hdr-header-footer")).sections
    context.footer = context.sections[section_idx].footer


@given("a _Header object {with_or_no} header definition as header")
def given_a_Header_object_with_or_no_header_definition(context, with_or_no):
    section_idx = {"with a": 0, "with no": 1}[with_or_no]
    context.sections = Document(test_docx("hdr-header-footer")).sections
    context.header = context.sections[section_idx].header


@given("the next _Footer object with no footer definition as footer_2")
def given_the_next_Footer_object_with_no_footer_definition(context):
    context.footer_2 = context.sections[1].footer


@given("the next _Header object with no header definition as header_2")
def given_the_next_Header_object_with_no_header_definition(context):
    context.header_2 = context.sections[1].header


# when =====================================================

@when("I assign {value} to header.is_linked_to_previous")
def when_I_assign_value_to_header_is_linked_to_previous(context, value):
    context.header.is_linked_to_previous = eval(value)


@when("I assign {value} to footer.is_linked_to_previous")
def when_I_assign_value_to_footer_is_linked_to_previous(context, value):
    context.footer.is_linked_to_previous = eval(value)


# then =====================================================

@then("footer.is_linked_to_previous is {value}")
def then_footer_is_linked_to_previous_is_value(context, value):
    actual = context.footer.is_linked_to_previous
    expected = eval(value)
    assert actual == expected, "footer.is_linked_to_previous is %s" % actual


@then("footer_2.paragraphs[0].text == footer.paragraphs[0].text")
def then_footer_2_text_eq_footer_text(context):
    actual = context.footer_2.paragraphs[0].text
    expected = context.footer.paragraphs[0].text
    assert actual == expected, "footer_2.paragraphs[0].text == %s" % actual


@then("footer_2.is_linked_to_previous is {value}")
def then_footer_2_is_linked_to_previous_is_value(context, value):
    actual = context.footer_2.is_linked_to_previous
    expected = eval(value)
    assert actual == expected, "footer_2.is_linked_to_previous is %s" % actual


@then("header.is_linked_to_previous is {value}")
def then_header_is_linked_to_previous_is_value(context, value):
    actual = context.header.is_linked_to_previous
    expected = eval(value)
    assert actual == expected, "header.is_linked_to_previous is %s" % actual


@then("header_2.is_linked_to_previous is {value}")
def then_header_2_is_linked_to_previous_is_value(context, value):
    actual = context.header_2.is_linked_to_previous
    expected = eval(value)
    assert actual == expected, "header_2.is_linked_to_previous is %s" % actual


@then("header_2.paragraphs[0].text == header.paragraphs[0].text")
def then_header_2_text_eq_header_text(context):
    actual = context.header_2.paragraphs[0].text
    expected = context.header.paragraphs[0].text
    assert actual == expected, "header_2.paragraphs[0].text == %s" % actual
