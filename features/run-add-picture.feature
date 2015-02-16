Feature: Add picture to a run
  In order to place an inline picture at an arbitrary place in a document
  As a developer using python-docx
  I need a way to add a picture to a run


  Scenario: Add a picture to a body paragraph run
    Given a run
     When I add a picture to the run
     Then the picture appears at the end of the run
      And the document contains the inline picture


  Scenario Outline: Add a picture to a run in a table cell
    Given a run inside a table cell retrieved from <cell-source>
     When I add a picture to the run
     Then the picture appears at the end of the run
      And the document contains the inline picture

    Examples: Table cell sources
      | cell-source        |
      | Table.cell         |
      | Table.row.cells    |
      | Table.column.cells |
