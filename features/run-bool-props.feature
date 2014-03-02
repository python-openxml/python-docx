Feature: Query or apply boolean property to a run
  In order to query or change a boolean display property of a word or phrase
  As a python-docx developer
  I need a way to query and set the boolean properties on a run

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
