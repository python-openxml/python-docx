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
     Then the cell collection length of the row(s) indexed by [0,1] is 2
      And the cell collection length of the column(s) indexed by [0,1] is 2


  Scenario: Merge an already merged area
    Given a 4 x 4 table
     When I merge the 2 x 2 topleftmost cells
      And I merge the 3 x 3 topleftmost cells
     Then the cell collection length of the row(s) indexed by [0,1,2] is 2
      And the cell collection length of the column(s) indexed by [0,1,2] is 2


  Scenario: Unsupported merge of an already merged area
    Given a 2 x 2 table
     When I merge the 1 x 2 topleftmost cells
      And I merge the 2 x 1 topleftmost cells
     Then an exception is raised with a detailed error message


  Scenario: Merge resulting in a table reduction (simplification)
    Given a 2 x 2 table
     When I merge the 2 x 2 topleftmost cells
     Then the table has 1 row(s)
      And the table has 1 column(s)