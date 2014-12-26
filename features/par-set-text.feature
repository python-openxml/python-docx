Feature: Replace paragraph text
  In order to conveniently change the text of a paragraph in place
  As a developer using python-docx
  I need a writable text property on paragraph


  Scenario: Set paragraph text
    Given a paragraph with content and formatting
     When I set the paragraph text
     Then the paragraph has the text I set
      And the paragraph formatting is preserved
