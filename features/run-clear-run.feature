Feature: Remove the content of a run
  In order to edit the content of a run while preserving its formatting
  As a developer using python-docx
  I need a way to clear the content of a run


  Scenario: Clear run content
    Given a run having known text and formatting
     When I clear the run
     Then the run contains no text
      But the run formatting is preserved
