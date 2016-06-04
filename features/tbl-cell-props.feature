Feature: Get and set table cell properties
  In order to format a table cell to my requirements
  As a developer using python-docx
  I need a way to get and set the properties of a table cell


  @wip
  Scenario Outline: Get Cell.vertical_alignment
    Given a table cell having vertical alignment of <state>
     Then cell.vertical_alignment is <value>

    Examples: Cell.vertical_alignment value cases
      | state               | value  |
      | no explicit setting | None   |
      | bottom              | BOTTOM |
      | center              | CENTER |
      | top                 | TOP    |


  @wip
  Scenario Outline: Set Cell.vertical_alignment
    Given a table cell having vertical alignment of <state>
     When I assign <value> to cell.vertical_alignment
     Then cell.vertical_alignment is <value>

    Examples: table cell vertical alignment values
      | state               | value  |
      | no explicit setting | BOTTOM |
      | bottom              | CENTER |
      | center              | TOP    |
      | top                 | None   |
      | no explicit setting | None   |


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
