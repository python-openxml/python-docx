Feature: Add a run with optional text and style
  In order to add distinctively formatted text to a paragraph
  As a python-docx programmer
  I want a way to add a styled run of text in a single step


  Scenario: Add a run specifying its text
    Given a paragraph
     When I add a run specifying its text
     Then the run contains the text I specified


  Scenario: Add a run specifying its style
    Given a paragraph
     When I add a run specifying the character style Emphasis
     Then run.style is styles['Emphasis']
