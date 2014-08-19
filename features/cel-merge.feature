Feature: Merge table cells
  In order to format a table layout to my requirements
  As an python-docx developer
  I need a way to merge the cells of a table


  Scenario: Merge cells horizontally
    Given a 2 x 2 table
     When I merge the 1 x 2 topleftmost cells
     Then the cell collection length of the row(s) indexed by [0] is 1


  Scenario: Merge cells vertically
    Given a 2 x 2 table
     When I merge the 2 x 1 topleftmost cells
     Then the cell collection length of the column(s) indexed by [0] is 1


  Scenario: Merge cells both horizontally and vertically
    Given a 3 x 3 table
     When I merge the 2 x 2 topleftmost cells
     Then the cell collection length of the row(s) indexed by [0] is 2
      And the cell collection length of the row(s) indexed by [1] is 1
      And the cell collection length of the column(s) indexed by [0] is 2
      And the cell collection length of the column(s) indexed by [1] is 1


  Scenario Outline: Error when attempting to merge cells from different tables
    Given two cells from two different tables
     When I attempt to merge the cells
     Then a <exception-type> exception is raised with a detailed <err-message>

    Examples: Exception type and error message variables
      | exception-type | err-message                               |
      | ValueError     | Cannot merge cells from different tables. |
