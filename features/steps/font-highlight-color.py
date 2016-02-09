# encoding: utf-8

"""
Step implementations for font-highlight-color-related features.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from behave import given, then, when

from docx import Document
#from docx.enum.text import WD_COLOR_INDEX

from helpers import test_docx


# given ===================================================

@given('a font having highlight color {highlight_color}')
def given_a_font_having_highlight_color(context, highlight_color):
    # This translates the highlight color used in the Word document to the appropriate paragraph number from the test document 
    color_index = { 'None'          : 0,
                    'Yellow'        : 1,
                    'Bright Green'  : 2,
                    'Turquoise'     : 3,
                    'Pink'          : 4,
                    'Blue'          : 5,
                    'Red'           : 6,
                    'Dark Blue'     : 7,
                    'Teal'          : 8,
                    'Green'         : 9,
                    'Violet'        : 10,
                    'Dark Red'      : 11,
                    'Dark Yellow'   : 12,
                    'Dark Gray'     : 13,
                    'Light Gray'    : 14,
                    'Black'         : 15 }
    par_index = color_index[highlight_color]
    document = Document(test_docx('txt-font-highlight-color'))
    context.font = document.paragraphs[par_index].runs[0].font


# when ====================================================

@when('I assign {value} to font.highlight_color')
def when_I_assign_value_to_font_highlight_color(context, value):
    from docx.enum.text import WD_COLOR_INDEX
    font = context.font
    if value == u'None':
        expected_result = None
    else:
        expected_result = getattr(WD_COLOR_INDEX, value)
    font.highlight_color = expected_result


# then =====================================================

@then('font.highlight_color is {value}')
def then_font_highlight_color_is_value(context, value):
    from docx.enum.text import WD_COLOR_INDEX
    font = context.font
    if value == u'None':
        expected_result = None
    else:
        expected_result = getattr(WD_COLOR_INDEX, value)
    assert font.highlight_color == expected_result

@then('the XML value is {xml_value}')
def then_font_highlight_color_is_value(context, xml_value):
    from docx.enum.text import WD_COLOR_INDEX
    font = context.font
    assert WD_COLOR_INDEX.to_xml(font.highlight_color) == xml_value
