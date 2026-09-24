Feature: Configure repeating table header rows
  Scenario: Save and clear the direct setting
    Given a table with two leading header rows
     When I save and reopen the repeating-header document
     Then both leading rows remain headers and the body remains unmarked
