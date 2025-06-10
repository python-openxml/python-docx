Feature: Comment mutations
  In order to add and modify the content of a comment
  As a developer using python-docx
  I need mutation methods on Comment objects


  Scenario: Comments.add_comment()
    Given a Comments object with 0 comments
     When I assign comment = comments.add_comment()
     Then comment.comment_id == 0
      And len(comment.paragraphs) == 1
      And comment.paragraphs[0].style.name == "CommentText"
      And len(comments) == 1
      And comments.get(0) == comment


  Scenario: Comments.add_comment() specifying author and initials
    Given a Comments object with 0 comments
     When I assign comment = comments.add_comment(author="John Doe", initials="JD")
     Then comment.author == "John Doe"
      And comment.initials == "JD"


  Scenario: Comment.add_paragraph() specifying text and style
    Given a default Comment object
     When I assign paragraph = comment.add_paragraph(text, style)
     Then len(comment.paragraphs) == 2
      And paragraph.text == text
      And paragraph.style == style
      And comment.paragraphs[-1] == paragraph


  Scenario: Comment.add_paragraph() not specifying text or style
    Given a default Comment object
     When I assign paragraph = comment.add_paragraph()
     Then len(comment.paragraphs) == 2
      And paragraph.text == ""
      And paragraph.style == "CommentText"
      And comment.paragraphs[-1] == paragraph


  Scenario: Add image to comment
    Given a default Comment object
     When I assign paragraph = comment.add_paragraph()
      And I assign run = paragraph.add_run()
      And I call run.add_picture()
     Then run.iter_inner_content() yields a single Picture drawing


  Scenario: update Comment.author
    Given a Comment object
     When I assign "Jane Smith" to comment.author
     Then comment.author == "Jane Smith"


  Scenario: update Comment.initials
    Given a Comment object
     When I assign "JS" to comment.initials
     Then comment.initials == "JS"
