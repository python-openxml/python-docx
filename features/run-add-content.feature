Feature: Add content to a run
  In order to populate a run with varied content
  As a developer using python-docx
  I need a way to add each of the run content elements to a run


  Scenario: Add a tab
    Given a run
     When I add a tab
     Then the tab appears at the end of the run
