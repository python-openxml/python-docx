"""Step implementations for document comments-related features."""

from behave import given, then, when
from behave.runner import Context

from docx import Document
from docx.comments import Comment, Comments

from helpers import test_docx

# given ====================================================


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


@when("I call comments.get(2)")
def when_I_call_comments_get_2(context: Context):
    context.comment = context.comments.get(2)


# then =====================================================


@then("document.comments is a Comments object")
def then_document_comments_is_a_Comments_object(context: Context):
    document = context.document
    assert type(document.comments) is Comments


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


@then("the result is a Comment object with id 2")
def then_the_result_is_a_comment_object_with_id_2(context: Context):
    comment = context.comment
    assert type(comment) is Comment, f"expected a Comment object, got {type(comment)}"
    assert comment.comment_id == 2, f"expected comment_id `2`, got '{comment.comment_id}'"
