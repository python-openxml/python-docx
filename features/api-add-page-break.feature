Feature: Add a page break
  In order to force a page break at a particular location
  As a programmer using the basic python-docx API
  I need a method that adds a hard page break on its own paragraph

  Scenario: Add a hard page break paragraph
    Given a document
     When I add a page break to the document
     Then the last paragraph contains only a page break
