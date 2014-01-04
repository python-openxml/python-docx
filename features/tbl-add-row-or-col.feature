Feature: Add a row or column to a table
  In order to extend an existing table
  As an python-docx developer
  I need methods to add a row or column

  Scenario: Add a row to a table
     Given a 2 x 2 table
      When I add a row to the table
      Then the table has 3 rows
       And the new row has 2 cells

  Scenario: Add a column to a table
     Given a 2 x 2 table
      When I add a column to the table
      Then the table has 3 columns
       And the new column has 2 cells
