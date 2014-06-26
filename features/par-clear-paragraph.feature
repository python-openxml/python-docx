Feature: Clear paragraph content
  In order to change paragraph content while retaining its formatting
  As a developer using python-docx
  I need a way to remove the content of a paragraph


  Scenario: Clear paragraph content
    Given a paragraph with content and formatting
     When I clear the paragraph content
     Then the paragraph has no content
      But the paragraph formatting is preserved
