Feature: Get or set paragraph formatting properties
  In order to customize the formatting of paragraphs in a document
  As a python-docx developer
  I need a ParagraphFormat object with read/write formatting properties


  Scenario Outline: Get paragraph alignment
    Given a paragraph format having <align-type> alignment
     Then paragraph_format.alignment is <value>

    Examples: paragraph_format.alignment values
      | align-type | value                     |
      | inherited  | None                      |
      | center     | WD_ALIGN_PARAGRAPH.CENTER |
      | right      | WD_ALIGN_PARAGRAPH.RIGHT  |


  Scenario Outline: Set paragraph alignment
    Given a paragraph format having <align-type> alignment
     When I assign <new-value> to paragraph_format.alignment
     Then paragraph_format.alignment is <value>

    Examples: paragraph_format.alignment assignment results
      | align-type | new-value                 | value                     |
      | inherited  | WD_ALIGN_PARAGRAPH.CENTER | WD_ALIGN_PARAGRAPH.CENTER |
      | center     | WD_ALIGN_PARAGRAPH.RIGHT  | WD_ALIGN_PARAGRAPH.RIGHT  |
      | right      | None                      | None                      |


  Scenario Outline: Get paragraph spacing
    Given a paragraph format having <setting> space <side>
     Then paragraph_format.space_<side> is <value>

    Examples: paragraph_format spacing values
      | side   | setting   | value  |
      | before | inherited | None   |
      | before | 24 pt     | 304800 |
      | after  | inherited | None   |
      | after  | 42 pt     | 533400 |


  @wip
  Scenario Outline: Set paragraph spacing
    Given a paragraph format having <setting> space <side>
     When I assign <new-value> to paragraph_format.space_<side>
     Then paragraph_format.space_<side> is <value>

    Examples: paragraph_format spacing assignment results
      | side   | setting   | new-value | value  |
      | before | inherited | Pt(12)    | 152400 |
      | before | 24 pt     | Pt(18)    | 228600 |
      | before | 24 pt     | None      | None   |
      | after  | inherited | Pt(12)    | 152400 |
      | after  | 42 pt     | Pt(18)    | 228600 |
      | after  | 42 pt     | None      | None   |
