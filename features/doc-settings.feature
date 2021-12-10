Feature: Document.settings
  In order to operate on document-level settings
  As a developer using python-docx
  I need access to settings to the Settings object for the document
  And I need properties and methods on Settings


  Scenario Outline: Access document settings
    Given a document having <a-or-no> settings part
     Then document.settings is a Settings object

    Examples: having a settings part or not
      | a-or-no   |
      | a         |
      | no        |


  Scenario Outline: Settings.odd_and_even_pages_header_footer getter
    Given a Settings object <with-or-without> odd and even page headers as settings
     Then settings.odd_and_even_pages_header_footer is <value>

    Examples: Settings.odd_and_even_pages_header_footer states
      | with-or-without | value |
      | with            | True  |
      | without         | False |


  Scenario Outline: Settings.odd_and_even_pages_header_footer setter
    Given a Settings object <with-or-without> odd and even page headers as settings
     When I assign <value> to settings.odd_and_even_pages_header_footer
     Then settings.odd_and_even_pages_header_footer is <value>

    Examples: Settings.odd_and_even_pages_header_footer assignment cases
      | with-or-without | value |
      | with            | True  |
      | with            | False |
      | without         | True  |
      | without         | False |
