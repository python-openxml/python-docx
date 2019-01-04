Feature: Header and footer behaviors
  In order to control the appearance of page headers and footers
  As a developer using python-docx
  I need properties and methods on _Header and _Footer objects


  Scenario Outline: _Header.is_linked_to_previous getter
    Given a _Header object <with-or-no> header definition as header
     Then header.is_linked_to_previous is <value>

    Examples: _Header.is_linked_to_previous states
      | with-or-no | value |
      | with a     | False |
      | with no    | True  |


  Scenario Outline: _Header.is_linked_to_previous setter
    Given a _Header object <with-or-no> header definition as header
     When I assign <value> to header.is_linked_to_previous
     Then header.is_linked_to_previous is <value>

    Examples: _Header.is_linked_to_previous state changes
      | with-or-no | value |
      | with a     | True  |
      | with no    | False |
      | with a     | False |
      | with no    | True  |


  Scenario: _Header inherits content
    Given a _Header object with a header definition as header
      And the next _Header object with no header definition as header_2
     Then header_2.paragraphs[0].text == header.paragraphs[0].text
      And header_2.is_linked_to_previous is True


  Scenario: _Header text accepts style assignment
    Given a _Header object with a header definition as header
     When I assign "Normal" to header.paragraphs[0].style
     Then header.paragraphs[0].style.name == "Normal"


  Scenario: _Header allows image insertion
    Given a _Run object from a header as run
     When I call run.add_picture()
     Then I can't detect the image but no exception is raised


  Scenario Outline: _Footer.is_linked_to_previous getter
    Given a _Footer object <with-or-no> footer definition as footer
     Then footer.is_linked_to_previous is <value>

    Examples: _Footer.is_linked_to_previous states
      | with-or-no | value |
      | with a     | False |
      | with no    | True  |


  Scenario Outline: _Footer.is_linked_to_previous setter
    Given a _Footer object <with-or-no> footer definition as footer
     When I assign <value> to footer.is_linked_to_previous
     Then footer.is_linked_to_previous is <value>

    Examples: _Footer.is_linked_to_previous state changes
      | with-or-no | value |
      | with a     | True  |
      | with no    | False |
      | with a     | False |
      | with no    | True  |


  Scenario: _Footer inherits content
    Given a _Footer object with a footer definition as footer
      And the next _Footer object with no footer definition as footer_2
     Then footer_2.paragraphs[0].text == footer.paragraphs[0].text
      And footer_2.is_linked_to_previous is True


  Scenario: _Footer text accepts style assignment
    Given a _Footer object with a footer definition as footer
     When I assign "Normal" to footer.paragraphs[0].style
     Then footer.paragraphs[0].style.name == "Normal"


  Scenario: _Footer allows image insertion
    Given a _Run object from a footer as run
     When I call run.add_picture()
     Then I can't detect the image but no exception is raised
