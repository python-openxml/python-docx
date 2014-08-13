Feature: Merge table cells
  In order to format a table layout to my requirements
  As an python-docx developer
  I need a way to merge the cells of a table


  Scenario: Merge cells horizontally
    Given a 2 x 2 table
     When I merge the cells of the first row
     Then the lenght of the first row cells collection is reported as 1


  Scenario: Merge cells vertically
    Given a 2 x 2 table
     When I merge the cells of the first column
     Then the length of the first column cells collection is reported as 1


  Scenario: Merge cells both horizontally and vertically
    Given a 3 x 3 table
     When I merge the 2 x 2 topleftmost cells
     Then the length of the first two rows cells collection is reported as 2
      And the length of the first two columns cells collection is reported as 2


  Scenario: Merge a previously merged area
    Given a 4 x 4 table with the 2 x 2 topleftmost cells already merged
     When I merge the 3 x 3 topleftmost cells
     Then the length of the first three rows cells collection is reported as 2
      And the length of the first three columns cells collection is reported 
          as 2


  Scenario: Unsupported merge of a previously merged area
    Given a 2 x 2 cells table with the first row cells already merged
     When I try to merge the cells from the first column
     Then an exception is raised with a detailed error message

  Scenario: Merge resulting in a table reduction (simplification)
    Given a 2 x 2 table
     When I merge all the cells of the table
     Then the resulting table is contains exactly one cell