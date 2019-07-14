Feature: Document properties and methods
  In order manipulate a Word document
  As a developer using python-docx
  I need properties and methods on the Document object

  @wip
  Scenario: Document.start_bookmark()
    Given a Document object as document
     When I assign bookmark = document.start_bookmark("Target")
     Then bookmark.name == "Target"
      And bookmark.id is an int
