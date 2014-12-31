Feature: Get or set paragraph formatting properties
  In order to customize the formatting of paragraphs in a document
  As a python-docx developer
  I need a ParagraphFormat object with read/write formatting properties


  @wip
  Scenario Outline: Get paragraph alignment
    Given a paragraph format having <align-type> alignment
     Then paragraph_format.alignment is <value>

    Examples: paragraph_format.alignment values
      | align-type | value                     |
      | inherited  | None                      |
      | center     | WD_ALIGN_PARAGRAPH.CENTER |
      | right      | WD_ALIGN_PARAGRAPH.RIGHT  |


  @wip
  Scenario Outline: Set paragraph alignment
    Given a paragraph format having <align-type> alignment
     When I assign <new-value> to paragraph_format.alignment
     Then paragraph_format.alignment is <value>

    Examples: paragraph_format.alignment assignment results
      | align-type | new-value                 | value                     |
      | inherited  | WD_ALIGN_PARAGRAPH.CENTER | WD_ALIGN_PARAGRAPH.CENTER |
      | center     | WD_ALIGN_PARAGRAPH.RIGHT  | WD_ALIGN_PARAGRAPH.RIGHT  |
      | right      | None                      | None                      |
