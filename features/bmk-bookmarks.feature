Feature: Access a bookmark
  In order to operate on document bookmark objects
  As a developer using python-docx
  I need sequence operations on Bookmarks


  Scenario: Bookmarks is a sequence
    Given a Bookmarks object of length 5 as bookmarks
     Then len(bookmarks) == 5
      And bookmarks[1] is a _Bookmark object
      And iterating bookmarks produces 5 _Bookmark objects

  Scenario Outline: Bookmarks.get(bookmark_name)
    Given a Bookmarks object of length 5 as bookmarks
     Then bookmarks.get(<name>) returns bookmark named "<name>" with id <id>

    Examples: Named Bookmarks
        | name               | id |
        | bookmark_body      | 2  |
        | bookmark_endnote   | 1  |
        | bookmark_footer    | 5  |
        | bookmark_footnote  | 0  |
        | bookmark_header    | 4  |
