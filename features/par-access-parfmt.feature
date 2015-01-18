Feature: Access paragraph format
  In order to get or change the formatting of a paragraph
  As a developer using python-docx
  I need access to the paragraph format of a paragraph


  Scenario: Get paragraph format object
    Given a paragraph
     Then paragraph.paragraph_format is its ParagraphFormat object
