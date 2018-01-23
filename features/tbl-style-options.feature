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


      #   Scenario Outline: Apply a table style
      #     Given a table having <style> style
      #      When I assign <value> to table.style
      #      Then table.style is styles['<style-name>']
      # 
      #     Examples: Character style transitions
      #       | style       | value                  | style-name   |
      #       | no explicit | Table Grid             | Table Grid   |
      #       | no explicit | styles['Table Grid']   | Table Grid   |
      #       | Table Grid  | Normal Table           | Normal Table |
      #       | Table Grid  | styles['Normal Table'] | Normal Table |
      #       | Table Grid  | None                   | Normal Table |
