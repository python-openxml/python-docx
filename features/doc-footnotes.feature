Feature: Create editable native footnotes
  As a document author
  I need references placed deliberately and editable note content

  Scenario: Save a formatted note between existing runs
    Given a document with a native footnote between existing runs
     When I save and reopen the footnote document
     Then the reference position and formatted note content are preserved
