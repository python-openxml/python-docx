Feature: Get or set paragraph formatting properties
  In order to customize the formatting of paragraphs in a document
  As a python-docx developer
  I need a ParagraphFormat object with read/write formatting properties


  Scenario: Get tab stops
    Given a paragraph format
     Then paragraph_format.tab_stops is a TabStops object


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


  Scenario Outline: Get line spacing
    Given a paragraph format having <setting> line spacing
     Then paragraph_format.line_spacing is <value>
     Then paragraph_format.line_spacing_rule is <rule-value>

    Examples: paragraph_format.line_spacing values
      | setting   | value  | rule-value               |
      | inherited | None   | None                     |
      | 14 pt     | 177800 | WD_LINE_SPACING.EXACTLY  |
      | double    | 2.0    | WD_LINE_SPACING.DOUBLE   |


  Scenario Outline: Set line spacing
    Given a paragraph format having <setting> line spacing
     When I assign <new-value> to paragraph_format.line_spacing
     Then paragraph_format.line_spacing is <value>
     Then paragraph_format.line_spacing_rule is <rule-value>

    Examples: paragraph_format.line_spacing assignment results
      | setting   | new-value | value  | rule-value                     |
      | inherited | Pt(14)    | 177800 | WD_LINE_SPACING.EXACTLY        |
      | 14 pt     | 2         | 2.0    | WD_LINE_SPACING.DOUBLE         |
      | double    | 1.75      | 1.75   | WD_LINE_SPACING.MULTIPLE       |
      | inherited | 1.0       | 1.0    | WD_LINE_SPACING.SINGLE         |
      | 14 pt     | 1.5       | 1.5    | WD_LINE_SPACING.ONE_POINT_FIVE |


  Scenario Outline: Set line spacing rule
    Given a paragraph format having <setting> line spacing
     When I assign <new-value> to paragraph_format.line_spacing_rule
     Then paragraph_format.line_spacing is <value>
     Then paragraph_format.line_spacing_rule is <rule-value>

    Examples: paragraph_format.line_spacing_rule assignment results
      | setting | new-value                | value  | rule-value               |
      | 14 pt   | WD_LINE_SPACING.DOUBLE   | 2.0    | WD_LINE_SPACING.DOUBLE   |
      | double  | WD_LINE_SPACING.SINGLE   | 1.0    | WD_LINE_SPACING.SINGLE   |
      | 14 pt   | WD_LINE_SPACING.AT_LEAST | 177800 | WD_LINE_SPACING.AT_LEAST |
      | 14 pt   | None                     | 1.1666 | WD_LINE_SPACING.MULTIPLE |


  Scenario Outline: Get paragraph indents
    Given a paragraph format having <type> indent of <setting>
     Then paragraph_format.<type>_indent is <value>

    Examples: paragraph_format indent values
      | type       | setting  | value   |
      | first_line | inherit  | None    |
      | first_line | 18 pt    | 228600  |
      | first_line | -17.3 pt | -219710 |
      | left       | inherit  | None    |
      | left       | 46.1 pt  | 585470  |
      | right      | inherit  | None    |
      | right      | 17.3 pt  | 219710  |


  Scenario Outline: Set paragraph indents
    Given a paragraph format having <type> indent of <setting>
     When I assign <new-value> to paragraph_format.<type>_indent
     Then paragraph_format.<type>_indent is <value>

    Examples: paragraph_format indent assignment results
      | type       | setting  | new-value | value   |
      | first_line | inherit  | 18 pt     | 228600  |
      | first_line | 18 pt    | -18 pt    | -228600 |
      | first_line | -17.3 pt | None      | None    |
      | left       | inherit  | 36 pt     | 457200  |
      | left       | 46.1 pt  | -12 pt    | -152400 |
      | left       | 46.1 pt  | None      | None    |
      | right      | inherit  | 24 pt     | 304800  |
      | right      | 17.3 pt  | -6 pt     | -76200  |
      | right      | 17.3 pt  | None      | None    |


  Scenario Outline: Get On/Off paragraph property
    Given a paragraph format having <prop-name> set <state>
     Then paragraph_format.<prop-name> is <value>

    Examples: ParagraphFormat On/Off property values
      | prop-name         | state      | value |
      | keep_together     | to inherit | None  |
      | keep_together     | On         | True  |
      | keep_together     | Off        | False |
      | keep_with_next    | to inherit | None  |
      | keep_with_next    | On         | True  |
      | keep_with_next    | Off        | False |
      | page_break_before | to inherit | None  |
      | page_break_before | On         | True  |
      | page_break_before | Off        | False |
      | widow_control     | to inherit | None  |
      | widow_control     | On         | True  |
      | widow_control     | Off        | False |


  Scenario Outline: Set On/Off paragraph property
    Given a paragraph format having <prop-name> set <state>
     When I assign <new-value> to paragraph_format.<prop-name>
     Then paragraph_format.<prop-name> is <value>

    Examples: ParagraphFormat On/Off property values
      | prop-name         | state      | new-value | value |
      | keep_together     | to inherit |   True    | True  |
      | keep_together     | On         |   False   | False |
      | keep_together     | Off        |   None    | None  |
      | keep_with_next    | to inherit |   False   | False |
      | keep_with_next    | Off        |   True    | True  |
      | keep_with_next    | On         |   None    | None  |
      | page_break_before | to inherit |   True    | True  |
      | page_break_before | On         |   False   | False |
      | page_break_before | Off        |   None    | None  |
      | widow_control     | to inherit |   False   | False |
      | widow_control     | Off        |   True    | True  |
      | widow_control     | On         |   None    | None  |
