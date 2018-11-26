# Created by Ondrej at 18/11/2018
Feature: Access and change header properties
  In order to discover and modify document header behaviors
  As a developer using python-docx
  I need a way to get and set the properties of a header

  Scenario Outline: Get is linked to previous property
    Given a header having <a-or-no> is_linked_to_previous property
    Then document.sections[-1].header.is_linked_to_previous is <value>

    Examples: Even and odd headers settings values
      | a-or-no | value |
      | a       | True  |
      | no      | False |