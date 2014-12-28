Feature: Delete a style
  In order to customize the available styles in a document
  As a developer using python-docx
  I need a way to delete a style


  Scenario: Delete a style
    Given a document having known styles
     When I delete a style
     Then the document has one fewer styles
      And the deleted style is not in the styles collection
