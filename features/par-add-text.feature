Feature: Add text to a paragraph, preserving the style of the last text
  In order to easily add new text to the end of a paragraph
  As a python-docx programmer
  I want an easy way to add text to the last run

  Scenario: Add text to an empty paragraph
    Given a paragraph
     Then the paragraph has no content
     When I add text to the paragraph
     Then the paragraph has the text I added

  Scenario: Add text to a non-empty paragraph with a style on the last run
    Given a paragraph with some text and a style on the last run
    When I add text to the paragraph
    Then the paragraph has the same amount of runs
    And the paragraph ends with the text I added
    And the initial text is still there
    And the last run still has the same style
