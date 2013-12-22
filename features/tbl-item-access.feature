Feature: Access table rows, columns, and cells
  In order to query and modify individual table items
  As an python-docx developer
  I need the ability to access table rows, columns, and cells

  Scenario: Access table row collection
     Given a table having two rows
      Then the length of its row collection is 2
       And each item in its row collection is a table row

  Scenario: Access table row by collection index
     Given a table having two rows
      Then I can access the rows by index

  @wip
  Scenario: Access cell collection of table row
     Given a table row having two cells
      Then I can access the cell collection of the row
       And I can get the length of the cell collection
       And I can iterate over the cell collection
       And I can access a collection cell by index
