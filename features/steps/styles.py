# encoding: utf-8

"""
Step implementations for styles-related features
"""

from behave import given, then, when

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.styles.styles import Styles
from docx.styles.style import BaseStyle
from docx.text.paragraph import ParagraphFormat
from docx.text.run import Font

from helpers import test_docx

bool_vals = {
    'True':  True,
    'False': False
}

style_types = {
    'WD_STYLE_TYPE.CHARACTER': WD_STYLE_TYPE.CHARACTER,
    'WD_STYLE_TYPE.PARAGRAPH': WD_STYLE_TYPE.PARAGRAPH,
    'WD_STYLE_TYPE.LIST':      WD_STYLE_TYPE.LIST,
    'WD_STYLE_TYPE.TABLE':     WD_STYLE_TYPE.TABLE,
}

tri_state_vals = {
    'True':  True,
    'False': False,
    'None':  None,
}


# given ===================================================

@given('a document having a styles part')
def given_a_document_having_a_styles_part(context):
    docx_path = test_docx('sty-having-styles-part')
    context.document = Document(docx_path)


@given('a document having known styles')
def given_a_document_having_known_styles(context):
    docx_path = test_docx('sty-known-styles')
    document = Document(docx_path)
    context.document = document
    context.style_count = len(document.styles)


@given('a document having no styles part')
def given_a_document_having_no_styles_part(context):
    docx_path = test_docx('sty-having-no-styles-part')
    context.document = Document(docx_path)


@given('a style based on {base_style}')
def given_a_style_based_on_setting(context, base_style):
    style_name = {
        'no style': 'Base',
        'Normal':   'Sub Normal',
        'Base':     'Citation',
    }[base_style]
    document = Document(test_docx('sty-known-styles'))
    context.styles = document.styles
    context.style = document.styles[style_name]


@given('a style having a known {attr_name}')
def given_a_style_having_a_known_attr_name(context, attr_name):
    docx_path = test_docx('sty-having-styles-part')
    document = Document(docx_path)
    context.style = document.styles['Normal']


@given('a style having hidden set {setting}')
def given_a_style_having_hidden_set_setting(context, setting):
    document = Document(test_docx('sty-behav-props'))
    style_name = {
        'on':         'Foo',
        'off':        'Bar',
        'no setting': 'Baz',
    }[setting]
    context.style = document.styles[style_name]


@given('a style having priority of {setting}')
def given_a_style_having_priority_of_setting(context, setting):
    document = Document(test_docx('sty-behav-props'))
    style_name = {
        'no setting': 'Baz',
        '42':         'Foo',
    }[setting]
    context.style = document.styles[style_name]


@given('a style of type {style_type}')
def given_a_style_of_type(context, style_type):
    document = Document(test_docx('sty-known-styles'))
    name = {
        'WD_STYLE_TYPE.CHARACTER': 'Default Paragraph Font',
        'WD_STYLE_TYPE.LIST':      'No List',
        'WD_STYLE_TYPE.PARAGRAPH': 'Normal',
        'WD_STYLE_TYPE.TABLE':     'Normal Table',
    }[style_type]
    context.style = document.styles[name]


# when =====================================================

@when('I assign a new name to the style')
def when_I_assign_a_new_name_to_the_style(context):
    context.style.name = 'Foobar'


@when('I assign a new style id to the style')
def when_I_assign_a_new_style_id_to_the_style(context):
    context.style.style_id = 'Foo42'


@when('I assign {value_key} to style.base_style')
def when_I_assign_value_to_style_base_style(context, value_key):
    value = {
        'None':               None,
        'styles[\'Normal\']': context.styles['Normal'],
        'styles[\'Base\']':   context.styles['Base'],
    }[value_key]
    context.style.base_style = value


@when('I assign {value} to style.hidden')
def when_I_assign_value_to_style_hidden(context, value):
    style, new_value = context.style, tri_state_vals[value]
    style.hidden = new_value


@when('I assign {value} to style.priority')
def when_I_assign_value_to_style_priority(context, value):
    style = context.style
    new_value = None if value == 'None' else int(value)
    style.priority = new_value


@when('I call add_style(\'{name}\', {type_str}, builtin={builtin_str})')
def when_I_call_add_style(context, name, type_str, builtin_str):
    styles = context.document.styles
    type = style_types[type_str]
    builtin = bool_vals[builtin_str]
    styles.add_style(name, type, builtin=builtin)


