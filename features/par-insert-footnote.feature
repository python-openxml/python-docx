Feature: Insert a footnote at the end of a paragraph
  In order to add new footnote at the end of a text (paragraph)
  As a developer using python-docx
  I need a way to add a footnote to the end of a specific paragraph


  Scenario: Add a new footnote to a paragraph in a document without footnotes
    Given a paragraph in a document without footnotes
     When I add a footnote to the paragraphs[1] with text ' NEW FOOTNOTE'
     Then the document contains a footnote with footnote reference id of 1 with text ' NEW FOOTNOTE'
      And len(footnotes) is 3

  Scenario Outline: Add a new footnote to a paragraph in a document containing one footnote before the paragraph and two footnote after
    Given a document with paragraphs[0] containing one, paragraphs[1] containing none, and paragraphs[2] containing two footnotes
     When I add a footnote to the paragraphs[1] with text ' NEW FOOTNOTE'
     Then paragraphs[<parId>] has footnote reference ids of <refIds>, with footnote text <fText>
      And len(footnotes) is 6

    Examples: footnote values per paragraph
      | parId | refIds      | fText                                                                                                |
      | 0     | int(1)      | str(' This is footnote text for the first footnote.')                                                |
      | 1     | int(2)      | str(' NEW FOOTNOTE')                                                                                 |
      | 2     | [3,4]       | [' This is footnote text for the second footnote.',' This is footnote text for the third footnote.'] |
