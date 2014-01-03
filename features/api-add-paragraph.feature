Feature: Add a paragraph with optional text and style
  In order to populate the text of a document
  As a programmer using the basic python-docx API
  I want to add a styled paragraph of text in a single step

  @wip
  Scenario: Add an empty paragraph
    Given a document
     When I add a paragraph without specifying text or style
     Then the last paragraph is the empty paragraph I added

  @wip
  Scenario: Add a paragraph specifying its text
    Given a document
     When I add a paragraph spefifying its text
     Then the last paragraph contains the text I specified

  @wip
  Scenario: Add a paragraph specifying its style
    Given a document
     When I add a paragraph spefifying its style
     Then the style of the last paragraph is the style I specified
