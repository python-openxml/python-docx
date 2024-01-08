Feature: Set footnote properties
  In order to change footnote properties of a document
  As a developer using python-docx
  I need a setter for footnote properties

  Scenario Outline: Change footnote properties
     Given a document with footnotes and with all footnotes properties
      When I change footnote property <propName> to <value>
      Then I can access footnote property <propName> with value <value>

     Examples: footnote property names and values
       | propName                            | value      |
       | footnote_position                   | str('beneathText') |
       | footnote_position                   | str('pageBottom')  |
       | footnote_number_format              | str('upperRoman')  |
       | footnote_number_format              | str('decimal')     |
       | footnote_number_format              | str('hex')         |
       | footnote_numbering_start_value      | int(10)            |
       | footnote_numbering_restart_location | str('eachPage')    |
       | footnote_numbering_restart_location | str('eachSect')    |
       | footnote_numbering_restart_location | str('continuous')  |
