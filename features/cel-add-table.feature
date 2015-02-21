Feature: Add a table into a table cell
  In order to nest a table within a table cell
  As a developer using python-docx
  I need a way to add a table to a table cell


  Scenario: Add a table into a table cell
    Given a table cell
     When I add a 2 x 2 table into the first cell
     Then cell.tables[0] is a 2 x 2 table
      And the width of each column is 1.5375 inches
      And the width of each cell is 1.5375 inches
