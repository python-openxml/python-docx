Feature: Access paragraph footnotes
  In order to operate on an individual footnote
  As a developer using python-docx
  I need access to every footnote if present in s specific paragraph


  Scenario Outline: Access all footnote text from a paragraph that might contain a footnote
    Given a document with paragraphs[0] containing one, paragraphs[1] containing none, and paragraphs[2] containing two footnotes
     Then paragraphs[<parId>] has footnote reference ids of <refIds>, with footnote text <fText>

    Examples: footnote values per paragraph
      | parId | refIds      | fText                                                                                                 |
      | 0     | int(1)      | str(' This is footnote text for the first footnote.')                                                 |
      | 1     | None        | None                                                                                                  |
      | 2     | [2,3]       | [' This is footnote text for the second footnote.', ' This is footnote text for the third footnote.'] |
