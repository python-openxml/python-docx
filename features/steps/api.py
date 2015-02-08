# encoding: utf-8

"""
Step implementations for basic API features
"""

from behave import then, when

from docx.shared import Inches
from docx.table import Table

from helpers import test_file


# when ====================================================

@when('I add a 2 x 2 table specifying only row and column count')
def when_add_2x2_table_specifying_only_row_and_col_count(context):
    document = context.document
    document.add_table(rows=2, cols=2)


@when('I add a 2 x 2 table specifying style \'{style_name}\'')
def when_add_2x2_table_specifying_style_name(context, style_name):
    document = context.document
    document.add_table(rows=2, cols=2, style=style_name)


@when('I add a heading specifying level={level_str}')
def when_add_heading_specifying_level(context, level_str):
    level = int(level_str)
    document = context.document
    document.add_heading(level=level)


@when('I add a heading specifying only its text')
def when_add_heading_specifying_only_its_text(context):
    document = context.document
    context.heading_text = 'Spam vs. Eggs'
    document.add_heading(context.heading_text)


@when('I add a page break to the document')
def when_add_page_break_to_document(context):
    document = context.document
    document.add_page_break()


@when('I add a paragraph specifying its style as a {kind}')
def when_I_add_a_paragraph_specifying_its_style_as_a(context, kind):
    document = context.document
    style = context.style = document.styles['Heading 1']
    style_spec = {
        'style object': style,
        'style name':   'Heading 1',
    }[kind]
    document.add_paragraph(style=style_spec)


@when('I add a paragraph specifying its text')
def when_add_paragraph_specifying_text(context):
    document = context.document
    context.paragraph_text = 'foobar'
    document.add_paragraph(context.paragraph_text)


@when('I add a paragraph without specifying text or style')
def when_add_paragraph_without_specifying_text_or_style(context):
    document = context.document
    document.add_paragraph()


@when('I add a picture specifying 1.75" width and 2.5" height')
def when_add_picture_specifying_width_and_height(context):
    document = context.document
    context.picture = document.add_picture(
        test_file('monty-truth.png'),
        width=Inches(1.75), height=Inches(2.5)
    )


@when('I add a picture specifying a height of 1.5 inches')
def when_add_picture_specifying_height(context):
    document = context.document
    context.picture = document.add_picture(
        test_file('monty-truth.png'), height=Inches(1.5)
    )


@when('I add a picture specifying a width of 1.5 inches')
def when_add_picture_specifying_width(context):
    document = context.document
    context.picture = document.add_picture(
        test_file('monty-truth.png'), width=Inches(1.5)
    )


@when('I add a picture specifying only the image file')
def when_add_picture_specifying_only_image_file(context):
    document = context.document
    context.picture = document.add_picture(test_file('monty-truth.png'))


# then =====================================================

@then('the document contains a 2 x 2 table')
def then_document_contains_2x2_table(context):
    document = context.document
    table = document.tables[-1]
    assert isinstance(table, Table)
    assert len(table.rows) == 2
    assert len(table.columns) == 2
    context.table_ = table


@then('the last paragraph contains only a page break')
def then_last_paragraph_contains_only_a_page_break(context):
    document = context.document
    p = document.paragraphs[-1]
    assert len(p.runs) == 1
    assert len(p.runs[0]._r) == 1
    assert p.runs[0]._r[0].type == 'page'


@then('the last paragraph contains the heading text')
def then_last_p_contains_heading_text(context):
    document = context.document
    text = context.heading_text
    p = document.paragraphs[-1]
    assert p.text == text


@then('the last paragraph contains the text I specified')
def then_last_p_contains_specified_text(context):
    document = context.document
    text = context.paragraph_text
    p = document.paragraphs[-1]
    assert p.text == text


@then('the last paragraph has the style I specified')
def then_the_last_paragraph_has_the_style_I_specified(context):
    document, expected_style = context.document, context.style
    paragraph = document.paragraphs[-1]
    assert paragraph.style == expected_style


@then('the last paragraph is the empty paragraph I added')
def then_last_p_is_empty_paragraph_added(context):
    document = context.document
    p = document.paragraphs[-1]
    assert p.text == ''


@then('the style of the last paragraph is \'{style_name}\'')
def then_the_style_of_the_last_paragraph_is_style(context, style_name):
    document = context.document
    paragraph = document.paragraphs[-1]
    assert paragraph.style.name == style_name, (
        'got %s' % paragraph.style.name
    )
