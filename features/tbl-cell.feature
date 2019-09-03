Feature: Get and set table cell properties
  In order to format a table cell to my requirements
  As a developer using python-docx
  I need a way to get and set the properties of a table cell


  Scenario Outline: Get _Cell.vertical_alignment
    Given a _Cell object with <state> vertical alignment as cell
     Then cell.vertical_alignment is <value>

    Examples: Cell.vertical_alignment value cases
      | state     | value                    |
      | inherited | None                     |
      | bottom    | WD_ALIGN_VERTICAL.BOTTOM |
      | center    | WD_ALIGN_VERTICAL.CENTER |


  Scenario Outline: Set Cell.vertical_alignment
    Given a _Cell object with <state> vertical alignment as cell
     When I assign <value> to cell.vertical_alignment
     Then cell.vertical_alignment is <value>

    Examples: Cell.vertical_alignment assignment cases
      | state     | value                    |
      | inherited | WD_ALIGN_VERTICAL.BOTTOM |
      | bottom    | WD_ALIGN_VERTICAL.CENTER |
      | center    | None                     |
      | inherited | None                     |


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

    Examples: table column width values
      | width-setting       | new-setting | reported-width |
      | no explicit setting | 1 inch      | 1 inch         |
      | 2 inches            | 1 inch      | 1 inch         |
