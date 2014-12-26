Feature: Insert a paragraph before or after a paragraph
  In order to add new content in the middle of an existing document
  As a developer using python-docx
  I need a way to insert a paragraph relative to another paragraph


  Scenario: Add a new paragraph above an existing paragraph
    Given a document containing three paragraphs
     When I insert a paragraph above the second paragraph
     Then the document contains four paragraphs
      And the text of the second paragraph matches the text I set
      And the style of the second paragraph matches the style I set
