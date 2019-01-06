Feature: Access and change section properties
  In order to discover and modify document section behaviors
  As a developer using python-docx
  I need a way to get and set the properties of a section


  Scenario Outline: Section.different_first_page_header_footer getter
    Given a Section object <with-or-without> a distinct first-page header as section
     Then section.different_first_page_header_footer is <value>

    Examples: Section.different_first_page_header_footer states
      | with-or-without | value |
      | with            | True  |
      | without         | False |


  Scenario Outline: Section.different_first_page_header_footer setter
    Given a Section object <with-or-without> a distinct first-page header as section
     When I assign <value> to section.different_first_page_header_footer
     Then section.different_first_page_header_footer is <value>

    Examples: Section.different_first_page_header_footer assignment cases
      | with-or-without | value |
      | with            | True  |
      | with            | False |
      | without         | True  |
      | without         | False |


  Scenario: Section.even_page_footer
    Given a Section object as section
     Then section.even_page_footer is a _Footer object


  Scenario: Section.even_page_header
    Given a Section object as section
     Then section.even_page_header is a _Header object


  Scenario: Section.first_page_footer
    Given a Section object as section
     Then section.first_page_footer is a _Footer object


  Scenario: Section.first_page_header
    Given a Section object as section
     Then section.first_page_header is a _Header object


  Scenario: Section.footer
    Given a Section object as section
     Then section.footer is a _Footer object


  Scenario: Section.header
    Given a Section object as section
     Then section.header is a _Header object


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


  Scenario: Get section page size
    Given a section having known page dimension
     Then the reported page width is 8.5 inches
      And the reported page height is 11 inches


  Scenario: Set section page size
    Given a section having known page dimension
     When I set the section page width to 11 inches
      And I set the section page height to 8.5 inches
     Then the reported page width is 11 inches
      And the reported page height is 8.5 inches


  Scenario Outline: Get section orientation
    Given a section known to have <orientation> orientation
     Then the reported page orientation is <reported-orientation>

    Examples: Section page orientations
      | orientation | reported-orientation |
      | landscape   | WD_ORIENT.LANDSCAPE  |
      | portrait    | WD_ORIENT.PORTRAIT   |


  Scenario Outline: Set section orientation
    Given a section known to have <initial-orientation> orientation
     When I set the section orientation to <new-orientation>
     Then the reported page orientation is <reported-orientation>

    Examples: Section page orientations
      | initial-orientation | new-orientation      |  reported-orientation |
      | portrait            | WD_ORIENT.LANDSCAPE  |  WD_ORIENT.LANDSCAPE  |
      | landscape           | WD_ORIENT.PORTRAIT   |  WD_ORIENT.PORTRAIT   |
      | landscape           | None                 |  WD_ORIENT.PORTRAIT   |


  Scenario: Get section page margins
    Given a section having known page margins
     Then the reported left margin is 1.0 inches
      And the reported right margin is 1.25 inches
      And the reported top margin is 1.5 inches
      And the reported bottom margin is 1.75 inches
      And the reported gutter margin is 0.25 inches
      And the reported header margin is 0.5 inches
      And the reported footer margin is 0.75 inches


  Scenario Outline: Set section page margins
    Given a section having known page margins
     When I set the <margin-type> margin to <length> inches
     Then the reported <margin-type> margin is <length> inches

    Examples: Section margin settings
      | margin-type | length |
      | left        |  1.0   |
      | right       |  1.25  |
      | top         |  0.75  |
      | bottom      |  1.5   |
      | header      |  0.25  |
      | footer      |  0.5   |
      | gutter      |  0.25  |
