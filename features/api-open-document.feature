Feature: Open a document
  In order work on a document
  As a developer using python-docx
  I need a way to open a document


  Scenario: Open a specified document
    Given I have python-docx installed
     When I call docx.Document() with the path of a .docx file
     Then document is a Document object


  Scenario: Open the default document
    Given I have python-docx installed
     When I call docx.Document() with no arguments
     Then document is a Document object


  Scenario Outline: Open a macro-enabled document or a template
    Given I have python-docx installed
     When I call docx.Document() with the path of a <ext> file
     Then document is a Document object

    Examples: Word file kinds
      | ext   |
      | .docm |
      | .dotx |
      | .dotm |


  Scenario Outline: Save a macro-enabled document or a template
    Given a document opened from a <ext> file
     When I save and reload the document
     Then the document part content type is the <ext> content type
      And the VBA project part is preserved: <has-vba>

    Examples: Word file kinds
      | ext   | has-vba |
      | .docm | True    |
      | .dotx | False   |
      | .dotm | True    |
