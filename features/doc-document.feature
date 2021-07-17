Feature: Document properties and methods
  In order to manipulate a Word document
  As a developer using python-docx
  I need properties and methods on the Document object

  Scenario: Document.start_bookmark()
    Given a Document object as document
     When I assign bookmark = document.start_bookmark("Target")
     Then bookmark.name == "Target"
      And bookmark.id is an int

  @wip
  Scenario: Document.end_bookmark()
    Given a Document object as document
      And an open Bookmark object named "Target" as bookmark
     Then bookmark == document.end_bookmark(bookmark)
      And bookmark == document.bookmarks.get("Target")
