# Created by Ondrej at 18/11/2018
Feature: Access all types of headers and footers (default, first, even)
  In order to discover and modify section header access
  As a developer using python-docx
  I need a way to get headers of sections

  Scenario: Access header of all types
    Given a section with all header types
    Then header, first_page_header, even_odd_header is present in document.section

  Scenario: Access footer of all types
    Given a section with all footer types
    Then footer, first_page_footer, even_odd_footer is present in document.section