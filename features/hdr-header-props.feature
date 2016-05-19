Feature: Header properties
  In order to interact with document headers
  As a developer using python-docx
  I need read/write properties on the Header object


  Scenario Outline: Get Header.is_linked_to_previous
    Given a header <having-or-no> definition
     Then header.is_linked_to_previous is <value>

    Examples: Header.is_linked_to_previous states
      | having-or-no | value |
      | having a     | False |
      | having no    | True  |
