Feature: Get or set paragraph alignment
  In order to specify the justification of a paragraph
  As a python-docx developer
  I need a read/write alignment property on paragraph objects


  Scenario Outline: Get paragraph alignment
    Given a paragraph having <align-type> alignment
     Then the paragraph alignment property value is <align-value>

    Examples: align property values
      | align-type | align-value               |
      | inherited  | None                      |
      | left       | WD_ALIGN_PARAGRAPH.LEFT   |
      | center     | WD_ALIGN_PARAGRAPH.CENTER |
      | right      | WD_ALIGN_PARAGRAPH.RIGHT  |
