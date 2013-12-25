# encoding: utf-8

"""
Step implementations for graphical object (shape) related features
"""

from __future__ import absolute_import, print_function, unicode_literals

from behave import given, then

from docx import Document
from docx.parts import InlineShape, InlineShapes

from .helpers import test_docx


# given ===================================================

@given('a document containing two inline shapes')
def given_a_document_containing_two_inline_shapes(context):
    docx_path = test_docx('shp-inline-shape-access')
    context.document = Document(docx_path)


@given('an inline shape collection containing two shapes')
def given_inline_shape_collection_containing_two_shapes(context):
    docx_path = test_docx('shp-inline-shape-access')
    document = Document(docx_path)
    context.inline_shapes = document.inline_shapes


# then =====================================================

@then('I can access an inline shape by index')
def then_can_access_inline_shape_by_index(context):
    inline_shapes = context.inline_shapes
    for idx in range(2):
        inline_shape = inline_shapes[idx]
        assert isinstance(inline_shape, InlineShape)


@then('I can access the inline shape collection of the document')
def then_can_access_inline_shape_collection_of_document(context):
    document = context.document
    inline_shapes = document.inline_shapes
    assert isinstance(inline_shapes, InlineShapes)


@then('I can iterate over the inline shape collection')
def then_can_iterate_over_inline_shape_collection(context):
    inline_shapes = context.inline_shapes
    actual_count = 0
    for inline_shape in inline_shapes:
        actual_count += 1
        assert isinstance(inline_shape, InlineShape)
    assert actual_count == 2


@then('the length of the inline shape collection is 2')
def then_len_of_inline_shape_collection_is_2(context):
    inline_shapes = context.document.inline_shapes
    assert len(inline_shapes) == 2
