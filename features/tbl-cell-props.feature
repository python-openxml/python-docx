Feature: Get and set table cell properties
  In order to format a table cell to my requirements
  As an python-docx developer
  I need a way to get and set the properties of a table cell


  Scenario Outline: Get cell width
    Given a table cell having a width of <width-setting>
     Then the reported width of the cell is <reported-width>

    Examples: Table cell width settings
      | width-setting       | reported-width |
      | no explicit setting | None           |
      | 1 inch              | 1 inch         |


  Scenario Outline: Set cell width
    Given a table cell having a width of <width-setting>
     When I set the cell width to <new-setting>
     Then the reported width of the cell is <reported-width>

    Examples: Table column width values
      | width-setting       | new-setting | reported-width |
      | no explicit setting | 1 inch      | 1 inch         |
      | 2 inches            | 1 inch      | 1 inch         |


  Scenario Outline: Get the row/column index of a cell
    Given a 3 x 3 table
     When I access the cell at the position (<row-index>, <column-index>)
     Then the cell row index value is <row-index>
      And the cell column index value is <column-index>
     
    Examples: Cell position in the table
      | row-index | column-index |
      | 0         | 0            |   
      | 2         | 1            |
      | 1         | 2            |
