Feature: Add a section heading with text
  In order add a section heading to a document
  As a programmer using the basic python-docx API
  I need a method to add a heading with its text in a single step


  Scenario: Add a heading specifying only its text
    Given a document
     When I add a heading specifying only its text
     Then the style of the last paragraph is 'Heading 1'
      And the last paragraph contains the heading text


  Scenario Outline: Add a heading specifying level
    Given a document
     When I add a heading specifying level=<heading level>
     Then the style of the last paragraph is '<paragraph style>'

   Examples: Heading level styles
     | heading level | paragraph style |
     |       0       | Title           |
     |       1       | Heading 1       |
     |       2       | Heading 2       |
     |       3       | Heading 3       |
     |       4       | Heading 4       |
     |       5       | Heading 5       |
     |       6       | Heading 6       |
     |       7       | Heading 7       |
     |       8       | Heading 8       |
     |       9       | Heading 9       |
