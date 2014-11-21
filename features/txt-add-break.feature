Feature: Add a line, page, or column break
  In order to control the flow of text in a document
  As a developer using python-docx
  I need the ability to add a line, page, or column break

  Scenario: Add a line break
    Given a run
     When I add a line break
     Then the last item in the run is a break
      And it is a line break

  Scenario: Add a page break
    Given a run
     When I add a page break
     Then the last item in the run is a break
      And it is a page break

  Scenario: Add a column break
    Given a run
     When I add a column break
     Then the last item in the run is a break
      And it is a column break
