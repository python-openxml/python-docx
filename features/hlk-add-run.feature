Feature: Append runs to a hyperlink
  In order to create a formatted hyperlink label
  As a developer using python-docx
  I need to append runs using the existing text and character style APIs

  Scenario: Append individually formatted runs
    Given an existing hyperlink for authoring
     When I append formatted runs to the hyperlink
     Then the appended runs retain their text and formatting after saving

  Scenario: Append an empty run for a picture
    Given an existing hyperlink for authoring
     When I append a picture run to the hyperlink
     Then the hyperlink contains the picture after saving

  Scenario: Reject an invalid run without changing the hyperlink
    Given an existing hyperlink for authoring
     When I try to append a run with a missing character style
     Then the hyperlink's runs remain unchanged
