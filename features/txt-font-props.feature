Feature: Get or set font properties
  In order to customize the character formatting of text in a document
  As a python-docx developer
  I need a set of read/write properties on the Font object


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


  @wip
  Scenario Outline: Get font underline value
    Given a font having <underline-type> underline
     Then font.underline is <value>

    Examples: font underline values
      | underline-type | value               |
      | inherited      | None                |
      | no             | False               |
      | single         | True                |
      | double         | WD_UNDERLINE.DOUBLE |


  @wip
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
