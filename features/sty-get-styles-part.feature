Feature: Get the document styles part
  In order to query and modify styles
  As a programmer using the advanced python-docx API
  I need access to the styles part of the document

  Scenario: Get an existing styles part from document
    Given a document having a styles part
     When I get the styles part from the document
     Then the styles part has the expected number of style definitions
