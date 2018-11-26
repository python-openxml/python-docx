Feature: Link footer of section
  In order link footer to section
  As a developer using python-docx
  I need a way to link footer in one step


  Scenario Outline: Link and unlink footer to section
    Given a document section having footer
    When I set footer to <value>
    Then a section footer is_linked to previous is <value>

    Examples: Footer values
      | value |
      | True  |
      | False |
