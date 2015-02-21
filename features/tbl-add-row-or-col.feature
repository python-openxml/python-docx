Feature: Add a row or column to a table
  In order to extend an existing table
  As a developer using python-docx
  I need methods to add a row or column


  Scenario: Add a row to a table
     Given a 2 x 2 table
      When I add a row to the table
      Then the table has 3 rows
       And the new row has 2 cells
       And the width of each cell is 3.0 inches


  Scenario: Add a column to a table
     Given a 2 x 2 table
      When I add a 1.0 inch column to the table
      Then the table has 3 columns
       And the new column has 2 cells
       And the new column is 1.0 inches wide
