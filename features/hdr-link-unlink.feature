Feature: Link header of section
  In order link header to section
  As a developer using python-docx
  I need a way to link header in one step


  Scenario Outline: Link and unlink header to section
    Given a document section having header
    When I set header to <value>
    Then a section header is_linked to previous is <value>

    Examples: Header values
      | value |
      | True  |
      | False |
