Feature: Access document footnotes
  In order to operate on an individual footnote
  As a developer using python-docx
  I need access to each footnote in the footnote collection of a document
  I need access to footnote properties

  Scenario: Access footnote from a document containing footnotes
     Given a document with 3 footnotes and 2 default footnotes
      Then len(footnotes) is 5
       And I can access a footnote by footnote reference id
       And I can access a paragraph in a specific footnote

  Scenario: Access a footnote from document with an invalid footnote reference id
    Given a document with footnotes
     When I try to access a footnote with invalid reference id
     Then it trows an IndexError

  Scenario Outline: Access footnote properties
     Given a document with footnotes and with all footnotes properties
      Then I can access footnote property <propName> with value <value>

     Examples: footnote property names and values
       | propName                            | value             |
       | footnote_position                   | str('pageBottom') |
       | footnote_number_format              | str('lowerRoman') |
       | footnote_numbering_start_value      | int(1)            |
       | footnote_numbering_restart_location | str('continuous') |

  Scenario Outline: Access footnotes and footnote properties in a document without footnotes
    Given a document without footnotes
      # there are always 2 default footnotes with footnote reference id of -1 and 0
      Then len(footnotes) is 2
       And I can access footnote property <propName> with value <value>

     Examples: footnote property names and values
       | propName                            | value      |
       | footnote_position                   | None       |
       | footnote_number_format              | None       |
       | footnote_numbering_start_value      | None       |
       | footnote_numbering_restart_location | None       |
