Feature: Access section headers and footers
  In order to operate on the headers or footers of a section
  As a developer using python-docx
  I need access to the section headers and footers


  Scenario: Access default header of section
    Given a section
     Then section.header is a Header object
