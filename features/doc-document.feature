Feature: Document properties and methods
  In order to manipulate a Word document
  As a developer using python-docx
  I need properties and methods on the Document object

  Scenario: Document.start_bookmark()
    Given a Document object as document
     When I assign bookmark = document.start_bookmark("Target")
     Then bookmark.name == "Target"
      And bookmark.id is an int


  Scenario: Document.end_bookmark()
    Given a Document object as document
     When I assign bookmark = document.start_bookmark("Target")
      And I end bookmark by calling document.end_bookmark(bookmark)
      # ---bookmark can only be looked up by name if it is closed---
     Then document.bookmarks.get("Target").name == "Target"
