Feature: Add text to a paragraph, preserving the style of the last text
  In order to easily add new text to the end of a paragraph
  As a python-docx programmer
  I want an easy way to add text to the last run

  Scenario: Add text to an empty paragraph
    Given a paragraph
     Then the paragraph has no content
     When I add text to the paragraph
     Then the paragraph has one run
     And the paragraph has the text I set

  Scenario: Add text of the same style to a non-empty paragraph
    Given a paragraph with some text
    When I add text to the paragraph
    Then the paragraph has one run
    And the paragraph ends with the text I added
    And the initial text is still there

  Scenario: Add text of a different style to a non-empty paragraph
    Given a paragraph with some text
    When I add text of a different style to the paragraph
    Then the paragraph has two runs
    And the second run contains the text I added
    And the second run has the style I specified
