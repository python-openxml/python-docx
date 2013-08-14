Feature: Add a paragraph of text
  In order to add text to a document
  As an python-docx developer
  I need to add a paragraph

  @wip
  Scenario: Add a paragraph to a document created from the default template
     Given a new document created from the default template
      When I add a new paragraph to the body
       And I add a new run to the paragraph
       And I add new text to the run
       And I save the document
      Then the document contains the text I added
