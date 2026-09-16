Feature: Read and change hyperlink tooltips
  In order to provide hover text for a hyperlink
  As a developer using python-docx
  I need to distinguish absent, empty, and populated tooltips

  Scenario: Read an absent tooltip
    Given a hyperlink authoring paragraph in a body
     When I create a hyperlink without an initial label
     Then the hyperlink has no tooltip

  Scenario Outline: Set or clear a tooltip
    Given a hyperlink authoring paragraph in a body
     When I create a hyperlink without an initial label
      And I assign a <value> tooltip to the hyperlink
     Then the assigned tooltip survives saving

    Examples:
      | value     |
      | populated |
      | empty     |
      | absent    |

  Scenario: Reject invalid tooltip characters
    Given a hyperlink authoring paragraph in a body
     When I create a hyperlink without an initial label
      And I try to assign a tooltip containing invalid XML characters
     Then the previous tooltip is preserved
