Feature: Add a document section
  In order to change page layout mid-document
  As a developer using python-docx
  I need a way to add a new section to a document


  Scenario: Add a landscape section to a portrait document
     Given a single-section document having portrait layout
      When I add an even-page section to the document
       And I change the new section layout to landscape
      Then the document has two sections
       And the first section is portrait
       And the second section is landscape
