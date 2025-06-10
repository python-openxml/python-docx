Feature: Get comment properties
  In order to characterize comments by their metadata
  As a developer using python-docx
  I need methods to access comment metadata properties


  Scenario: Comment.id
    Given a Comment object
     Then comment.comment_id is the comment identifier


  Scenario: Comment.author
    Given a Comment object
     Then comment.author is the author of the comment


  @wip
  Scenario: Comment.initials
    Given a Comment object
     Then comment.initials is the initials of the comment author


  @wip
  Scenario: Comment.timestamp
    Given a Comment object
     Then comment.timestamp is the date and time the comment was authored


  @wip
  Scenario: Comment.paragraphs[0].text
    Given a Comment object
     When I assign para_text = comment.paragraphs[0].text
     Then para_text is the text of the first paragraph in the comment


  @wip
  Scenario: Retrieve embedded image from a comment
    Given a Comment object containing an embedded image
     Then I can extract the image from the comment
