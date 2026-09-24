Feature: Configure theme fonts
  In order to change heading and body fonts together
  As a document author
  I want styles to inherit from the document theme

  Scenario: Save and reopen a document with theme-based heading and body fonts
    Given a document with theme-based heading and body styles
    When I set its theme fonts to Aptos Display and Aptos and reopen it
    Then its heading and body styles still reference the theme
    And its theme fonts are Aptos Display and Aptos
