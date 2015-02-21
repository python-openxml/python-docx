Feature: Add a heading paragraph
  In order add a heading to a document
  As a developer using python-docx
  I need a way to add a heading with its text and level in a single step


  Scenario: Add a heading specifying only its text
    Given a document having built-in styles
     When I add a heading specifying only its text
     Then the style of the last paragraph is 'Heading 1'
      And the last paragraph contains the heading text


  Scenario Outline: Add a heading specifying level
    Given a document having built-in styles
     When I add a heading specifying level=<level>
     Then the style of the last paragraph is '<style>'

   Examples: Heading level styles
     | level | style     |
     |   0   | Title     |
     |   1   | Heading 1 |
     |   2   | Heading 2 |
     |   5   | Heading 5 |
     |   9   | Heading 9 |
