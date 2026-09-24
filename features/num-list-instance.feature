Feature: Author independent list sequences
  In order to control native Word numbering without editing XML
  As a document author
  I need independent lists and unnumbered continuation paragraphs

  Scenario: Start, continue, and restart a numbered list
    Given a document with an independent list starting at three
     When I add two items with an intervening paragraph
      And I restart the list at one
      And I save and reopen the list document
     Then the items retain their separate numbering identities

  Scenario: Add an unnumbered continuation paragraph
    Given a document with an independent list starting at three
     When I add an item with an unnumbered continuation
      And I save and reopen the list document
     Then the continuation retains text alignment without a number
