Feature: Add a paragraph of text
  In order to populate the text of a document
  As a developer using python-docx
  I need the ability to add a paragraph

  Scenario: Add a paragraph using low-level text API
    Given a document
     When I add a paragraph
      And I add a run to the paragraph
      And I add text to the run
      And I save the document
     Then the document contains the text I added
