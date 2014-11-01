Feature: Access table rows and columns
  In order to query and modify individual table items
  As a developer using python-docx
  I need the ability to access table rows and columns

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
