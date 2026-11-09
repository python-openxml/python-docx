"""Step implementations for basic API features."""

import os

from behave import given, then, when

import docx
from docx import Document
from docx.opc.constants import CONTENT_TYPE as CT

from helpers import bool_vals, saved_docx_path, test_docx, test_file

main_content_types = {
    ".docm": CT.WML_DOCUMENT_MACRO_MAIN,
    ".dotx": CT.WML_TEMPLATE_MAIN,
    ".dotm": CT.WML_TEMPLATE_MACRO_MAIN,
}

# given ====================================================


@given("a document opened from a {ext} file")
def given_a_document_opened_from_an_ext_file(context, ext):
    context.ext = ext
    context.document = Document(test_file("doc-default%s" % ext))


@given("I have python-docx installed")
def given_I_have_python_docx_installed(context):
    pass


# when =====================================================


@when("I call docx.Document() with no arguments")
def when_I_call_docx_Document_with_no_arguments(context):
    context.document = Document()


@when("I call docx.Document() with the path of a .docx file")
def when_I_call_docx_Document_with_the_path_of_a_docx_file(context):
    context.document = Document(test_docx("doc-default"))


@when("I call docx.Document() with the path of a {ext} file")
def when_I_call_docx_Document_with_the_path_of_an_ext_file(context, ext):
    context.document = Document(test_file("doc-default%s" % ext))


@when("I save and reload the document")
def when_I_save_and_reload_the_document(context):
    path = os.path.splitext(saved_docx_path)[0] + context.ext
    context.document.save(path)
    context.document = Document(path)


# then =====================================================


@then("the document part content type is the {ext} content type")
def then_the_document_part_content_type_is_the_ext_content_type(context, ext):
    actual = context.document.part.content_type
    expected = main_content_types[ext]
    assert actual == expected, "expected '%s', got '%s'" % (expected, actual)


@then("the VBA project part is preserved: {has_vba}")
def then_the_VBA_project_part_is_preserved(context, has_vba):
    original = Document(test_file("doc-default%s" % context.ext)).part.package
    reloaded = context.document.part.package

    def vba_blob(package):
        parts = [p for p in package.iter_parts() if p.partname == "/word/vbaProject.bin"]
        return parts[0].blob if parts else None

    expected = vba_blob(original)
    assert (expected is not None) is bool_vals[has_vba]
    assert vba_blob(reloaded) == expected


@then("document is a Document object")
def then_document_is_a_Document_object(context):
    document = context.document
    assert isinstance(document, docx.document.Document)


@then("the last paragraph contains the text I specified")
def then_last_p_contains_specified_text(context):
    document = context.document
    text = context.paragraph_text
    p = document.paragraphs[-1]
    assert p.text == text


@then("the last paragraph has the style I specified")
def then_the_last_paragraph_has_the_style_I_specified(context):
    document, expected_style = context.document, context.style
    paragraph = document.paragraphs[-1]
    assert paragraph.style == expected_style


@then("the last paragraph is the empty paragraph I added")
def then_last_p_is_empty_paragraph_added(context):
    document = context.document
    p = document.paragraphs[-1]
    assert p.text == ""
