Feature: Access table cells
  In order to access individual cells in a table
  As a developer using python-docx
  I need a way to access a cell from a table, row, or column

  Scenario Outline: Access cell sequence of a row
     Given a 3x3 table having <span-state>
      Then the row cells text is <expected-text>

    Examples: Reported row cell contents
      | span-state         | expected-text     |
      | only uniform cells | 1 2 3 4 5 6 7 8 9 |
      | a horizontal span  | 1 2 3 4 4 6 7 8 9 |
      | a vertical span    | 1 2 3 4 5 6 7 5 9 |
      | a combined span    | 1 2 3 4 4 6 4 4 9 |


  Scenario Outline: Access cell sequence of a column
     Given a 3x3 table having <span-state>
      Then the column cells text is <expected-text>

    Examples: Reported column cell contents
      | span-state         | expected-text     |
      | only uniform cells | 1 4 7 2 5 8 3 6 9 |
      | a horizontal span  | 1 4 7 2 4 8 3 6 9 |
      | a vertical span    | 1 4 7 2 5 5 3 6 9 |
      | a combined span    | 1 4 4 2 4 4 3 6 9 |


  Scenario Outline: Access cell by row and column index
     Given a 3x3 table having <span-state>
      Then table.cell(<row>, <col>).text is <expected-text>

    Examples: Reported cell text
      | span-state         | row | col | expected-text |
      | only uniform cells |  1  |  1  |       5       |
      | a horizontal span  |  1  |  1  |       4       |
      | a vertical span    |  2  |  1  |       5       |
      | a combined span    |  2  |  1  |       4       |
