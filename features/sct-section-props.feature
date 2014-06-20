Feature: Access and change section properties
  In order to discover and modify document section behaviors
  As a developer using python-docx
  I need a way to get and set the properties of a section


  @wip
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
