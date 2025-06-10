"""Step implementations for document comments-related features."""

import datetime as dt

from behave import given, then, when
from behave.runner import Context

from docx import Document
from docx.comments import Comment, Comments
from docx.drawing import Drawing

from helpers import test_docx

# given ====================================================


@given("a Comment object")
def given_a_comment_object(context: Context):
    context.comment = Document(test_docx("comments-rich-para")).comments.get(0)


@given("a Comment object containing an embedded image")
def given_a_comment_object_containing_an_embedded_image(context: Context):
    context.comment = Document(test_docx("comments-rich-para")).comments.get(1)


@given("a Comments object with {count} comments")
def given_a_comments_object_with_count_comments(context: Context, count: str):
    testfile_name = {"0": "doc-default", "4": "comments-rich-para"}[count]
    context.comments = Document(test_docx(testfile_name)).comments


@given("a document having a comments part")
def given_a_document_having_a_comments_part(context: Context):
    context.document = Document(test_docx("comments-rich-para"))


@given("a document having no comments part")
def given_a_document_having_no_comments_part(context: Context):
    context.document = Document(test_docx("doc-default"))


# when =====================================================


@when("I assign para_text = comment.paragraphs[0].text")
def when_I_assign_para_text(context: Context):
    context.para_text = context.comment.paragraphs[0].text


@when("I call comments.get(2)")
def when_I_call_comments_get_2(context: Context):
    context.comment = context.comments.get(2)


# then =====================================================


@then("comment.author is the author of the comment")
def then_comment_author_is_the_author_of_the_comment(context: Context):
    actual = context.comment.author
    assert actual == "Steve Canny", f"expected author 'Steve Canny', got '{actual}'"


@then("comment.comment_id is the comment identifier")
def then_comment_comment_id_is_the_comment_identifier(context: Context):
    assert context.comment.comment_id == 0


@then("comment.initials is the initials of the comment author")
def then_comment_initials_is_the_initials_of_the_comment_author(context: Context):
    initials = context.comment.initials
    assert initials == "SJC", f"expected initials 'SJC', got '{initials}'"


@then("comment.timestamp is the date and time the comment was authored")
def then_comment_timestamp_is_the_date_and_time_the_comment_was_authored(context: Context):
    assert context.comment.timestamp == dt.datetime(2025, 6, 7, 11, 20, 0, tzinfo=dt.timezone.utc)


@then("document.comments is a Comments object")
def then_document_comments_is_a_Comments_object(context: Context):
    document = context.document
    assert type(document.comments) is Comments


@then("I can extract the image from the comment")
def then_I_can_extract_the_image_from_the_comment(context: Context):
    paragraph = context.comment.paragraphs[0]
    run = paragraph.runs[2]
    drawing = next(d for d in run.iter_inner_content() if isinstance(d, Drawing))
    assert drawing.has_picture

    image = drawing.image

    assert image.content_type == "image/jpeg", f"got {image.content_type}"
    assert image.filename == "image.jpg", f"got {image.filename}"
    assert image.sha1 == "1be010ea47803b00e140b852765cdf84f491da47", f"got {image.sha1}"


@then("iterating comments yields {count} Comment objects")
def then_iterating_comments_yields_count_comments(context: Context, count: str):
    comment_iter = iter(context.comments)

    comment = next(comment_iter)
    assert type(comment) is Comment, f"expected a Comment object, got {type(comment)}"

    remaining = list(comment_iter)
    assert len(remaining) == int(count) - 1, "iterating comments did not yield the expected count"


@then("len(comments) == {count}")
def then_len_comments_eq_count(context: Context, count: str):
    actual = len(context.comments)
    expected = int(count)
    assert actual == expected, f"expected len(comments) of {expected}, got {actual}"


@then("para_text is the text of the first paragraph in the comment")
def then_para_text_is_the_text_of_the_first_paragraph_in_the_comment(context: Context):
    actual = context.para_text
    expected = "Text with hyperlink https://google.com embedded."
    assert actual == expected, f"expected para_text '{expected}', got '{actual}'"


@then("the result is a Comment object with id 2")
def then_the_result_is_a_comment_object_with_id_2(context: Context):
    comment = context.comment
    assert type(comment) is Comment, f"expected a Comment object, got {type(comment)}"
    assert comment.comment_id == 2, f"expected comment_id `2`, got '{comment.comment_id}'"
