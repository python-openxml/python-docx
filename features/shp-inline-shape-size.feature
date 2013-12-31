Feature: Query and change dimensions of inline shape
  In order to adjust the display size of an inline shape
  As a python-docx developer
  I need to query and change the width and height of an inline shape

  Scenario: Query inline shape dimensions
    Given an inline shape of known dimensions
     Then the dimensions of the inline shape match the known values

  Scenario: Change inline shape dimensions
    Given an inline shape of known dimensions
     When I change the dimensions of the inline shape
     Then the dimensions of the inline shape match the new values
