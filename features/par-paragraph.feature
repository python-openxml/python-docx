Feature: Paragraph properties and methods
  In order to manipulate a paragraph within a Word docment
  As a developer using python-docx
  I need properties and methods on the Paragraph object


  Scenario: Paragraph.start_bookmark()
    Given a Paragraph object as paragraph
     When I assign bookmark = paragraph.start_bookmark("Target")
     Then bookmark.name == "Target"
      And bookmark.id is an int


  Scenario: Paragraph.end_bookmark()
    Given a Paragraph object as paragraph
     When I assign bookmark = paragraph.start_bookmark("Target")
      And I end bookmark by calling paragraph.end_bookmark(bookmark)
     Then document.bookmarks.get("Target").name == "Target"
