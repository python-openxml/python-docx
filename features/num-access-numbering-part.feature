Feature: Access the document numbering part
  In order to operate on numbering settings
  As a developer using python-docx
  I need access to the numbering part of the document


  Scenario: Get an existing numbering part from document
    Given a document having a numbering part
     When I get the numbering part from the document
     Then the numbering part has the expected numbering definitions
