Feature: Add a paragraph with optional text and style
  In order to populate the text of a document
  As a programmer using the basic python-docx API
  I want to add a styled paragraph of text in a single step

  Scenario: Add an empty paragraph
    Given a document
     When I add a paragraph without specifying text or style
     Then the last paragraph is the empty paragraph I added

  Scenario: Add a paragraph specifying its text
    Given a document
     When I add a paragraph specifying its text
     Then the last paragraph contains the text I specified

  Scenario: Add a paragraph specifying its style
    Given a document
     When I add a paragraph specifying its style
     Then the last paragraph has the style I specified
