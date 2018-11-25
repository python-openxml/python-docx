# Created by Ondrej at 18/11/2018
Feature: Access and change settings properties
  In order to discover and modify document settings behaviors
  As a developer using python-docx
  I need a way to get and set the properties of a settings

  Scenario Outline: Get even and odd headers settings
    Given a settings having <a-or-no> even and odd headers settings
    Then document.settings.odd_and_even_pages_header_footer is <value>

    Examples: Even and odd headers settings values
      | a-or-no | value |
      | a       | True  |
      | no      | False |