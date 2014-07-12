# encoding: utf-8

"""
Step implementations for image characterization features
"""

from __future__ import absolute_import, print_function, unicode_literals

from behave import given, then, when

from docx.image.image import Image

from helpers import test_file


# given ===================================================

@given('the image file \'{filename}\'')
def given_image_filename(context, filename):
    context.image_path = test_file(filename)


# when ====================================================

@when('I construct an image using the image path')
def when_construct_image_using_path(context):
    context.image = Image.from_file(context.image_path)


# then ====================================================

@then('the image has content type \'{mime_type}\'')
def then_image_has_content_type(context, mime_type):
    content_type = context.image.content_type
    assert content_type == mime_type, (
        "expected MIME type '%s', got '%s'" % (mime_type, content_type)
    )


@then('the image has {horz_dpi_str} horizontal dpi')
def then_image_has_horizontal_dpi(context, horz_dpi_str):
    expected_horz_dpi = int(horz_dpi_str)
    horz_dpi = context.image.horz_dpi
    assert horz_dpi == expected_horz_dpi, (
        "expected horizontal dpi %d, got %d" % (expected_horz_dpi, horz_dpi)
    )


@then('the image has {vert_dpi_str} vertical dpi')
def then_image_has_vertical_dpi(context, vert_dpi_str):
    expected_vert_dpi = int(vert_dpi_str)
    vert_dpi = context.image.vert_dpi
    assert vert_dpi == expected_vert_dpi, (
        "expected vertical dpi %d, got %d" % (expected_vert_dpi, vert_dpi)
    )


@then('the image is {px_height_str} pixels high')
def then_image_is_cx_pixels_high(context, px_height_str):
    expected_px_height = int(px_height_str)
    px_height = context.image.px_height
    assert px_height == expected_px_height, (
        "expected pixel height %d, got %d" % (expected_px_height, px_height)
    )


@then('the image is {px_width_str} pixels wide')
def then_image_is_cx_pixels_wide(context, px_width_str):
    expected_px_width = int(px_width_str)
    px_width = context.image.px_width
    assert px_width == expected_px_width, (
        "expected pixel width %d, got %d" % (expected_px_width, px_width)
    )
