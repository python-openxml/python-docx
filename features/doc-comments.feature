Feature: Document.comments
  In order to operate on comments added to a document
  As a developer using python-docx
  I need access to the comments collection for the document
  And I need methods allowing access to the comments in the collection


  Scenario Outline: Access document comments
    Given a document having <a-or-no> comments part
     Then document.comments is a Comments object

    Examples: having a comments part or not
      | a-or-no |
      | a       |
      | no      |


  Scenario Outline: Comments.__len__()
    Given a Comments object with <count> comments
     Then len(comments) == <count>

    Examples: len(comments) values
      | count |
      | 0    |
      | 4    |


  Scenario: Comments.__iter__()
    Given a Comments object with 4 comments
     Then iterating comments yields 4 Comment objects


  Scenario: Comments.get()
    Given a Comments object with 4 comments
     When I call comments.get(2)
     Then the result is a Comment object with id 2
