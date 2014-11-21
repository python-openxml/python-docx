Feature: Add a table
  In order to fulfill a requirement for a table in a document
  As a developer using python-docx
  I need the ability to add a table

  Scenario: Access a table
     Given a document containing a table
      Then I can access the table

  Scenario: Add a table
     Given a document
      When I add a table
      Then the new table appears in the document
