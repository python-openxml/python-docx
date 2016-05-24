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

  @wip
  Scenario: Get Header.body
    Given a header having a definition
     Then header.body is a BlockItemContainer object
      And header.body contains the text of the header
