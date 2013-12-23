Feature: Access table rows, columns, and cells
  In order to query and modify individual table items
  As an python-docx developer
  I need the ability to access table rows, columns, and cells

  Scenario: Access table row collection
     Given a table having two rows
      Then I can access the row collection of the table
       And the length of the row collection is 2

  Scenario: Access row in row collection
     Given a row collection having two rows
      Then I can iterate over the row collection
       And I can access a collection row by index

  Scenario: Access table column collection
     Given a table having two columns
      Then I can access the column collection of the table
       And the length of the column collection is 2

  Scenario: Access column in column collection
     Given a column collection having two columns
      Then I can iterate over the column collection
       And I can access a collection column by index

  Scenario: Access cell collection of table column
     Given a table column having two cells
      Then I can access the cell collection of the column
       And I can get the length of the column cell collection

  Scenario: Access cell collection of table row
     Given a table row having two cells
      Then I can access the cell collection of the row
       And I can get the length of the row cell collection

  Scenario: Access cell in column cell collection
     Given a column cell collection having two cells
      Then I can iterate over the column cells
       And I can access a column cell by index

  Scenario: Access cell in row cell collection
     Given a row cell collection having two cells
      Then I can iterate over the row cells
       And I can access a row cell by index

  Scenario: Access cell in table
     Given a table having two rows
      Then I can access a cell using its row and column indices
