Feature: Get or set font properties
  In order to customize the character formatting of text in a document
  As a python-docx developer
  I need a set of read/write properties on the Font object


  Scenario Outline: Get highlight color
    Given a font having <color> highlighting 
     Then font.highlight_color is <value>

    Examples: font.highlight_color values
      | color           | value        |
      | no              | None         |
      | yellow          | YELLOW       |
      | bright green    | BRIGHT_GREEN |


  Scenario Outline: Set highlight color
    Given a font having <color> highlighting
     When I assign <value> to font.highlight_color
     Then font.highlight_color is <value>

    Examples: font.highlight_color values
      | color           | value        |
      | no              | YELLOW       |
      | yellow          | None         |
      | bright green    | BRIGHT_GREEN |
      
      
  Scenario Outline: Get typeface name
    Given a font having typeface name <name>
     Then font.name is <value>

    Examples: font.name values
      | name          | value        |
      | not specified | None         |
      | Avenir Black  | Avenir Black |


  Scenario Outline: Set typeface name
    Given a font having typeface name <name>
     When I assign <value> to font.name
     Then font.name is <value>

    Examples: font.name values
      | name          | value        |
      | not specified | Avenir Black |
      | Avenir Black  | Calibri      |
      | Avenir Black  | None         |


  Scenario Outline: Get font size
    Given a font of size <size>
     Then font.size is <value>

    Examples: font.size values
      | size        | value  |
      | unspecified | None   |
      | 14 pt       | 177800 |


  Scenario Outline: Set font size
    Given a font of size <size>
     When I assign <value> to font.size
     Then font.size is <value>

    Examples: font.size post-assignment values
      | size        | value  |
      | unspecified | 177800 |
      | 14 pt       | 228600 |
      | 18 pt       | None   |


  Scenario: Get font color object
    Given a font
     Then font.color is a ColorFormat object


  Scenario Outline: Get font underline value
    Given a font having <underline-type> underline
     Then font.underline is <value>

    Examples: font underline values
      | underline-type | value               |
      | inherited      | None                |
      | no             | False               |
      | single         | True                |
      | double         | WD_UNDERLINE.DOUBLE |


  Scenario Outline: Change font underline
    Given a font having <underline-type> underline
     When I assign <new-value> to font.underline
     Then font.underline is <expected-value>

    Examples: underline property values
      | underline-type | new-value           | expected-value      |
      | inherited      | True                | True                |
      | inherited      | False               | False               |
      | inherited      | None                | None                |
      | inherited      | WD_UNDERLINE.SINGLE | True                |
      | inherited      | WD_UNDERLINE.DOUBLE | WD_UNDERLINE.DOUBLE |
      | single         | None                | None                |
      | single         | True                | True                |
      | single         | False               | False               |
      | single         | WD_UNDERLINE.SINGLE | True                |
      | single         | WD_UNDERLINE.DOUBLE | WD_UNDERLINE.DOUBLE |


  Scenario Outline: Get font sub/superscript value
    Given a font having <vertAlign-state> vertical alignment
     Then font.subscript is <sub-value>
      And font.superscript is <super-value>

    Examples: font sub/superscript values
      | vertAlign-state | sub-value | super-value |
      | inherited       | None      | None        |
      | subscript       | True      | False       |
      | superscript     | False     | True        |


  Scenario Outline: Change font sub/superscript
    Given a font having <vertAlign-state> vertical alignment
     When I assign <value> to font.<name>script
     Then font.<name-2>script is <expected-value>

    Examples: value of sub/superscript after assignment
      | vertAlign-state | name  | value | name-2  | expected-value |
      | inherited       | sub   | True  |  sub    | True           |
      | inherited       | sub   | True  |  super  | False          |
      | inherited       | sub   | False |  sub    | None           |
      | inherited       | super | True  |  super  | True           |
      | inherited       | super | True  |  sub    | False          |
      | inherited       | super | False |  super  | None           |
      | subscript       | sub   | True  |  sub    | True           |
      | subscript       | sub   | False |  sub    | None           |
      | subscript       | sub   | None  |  sub    | None           |
      | subscript       | super | True  |  sub    | False          |
      | subscript       | super | False |  sub    | True           |
      | subscript       | super | None  |  sub    | None           |
      | superscript     | super | True  |  super  | True           |
      | superscript     | super | False |  super  | None           |
      | superscript     | super | None  |  super  | None           |
      | superscript     | sub   | True  |  super  | False          |
      | superscript     | sub   | False |  super  | True           |
      | superscript     | sub   | None  |  super  | None           |


  Scenario Outline: Apply boolean property to a run
    Given a run
     When I assign True to its <boolean_prop_name> property
     Then the run appears in <boolean_prop_name> unconditionally

    Examples: Boolean run properties
      | boolean_prop_name |
      | all_caps          |
      | bold              |
      | complex_script    |
      | cs_bold           |
      | cs_italic         |
      | double_strike     |
      | emboss            |
      | hidden            |
      | italic            |
      | imprint           |
      | math              |
      | no_proof          |
      | outline           |
      | rtl               |
      | shadow            |
      | small_caps        |
      | snap_to_grid      |
      | spec_vanish       |
      | strike            |
      | web_hidden        |


  Scenario Outline: Set <boolean_prop_name> off unconditionally
    Given a run
     When I assign False to its <boolean_prop_name> property
     Then the run appears without <boolean_prop_name> unconditionally

    Examples: Boolean run properties
      | boolean_prop_name |
      | all_caps          |
      | bold              |
      | complex_script    |
      | cs_bold           |
      | cs_italic         |
      | double_strike     |
      | emboss            |
      | hidden            |
      | italic            |
      | imprint           |
      | math              |
      | no_proof          |
      | outline           |
      | rtl               |
      | shadow            |
      | small_caps        |
      | snap_to_grid      |
      | spec_vanish       |
      | strike            |
      | web_hidden        |


  Scenario Outline: Remove boolean property from a run
    Given a run having <boolean_prop_name> set on
     When I assign None to its <boolean_prop_name> property
     Then the run appears with its inherited <boolean_prop_name> setting

    Examples: Boolean run properties
      | boolean_prop_name |
      | all_caps          |
      | bold              |
      | complex_script    |
      | cs_bold           |
      | cs_italic         |
      | double_strike     |
      | emboss            |
      | hidden            |
      | italic            |
      | imprint           |
      | math              |
      | no_proof          |
      | outline           |
      | rtl               |
      | shadow            |
      | small_caps        |
      | snap_to_grid      |
      | spec_vanish       |
      | strike            |
      | web_hidden        |
