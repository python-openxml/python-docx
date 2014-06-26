Feature: Access run content
  In order to discover or locate existing inline content
  As a developer using python-docx
  I need ways to access the run content


  Scenario: Get run content as Python text
    Given a run having mixed text content
     Then the text of the run represents the textual run content
