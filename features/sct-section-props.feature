Feature: Access and change section properties
  In order to discover and modify document section behaviors
  As a developer using python-docx
  I need a way to get and set the properties of a section


  Scenario Outline: Get section start type
    Given a section having start type <start-type>
     Then the reported section start type is <start-type>

    Examples: Section start types
      | start-type |
      | CONTINUOUS |
      | NEW_COLUMN |
      | NEW_PAGE   |
      | EVEN_PAGE  |
      | ODD_PAGE   |


  Scenario Outline: Set section start type
    Given a section having start type <initial-start-type>
     When I set the section start type to <new-start-type>
     Then the reported section start type is <reported-start-type>

    Examples: Section start types
      | initial-start-type | new-start-type | reported-start-type |
      | CONTINUOUS         | NEW_PAGE       | NEW_PAGE            |
      | NEW_PAGE           | ODD_PAGE       | ODD_PAGE            |
      | NEW_COLUMN         | None           | NEW_PAGE            |


  Scenario: Get section page width
    Given a section having known page dimension
     Then the reported page width is 8.5 inches
      And the reported page height is 11 inches
