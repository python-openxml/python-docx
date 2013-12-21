Feature: Each paragraph has a read/write style
  In order to use the stylesheet capability built into Word
  As an python-docx developer
  I need the ability to get and set the style of a paragraph

  Scenario: Set the style of a paragraph
     Given a paragraph
      When I set the paragraph style
       And I save the document
      Then the paragraph has the style I set
