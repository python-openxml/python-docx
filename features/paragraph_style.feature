Feature: Each paragraph has a read/write style
  In order use the stylesheet capability built into Word
  As an python-docx developer
  I need to get and set the style of a paragraph

  Scenario: Set the style of a paragraph
     Given a new document created from the default template
      When I add a new paragraph to the body
       And I set the paragraph style
       And I save the document
      Then the paragraph has the style I set
