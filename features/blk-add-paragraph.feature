Feature: Add a paragraph of text
  In order to add text to a document
  As an python-docx developer
  I need to add a paragraph

  Scenario: Add a paragraph
     Given a document
      When I add a paragraph
       And I add a run to the paragraph
       And I add text to the run
       And I save the document
      Then the document contains the text I added
