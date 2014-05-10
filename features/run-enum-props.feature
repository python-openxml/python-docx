Feature: Query or apply enumerated run property
  In order to query or change an enumerated font property of a word or phrase
  As a python-docx developer
  I need a way to query and set the enumerated properties on a run


  Scenario Outline: Get underline value of a run
    Given a run having <underline-type> underline
     Then the run underline property value is <underline-value>

    Examples: underline property values
      | underline-type | underline-value     |
      | inherited      | None                |
      | no             | False               |
      | single         | True                |
      | double         | WD_UNDERLINE.DOUBLE |


  Scenario Outline: Change underline setting for a run
    Given a run having <underline-type> underline
     When I set the run underline to <new-underline-value>
     Then the run underline property value is <expected-underline-value>

    Examples: underline property values
      | underline-type | new-underline-value | expected-underline-value |
      | inherited      | True                | True                     |
      | inherited      | False               | False                    |
      | inherited      | None                | None                     |
      | inherited      | WD_UNDERLINE.SINGLE | True                     |
      | inherited      | WD_UNDERLINE.DOUBLE | WD_UNDERLINE.DOUBLE      |
      | single         | None                | None                     |
      | single         | True                | True                     |
      | single         | False               | False                    |
      | single         | WD_UNDERLINE.SINGLE | True                     |
      | single         | WD_UNDERLINE.DOUBLE | WD_UNDERLINE.DOUBLE      |
