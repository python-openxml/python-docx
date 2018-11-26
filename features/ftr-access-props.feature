# Created by Ondrej at 18/11/2018
Feature: Access and change footer properties
  In order to discover and modify document footer behaviors
  As a developer using python-docx
  I need a way to get and set the properties of a footer

  Scenario Outline: Get is linked to previous property
    Given a footer having <a-or-no> is_linked_to_previous property
    Then document.sections[-1].footer.is_linked_to_previous is <value>

    Examples: Even and odd footers settings values
      | a-or-no | value |
      | a       | True  |
      | no      | False |