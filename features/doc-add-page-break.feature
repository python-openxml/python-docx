Feature: Add a page break
  In order to force a page break at a particular location
  As a developer using the python-docx
  I need a way to add a hard page break on its own paragraph


  Scenario: Add a hard page break paragraph
    Given a blank document
     When I add a page break to the document
     Then the last paragraph contains only a page break
