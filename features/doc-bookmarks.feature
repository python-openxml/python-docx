Feature: Create named bookmark destinations
  In order to navigate generated documents
  As a document author
  I need named targets and range bookmarks

  Scenario: Save a paragraph target
    Given a document with a bookmark on a heading
     When I save and reopen the bookmark document
     Then I can find its heading by bookmark name

  Scenario: Reject a duplicate without replacing the target
    Given a document with a bookmark on a heading
     When I try to reuse that bookmark name
     Then the original bookmark target is preserved
