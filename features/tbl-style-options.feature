Feature: Query and apply table style options
  In order to maintain consistent formatting of tables
  As a developer using python-docx
  I need the ability to get and set the table style options


  Scenario Outline: Get the "Header Row" table style option value
    Given a table having a Header Row setting of <header_row>
    Then table.show_header_row is <setting>

    Examples: table Header Row settings
      | header_row | setting |
      | True       | True    |
      | False      | False   |


  Scenario Outline: Get the "Total Row" table style option value
    Given a table having a Total Row setting of <total_row>
      Then table.show_total_row is <setting>

    Examples: table Total Row settings
      | total_row  | setting |
      | True       | True    |
      | False      | False   |


  Scenario Outline: Get the "First Column" table style option value
    Given a table having a First Column setting of <header_column>
      Then table.show_header_column is <setting>

    Examples: table First Column settings
      | header_column | setting |
      | True          | True    |
      | False         | False   |


  Scenario Outline: Get the "Last Column" table style option value
    Given a table having a Last Column setting of <last_column>
      Then table.show_last_column is <setting>

    Examples: table Last Column settings
      | last_column | setting |
      | True        | True    |
      | False       | False   |


  Scenario Outline: Get the "Banded Rows" table style option value
    Given a table having a Banded Rows setting of <banded_rows>
      Then table.show_banded_rows is <setting>

    Examples: table Banded Rows settings
      | banded_rows | setting |
      | True        | False   |
      | False       | True    |


  Scenario Outline: Get the "Banded Columns" table style option value
    Given a table having a Banded Columns setting of <banded_columns>
      Then table.show_banded_columns is <setting>

    Examples: table Banded Columns settings
      | banded_columns | setting |
      | True        | False   |
      | False       | True    |


  Scenario Outline: Control the "Header Row" table style option value
    Given a table having a Header Row setting of <header_row>
     When I assign <updated_value> to table.show_header_row
     Then table.show_header_row is <value>

    Examples: table Header Row settings
      | header_row | updated_value | value  |
      | True       | True          | True   |
      | True       | False         | False  |
      | False      | True          | True   |
      | False      | False         | False  |


  Scenario Outline: Control the "Total Row" table style option value
    Given a table having a Total Row setting of <total_row>
     When I assign <updated_value> to table.show_total_row
     Then table.show_total_row is <value>

    Examples: table Total Row settings
      | total_row  | updated_value | value  |
      | True       | True          | True   |
      | True       | False         | False  |
      | False      | True          | True   |
      | False      | False         | False  |


  Scenario Outline: Control the "First Column" table style option value
    Given a table having a First Column setting of <header_column>
     When I assign <updated_value> to table.show_header_column
     Then table.show_header_column is <value>

    Examples: table First Column settings
      | first_column  | updated_value | value  |
      | True          | True          | True   |
      | True          | False         | False  |
      | False         | True          | True   |
      | False         | False         | False  |


  Scenario Outline: Control the "Last Column" table style option value
    Given a table having a Last Column setting of <last_column>
     When I assign <updated_value> to table.show_last_column
     Then table.show_last_column is <value>

    Examples: table Last Column settings
      | last_column   | updated_value | value  |
      | True          | True          | True   |
      | True          | False         | False  |
      | False         | True          | True   |
      | False         | False         | False  |


  Scenario Outline: Control the "Banded Rows" table style option value
    Given a table having a Banded Rows setting of <banded_rows>
     When I assign <updated_value> to table.show_banded_rows
     Then table.show_banded_rows is <value>

    Examples: table Banded Rows settings
      | banded_rows   | updated_value | value  |
      | True          | True          | False  |
      | True          | False         | True   |
      | False         | True          | False  |
      | False         | False         | True   |


  Scenario Outline: Control the "Banded Columns" table style option value
    Given a table having a Banded Columns setting of <banded_columns>
     When I assign <updated_value> to table.show_banded_columns
     Then table.show_banded_columns is <value>

    Examples: table Banded Columns settings
      | banded_columns | updated_value | value  |
      | True           | True          | False  |
      | True           | False         | True   |
      | False          | True          | False  |
      | False          | False         | True   |