@when('I delete a style')
def when_I_delete_a_style(context):
    context.document.styles['No List'].delete()


# then =====================================================

@then('I can access a style by its UI name')
def then_I_can_access_a_style_by_its_UI_name(context):
    styles = context.document.styles
    style = styles['Default Paragraph Font']
    assert isinstance(style, BaseStyle)


@then('I can access a style by style id')
def then_I_can_access_a_style_by_style_id(context):
    styles = context.document.styles
    style = styles['DefaultParagraphFont']
    assert isinstance(style, BaseStyle)


@then('I can access the document styles collection')
def then_I_can_access_the_document_styles_collection(context):
    document = context.document
    styles = document.styles
    assert isinstance(styles, Styles)


@then('I can iterate over its styles')
def then_I_can_iterate_over_its_styles(context):
    styles = [s for s in context.document.styles]
    assert len(styles) > 0
    assert all(isinstance(s, BaseStyle) for s in styles)


@then('len(styles) is {style_count_str}')
def then_len_styles_is_style_count(context, style_count_str):
    assert len(context.document.styles) == int(style_count_str)


@then('style.base_style is {value_key}')
def then_style_base_style_is_value(context, value_key):
    expected_value = {
        'None':               None,
        'styles[\'Normal\']': context.styles['Normal'],
        'styles[\'Base\']':   context.styles['Base'],
    }[value_key]
    style = context.style
    assert style.base_style == expected_value


@then('style.builtin is {builtin_str}')
def then_style_builtin_is_builtin(context, builtin_str):
    style = context.style
    builtin = bool_vals[builtin_str]
    assert style.builtin == builtin


@then('style.font is the Font object for the style')
def then_style_font_is_the_Font_object_for_the_style(context):
    style = context.style
    font = style.font
    assert isinstance(font, Font)
    assert font.element is style.element


@then('style.hidden is {value}')
def then_style_hidden_is_value(context, value):
    style, expected_value = context.style, tri_state_vals[value]
    assert style.hidden is expected_value


@then('style.name is the {which} name')
def then_style_name_is_the_which_name(context, which):
    expected_name = {
        'known': 'Normal',
        'new':   'Foobar',
    }[which]
    style = context.style
    assert style.name == expected_name


@then('style.paragraph_format is the ParagraphFormat object for the style')
def then_style_paragraph_format_is_the_ParagraphFormat_object(context):
    style = context.style
    paragraph_format = style.paragraph_format
    assert isinstance(paragraph_format, ParagraphFormat)
    assert paragraph_format.element is style.element


@then('style.priority is {value}')
def then_style_priority_is_value(context, value):
    style = context.style
    expected_value = None if value == 'None' else int(value)
    assert style.priority == expected_value


@then('style.style_id is the {which} style id')
def then_style_style_id_is_the_which_style_id(context, which):
    expected_style_id = {
        'known': 'Normal',
        'new':   'Foo42',
    }[which]
    style = context.style
    assert style.style_id == expected_style_id


@then('style.type is the known type')
def then_style_type_is_the_known_type(context):
    style = context.style
    assert style.type == WD_STYLE_TYPE.PARAGRAPH


@then('style.type is {type_str}')
def then_style_type_is_type(context, type_str):
    style = context.style
    style_type = style_types[type_str]
    assert style.type == style_type


@then('styles[\'{name}\'] is a style')
def then_styles_name_is_a_style(context, name):
    styles = context.document.styles
    style = context.style = styles[name]
    assert isinstance(style, BaseStyle)


@then('the deleted style is not in the styles collection')
def then_the_deleted_style_is_not_in_the_styles_collection(context):
    document = context.document
    try:
        document.styles['No List']
    except KeyError:
        return
    raise AssertionError('Style not deleted')


@then('the document has one additional style')
def then_the_document_has_one_additional_style(context):
    document = context.document
    style_count = len(document.styles)
    expected_style_count = context.style_count + 1
    assert style_count == expected_style_count


@then('the document has one fewer styles')
def then_the_document_has_one_fewer_styles(context):
    document = context.document
    style_count = len(document.styles)
    expected_style_count = context.style_count - 1
    assert style_count == expected_style_count
