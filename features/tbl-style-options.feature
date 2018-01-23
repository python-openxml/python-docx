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


      #   Scenario Outline: Get the "First Column" table style option value
      #     Given a table
      #       Then table.show_header_column either True or False and reflects the
      #            state of the "First Column" checkox in the Table Style Options
      # 
      # 
      #   Scenario Outline: Get the "Last Column" table style option value
      #     Given a table
      #       Then table.show_last_column either True or False and reflects the
      #            state of the "Last Column" checkox in the Table Style Options
      # 
      # 
      #   Scenario Outline: Get the "Banded Rows" table style option value
      #     Given a table
      #       Then table.show_banded_rows either True or False and reflects the
      #            state of the "Banded Rows" checkox in the Table Style Options
      # 
      # 
      #   Scenario Outline: Get the "Banded Columns" table style option value
      #     Given a table
      #       Then table.show_banded_columns either True or False and reflects the
      #            state of the "Banded Columns" checkox in the Table Style Options
      # 
      # 
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
