Feature: Add a comment to a document
  In order add a comment to a document
  As a developer using python-docx
  I need a way to add a comment specifying both its content and its reference


  Scenario: Document.add_comment(runs, text, author, initials)
    Given a document having a comments part
     When I assign comment = document.add_comment(runs, "A comment", "John Doe", "JD")
     Then comment is a Comment object
      And comment.text == "A comment"
      And comment.author == "John Doe"
      And comment.initials == "JD"
