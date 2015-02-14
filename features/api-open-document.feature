Feature: Open a document
  In order work on a document
  As a developer using python-docx
  I need a way to open a document


  Scenario: Open a specified document
    Given I have python-docx installed
     When I call docx.Document() with the path of a .docx file
     Then document is a Document object


  Scenario: Open the default document
    Given I have python-docx installed
     When I call docx.Document() with no arguments
     Then document is a Document object
