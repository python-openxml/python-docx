Feature: Get and set table column widths
  In order to produce properly formatted tables
  As a developer using python-docx
  I need a way to get and set the width of a table's columns


  Scenario Outline: Get existing column width
    Given a table column having a width of <width>
     Then the reported column width is <width-emu>

    Examples: table column width values
      | width               | width-emu   |
      | no explicit setting | None        |
      | 1440                | 914400      |


  Scenario Outline: Set column width
    Given a table column having a width of <width>
     When I set the column width to <new-width>
     Then the reported column width is <width-emu>

    Examples: table column width values
      | width               | new-width | width-emu |
      | no explicit setting | None      | None      |
      | no explicit setting | 914400    | 914400    |
      | 1440                | None      | None      |
      | 1440                | 914400    | 914400    |
      | 1440                | 424497    | 424180    |
