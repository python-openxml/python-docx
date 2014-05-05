Feature: Each run has a read/write style
  In order to use the stylesheet capability built into Word
  As an python-docx developer
  I need the ability to get and set the character style of a run


  Scenario Outline: Get the character style of a run
    Given a run having style <char style>
     Then the style of the run is <char style>

    Examples: Character styles
      | char style |
      | None       |
      | Emphasis   |
      | Strong     |


  Scenario Outline: Set the style of a run
    Given a run having style <char style>
     When I set the character style of the run to <new char style>
     Then the style of the run is <new char style>

    Examples: Character style transitions
      | char style | new char style |
      | None       | None           |
      | None       | Emphasis       |
      | Emphasis   | None           |
      | Emphasis   | Emphasis       |
      | Emphasis   | Strong         |
